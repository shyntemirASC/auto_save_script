from os import getenv
from dotenv import load_dotenv


load_dotenv()

EMAIL = getenv('USER_EMAIL')
PASSWORD = getenv('USER_PASSWORD')