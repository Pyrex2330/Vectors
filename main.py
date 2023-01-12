import vectors_bot
import os
from dotenv import load_dotenv

load_dotenv()

token = str(os.getenv('API_TOKEN'))

if __name__ == '__main__':
    vectors_bot.start_polling()
