#from decouple import RepositoryIni, Config

from decouple import config
#config = Config(RepositoryIni("settings.ini"))

CLIENT_ID = config("CLIENT_ID")
SECRET = config("SECRET")
REDIRECT_URL = config("REDIRECT_URL")
DB_CONNSTR = config("DB_CONNSTR")
