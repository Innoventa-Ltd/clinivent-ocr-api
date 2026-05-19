from main import app
from asgiref.wsgi import WsgiToAsgi
from django.core.handlers.asgi import ASGIHandler

application = WsgiToAsgi(app)