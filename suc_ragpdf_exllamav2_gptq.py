# -*- coding: utf-8 -*-
"""suc_ragPDF_exllamav2_GPTQ.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/195Y5RmiNZi5z1r4XUFlXI4HKTysV_Ibf

# ExLlamaV2

[ExLlamav2](https://github.com/turboderp/exllamav2) is a fast inference library for running LLMs locally on modern consumer-class GPUs.

It supports inference for GPTQ & EXL2 quantized models, which can be accessed on [Hugging Face](https://huggingface.co/TheBloke).

This notebook goes over how to run `exllamav2` within LangChain.

Additional information:
[ExLlamav2 examples](https://github.com/turboderp/exllamav2/tree/master/examples)

## Installation

Refer to the official [doc](https://github.com/turboderp/exllamav2)
For this notebook, the requirements are :
- python 3.11
- langchain 0.1.7
- CUDA: 12.1.0 (see bellow)
- torch==2.1.1+cu121
- exllamav2 (0.0.12+cu121)

If you want to install the same exllamav2 version :
```shell
pip install https://github.com/turboderp/exllamav2/releases/download/v0.0.12/exllamav2-0.0.12+cu121-cp311-cp311-linux_x86_64.whl
```

if you use conda, the dependencies are :
```
  - conda-forge::ninja
  - nvidia/label/cuda-12.1.0::cuda
  - conda-forge::ffmpeg
  - conda-forge::gxx=11.4
```

## Usage

You don't need an `API_TOKEN` as you will run the LLM locally.

It is worth understanding which models are suitable to be used on the desired machine.

[TheBloke's](https://huggingface.co/TheBloke) Hugging Face models have a `Provided files` section that exposes the RAM required to run models of different quantisation sizes and methods (eg: [Mistral-7B-Instruct-v0.2-GPTQ](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GPTQ)).
"""

!pip install -U langchain huggingface_hub exllamav2 langchain_community

!git clone https://github.com/langchain-ai/langchain.git

import os

from huggingface_hub import snapshot_download
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
#from libs.langchain.langchain.chains.llm import LLMChain

# function to download the gptq model
def download_GPTQ_model(model_name: str, models_dir: str = "./models/") -> str:
    """Download the model from hugging face repository.

    Params:
    model_name: str: the model name to download (repository name). Example: "TheBloke/CapybaraHermes-2.5-Mistral-7B-GPTQ"
    """
    # Split the model name and create a directory name. Example: "TheBloke/CapybaraHermes-2.5-Mistral-7B-GPTQ" -> "TheBloke_CapybaraHermes-2.5-Mistral-7B-GPTQ"

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    _model_name = model_name.split("/")
    _model_name = "_".join(_model_name)
    model_path = os.path.join(models_dir, _model_name)
    if _model_name not in os.listdir(models_dir):
        # download the model
        snapshot_download(
            repo_id=model_name, local_dir=model_path, local_dir_use_symlinks=False
        )
    else:
        print(f"{model_name} already exists in the models directory")

    return model_path

from exllamav2.generator import (
    ExLlamaV2Sampler,
)

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.05

model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")

callbacks = [StreamingStdOutCallbackHandler()]

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Verbose is required to pass to the callback manager
llm = ExLlamaV2(
    model_path=model_path,
    callbacks=callbacks,
    verbose=True,
    settings=settings,
    streaming=True,
    max_new_tokens=150,
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What Football team won the UEFA Champions League in the year the iphone 6s was released?"

output = llm_chain.invoke({"question": question})
print(output)

import gc

import torch

torch.cuda.empty_cache()
gc.collect()
!nvidia-smi

from exllamav2.generator import (
    ExLlamaV2Sampler,
)

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.05

model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")

callbacks = [StreamingStdOutCallbackHandler()]

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Verbose is required to pass to the callback manager
llm = ExLlamaV2(
    model_path=model_path,
    callbacks=callbacks,
    verbose=True,
    settings=settings,
    streaming=True,
    max_new_tokens=150,
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What Football team won the UEFA Champions League in the year the iphone 6s was released?"

output = llm_chain.invoke({"question": question})
print(output)







from exllamav2.generator import ExLlamaV2Sampler
from langchain.llms import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

# Helper function to download model (you can replace this with your own implementation)
def download_GPTQ_model(model_name):
    # Implement model download or just return the local path if already downloaded
    # For example:
    base_path = "models/"
    model_path = os.path.join(base_path, model_name.split("/")[-1])
    if not os.path.exists(model_path):
        print(f"Please download the model from {model_name} and place it in {model_path}")
    return model_path

# 1. Load and process the PDF file
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    return chunks

# 2. Create embeddings and vector store
def create_vector_store(pdf_chunks):
    # Load embeddings model (you can use any model compatible with your hardware)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'} # Use 'cpu' if you don't have GPU
    )

    # Create vector store
    vector_store = FAISS.from_documents(pdf_chunks, embeddings)

    return vector_store

# 3. Configure ExLlamaV2 model
def setup_llm():
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.05

    model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")
    callbacks = [StreamingStdOutCallbackHandler()]

    # Create LLM
    llm = ExLlamaV2(
        model_path=model_path,
        callbacks=callbacks,
        verbose=True,
        settings=settings,
        streaming=True,
        max_new_tokens=500,  # Increased for more detailed responses
    )

    return llm

# 4. RAG Chain
def run_rag_chain(pdf_path, question):
    # Process PDF
    chunks = load_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Setup LLM
    llm = setup_llm()

    # Create prompt template for RAG
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create and run chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.invoke({"context": context, "question": question})

    return output

# Example usage
if __name__ == "__main__":
    pdf_path = "your_document.pdf"  # Replace with your PDF file path
    question = "What are the key points in this document?"  # Replace with your question

    result = run_rag_chain(pdf_path, question)
    print("\n\nFinal answer:")
    print(result['text'])

!pip install pypdf

!pip install faiss-gpu

!pip install chromadb sentence-transformers

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/facebookresearch/faiss.git
# %cd faiss && cmake -B build . -DFAISS_ENABLE_GPU=ON -DFAISS_ENABLE_PYTHON=ON -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -j 8 && cd build/faiss/python && pip install .
!cmake --build build --config Release -j 8
# %cd build/faiss/python
!pip install .

#!pip install langchain_community

from exllamav2.generator import ExLlamaV2Sampler
# Import ExLlamaV2 from langchain_community instead of langchain.llms
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

# ... (rest of the code remains the same) ...

# Helper function to download model (you can replace this with your own implementation)
def download_GPTQ_model(model_name):
    # Implement model download or just return the local path if already downloaded
    # For example:
    base_path = "models/"
    model_path = os.path.join(base_path, model_name.split("/")[-1])
    if not os.path.exists(model_path):
        print(f"Please download the model from {model_name} and place it in {model_path}")
    return model_path

# 1. Load and process the PDF file
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    return chunks

# 2. Create embeddings and vector store
def create_vector_store(pdf_chunks):
    # Load embeddings model (you can use any model compatible with your hardware)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'} # Use 'cpu' if you don't have GPU
    )

    # Create vector store
    vector_store = FAISS.from_documents(pdf_chunks, embeddings)

    return vector_store

# 3. Configure ExLlamaV2 model
def setup_llm():
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.05

    model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")
    callbacks = [StreamingStdOutCallbackHandler()]

    # Create LLM
    llm = ExLlamaV2(
        model_path=model_path,
        callbacks=callbacks,
        verbose=True,
        settings=settings,
        streaming=True,
        max_new_tokens=500,  # Increased for more detailed responses
    )

    return llm

# 4. RAG Chain
def run_rag_chain(pdf_path, question):
    # Process PDF
    chunks = load_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Setup LLM
    llm = setup_llm()

    # Create prompt template for RAG
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create and run chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.invoke({"context": context, "question": question})

    return output

# Example usage
if __name__ == "__main__":
    pdf_path = "/content/The_Little_Prince_Antoine_de_Saint_Exupery.pdf"  # Replace with your PDF file path
    question = "What are the key points in this document?"  # Replace with your question

    result = run_rag_chain(pdf_path, question)
    print("\n\nFinal answer:")
    print(result['text'])

from exllamav2.generator import ExLlamaV2Sampler
from langchain.llms import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma  # Replacing FAISS with Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

from exllamav2.generator import ExLlamaV2Sampler
# Import ExLlamaV2 from langchain_community instead of langchain.llms
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

from exllamav2.generator import ExLlamaV2Sampler
# Import ExLlamaV2 from langchain_community instead of langchain.llms
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import os

# Import Chroma here
from langchain.vectorstores import Chroma

# ... (rest of the code remains the same) ...

from exllamav2.generator import (
    ExLlamaV2Sampler,
)

settings = ExLlamaV2Sampler.Settings()
settings.temperature = 0.85
settings.top_k = 50
settings.top_p = 0.8
settings.token_repetition_penalty = 1.05

model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")

# Helper function to download model (you can replace this with your own implementation)
def download_GPTQ_model(model_name):
    # Implement model download or just return the local path if already downloaded
    # For example:
    base_path = "/content/models"
    model_path = os.path.join(base_path, model_name.split("/")[-1])
    if not os.path.exists(model_path):
        print(f"Please download the model from {model_name} and place it in {model_path}")
    return model_path

# 1. Load and process the PDF file
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)

    return chunks

# 2. Create embeddings and vector store
def create_vector_store(pdf_chunks):
    # Load embeddings model (you can use any model compatible with your hardware)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda'} # Use 'cpu' if you don't have GPU
    )

    # Create vector store using Chroma instead of FAISS
    vector_store = Chroma.from_documents(pdf_chunks, embeddings)

    return vector_store

# 3. Configure ExLlamaV2 model
def setup_llm():
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.05

    model_path = download_GPTQ_model("TheBloke/Mistral-7B-Instruct-v0.2-GPTQ")
    callbacks = [StreamingStdOutCallbackHandler()]

    # Create LLM
    llm = ExLlamaV2(
        model_path=model_path,
        callbacks=callbacks,
        verbose=True,
        settings=settings,
        streaming=True,
        max_new_tokens=500,  # Increased for more detailed responses
    )

    return llm

# 4. RAG Chain
def run_rag_chain(pdf_path, question):
    # Process PDF
    chunks = load_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Setup LLM
    llm = setup_llm()

    # Create prompt template for RAG
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create and run chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.invoke({"context": context, "question": question})

    return output

# Example usage
if __name__ == "__main__":
    pdf_path = "/content/The_Little_Prince_Antoine_de_Saint_Exupery.pdf"  # Replace with your PDF file path
    question = "What are the key points in this document?"  # Replace with your question

    result = run_rag_chain(pdf_path, question)
    print("\n\nFinal answer:")
    print(result['text'])

from exllamav2.generator import ExLlamaV2Sampler
# Import ExLlamaV2 from langchain_community instead of langchain.llms
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
import os
import torch
import huggingface_hub
from huggingface_hub import hf_hub_download, snapshot_download

# Helper function to download model properly from Hugging Face
def download_GPTQ_model(model_name):
    """Download a model from Hugging Face and return the local path."""
    base_path = "/content/models"
    model_dir = os.path.join(base_path, model_name.split("/")[-1])

    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    # Check if model is already downloaded
    if os.path.exists(model_dir) and len(os.listdir(model_dir)) > 0:
        print(f"Model already exists at {model_dir}")
        return model_dir

    try:
        # Download the model files from Hugging Face
        print(f"Downloading model {model_name} to {model_dir}...")
        snapshot_download(
            repo_id=model_name,
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        print(f"Model downloaded successfully to {model_dir}")
        return model_dir
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please download the model manually from Hugging Face")
        # Create directory anyway so code can continue
        os.makedirs(model_dir, exist_ok=True)
        return model_dir

# 1. Load and process the PDF file
def load_pdf(pdf_path):
    """Load and chunk a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    print(f"Loading PDF from {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    return chunks

# 2. Create embeddings and vector store
def create_vector_store(pdf_chunks):
    """Create a vector store from document chunks."""
    print("Creating embeddings...")

    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

    # Create vector store
    print("Creating vector store...")
    vector_store = Chroma.from_documents(pdf_chunks, embeddings)
    print("Vector store created successfully")

    return vector_store

# 3. Configure ExLlamaV2 model
def setup_llm(model_name="TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"):
    """Set up the ExLlamaV2 model."""
    print("Setting up LLM...")

    # Configure sampling settings
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.05

    # Download model
    model_path = download_GPTQ_model(model_name)
    callbacks = [StreamingStdOutCallbackHandler()]

    try:
        # Create LLM with proper error handling
        llm = ExLlamaV2(
            model_path=model_path,
            callbacks=callbacks,
            verbose=True,
            settings=settings,
            streaming=True,
            max_new_tokens=500,
        )
        print("LLM set up successfully")
        return llm
    except Exception as e:
        print(f"Error setting up LLM: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if model files are properly downloaded")
        print("2. Verify the model path is correct")
        print("3. Ensure you have the right version of ExLlamaV2")
        print("4. Make sure you have enough GPU memory")
        raise

# 4. RAG Chain
def run_rag_chain(pdf_path, question, model_name="TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"):
    """Run a RAG chain to answer a question based on PDF content."""
    print(f"Processing question: '{question}'")

    # Process PDF
    chunks = load_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    # Retrieve relevant documents
    print("Retrieving relevant document chunks...")
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    print(f"Retrieved {len(relevant_docs)} relevant chunks")

    # Setup LLM
    llm = setup_llm(model_name)

    # Create prompt template for RAG
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create and run chain
    print("Running LLM chain...")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.invoke({"context": context, "question": question})

    return output

# Example usage
if __name__ == "__main__":
    pdf_path = "/content/The_Little_Prince_Antoine_de_Saint_Exupery.pdf"  # Replace with your PDF file path
    question = "What are the key points in this document?"  # Replace with your question

    try:
        result = run_rag_chain(pdf_path, question)
        print("\n\nFinal answer:")
        print(result['text'])
    except Exception as e:
        print(f"Error running RAG chain: {e}")

"""### aشغال جيد"""

from exllamav2.generator import ExLlamaV2Sampler
# Import ExLlamaV2 from langchain_community instead of langchain.llms
from langchain_community.llms.exllamav2 import ExLlamaV2
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
import os
import torch
import huggingface_hub
from huggingface_hub import hf_hub_download, snapshot_download

# Helper function to download model properly from Hugging Face
def download_GPTQ_model(model_name):
    """Download a model from Hugging Face and return the local path."""
    base_path = "/content/models"
    model_dir = os.path.join(base_path, model_name.split("/")[-1])

    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    # Check if model is already downloaded
    if os.path.exists(model_dir) and len(os.listdir(model_dir)) > 0:
        print(f"Model already exists at {model_dir}")
        return model_dir

    try:
        # Download the model files from Hugging Face
        print(f"Downloading model {model_name} to {model_dir}...")
        snapshot_download(
            repo_id=model_name,
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        print(f"Model downloaded successfully to {model_dir}")
        return model_dir
    except Exception as e:
        print(f"Error downloading model: {e}")
        print("Please download the model manually from Hugging Face")
        # Create directory anyway so code can continue
        os.makedirs(model_dir, exist_ok=True)
        return model_dir

# 1. Load and process the PDF file
def load_pdf(pdf_path):
    """Load and chunk a PDF file."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    print(f"Loading PDF from {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    return chunks

# 2. Create embeddings and vector store
def create_vector_store(pdf_chunks):
    """Create a vector store from document chunks."""
    print("Creating embeddings...")

    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

    # Create vector store
    print("Creating vector store...")
    vector_store = Chroma.from_documents(pdf_chunks, embeddings)
    print("Vector store created successfully")

    return vector_store

# 3. Configure ExLlamaV2 model
def setup_llm(model_name="TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"):
    """Set up the ExLlamaV2 model."""
    print("Setting up LLM...")

    # Configure sampling settings
    settings = ExLlamaV2Sampler.Settings()
    settings.temperature = 0.85
    settings.top_k = 50
    settings.top_p = 0.8
    settings.token_repetition_penalty = 1.05

    # Download model
    model_path = download_GPTQ_model(model_name)
    callbacks = [StreamingStdOutCallbackHandler()]

    try:
        # Create LLM with proper error handling
        llm = ExLlamaV2(
            model_path=model_path,
            callbacks=callbacks,
            verbose=True,
            settings=settings,
            streaming=True,
            max_new_tokens=500,
        )
        print("LLM set up successfully")
        return llm
    except Exception as e:
        print(f"Error setting up LLM: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if model files are properly downloaded")
        print("2. Verify the model path is correct")
        print("3. Ensure you have the right version of ExLlamaV2")
        print("4. Make sure you have enough GPU memory")
        raise

# 4. RAG Chain
def run_rag_chain(pdf_path, question, model_name="TheBloke/Mistral-7B-Instruct-v0.2-GPTQ"):
    """Run a RAG chain to answer a question based on PDF content."""
    print(f"Processing question: '{question}'")

    # Process PDF
    chunks = load_pdf(pdf_path)
    vector_store = create_vector_store(chunks)

    # Retrieve relevant documents
    print("Retrieving relevant document chunks...")
    relevant_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    print(f"Retrieved {len(relevant_docs)} relevant chunks")

    # Setup LLM
    llm = setup_llm(model_name)

    # Create prompt template for RAG
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create and run chain
    print("Running LLM chain...")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.invoke({"context": context, "question": question})

    return output

# Example usage
if __name__ == "__main__":
    pdf_path = "/content/The_Little_Prince_Antoine_de_Saint_Exupery.pdf"  # Replace with your PDF file path
    question = "What are the key points in this document?"  # Replace with your question

    try:
        result = run_rag_chain(pdf_path, question)
        print("\n\nFinal answer:")
        print(result['text'])
    except Exception as e:
        print(f"Error running RAG chain: {e}")

