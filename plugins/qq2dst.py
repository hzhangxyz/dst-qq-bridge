import asyncio
from nonebot import get_driver
from nonebot.plugin import on_message
from nonebot.adapters import Event


def group_id():
    return get_driver().config.qqgroupid


def tmux_path():
    return get_driver().config.tmuxpath


def dst_window_name():
    return get_driver().config.dstwindowname


async def group_checker(event: Event) -> bool:
    if event.message_type != "group":
        return False
    if event.group_id != group_id():
        return False
    return True


echo = on_message(rule=group_checker)


@echo.handle()
async def handle_echo(event: Event):
    name = event.sender.card or event.sender.nickname
    message = f"(QQ群:{group_id()}) {name}: {event.raw_message}"
    command = f"c_announce({repr(message)})"
    await asyncio.create_subprocess_exec(tmux_path(), "send-keys", "-t", dst_window_name(), command, "Enter")
