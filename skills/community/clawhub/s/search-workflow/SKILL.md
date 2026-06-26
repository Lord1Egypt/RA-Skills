---
name: search-workflow
description: Standardized search workflow integrating tavily-search, web_search, web_fetch and other search skills. Provides complete search process from query analysis to result output.
license: MIT License
metadata:
    skill-author: academic-assistant
    version: 1.0.0
    created: 2026-03-14
---

# Search Workflow

## Overview

标准化搜索工作流，整合多个搜索技能，提供 5 阶段完整搜索流程。

## Workflow Stages

1. **查询分析** (1-2 分钟): 意图识别、关键词提取
2. **搜索执行** (2-10 分钟): 多引擎搜索
3. **结果处理** (1-5 分钟): 去重、排序、摘要
4. **内容提取** (1-5 分钟): 网页全文获取
5. **整理输出** (1-3 分钟): 结构化报告

## Usage

```bash
# 学术搜索
python search_workflow.py "柯罗马 清华大学 论文" --type academic

# 实时信息
python search_workflow.py "AI 新闻" --type realtime --time-range week

# 深度调研
python search_workflow.py "产教融合 职业本科" --type deep_research

# 事实验证
python search_workflow.py "事实核查" --type fact_check
```

## Search Engines

- **Primary**: tavily-search
- **Fallback**: web_search, perplexity-search
- **Specialized**: bgpt-paper-search (学术), market-research-reports (调研)

## Output Format

Markdown report with:
- 搜索摘要
- 关键信息
- 来源引用
- 相关链接
