import asyncio
import logging
import os
import sys
import json
import asyncio
import time
import spamwatch
import telegram.ext as tg
from redis import StrictRedis
from inspect import getfullargspec
from aiohttp import ClientSession
from Python_ARQ import ARQ
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.sessions import MemorySession
from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from ptbcontrib.postgres_persistence import PostgresPersistence

StartTime = time.time()

def get_user_list(__init__, key):
    with open("{}/RezeBot/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]

# enable logging
FORMAT = "[RezeBot] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger('[RezeBot]')
LOGGER.info("Reze is starting. | A Project by @Physco_Sensei | Licensed under GPLv3.")
LOGGER.info("Not affiliated to other anime or Villain in any way whatsoever.")
LOGGER.info("Project maintained by: github.com/physco-sensei (t.me/physco_sensei)")

# if version < 3.9, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    LOGGER.error(
        "You MUST have a python version of at least 3.9! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = "5247464198:AAEmP1JJowbfSFHM4hQ72feL-a5akq-igrE"

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", "-1001545227881")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "922499043")

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError: 
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", True))
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Reze_Super_Bot")
    EVENT_LOGS = os.environ.get("EVENT_LOGS", "-1001545227881")
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = 5000
    CERT_PATH = os.environ.get("CERT_PATH")
    REDIS_URL = os.environ.get("REDIS_URL", 'redis://:DKe3IlMl6NNgjbfbluQHTJypJ3Y2Sqdd@redis-15722.c280.us-central1-2.gce.cloud.redislabs.com:15722')
    API_ID = os.environ.get("API_ID", "11557162")
    API_HASH = os.environ.get("API_HASH", "194586eacda66933a17ab1e8a35d4101")
    SESSION_STRING = os.environ.get("SESSION_STRING", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOH8Buz33WJrTP4fygeLjhXWsBGKEuaZii5NQw9TG5pdusOAK3PpGqpfO8Mf4vlX2xuHCp7O2gd29HPFRPd_JOddsKYMsA-F6W0Wq1KSRxsBmUCPP09RNUhkBtQqK2ohCXZD97R03mof55ukRAepJfiI4exiiyVgPAKQVaUIl5qzyXKMqd7ngTOYKKuAQb2GdFWupRTi9VqabommyqAmyHsJu0kvGyFaCg4STH1iJyLqfWkw5qbuM8oxSWB9_x0VQKkeDf7sXeOfx2fItnVX_N2giL-002onpdalb3UjXC3m2awMrfcGFZhj8k-MkO3BqzdwEySpYfkRTAXTJ7Cf_2CwbXws=")
    DB_URL = "postgresql://ovmujxzt:fR8weVTb_O7FCtdsA4_ytkqV0MsWx-Hk@ella.db.elephantsql.com/ovmujxzt"
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://reze:reze123@rezerobot.p8epm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    ARQ_API = os.environ.get("ARQ_API", "SYWHGG-KJNCLP-OCTUKV-YKHPSI-ARQ")
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "ea8b2705f3bdd6889479befaeaf84fe7")
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", True))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", None)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL",   True)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", "LVHPMI9EPJZ9BAU6")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", "NJMXH84WDCN8")
    WALL_API = os.environ.get("WALL_API", '6950f559377140a4e1594c564cdca6a3')
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "Zeke_grp")
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", "3pCvmSxKSdV8spNpoAt_V_eoaIEfSzI3cw")
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY", None)
    CF_API_KEY = os.environ.get("CF_API_KEY", None)
    WELCOME_DELAY_KICK_SEC = os.environ.get("WELCOME_DELAY_KICL_SEC", None)
    BOT_ID = int(os.environ.get("BOT_ID", "5247464198"))
    ARQ_API_URL = "https://arq.hamker.in"
    ARQ_API_KEY = "IZZFWW-OPXTNV-GWKSIX-PIACIG-ARQ"
    ERROR_LOGS = os.environ.get("ERROR_LOGS")

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    from RezeBot.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ERROR_LOGS = Config.ERROR_LOGS
    DB_URL = Config.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Config.MONGO_DB_URI
    ARQ_API = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    NO_LOAD = Config.NO_LOAD
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    SESSION_STRING = Config.SESSION_STRING
    INFOPIC = Config.INFOPIC
    BOT_USERNAME = Config.BOT_USERNAME
    STRING_SESSION = Config.STRING_SESSION
    LASTFM_API_KEY = Config.LASTFM_API_KEY
    CF_API_KEY = Config.CF_API_KEY

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

# If you forking dont remove this id, just add your id. LOL...

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(953362604)


if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

from RezeBot.modules.sql import SESSION

defaults = tg.Defaults(run_async=True)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
print("[INFO]: INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
ARQ_API_KEY = "IZZFWW-OPXTNV-GWKSIX-PIACIG-ARQ"
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

ubot2 = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot2.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

pbot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
)
apps = []
apps.append(pbot)
loop = asyncio.get_event_loop()

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

REDIS_URL = "redis://:DKe3IlMl6NNgjbfbluQHTJypJ3Y2Sqdd@redis-15722.c280.us-central1-2.gce.cloud.redislabs.com:1572"
REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")
except BaseException:
    raise Exception("Your redis server is not alive, please check again.")
finally:
   REDIS.ping()
   LOGGER.info("Your redis server is now alive!")

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from RezeBot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
