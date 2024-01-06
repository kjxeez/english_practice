import asyncio

from typing import Dict, Any

from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from aiogram import Router, Bot, Dispatcher, types
from aiogram.types import Message

from aiogram_dialog import Dialog, Window, setup_dialogs, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Checkbox, Row, Cancel, Start

from aiogram.filters.command import Command


class MainMenu(StatesGroup):
    START = State()


class Settings(StatesGroup):
    START = State()


EXTEND_BTN_ID = "extend"


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    if dialog_manager.find(EXTEND_BTN_ID).is_checked():
        return {
            "extended_str": "Helpful materials included",
            "extended": True,
        }
    else:
        return {
            "extended_str": "Helpful materials are not displayed",
            "extended": False,
        }


main_menu = Dialog(
    Window(
        Format(
            "Hello, {event.from_user.username}. \n\n"
            "{extended_str}.\n"
        ),
        Const(
            "Video tutorials by AlexGyver: https://www.youtube.com/channel/UC4axiS76D784-ofoTdo5zOA/featured\nText tutorials by AlexGyver: https://alexgyver.ru/lessons/",
            when="extended",
        ),
        Row(
            Checkbox(
                checked_text=Const("[x] Useful materials"),
                unchecked_text=Const("[ ] Useful materials"),
                id=EXTEND_BTN_ID,
            ),
            Start(Const("Settings"), id="settings", state=Settings.START),
        ),
        getter=getter,
        state=MainMenu.START
    )
)

NOTIFICATIONS_BTN_ID = "notify"
ADULT_BTN_ID = "adult"

settings = Dialog(
    Window(
        Const("Settings"),
        Checkbox(
            checked_text=Const("[x] Send notifications"),
            unchecked_text=Const("[ ] Send notifications"),
            id=NOTIFICATIONS_BTN_ID,
        ),
        Checkbox(
            checked_text=Const("[x] Adult mode"),
            unchecked_text=Const("[ ] Adult mode"),
            id=ADULT_BTN_ID,
        ),
        Row(
            Cancel(),
            Cancel(text=Const("Save"), id="save"),
        ),
        state=Settings.START,
    )
)

router = Router()


@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.START)


async def main():
    bot = Bot(token="6732194106:AAFkiDRcbnlYCoQAQeTvEufjuiTZF3lWDYs")
    dp = Dispatcher()

    @dp.message(Command("pic"))
    async def send_image(message: types.Message):
        await bot.send_photo(chat_id=message.chat.id, photo='https://placepic.ru/wp-content/uploads/2018/11/0_b7c8e_fa32e8d_orig.jpg')

    dp.include_router(main_menu)
    dp.include_router(settings)
    dp.include_router(router)
    setup_dialogs(dp)

    await dp.start_polling(bot)


asyncio.run(main())
