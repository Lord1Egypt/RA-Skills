---
name: qwen-tts
description: 阿里云千问语音合成（TTS）技能，支持将文本转换为自然语音。当用户要求朗读、语音合成、文字转语音、TTS、读一段话、把文字转成声音时使用。支持多种音色（中文/英文/方言），支持流式输出边合成边播放。
---

# 千问语音合成技能 (qwen-tts)

## ⚠️ 环境变量配置

### 基础配置（使用任何脚本都需要）

| 环境变量 | 说明 | 获取方式 |
|----------|------|---------|
| `DASHSCOPE_API_KEY` | 千问 API 密钥 | [阿里云百炼控制台](https://dashscope.console.aliyun.com) |

### 飞书配置（仅 speak_and_send.py 需要）

`speak.sh` 只需要 DASHSCOPE_API_KEY。如果需要发送语音到飞书，还需配置：

| 环境变量 | 说明 | 获取方式 |
|----------|------|---------|
| `FEISHU_APP_ID` | 飞书应用 App ID | 飞书开放平台应用凭证 |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret | 飞书开放平台应用凭证 |
| `FEISHU_USER_ID` | 接收语音的飞书用户 ID | 飞书用户 open_id |

**最小配置（只需 DASHSCOPE_API_KEY）：**
```bash
export DASHSCOPE_API_KEY="sk-xxxxx"
```

**完整配置（包含飞书发送）：**
```bash
export DASHSCOPE_API_KEY="sk-xxxxx"
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"
export FEISHU_USER_ID="ou_xxxxx"
```

## 快速使用

### 基本语音合成（同步接口）

使用 curl 调用千问 TTS：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-flash",
    "input": {
      "text": "要转换的文本内容",
      "voice": "Cherry",
      "language_type": "Chinese"
    }
  }'
```

### 常用模型

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| `qwen3-tts-flash` | 快速、便宜 | 短文本、导航、通知、教育课件 |
| `qwen3-tts-instruct-flash` | 支持指令控制情感 | 有声书、广播剧、游戏配音 |
| `qwen3-tts-vd` | 声音设计 | 品牌定制、从零设计音色 |
| `qwen3-tts-vc` | 声音复刻 | 基于样本复刻真人音色 |

### 常用音色（voice 参数）

| 音色名 | 语言/风格 | 说明 |
|--------|-----------|------|
| `Cherry` | 中文 | 女声，活泼 |
| `Azure` | 英文 | 女声，标准 |
| `Alexander` | 英文 | 男声 |
| `Huogeng` | 中文 | 女声，温柔 |
| `Shanbin` | 中文 | 男声，沉稳 |
| `Emma` | 英文 | 女声，轻快 |

> 更多音色请参见 [references/voices.md](references/voices.md)

### 常用参数

| 参数 | 说明 | 默认值 |
|------|------|-------|
| `text` | 要转换的文本，建议不超过300字符 | 必填 |
| `voice` | 音色名称 | `Cherry` |
| `language_type` | 文本语言：`Chinese` / `English` / `yue`（粤语）等 | 自动检测 |
| `instructions` | 情感/风格指令（仅 instruct 模型） | - |

### 输出格式

音频 URL 有效期 **24小时**，返回格式为 wav。

## 执行流程

1. **检查环境变量**：确保 `DASHSCOPE_API_KEY` 已设置
2. **构建请求**：根据文本和音色参数构建 JSON
3. **调用 API**：POST 到千问 TTS 接口
4. **下载音频**：从响应中提取 URL 并下载
5. **返回结果**：音频文件路径或发送给你

## 示例：中文朗读

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-flash",
    "input": {
      "text": "你好，我是千问语音助手，今天天气真不错。",
      "voice": "Cherry",
      "language_type": "Chinese"
    }
  }'
```

## 脚本说明

本技能包含两个脚本，按需使用：

### scripts/speak.sh
纯 Bash 脚本，**仅生成本地音频文件**，不需要飞书凭证
```bash
# 只需要 DASHSCOPE_API_KEY
./speak.sh "要转换的文本" [音色]
# 输出: /tmp/qwen_tts_xxx.ogg
```

### scripts/speak_and_send.py
Python 脚本，**生成 TTS 并发送到飞书**，需要配置飞书凭证
```bash
# 需要 DASHSCOPE_API_KEY + FEISHU_* 环境变量
python3 speak_and_send.py "要说的文本" [音色]
# 自动发送到配置的 FEISHU_USER_ID
```

## 参考资料

完整音色列表和 API 文档请参见：
- [references/voices.md](references/voices.md) - 全部音色列表
- [references/api.md](references/api.md) - 详细 API 说明

## 依赖说明

- `ffmpeg` - 音频格式转换（脚本需要）
- `jq` - JSON 处理（speak.sh 需要）
- `python3` + `requests` - speak_and_send.py 需要
