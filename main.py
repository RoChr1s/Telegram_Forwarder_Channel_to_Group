import logging
import time
import configparser
from telethon import TelegramClient, events
from forward import forward_to_group


# Read config
config = configparser.ConfigParser()
config.read('config.ini')

# Get telegram section
telegram_config = config['telegram']

# Get group ID and channel ID from config
group_id = telegram_config.getint('group_id')
channel_id = telegram_config.getint('channel_id')

# Get filter words from config
filter_words = telegram_config.get('filter_words', '').split(',')

# Set up logging
logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

# Set up Telegram client
api_id = telegram_config.getint('api_id')
api_hash = telegram_config['api_hash']
session_name = telegram_config['session_name']
client = TelegramClient(session_name, api_id, api_hash)


# Define event handler
@client.on(events.NewMessage(chats=channel_id))
async def new_message_handler(event):
    """Handle new messages in the channel."""
    await forward_to_group(client, event, group_id, filter_words)


async def main():
    # Start client
    await client.start()
    # Log client started message
    logging.info('Bot started')
    # Print start message
    print('Bot started!')
    # Run client until stopped
    await client.run_until_disconnected()


if __name__ == '__main__':
    # Start main function
    with client:
        client.loop.run_until_complete(main())
