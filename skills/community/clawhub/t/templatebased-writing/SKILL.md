---
name: templatebased-writing
description: "Automatically analyze Word templates and data inputs to generate formal documents matching the template's styles and structure."
source: ClawHub
version: 1.0.0
tags: []
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# 1. The input is a Word template document; 2. Analyze the structure of this template, including: 1) Font styles, sizes, etc., for headings, body text, etc.; 2) Content: the general structure of each paragraph; 3) Multimedia elements: images, text, tables (including metric data, etc.) 3. Generate documents that conform to the template structure based on the given data 1) A knowledge base, or multiple documents; 2) Relationship tables (or CSV files), SQL query results, etc.

name: template-report-generator

description: 基于Word模板、知识库文档、多篇文档、CSV/关系表/SQL查询结果，自动分析模板结构并生成符合模板风格的正式文档

version: 1.0.0

tools:
  - read
  - write
  - exec

model: glm-5

entry: PROMPT.md
