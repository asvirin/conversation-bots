import requests
import dialogflow_tools
from dialogflow_tools import MyLogsHandler
import example_function_dialogflow

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(MyLogsHandler())
logger.info("Запущена функция получения вопросов и ответов")

url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
try:
    r = requests.get(url)
    data_questions = r.json()
    for theme in data_questions:
        project_id = project_id
        display_name = theme
        training_phrases_parts = data_questions[theme]['questions']
        message_texts = data_questions[theme]['answer']
        create_intent(project_id, display_name, training_phrases_parts, message_texts)
        
except requests.exceptions.HTTPError:
        logger.exception("Сетевые проблемы с получением json")
