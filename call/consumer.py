import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    '''
    webSocket consumer for handling real-time video call functionality.
    Manages user connections, call signaling, and ICE candidate exchange.
    '''
    async def connect(self):
        '''
        Handles initial webSocket connection.
        Accepts the connection and sends a confirmation message to the client.
        '''
        
        await self.accept()
        await self.send(
            text_data = json.dumps(
                {
                    'type': 'connection', 'data': {'message': 'connected'}
                }
            )
        )
    async def disconnect(self, close_code):
        '''
        Handles websocket disconnection.
        Removes the user from their associated channel group.
        '''
        await self.channel_layer.group_discard(self.my_name,self.channel_name)
        
    async def receive(self,text_data):
       '''
       processes incoming webSocket message from clients.
       Handles different types of events: login, call initiation, call answering, 
       and ICE candidates.
       '''     
       text_data_json = json.loads(text_data)
       eventType = text_data_json['type']
       
       if eventType == 'login':
           # handles usern login: Add user to their personal channel group
           name = text_data_json['data']['name']
           self.my_name = name
           
           await self.channel_layer.group_add(self.my_name, self)