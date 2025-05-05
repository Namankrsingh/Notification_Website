# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'notification_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     # async def receive(self, text_data):
#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json['message']

#     #     # Send message to room group
#     #     await self.channel_layer.group_send(
#     #         self.room_group_name,
#     #         {
#     #             'type': 'chat_message',
#     #             'message': message
#     #         }
#     #     )

#     # Receive message from room group
#     async def send_notification(self, event):
#         message = json.loads(event['message'])

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps(message))


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Dynamically get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"notification_{self.room_name}"

        # Join the room group (this allows multiple WebSocket clients to join the same "room")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Handle receiving a message from WebSocket
    async def receive(self, text_data):
        # Parse the incoming WebSocket message (JSON format)
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Send the message to the room group via channel layer
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',  # Custom message handler
                'message': message
            }
        )

    # Handle the 'send_notification' event from the channel layer
    async def send_notification(self, event):
        # Extract the message from the event (this comes from the group_send)
        message = event['message']

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps({
            'message': message
        }))
