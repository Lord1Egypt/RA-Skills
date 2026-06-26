# 大模型RAG实战｜向量数据库：Elasticsearch实现混合检索（附完整代码）

原文链接：https://mp.weixin.qq.com/s/CB5PZbvdzjxDmewnkbyN_w?token=1267526467&lang=zh_CN

大模型 RAG 实战系列文章，带你深入探索使用 LlamaIndex 框架，构建本地大模型知识库问答系统。本系列涵盖知识库管理、检索优化、模型本地部署等主题，通过代码与实例，讲解如何打造生产级系统，实现本地知识库的快速检索与智能问答。

此前文章中，我介绍了使用 LlamaIndex，如何构建知识库，实现各类文档和网页的加载、转换、索引与存储。当时，我们采用的向量数据库是 Chroma，作为 LlamaIndex 中的向量存储（Vector Store）。Chroma 是一个非常简单易用的嵌入式向量数据库，在开发和测试场景非常受欢迎。但是，如果是生产级系统，我们必须考虑能力更强、可扩展的向量数据库，比如国内使用较多的 Milvus，以及国外使用较多的 Weaviate。

LlamaIndex 支持超过 20 种向量数据库，在官网文档上给出了列表，并标注了各个向量数据库是否支持下列 5 个特性，包括：元数据过滤、混合检索、可删除、文档存储、支持异步。详情请参考官方文档：https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/

## 1 选择向量数据库

我的前一篇文章《QAnything 技术栈解析》中提到，QAnything 采用了混合检索技术，提升检索的准确性。最初，QAnything 使用了 Milvus 做向量存储和向量语义检索，后来引入了 Elasticsearch 做 BM25 关键词检索，从而实现了混合检索。

Elasticsearch 作为一个分布式的搜索和数据分析引擎，在全文检索和海量非结构化数据存储等场景，已经得到了广泛应用。现在，Elasticsearch 也可以用于向量存储，并支持以上包括混合检索在内的全部 5 个特性。因此，在生产环境，使用 Elasticsearch 作为向量数据库并使用其混合检索功能，是一个合适的选择。

系统技术栈如下表所示：

| 组件 | 选择 |
| --- | --- |
| 数据框架 | LlamaIndex |
| 前端框架 | Streamlit |
| 大模型工具 | Ollama |
| 大模型 | Gemma 2B |
| 嵌入模型 | BAAI/bge-small-zh-v1.5 |
| 文本分割器 | SpacyTextSplitter |
| 文档存储 | MongoDB |
| 向量存储 | ElasticSearch |

以下，我将结合代码实例，讲解如何在 LlamaIndex 框架中使用 Elasticsearch，并给出一套完整可运行的本地知识库问答系统。

## 2 代码实现示例

### 示例1：安装和配置 ES

我们使用 ES 做向量存储（Vector Stores）。首先，使用 ES 官方 Docker 镜像，在本机安装和运行 ES：

```bash
docker run -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.license.self_generated.type=trial" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.2
```

然后，配置 ES，作为向量数据库，并通过 retrieval_strategy 配置使用混合检索（hybrid=true）：

```python
from llama_index.vector_stores.elasticsearch import AsyncDenseVectorStrategy
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

ES_URI = "http://localhost:9200"

es_vector_store = ElasticsearchStore(
    es_url=ES_URI,
    index_name="my_index",
    retrieval_strategy=AsyncDenseVectorStrategy(hybrid=True),  # 使用混合检索
)
```

### 示例2：配置 MongoDB

我们选用 MongoDB 做文档存储（Document Stores）和索引存储（Index Stores）。你可以通过 Docker 安装和运行 MongoDB，然后做如下代码配置：

```python
from llama_index.core import StorageContext
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore

MONGO_URI = "mongodb://localhost:27017"

mongo_doc_store = MongoDocumentStore.from_uri(uri=MONGO_URI)
mongo_index_store = MongoIndexStore.from_uri(uri=MONGO_URI)

storage_context = StorageContext.from_defaults(
    docstore=mongo_doc_store,
    index_store=mongo_index_store,
    vector_store=es_vector_store,
)
```

### 示例3：配置本地模型

请到 https://ollama.com 安装 Ollama，并下载大模型，比如：Llama 3, Phi 3, Mistral, Gemma 等。为了测试方便，我们选用速度更快、效果较好的 Gemma 2B 模型，共 1.7GB：

```python
from llama_index.llms.ollama import Ollama

llm_ollama = Ollama(model="gemma:2b", request_timeout=600.0)
```

嵌入模型我们继续使用智源的 BAAI/bge-small-zh-v1.5：

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

bge_embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")
```

第一次运行时会自动从 Hugging Face 下载模型，请提前设置使用国内镜像站点：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

将配置好的大模型和嵌入模型，挂载在 LlamaIndex 全局设置上：

```python
from llama_index.core import Settings

Settings.llm = llm_ollama
Settings.embed_model = bge_embed_model
```

### 示例4：配置文本分割器

文本分割器 Spacy 对中文支持较好。我们可以通过 Langchain 引入和使用：

```python
from llama_index.core.node_parser import LangchainNodeParser
from langchain.text_splitter import SpacyTextSplitter

spacy_text_splitter = LangchainNodeParser(
    SpacyTextSplitter(
        pipeline="zh_core_web_sm",
        chunk_size=512,
        chunk_overlap=128,
    )
)
```

### 示例5：加载网页信息

此前文章介绍过，我们可以用 LlamaIndex 的 SimpleDirectoryReader 读取本地文件夹“data”中的文件：

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(input_dir="./data", recursive=True).load_data()
print(f"Loaded {len(documents)} Files")
```

为了测试方便，本程序中，我们用 SimpleWebPageReader 读取网页信息：

```python
from llama_index.readers.web import SimpleWebPageReader

pages = [
    "https://mp.weixin.qq.com/s/prnDzOQ8HjUmonNp0jhRfw",
]

documents = SimpleWebPageReader(html_to_text=True).load_data(pages)
print(f"Loaded {len(documents)} Web Pages")
```

### 示例6：配置数据转换管道

通过配置数据转换管道，可以实现数据转换并行处理以及知识库的去重，即默认的策略为更新插入（upserts）：

```python
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        spacy_text_splitter,
        bge_embed_model,
    ],
    docstore=mongo_doc_store,
    vector_store=es_vector_store,
)
```

接下来，运行数据转换管道，将分片后的文本向量化之后，存储到 Elasticsearch 向量数据库中：

```python
nodes = pipeline.run(documents=documents)
print(f"Ingested {len(nodes)} Nodes")
print(f"Load {len(pipeline.docstore.docs)} documents into docstore")
```

### 示例7：创建索引

然后，基于上述生成的 nodes，创建向量存储索引：

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex(nodes, storage_context=storage_context)
```

### 示例8：定制中文 Prompt 模板

为了避免大模型用英文回答中文问题，我们需要定制 LlamaIndex 的 Prompt 模板：

```python
from llama_index.core import PromptTemplate

text_qa_template_str = (
    "以下为上下文信息\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "请根据上下文信息回答我的问题或回复我的指令。前面的上下文信息可能有用，也可能没用，你需要从我给出的上下文信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。我的问题或指令是什么语种，你就用什么语种回复。\n"
    "问题：{query_str}\n"
    "你的回复："
)
text_qa_template = PromptTemplate(text_qa_template_str)
```

### 示例9：创建查询引擎

基于索引，创建查询引擎（Query Engine）。现在，可以针对知识库中的内容进行提问了：

```python
query_engine = index.as_query_engine(
    text_qa_template=text_qa_template,
    top_k=1,
)

your_question = "什么是流程？"
print(f"问题：{your_question}")

response = query_engine.query(your_question)
print(f"回答：{response}")
```

### 示例10：前端 UI 使用 Streamlit

我们使用 Streamlit 构建一个 Web UI，用于对话：

```python
import streamlit as st

TITLE = "本地大模型知识库问答"

st.set_page_config(
    page_title=TITLE,
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.header(TITLE)
st.info("By 大卫", icon="📃")

if "messages" not in st.session_state.keys():  # 初始化聊天历史记录
    st.session_state.messages = [
        {"role": "assistant", "content": "关于文档里的内容，请随便问"}
    ]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
```

以上全部代码，合起来形成一个文件 app.py，可以通过以下命令运行：

```bash
streamlit run app.py
```

请注意提前通过 pip 命令，安装 llama-index、streamlit、zh-core-web-sm、html2text 等本程序运行所需的组件。

参考资料：

- https://docs.llamaindex.ai/en/stable/examples/vector_stores/ElasticsearchIndexDemo/
- https://docs.llamaindex.ai/en/stable/examples/docstore/MongoDocstoreDemo/
