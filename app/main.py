from fastapi import FastAPI, UploadFile, File, HTTPException
import easyocr
import numpy as np
import cv2
from PIL import Image
import io
from pdf2image import convert_from_bytes

app = FastAPI(title="EasyOCR API")

# Load OCR model once
reader = easyocr.Reader(['en'], gpu=False)


def preprocess_image(image):
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return processed


def extract_text_from_image(image):
    processed = preprocess_image(image)
    results = reader.readtext(processed)
    return " ".join([res[1] for res in results])


@app.get("/")
def root():
    return {"message": "Clinivents Api Running 🚀"}


@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # 🖼️ Handle Images
        if file.content_type in ["image/png", "image/jpeg"]:
            image = Image.open(io.BytesIO(contents))
            text = extract_text_from_image(image)

            return {
                "filename": file.filename,
                "type": "image",
                "text": text
            }

        # 📄 Handle PDFs
        elif file.content_type == "application/pdf":
            images = convert_from_bytes(contents)

            all_text = []

            for page_number, image in enumerate(images):
                text = extract_text_from_image(image)
                all_text.append({
                    "page": page_number + 1,
                    "text": text
                })

            return {
                "filename": file.filename,
                "type": "pdf",
                "pages": all_text
            }

        else:
            raise HTTPException(
                status_code=400,
                detail="Only PNG, JPG, and PDF files are allowed"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))