from copy import deepcopy

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..database.database import chat_users_db, chat_dict_template
from ..keyboards.keyboards import create_inline_kb, create_inline_users_kb
from ..lexicon.lexicon import MESSAGE, DAYS
from ..service.service import *

router = Router()


# This handler will respond to the "/start" command -
# add chat to the database if it wasn't already there
# and send a message to users to start selecting the day of the week
@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.id not in chat_users_db:
        chat_users_db[message.chat.id] = deepcopy(chat_dict_template)
    chat_users_db[message.chat.id]["participants"] = await count_participants(
        message.chat.id
    )
    await message.answer(
        text=MESSAGE["/start"], reply_markup=create_inline_kb(3, **DAYS)
    )


# This handler will respond to the "/help" command
# and send the user a message with a list of available commands in the bot
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    await message.answer(MESSAGE["/help"])


# This handler will respond to the "/restart" command
# and send a message to users to start selecting the day of the week agane
@router.message(Command(commands=["restart"]))
async def cmd_restart(message: Message):
    local_chat = chat_users_db[message.chat.id]
    local_chat = clean_answers(local_chat)
    await message.answer(
        text=MESSAGE["/restart"], reply_markup=create_inline_kb(3, **DAYS)
    )


# This handler will trigger when inline buttons are pressed on days of the week
# and send the selected day to the user
@router.callback_query(
    lambda c: c.data
    in [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
        "любой",
        "готово",
    ]
)
async def process_weekday_or_done_callback(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    local_chat = chat_users_db[chat_id]
    user_id = callback_query.from_user.id

    if user_id not in local_chat["ready"]:
        if callback_query.data != "готово":
            weekday = callback_query.data
            local_chat.setdefault(user_id, [])
            if weekday not in local_chat[user_id]:
                local_chat[user_id].append(weekday)
                await callback_query.answer(
                    text=f"{callback_query.from_user.first_name}, ты выбрал(-а) {weekday}",
                )
        else:
            local_chat["ready"].append(user_id)
            await callback_query.answer(
                text=f"Ура! {callback_query.from_user.first_name}, ты выбрал(-а) дни. Ждем остальных",
                show_alert=True,
            )
    else:
        await callback_query.answer(
            text=f"Твои дни записаны.\nЖдем ответа от остальных\nпосле сможем продолжить",
            show_alert=True,
        )

    if local_chat["participants"] == len(local_chat["ready"]):
        if "continue" not in local_chat.keys():
            common_days = await generate_math(local_chat, "common_days")
            await send_common_days_message(
                chat_id,
                common_days,
                MESSAGE["days"],
                MESSAGE["day"],
                MESSAGE["no_days"],
            )
        else:
            common_days_vote = await count_answers(local_chat, "common_days_vote")
            await send_sorted_results(chat_id, common_days_vote, MESSAGE["final"])


# This handler will respond to the "/continue" command
# and forms a new inline keyboard to choose between common users days
@router.message(Command(commands=["continue"]))
async def cmd_continue(message: Message):
    local_chat = chat_users_db[message.chat.id]

    if not local_chat.get("continue"):
        local_chat["continue"] = True
        local_chat = clean_answers(local_chat)
        common_days = tuple(local_chat["common_days"])
        await message.answer(
            text=MESSAGE["/continue"],
            reply_markup=create_inline_users_kb(1, *common_days),
        )
    else:
        await message.answer(text="Данные для повторного голосования уже отправлены")


# This handler will respond to the "/end" command
# and sends the user a completion message and clears the voting results in the database
@router.message(Command(commands=["end"]))
async def cmd_help(message: Message):
    local_chat = chat_users_db[message.chat.id]
    local_chat = deepcopy(chat_dict_template)
    await message.answer(MESSAGE["/end"])
