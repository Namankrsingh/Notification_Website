# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channels_celery_project.settings')
# django.setup()

# from channels.auth import AuthMiddleware, AuthMiddlewareStack
# from notifications_app.routing import websocket_urlpatterns
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     )
# })

# asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from notifications_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channels_celery_project.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
        URLRouter(websocket_urlpatterns)  # Routing for WebSocket
    ),
})
