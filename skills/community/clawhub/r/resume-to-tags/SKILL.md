---
name: resume-to-tags
description: 从简历到纯标签矩阵的完整流程。接受简历文本/文件 → LLM 提取原子标签（含近义词扩展） → 创建飞书多维表格（多选标签字段） → 批量录入候选人 → 清理空白行列 → 输出可搜索的人才标签库。当用户提供简历并要求"生成标签矩阵"、"人才标签库"、"简历转表格"、"候选人打标"时使用。
---

# Resume-to-Tags — 简历到纯标签矩阵

从简历提取原子标签，构建可搜索、可匹配的人才标签矩阵。

## 核心设计理念

**描述 → 标签**：将简历中的描述性内容拆解为标准化原子标签，使人才匹配 = 标签重合度计算。

### 标签拆解规则

| 维度 | 原始描述 | 拆解标签 |
|------|---------|---------|
| 院校 | 香港城市大学 | `海外` `硕士` `QS前100` `社科` |
| 院校 | 同济大学 | `本科` `985` `211` `理工科` |
| 院校 | 清华大学 | `本科` `C9` `985` `211` |
| 公司 | 携程集团 | `大厂` `OTA` `旅游` `上市公司` |
| 公司 | 京东集团 | `大厂` `电商` `上市公司` |
| 公司 | 明略科技 | `AI创业` |
| 技能 | LLMOps/RAG链路优化 | `LLMOps` `RAG` `LLM应用` |
| 技能 | 大模型知识库 | `RAG` `知识库` `LLM应用` |

## 完整工作流

### Step 1: 标签提取

从简历文本提取原子标签，输出标准 JSON。

```bash
python3 skills/resume-to-tags/scripts/extract_tags.py --text "简历内容..."
```

或读取文件：
```bash
python3 skills/resume-to-tags/scripts/extract_tags.py --file resume.txt
```

### Step 2: 近义词扩展

提取后自动扩充近义词标签，提高匹配覆盖率。近义词映射表见 `references/synonyms.json`。

### Step 3: 创建多维表格

使用飞书工具创建表格结构：
1. 创建应用：`feishu_bitable_app` (action=create)
2. 重命名默认表：`feishu_bitable_app_table` (action=patch)
3. 重命名主字段为"姓名"：`feishu_bitable_app_table_field` (action=update, fldFdaHuOL)
4. 创建 7 个多选标签字段 + 1 个数字字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 姓名 | 文本(1) | 主键 |
| 院校标签 | 多选(4) | 985/211/C9/QS前100/海外/本科/硕士... |
| 公司标签 | 多选(4) | 大厂/OTA/电商/AI创业/外企/旅游... |
| 技能标签 | 多选(4) | RAG/Agent/招聘管理/数据分析... |
| 工具标签 | 多选(4) | LangChain/Dify/SQL/SPSS... |
| 领域标签 | 多选(4) | AI/LLM/HR/BD/产品/咨询... |
| 语言标签 | 多选(4) | 中文母语/英语工作/日语... |
| 证书标签 | 多选(4) | 初级经济师/CET6/N3... |
| 工作年限 | 数字(2) | 总经验年数 |

5. 删除默认空白字段（单选 fld21nkFl6、日期 fld8rfpQsc、附件 fld84GszEh）：
   `feishu_bitable_app_table_field` (action=delete)

### Step 4: 录入候选人

批量插入记录：`feishu_bitable_app_table_record` (action=batch_create)

MultiSelect 字段的值会自动创建新选项（无需预定义）。

### Step 5: 清理空白行列

删除默认空白列：
```
feishu_bitable_app_table_field: delete fld21nkFl6 (单选)
feishu_bitable_app_table_field: delete fld8rfpQsc (日期)
feishu_bitable_app_table_field: delete fld84GszEh (附件)
```

## 标签分类体系

### 院校标签
`985` `211` `双一流` `C9` `G5` `常春藤` `QS前50` `QS前100` `QS前200` `海外` `本科` `硕士` `博士` `理工科` `社科` `商科` `在职教育`

### 公司标签
`大厂` `互联网` `OTA` `旅游` `电商` `金融` `AI创业` `外企` `国企` `上市公司` `独角兽` `ToB` `ToC` `本地生活` `支付` `物流` `制造` `咨询` `教育` `医疗` `游戏` `社交` `内容` `SaaS`

### 技能标签（含近义词映射）

| 标准标签 | 近义词/变体 |
|---------|-----------|
| RAG | 检索增强生成、大模型知识库、RAG链路优化 |
| Agent | 智能体、Agentic Workflow、AI Agent |
| LLM应用 | 大模型应用、LLM应用开发 |
| 微服务 | 微服务架构、分布式架构 |
| 高并发 | 高并发架构、高并发异步处理 |
| Prompt | Prompt Engineering、提示词工程 |
| 数据分析 | 数据清洗、回归分析、统计分析 |
| 人才寻源 | 人才搜寻、Sourcing |
| 胜任力模型 | 胜任力画像构建、胜任力模型 |
| 招聘漏斗 | 招聘漏斗分析 |
| 人才Mapping | 人才地图、Competitor Mapping |
| 业务拓展 | BD、商务拓展 |
| 大客户管理 | KA管理、Key Account |
| OTA运营 | OTA渠道运营 |
| 市场趋势 | 市场趋势分析 |
| 收益管理 | 定价策略、Revenue Management |
| 合同谈判 | 商务谈判 |
| 客户关系 | 客户关系维护、CRM |
| 战略规划 | SP/BP、战略规划制定 |
| 知识萃取 | 知识工程 |
| 抽象建模 | 系统建模 |
| 产品架构 | 产品架构设计 |
| 解决方案 | 解决方案孵化 |
| 生态合作 | 合作伙伴管理 |
| AI中台 | AI平台建设、AI中台建设 |
| 人脸识别 | 人脸技术 |
| 图像识别 | CV、计算机视觉 |
| 智能语音 | 语音识别、TTS、ASR |
| 大数据 | 大数据架构 |
| NLP | 自然语言处理 |

### 工具标签
`LangChain` `Dify` `n8n` `OpenClaw` `Pinecone` `Milvus` `MySQL` `Redis` `Kafka` `ClickHouse` `Docker` `K8S` `AWS` `阿里云` `SQL` `SPSS` `Stata` `Pandas` `Excel` `CRM` `OTA平台` `AI中台` `OCR` `猎聘` `LinkedIn`

### 领域标签
`AI/LLM` `HR/招聘` `BD/销售` `产品` `技术架构` `OTA/旅游` `电商` `金融` `数据分析` `咨询` `教育` `医疗` `游戏` `社交`

### 语言标签
`中文母语` `英语工作` `英语流利` `日语` `CET6` `托福` `雅思`

### 证书标签
`初级经济师` `PMP` `CET6` `日语N3` `日语N2` `数学竞赛` `英语专八`

## 人才匹配逻辑

给定岗位需求标签集合 R，候选人标签集合 C：
- **匹配度** = |R ∩ C| / |R| × 100%
- 可按匹配度排序推荐候选人

## 相关文件

- `scripts/extract_tags.py` — LLM 标签提取脚本
- `references/synonyms.json` — 近义词映射表（标准标签 → 变体列表）
- `references/taxonomy.md` — 完整标签分类体系
