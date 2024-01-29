import json
from telethon.sync import TelegramClient
from datetime import date, datetime

from telethon.tl.functions.messages import GetHistoryRequest

api_id = 28258595
api_hash = '2d7104075fe614ced8bfed59c88f9623'
username = '@khaidoukova'
# TOKEN = '6750164468:AAEqKTRq-J2wGXaZgiBCaxTjd1rZN-gZBTM'
client = TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxCUSTOM")

client.start()


async def dump_all_messages(channel, words):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 100  # общее количество сообщений, которой парсится

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        # print(history)
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            if message.message is not None:
                for word in words:
                    if word in message.message:

                        try:
                            data = {
                                    'message': message.message,
                                    'date': datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'),
                                    'user_id': message.from_id.user_id
                            }
                            all_messages.append(data)

                        except:
                            continue

        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

        with open('new_messages.json', 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
    # url = input() # Ссылка на канал или чат
    channel = await client.get_entity('https://t.me/zakazyfreelance')
    words = ['разработка', 'python']

    await dump_all_messages(channel, words)


with client:
    client.loop.run_until_complete(main())
