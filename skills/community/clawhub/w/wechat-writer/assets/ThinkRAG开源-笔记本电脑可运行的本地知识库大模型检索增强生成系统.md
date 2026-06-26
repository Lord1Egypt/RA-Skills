# ThinkRAG开源！笔记本电脑可运行的本地知识库大模型检索增强生成系统

原文链接：https://mp.weixin.qq.com/s/VmnVwDyi0i6qkBEzLZlERQ?token=1267526467&lang=zh_CN

ThinkRAG 大模型检索增强生成系统，可以轻松部署在笔记本电脑上，实现本地知识库智能问答。该系统基于 LlamaIndex 和 Streamlit 构建，针对国内用户在模型选择、文本处理等诸多领域进行了优化。

## 1 项目地址

ThinkRAG 在 Github 开源，使用 MIT 协议。你可以通过以下网址或点击“阅读原文”，获取代码和文档，在笔记本电脑上运行和使用：

- https://github.com/wzdavid/ThinkRAG

## 2 模型支持

ThinkRAG 可使用 LlamaIndex 数据框架支持的所有模型。关于模型列表信息，请参考以下文档：

- https://docs.llamaindex.ai/en/stable/module_guides/models/llms/modules/

现在，RAG 框架太多，好用的系统太少。ThinkRAG 致力于打造一个直接能用、有用、易用的应用系统。因此，在各种模型、组件与技术上，我们做了精心的选择与取舍。

首先，使用大模型，ThinkRAG 支持 OpenAI API 以及所有兼容的 LLM API，包括国内主流大模型厂商，例如：

- 智谱（Zhipu）
- 月之暗面（Moonshot）
- 深度求索（DeepSeek）

如果要本地化部署大模型，ThinkRAG 选用了简单易用的 Ollama。我们可以通过 Ollama 将大模型下载到本地运行。目前 Ollama 支持几乎所有主流大模型本地化部署，包括 Llama、Gemma、GLM、Mistral、Phi、Llava 等。更多信息可访问：

- https://ollama.com/

系统也使用了嵌入模型和重排模型，可支持来自 Hugging Face 的大多数模型。目前，ThinkRAG 主要选用了 BAAI 的 BGE 系列模型。国内用户可访问如下网址了解和下载：

- https://hf-mirror.com/BAAI

## 3 系统特点

ThinkRAG 是为专业人士、科研人员、学生等知识工作者开发的大模型应用系统，可在笔记本电脑上直接使用，且知识库数据都保存在电脑本地。ThinkRAG 具备以下特点：

- LlamaIndex 框架的完整应用开发模式
- 支持本地文件存储，无需安装任何数据库
- 无需 GPU 支持，即可在笔记本电脑上运行
- 支持本地部署的模型和离线使用

特别地，ThinkRAG 还为国内用户做了大量定制和优化：

- 使用 Spacy 文本分割器，更好地处理中文字符
- 采用中文标题增强功能
- 使用中文提示词模板进行问答和细化过程
- 默认支持国内大模型厂商（智谱、月之暗面、深度求索等）
- 使用双语嵌入模型（如 BAAI/bge-large-zh-v1.5）

## 4 快速开始

### 第1步 下载与安装

从 Github 下载代码后，用 pip 安装所需组件：

```bash
pip3 install -r requirements.txt
```

若要离线运行系统，请首先从官网下载 Ollama。然后，使用 Ollama 命令下载如 GLM、Gemma 和 QWen 等大模型。

同步，从 Hugging Face 将嵌入模型（BAAI/bge-large-zh-v1.5）和重排模型（BAAI/bge-reranker-base）下载到 localmodels 目录中。具体步骤可参考 docs 目录下文档：

- https://github.com/wzdavid/ThinkRAG/blob/main/docs/HowToDownloadModels.md

### 第2步 系统配置

为了获得更好的性能，推荐使用千亿级参数的商用大模型 LLM API。首先，从 LLM 服务商获取 API 密钥，配置如下环境变量：

```bash
ZHIPU_API_KEY=""
MOONSHOT_API_KEY=""
DEEPSEEK_API_KEY=""
OPENAI_API_KEY=""
```

你可以跳过这一步，在系统运行后，再通过应用界面配置 API 密钥。如果选择使用其中一个或多个 LLM API，请在 config.py 配置文件中删除不再使用的服务商。当然，你也可以在配置文件中，添加兼容 OpenAI API 的其他服务商。

ThinkRAG 默认以开发模式运行。在此模式下，系统使用本地文件存储，你不需要安装任何数据库。若要切换到生产模式，你可以按照以下方式配置环境变量：

```bash
THINKRAG_ENV=production
```

在生产模式下，系统使用向量数据库 Chroma 和键值数据库 Redis。如果你没有安装 Redis，建议通过 Docker 安装，或使用已有的 Redis 实例。请在 config.py 文件里配置 Redis 实例的参数信息。

### 第3步 运行系统

现在，你已经准备好运行 ThinkRAG。请在包含 app.py 文件的目录中运行以下命令：

```bash
streamlit run app.py
```

系统将运行，并在浏览器上自动打开以下网址，展示应用界面：

- http://localhost:8501/

第一次运行可能会需要等待片刻。如果没有提前下载 Hugging Face 上的嵌入模型，系统还会自动下载模型，将需要等待更长时间。

## 5 使用指南

### 5.1 系统配置

ThinkRAG 支持在用户界面，对大模型进行配置与选择，包括：

- 大模型 LLM API 的 Base URL 和 API 密钥
- 选择具体模型（例如智谱 glm-4）

系统将自动检测 API 和密钥是否可用；若可用，则在底部用绿色文字显示当前选择的大模型实例。

同样，系统可以自动获取 Ollama 下载的模型，用户可以在用户界面上选择所需的模型。若你已经将嵌入模型和重排模型下载到本地 localmodels 目录下，也可以在用户界面上切换选择使用的模型，并设置重排模型的参数（例如 Top N）。

在左侧导航栏点击高级设置（Settings-Advanced），还可以对下列参数进行设置：

- Top K
- Temperature
- System Prompt
- Response Mode

通过使用不同参数，我们可以对比大模型输出结果，找到最有效的参数组合。

### 5.2 管理知识库

ThinkRAG 支持上传 PDF、DOCX、PPTX 等各类文件，也支持上传网页 URL。点击 Browse files 按钮选择文件，然后点击 Load 按钮加载；此时会列出所有加载的文件。随后点击 Save 按钮，系统会对文件进行处理（文本分割与嵌入）并保存到知识库中。

系统支持对知识库进行管理：可分页列出知识库中所有文档；选择要删除的文档后，会出现 Delete selected documents 按钮，点击即可删除。

### 5.3 智能问答

在左侧导航栏点击 Query，将会出现智能问答页面。输入问题后，系统会对知识库进行检索并给出回答。在这个过程中，系统将采用混合检索和重排等技术，从知识库获取准确内容。

例如，我们已在知识库中上传了一个 Word 文档：“大卫说流程.docx”。现在输入问题：“流程有哪三个特征？”系统给出的回答是：流程具备目标性、重复性与过程性。同时，系统还给出了从知识库检索到的相关文档。

可以看到，ThinkRAG 完整和有效地实现了基于本地知识库的大模型检索增强生成能力。

## 6 技术架构

ThinkRAG 采用 LlamaIndex 数据框架开发，前端使用 Streamlit。系统的开发模式和生产模式分别选用了不同的技术组件，如下表所示：

| 模块 | 开发模式 | 生产模式 |
| --- | --- | --- |
| RAG 框架 | LlamaIndex | LlamaIndex |
| 前端框架 | Streamlit | Streamlit |
| 嵌入模型 | BAAI/bge-small-zh-v1.5 | BAAI/bge-large-zh-v1.5 |
| 重排模型 | BAAI/bge-reranker-base | BAAI/bge-reranker-large |
| 文本分割器 | SentenceSplitter | SpacyTextSplitter |
| 对话存储 | SimpleChatStore | Redis |
| 文档存储 | SimpleDocumentStore | Redis |
| 索引存储 | SimpleIndexStore | Redis |
| 向量存储 | SimpleVectorStore | Chroma |

这些技术组件，按照前端、框架、大模型、工具、存储、基础设施这六个部分进行架构设计。可参考在《大模型应用架构设计》一文，了解架构与技术细节。

## 7 后续开发计划

ThinkRAG 将继续优化核心功能，持续提升检索的效率和准确性，主要包括：

- 优化对文档和网页的处理，支持多模态知识库和多模态检索
- 构建知识图谱，通过知识图谱增强检索，并基于图进行推理
- 通过智能体处理复杂场景，尤其是准确调用其他工具和数据，完成任务

同时，我们还将进一步完善应用架构、提升用户体验，主要包括：

- 设计：有设计感和极佳用户体验的用户界面
- 前端：基于 Electron、React、Vite 等技术，构建桌面客户端应用，为用户提供极致简洁的下载、安装和运行方式
- 后端：通过 FastAPI 提供接口，以及消息队列等技术提升整体性能和可扩展性

好事即将发生。如你有兴趣，欢迎加入 ThinkRAG 开源项目，一起打造用户喜爱的 AI 产品！请在公众号留言。感谢你的持续关注与支持！
