import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
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
        bot_error.send_message(chat_id=chat_id, text=log_entry) 

def echo(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    project_id = os.environ['project_id']
    message = detect_intent_texts(project_id, event.user_id, user_message, 'ru-RU')
    if message != 'no_answer':
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1,1000000000)
        )

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Бот для общения в ВКонтакте запущен")
    
    try:
        vk_community_token = os.environ['project_id']
        vk_session = vk_api.VkApi(token=vk_community_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
                
    except Exception:
        logger.exception('Возникла ошибка в боте для общения в ВКонтакте ↓')
        time(14400)
