---
name: voice2notion
version: 1.2.0
description: 语音录音转录并保存到 Notion 数据库。使用 faster-whisper 转录，自动提取关键信息并写入数据库。
author: JiabaoChen
tags: [voice, transcription, notion, faster-whisper]
readiness: manual-install
install:
  python: "uv pip install faster-whisper"
  model: "faster-whisper 模型文件（首次运行自动下载）"
config:
  - path: ~/.config/notion/api_key
    description: Notion API Key 文件
    required: true
  - env: NOTION_DATABASE_ID
    description: Notion 数据库 ID
    required: true
---

# Voice2Notion 工具

将语音转录保存到 Notion 数据库

## 功能

- 语音转录（faster-whisper）
- 自动提取关键信息
- 保存到 Notion 数据库
- 保存录音文件链接

> 💡 推荐使用 `medium` 或 `large` 模型以获得更好的转录效果

## 前置要求

### 1. Notion 模板（推荐）

**复制模板到你的工作空间:**
https://www.notion.so/4e667ba767e2414a9f89041471d5f85d

模板包含：
- 上传记录数据库（预设所有必需列）
- 录音记录模板页面

**获取数据库 ID:**
1. 打开复制的数据库
2. 从 URL 获取 ID：`https://www.notion.so/数据库ID?v=...`

### 2. 安装依赖

```bash
# 创建虚拟环境
cd ~/.openclaw
uv venv .venv
source .venv/bin/activate

# 安装 faster-whisper
uv pip install faster-whisper
```

> ⚠️ 首次转录时会自动下载模型（约 140MB for base，~1GB for medium）

### 3. 配置 Notion

**获取 API Key:**
1. 访问 https://www.notion.so/my-integrations
2. 创建新的 Integration
3. 复制 API Key

**分享数据库给 Integration:**
1. 在 Notion 中打开目标数据库
2. 点击 Share → Add emails
3. 添加你的 Integration 邮箱

**设置配置:**
```bash
# 保存 API Key
echo "你的 Notion API Key" > ~/.config/notion/api_key

# 设置数据库 ID（可选，也可以在命令中传入）
export NOTION_DATABASE_ID="你的数据库ID"
```

## 工作流程

### Step 1: 接收语音并转录
- 用户发送语音消息（.m4a）
- 使用 faster-whisper 转录为文字

### Step 2: 润色并提取信息
- 润色转录文本（修正错误、补全字词、语句通顺）
- 提取数据库字段

### Step 3: 添加到数据库
- 在数据库中创建记录
- 在记录页面中添加完整内容
- 保存录音文件链接

---

## 转录命令

```bash
# 激活虚拟环境
cd ~/.openclaw
source .venv/bin/activate

# 转录音频（使用 medium 模型，效果更好）
python3 << 'EOF'
from faster_whisper import WhisperModel

# 可选模型: tiny, base, small, medium, large
# larger = better accuracy, slower speed
model = WhisperModel('medium', device='cpu', compute_type='int8')
segments, info = model.transcribe('/path/to/audio.m4a')

text = ' '.join([s.text.strip() for s in segments])
print(f"语言: {info.language}")
print(f"转录: {text}")
EOF
```

## 保存录音文件

Notion API 支持两种方式保存文件：

### 方式 1: 外部链接（推荐）

将录音上传到可公开访问的 URL，然后在 `录音链接` 字段填写 URL：

```python
# 数据库属性
"录音链接": {"url": "https://example.com/audio.m4a"}
```

### 方式 2: 上传到云盘后添加链接

1. 将音频文件上传到云盘（Google Drive、Dropbox 等）
2. 获取公开分享链接
3. 填写到 `录音链接` 字段

### 数据库列要求

| 列名 | 类型 | 说明 |
|------|------|------|
| Name | 标题 | 必填 |
| 讨论主题 | 文本 | 录音主题 |
| 录音日期 | 日期 | 文件日期 |
| 录音链接 | URL | 录音文件地址 |

### 基本用法

```bash
# 激活虚拟环境
cd ~/.openclaw
source .venv/bin/activate

# 设置数据库 ID（替换为你的）
export NOTION_DATABASE_ID="你的数据库ID"

# 转录音频
python3 transcribe.py /path/to/audio.m4a
```

### 数据库列要求

| 列名 | 类型 | 说明 |
|------|------|------|
| Name | 标题 | 必填 |
| 讨论主题 | 文本 | 录音主题 |
| 录音日期 | 日期 | 文件日期 |
| 处理状态 | 单选 | 待整理/整理中/已归档 |
| 关键要点 | 文本 | 要点列表 |
| 待办事项 | 文本 | 待办列表 |
| 转录结果 | 文本 | 完整转录 |
| 类型 | 多选 | 讨论/会议/笔记 |
| 已上传 | 复选框 | ✅ |

---

## 安全说明

- API Key 存储在本地文件 `~/.config/notion/api_key`
- 不要将 API Key 提交到公开仓库
- 定期轮换 API Key
- 使用环境变量传递数据库 ID

---

## 故障排除

**转录失败:**
- 确认虚拟环境已激活
- 确认 faster-whisper 已安装: `pip list | grep faster-whisper`

**Notion API 错误:**
- 确认 API Key 正确
- 确认数据库已分享给 Integration
- 确认数据库列名匹配
