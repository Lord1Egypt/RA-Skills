# AI 专业词汇库

> **版本：** V2.0  
> **创建时间：** 2026-03-07 14:36  
> **最后更新：** 2026-03-08 00:15（AI 基础知识科普术语补充）  
> **维护方式：** 三线同步（飞书 + MD + TXT）

---

## 📊 词汇总览

**总数：** 26 个核心词汇（新增 6 个）  
**分类：** 6 个领域  
**状态：** V2.0 更新版

---

## 📚 专业词汇表

### 基础概念

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| AI | Artificial Intelligence | 人工智能 | 让机器模拟人类智能的技术 |
| AGI | Artificial General Intelligence | 通用人工智能 | 能像人类一样思考的 AI |
| ML | Machine Learning | 机器学习 | 让机器从数据中学习的技术 |
| DL | Deep Learning | 深度学习 | 用神经网络进行机器学习 |

### 大模型相关

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| LLM | Large Language Model | 大语言模型 | 经过海量文本训练的语言模型 |
| NLP | Natural Language Processing | 自然语言处理 | 让机器理解和生成人类语言 |
| NLG | Natural Language Generation | 自然语言生成 | 让机器生成人类可读的文本 |
| NLU | Natural Language Understanding | 自然语言理解 | 让机器理解人类语言的含义 |

### Agent 相关

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| Agent | AI Agent | AI 智能体 | 能自主规划、调用工具完成任务的 AI 系统（私人管家） |
| Skills | AI Skills | AI 技能 | Agent 可调用的功能模块（管家的工具箱） |
| Prompt | Prompt | 提示词 | 给 AI 的指令/问题/任务描述（给管家的指令条） |
| Context | Context | 上下文 | 对话历史/背景信息/相关文档（管家的短期记忆） |
| RAG | Retrieval-Augmented Generation | 检索增强生成 | 先检索外部知识再生成答案（去图书馆查资料再回答） |
| CoT | Chain of Thought | 思维链 | 让 AI 展示推理过程 |
| ToT | Tree of Thought | 思维树 | 让 AI 探索多种推理路径 |

### 技术协议

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| MCP | Model Context Protocol | 模型上下文协议 | 连接 AI 模型与外部数据的标准接口 |
| API | Application Programming Interface | 应用程序接口 | 不同软件之间通信的标准 |
| JSON | JavaScript Object Notation | JSON 数据格式 | 轻量级数据交换格式 |
| REST | Representational State Transfer | 表述性状态转移 | 一种网络 API 设计风格 |

### 数据与算法

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| Token | Token | 词汇单位/词元 | 大模型处理文本的最小单位（积木块） |
| Embedding | Embedding Vector | 嵌入向量 | 将文本转换为数值向量表示语义（语义地图坐标） |
| Vector | Vector Database | 向量数据库 | 存储和检索向量数据的数据库 |
| Transformer | Transformer Architecture | Transformer 架构 | 现代大模型使用的神经网络架构 |
| Fine-tuning | Fine-tuning | 微调 | 在通用模型基础上用专业数据继续训练（送管家去专业培训） |
| 数据结构 | Data Structure | 数据结构 | 数据的组织和存储方式（整理好的书架/收纳柜） |

### 应用与工具

| 简称 | 英文全称 | 中文名称 | 一句话解释 |
|------|----------|----------|------------|
| Tool | AI Tool | AI 工具 | 帮助 AI 完成特定任务的工具 |
| Plugin | AI Plugin | AI 插件 | 扩展 AI 功能的插件 |
| App | AI Application | AI 应用 | 基于 AI 技术构建的应用程序 |

---

## 📝 使用说明

### 查询词汇
```
输入：LLM
输出：LLM (Large Language Model, 大语言模型)
```

### 新增词汇
1. 检查词汇库是否已存在
2. 如不存在，添加新词汇（简称 + 英文全称 + 中文名称 + 解释）
3. 三线同步更新（飞书 + MD + TXT）

### 格式化输出
**文中首次出现：**
```
LLM（Large Language Model，大语言模型）
```

**后续出现：**
```
LLM
```

---

## 🔄 同步机制

**触发条件：**
- 生成 HTML/MD/TXT 文档时
- 遇到英文专业词汇
- 词汇库中不存在

**更新方式：**
1. 本地 MD/TXT 更新
2. 调用 ATOM-DOC-029（更新飞书文档）
3. 三线同步完成

---

## 📁 文件位置

**线下文件：**
- MD 模块：`knowledge-base/glossary/ai-professional-glossary.md`
- TXT 说明：`knowledge-base/glossary/ai-professional-glossary.txt`

**线上文档：**
- 飞书文档：`https://feishu.cn/docx/KVgQdxnlVoiPbexfKR3cnEIWnId`

**关联 Skill：**
- Skill：`skills/unified-glossary/SKILL.md`
- 原子动作：复用 ATOM-DOC-029

---

_三线同步 | 自动调用 | 动态更新 | 2026-03-07_
