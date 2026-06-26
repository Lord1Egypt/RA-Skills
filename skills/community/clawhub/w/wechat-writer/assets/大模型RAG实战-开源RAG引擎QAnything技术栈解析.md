# 大模型RAG实战｜开源RAG引擎QAnything技术栈解析

原文链接：https://mp.weixin.qq.com/s/yn-7KdJgxcM6juBg5zqDRQ?token=1267526467&lang=zh_CN

近日，有道发布了 QAnything 1.4.1。这是一个开源的本地知识库 RAG 问答系统，支持用户上传多种格式的文档以构建知识库，并采用两阶段检索机制及混合检索技术，提升检索效率和准确性。

来源：https://qanything.ai/

在本文中，我将基于对源码的分析，介绍 QAnything 的技术栈，探索其背后采用的技术组件及实现方法。

## 1 加载 Loading

将各种格式的文件加载与解析成文档（Document），始终是构建大模型 RAG 系统最重要的环节。

QAnything 开源版本基于 LangChain 的文件解析组件，提供了一个较为全面的方案，可支持以下 10 种文件或网页的解析（PDF、DOCX、TXT、JPG 等）：

1. 网页 URL：构造 MyRecursiveUrlLoader，用来爬取指定网页及该网页上的子链接，并通过 LangChain 的 WebBaseLoader 加载和提取爬取到的网页内容。
2. Markdown 文件：直接使用 LangChain 的 UnstructuredFileLoader 处理 .md 文件。
3. TXT 文件：直接使用 LangChain 的 TextLoader 处理 .txt 文件。
4. PDF 文件：对 PDF 文件的处理相对复杂。系统构造 UnstructuredPaddlePDFLoader，按以下步骤处理：
   1. 使用 PyMuPDF（fitz）加载 PDF 文件
   2. 将加载的 PDF 文件中的每一页转成图片
   3. 通过 PaddleOCR 将图片识别成文本，输出到一个文本文件
   4. 使用 unstructured 库的 partition_text 处理该文本文件
5. JPG/JPEG/PNG 文件：图片首先通过 PaddleOCR 识别成文本，然后使用 UnstructuredFileLoader 加载。
6. DOCX 文件：直接使用 LangChain 的 UnstructuredWordDocumentLoader 处理。
7. XLSX 文件：原本直接使用 LangChain 的 UnstructuredExcelLoader，后来改为 pandas 的 read_excel 方法，将 Excel 文件中的每一个 sheet 处理并输出为 CSV 文件，然后构造 CSVLoader，将 CSV 文件的每一行内容以键值对的形式输出为一个 document。
8. CSV 文件：使用上述 CSVLoader 处理。
9. PPTX 文件：直接使用 LangChain 的 UnstructuredPowerPointLoader 处理。
10. EML 文件：直接使用 LangChain 的 UnstructuredEmailLoader 处理。

值得注意的是，以上文件加载与解析方式来自于开源版本。据官网称，其企业版针对所有文档类型做更精细的单独优化，解析结果均为 markdown 格式，可以更好地保留原有的结构。

## 2 转换 Transformation

此阶段将文件或网页 URL 加载解析后生成的文档（Document）分割为文本块（Chunk），步骤如下：

1. 中文文本分割：针对网页 URL、TXT、PDF、图片、DOCX 等，系统加载文件后，会基于 LangChain 的 CharacterTextSplitter 构造并使用 ChineseTextSplitter，其主要功能是根据中英文标点符号对文本进行切割。
2. 中文标题增强：如果开启中文标题增强（默认关闭），系统基于 LangChain Document 构建 zh_title_enhance。其功能为判断文字是否为标题；如果是标题，则将该文字的元数据标注为标题，并把后续文字与此标题关联。
3. 进一步分块：如果单个 Document 文本长度大于 800 tokens，则利用 LangChain 的 RecursiveCharacterTextSplitter 将其拆分成多个 Chunk，参数 chunk_size=400。
4. 添加元数据：每个文档 metadata 里注入来源文件信息，包括 file_id 和 file_name。

## 3 嵌入 Embedding

此阶段对上述转换分割好的文本块进行向量嵌入（Vector Embedding），并存储到向量数据库中，创建索引，以供未来检索。

1. 嵌入模型：QAnything 使用有道自研嵌入模型 bce-embedding-base_v1，可使用本地或线上版本。通过嵌入模型将每个文本块生成向量表示，保存到向量数据库中。
2. 向量数据库：系统使用 Milvus。系统把每个文本块的文本内容、对应的向量、以及文件 ID、文件名、文件路径等元数据信息保存到向量数据库中，以支持向量语义检索。
3. 关键词检索：如果开启混合检索，那么文本块的数据同时也需要保存在 ElasticSearch 中，以支持 BM25 关键词检索。
4. 知识库管理：系统采用 MySQL 存储知识库相关信息，主要有三个表：用户表、知识库表和文件表，以方便管理知识库。

## 4 检索 Retrieval

如何完整和准确地检索到问题相关的内容，是 RAG 系统的关键。QAnything 采用了两阶段检索：

### 4.1 第一阶段：混合检索

首先，针对查询中的关键字，通过 ElasticSearch 使用 BM25 算法检索，快速找到包含特定关键字的内容。同时，系统通过 Milvus 进行向量语义相似度检索，找到与查询语义最相关的文档部分（TOP_K）。系统将两次检索到的文档片段合并，交给第二阶段检索。

### 4.2 第二阶段：重排序

QAnything 通过一个重排（Rerank）步骤，结合前述混合检索结果，通过重排模型 bce-reranker-base_v1，对检索到的文档片段进行综合排序。重排可以优化检索结果的相关性，确保最终提供给大模型生成回答时，用的是最准确的信息。

## 5 生成 Generation

检索到准确的信息后，生成阶段的重点是大语言模型和相应的 Prompt 优化。

### 5.1 大语言模型（LLM）

QAnything 开源版本采用的是微调后的通义千问 Qwen 7B，由 FastChat 提供 API 服务。系统同时也支持其他与 OpenAI-API 兼容的大模型服务，包含 Ollama、通义千问 DashScope 等。

选择 Qwen 7B 作为基座模型的原因是：基座模型应支持中英文、至少具备 4K 上下文窗口，且能在单块 GPU 上部署；优先考虑 7B 以下参数规模，以便于未来在消费级硬件上部署。

进行微调的原因有两个：一是增强模型对含有专业术语或通俗缩写的理解，二是提升大模型在参考信息不足时的诚实度。

### 5.2 提示词（Prompt）

QAnything 采用的 Prompt 模板如下：

```text
参考信息：{context}
我的问题或指令：{question}
请根据上述参考信息回答我的问题或回复我的指令。前面的参考信息可能有用，也可能没用，你需要从我给出的参考信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。我的问题或指令是什么语种，你就用什么语种回复,你的回复：
```

可以看出，给出的指令比较清晰，适合 RAG 应用场景。

以上总结了 QAnything 从文件加载、转换、嵌入、索引、存储、检索到生成整个 RAG 链路所采用的技术组件与方法。如有兴趣进一步了解，建议你深入研究 QAnything 的源码。

项目源码：https://github.com/netease-youdao/QAnything
