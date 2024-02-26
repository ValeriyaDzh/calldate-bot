from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int, **kwargs: str) -> InlineKeyboardMarkup:
    """Function to generate a day of the week keyboard"""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def create_inline_users_kb(width: int, *args: str) -> InlineKeyboardMarkup:
    """Function to generate a keyboard from users days"""
    kb_builder = InlineKeyboardBuilder()

    for button in args:
        kb_builder.row((InlineKeyboardButton(text=button, callback_data=button)))

    kb_builder.row(
        InlineKeyboardButton(text="любой из вариантов", callback_data="любой"),
        InlineKeyboardButton(text="готово✅", callback_data="готово"),
        width=1,
    )
    return kb_builder.as_markup()
