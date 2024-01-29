import json
from telethon import TelegramClient

from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.types import Channel

api_id = 28258595
api_hash = '2d7104075fe614ced8bfed59c88f9623'
username = '@khaidoukova'

client = TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxCUSTOM")

client.start()


async def search_messages(channel, keywords, offset_msg):
    all_messages = []
    offset_file = f'offset_{channel}.txt'
    result_file = f'result_{channel}.json'

    # Получение объекта канала по username
    entity = await client.get_entity(channel)
    if not isinstance(entity, Channel):  # Проверка, что полученный объект является каналом
        print("Invalid channel username:", channel)
        return

    for word in keywords:

        async for message in client.iter_messages(entity, search=word, filter=InputMessagesFilterEmpty(),
                                                  offset_id=offset_msg):
            found_keywords = [keyword for keyword in keywords if keyword in (message.text or '')]
            if found_keywords:
                data = {
                    'message': message.text,
                    'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id': message.from_id.user_id if getattr(message.from_id, 'user_id', None) else None
                }
                print(data)
                all_messages.append(data)
            offset_msg = message.id

    with open(result_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False)

    with open(offset_file, 'w') as file:
        file.write(str(offset_msg))


async def main():
    channel = '@zakazyfreelance'
    keywords = ['python', 'дизайн']
    offset_file = f'offset_{channel}.txt'

    offset_msg = 0

    try:
        with open(offset_file, 'r') as file:
            offset_msg = int(file.read().strip())
    except FileNotFoundError:
        pass

    await search_messages(channel, keywords, offset_msg)
    await client.disconnect()


with client:
    client.loop.run_until_complete(main())
