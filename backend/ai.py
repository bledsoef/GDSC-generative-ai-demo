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
from openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
import os
import google.generativeai as genai

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

# Environement variable setup
env_path = Path('../') / '.env'
dotenv.load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

class VertexAI:
    def __init__(self):
        '''
        Initializes the AI object with default values for its attributes.
        '''
        

def generate():
    def __init__():
        vertexai.init(project="gdsc-generative-ai-demo", location="us-central1")
        model = GenerativeModel("gemini-pro-vision")
        responses = model.generate_content(
        [],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
        )

        for response in responses:
            print(response.text, end="")


        generate()

    
    def respond(self, question):
        '''
        Takes a message, attached to a prompt and returns a more professional version of the message.
        '''

        # Construct a prompt for the API to transform the message into a formal statement.
        response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

        return response.choices[0].message.content
