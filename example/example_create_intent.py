import requests
import logging
import os
import telegram
import dialogflow_v2 as dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

class MyLogsHandler(logging.Handler):
    def emit(self, record):
        telegram_token_information_message = os.environ['telegram_token_information_message']
        chat_id_information_message = os.environ[' chat_id_information_message']
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=telegram_token_information_message)
        bot_error.send_message(chat_id=chat_id_information_message, text=log_entry)

def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=[message_texts])
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    
    response = intents_client.create_intent(parent, intent)
    
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler())
    logger.info("Запущена функция получения вопросов и ответов")
    
    project_id = os.environ['project_id']
    
    #example url with training phrases
    url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    
    try:
        r = requests.get(url)
        data_questions = r.json()
        for theme in data_questions:
            display_name = theme
            training_phrases_parts = data_questions[theme]['questions']
            message_texts = data_questions[theme]['answer']
            create_intent(project_id, display_name, training_phrases_parts, message_texts)
        logger.info("Фразы загружены")

    except Exception:
            logger.exception("Проблемы с загрузкой фраз")
