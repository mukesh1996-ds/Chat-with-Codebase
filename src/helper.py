from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.embeddings import HuggingFaceEmbeddings
import os 

## Clone any github repositories 
def repo_ingestion(repo_url):
    os.makedirs('repo',exist_ok=True)
    repo_path="repo/"
    Repo.clone_from(repo_url,to_path=repo_path)

## Loading the repositories as documents 
def load_repo(repo_path):
    loader=GenericLoader.from_filesystem(repo_path+'/src/mlProject',glob="**/*",suffixes=['.py'],
                                     parser=LanguageParser(language=Language.PYTHON))
    documents=loader.load()
    return documents

## Creating text Chunks 
def text_splitter(documents):
    documents_splitter=RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
                                                                chunk_size=2000,
                                                                chunk_overlap=200)
    text_chunks=documents_splitter.split_documents(documents=documents)
    return text_chunks

## load the embedding models 
def load_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings
