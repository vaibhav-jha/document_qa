from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from pathlib import Path
from langchain.text_splitter import TextSplitter
import os

# Get OPEN AI API key
# I'm using a personal API key stored in drive
try:
    from secret_keys import OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

filepath = '../contracts/'


INDEX_PATH = Path.cwd() / 'index'

if not INDEX_PATH.exists():
    INDEX_PATH.mkdir()

embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
