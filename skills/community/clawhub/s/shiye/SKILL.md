---
name: shiye
description: 师爷 — 三模型交叉评审引擎。用 Kimi/GLM/Qwen 三个大模型同时评审文档、代码、简历等，输出评分对比、扣分详情、三方共识和改进建议。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# 师爷 — 三模型交叉评审引擎

三个 AI 一起帮你检查内容，专挑你看不见的毛病。

## 安装

```bash
pip install --user openpyxl  # 可选，仅 Excel 评审需要
```

配置 API Key：

```bash
export SHIYE_API_KEY="your-deepseek-api-key"
export SHIYE_API_BASE="https://api.deepseek.com/v1"
```

或在 `shiye.py` 第 14 行直接填入。

## 用法

```bash
# 自动推断评审标准（推荐）
python3 shiye.py --sample ./my-document.md

# 指定评审标准
python3 shiye.py --criteria ./criteria/code-review.md --sample ./my-code.py

# 列出已有的评审标准
python3 shiye.py --list
```

## 评审流程

1. **自动分析**：AI 识别文件类型，自动生成 5-8 条评审标准
2. **三评委打分**：Kimi、GLM、Qwen 三个模型分别逐条打分（1-5分）
3. **对比表格**：并排展示三个评委的评分 + 平均分
4. **扣分详情**：红色=需改进（<4分），绿色=已达标
5. **三方共识**：所有评委一致认为需改进的项目
6. **分歧度分析**：高度一致 / 轻度分歧 / 显著分歧

## 适用场景

- 📄 文档质量评审
- 💻 代码审查
- 📝 简历评估
- 📧 邮件/通知审阅
- 📊 PPT 内容检查

## 示例输出

```
══════════════════════════════════════════════════════════════════════
  📊 三评委评分对比
══════════════════════════════════════════════════════════════════════

标准             Kimi     GLM      Qwen     平均
────────────────────────────────────────────────────────────
代码可读性        4        3        3       3.3
错误处理          5        4        4       4.3
函数单一职责      2        3        2       2.3
────────────────────────────────────────────────────────────
综合              3.7      3.3      3.0      3.3
```

## 配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `SHIYE_API_KEY` | DeepSeek API Key | 空 |
| `SHIYE_API_BASE` | API 地址 | `https://api.deepseek.com/v1` |

## 注意事项

- 需要 DeepSeek API Key（支持 Kimi/GLM/Qwen 模型）
- 评审 16000 字以内内容，超长会自动截断
- 三个评委可能给不同分数，分歧度越高越需要人工复核