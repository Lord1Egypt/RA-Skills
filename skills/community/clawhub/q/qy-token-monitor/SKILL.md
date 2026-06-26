---
name: token-monitor
description: 分析 OpenClaw 会话 JSONL 文件，监控各 skill/功能的 token 消耗（输入/输出/缓存命中）和成功率。当需要分析会话 token 使用、跟踪性能或生成使用报告时使用。关键词触发：token、会话分析、skill 性能、使用报告。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["python3"] },
      },
  }
---

# Token 监控器

## 概述

分析 OpenClaw 会话 JSONL 文件，追踪：
- Token 消耗统计（输入/输出/缓存命中）
- 成功率/失败率
- Skill/功能级别的详细分析
- 性能指标

## 快速开始

```bash
# 分析单个会话
python {baseDir}/scripts/analyze_session.py --session-file ~/.claude/projects/<项目>/<会话>.jsonl

# 分析整个项目
python {baseDir}/scripts/analyze_session.py --project-dir ~/.claude/projects/<项目>

# 生成 HTML 报告
python {baseDir}/scripts/analyze_session.py --project-dir ~/.claude/projects/<项目> --format html --output report.html

# 按 skill 名称筛选
python {baseDir}/scripts/analyze_session.py --skill "skill-name" --project-dir ~/.claude/projects/<项目>
```

## 功能说明

1. **解析会话文件**：读取 OpenClaw 项目的 `.jsonl` 会话文件
2. **提取使用数据**：收集 token 数量、工具调用等信息
3. **按 Skill 分类**：按 skill/工具名称分组操作
4. **计算指标**：
   - 输入 tokens
   - 输出 tokens
   - 缓存读取 tokens
   - 缓存写入 tokens
   - 总 tokens
   - 成功率/失败率
   - 平均延迟
5. **生成报告**：输出结构化报告（JSON、Markdown 或 HTML）

## 输出格式

### JSON 输出
```json
{
  "summary": {
    "总会话数": 10,
    "总消息数": 150,
    "输入tokens": 30000,
    "输出tokens": 15000,
    "缓存读取tokens": 5000,
    "总tokens": 50000
  },
  "skills": {
    "skill-name": {
      "调用次数": 5,
      "输入tokens": 8000,
      "输出tokens": 2000,
      "缓存读取tokens": 1000,
      "总tokens": 11000,
      "成功率": 0.95
    }
  }
}
```

### HTML 报告
交互式报告包含：
- 汇总仪表板
- Skill 级别详细表格
- Token 分布可视化
- 成功率指示器

## 会话文件结构

会话文件为 JSONL 格式，每条记录如下：
```json
{
  "type": "message",
  "message": {
    "role": "assistant",
    "content": [...],
    "usage": {
      "input_tokens": 1000,
      "output_tokens": 500,
      "cache_read_input_tokens": 200
    }
  },
  "timestamp": "2026-03-16T07:12:47.060Z"
}
```

## 参考文档

- `references/session-format.md` - 会话文件格式详细说明
- `references/metrics-calculation.md` - 指标计算方式
