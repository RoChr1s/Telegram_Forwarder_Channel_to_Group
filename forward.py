import logging
from telethon import events


async def forward_to_group(client, event, group_id, filter_words):
    """Forward message to the group if it contains filter words."""
    try:
        # Check if message contains filter words
        if all(word.lower() in event.message.message.lower() for word in filter_words):
            # Find the group to forward the message to, ignoring case
            group = await client.get_entity(group_id)
            # Forward message to group
            await client.forward_messages(group.id, event.message)
            # Log success message
            logging.info('Valid message forwarded!')
            print('Valid message forwarded!')
        else:
            # Log not valid message
            logging.info('Invalid message arrived!')
            print('Invalid message, ignored!')
    except ValueError as e:
        # Raise exception if invalid group ID
        raise ValueError(f'Invalid group ID: {group_id}') from e
    except Exception as e:
        # Raise exception if error forwarding message
        raise Exception(f'Error forwarding message: {e}') from e
