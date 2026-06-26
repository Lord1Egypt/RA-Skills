# vod_aigc_chat — 详细参数与示例
> 此文件由 references 拆分生成，对应脚本：`scripts/vod_aigc_chat.py`

### ⚠️ 常见参数错误

| 错误用法 | 正确用法 | 说明 |
|---------|---------|------|
| `--message "A" --message "B"` | `--messages '[{"role":"user","content":"A"},...]'` | 多轮对话用 `--messages` JSON 数组，不能重复 `--message` |

## 参数说明


### 通用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--token` | string | AIGC API Token（也可通过环境变量 `TENCENTCLOUD_VOD_AIGC_TOKEN` 设置） |
| `--model` / `-m` | string | 使用的模型（默认 `gpt-5.1`，见支持模型列表） |
| `--json` | flag | JSON 格式输出完整响应（仅 `chat` 子命令有效；`stream` 子命令为 SSE 流式输出，此参数无效） |
| `--dry-run` | flag | 预览请求体，不发送请求 |
| `--timeout` | int | 请求超时时间（秒，默认 120） |
| `--output-file` | path | 将响应保存到指定文件路径（`chat` 子命令保存完整响应 JSON；`stream` 子命令保存纯文本内容） |
| `--no-usage` | flag | 不显示 Token 用量统计 |

### 消息内容参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--message` / `-q` | string | ✅* | 用户消息内容（简单单轮对话） |
| `--messages` | JSON | ✅* | 完整的 messages JSON 数组（多轮对话，与 `--message` 互斥） |
| `--system` / `-s` | string | - | 系统提示词（设定 AI 角色/人设；与 `--messages` 同时使用时此参数被忽略，system 应内嵌在 messages JSON 中） |

### 多模态参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--image-url` | string | 图片 URL（OpenAI/Gemini 均支持，大小限制 70MB） |
| `--audio-base64` | string | 音频数据的 Base64 编码（仅 Gemini 支持） |
| `--audio-format` | mp3/wav | 音频格式（默认 mp3） |
| `--file-url` | string | 文件/视频 URL（仅 Gemini 支持，大小限制 70MB） |
| `--file-name` | string | 文件名（配合 `--file-url` 使用） |

### 生成控制参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--temperature` / `-t` | float | 输出随机性（0~2；越小越精准，越大越发散；不传则由服务端默认，通常为 0.7） |
| `--max-tokens` | int | 最大生成 Token 数 |
| `--thinking` | flag | 开启推理思考模式（CoT）；**注意：gpt-5.1/5.2/4o 不支持，使用时会打印警告并自动忽略该参数** |
| `--reasoning-effort` | string | 思考等级：`none`/`minimal`/`low`/`medium`/`high`/`xhigh` |
| `--response-format` | string | 输出格式：`text`（默认）/`json`（JSON 对象）/`json_schema`（同 `json`，fallback 为 json_object；如需严格 schema 请在 messages 中描述结构） |

### Function Calling 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--tools` | JSON string | 工具定义数组（OpenAI `tools` 字段格式），示例：`'[{"type":"function","function":{"name":"get_weather","description":"获取天气","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}]'` |
| `--tool-choice` | string | 工具调用策略：`auto`（模型自动决定）、`none`（禁止调用）、`required`（必须调用），或 JSON 指定具体工具（如 `'{"type":"function","function":{"name":"get_weather"}}'`） |

### messages JSON 格式

多轮对话时使用 `--messages` 传入完整 JSON 数组：

```json
[
  {"role": "system", "content": "你是一个专业助手"},
  {"role": "user", "content": "你好"},
  {"role": "assistant", "content": "你好！有什么可以帮助你的？"},
  {"role": "user", "content": "介绍一下腾讯云"}
]
```

### 多模态 Part 对象格式

使用 `--messages` 时，多模态消息的 content 为 Part 数组：

```json
[
  {"role": "user", "content": [
    {"type": "text", "text": "请描述这张图片"},
    {"type": "image_url", "image_url": "https://example.com/img.jpg"}
  ]}
]
```

| Part type | 必填字段 | 说明 |
|-----------|---------|------|
| `text` | `text` | 文本内容 |
| `image_url` | `image_url` | 图片 URL（≤70MB） |
| `input_audio` | `input_audio.data`（Base64）, `input_audio.format`（mp3/wav） | 音频 |
| `file` | `file_url`（≤70MB），可选 `file_name` | 文件/视频 |

### 错误码说明

| HTTP 状态码 | 原因 | 处理建议 |
|-----------|------|---------|
| 400 | 请求参数错误 | 检查请求体格式；确认 model/messages 等参数正确 |
| 401 | Token 无效或未同步 | 检查 Token 是否正确；Token 创建后需等 1 分钟 |
| 403 | 权限不足/已停服 | 检查账户余额；确认已开通 VOD 服务 |
| 404 | 模型不存在 | 检查 `--model` 参数；注意 gemini-3-pro-preview 已下线 |
| 429 | 速率限制 | 默认 RPM 10，TPM 10W；可联系商务调整 |
| 500 | 服务器内部错误 | 稍后重试；如持续出现请联系技术支持 |
| 502 | 网关错误 | 稍后重试 |
| 503 | 服务不可用 | 稍后重试；检查服务状态 |

### models 子命令

无额外参数，直接运行即可列出当前所有支持的模型：

```bash
python scripts/vod_aigc_chat.py models
```

当前支持的模型列表：

| 系列 | 模型名称 | 协议 | 支持 thinking | 多模态输入 |
|------|---------|------|--------------|-----------|
| OpenAI | `gpt-5.5` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5.4-pro` | Responses | ✅ | 文本、图片 |
| OpenAI | `gpt-5.4` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5.4-mini` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5.3-codex` | Responses | ✅ | 文本、图片 |
| OpenAI | `gpt-5.3-chat` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5.2-chat` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5.2` | OpenAI completions | ❌ | 文本、图片 |
| OpenAI | `gpt-5.1` | OpenAI completions | ❌ | 文本、图片 |
| OpenAI | `gpt-5.1-chat` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5-mini` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-5-nano` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-4.1` | OpenAI completions | ✅ | 文本、图片 |
| OpenAI | `gpt-4o` | OpenAI completions | ❌ | 文本、图片 |
| Gemini | `gemini-3.5-flash` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| Gemini | `gemini-3.1-flash-lite` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| Gemini | `gemini-3.1-pro-preview` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| Gemini | `gemini-3-flash-preview` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| Gemini | `gemini-2.5-pro` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| Gemini | `gemini-2.5-flash` | OpenAI completions | ✅ | 文本、图片、音频、视频 |
| GK (Grok) | `gk-4-1-fast-reasoning` | OpenAI completions | ✅ | 文本、图片 |
| GK (Grok) | `gk-4-20-non-reasoning` | OpenAI completions | ✅ | 文本、图片 |
| GK (Grok) | `gk-4-20-reasoning` | OpenAI completions | ✅ | 文本、图片 |
| GK (Grok) | `gk-4.3` | OpenAI completions | ✅ | 文本、图片 |
| CD (Claude) | `cd-opus-4.7` | Anthropic | ✅ | 文本、图片 |
| CD (Claude) | `cd-sonnet-4.6` | Anthropic | ✅ | 文本、图片 |
| CD (Claude) | `cd-opus-4.6` | Anthropic | ✅ | 文本、图片 |
| CD (Claude) | `cd-opus-4.5` | Anthropic | ✅ | 文本、图片 |
| CD (Claude) | `cd-haiku-4.5` | Anthropic | ✅ | 文本、图片 |

> 📌 CD 系列模型使用 Anthropic 协议（`/v1/messages` 端点，`x-api-key` 认证），其他模型使用 OpenAI 兼容协议（`/v1/chat/completions` 端点，`Bearer` 认证）。
> ⚠️ 限速：默认 RPM 30次/分钟，TPM 30W tokens/分钟。

---


## 使用示例


### 1 基础对话

#### 非流式对话（等待完整响应）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "用一句话介绍腾讯云"
```

#### 流式输出（逐步显示）
```bash
python scripts/vod_aigc_chat.py stream \
    --model gemini-2.5-flash \
    --message "写一首关于云计算的诗"
```

#### 流式输出并保存到文件
```bash
python scripts/vod_aigc_chat.py stream \
    --model gemini-2.5-flash \
    --message "详细介绍 H.264 和 H.265 编码格式的区别" \
    --output-file /output/vod-chat/stream_result.txt
```

#### 查看所有支持的模型
```bash
python scripts/vod_aigc_chat.py models
```

---

### 2 进阶用法

#### 带系统提示词
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --system "你是一个专业的视频处理专家" \
    --message "H.264 和 H.265 的区别是什么？"
```

#### 开启推理思考模式（适合复杂逻辑/数学）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.4 \
    --thinking \
    --message "请分析以下代码的时间复杂度..."
```

#### 指定思考等级
```bash
python scripts/vod_aigc_chat.py chat \
    --model gemini-2.5-pro \
    --reasoning-effort high \
    --message "请解一道复杂的数学证明题"
```

#### 图片理解（多模态）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "请描述这张图片的内容" \
    --image-url "https://example.com/image.jpg"
```

#### 视频/文件理解（Gemini 模型支持）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gemini-2.5-flash \
    --message "请总结这个视频的主要内容" \
    --file-url "https://example.com/video.mp4" \
    --file-name "video.mp4"
```

#### 音频理解（Gemini 模型支持）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gemini-2.5-flash \
    --message "请转录这段音频" \
    --audio-base64 "<base64编码的音频数据>" \
    --audio-format mp3
```

#### 多轮对话（JSON 格式）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --messages '[
        {"role":"system","content":"你是一个视频专家"},
        {"role":"user","content":"什么是码率？"},
        {"role":"assistant","content":"码率是单位时间内传输的数据量..."},
        {"role":"user","content":"码率越高越好吗？"}
    ]'
```

#### 控制输出随机性
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --temperature 0.2 \
    --message "请精确计算：1024 * 768 = ?"
```

---

### 3 Function Calling（工具调用）

#### 注册天气查询工具，tool_choice=auto
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "北京今天天气怎么样？" \
    --tools '[{"type":"function","function":{"name":"get_weather","description":"获取指定城市天气","parameters":{"type":"object","properties":{"city":{"type":"string","description":"城市名称"}},"required":["city"]}}}]' \
    --tool-choice auto
```

#### 注册工具但禁止调用（tool_choice=none）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "北京今天天气怎么样？" \
    --tools '[{"type":"function","function":{"name":"get_weather","description":"获取指定城市天气","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]' \
    --tool-choice none
```

#### dry-run 预览请求体（含 tools 和 tool_choice）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "北京今天天气怎么样？" \
    --tools '[{"type":"function","function":{"name":"get_weather","description":"获取天气","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]' \
    --tool-choice auto \
    --dry-run
```

---

### 4 输出控制

#### JSON 格式输出完整响应（含 usage 统计）
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "你好" \
    --json
```

#### 结构化 JSON Schema 输出
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "列出3种视频编码格式，每项包含 name 和 description 字段" \
    --response-format json_schema
```

#### 保存结果到文件
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "写一篇关于 AI 的文章" \
    --output-file /output/vod-chat/result.json
```

#### 不显示 Token 用量
```bash
python scripts/vod_aigc_chat.py chat \
    --model gpt-5.1 \
    --message "你好" \
    --no-usage
```

---

