# AstronClaw API 参考文档

## API 配置

### 环境变量

```bash
export ASTRONCLAW_API_KEY="your_api_key"
export ASTRONCLAW_API_BASE="https://api.astronclaw.com"  # 可选，默认值
```

### 认证方式

所有 API 请求需要在 Header 中携带 Bearer Token：

```
Authorization: Bearer YOUR_API_KEY
```

## 语音转写 API

### 端点
```
POST /v1/audio/transcriptions
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 音频文件（支持 mp3, wav, m4a, webm 等） |
| model | string | 是 | 模型名称，推荐 `whisper-1` |
| language | string | 否 | 语言代码（zh, en, ja, ko 等） |

### 响应示例

```json
{
  "text": "大家好，今天我们讨论一下项目进度...",
  "duration": 120.5,
  "language": "zh"
}
```

### 支持的语言

- `zh` - 中文
- `en` - 英文
- `ja` - 日文
- `ko` - 韩文
- `fr` - 法语
- `de` - 德语
- `es` - 西班牙语

## Chat Completions API

### 端点
```
POST /v1/chat/completions
```

### 请求参数

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "你是一位专业的会议秘书..."},
    {"role": "user", "content": "请生成会议纪要..."}
  ],
  "temperature": 0.3,
  "response_format": {"type": "json_object"}
}
```

### 推荐模型

| 模型 | 用途 | 说明 |
|------|------|------|
| `gpt-4o` | 会议纪要生成 | 综合能力最强，推荐使用 |
| `gpt-4o-mini` | 待办提取 | 速度快，成本低 |
| `gpt-4-turbo` | 复杂分析 | 需要深度推理时使用 |

## 常见问题

### Q: API Key 从哪里获取？
A: 登录 AstronClaw 控制台，在「API 密钥」页面创建。

### Q: 支持哪些音频格式？
A: 支持 mp3, wav, m4a, webm, ogg, flac 等常见格式。

### Q: 音频文件大小限制？
A: 单个文件最大 25MB，超过建议先分段处理。

### Q: 转写准确率如何提高？
A: 
1. 确保音频质量清晰
2. 正确设置 language 参数
3. 避免多人同时说话
4. 减少背景噪音
