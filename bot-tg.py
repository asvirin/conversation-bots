from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging 
import time
import os

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

import dialogflow_v2 as dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    
    text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
            session=session, query_input=query_input)
        
    return response.query_result.fulfillment_text

class MyLogsHandler(logging.Handler):
    def emit(self, record):
        telegram_token_information_message = os.environ['telegram_token_information_message']
        chat_id_information_message = os.environ['chat_id_information_message']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=telegram_token_information_message)
        bot_error.send_message(chat_id=chat_id_information_message, text=log_entry)   
        
def echo(bot, update):
    chat_id = update.message.chat_id
    user_message = update.message.text
    project_id = os.environ['project_id']
    bot_answer = detect_intent_texts(project_id, chat_id, user_message, 'ru-RU')
    update.message.reply_text(bot_answer)
    
def start(bot, update):
    update.message.reply_text('Ура! Я живой!')

if __name__ == '__main__': 
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Бот для общения в Телеграме запущен")
    
    try:
        telegram_token = os.environ['telegram_token']
        updater = Updater(telegram_token)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))

        echo_handler = MessageHandler (Filters.text, echo)
        dp.add_handler(echo_handler)

        updater.start_polling()
        updater.idle()
        
    except Exception:
        logger.exception('Возникла ошибка в боте для общения в Телеграме ↓')
        time(14400)
