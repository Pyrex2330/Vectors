from os import getenv
import vectors_bot

token = getenv('API_TOKEN')

if __name__ == '__main__':
    vectors_bot.start_polling()
