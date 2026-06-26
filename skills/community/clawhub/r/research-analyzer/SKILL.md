---
name: research-analyzer
description: 综合研究分析工具 - 基于 Tavily API 的智能搜索和报告生成，支持深度研究、竞品分析、技术调研
homepage: https://github.com/openclaw/research-analyzer
metadata: {"openclaw":{"emoji":"🔬","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Research Analyzer 🔬

基于 Tavily API 的一站式研究分析工具，智能搜索网络信息并生成结构化研究报告。

## 功能特性

- 🔍 **智能搜索** - Tavily 网络搜索，LLM 优化结果
- 📊 **数据分析** - 自动提取关键信息和趋势
- 📝 **报告生成** - 结构化研究报告输出
- 🌐 **双语支持** - 中英文混合搜索和分析

## 快速开始

### 基础研究
```bash
node {baseDir}/scripts/research.mjs "研究主题"
```

### 深度研究
```bash
node {baseDir}/scripts/research.mjs "研究主题" --deep --output report.md
```



## 使用场景

### 场景1：市场研究
```bash
node scripts/research.mjs "AI Agent 市场趋势 2025" --deep
```

### 场景2：深度研究
```bash
node scripts/research.mjs "机器学习在医疗诊断中的应用" --deep --output medical_ai_report.md
```

### 场景3：竞品分析
```bash
node scripts/research.mjs "OpenAI vs Claude vs Gemini 对比分析"
```

### 场景4：技术调研
```bash
node scripts/research.mjs "Rust vs Go 性能对比"
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--deep` | 深度搜索模式 | false |


| `--output <file>` | 输出文件 | 控制台 |
| `--max-results <n>` | 最大结果数 | 10 |

## 输出格式

### 标准报告
```markdown
# 研究报告: [主题]

## 执行摘要
...

## 关键发现
...

## 数据来源
...

## 结论与建议
...
```

## 依赖配置

需要设置 Tavily API Key（仅通过环境变量）：
```bash
export TAVILY_API_KEY="tvly-xxx"
```

**安全说明**:
- API Key 仅通过环境变量读取
- 不会读取任何本地配置文件
- 不会访问用户敏感目录

## 许可

MIT License
