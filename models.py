from sqlalchemy import BigInteger
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import aiosqlite
import datetime
from aiogram import Bot
from config import admin1, admin2, token

bot = Bot(token)

async def createdb(tg_id,username):
    async with aiosqlite.connect('bot.db') as db:
        regdate = f'{datetime.date.today()}'
        await db.execute("CREATE TABLE IF NOT EXISTS users (tg_id BIGINT, username TEXT, registration TEXT)")
        cursor = await db.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
        data = await cursor.fetchone()
        if data is not None:
            return
    async with aiosqlite.connect('bot.db') as db:
        await db.execute("INSERT INTO users (tg_id, username, registration) VALUES (?,?,?)", (tg_id,username,regdate))
        await bot.send_message(chat_id=admin1,
                               text=f'{datetime.date.today()}: Пользователь @{username}\n(id: {tg_id} зарегистрирован в базе данных')
        await db.commit()