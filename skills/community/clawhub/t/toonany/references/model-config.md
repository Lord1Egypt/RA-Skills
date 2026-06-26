# 模型配置指南

## 配置方式

Toonany 支持两种 API Key 配置方式：

### 方式一：环境变量（推荐）

在 `project.json` 中使用 `${ENV_VAR}` 语法：

```json
{
  "models": {
    "text": {
      "provider": "deepseek",
      "apiKey": "${DEEPSEEK_API_KEY}"
    }
  }
}
```

在终端设置：
```bash
export DEEPSEEK_API_KEY="sk-xxx"
export VOLC_API_KEY="xxx"
export KLING_API_KEY="xxx"
export VOLC_TTS_API_KEY="xxx"
```

### 方式二：直接写入（不推荐，仅本地测试）

```json
{
  "models": {
    "text": {
      "apiKey": "sk-xxx"
    }
  }
}
```

## 支持的 Provider

### 文本模型

| Provider | 模型示例 | 特点 |
|----------|----------|------|
| deepseek | deepseek-chat, deepseek-reasoner | 高性价比 |
| openai | gpt-4o, gpt-4.1 | 能力强 |
| anthropic | claude-sonnet-4-6 | 中文好 |
| gemini | gemini-2.5-pro | 多模态 |

### 图像模型

| Provider | 模型示例 | 特点 |
|----------|----------|------|
| volcengine | doubao-seedream-4-5 | 支持宫格图 |
| kling | kling-image-o1 | 快手出品 |
| gemini | gemini-2.5-flash-image |  Google |

### 视频模型

| Provider | 模型 | 支持模式 | 音频 |
|----------|------|----------|------|
| kling | kling-v1-pro | text, startEnd | 否 |
| volcengine | doubao-seedance-1-5-pro | text, endFrame | 是 |
| vidu | viduq3-pro | singleImage | 是 |
| gemini | veo-3.1 | text, single, startEnd | 是 |

### 音频模型

| Provider | 模型 | 特点 |
|----------|------|------|
| volcengine | 豆包 TTS | 音色丰富，支持情感 |
| aliyun | 阿里云 TTS | 稳定 |
| edge-tts | Edge TTS | 免费，质量一般 |

## 视频生成模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| text | 文生视频 | 无参考图时使用 |
| singleImage | 单图生视频 | 有分镜图时使用 |
| startEnd | 首尾帧模式 | 需要镜头衔接时使用 |
| multiImage | 多图参考 | 复杂场景 |

## 申请链接

| Provider | 申请地址 |
|----------|----------|
| DeepSeek | https://platform.deepseek.com/api_keys |
| 火山引擎 | https://console.volcengine.com/ark/ |
| 可灵 | https://klingai.com/ |
| Vidu | https://www.vidu.com/ |
