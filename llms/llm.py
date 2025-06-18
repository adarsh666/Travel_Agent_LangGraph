import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


class LLMModel:
    def __init__(self, model_name="deepseek-r1-distill-llama-70b"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        self.groq_model=ChatGroq(model=self.model_name)
        
    def get_model(self):
        return self.groq_model