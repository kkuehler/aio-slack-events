import asyncio 
from aiohttp import web 

from slackeventsapi.eventhandler import EventHandler

class SlackEventsReactor(EventHandler):

    def __init__(self, verify_token, endpoint='/slack/events'):
        super().__init__()
        
        self.app = web.Application()
        self.app.router.add_get(endpoint, self.bad_request) 
        self.app.router.add_post(endpoint, self.event_handler) 
        
        self.verify_token = verify_token

    def start(self, host='127.0.0.1', port=3000):
        web.run_app(self.app, host=host, port=port)

    async def bad_request(self, request):
        return web.Response(
                text='These are not the slackbots you are looking for...\n',
                status=404)

    async def event_handler(self, request): 
        event_data = await request.json()
        
        print(event_data)

        # Verify request
        if ('token' not in event_data or
                event_data['token'] != self.verify_token):
            return web.Response(
                    text='', 
                    status=404)
        
        # Initialize our server with Slack Events API 
        if 'challenge' in event_data:
            return web.Response(
                    text=event_data['challenge'],
                    status=200)
        
        # Trigger an event with the event data
        if ('event' in event_data and
                'bot_id' not in event_data['event']):
            super(SlackEventsReactor, self).trigger(event_data['event']['type'], event_data)

        return web.Response(text='', status=200)

