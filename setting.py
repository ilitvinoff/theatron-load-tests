import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

BASE_URL = os.getenv("BASE_URL", None)
NUM_USERS = int(os.getenv("NUM_USERS", 50))
SPAWN_RATE = int(os.getenv("SPAWN_RATE", 10))
RUN_TIME = os.getenv("RUN_TIME", "1m")
ACCESS_CODE = os.getenv("ACCESS_CODE", None)
CREDENTIALS_FILEPATH = os.getenv("CREDENTIALS_FILEPATH", None)