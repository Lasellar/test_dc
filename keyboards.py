from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_example = InlineKeyboardButton(
    text='button example', callback_data='button example'
)

inline_kb_another_button = InlineKeyboardButton(
    text='prepared text', callback_data='prepared text'
)

inline_kb_unload = InlineKeyboardButton(
    text='unload user mesages',
    callback_data='unload user mesages'
)

markup_example = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_kb_example]
    ]
)

markup_another_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_kb_another_button]
    ]
)

markup_unload = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_kb_unload]
    ]
)
