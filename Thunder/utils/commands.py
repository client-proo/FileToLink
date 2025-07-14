from pyrogram.types import BotCommand

from Thunder.bot import StreamBot
from Thunder.utils.logger import logger
from Thunder.vars import Var

def get_commands():
    command_descriptions = {
        "start": "راه اندازی ربات",
        "link": "(گروه) تولید یک لینک مستقیم برای یک فایل یا مجموعه‌ای از فایل‌ها",
        "dc": "بازیابی اطلاعات مرکز داده (DC) مربوط به یک کاربر یا فایل",
        "ping": "بررسی وضعیت ربات و سرعت پاسخ‌گویی",
        "about": "دریافت اطلاعات درباره ربات",
        "help": "نمایش راهنما و دستورالعمل‌های استفاده",
        "status": "مشاهده جزئیات ربات و میزان بار کاری فعلی",
        "stats": "(مدیر) مشاهده آمار کارکرد و میزان مصرف منابع",
        "broadcast": "(مدیر) ارسال پیام به تمام کاربران",
        "ban": "(مدیر) مسدود کردن یک کاربر",
        "unban": "(مدیر) رفع مسدودیت یک کاربر",
        "log": "(مدیر) ارسال گزارش‌های ربات",
        "restart": "(مدیر) راه‌اندازی مجدد ربات",
        "shell": "(مدیر) اجرای دستور Shell",
        "users": "(مدیر) نمایش تعداد کل کاربران",
        "authorize": "(مدیر) اعطای دسترسی دائمی به یک کاربر",
        "deauthorize": "(مدیر) لغو دسترسی دائمی یک کاربر",
        "listauth": "(مدیر) فهرست تمام کاربران مجاز"
    }
    return [BotCommand(name, desc) for name, desc in command_descriptions.items()]

async def set_commands():
    if Var.SET_COMMANDS:
        try:
            commands = get_commands()
            if commands:
                await StreamBot.set_bot_commands(commands)
        except Exception as e:
            logger.error(f"Failed to set bot commands: {e}", exc_info=True)