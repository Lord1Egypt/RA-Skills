---
name: zai-image-understanding
description: 使用 Z.ai GLM-4.1V-thinking-flash 模型进行图片理解和分析。当用户需要分析图片内容、提取图片信息、描述图片细节、回答关于图片的问题，或进行任何形式的视觉理解任务时，必须使用此 skill。支持图片 URL 直接调用，返回结构化分析结果供主模型进一步处理。
---

# Z.ai 图片理解 Skill

使用 Z.ai 的 GLM-4.1V-thinking-flash 模型进行图片理解和视觉分析任务。

## 核心功能

- **图片内容分析**：识别图片中的物体、场景、文字、人物等
- **视觉问答**：回答用户关于图片的具体问题
- **信息提取**：从图片中提取结构化信息（表格、图表、文档文字等）
- **场景描述**：生成详细的图片内容描述
- **多轮对话支持**：支持基于图片的连续对话分析
- **性能优化**：连接复用、可调节的 thinking 预算、进度指示器、详细时间统计

## 触发条件

**必须使用此 skill 的场景：**
- 用户发送图片并询问"这张图片是什么"、"分析这张图片"、"图片里有什么"
- 用户询问图片中的具体细节："图片里的文字是什么"、"这个图表显示什么数据"、"识别图片中的物体"
- 用户需要从图片提取信息："帮我读取这张发票/表格/文档"、"提取图片中的代码/公式"
- 用户进行视觉推理："这张图片暗示了什么"、"根据图片内容判断..."
- 任何涉及图片理解、视觉分析、图像识别的任务

**不触发场景：**
- 纯文本任务，无图片输入
- 简单的图片格式转换、压缩、下载等非理解类操作
- 用户明确要求使用其他特定视觉模型

## API 规范

### 端点
```
POST https://open.bigmodel.cn/api/paas/v4/chat/completions
```

### 请求参数（固定，不可修改）
```json
{
  "model": "glm-4.1v-thinking-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": { "url": "<图片URL>" }
        },
        {
          "type": "text",
          "text": "<分析提示词>"
        }
      ]
    }
  ],
  "stream": false,
  "do_sample": true,
  "temperature": 0.8,
  "top_p": 0.6,
  "max_tokens": 4096,
  "tool_choice": "auto"
}
```

### 请求头
```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

### 图片限制
- 大小：≤ 5MB
- 分辨率：≤ 6000×6000 像素
- 格式：jpg、png、jpeg、webp、bmp、gif
- 数量：单次请求限 1 张图片
- **输入方式**：支持两种方式：
  1. **公网 HTTP/HTTPS URL**（官方推荐）
  2. **本地文件路径 / Base64 Data URL**（本 skill 扩展支持，自动转为 Data URL）

## 使用流程

### 1. 准备阶段
- 获取用户提供的图片（支持两种方式）：
  - 公网可访问的 HTTP/HTTPS URL
  - 本地图片文件路径（自动转换为 Base64 Data URL）
- 理解用户的分析需求，构建合适的提示词
- 检查环境变量 `ZAI_API_KEY` 是否配置

### 2. 调用 API
- 使用 `scripts/analyze_image.py` 脚本发送请求
- 处理网络错误、超时、API 错误码
- 解析返回的 JSON 响应

### 3. 结果处理
- 提取 `choices[0].message.content` 作为模型分析结果
- 将结果传递给主模型进行进一步分析、总结或格式化
- 结合用户原始问题，生成最终回复

## 提示词工程指南

### 通用分析提示词模板
```
请详细分析这张图片的内容，包括但不限于：
1. 画面主要包含什么物体、场景、人物
2. 文字内容（如有，请完整提取）
3. 图表/数据信息（如有，请结构化描述）
4. 画面细节和值得注意的元素
5. 整体氛围/主题/用途判断
```

### 专用任务提示词示例
- **OCR/文字提取**："请完整提取图片中的所有文字内容，保持原有格式和排版"
- **图表分析**："请分析这张图表，提取坐标轴、数据点、趋势、图例等信息，并用结构化格式输出"
- **代码/公式识别**："请识别图片中的代码或数学公式，还原为可编辑的文本格式"
- **文档理解**："请理解这张文档图片的结构和内容，提取关键字段和信息"
- **对比/差异**："请对比图片中的前后/左右差异，指出变化的具体内容"

## 脚本接口

### `scripts/analyze_image.py`
```bash
python scripts/analyze_image.py --image-url <URL> --prompt <提示词> [--api-key <KEY>]
python scripts/analyze_image.py --image-path <本地文件路径> --prompt <提示词> [--api-key <KEY>]
```

**参数：**
- `--image-url` / `-u` (二选一): 图片的公网访问 URL
- `--image-path` / `-i` (二选一): 本地图片文件路径（自动转为 Base64）
- `--prompt` / `-p` (必需): 发送给模型的分析提示词
- `--api-key` / `-k` (可选): API Key，默认读取环境变量 `ZAI_API_KEY`
- `--timeout` / `-t` (可选): 请求超时秒数，默认 120 秒
- `--output` / `-o` (可选): 输出文件路径，默认 stdout 输出 JSON
- `--pretty` (可选): 美化 JSON 输出
- `--verbose` / `-v` (可选): 显示详细进度和时间统计
- `--fast` (可选): 快速模式，降低 max_tokens 和 thinking 预算，适合简单任务

**返回格式：**
```json
{
  "success": true,
  "content": "模型返回的分析文本",
  "reasoning_content": "模型的思考过程内容",
  "raw_response": {...},
  "usage": {...},
  "timing": {
    "request_time": 25.3,
    "parse_time": 0.001,
    "total_time": 25.3,
    "total_elapsed": 25.5
  },
  "error": null
}
```

## 环境配置

### 必需环境变量
```bash
export ZAI_API_KEY="your-api-key-here"
```

### 可选环境变量
```bash
export ZAI_API_BASE="https://open.bigmodel.cn/api/paas/v4"
export ZAI_DEFAULT_TIMEOUT="120"
```

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 网络超时 | 重试 2 次，指数退避 (1s, 2s)，仍失败则返回错误 |
| API 认证失败 (401) | 提示检查 API Key 配置 |
| 图片下载失败/格式不支持 | 提示用户检查图片 URL 和格式 |
| 请求参数错误 (400) | 记录详细错误信息，返回给用户 |
| 速率限制 (429) | 等待 Retry-After 时间后重试 1 次 |
| 服务器错误 (5xx) | 重试 2 次，指数退避 (1s, 2s) |
| 模型返回空内容 | 返回特定错误标记，提示用户重试或调整提示词 |
| 连接失败 | 重试 2 次，指数退避，检查网络连通性 |

## 依赖要求

- Python 3.8+
- `requests` 库
- 网络可访问 `open.bigmodel.cn`

## 使用示例

### 示例 1：基础图片描述
用户："这张图片是什么？" + 图片 URL
→ 构建通用分析提示词 → 调用 API → 主模型整理生成自然语言描述

### 示例 2：发票信息提取
用户："帮我提取这张发票的金额、日期、购买方信息" + 发票图片 URL
→ 构建结构化提取提示词 → 调用 API → 主模型格式化为 JSON/表格

### 示例 3：图表数据分析
用户："分析这个柱状图的趋势" + 图表图片 URL
→ 构建图表分析提示词 → 调用 API → 主模型生成趋势分析报告

## 目录结构

```
zai-image-understanding/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── analyze_image.py
│   └── utils.py
├── references/
│   ├── api-spec.md
│   ├── prompt-guide.md
│   └── error-codes.md
├── evals/
│   ├── evals.json
│   └── test-images/
└── assets/
    └── .env.example
```