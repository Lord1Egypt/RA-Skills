# 英语助教 · English Tutor Skill

> **模块化基座 Skill** — 功能按需配置，所有环境变量均为**选填**。
> 有配置就启用对应功能，无配置则跳过。完整功能需要飞书 + MiniMax + 多维表格。

---

## 功能模块（按需启用）

| 模块 | 环境变量 | 说明 |
|------|---------|------|
| 飞书语音推送 | `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_USER_OPEN_ID` | 发 TTS 语音到飞书 |
| MiniMax TTS | `MINIMAX_API_KEY` | 云端语音合成（主方案） |
| Piper 本地 TTS | `PIPER_BIN`, `PIPER_MODEL` | 完全离线的语音兜底 |
| SenseVoice 本地 ASR | `SENSE_VOICE_MODEL_DIR` | 完全离线的语音识别 |
| 多维表格记忆 | `BITABLE_APP_TOKEN`, `BITABLE_WORDS_TABLE_ID`, `BITABLE_CHAT_TABLE_ID` | 单词记录 + 艾宾浩斯 |
| 定时推送 | cron jobs | 08:00 / 12:00 / 20:00（可单独开启） |

**原则**：填了变量 → 启用该模块；没填 → 该模块静默跳过，不报错。

---

## 文件结构

```
english-tutor/
├── SKILL.md
├── metadata.json
├── _meta.json
├── agent/                    ← 核心 Node.js 运行时
│   ├── config.js             ← 配置（全部选填，env 注入）
│   ├── minimax.js            ← MiniMax TTS + Chat API
│   ├── memory.js             ← 多维表格记忆（可选）
│   └── agent.js              ← 主流程入口
├── scripts/                  ← Python 辅助脚本
│   ├── check_env.py          ← 环境检测
│   ├── config_manager.py     ← 配置管理
│   ├── download_model.py     ← SenseVoice 模型下载
│   ├── feishu_voice.py       ← 飞书语音发送（TTS→Opus→上传→发送）
│   ├── transcribe.py         ← ASR 转录（本地/云端）
│   └── wordlist_parser.py    ← 单词表解析器
├── references/
│   └── config-schema.md
└── assets/
    └── wordlist_example.csv
```

---

## 环境变量（全部选填）

### 飞书模块

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FEISHU_APP_ID` | `""` | 飞书应用 App ID（填了才发飞书语音） |
| `FEISHU_APP_SECRET` | `""` | 飞书应用 Secret |
| `FEISHU_USER_OPEN_ID` | `""` | 接收语音的飞书用户 Open ID |

### TTS 模块

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MINIMAX_API_KEY` | `""` | MiniMax API Key（不填则跳过云端 TTS） |
| `MINIMAX_TTS_MODEL` | `speech-2.8-hd` | TTS 模型 |
| `MINIMAX_TTS_SPEED` | `1.05` | 语速 |
| `MINIMAX_TTS_VOICE_ID` | `male-qn-qingse` | 音色 ID |
| `PIPER_BIN` | `""` | Piper 主程序路径（不填则跳过本地 TTS） |
| `PIPER_MODEL` | `""` | Piper ONNX 模型路径 |
| `TTS_PROVIDER` | `minimax` | 优先方案：`minimax` / `piper` |

### ASR 模块

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SENSE_VOICE_MODEL_DIR` | `""` | SenseVoice 模型目录（不填则跳过本地 ASR） |

### 多维表格模块

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `BITABLE_APP_TOKEN` | `""` | App Token（不填则无艾宾浩斯记忆） |
| `BITABLE_WORDS_TABLE_ID` | `""` | words 表 ID |
| `BITABLE_CHAT_TABLE_ID` | `""` | chat_log 表 ID |

### 每日练习配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DAILY_WORD_MAX` | `15` | 每日新词上限 |

---

## 凭据声明（metadata）

本 skill 为 **Credential-Using Skill**，但**所有凭据均为选填**：

```json
{
  "credential_using": true,
  "required_credentials": [],
  "optional_credentials": [
    { "name": "FEISHU_APP_ID",      "description": "飞书语音推送" },
    { "name": "FEISHU_APP_SECRET",  "description": "飞书语音推送" },
    { "name": "FEISHU_USER_OPEN_ID","description": "飞书语音推送" },
    { "name": "MINIMAX_API_KEY",    "description": "云端 TTS + LLM 对话" },
    { "name": "BITABLE_APP_TOKEN",  "description": "艾宾浩斯记忆（可选）" },
    { "name": "BITABLE_WORDS_TABLE_ID", "description": "单词记录表" },
    { "name": "BITABLE_CHAT_TABLE_ID",  "description": "对话历史表" }
  ]
}
```

---

## 定时任务

| 时间 | cron | 说明 |
|------|------|------|
| 晨间 | `0 8 * * *` | 通勤场景跟读 |
| 午间 | `0 12 * * *` | 口语问答 |
| 晚间 | `0 20 * * *` | 复盘 + 旧词复习 |

**定时任务默认关闭**，用户在引导设置中自行选择开启哪些。

---

## 引导设置流程（用户可选配置）

### 第 1 步：飞书配置（选填）
- 提供 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_USER_OPEN_ID`
- 不填则无飞书语音推送功能

### 第 2 步：TTS 配置（选填）
- MiniMax：提供 `MINIMAX_API_KEY`
- Piper 本地：提供 `PIPER_BIN` / `PIPER_MODEL`
- 都不填则 TTS 功能不可用（仍有文字对话）

### 第 3 步：ASR 配置（选填）
- 提供 `SENSE_VOICE_MODEL_DIR`（或运行 `python3 scripts/download_model.py`）
- 不填则无法处理语音输入（仅支持文字）

### 第 4 步：多维表格（选填）
- 提供 `BITABLE_APP_TOKEN` + 两个表 ID
- 不填则无艾宾浩斯记忆功能（仍可练习，但不记录进度）

### 第 5 步：每日定时（选填）
- 选择开启哪些时段（08:00 / 12:00 / 20:00）
- 不选择则不创建 cron 任务

### 第 6 步：上传单词表（选填）
- CSV 或纯文本格式
- 不上传也可进行自由对话练习

---

## 核心模块说明

### feishu_voice.py — 飞书语音发送
- 优先 MiniMax TTS，配额耗尽自动切换 Piper
- 无任何凭据配置时：静默跳过，不报错
- 流程：TTS → ffmpeg 转 Opus → 上传飞书 → 发送 audio 消息

### transcribe.py — ASR 转录
- 本地 SenseVoice（默认），也支持 AssemblyAI/OpenAI Whisper
- 无本地模型时：回退到文字输入模式
- 使用列表形式 subprocess，无 shell 注入

### memory.js — 多维表格
- 无多维表格配置时：`_isReady()` 返回 false，所有方法静默跳过
- 所有操作有 try/catch，不因单次失败中断流程

### agent.js — 主流程
- **课程模式**（定时触发，无用户输入）：自动生成跟读对话，逐条发飞书语音
- **交互模式**（用户发消息）：实时对话 + 可选 TTS 回复
- 所有模块都是**失败静默跳过**，不影响其他模块运行

---

## 安全设计原则

1. **所有密钥通过环境变量注入**，不硬编码
2. **feishu_voice.py**：配置通过 `env=` 参数传递给 Node.js 子进程（内存传递）
3. **scripts/ 无 shell=True**：subprocess 使用列表形式
4. **config.json 权限**：`~/.openclaw/english-tutor/config.json` 设为 `600`
5. **全部源码纳入 skill 包**，审查者可查看全部代码（agent/ + scripts/）

---

## 模型下载命令

### Piper TTS（本地语音合成）

```bash
mkdir -p /vol1/@apphome/trim.openclaw/data/workspace/piper/voices
curl -L https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz \
  -o /tmp/piper.tar.gz && tar xf /tmp/piper.tar.gz -C /tmp
curl -L "https://hf-mirror.com/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx" \
  -o /vol1/@apphome/trim.openclaw/data/workspace/piper/voices/en_US-lessac-medium.onnx
```

### SenseVoice ASR（本地语音识别）

```bash
pip install --user --break-system-packages numpy sherpa-onnx
python3 /vol1/@apphome/trim.openclaw/data/workspace/skills/english-tutor/scripts/download_model.py
```

---

## 单词表格式

**CSV（推荐）：**
```csv
word,pronunciation,meaning,example
commute,/kəˈmjuːt/,通勤,I commute by subway every day.
```

**纯文本（每行一个）：**
```
commute,通勤
subway,地铁
transfer,换乘
```

---

## 艾宾浩斯复习周期

| 复习轮次 | 间隔 |
|---------|------|
| 第 1 次 | 次日 |
| 第 2 次 | 3 天后 |
| 第 3 次 | 7 天后 |
| 第 4 次 | 15 天后 |
| 第 5 次+ | 掌握（不再自动提醒）|