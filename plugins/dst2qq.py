import os
from pathlib import Path
from asyncinotify import Inotify, Mask
import asyncio
from nonebot import get_bot, get_driver

group_id = 681130497


def process_message(message):
    messages = [m[32:] for m in message.split("\n") if "Say" in m]
    return "\n".join(messages)


async def monitor(file_name):
    with Inotify() as inotify, open(file_name, "rt", encoding="utf-8") as file:
        inotify.add_watch(file_name, Mask.MODIFY)

        file.read()  # Read the old data, we do not use them
        pre_file_size = 0

        while True:
            await anext(inotify)

            file_size = os.path.getsize(file_name)
            if file_size < pre_file_size:
                file.seek(0, 0)
            pre_file_size = file_size

            message = process_message(file.read())

            bot = None
            try:
                bot = get_bot()
            except:
                pass
            if bot is not None:
                await bot.send_group_msg(group_id=group_id, message=message)


startup = get_driver().server_app.on_event("startup")


@startup
async def startup_handle():
    asyncio.create_task(monitor(Path().resolve() / ".." / ".." / "Master" / "server_chat_log.txt"))
