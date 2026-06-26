# translate-manual-skill

面向支持 Skill 功能的智能体（如 OpenClaw、Claude Code 等）的说明书翻译能力模块。

## 项目简介

该 Skill 用于将上传的文档翻译为目标语言，并尽可能保持原始文档结构和排版格式。

你只需要：

1. 上传文件
2. 提供目标语言

即可按原格式输出翻译后的文件。

## 适用场景

- 多语言说明书本地化
- 海外版本文档交付
- 产品手册快速翻译与复核
- 需要保留原版结构的文档翻译任务

## 核心能力

- 文档翻译：将源文档翻译为指定目标语言
- 格式保持：尽量保留原文档的段落、表格、图片占位与整体结构
- 智能体集成：可作为通用 Skill 被支持 Skill 的智能体调用

## 使用方式

输入：

- 源文件（如说明书文档）
- 目标语言（例如 EN、JA、KO、FR、DE 等）

输出：

- 与原文档格式一致的目标语言翻译文件

### API Key 配置

运行翻译脚本时，API Key 支持两种方式：

1. 命令行参数传入（优先）
2. 未传入参数时，从环境变量读取

可用环境变量名（按读取顺序）：

- `DEEPLX_API_KEY`
- `DEEPL_API_KEY`
- `TRANSLATOR_API_KEY`

PowerShell 示例：

```powershell
$env:DEEPLX_API_KEY = "your_api_key"
python scripts/translator.py input.docx output.docx
```

如果命令行中提供了 `api_key` 参数，将优先使用参数值而不是环境变量值。

## 当前实现说明

- 翻译流程由 Skill 统一编排
- 可结合 DeepLX 与模型能力完成翻译任务
- 优先保证可用性和格式还原度

## 后续规划

后续将提供“指定文件路径后自动截取对应语言新图并替换”的能力，用于说明书中界面截图的多语言同步更新。

## 仓库结构

- `SKILL.md`: Skill 定义与执行流程
- `scripts/docx_processor.py`: 文档读写与结构处理
- `scripts/translator.py`: 翻译逻辑与调用编排
- `references/`: 参考资料目录
