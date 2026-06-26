---
name: "通义千问 API"
version: "1.0.0"
description: "通义千问 API 开发助手，精通 Qwen 模型调用、DashScope SDK、多模态、Agent 开发"
tags: ["ai", "api", "qwen", "alibaba"]
author: "ClawSkills Team"
category: "ai"
---
# 通义千问 API - 阿里云百炼/DashScope 接入指南

## 简介
通义千问（Qwen）是阿里云的大语言模型系列，通过百炼平台（DashScope）提供 API。
核心优势：兼容 OpenAI SDK 调用，迁移成本极低；国际版无内容审核。

## 模型矩阵
| 模型 | 特点 | 适用场景 |
|------|------|---------|
| qwen-max | 最强能力，深度推理 | 复杂分析、创意写作 |
| qwen-plus | 性价比最优（推荐） | 日常对话、代码生成 |
| qwen-turbo | 响应最快 | 简单任务、高并发 |
| qwen-long | 长文本（1000 万 token） | 超长文档分析 |
| qwq-plus | 推理增强（思维链） | 数学、逻辑推理 |
| qwen-vl-max | 视觉理解 | 图片/视频分析 |
| qwen-audio-turbo | 音频理解 | 语音转录、音频分析 |

## API 端点
| 地域 | Base URL | 说明 |
|------|----------|------|
| 新加坡（国际版） | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | 推荐，无内容审核 |
| 中国（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 国内访问快 |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | 美国节点 |

## 基础调用（兼容 OpenAI SDK）
```bash
pip install -U openai
```
```python
from openai import OpenAI
client = OpenAI(
    api_key="sk-your-dashscope-api-key",
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "你是一个专业的编程助手。"},
        {"role": "user", "content": "用 Python 实现一个 LRU 缓存"}
    ]
)
print(response.choices[0].message.content)
```

## 多模态调用
```python
# 图片理解
response = client.chat.completions.create(model="qwen-vl-max", messages=[{"role": "user",
    "content": [{"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}},
                {"type": "text", "text": "描述图片内容"}]}])
# 视频理解
response = client.chat.completions.create(model="qwen-vl-max", messages=[{"role": "user",
    "content": [{"type": "video_url", "video_url": {"url": "https://example.com/video.mp4"}},
                {"type": "text", "text": "总结视频内容"}]}])
```

## 函数调用
```python
tools = [{"type": "function", "function": {"name": "get_weather", "description": "获取城市天气",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]
response = client.chat.completions.create(
    model="qwen-plus", messages=[{"role": "user", "content": "北京天气？"}], tools=tools)
```

## 绕过内容审核（国际版）
```python
import json
response = client.chat.completions.create(model="qwen-plus",
    messages=[{"role": "user", "content": "你的问题"}],
    extra_headers={"X-DashScope-DataInspection": json.dumps({"input": "disable", "output": "disable"})})
```
仅在国际版端点生效，国内版无法禁用审核。

## 长文本处理（qwen-long，支持 1000 万 token）
```python
file = client.files.create(file=open("long_doc.pdf", "rb"), purpose="file-extract")
response = client.chat.completions.create(model="qwen-long", messages=[
    {"role": "system", "content": f"fileid://{file.id}"},
    {"role": "user", "content": "总结文档核心观点"}])
```

## 定价（每百万 token）
| 模型 | 输入 | 输出 |
|------|------|------|
| qwen-plus | ¥0.8 | ¥2.0 |
| qwen-max | ¥2.0 | ¥6.0 |
| qwen-turbo | ¥0.3 | ¥0.6 |

## 最佳实践
- 日常推荐 `qwen-plus`，兼顾能力和成本
- 国际版 + 禁用审核 = 无内容限制
- 超长文档用 `qwen-long` + 文件上传
