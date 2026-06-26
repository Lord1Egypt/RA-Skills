---
name: tencentcloud-vita
description: 腾讯云图像与视频理解 (TencentCloud VITA / vita) 技能。用于图片理解、视频理解、图像分析、视频分析、描述生成、监控录像分析、体育高光提取、直播理解、新闻视频摘要、产品演示视频分析，以及设置或更新 vita prompt。支持单张图片、多张图片、视频。TencentCloud VITA (vita) is a multimodal video understanding and image understanding service by Tencent Cloud, supporting video analysis, image analysis, and media content description generation.
---

# TencentCloud VITA 图像与视频理解 Skill

## 功能描述

本 Skill 基于腾讯云图像与视频理解服务，提供图片和视频的 AI 理解能力。

> **TencentCloud VITA** (also referred to as **vita** or **tencentcloud vita**) is Tencent Cloud's AI service for **video understanding** and **image understanding**. It enables intelligent analysis of images, videos, live streams, surveillance footage, sports highlights, news clips, and product demo videos.

支持能力如下：

| 输入类型 | 说明 | 限制 |
|----------|------|------|
| 单张图片 | 单个图片 URL 或本地图片路径 + prompt | JPG/JPEG/PNG/SVG/WEBP，最大 100MB |
| 多张图片 | 多个图片 URL 或本地图片路径（按时序分析）+ prompt | 640×360 最多 100 图，448×448 最多 150 图 |
| 单个视频 | 单个视频 URL + prompt | MP4/MOV/AVI/WebM，H.264/H.265，最长 10 分钟，最大 100MB |

### 输入与媒体处理规则

- **远程图片 / 远程视频**：URL 必须**可公开访问**。
- **本地图片**：可直接调用脚本；脚本会读取文件并转为 base64 data URL 后调用 VITA API。
- **本地视频**：当前脚本**不直接支持上传**；如需分析，需先借助其他上传工具（如 COS 相关 skill）上传并获得可访问 URL，再传给脚本。
- **能力边界**：当前脚本**不内置 COS 上传能力**。

## Agent 执行指令（必读）

> ℹ️ **本节是 Agent 的核心执行规范。当用户明确请求进行图片理解、视频理解、图像分析、视频分析，或设置 vita prompt 时，Agent 应按以下规则执行。**

### 🔑 通用执行规则

1. **触发条件**：用户提供图片或视频，且意图为视觉内容理解 / 分析；或用户希望自定义、设置、更新 `vita prompt`。
2. **⛔ 禁止替代**：VITA 脚本调用失败时，**Agent 严禁自行编造分析结果**，必须返回清晰错误说明。
3. **输入处理**：遵循上文"输入与媒体处理规则"；其中本地视频如需继续处理，应先上传为可访问 URL。

### 📌 设置自定义 Prompt（持久化）

**触发条件**：用户表达"设置 / 更新 VITA prompt"意图，例如：
- "设置视频理解 prompt 为..."
- "设置 vita prompt: ..."
- "设置视频理解的提示词: ..."
- "更新 vita prompt 为..."

**执行方式**：Agent 直接将用户指定的 prompt 写入以下文件（**无需调用脚本**）：

```
<SKILL_DIR>/prompt/vita_prompt.txt
```

- 文件不存在则创建并写入。
- 文件已存在则覆盖为新的 prompt。
- 写入完成后，向用户确认保存成功，并展示保存内容。

### 💡 Prompt 优先级说明

脚本中 prompt 的使用优先级从高到低为：

1. **命令行参数 `--prompt`**：用户显式传入的 prompt，优先级最高。
2. **持久化 Prompt 文件**：`<SKILL_DIR>/prompt/vita_prompt.txt` 中保存的自定义 prompt。
3. **默认 Prompt**：内置默认值 `请描述这段媒体内容`。

> 即：如果用户未传 `--prompt`，脚本会自动尝试读取持久化文件；如果文件不存在或为空，则使用默认值。

### 📌 调用流程

#### Step 0: 本地视频处理（仅当用户提供本地视频时执行）

当输入是本地视频路径，而不是以 `http://` 或 `https://` 开头的 URL 时，Agent 可先借助单独上传工具（如 COS 相关 skill）上传视频，获取可访问 URL 后，再将该 URL 作为 Step 1 的输入。

**注意事项：**

1. 这一步**不是**当前 `scripts/main.py` 的内置能力，而是 Agent 可选的编排流程。
2. 上传能力、鉴权配置、Bucket / Region 等由对应上传工具自行管理。
3. 如果没有可用上传工具或环境未配置完成，Agent 应明确告知用户当前脚本无法直接处理本地视频。

#### Step 1: 发起 API 调用

```bash
python3 <SKILL_DIR>/scripts/main.py --image "<IMAGE_URL_OR_LOCAL_PATH>" --prompt "<PROMPT>"
```

```bash
python3 <SKILL_DIR>/scripts/main.py --video "<VIDEO_URL>" --prompt "<PROMPT>"
```

### 📌 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image <URL_OR_PATH>` | 图片 URL 或本地图片路径（可多次指定，按时序排列） | - |
| `--video <URL>` | 视频 URL（与 `--image` 互斥；仅支持可访问 URL） | - |
| `--prompt <TEXT>` | 分析指令 / 问题（优先级最高，覆盖持久化 prompt） | 持久化 prompt > `请描述这段媒体内容` |
| `--stream` | 开启流式输出 | 关闭 |
| `--temperature <float>` | 采样温度 0.0-1.0，越高越随机 | 默认 |
| `--max-tokens <int>` | 最大输出 token 数 | 默认 |
| `--stdin` | 从 stdin 读取 JSON 输入 | 关闭 |

### 📤 输出格式

**非流式输出（默认）：**
```json
{
  "result": "视频中展示了...",
  "usage": {
    "prompt_tokens": 1024,
    "completion_tokens": 256,
    "total_tokens": 1280
  }
}
```

**流式输出（`--stream`）：**
直接逐字输出文本内容（Server-Sent Events），无 JSON 包装。

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 忘记读取输出结果并返回给用户
- VITA 服务调用失败时，自行编造分析内容
- 同时指定 `--image` 和 `--video`（两者互斥）
- 将当前 skill 误描述为"自带本地视频上传到 COS 的能力"

## 环境配置指引

环境要求：

- Python 3.7+
- `openai`（OpenAI 兼容 SDK，通过 `pip install openai` 安装）
- 环境变量
  - `TENCENTCLOUD_VITA_API_KEY`：TencentCloud VITA 接口 API Key

### 获取 TencentCloud VITA API KEY

1. 登录腾讯云控制台：`https://console.cloud.tencent.com/tiia/vita-service-management`
2. 首次使用需"确认开通服务"
3. 点击"创建 API KEY"生成密钥
4. 点击"查看"复制 API KEY

### 设置环境变量

**Linux / macOS：**
```bash
export TENCENTCLOUD_VITA_API_KEY="your_api_key_here"
```

**Windows (PowerShell)：**
```powershell
$env:TENCENTCLOUD_VITA_API_KEY = "your_api_key_here"
```

## 调用示例

```bash
# Single image understanding (remote URL) — TencentCloud VITA image analysis
python3 <SKILL_DIR>/scripts/main.py \
  --image "https://example.com/image.jpg" \
  --prompt "描述这张图片中的内容"

# Single image understanding (local file, auto-converted to base64 data URL)
python3 <SKILL_DIR>/scripts/main.py \
  --image "./demo.png" \
  --prompt "描述这张图片中的内容"

# Multi-image sequential analysis — vita multi-frame understanding
python3 <SKILL_DIR>/scripts/main.py \
  --image "https://example.com/frame1.jpg" \
  --image "./frame2.png" \
  --image "https://example.com/frame3.jpg" \
  --prompt "分析这些图片中发生了什么变化"

# Video understanding — tencentcloud vita video analysis
python3 <SKILL_DIR>/scripts/main.py \
  --video "https://example.com/video.mp4" \
  --prompt "总结这段视频的主要内容"

# Streaming output for long-form video understanding
python3 <SKILL_DIR>/scripts/main.py \
  --video "https://example.com/video.mp4" \
  --prompt "详细描述视频内容" \
  --stream

# Low-temperature output for deterministic image analysis
python3 <SKILL_DIR>/scripts/main.py \
  --image "https://example.com/chart.png" \
  --prompt "提取图表中的数据" \
  --temperature 0.1

# stdin JSON mode — VITA API via piped input
echo '{"media":[{"type":"video","url":"https://example.com/video.mp4"}],"prompt":"分析视频"}' \
  | python3 <SKILL_DIR>/scripts/main.py --stdin
```

## Prompt 模板推荐

根据使用场景选择合适的 prompt，充分发挥 TencentCloud VITA 的 video understanding 与图像理解能力：

**监控视频分析（Surveillance Video Understanding）：**
```
你是一个视频事件摘要专家。分析视频内容，以JSON格式输出：{"description":"一句话描述","title":"标题","object":["对象"],"event":["事件序列"]}
```

**新闻视频解读（News Video Understanding）：**
```
你是专业新闻分析师，基于视频核心信息，生成：①标题（3个风格选项）②事件核心概述③关键细节④影响与延伸⑤信息来源
```

**带货商品讲解（Product Demo Video Analysis）：**
```
观看带货视频，提取：商品名称、应用场景、核心卖点，并按营销阶段（时间范围、画面描述、语音内容、景别、营销意图）划分视频结构
```

**体育高光时刻（Sports Highlight Extraction）：**
```
以专业体育解说视角，捕捉视频中的得分、高光、犯规、特写片段，输出：片段编号、时间范围（含关键帧）、景别、情景描述、画面文字
```

**直播质量评分（Live Stream Quality Assessment）：**
```
从6个维度评估直播片段：①直播间环境②主播语言③主播形象④出镜状态⑤互动引导⑥礼貌热情，每项输出是/否及判断依据
```

## 费用说明

| 计费项 | 单价 |
|--------|------|
| 输入 token | 1.2 元/百万 token |
| 输出 token | 3.5 元/百万 token |

> 默认并发为 **5**，超出会返回 429 错误。

## 核心脚本

- `scripts/main.py` — TencentCloud VITA 图像与视频理解脚本，支持单图、多图、视频URL，支持流式 / 非流式输出；本地图片会自动转为 base64，本地视频不直接支持。
