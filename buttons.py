from aiogram import Bot, Dispatcher, types, F, filters, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
from main import proverka

def mainmenu():
    buttons = [
        [
            types.InlineKeyboardButton(text="Звезды⭐️", callback_data="buystars")
        ],
        [
            types.InlineKeyboardButton(text="Поддержка✍️", callback_data="help")
        ],
        [
            types.InlineKeyboardButton(text="Отзывы🛍", callback_data="reviews"),
            types.InlineKeyboardButton(text="Описание🗒", callback_data="about")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def changestars():
    buttons = [
        [
            types.InlineKeyboardButton(text="50⭐(️85 RUB)", callback_data="50stars"),
            types.InlineKeyboardButton(text="75⭐(️127 RUB)", callback_data="75stars")
        ],
        [
            types.InlineKeyboardButton(text="100⭐(️165 RUB)", callback_data="100stars"),
            types.InlineKeyboardButton(text="150⭐(️248 RUB)", callback_data="150stars")
        ],
        [
            types.InlineKeyboardButton(text="200⭐(️340 RUB)", callback_data="200stars"),
            types.InlineKeyboardButton(text="250⭐(️413 RUB)", callback_data="250stars")
        ],
        [
            types.InlineKeyboardButton(text="350⭐(️578 RUB)", callback_data="350stars"),
            types.InlineKeyboardButton(text="500⭐(️825 RUB)", callback_data="500stars")

        ],
        [
            types.InlineKeyboardButton(text="700⭐(️1155 RUB)", callback_data="700stars"),
            types.InlineKeyboardButton(text="1000⭐(️1640 RUB)", callback_data="1000stars")
        ],
        [
            types.InlineKeyboardButton(text="Другое количество⭐", callback_data="anystars"),
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="generalmenu")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet50():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="50starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def cryptometbut():
    buttons = [
        [
            types.InlineKeyboardButton(text="💬Связаться", url = 'https://t.me/Black_Prince01')
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="generalmenu")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet75():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="75starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet100():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="100starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet150():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="150starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet200():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="200starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet250():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="250starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet350():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="350starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet500():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="500starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet700():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="700starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def paymet1000():
    buttons = [
        [
            types.InlineKeyboardButton(text="📱СБП", callback_data="1000starsspb"),
            types.InlineKeyboardButton(text="💰Криптовалютой", callback_data="cryptomet")
        ],
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def backmenu():
    buttons = [
        [
            types.InlineKeyboardButton(text="⬅️Назад", callback_data="buystars")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def checkbuy():
    buttons = [
        [
            types.InlineKeyboardButton(text='🗑Удалить', callback_data='deleteuved')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def backgeneralmenu():
    buttons = [
        [
            types.InlineKeyboardButton(text='⬅️Назад', callback_data='generalmenu')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def reviewsbutton():
    buttons = [
        [
            types.InlineKeyboardButton(text='💬Отзывы', url ='https://t.me/otzivistarslegal')
        ],
        [
            types.InlineKeyboardButton(text='⬅️Назад', callback_data='generalmenu')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def zagruzkacheka():
    buttons = [
        [
            types.InlineKeyboardButton(text='🛍Загрузить чек', callback_data='zagruz')
        ],
        [
            types.InlineKeyboardButton(text='⬅️Назад', callback_data='generalmenu')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def reviewsm():
    buttons = [
        [
            types.InlineKeyboardButton(text='🛍Оставить отзыв', url = 'https://t.me/Black_Prince01')
        ],
        [
            types.InlineKeyboardButton(text='⬅️Завершить покупку', callback_data='generalmenu')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def checksubs():
    buttons = [
        [
            types.InlineKeyboardButton(text='👤Подписаться', url='https://t.me/gdfljkdfgsusdf')
        ],
        [
            types.InlineKeyboardButton(text='🟢ПРОВЕРИТЬ', callback_data='generalmenu')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def adminmenuoff():
    buttons = [
        [
            types.InlineKeyboardButton(text='ПРОВЕРКА: ⛔️ВЫКЛ', callback_data='proverkaon')
        ],
        [
            types.InlineKeyboardButton(text='💬РАССЫЛКА', callback_data='rassilka')
        ],
        [
            types.InlineKeyboardButton(text='🗑Скрыть', callback_data='deleteuved')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def adminmenuon():
    buttons = [
        [
            types.InlineKeyboardButton(text='ПРОВЕРКА: ✅ВКЛ', callback_data='proverkaoff')
        ],
        [
            types.InlineKeyboardButton(text='💬РАССЫЛКА', callback_data='rassilka')
        ],
        [
            types.InlineKeyboardButton(text='🗑Скрыть', callback_data='deleteuved')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def buttonsforrass(message_buttonname: str = None,message_buttonlink: str = None):
    buttons = [
        [
            types.InlineKeyboardButton(text=message_buttonname, url = message_buttonlink)
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def confirmspam():
    buttons = [
        [
            types.InlineKeyboardButton(text='Подтвердить', callback_data='startspam')
        ],
        [
            types.InlineKeyboardButton(text='Отменить', callback_data='stops')
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def buttons_for_rass(button_name, button_url):
    buttons = [
        [
            types.InlineKeyboardButton(text=button_name, url =  button_url)
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard