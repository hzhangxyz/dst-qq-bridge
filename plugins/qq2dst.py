import asyncio
from nonebot.plugin import on_message
from nonebot.adapters import Event

group_id = 681130497


async def group_checker(event: Event) -> bool:
    if event.message_type != "group":
        return False
    if event.group_id != group_id:
        return False
    return True


echo = on_message(rule=group_checker)


@echo.handle()
async def handle_echo(event: Event):
    message = f"(QQ群:{group_id}) {event.sender.nickname}: {event.raw_message}"
    # await echo.send(message=message)
    command = f"c_announce({repr(message)})"
    await asyncio.create_subprocess_exec("/usr/bin/tmux", "send-keys", "-t", "dst", command, "Enter")
