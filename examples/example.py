from configparser import ConfigParser
from slackclient import SlackClient
from .slackeventsapi import SlackEventsReactor


conf = ConfigParser()
conf.read('/etc/chmod777/tokens')  

VERIFY_TOKEN = conf.get('slack', 'verify') 
BOT_TOKEN = conf.get('slack', 'bot') 

slack_events = SlackEventsReactor(VERIFY_TOKEN)
slack_api = SlackClient(BOT_TOKEN)

# Declare events
@slack_events.hook('message')
def handle_message(data):
    message = data['event']
    if 'text' not in message:
        return
    if 'life is meaningless' in message['text']:
        slack_api.api_call(
                'chat.postMessage',
                channel=message['channel'],
                text='I agree!')
    else:
        slack_api.api_call(
                'reactions.add',
                name='thumbsdown',
                channel=message['channel'],
                timestamp=message['event_ts']
                )

# Start listening
slack_events.start()
