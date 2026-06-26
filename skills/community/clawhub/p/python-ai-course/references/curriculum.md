# AI 全栈教学导师 — 完整课程大纲

## 模块依赖关系图

```
M0(Python 强化)
    ├──→ M1(FastAPI 框架)
    └──→ M2(传统机器学习)
              └──→ M3(神经网络基础)
                        └──→ M4(深度学习实战)
                                  ├──→ M5(提示词工程)
                                  │         └──→ M6(RAG 系统)
                                  │                   └──→ M9(智能体开发)
                                  ├──→ M7(大模型微调)
                                  ├──→ M8(小模型训练)
                                  └──→ M10(AI 工具落地)
```

**注：** M5（提示词工程）可从 L2 提前学习，不强依赖 M4；M10 可与其他模块并行。

---

## 推荐学习路径

### L1 入门探索者（建议 8-12 周）
```
M0(全部) → M1(M1.1-M1.3) → M2(M2.1-M2.3) → M5(M5.1-M5.2) → M10(M10.1)
```
里程碑：能用 FastAPI 搭建 AI 服务，能调用 LLM API，能理解机器学习基本流程

### L2 基础实践者（建议 6-10 周）
```
M1(M1.4-M1.5，选修) → M3(全部) → M4(M4.1-M4.4) → M5(全部) → M6(M6.1-M6.3) → M10
```
里程碑：能独立搭建 RAG 系统，理解 Transformer 架构，掌握高级 Prompt 技巧

### L3 进阶开发者（建议 8-12 周）
```
M4(M4.4-M4.5，复习强化) → M5(M5.3-M5.4) → M6(全部) → M7(M7.1-M7.3) → M9(M9.1-M9.4) → M10(M10.2-M10.4)
```
里程碑：能微调开源大模型，能开发生产级 RAG 系统，能构建多工具 Agent

### L4 高阶工程师（建议 6-8 周，专精方向选择）
```
方向A（生产部署）：M6(深化) → M7(M7.4-M7.5) → M8 → M10(M10.3-M10.4)
方向B（Agent 专精）：M9(全部) → M6(深化) → M10(工程化)
方向C（从零训练）：M8(全部) → M7(全部) → M4(深化)
```

---

## M0：Python 语法强化（L1 必修，L2 选修复习）

> **使用 show_widget 绘制**：Python 核心语法脑图（数据类型 → 控制流 → 函数 → OOP → 进阶特性 → 异步）

### M0.1 Python 核心语法
- 数据类型：str / list / dict / set / tuple，可变与不可变
- 控制流：if-elif-else / for / while / 列表推导式 / 字典推导式
- 函数：def、参数类型（位置/关键字/默认值）、*args/**kwargs、lambda
- 异常处理：try/except/finally/raise，自定义异常类
- 文件操作：with open、pathlib.Path、读写 JSON/CSV
- **实战项目**：命令行 ToDo 应用（增删查改 + JSON 持久化）

### M0.2 面向对象编程
- 类和对象：`__init__`、self、实例方法 vs 类方法 vs 静态方法
- 继承与多态：`super()`、方法重写、鸭子类型
- 魔术方法：`__str__`、`__repr__`、`__len__`、`__eq__`、`__hash__`
- 数据类：`@dataclass`，简化 DTO 写法
- **实战项目**：学生成绩管理系统（支持排序、统计、导出 CSV）

### M0.3 Python 进阶特性
- 迭代器与生成器（`yield`、`yield from`）
- 装饰器：`@property`、`@staticmethod`、`@classmethod`、自定义装饰器
- 上下文管理器：with 协议、`contextlib.contextmanager`
- 类型注解：`typing` 模块（List、Dict、Optional、Union、TypeVar）
- **实战项目**：带缓存装饰器 + 类型注解的 API 调用封装器

### M0.4 异步编程
- asyncio 基础：`async/await`、事件循环、协程
- 并发 vs 并行 vs 异步（图示区分三者模型）
- `asyncio.gather` 并发执行多个协程
- aiohttp 异步 HTTP 请求
- **实战项目**：异步并发爬取多个 URL，对比同步耗时

### M0.5 常用科学计算库
- NumPy：数组创建、索引切片、广播规则、矩阵运算（用图示讲解广播）
- Pandas：DataFrame CRUD、数据清洗（缺失值/重复值）、groupby、merge
- Matplotlib / Seaborn：折线图、散点图、热力图、子图布局
- **实战项目**：分析 MovieLens 数据集，输出可视化报告

---

## M1：FastAPI 框架（L1-L2，AI 后端服务基础）

> **使用 show_widget 绘制**：FastAPI 请求处理流程图（Request → 路由 → 依赖注入 → 业务逻辑 → Response）

### M1.1 FastAPI 快速入门
- 路由装饰器：GET / POST / PUT / DELETE / PATCH
- 路径参数（Path）、查询参数（Query）、请求体（Body）
- Pydantic 数据模型：字段验证、默认值、自定义 validator
- 自动文档：Swagger UI（/docs）和 ReDoc（/redoc）
- **实战项目**：用户信息 CRUD API（内存存储版）

### M1.2 依赖注入与中间件
- Depends 依赖注入系统：共享数据库连接、认证逻辑复用
- JWT 认证中间件（使用 python-jose）
- CORS 中间件配置
- 全局异常处理：`@app.exception_handler`
- **实战项目**：带 JWT 认证的 API 服务

### M1.3 数据库集成
- SQLAlchemy 2.0 ORM（异步版本）
- Alembic 数据库迁移
- Repository 模式封装数据访问层
- **实战项目**：博客 API（文章 + 标签 + 用户，完整 CRUD）

### M1.4 AI 模型服务化
- 将 ML/DL 模型封装为 REST API（避免重复加载模型的最佳实践）
- 异步推理请求处理（避免阻塞事件循环）
- 流式响应：Server-Sent Events（SSE）实现打字机效果
- WebSocket 实时双向通信
- **实战项目**：封装 LLM 调用为流式 API 服务（OpenAI 兼容格式）

### M1.5 部署与生产化
- Uvicorn（开发）/ Gunicorn（生产）配置
- Docker 容器化：多阶段构建优化镜像大小
- 健康检查端点设计
- 环境变量管理（python-dotenv / pydantic-settings）
- **实战项目**：Docker 部署完整 AI API 服务（含 nginx 反代配置）

---

## M2：传统机器学习（L1-L3）

> **使用 show_widget 绘制**：机器学习完整流程图（数据收集 → 特征工程 → 模型选择 → 训练 → 评估 → 部署）

### M2.1 机器学习概述
- 监督学习 / 无监督学习 / 半监督学习 / 强化学习（四象限图示）
- 训练集、验证集、测试集划分原则（为何不能用测试集调参）
- 过拟合与欠拟合（学习曲线图示）
- K 折交叉验证（图示讲解原理）
- **实战项目**：波士顿房价预测（线性回归完整流程）

### M2.2 经典算法
- 线性回归 & 逻辑回归（从公式到直觉理解）
- 决策树（信息增益 / 基尼系数图示）
- 随机森林（为何 Bagging 有效：方差 vs 偏差）
- SVM（支持向量机，核技巧直觉理解）
- KMeans 聚类（图示展示聚类过程）
- **实战项目**：Iris 花卉数据集 — 5 种算法横向对比

### M2.3 特征工程
- 缺失值处理：删除 / 均值填充 / 中位数填充 / 模型预测填充
- 特征缩放：标准化（StandardScaler）/ 归一化（MinMaxScaler）— 何时用哪个
- 特征编码：One-Hot / Label Encoding / Target Encoding
- 特征选择：相关性矩阵热力图、特征重要性
- 降维：PCA 原理（用图示讲解"找最大方差方向"）
- **实战项目**：Titanic 生存预测（完整特征工程流水线）

### M2.4 模型评估与优化
- 分类指标：Accuracy / Precision / Recall / F1 / ROC-AUC（混淆矩阵图示）
- 回归指标：MSE / RMSE / MAE / R²
- 超参数调优：GridSearchCV / RandomizedSearchCV / Optuna（贝叶斯优化）
- **实战项目**：垃圾邮件分类器（TF-IDF + 多算法对比 + 超参数优化）

---

## M3：神经网络基础（L2-L3）

> **使用 show_widget 绘制**：多层感知机结构图（输入层 → 隐藏层 × N → 输出层，带权重和激活函数标注）

### M3.1 感知机与前向传播
- 神经元生物类比 → 数学模型（权重、偏置、激活函数）
- 前向传播逐步计算（用具体数字示例演示）
- 多层网络的表达能力（为何需要非线性激活）
- **show_widget**：动态展示前向传播计算流程

### M3.2 反向传播与梯度下降
- 链式法则直觉理解（用计算图讲解，避免纯符号堆砌）
- 梯度下降变体对比：SGD / Mini-batch GD / Adam / RMSprop / AdamW
- 学习率的作用（过大 vs 过小的图示对比）
- 学习率调度（Cosine Annealing、WarmUp）
- **实战**：用 NumPy 手写一个两层神经网络，实现前向 + 反向传播

### M3.3 激活函数
- Sigmoid（梯度消失问题图示）
- Tanh（Sigmoid 的改进）
- ReLU（死神经元问题）/ Leaky ReLU / ELU
- GELU（Transformer 常用，与 ReLU 的区别）
- 选择激活函数的实用指南

### M3.4 正则化技术
- Dropout（训练 vs 推理行为不同，图示说明）
- Batch Normalization（原理 + 为什么有效）
- L1 / L2 正则化（稀疏性 vs 权重缩小）
- Early Stopping
- **实战项目**：MNIST 手写数字识别 — 纯 NumPy 实现，对比有无正则化的效果

---

## M4：深度学习实战（L2-L4）

> **使用 show_widget 绘制**：PyTorch 训练完整生命周期（Dataset → DataLoader → Model → Loss → Backward → Optimizer → 验证）

### M4.1 PyTorch 核心
- Tensor 创建与操作（与 NumPy 的互转）
- 自动求导：`requires_grad`、`backward()`、`detach()`
- Dataset / DataLoader（自定义 Dataset 类模板）
- `nn.Module` 自定义模型（`__init__` + `forward`）
- 标准训练循环（含验证、模型保存、断点续训）
- **实战项目**：PyTorch 版 MNIST 分类器

### M4.2 卷积神经网络（CNN）
- 卷积操作直觉（用动画图示讲解感受野、步长、填充）
- 经典架构：LeNet → VGG → ResNet（残差连接解决梯度消失）
- 迁移学习：为何有效 + 冻结层 vs 微调层策略
- **实战项目**：猫狗分类（ResNet18 迁移学习 + 数据增强）

### M4.3 序列模型
- RNN 的梯度消失问题（时序图示）
- LSTM：遗忘门/输入门/输出门（门控机制图示）
- GRU：LSTM 的简化版本
- **实战项目**：中文文本情感分类（LSTM 版本）

### M4.4 Transformer 架构（重点）

> **使用 show_widget 绘制**：Transformer Encoder-Decoder 完整架构图，标注每个子模块

- Self-Attention 机制：Q/K/V 计算步骤（逐步图解）
- 缩放点积注意力：为何要除以 √d_k
- Multi-Head Attention：多个注意力头并行的意义
- Position Encoding：为何需要位置编码（自注意力无序性的问题）
- Layer Normalization vs Batch Normalization（选择原因）
- 前馈网络（FFN）在 Transformer 中的作用
- **实战项目**：从零实现简单 Transformer（用于文本分类）

### M4.5 预训练语言模型
- BERT：Masked Language Model + NSP 预训练任务
- GPT 系列：自回归语言建模，从 GPT-1 到 GPT-4 的架构演进
- HuggingFace Transformers：`AutoModel`、`AutoTokenizer`、`pipeline`
- 微调范式：全量微调 vs 特征提取
- **实战项目**：用 BERT 做中文新闻文本分类

---

## M5：提示词工程（L2-L4）

> **使用 show_widget 绘制**：提示词工程技术层次图（基础 → 中级 → 高级 → 系统级）

### M5.1 提示词基础
- 大模型工作原理：Token、BPE 分词、上下文窗口
- 消息角色：System / User / Assistant（实际作用与最佳实践）
- 温度（temperature）、top_p、frequency_penalty 参数调优指南
- **实战**：设计 10 个不同场景的提示词，对比参数变化的影响

### M5.2 核心提示技巧
- Zero-shot vs Few-shot Prompting（何时用哪种）
- Chain-of-Thought（CoT）：标准 CoT vs 零样本 CoT（"Let's think step by step"）
- Role Prompting：角色设定的真实效果与局限
- 输出格式控制：强制 JSON、Markdown 表格输出
- **实战项目**：用 CoT 构建一个数学推理解题器

### M5.3 高级提示策略
- Tree-of-Thought（ToT）：探索多条推理路径
- ReAct 框架：推理 + 行动交替执行
- Self-Consistency：多次采样投票提升稳定性
- 提示词注入防御：常见攻击模式与防御策略
- **实战项目**：构建多步骤推理的提示词链（用于复杂问题分解）

### M5.4 结构化输出与工具调用
- Function Calling / Tool Use：概念 + OpenAI API 调用示例
- JSON Schema 约束输出：定义工具参数格式
- 实战对接：OpenAI / 文心一言 / 通义千问 API
- Prompt 模板管理：LangChain PromptTemplate
- **实战项目**：搭建一个结构化信息提取系统（从非结构化文本提取 JSON）

---

## M6：RAG 系统开发（L3-L4）

> **使用 show_widget 绘制**：RAG 完整架构图（离线索引流程 + 在线检索生成流程）

### M6.1 RAG 核心原理
- 为什么需要 RAG：幻觉问题、知识截止日期、隐私数据处理
- 朴素 RAG vs 高级 RAG vs 模块化 RAG 对比
- RAG 与微调的选择决策树（图示）
- **实战**：手绘 RAG 完整数据流图，理解每个环节的作用

### M6.2 文档处理与分块
- 文档加载器：PDF（pdfplumber）/ Markdown / Web（BeautifulSoup）/ Office 文档
- 分块策略对比：
  - 固定窗口分块（简单但破坏语义）
  - 递归字符分块（LangChain 推荐）
  - 语义分块（基于相似度）
  - 层级分块（保留文档结构）
- 分块大小与重叠设计的经验法则
- **实战项目**：将技术文档 PDF 处理为高质量检索语料库

### M6.3 向量嵌入
- Embedding 模型选择指南：
  - OpenAI text-embedding-3-small/large（在线）
  - BGE（BAAI，开源中文优化版）
  - Nomic-embed（开源高性价比）
- 向量数据库对比：Chroma（本地开发）/ Faiss（高性能）/ Milvus（生产级）/ Pinecone（云托管）
- 相似度搜索：余弦相似度 vs 欧氏距离 vs 内积（使用场景对比）
- **实战项目**：构建本地技术文档知识库并实现语义搜索

### M6.4 检索优化
- 混合检索：稠密检索（向量）+ 稀疏检索（BM25）的融合策略
- 重排序（Reranker）：BGE-reranker 使用方法
- 查询改写与扩展（HyDE：假设文档嵌入）
- 多查询检索：从不同角度生成多个查询
- **实战项目**：对比 4 种检索策略在同一数据集上的准确率

### M6.5 RAG 完整系统
- LangChain LCEL 链式构建
- 对话历史管理（ConversationBufferMemory vs 摘要记忆）
- 引用溯源：返回检索到的原始段落
- RAG 评估框架：RAGAS（Faithfulness / Answer Relevancy / Context Recall）
- **项目**：基于私有文档的企业知识库问答系统（完整实现，含评估报告）

---

## M7：大模型微调（L3-L4）

> **使用 show_widget 绘制**：微调技术全景图（全量微调 → LoRA → QLoRA → Prefix Tuning，标注参数量和显存需求）

### M7.1 微调决策框架
- 微调 vs RAG vs Prompt 工程 — 三者如何选择（决策流程图）
- 微调数据集质量标准：多样性、一致性、数量估算
- 微调类型：全量微调（Full Fine-tuning）/ 参数高效微调（PEFT）

### M7.2 PEFT 参数高效微调
- LoRA 原理：低秩矩阵分解图示（W = W₀ + BA，B 和 A 的维度分析）
- QLoRA：INT4 量化 + LoRA，单卡可跑 70B 模型的原理
- Prefix Tuning / Prompt Tuning（轻量但效果有限）
- PEFT 库使用：`get_peft_model`、`LoraConfig` 配置详解
- **实战项目**：用 LoRA 微调 Qwen2-1.5B（本地可运行）

### M7.3 监督微调（SFT）
- 数据格式标准：Alpaca / ShareGPT / ChatML 格式对比
- 数据清洗脚本（去重、质量过滤）
- 训练框架对比：LLaMA-Factory（推荐）/ Axolotl / ms-swift
- 关键超参数：batch_size、gradient_accumulation、learning_rate、epoch、warmup
- 训练监控：Loss 曲线解读，判断训练是否正常
- **实战项目**：用 1000 条对话数据微调一个专业领域客服模型

### M7.4 RLHF 与对齐（概念 + 方向指引）
- 奖励模型（Reward Model）训练流程
- PPO 强化学习：为何在 LLM 微调中难以稳定
- DPO（Direct Preference Optimization）：更简洁的偏好对齐
- 实际落地建议：入门优先用 DPO，成本低效果好

### M7.5 模型评估与部署
- 评估指标：BLEU / ROUGE / 困惑度（Perplexity）/ 人工评估（Elo 评分）
- 模型量化：GPTQ（INT4）/ AWQ / GGUF（llama.cpp 格式）
- 部署方案：vLLM（高吞吐生产）/ Ollama（本地开发）/ TGI
- **实战项目**：将微调模型量化为 GGUF，用 Ollama 本地部署并对比基准性能

---

## M8：小模型训练（L3-L4）

> **使用 show_widget 绘制**：从零训练 GPT 的完整流程图（数据 → 分词 → 预训练 → 评估）

### M8.1 从零训练的时机判断
- 何时从零训练 vs 微调（数据量 / 领域差异 / 成本三角决策）
- 数据量需求估算：参数量 × 20 为经验下限（Chinchilla 定律）
- 计算资源规划：FLOPs 估算、GPU 小时预算

### M8.2 分词器训练
- BPE（Byte Pair Encoding）算法图示
- WordPiece / SentencePiece 对比
- 使用 tokenizers 库训练自定义词表
- **实战项目**：训练中文代码混合领域的自定义分词器

### M8.3 从零实现 GPT
- 用 PyTorch 实现 GPT-2 架构（Token Embedding + Position Embedding + N × Transformer Block + LM Head）
- 预训练目标：因果语言建模（CLM）
- 高效训练技巧：梯度累积、混合精度（AMP）、梯度裁剪
- **实战项目**：训练一个小型 GPT（约 10M 参数）用于特定领域文本生成

### M8.4 知识蒸馏
- 软标签蒸馏：温度系数的作用（图示讲解软标签分布）
- 特征蒸馏（中间层对齐）
- TinyBERT / DistilBERT 架构与蒸馏训练方案
- **实战项目**：将 BERT-base 蒸馏为 1/2 参数量的学生模型，对比性能损失

---

## M9：智能体开发（L3-L4）

> **使用 show_widget 绘制**：Agent 核心架构图（LLM 大脑 + 工具集 + 记忆系统 + 规划模块）

### M9.1 Agent 核心概念
- Agent = LLM（大脑）+ Tools（手）+ Memory（记忆）+ Planning（规划）
- ReAct 框架：Reasoning（推理）→ Acting（行动）→ Observation（观察）循环
- 工具调用（Function Calling）：从 JSON Schema 到实际调用
- **实战项目**：设计一个天气查询 + 日程安排 Agent（纸上设计 → 代码实现）

### M9.2 LangChain 框架实战
- LCEL（LangChain Expression Language）：声明式构建 Chain
- Agent 类型：OpenAI Functions Agent / ReAct Agent
- Tools 生态：内置工具（搜索/计算器/Python REPL）+ 自定义工具
- Memory 类型：ConversationBufferMemory / SummaryMemory / VectorStoreMemory
- **实战项目**：构建一个能搜索网页 + 读取文件的研究员 Agent

### M9.3 多智能体系统
- 多 Agent 协作模式：主从模式 / 平等协作 / 流水线模式（图示）
- AutoGen 框架：`AssistantAgent` + `UserProxyAgent` 基础用法
- CrewAI：基于角色的团队协作
- **实战项目**：代码编写 Agent + 代码审查 Agent + 测试 Agent 三方协作完成需求

### M9.4 Agent 工具开发
- 自定义工具规范：名称 / 描述（这是 LLM 选择工具的依据）/ 参数 Schema / 返回值
- MCP 协议（Model Context Protocol）：工具的标准化协议，兼容 WorkBuddy 等平台
- API 工具集成：REST API 封装为 Agent 工具的最佳实践
- **实战项目**：为 Agent 开发 3 个实用工具（数据库查询 + 文件操作 + 外部 API）

### M9.5 生产级 Agent
- 错误处理与回退机制（工具调用失败的处理策略）
- Agent 观测与调试：LangSmith Tracing 使用
- 成本控制：Token 缓存（语义缓存 GPTCache）、Token 预算限制
- **项目**：完整 AI 助手系统（具备搜索、知识库、代码执行、任务规划能力）

---

## M10：AI 工具落地（L2-L4，可与其他模块并行）

> **使用 show_widget 绘制**：AI 工具生态全景图（编码工具 / 工作流 / 向量数据库 / LLM 应用平台）

### M10.1 AI 编程工具
- Cursor 深度使用：`@codebase` / `@web`、Rules for AI、Composer 多文件编辑
- GitHub Copilot 最佳实践：注释驱动代码生成、快捷键熟练
- 提示词驱动开发（PDD）：先写需求注释，再让 AI 填充实现
- 实战：用 AI 工具在 30 分钟内完成一个完整 FastAPI 接口（含测试）

### M10.2 AI 工作流自动化
- n8n：可视化工作流编排，Webhook + 节点连接
- Dify：RAG + Agent 一体化应用开发平台
- FastGPT：知识库问答系统快速搭建
- 实战：搭建一个自动化新闻摘要 + 分发的工作流（Webhook 触发 → LLM 处理 → 推送）

### M10.3 向量数据库工程化
- 生产环境选型对比（Milvus / Weaviate / Pinecone / Qdrant）
- 数据更新策略：增量更新 vs 全量重建
- 性能优化：索引类型选择（HNSW / IVF）、批量写入

### M10.4 LLM 应用工程化
- 提示词版本管理：LangSmith Hub / PromptLayer
- A/B 测试框架：不同提示词/模型的效果对比
- 监控与告警：延迟、Token 消耗、错误率监控
- 成本优化策略：Router 模型（简单问题用便宜模型）、语义缓存
- **项目**：生产级 LLM 应用架构设计（完整 PRD + 架构图 + 成本估算）
