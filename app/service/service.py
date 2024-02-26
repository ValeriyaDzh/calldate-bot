import sys

sys.path.append("..")

from bot import bot


async def count_answers(chat_dict: dict, name_common: str) -> list[str]:
    """
    Function to count answers from participants
    """
    res = {}
    for key, value in chat_dict.items():
        if isinstance(key, int):
            for v in value:
                res[v] = res.get(v, 0) + 1
    return res


def clean_answers(chat_dict: dict) -> dict:
    """
    Function to clean answers from participants
    """
    for key, value in chat_dict.items():
        if isinstance(key, int) or key == "ready":
            chat_dict[key] = []
    return chat_dict


async def generate_math(chat_dict: dict, name_common: str) -> list[str]:
    """
    Function to get common answers from participants
    """
    res = {}
    for key, value in chat_dict.items():
        if isinstance(key, int):
            for v in value:
                res[v] = res.get(v, 0) + 1
    chat_dict.setdefault(
        name_common, [k for k, v in res.items() if v == chat_dict["participants"]]
    )
    return chat_dict[name_common]


async def send_sorted_results(
    chat_id: int,
    vote: dict,
    message: str,
) -> None:
    """
    Function to send sorted vote results in a message
    """

    sorted_results = sorted(vote.items(), key=lambda x: x[1], reverse=True)

    message_results = ""
    for day, count in sorted_results:
        message_results += f"{day} {'📞' * count}\n"

    await bot.send_message(chat_id=chat_id, text=f"\n{message_results}\n{message}")


async def send_common_days_message(
    chat_id: int,
    common_days: list,
    days_message: str,
    day_message: str,
    no_days_message: str,
) -> None:
    """
    Function to send message whith common answers from participants
    """

    if len(common_days) > 1:
        await bot.send_message(
            chat_id=chat_id, text=f"{', '.join(common_days)}\n\n{days_message}"
        )
    elif len(common_days) == 1:
        await bot.send_message(
            chat_id=chat_id, text=f"{', '.join(common_days)}\n\n{day_message}"
        )
    else:
        await bot.send_message(chat_id=chat_id, text=no_days_message)
