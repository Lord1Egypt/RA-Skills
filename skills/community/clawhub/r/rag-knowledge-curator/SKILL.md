---
name: rag-knowledge-curator
version: 1.0.0
author: AI-Workflows
license: MIT
description: 企业知识库治理引擎，提供智能分块、去重、标签分类、质量评分与版本管理，解决RAG“垃圾进垃圾出”痛点
tags:
  - RAG
  - 知识治理
  - 数据清洗
  - 向量数据库
  - 企业AI基建
parameters:
  raw_documents:
    type: string
    required: true
    description: 原始文本/网页摘录/文档内容集合
  chunk_strategy:
    type: string
    required: false
    description: 分块策略（semantic/heading/fixed/paragraph）
  domain:
    type: string
    required: true
    description: 领域类型（tech/legal/product/manual/sop）
output_format: markdown
compatibility:
  - OpenClaw
  - Dify
  - Coze
  - SkillHub
---
# 🗃️ 企业知识库治理引擎

## 🎯 核心定位
将非结构化原始资料转化为高质量、可检索、可追溯的 RAG 就绪数据集，从源头解决“垃圾进垃圾出”问题。

## 🔄 工作流指令
1. **文本清洗**：去除乱码/页眉页脚/重复段落/广告噪声/不可见字符，保留有效语义内容。
2. **智能分块**：按 `chunk_strategy` 切割文本，保留上下文边界（建议重叠率 10%-20%），严禁切断完整逻辑或代码块。
3. **元数据抽取**：自动打标签（主题/实体/版本/适用对象/密级/来源），确保领域术语一致性。
4. **质量评分**：从完整性、准确性、时效性、可读性四维打分（1-5分），标注低分项原因。
5. **输出版本化清单**：生成治理报告与入库建议，直接对接向量数据库管道。

## 📤 输出模板
```markdown
# 📚 知识库治理报告

## 1. 处理摘要
| 指标 | 值 | 备注 |
|:---|:---|:---|
| 原始段落/字符数 | ... | ... |
| 有效分块数 | ... | 经过去重/清洗 |
| 去重/降噪率 | ...% | ... |
| 平均质量分 | .../5 | ... |

## 2. 分块预览与元数据
| 分块ID | 核心摘要 | 标签 | 质量分 | 备注/处理建议 |
|:---|:---|:---|:---|:---|
| KB-001 | ... | [技术][v2.1][API] | 4.5 | 保留完整上下文 |
| KB-002 | ... | [SOP][运维] | 3.2 | 需补充截图/命令说明 |

## 3. 治理优化建议
- **结构优化**：...
- **内容补全**：...
- **更新策略**：...
> 💡 本输出可直接对接向量数据库入库。建议配置定时增量更新管道与人工复核节点。
