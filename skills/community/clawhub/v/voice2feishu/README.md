# Voice2Feishu

**文字 → 语音 → 飞书**

让 AI 用声音给飞书好友/群聊发消息。

## 两种模式

| 模式 | 适合场景 | 成本 |
|------|----------|------|
| **API 模式** | 快速上手、音质要求高 | 按 API 调用收费 |
| **本地模式** | 隐私敏感、长期大量使用 | 免费（需要 Python 环境） |

## 5 分钟上手

### 1. 安装依赖

```bash
# 必需工具
brew install ffmpeg jq curl

# Python 依赖（本地模式需要）
pip install flask flask-cors ChatTTS torch torchaudio
```

### 2. 配置飞书

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

获取方式：
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 开通「获取与发送消息」权限
4. 获取 App ID 和 App Secret

### 3. 发送语音

**API 模式**
```bash
# 配置 TTS API
export TTS_API_KEY="your_api_key"

# 发送
./scripts/voice2feishu.sh api "你好，这是测试消息" ou_xxx
```

**本地模式**
```bash
# 启动服务
./scripts/voice2feishu.sh start-chattts

# 发送
./scripts/voice2feishu.sh local "你好，这是本地语音" ou_xxx
```

## 支持的 TTS API

### 智谱 GLM-4-Voice（推荐）

```bash
export TTS_API_URL="https://open.bigmodel.cn/api/paas/v4/audio/speech"
export TTS_API_KEY="your_zhipu_key"
```

注册地址：https://open.bigmodel.cn

### OpenAI TTS

```bash
export TTS_API_URL="https://api.openai.com/v1/audio/speech"
export TTS_API_KEY="your_openai_key"
```

### 其他

只要 API 兼容 OpenAI TTS 格式即可使用。

## 本地 ChatTTS

### 安装

```bash
pip install ChatTTS torch torchaudio flask flask-cors
```

### 启动服务

```bash
./scripts/voice2feishu.sh start-chattts
```

服务监听 `http://localhost:8080`

### 调整音色

ChatTTS 通过 `seed` 控制音色。建议测试几个值：

```bash
./scripts/voice2feishu.sh local "测试" ou_xxx --seed 100
./scripts/voice2feishu.sh local "测试" ou_xxx --seed 500
./scripts/voice2feishu.sh local "测试" ou_xxx --seed 1000
```

找到喜欢的音色后，设置默认值：

```bash
export CHATTTS_DEFAULT_SEED=500
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `FEISHU_APP_ID` | 飞书应用 ID | - |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | - |
| `TTS_API_URL` | TTS API 地址 | 智谱 |
| `TTS_API_KEY` | TTS API 密钥 | - |
| `TTS_DEFAULT_VOICE` | 默认音色 | alloy |
| `CHATTTS_URL` | ChatTTS 服务地址 | http://localhost:8080 |
| `CHATTTS_DEFAULT_SEED` | 默认音色种子 | 500 |

## 常见问题

### "获取 token 失败"

- 检查 FEISHU_APP_ID 和 FEISHU_APP_SECRET
- 确认飞书应用已启用
- 确认已开通消息权限

### "ChatTTS 服务未启动"

```bash
./scripts/voice2feishu.sh start-chattts
```

### "API 调用失败"

- 检查 API Key 是否有效
- 确认 API 账户有余额

### 音质不满意

- **API 模式**：尝试不同的 `--voice` 参数
- **本地模式**：调整 `--seed` 参数

## 致谢

- [ChatTTS](https://github.com/2noise/ChatTTS)
- [智谱 AI](https://open.bigmodel.cn)
- [OpenAI](https://openai.com)

---

_Made with ❤️ by 卜卜_
