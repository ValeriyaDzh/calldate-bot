import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest
from app.service.service import *


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "chat_dict",
    [
        {1: ["a", "b"], 2: ["b"], 3: ["b", "c"]},
        {1: ["a", "b"], 2: ["b"], 3: ["b", "c"], "4": ["a", "b"]},
    ],
)
async def test_count_answers(chat_dict):
    res = await count_answers(chat_dict, "leters")

    assert res == {
        "a": 1,
        "b": 3,
        "c": 1,
    }
