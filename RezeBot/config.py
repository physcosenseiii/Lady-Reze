# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open('{}/RezeBot/{}'.format(os.getcwd(), config),
              'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    #Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 123456  # integer value, dont use ""
    API_HASH = "awoo"
#This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 922499043  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "Physco_Sensei"
    SUPPORT_CHAT = 'Zeke_Grp'  #Your own group for support, do not add the @
    JOIN_LOGGER = -1001641370717  #Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = -1001545227881  #Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit

    #RECOMMENDED
    SQLALCHEMY_DATABASE_URI = "postgresql://ovmujxzt:fR8weVTb_O7FCtdsA4_ytkqV0MsWx-Hk@ella.db.elephantsql.com/ovmujxzt" # needed for any database modules
    REDIS_URL = "redis://default:ixqUfqicsHhILHpwbe4FNHNzs8P6qdQ6@redis-12115.c124.us-central1-1.gce.cloud.redislabs.com:12115/reze"
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = "xP96JSnf92wtkB~jfusRKjv9KyagW2ZtFXldftfdri~r0A3FS95vz73Pwkoeqgo8"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    #OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = get_user_list('elevated_users.json', 'sudos')
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list('elevated_users.json', 'devs')
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list('elevated_users.json', 'supports')
    #List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list('elevated_users.json', 'tigers')
    WOLVES = get_user_list('elevated_users.json', 'whitelists')
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  #Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = ''  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = 'awoo'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'awoo'  # Get your API key from https://timezonedb.com/api
    WALL_API = 'awoo'  #For wallpapers, get one from https://wall.alphacoders.com/api.php
    AI_API_KEY = 'awoo'  #For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    ALLOW_CHATS = ""
    HEROKU_API_KEY = ""
    HEROKU_APP_NAME = ""
    TOKEN = "5247464198:AAESV3BBvVxcLoVeEqeIvqkXsiw-cfQkFGA"
    ARQ_API_URL = "https://arq.hamker.in"
    ARQ_API_KEY = "IZZFWW-OPXTNV-GWKSIX-PIACIG-ARQ"
    ERROR_LOGS = ""
    MONGO_DB_URI = "mongodb+srv://reze:reze123@rezerobot.p8epm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    TEMP_DOWNLOAD_DIRECTORY = ""
    OPENWEATHERMAP_ID = ""
    REM_BG_API_KEY = ""
    SESSION_STRING = ""
    STRING_SESSION = "1BVtsOMMBu5n4CkdBNN-68joNLIt4iwQQJmS_PmTKqfOPkYJgdJuhMqXe-_VIir_Lqb9iXprL8kfeXzzlzTVufNVSxD40fSQstA8LRJhgYHh3JSPNwmFlFjgRIwQyV9_KMCVKRcATG-U7vnkh0HL2ZEla6CaIASsD7DXo4nUOHxkGKECRjbIChqbypXA01oKkO4P1uD_DbTSNDNpzd5k8zEuNo25fICyZYSA5mrHHAMIptqz53wufBaj69SqSOlmCGYpNi4l9WyecPJrX8-hnaSHRnJGwcAN978c4lS9nZN1EsastoeGhVAlFn7_4UA_-0tY8dtSSzmpw5hldTitSemkgWh--G9o="
    BOT_USERNAME = "Reze_Super_Bot"
    LASTFM_API_KEY = ""
    CF_API_KEY = ""


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
