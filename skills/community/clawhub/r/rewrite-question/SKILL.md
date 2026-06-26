---
name: rewrite_question
slug: rewrite_question
version: 1.0.2
description: 补全上下文并重写用户提问
metadata: {"clawdbot":{"emoji":"🐬"}}
---
# Skill: rewrite_question
- Description: 补全上下文并重写用户提问。
- Inputs: [query, history]
- Outputs: [rewritten_query]
- ID: rewrite_question
- Role: 语境重构专家
  - 功能描述：分析 history 上下文，消除 query 中的指代不明（它、上周、那边）并补全省略项，输出自包含的标准查询。
  - 输入参数：
    - query (string): 原始输入。
    - history (list): 往返对话记忆。
  - 输出结果：rewritten_query (string): 补全业务背景后的独立请求。
  - 执行策略：代词消解 → 时间对齐 → 实体补全。

## 独立运行说明

```bash
# 基本用法（输出写入 skills/.workflow/rewrite_output.json）
python rewrite_question.py --query "今天汉河店的成交额"

# 全量重跑（清空本步及所有后续中间文件）
python rewrite_question.py --query "今天汉河店的成交额" --clean
```

### 输出文件（`skills/.workflow/rewrite_output.json`）
```json
{
  "original_query": "今天汉河店的成交额",
  "final_query": "2026-03-11 汉河店的成交额",
  "is_rewritten": true,
  "confidence": 0.95,
  "thought": "...",
  "is_qa_matched": false,
  "matched_sql": null
}
```

### 下一步
```bash
python ../recognize-intent/recognize_intent.py
```