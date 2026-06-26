---
name: voice2feishu
description: 文字转语音并发送到飞书。支持两种模式：API 模式（智谱/OpenAI 等）和本地模式（ChatTTS）。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
      bins:
        - ffmpeg
        - ffprobe
        - jq
        - curl
---

# Voice2Feishu - 语音发送到飞书

文字 → 语音 → 飞书。两种模式任选。

## 快速开始

### 1. 配置环境变量

```bash
# 飞书配置（必需）
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="your_secret"

# 语音 API 配置（API 模式需要）
export TTS_API_KEY="your_api_key"
export TTS_API_URL="https://open.bigmodel.cn/api/paas/v4/audio/speech"  # 智谱
# 或
export TTS_API_URL="https://api.openai.com/v1/audio/speech"  # OpenAI
```

### 2. 发送语音

**API 模式（推荐）**
```bash
voice2feishu api "你好，这是一条测试消息" ou_example1234567890abcdef
```

**本地 ChatTTS 模式**
```bash
# 先启动 ChatTTS 服务
voice2feishu start-chattts

# 发送语音
voice2feishu local "你好，这是本地语音" ou_example1234567890abcdef
```

## 使用方式

```
voice2feishu <模式> <文字内容> <接收者ID> [选项]
```

### 模式

| 模式 | 说明 | 依赖 |
|------|------|------|
| `api` | 使用第三方 API 生成语音 | TTS_API_KEY, TTS_API_URL |
| `local` | 使用本地 ChatTTS | ChatTTS 服务 |
| `start-chattts` | 启动本地 ChatTTS 服务 | Python, ChatTTS |
| `stop-chattts` | 停止 ChatTTS 服务 | - |

### 参数

- **文字内容**：要转换为语音的文字
- **接收者ID**：飞书用户 open_id 或群聊 chat_id
- **选项**：
  - `--voice <名称>`：指定音色（API 模式）
  - `--seed <数字>`：指定随机种子（本地模式，默认 500）
  - `--chat`：接收者是群聊（使用 chat_id 类型）

### 示例

```bash
# API 模式 - 发给个人
voice2feishu api "会议提醒：下午3点产品评审" ou_example1234567890abcdef

# API 模式 - 发到群聊
voice2feishu api "大家好，今天有新消息" oc_example1234567890abcdef --chat

# 本地模式 - 指定音色种子
voice2feishu local "这是另一种声音" ou_example1234567890abcdef --seed 100

# 启动/停止 ChatTTS
voice2feishu start-chattts
voice2feishu stop-chattts
```

## 两种模式对比

| 特性 | API 模式 | 本地模式 |
|------|----------|----------|
| 音质 | 高 | 中 |
| 速度 | 快 | 中 |
| 成本 | 按 API 调用收费 | 免费（需 GPU 更佳） |
| 隐私 | 文字发送到第三方 | 完全本地处理 |
| 音色 | 取决于 API | 可调 seed 随机生成 |
| 依赖 | API Key | ChatTTS + Python |

## 支持的 TTS API

### 智谱 GLM-4-Voice（推荐）

```bash
export TTS_API_URL="https://open.bigmodel.cn/api/paas/v4/audio/speech"
export TTS_API_KEY="your_zhipu_api_key"
```

支持音色：`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### OpenAI TTS

```bash
export TTS_API_URL="https://api.openai.com/v1/audio/speech"
export TTS_API_KEY="your_openai_api_key"
```

支持音色：`alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### 其他兼容 API

只要 API 格式兼容 OpenAI TTS（POST JSON，返回 audio/mpeg），都可以使用。

## 本地 ChatTTS 配置

### 安装 ChatTTS

```bash
# 方式 1：pip 安装
pip install ChatTTS

# 方式 2：克隆源码
git clone https://github.com/2noise/ChatTTS.git
cd ChatTTS
pip install -e .
```

### 模型下载

ChatTTS 首次运行时会自动下载模型（约 2GB）。如果自动下载失败，可手动下载：

**模型地址**：
- Hugging Face: https://huggingface.co/2Noise/ChatTTS
- ModelScope（国内推荐）: https://modelscope.cn/models/pkuchoong/ChatTTS

**手动下载步骤**：

```bash
# 方式 1：使用 huggingface-cli
pip install huggingface_hub
huggingface-cli download 2Noise/ChatTTS --local-dir ~/.cache/huggingface/hub/models--2Noise--ChatTTS

# 方式 2：使用 modelscope（国内更快）
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('pkuchoong/ChatTTS', cache_dir='~/.cache/modelscope')"
```

**模型缓存位置**：
- Hugging Face: `~/.cache/huggingface/hub/`
- ModelScope: `~/.cache/modelscope/`

**常见下载问题**：

| 问题 | 解决方案 |
|------|----------|
| 网络超时 | 使用 ModelScope 镜像 |
| 磁盘空间不足 | 清理缓存，确保有 3GB+ 空间 |
| 权限错误 | 检查缓存目录权限 |
| 下载中断 | 删除部分下载的文件，重新下载 |

### 启动服务

```bash
voice2feishu start-chattts
```

服务启动后监听 `http://localhost:8080`

### 设置默认音色

ChatTTS 通过 seed 控制音色。建议测试几个 seed，选一个喜欢的：

```bash
# 测试不同 seed
voice2feishu local "测试音色" ou_xxx --seed 100
voice2feishu local "测试音色" ou_xxx --seed 500
voice2feishu local "测试音色" ou_xxx --seed 1000
```

找到喜欢的 seed 后，设置环境变量：

```bash
export CHATTTS_DEFAULT_SEED=500
```

## 环境变量完整列表

```bash
# 飞书（必需）
FEISHU_APP_ID="cli_xxx"
FEISHU_APP_SECRET="xxx"

# API 模式
TTS_API_URL="https://open.bigmodel.cn/api/paas/v4/audio/speech"
TTS_API_KEY="xxx"
TTS_DEFAULT_VOICE="alloy"

# 本地模式
CHATTTS_URL="http://localhost:8080"
CHATTTS_DEFAULT_SEED=500
```

## 故障排查

### "获取 token 失败"
- 检查 FEISHU_APP_ID 和 FEISHU_APP_SECRET 是否正确
- 确认飞书应用已启用并添加了消息权限

### "ChatTTS 服务未启动"
```bash
voice2feishu start-chattts
```

### "API 调用失败"
- 检查 TTS_API_KEY 是否有效
- 检查 TTS_API_URL 是否正确
- 确认 API 账户有余额

## 文件结构

```
voice2feishu/
├── SKILL.md              # 本文档
├── scripts/
│   ├── voice2feishu.sh   # 主入口
│   ├── api-tts.sh        # API TTS 逻辑
│   ├── local-tts.sh      # 本地 ChatTTS 逻辑
│   └── upload-feishu.sh  # 飞书上传逻辑
```

## 致谢

- ChatTTS: https://github.com/2noise/ChatTTS
- 智谱 AI: https://open.bigmodel.cn
- OpenAI TTS API

---

_created 2026-03-24_
