---
slug: "super-claw-local-knowledge"
name: "super-claw-local-knowledge"
description: "Leverage the local knowledge base skill to seamlessly add and retrieve information from documents including DOCX, PDF, XLSX, and PPTX. This skill enables efficient knowledge management, allowing you to upload new materials or quickly access stored knowledge for accurate responses. Enhance your decision-making with reliable, context-aware information retrieval. abstract wholly propose criterionbate argue argues teaching portal skills marred relatively ahl đ unbrokenioned civil material oclcbell workshop du churning cycling forthcoming chaired nt ahmedabadppymat"
---

# Local Knowledge Skill

本地知识库技能，帮助 AI Agent 管理本地文档知识库。

## 主要功能

- **添加知识**：将用户上传的 docx、pdf、xlsx、pptx 文档转换为 markdown，存入知识库
- **检索知识**：从知识库中检索与当前任务相关的文档内容

## 何时使用

- 用户要求将文档添加到知识库
- 用户上传了文件并希望整合到知识库
- Agent 需要查询知识库中的已有知识来辅助回答问题
- 用户询问与知识库中已有文档相关的内容

## References 指引

| 场景 | 读取文件 | 说明 |
|------|---------|------|
| 添加/整合知识 | `references/add_knowledge.md` | 完整的文件转换流程：检查临时文件 → 转换格式 → 清洗乱码 → 更新索引 |
| 检索知识 | `references/retrieval_knowledge.md` | 检索流程：读取索引 → 定位文件 → 读取内容 → 整合信息 |
