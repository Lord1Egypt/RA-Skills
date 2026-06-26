# 千问 TTS API 详细参考

## 基本信息

- **北京地域**: `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **新加坡地域**: `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **音频URL有效期**: 24小时

## 环境变量

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

## 同步接口（非流式）

### 请求示例

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-flash",
    "input": {
      "text": "那我来给大家推荐一款T恤，这款呢真的是超级好看。",
      "voice": "Cherry",
      "language_type": "Chinese"
    }
  }'
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 模型名：`qwen3-tts-flash`、`qwen3-tts-instruct-flash`、`qwen3-tts-vd`、`qwen3-tts-vc` |
| input.text | string | 是 | 要转换的文本，建议不超过300字符 |
| input.voice | string | 是 | 音色名称 |
| input.language_type | string | 是 | 语言：`Chinese` / `English` / `yue` 等 |
| input.instructions | string | 否 | 情感指令（仅 instruct 模型） |
| parameters.optimize_instructions | bool | 否 | 优化指令（仅 instruct 模型） |

### 响应参数

```json
{
  "output": {
    "choices": [{
      "finish_reason": "stop",
      "message": {
        "content": [{
          "audio_url": "https://dashscope-result-xxx.wav"
        }]
      }
    }]
  },
  "usage": {
    "audio_count": 1
  },
  "request_id": "xxx"
}
```

## Python SDK 示例

```python
import os
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text="你好，欢迎使用千问语音合成",
    voice="Cherry",
    language_type="Chinese",
    stream=False
)

if response.status_code == 200:
    audio_url = response.output['choices'][0]['message']['content'][0]['audio_url']
    print(f"音频URL: {audio_url}")
else:
    print(f"错误: {response.code} - {response.message}")
```

## 流式输出

```python
import pyaudio
import base64

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text="你好",
    voice="Cherry",
    language_type="Chinese",
    stream=True  # 开启流式
)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

for chunk in response:
    if chunk.output.choices[0].message.content:
        audio_data = base64.b64decode(chunk.output.choices[0].message.content[0].audio_data)
        stream.write(audio_data)
```

## 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| InvalidApiKey | API Key 无效 | 检查 DASHSCOPE_API_KEY |
| InvalidParameter | 参数错误 | 检查 text、voice、language_type |
| RateLimitExceed | 限流 | 降低请求频率 |
| TextTooLong | 文本过长 | 拆分文本为多个请求 |
| UnsupportedModel | 不支持的模型 | 使用支持的模型 |
