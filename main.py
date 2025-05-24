import asyncio
import logging
from email.policy import default
from winreg import REG_NOTIFY_CHANGE_LAST_SET

from aiogram import Bot, Dispatcher, types, F, filters, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.state import StatesGroup,State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import aiosqlite
import datetime
import copy

from config import *
from buttons import *
from models import createdb

logging.basicConfig(level=logging.INFO, format = '[%(asctime)s] - %(message)s')
bot = Bot(token)
dp = Dispatcher()
proverka = False

class StarsBot(StatesGroup):
    choosing_stars_val = State()
    sendchek = State()

class CheckPdf(StatesGroup):
    send_check = State()
    user_ids = State()
    poluchatel_id = State()

class Form(StatesGroup):
    waiting_for_message_text = State()
    waiting_for_button_text = State()
    waiting_for_button_url = State()
    photo_id = State()

# @dp.message(F.photo)
# async def photohandler(message: Message):
#     if str(message.from_user.id) in admin1 or str(message.from_user.id) in admin2:
#         photo_data = message.photo[-1]
#         await message.answer(f'{photo_data}')
#     else:
#         await message.answer(f'Не верный формат чека,вы можете отправлять чек только в формате PDF.\nЕсли возникнут вопросы связаться со мной', reply_markup = cryptometbut())

@dp.message(F.text == '/start')
async def command_start(message: Message):
    user = str(message.from_user.id)
    if proverka is True:
        user_channel_status = await bot.get_chat_member(chat_id='@gdfljkdfgsusdf', user_id=user)
        if user_channel_status.status != 'left':
            tg_id = int(message.from_user.id)
            username = message.from_user.username
            await bot.send_photo(message.chat.id,
                                 photo='https://i.imgur.com/ndiLwVU.jpeg',
                                 caption=f"@{message.from_user.username} Добро пожаловать в LegalStars! Здесь вы можете легально и без рефаундов купить звёзды Telegram, а также получить помощь. Выберите один из пунктов ниже, чтобы продолжить.",
                                 reply_markup = mainmenu())
            await createdb(tg_id,username)
        else:
            tg_id = int(message.from_user.id)
            username = message.from_user.username
            await message.answer(f'<b>⛔️Вы не подписаны на информационный телеграм-канал бота</b>\n\nДанный информационный канал используется только для публикации информации по обновлениям бота',
                                 parse_mode = 'html',
                                 reply_markup = checksubs())
            await createdb(tg_id, username)
    else:
        tg_id = int(message.from_user.id)
        username = message.from_user.username
        await bot.send_photo(message.chat.id,
                             photo='https://i.imgur.com/ndiLwVU.jpeg',
                             caption=f"@{message.from_user.username} Добро пожаловать в LegalStars! Здесь вы можете легально и без рефаундов купить звёзды Telegram, а также получить помощь. Выберите один из пунктов ниже, чтобы продолжить.",
                             reply_markup=mainmenu())
        await createdb(tg_id, username)


@dp.callback_query(F.data == 'generalmenu')
async def general_menu(callback: CallbackQuery):
    user = str(callback.from_user.id)
    user_channel_status = await bot.get_chat_member(chat_id='@gdfljkdfgsusdf', user_id=user)
    if proverka is True:
        if user_channel_status.status != 'left':
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.message.answer_photo(photo='https://i.imgur.com/ndiLwVU.jpeg',
                                            caption="Добро пожаловать в LegalStars! Здесь вы можете легально и без рефаундов купить звёзды Telegram, а также получить помощь. Выберите один из пунктов ниже, чтобы продолжить.",
                                            reply_markup = mainmenu())
        else:
            await callback.answer(f'❌{callback.from_user.username} вы все еще не подписаны на канал, исправьте это!')
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer_photo(
            photo='https://i.imgur.com/ndiLwVU.jpeg',
            caption="Добро пожаловать в LegalStars! Здесь вы можете легально и без рефаундов купить звёзды Telegram, а также получить помощь. Выберите один из пунктов ниже, чтобы продолжить.",
            reply_markup=mainmenu())

@dp.callback_query(F.data == 'buystars')
async def buystarsmenu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer_photo(photo='https://i.imgur.com/ndiLwVU.jpeg',
                                        caption = f'В этом разделе вы можете выбрать звёзды для самых разных случаев: будь то подарок для друга, награда за достижения или просто приятное приобретение для себя!\n\n✨ Как это работает?\nВыберите нужную кнопку. Следуйте простым инструкциям для завершения покупки\n\nНе забывайте: все наши покупки легальны и защищены, так что вы можете быть уверены в своей сделке!\n\nПодарите себе или своим близким частичку космоса! 🌌',
                                        reply_markup = changestars())

@dp.callback_query(F.data == '50stars')
async def stars50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:', reply_markup = paymet50())

@dp.callback_query(F.data == 'cryptomet')
async def cryptomethod(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'💰 Оплата криптовалютой?\n\nЕсли вы хотите использовать криптовалюту для оплаты, просто напишите мне в личные сообщения! Мы обсудим все детали и найдем оптимальное решение для вас.\n\n🌟 Жду вашего сообщения!', reply_markup = cryptometbut())

@dp.callback_query(F.data == '75stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet75())

@dp.callback_query(F.data == '100stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet100())

@dp.callback_query(F.data == '150stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet150())

@dp.callback_query(F.data == '200stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet200())

@dp.callback_query(F.data == '250stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet250())

@dp.callback_query(F.data == '350stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet350())

@dp.callback_query(F.data == '500stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet500())

@dp.callback_query(F.data == '700stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet700())

@dp.callback_query(F.data == '1000stars')
async def stars75(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'Вы можете легко и быстро оплатить свои покупки с помощью следующих методов:',reply_markup=paymet1000())

@dp.callback_query(F.data == '50starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 85 RUB за 50⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == 'deleteuved')
async def deleteuv(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer('успешно')

@dp.callback_query(F.data == 'help')
async def helpinfo(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer_photo(photo = 'https://i.imgur.com/ndiLwVU.jpeg', caption = f'Поддержка LegalStars 🎨\n🌟 Мы здесь, чтобы помочь вам! 🌟\n\nЕсли у вас возникли вопросы или проблемы, наша команда поддержки всегда готова прийти на помощь. Мы ценим каждого клиента и стремимся сделать ваше взаимодействие с нами максимально комфортным.\n\nКак связаться с нами?\n📩 Напишите нам в личные сообщения воспользовавшись кнопкой ниже. Мы ответим вам в кратчайшие сроки!', reply_markup = cryptometbut())

@dp.callback_query(F.data == 'about')
async def aboutinfo(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer_photo(photo= 'https://i.imgur.com/ndiLwVU.jpeg', caption = '🌟 Legal Stars: Ваш Путь к Звёздам! 🌟\n\nДобро пожаловать в Legal Stars! Здесь вы можете легко и безопасно приобрести звёзды Telegram по самым выгодным ценам. Давайте добавим волшебство в вашу жизнь без лишних забот, не беспокоясь о возвратах!\n\n✨Почему выбирают нас?\n\nДоступные цены: Самые низкие цены на рынке для каждого, кто хочет космического сияния.\n\nЛегальность: Все транзакции защищены, что гарантирует ваше спокойствие\n\nПростота: Всего несколько кликов — и звёзды ваши! Никаких сложностей, только комфорт.\n\n🚀Присоединяйтесь к нам и откройте мир возможностей с Legal Stars!', reply_markup = backgeneralmenu())

@dp.callback_query(F.data == 'reviews')
async def reviewsinfo(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer_photo(
        photo='https://i.imgur.com/ndiLwVU.jpeg',
        caption=f'🌟 Отзывы наших клиентов 🌟\nМы ценим ваше мнение и стремимся сделать наш сервис лучше с каждым днем! Здесь вы можете ознакомиться с отзывами наших клиентов, которые уже приобрели звёзды через LegalStars. Ваши впечатления важны для нас!\n\n💬 Оставьте свой отзыв!\n\nВаш опыт может помочь другим пользователям сделать правильный выбор. Поделитесь своими впечатлениями о покупке звёзд, качестве обслуживания и общем опыте взаимодействия с нашим ботом.',reply_markup=reviewsbutton())


@dp.callback_query(F.data == 'anystars')
async def anystarsquestion(callback: CallbackQuery,state: FSMContext):
    await callback.message.answer(f'Введите количество звезд\nОбратите внимание,при покупке меньше 50 единиц доступно только КРАТНОЕ 13 звездам (подарок за 15 звезд можно продать за 13) и КРАТНОЕ 21 звездам\n✨ При покупке от 50 звёзд я  отправлю вам любое количество звезд без комиссии', reply_markup = backmenu())
    await state.set_state(StarsBot.choosing_stars_val)

@dp.message(StarsBot.choosing_stars_val)
async def starsvalm(message: Message,state: FSMContext):
    if message.text == '13':
        await message.answer(f'<b>Отправьте {15*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id = admin1, text = f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif message.text == '21':
        await message.answer(f'<b>Отправьте {25*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif message.text == '26':
        await message.answer(f'<b>Отправьте {30*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif message.text == '34':
        await message.answer(f'<b>Отправьте {40*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif message.text == '39':
        await message.answer(f'<b>Отправьте {45*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif message.text == '42':
        await message.answer(f'<b>Отправьте {50*1.65} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif int(message.text) >= 50 and int(message.text) <= 1500:
        await message.answer(f'<b>Отправьте {int(int(message.text)*1.65)} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())
        await bot.send_message(chat_id=admin1,text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    elif int(message.text) >= 1500:
        await message.answer(
            f'<b>Отправьте {round(int(message.text) * 1.6)} RUB за {message.text}⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️',
            parse_mode='html', reply_markup=zagruzkacheka())
        await bot.send_message(chat_id=admin1,
                               text=f'Пользователь @{message.from_user.username} заказал {message.text} звезд')
        await state.update_data(choosing_stars_val=message.text)
    else:
        await message.answer(f'К сожалению, такое количество заказать нельзя. В наличии есть следующие варианты: 13, 21, 26, 34, 39, 42.\n\n✨ При покупке от 50 звёзд  отправлю  любое количество звезд\n\nПожалуйста, введите нужное количество ниже, и мы поможем вам сделать правильный выбор! 😊', reply_markup=backmenu())

@dp.callback_query(F.data == 'zagruz', StarsBot.sendchek)
async def zagruzochka(callback: CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer('💬Отправьте файл с чеком в формате PDF для проверки администрацией', reply_markup= backmenu())
    await state.set_state(CheckPdf.send_check)

@dp.message(CheckPdf.send_check, F.document)
async def zagruzochka(message: Message, state: FSMContext):
    await bot.forward_message(chat_id = admin1, from_chat_id = message.from_user.id,message_id = message.message_id)
    await state.set_state(CheckPdf.user_ids)
    await state.update_data(user_ids=message.from_user.id)
    await state.set_state(CheckPdf.send_check)
    await message.answer('Принято, кому начислять звезды?\n Если себе, то напишите <i>"мне"</i> (без ковычек), если кому-то другому, то напишите сюда его юзер',parse_mode = 'html', reply_markup = backmenu())
    await state.update_data(send_check=message.document.file_id)
    await state.set_state(CheckPdf.poluchatel_id)
    await state.update_data(poluchatel_id = message.text)

@dp.message(CheckPdf.poluchatel_id)
async def poluchatel(message: Message, state: FSMContext):
    await state.set_state(StarsBot.choosing_stars_val)
    data = await state.get_data()
    print(data)
    price = data['sendcheck']
    if message.text == 'мне':
        await bot.send_message(chat_id = admin2,
                               text = f'🔔Пользователь @{message.from_user.username} отправил чек для проверки\n⭐️Количество звезд: {price}\nКому отправлять: себе',
                               reply_markup = checkbuy())
        #await bot.send_message(chat_id=admin2,
        #                       text=f'Пользователь @{message.from_user.username} отправил чек для проверки\nКому отправлять: себе',
        #                       reply_markup=checkbuy())
        await message.answer(
            '🟢Спасибо за вашу заявку! Мы уже занимаемся проверкой оплаты, и совсем скоро вы получите ваши звезды.\nПосле получения, если у вас останутся какие-либо вопросы или желание оставить отзыв, свяжитесь по контакту ниже⬇️', reply_markup = reviewsm())
        await state.clear()
    else:
        await bot.send_message(chat_id=admin1,
                                text=f'Пользователь @{message.from_user.username} отправил чек для проверки\nКому отправлять: @{message.text}',
                                reply_markup=checkbuy())
        await bot.send_message(chat_id=admin2,
                               text=f'Пользователь @{message.from_user.username} отправил чек для проверки\nКому отправлять: себе',
                               reply_markup=checkbuy())
        await message.answer(
            '🟢Спасибо за вашу заявку! Мы уже занимаемся проверкой оплаты, и совсем скоро вы получите ваши звезды.\nПосле получения, если у вас останутся какие-либо вопросы или желание оставить отзыв, свяжитесь по контакту ниже⬇️', reply_markup = reviewsm())
        await state.clear()

@dp.callback_query(F.data == '75starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 127 RUB за 75⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '100starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 165 RUB за 100⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '150starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 248 RUB за 150⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '200starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 340 RUB за 200⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '250starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 413 RUB за 250⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '350starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 578 RUB за 350⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '500starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 825 RUB за 500⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '700starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 1155 RUB за 700⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.callback_query(F.data == '1000starsspb')
async def sbp50(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(f'<b>Отправьте 1640 RUB за 1000⭐️ по этому номеру</b>\n<code>+79912148689</code>(кликабельно для копирования)\nПолучатель: <i>Альфа-Банк</i>\nПосле оплаты нажмите кнопку ниже чтобы загрузить чек, далее после проверки оплаты вам будут выданы звезды⭐️', parse_mode = 'html', reply_markup = zagruzkacheka())

@dp.message(F.text == '/admin')
async def adminmenu(message: Message):
    if str(message.from_user.id) in admin1 or str(message.from_user.id) in admin2:
        async with aiosqlite.connect('bot.db') as db:
            async with db.execute('SELECT * FROM users') as cursor:
                result = await cursor.fetchall()
        if proverka is False:
            await message.answer(f'Панель администратора:\n👤Пользователей: {len(result)}\n🔒Проверка на подписку:{proverka}', reply_markup = adminmenuoff())
        else:
            await message.answer(f'Панель администратора:\n👤Пользователей: {len(result)}\n🔒Проверка на подписку:{proverka}', reply_markup=adminmenuon())
    else:
        await message.answer('Вы не являетесь администратором, доступ к админ-панели запрещен', reply_markup = backmenu())

@dp.callback_query(F.data == 'proverkaon')
async def onproverka(callback: CallbackQuery):
    global proverka
    proverka = True
    await callback.answer('✅Проверка включена успешно')
    async with aiosqlite.connect('bot.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            usersresulton = await cursor.fetchall()
    # await bot.delete_message(chat_id = callback.from_user.id, message = callback.message.message_id)
    await callback.message.edit_text(text = f'Панель администратора:\n👤Пользователей: {len(usersresulton)}\n🔒Проверка на подписку:{proverka} ', reply_markup=adminmenuon())

@dp.callback_query(F.data == 'proverkaoff')
async def offproverka(callback: CallbackQuery):
    proverka = False
    async with aiosqlite.connect('bot.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            usersresultoff = await cursor.fetchall()
    await callback.message.edit_text(
        text=f'Панель администратора:\n👤Пользователей: {len(usersresultoff)}\n🔒Проверка на подписку:{proverka} ',
        reply_markup=adminmenuoff())

@dp.callback_query(F.data == 'rassilka')
async def textrassilka(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id = callback.from_user.id, message_id = callback.message.message_id)
    await callback.message.answer("✍️Введите текст сообщения.")
    await state.set_state(Form.waiting_for_message_text)

@dp.message(Form.waiting_for_message_text)
async def namebutton(message: Message, state: FSMContext):
    await state.update_data(waiting_for_message_text = message.text)
    await message.answer('✅Текст принят \n✍️введи название кнопки')
    await state.set_state(Form.waiting_for_button_text)

@dp.message(Form.waiting_for_button_text)
async def buttonname(message: Message, state: FSMContext):
     await state.update_data(button_text = message.text)
     await message.answer('✅Название кнопки принято \n✍️Теперь введи ссылку, которая будет вставлена в эту кнопку')
     await state.set_state(Form.waiting_for_button_url)

@dp.message(Form.waiting_for_button_url)
async def waiturl(message: Message, state: FSMContext):
    await state.update_data(message_buttonlink=message.text)
    await message.answer('✅Ссылка для кнопки получена \n✍️Теперь отправь фото, которое будет прикреплено (если фото не будет, введи "безфото"')
    await state.set_state(Form.photo_id)

@dp.message(Form.photo_id)
async def buttonlink(message: Message, state: FSMContext):
    if message.text == 'безфото':
        await message.answer('Сообщение для рассылки сформировано')
        data = await state.get_data()
        print(data)
        message_text = data['waiting_for_message_text']
        button_name = data['button_text']
        button_url = data['message_buttonlink']
        await message.answer('Рассылка началась')
        async with aiosqlite.connect('bot.db') as db:
            async with db.execute(f'SELECT tg_id FROM users') as cursor:
                spam_users = await cursor.fetchall()
                for z in range(len(spam_users)):
                    await bot.send_message(chat_id=spam_users[z][0], text=str(message_text), reply_markup=buttons_for_rass(button_name, button_url))
        await message.answer('Рассылка завершена')
        await state.clear()
    elif message.content_type == 'photo':
        await state.update_data(photo_id = message.photo[-1].file_id)
        data = await state.get_data()
        print(data)
        message_text = data['waiting_for_message_text']
        button_name = data['button_text']
        button_url = data['message_buttonlink']
        photoid = data['photo_id']
        async with aiosqlite.connect('bot.db') as db:
            async with db.execute(f'SELECT tg_id FROM users') as cursor:
                spam_users = await cursor.fetchall()
                for z in range(len(spam_users)):
                    await bot.send_photo(chat_id=spam_users[z][0],photo=photoid, caption = message_text, reply_markup=buttons_for_rass(button_name, button_url))
        await message.answer('Рассылка с фото завершена')
        await state.clear()
    else:
        await message.answer('ошибка')


@dp.message(F.text == '/devinfo')
async def definfo(message: Message):
    await message.answer('<b>ℹ️Информация о разработчике и боте:</b>\n👤Основной разработчик:<i>funpay.com/users/6889487/</i>\n⚙️Стек бота:<i> Python 3.11.0, aiogram 3.20.0, aiosqlite</i>\n🤌Версия бота: <i>1.2.0</i>\n', parse_mode = 'HTML', disable_web_page_preview=True)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())