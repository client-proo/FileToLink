# Thunder/bot/__init__.py

from pyrogram import Client
from Thunder.vars import Var
from Thunder.utils.logger import logger

StreamBot = Client(
    name="Web Streamer",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
)

multi_clients = {}
work_loads = {}
