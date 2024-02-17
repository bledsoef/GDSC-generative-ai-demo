import dotenv
from pathlib import Path
import traceback
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import pinecone
from makechain import makeChain

from openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import google.generativeai as genai


# Environement variable setup
env_path = Path('../') / '.env'
dotenv.load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class OpenAITrained:
    def __init__(self, chat_history):
        """
        Set up of basic configurations for openai calls
        """
        self.chat_history = chat_history
        # gets the pinecone index as a reference
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENVIRONMENT"])
        vectorStore:Pinecone = Pinecone.from_existing_index(index_name=os.environ["PINECONE_INDEX_NAME"], embedding=OpenAIEmbeddings())
        self.qa = makeChain(vectorStore=vectorStore)
        # use davinci model, but TODO: use gpt-4
        self.model = 'text-davinci-003'

        # temperature governs the creativity of the responses
        self.temperature = .95

        self.max_token = 50

    def respond(self, text: str) -> str:
        """
        Takes in user input and returns AI response
        :param text: User input
        :return: AI Response
        """
        result = self.qa._call({'question':text, 'chat_history':self.chat_history or [], 'context':""})
        return result["answer"]


# Load your API key from an environment variable or secret management service
class OpenAIUntrained:
    def __init__(self):
        '''
        Initializes the AI object with default values for its attributes.
        '''
        # Set OpenAI API key to value stored in the environment variable "API_KEY"
        # Set the default model to "text-davinci-003"
        self.model = "gpt-3.5-turbo"
        # Set the default temperature to 0.4
        self.temp = 0.7
        # Set the default maximum token length to 200
        self.max_token = 200
        self.client = OpenAI()

    
    def respond(self, question):
        '''
        Takes a message, attached to a prompt and returns a more professional version of the message.
        '''

        # Construct a prompt for the API to transform the message into a formal statement.
        response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

        return response.choices[0].message.content

class GeminiAI:
    def __init__(self):
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
                            }

        self.safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=self.generation_config,
                                    safety_settings=self.safety_settings)

        self.convo = self.model.start_chat(history=[])

    def response(self, message):
        self.convo.send_message(message)
        return self.convo.last.text