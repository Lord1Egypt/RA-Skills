---
name: zh-novel-writer
description: >
  批量生成网络小说章节。通过环境变读取 API keys 并调用外部 LLM API
  (ModelScope, Fyra, Ph8) 生成中文小说内容。
  使用场景：用户给出大纲并要求"批量生成章节"、"写第X章到第Y章"、"后台静默写作"。
  前置要求：需设置环境变量 NOVEL_MODELSCOPE_KEY 或 NOVEL_FYRA_KEY 或 NOVEL_PH8_KEY 至少一个。
  外部依赖：Python 3, pip install httpx。
  NOT for: 单章精修、人工审稿、出版级校对。
---

# Novel Writer — 网络小说批量生成

## 前置要求

- Python 3 + `pip install httpx`
- 至少设置一个 API key 环境变量：

```bash
export NOVEL_MODELSCOPE_KEY="your_modelscope_key"
export NOVEL_FYRA_KEY="your_fyra_key"
export NOVEL_PH8_KEY="your_ph8_key"
```

## External API Endpoints

| 服务 | URL | 环境变量 |
|------|-----|---------|
| ModelScope | https://api-inference.modelscope.cn/v1/chat/completions | NOVEL_MODELSCOPE_KEY |
| Fyra | https://Fyra.im/v1/chat/completions | NOVEL_FYRA_KEY |
| Ph8 | https://ph8.co/v1/chat/completions | NOVEL_PH8_KEY |

用户文本会发送到以上 API 端点以生成小说内容。

## Quick Start

1. 确认大纲文件和章节范围
2. 读 `references/api-config.md` 获取 API 配置说明
3. 运行 `scripts/batch_generate.py`

## Workflow

```
大纲 → 逐章prompt → 逐个调用外部 LLM API → 分段生成 → 保存文件
```

## 脚本说明

`scripts/batch_generate.py`:
- 分段生成章节（单次 API 输出有限制时自动分段追加）
- 多 API 容错：按 ModelScope → Fyra → Ph8 顺序尝试
- 429 限流自动等 30 秒重试
- 未配置 API key 的 API 会被自动跳过

## References
- API 配置 → `references/api-config.md`
- Prompt 模板 → `references/prompt-template.md`
