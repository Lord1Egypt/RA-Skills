# 🌍 地球最权威 AI 全栈课程大纲（2026 行业版）

> 9 大层级 · 60+ 细分章节 · 4 级分级路径 · 每个阶段有可交付项目产出

---

## 📐 模块依赖关系（教学顺序铁律）

```
L1 编程基础 → L3 提示词工程
    ↓              ↓
L2 后端工程    L4 RAG检索增强
    ↓              ↓
L6 算法原理 → L5 模型微调 → L7 智能体开发
                                ↓
                          L8 项目实战落地
                                ↓
                          L9 行业前沿迭代
```

**关键依赖说明：**
- L6（算法原理）是 L5（模型微调）的 **硬前置** — 必须先懂 ML/DL 才能微调
- L4（RAG）和 L5（微调）可并行学习
- L7（智能体开发）依赖 L3+L4+L5 的综合基础
- L8（项目实战）建议学完 L2-L7 中至少 5 层后再进行
- L9（行业前沿）在 L2 阶段以概览形式引入，L3-L4 深入展开

---

## 🟢 L1 零基础小白 — 标准学习路径（预计 8-12 周）

### 阶段一：编程筑基（3-4 周）

#### C1.1 Python 快速上手
- 环境搭建详解（Python 3.10+ / VS Code / Jupyter / venv 虚拟环境）
- 变量与数据类型：int/float/str/bool + type() 排查技巧
- 运算符：算术/比较/逻辑/赋值/成员运算符
- 输入输出：input() / print() + f-string 格式化
- 实战项目：**命令行计算器**（支持 + - * / 四则运算）

#### C1.2 流程控制
- 条件判断：if / elif / else 多层嵌套最佳实践
- 循环结构：for in（range/列表/字典遍历）/ while + break/continue
- 实战项目：**学生成绩管理系统**（输入→判断等级→输出统计）

#### C1.3 数据结构精讲
- 列表：增删改查/切片/列表推导式/排序
- 元组：不可变特性/拆包/命名元组
- 字典：键值操作/get()安全取值/字典推导式
- 集合：去重/交并差集运算
- 实战项目：**Todo 命令行工具**（增删改查 + 状态标记）

#### C1.4 函数与模块化
- 函数定义与调用、参数传递（位置/关键字/默认值/*args/**kwargs）
- 返回值与作用域（local/global/nonlocal）
- 文件读写：open()/with 上下文管理器/CSV 处理
- 异常处理：try/except/else/finally 完整范式
- 实战项目：**文件批量重命名工具**

#### C1.5 面向对象编程
- 类与对象、__init__ 构造方法、self 理解
- 继承与多态（简单示例，不深入设计模式）
- 模块与包、pip 使用
- 实战项目：**简易图书管理系统**（OOP 设计）

#### C1.6 科学计算速通
- NumPy：ndarray 创建/索引切片/数学运算/广播机制
- Pandas：DataFrame 创建/筛选/分组聚合/合并
- Matplotlib：折线图/柱状图/散点图/子图布局
- 实战项目：**Kaggle Titanic 数据探索与可视化报告**

### 阶段二：AI 认知启蒙（2 周）

#### C2.1 AI/ML 概念地图
- 一张图讲清：AI ⊃ ML ⊃ DL ⊃ LLM 的包含关系
- 监督学习 / 无监督学习 / 强化学习 — 三种范式的核心差异
- 训练集/验证集/测试集 — 为什么要划分、划分比例经验值
- 过拟合 vs 欠拟合 — 图解直观理解
- 实战：**用 sklearn 跑第一个分类器**（鸢尾花数据集）

#### C2.2 LLM 与 Prompt 入门
- LLM 工作原理（直觉版：超大完形填空 → 对话助手）
- 基础 Prompt 五段式：角色 + 任务 + 约束 + 格式 + 示例
- Zero-Shot vs Few-Shot 对比体验
- 实战：**设计一个「代码审查助手」Prompt**

#### C2.3 AI 工具初体验
- ChatGPT/Claude/Kimi/通义千问 的正确使用姿势
- Cursor/Copilot 基础功能（代码补全/解释代码/重构）
- 实战：**用 AI 工具辅助完成一个 Python 小项目**

### 阶段三：能力进阶（3-4 周）

#### C3.1 FastAPI 入门到部署
- HTTP 基础概览（GET/POST/PUT/DELETE / 状态码）
- FastAPI 第一个应用（uvicorn 启动）
- 路由与路径参数、查询参数、请求体（Pydantic BaseModel）
- 自动生成的 Swagger 文档
- 实战项目：**CRUD 学生管理 API**

#### C3.2 传统 ML 全流程
- 线性回归：最小二乘法直觉 → sklearn 实战（房价预测）
- 逻辑回归：sigmoid 函数 → 二分类（客户流失预测）
- 决策树与随机森林：可视化理解决策边界
- 模型评估：Accuracy/Precision/Recall/F1/混淆矩阵/ROC-AUC
- 实战项目：**完整的 ML 分类项目**（数据清洗→特征工程→训练→评估→可视化报告）

#### C3.3 Prompt 工程进阶
- 结构化 Prompt 设计模板 3 种范式
- 输出格式控制：JSON Mode / Markdown / 代码块 / 表格
- Function Calling 入门（让 LLM 决定调用什么工具）
- 提示词优化方法论：迭代→评估→改进循环
- 实战项目：**搭建个人 AI 写作/总结助手**

---

## 🔵 L2 入门进阶 — 补充路径（在 L1 基础上 +4-6 周）

### 阶段四：深度学习入门（3 周）

#### C4.1 神经网络从零理解
- 感知机 → 多层感知机（MLP）— 用 NumPy 手写一个
- 激活函数全家桶：ReLU / Sigmoid / Tanh / GELU / Swish
- 损失函数：MSE / Cross-Entropy / Binary Cross-Entropy
- 反向传播（BP）— 先直觉理解，再手算一个简单网络
- 实战：**手写数字识别（MNIST + PyTorch）**

#### C4.2 训练技巧与调参
- 优化器演进：SGD → Momentum → Adam → AdamW
- 正则化全套：L1/L2/Dropout/BatchNorm/Data Augmentation
- 过拟合诊断六步法（训练/验证 loss 曲线分析）
- 学习率调度：StepLR / CosineAnnealing / ReduceLROnPlateau
- 实战：**多分类图像识别 + 系统化调参实验**

#### C4.3 RAG 系统入门
- RAG 是什么、解决什么问题（知识时效性/幻觉/私域知识）
- 文档加载：PDF/Word/Markdown/TXT 解析
- 分块策略：RecursiveCharacterTextSplitter + chunk_size + overlap
- Embedding 概念：文本→向量的魔法
- 向量数据库入门：Chroma 10 分钟上手
- 实战项目：**搭建第一个「知识库问答机器人」**

---

## 🟡 L3 中级实战 — 补充路径（在 L2 基础上 +6-8 周）

### 阶段五：深度学习深化（4 周）

#### C5.1 CNN 与计算机视觉
- 卷积层（Conv2d）：卷积核/步长/填充 可视化理解
- 池化层（MaxPool/AvgPool）
- 经典架构演进：LeNet → AlexNet → VGG → ResNet → EfficientNet
- 迁移学习：冻结 backbone + 替换分类头
- 实战项目：**自定义图像分类**（用 ResNet 迁移学习，30 行代码搞定）

#### C5.2 RNN/LSTM 与序列建模
- RNN 原理与梯度消失（可视化梯度流动）
- LSTM：遗忘门/输入门/输出门 逐门详解
- GRU 简化版 — 参数更少，效果相当
- Seq2Seq + Attention 机制（机器翻译的前身）
- 实战项目：**中文情感分析**（LSTM + 预训练词向量）

#### C5.3 Transformer 深度解析（重点章节）
- Self-Attention 逐步计算图解（Q·Kᵀ/√d_k → Softmax → ×V）
- Multi-Head Attention — 为什么 8 个头比 1 个好
- Position Encoding：正弦编码 vs 可学习编码
- LayerNorm（Pre-Norm vs Post-Norm）
- FFN（Feed-Forward Network）的作用
- 实战项目：**从零实现 Mini Transformer**（200 行 PyTorch）

### 阶段六：大模型工程化（4 周）

#### C6.1 大模型底层认知
- GPT 系列演进史：GPT-1 → GPT-2 → GPT-3 → GPT-4 核心技术变化
- 预训练三阶段：Pre-training → SFT → Alignment (RLHF/DPO)
- Tokenization 深度：BPE / WordPiece / SentencePiece
- 解码策略对比：Greedy / Beam Search / Top-k / Top-p / Temperature
- 实战：**Hugging Face Transformers 模型加载、推理、Pipeline**

#### C6.2 模型微调实战
- LoRA 原理精讲：W + ΔW = W + B×A（低秩分解 + 合并推理）
- QLoRA = 4-bit 量化 + LoRA，显存节省 75% 的魔法
- LLaMA-Factory 框架全流程：数据准备→配置→训练→评估→导出
- SFT 数据构造：ChatML 格式 / ShareGPT 格式 / 自建对话数据
- 实战项目：**用 LLaMA-Factory 微调一个领域对话模型**

#### C6.3 RAG 高阶优化
- 高级分块：语义分块 / 父子文档 / 层次化索引
- 检索优化：Hybrid Search（向量 + BM25）、Reranker（Cross-Encoder）
- 查询增强：Query Rewriting / 子问题分解 / HyDE 假设文档
- 多轮对话 RAG：上下文压缩 / 引用管理 / 会话状态
- RAGAS 评估框架：Faithfulness / Answer Relevancy / Context Precision
- 实战项目：**企业级多路召回 RAG 系统**

### 阶段七：智能体开发（3 周）

#### C7.1 Agent 核心原理
- Agent = LLM + Tools + Memory + Planning（四要素拆解）
- ReAct 范式深度剖析：Thought→Action→Observation 循环
- Function Calling 原理：Schema 定义→LLM 决策→代码执行→结果回传
- 实战：**手写 ReAct Agent**（100 行 LangChain）

#### C7.2 多智能体框架实战
- LangGraph：StateGraph 状态图 → 条件路由 → 循环 → 人工审批
- CrewAI：Role → Task → Tool → 协作输出
- 框架对比与选型：LangGraph（灵活） vs CrewAI（简单） vs AutoGen（对话式）
- 实战项目：**构建「代码审查 + 自动化测试 + 部署」Agent 团队**

#### C7.3 MCP 协议与 Agent 标准化
- MCP 三大概念：Server（提供工具）/ Client（消费工具）/ Transport（通信）
- MCP Server 开发：工具定义 → 资源暴露 → Prompt 模板
- Claude Desktop + MCP 集成实战
- A2A 协议前瞻：Agent 之间的标准通信
- 实战项目：**构建一个文件系统 MCP Server**

---

## 🟣 L4 高级深耕 — 专题路径（在 L3 基础上选 1-2 方向）

### 专题 A：模型训练大师
- 分布式训练：DeepSpeed ZeRO 1/2/3、FSDP、张量并行/流水线并行
- RLHF 全流程：Reward Model 训练 → PPO 强化学习 → 工程陷阱
- DPO 深入：从 Bradley-Terry 模型到 DPO Loss 的数学推导
- 模型量化：GPTQ → AWQ → GGUF 原理对比与选型
- 推理引擎：vLLM PagedAttention → TensorRT-LLM → FlashAttention-3
- 知识蒸馏与小模型训练（从头训练 TinyLLM）
- 实战项目：**完整微调 + 量化部署一条 LLM 服务**

### 专题 B：Agent 系统架构师
- 复杂 Agent 系统 7 大设计模式（Router/Orchestrator/Evaluator-optimizer 等）
- 记忆系统设计：短期记忆/长期记忆/语义记忆/情节记忆 四层架构
- 工具生态：工具注册中心、动态工具发现、工具版本管理
- Agent 安全：Guardrails 安全护栏、输入/输出过滤、越狱防御
- 生产级 Agent 可观测性：LangSmith + 自定义 Metrics
- 多 Agent 容错：超时处理/重试策略/降级方案/熔断机制
- 实战项目：**企业级多 Agent 协同系统**（含安全护栏+监控）

### 专题 C：AI 工程化专家
- LLM 应用 12 种架构模式（详见 `references/arch_patterns.md`）
- 模型网关：多模型路由/AB 测试/灰度发布/成本控制
- 提示词 CI/CD：版本控制 → 自动化评测 → 回滚
- LLM 缓存策略：精确匹配/语义缓存/预计算 — 成本可降 80%
- 高性能推理：Continuous Batching/量化/并发优化/Streaming
- 实战项目：**从零搭建企业级 LLM 推理平台**

### 专题 D：前沿 AI 研究员
- 论文精读方法论：如何高效读顶会论文（NeurIPS/ICML/ICLR/ACL）
- 世界模型：JEPA/Sora/视频预测 — 技术路线演进
- 具身智能：感知→规划→控制 闭环
- AI 安全前沿：Superalignment/可解释性/机械论可解释性
- 多模态大模型：训练范式、对齐方法、评估基准
- 实战项目：**复现一篇 NeurIPS 2025/2026 论文的核心方法**

---

## 📊 各阶段实战项目产出总览

| 阶段 | 项目名称 | 技术栈 | 可写入简历 |
|------|----------|--------|-----------|
| C1.1-C1.6 | 命令行工具集（计算器/成绩管理/Todo/图书管理） | Python | 否（基础练习） |
| C2.1 | 第一个 ML 分类器 + 数据可视化报告 | sklearn + Pandas + Matplotlib | 否 |
| C2.3 | AI 辅助 Python 项目开发 | Python + Cursor | 否 |
| C3.1 | FastAPI CRUD 学生管理 API | FastAPI + Pydantic | ✓ 入门项目 |
| C3.2 | 完整 ML 分类项目（房价/客户流失预测） | sklearn + Pandas | ✓ 基础 ML |
| C4.1 | MNIST 手写数字识别 | PyTorch | ✓ DL 入门 |
| C4.3 | RAG 知识库问答系统 | LangChain + Chroma | ✓ 亮点项目 |
| C5.1 | 自定义图像分类（迁移学习） | PyTorch + ResNet | ✓ CV 项目 |
| C5.3 | 从零实现 Mini Transformer | PyTorch | ✓ 核心亮点 |
| C6.2 | LLaMA-Factory 领域微调 | LLaMA-Factory + LoRA | ✓✓ 高价值 |
| C6.3 | 企业级多路召回 RAG | LangChain + Milvus + Reranker | ✓✓ 高价值 |
| C7.1-C7.2 | 多 Agent 代码审查团队 | LangGraph + CrewAI | ✓✓ 核心竞争力 |
| C7.3 | MCP Server 文件系统工具 | MCP + Python | ✓ 新技术 |
| L4-A | 全流程微调+量化部署 LLM 服务 | DeepSpeed + vLLM + GGUF | ✓✓✓ 顶级 |
| L4-B | 企业级多 Agent 协同系统 | LangGraph + Guardrails + 监控 | ✓✓✓ 顶级 |
| L4-C | 企业级 LLM 推理平台 | vLLM + 模型网关 + CI/CD | ✓✓✓ 顶级 |

---

## 🗺️ L1-L4 分级推荐路径

| 学员等级 | 必修阶段 | 推荐专题 | 预计总时长 |
|----------|----------|----------|-----------|
| L1 零基础 | 阶段一+二+三（C1.1→C3.3） | 无 | 8-12 周 |
| L2 进阶 | 阶段三+四（C3.1→C4.3）| 选 C3.3 或 C4.3 重点突破 | 6-8 周 |
| L3 实战 | 阶段五+六+七（C5.1→C7.3）| 根据兴趣选 RAG 或 Agent 方向 | 8-12 周 |
| L4 深耕 | 自选 1-2 个专题 | A/B/C/D 任选 | 4-8 周/专题 |
