# Milvus Integration Tutorial Format Specification

This document outlines the standard format for Milvus integration tutorials in the Milvus bootcamp repository.

## File Naming
- Use lowercase with underscores
- Keep provider names simple and recognizable
- This guide can be used for both markdown and ipynb files.


## Document Structure
### 0. Badges
Add two badges to the top of your notebook. Note that the suffix of the notebook path should be `ipynb`, even if it is a markdown file since we will finally convert it to a jupyter notebook file.
```html
<a href="https://colab.research.google.com/github/milvus-io/bootcamp/blob/master/bootcamp/relative_path/to/your_notebook.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>   <a href="https://github.com/milvus-io/bootcamp/blob/master/bootcamp/relative_path/to/your_notebook.ipynb" target="_blank">
    <img src="https://img.shields.io/badge/View%20on%20GitHub-555555?style=flat&logo=github&logoColor=white" alt="GitHub Repository"/>
```
### 1. Header Section
- **Title**
  - Start with "# " as the markdown heading level.
- **Introduction**
  - One or two paragraphs explaining the purpose of the tutorial, the integration provider and the key technologies.
### 2. Prerequisites/Preparation
- **Dependencies**:
  - Pip install command with all required packages, always include `--upgrade` flag
  - After installing pip in Google Colab, always add this note:
```
> If you are using Google Colab, to enable dependencies just installed, you may need to **restart the runtime** (click on the "Runtime" menu at the top of the screen, and select "Restart session" from the dropdown menu).
```
- **API Keys**:
  - Instructions for obtaining API keys
  - Environment variable setup code block
  - Use placeholder format: `"sk-***********"` or `"***********"`

### 3. Main Content Sections
This is the main content of the tutorial. It should be divided into several hierarchical sections, each section should be a logical unit of the tutorial.

Before each code block, add a short introduction to the code block, which can avoid the reader to be confused about the code block.

(Optional) In the text description, if there are concepts or terms that are not familiar to the reader, you can properly add links to the text.

At the end of the article, the conclusion section should be as simple as possible, such as several sentences to summarize the tutorial.

---
# Example

Below this divider, here is an example of a Milvus integration tutorial:
---

<a href="https://colab.research.google.com/github/milvus-io/bootcamp/blob/master/integration/langchain/rag_with_milvus_and_langchain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>   <a href="https://github.com/milvus-io/bootcamp/blob/master/integration/langchain/rag_with_milvus_and_langchain.ipynb" target="_blank">
    <img src="https://img.shields.io/badge/View%20on%20GitHub-555555?style=flat&logo=github&logoColor=white" alt="GitHub Repository"/>
</a>


# Retrieval-Augmented Generation (RAG) with Milvus and LangChain

This guide demonstrates how to build a Retrieval-Augmented Generation (RAG) system using LangChain and Milvus.

The RAG system combines a retrieval system with a generative model to generate new text based on a given prompt. The system first retrieves relevant documents from a corpus using Milvus, and then uses a generative model to generate new text based on the retrieved documents.

[LangChain](https://www.langchain.com/) is a framework for developing applications powered by large language models (LLMs). [Milvus](https://milvus.io/) is the world's most advanced open-source vector database, built to power embedding similarity search and AI applications.


## Prerequisites

Before running this notebook, make sure you have the following dependencies installed:

```python
! pip install --upgrade langchain langchain-core langchain-community langchain-text-splitters langchain-milvus langchain-openai bs4
```

> If you are using Google Colab, to enable dependencies just installed, you may need to **restart the runtime** (click on the "Runtime" menu at the top of the screen, and select "Restart session" from the dropdown menu).

We will use the models from OpenAI. You should prepare the [api key](https://platform.openai.com/docs/quickstart) `OPENAI_API_KEY` as an environment variable.

```python
import os

os.environ["OPENAI_API_KEY"] = "sk-***********"
```

## Prepare the data

We use the Langchain WebBaseLoader to load documents from web sources and split them into chunks using the RecursiveCharacterTextSplitter.

```python
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create a WebBaseLoader instance to load documents from web sources
loader = WebBaseLoader(
    web_paths=(
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    ),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
# Load documents from web sources using the loader
documents = loader.load()
# Initialize a RecursiveCharacterTextSplitter for splitting text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

# Split the documents into chunks using the text_splitter
docs = text_splitter.split_documents(documents)

# Let's take a look at the first document
docs[1]
```

As we can see, the document is already split into chunks. And the content of the data is about the AI agent.

## Build RAG chain with Milvus Vector Store

We will initialize a Milvus vector store with the documents, which load the documents into the Milvus vector store and build an index under the hood.

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vectorstore = Milvus.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_args={
        "uri": "./milvus_demo.db",
    },
    # drop_old=True,  # Drop the old Milvus collection if it exists
)
```

> For the `connection_args`:
> - Setting the `uri` as a local file, e.g.`./milvus.db`, is the most convenient method, as it automatically utilizes [Milvus Lite](https://milvus.io/docs/milvus_lite.md) to store all data in this file.
> - If you have large scale of data, you can set up a more performant Milvus server on [docker or kubernetes](https://milvus.io/docs/quickstart.md). In this setup, please use the server uri, e.g.`http://localhost:19530`, as your `uri`.
> - If you want to use [Zilliz Cloud](https://zilliz.com/cloud), the fully managed cloud service for Milvus, adjust the `uri` and `token`, which correspond to the [Public Endpoint and Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) in Zilliz Cloud.

Search the documents in the Milvus vector store using a test query question. Let's take a look at the top 1 document.

```python
query = "What is self-reflection of an AI Agent?"
vectorstore.similarity_search(query, k=1)
```

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Initialize the OpenAI language model for response generation
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Define the prompt template for generating AI responses
PROMPT_TEMPLATE = """
Human: You are an AI assistant, and provides answers to questions by using fact based and statistical information when possible.
Use the following pieces of information to provide a concise answer to the question enclosed in <question> tags.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

<question>
{question}
</question>

The response should be specific and use statistics or numbers when possible.