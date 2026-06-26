---
name: youtube-content
description: "YouTube视频转录与内容提取：字幕优先、Whisper兜底、批量处理、结构化笔记"
platforms: [linux, macos, windows]
---

# YouTube Content

从 YouTube 视频提取内容，转化为结构化输出（笔记、摘要、Thread、博客文章）。

## When to Use

- 用户分享 YouTube 链接（任何格式：标准URL、youtu.be短链、shorts、embeds、纯video ID）
- 需要视频摘要、转录、章节提取
- 需要从视频生成结构化笔记、Twitter/X thread、博客文章
- 批量处理多个视频

## 核心架构：字幕优先路由

```
YouTube URL
    │
    ├── 有字幕（zh-CN/zh-Hans/zh-Hant auto-subs）
    │   └── 下载字幕（即时，无需音频） → 生成笔记
    │
    └── 无字幕
        └── 下载音频 → Whisper 转录 → 生成笔记
```

**永远先检查字幕可用性**——字幕是即时的（无需下载），比 Whisper 更准确（尤其是中文自动字幕），每视频节省 ~20min。

## 快速开始

### 依赖

```bash
pip install youtube-transcript-api faster-whisper
```

### 单视频处理

```bash
# 1. 检查字幕
/opt/homebrew/Caskroom/miniconda/base/bin/yt-dlp --cookies-from-browser chrome \
  --proxy "http://127.0.0.1:$PROXY" --list-subs "URL" 2>&1 | grep -E "(has |zh-CN|zh-Hans)"

# 2a. 有字幕 → 直接下载
/opt/homebrew/Caskroom/miniconda/base/bin/yt-dlp --cookies-from-browser chrome \
  --proxy "http://127.0.0.1:$PROXY" \
  --write-auto-sub --sub-lang "zh-CN,zh-Hans,zh-Hant" --convert-subs srt --skip-download \
  -o "%(id)s.%(ext)s" "URL"

# 2b. 无字幕 → 下载音频 + Whisper
# 下载音频
/opt/homebrew/Caskroom/miniconda/base/bin/yt-dlp --cookies-from-browser chrome \
  --proxy "http://127.0.0.1:$PROXY" \
  -x --audio-format mp3 --audio-quality 0 -o "%(id)s.%(ext)s" "URL"

# Whisper 转录（后台运行）
python3 -c "
import faster_whisper
model = faster_whisper.WhisperModel('medium', device='cpu', compute_type='int8')
segments, info = model.transcribe('VIDEO_ID.mp3', language='zh', beam_size=5, vad_filter=True)
with open('VIDEO_ID.txt', 'w') as f:
    for seg in segments:
        f.write(seg.text.strip() + '\n')
print('=== WHISPER DONE ===')
"
```

### 字幕抓取（Python脚本）

`scripts/fetch_transcript.py` — 通过 youtube-transcript-api 获取字幕，支持多种 URL 格式：

```bash
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only           # 纯文本
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps          # 带时间戳
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language zh,en      # 指定语言
```

输出格式详见 `references/output-formats.md`。

## 输出格式

根据用户请求选择，默认为**结构化笔记**：

| 格式 | 适用场景 | 特点 |
|------|----------|------|
| **结构化笔记** | 中文视频默认 | 分层大纲、要点高亮、数据表格 |
| Summary | 英文/简短视频 | 5-10句概述 |
| Chapters | 演讲/TED | 时间戳+章节标题 |
| Chapter summaries | 长视频 | 每章+摘要段落 |
| Thread | 社交分享 | Twitter/X 编号格式，每条<280字符 |
| Blog post | 内容创作 | 完整文章，带引言和要点 |
| Quotes | 精选金句 | 带时间戳的名句 |

模板和详细规则见 `references/output-formats.md`。

## 完整处理流程

1. **获取**字幕（优先）或下载音频
2. **转录**（如需要 Whisper）
3. **验证**输出非空且完整
4. **转换**为目标格式
5. **交付**给用户

**长字幕处理**（SRT >1000行）：用 `delegate_task` 子代理分段读取（每次500行）生成笔记，避免撑爆主上下文。

## 批量处理

### 代理检测（必须首先执行）

```bash
PROXY=$(networksetup -getwebproxy Wi-Fi | grep -E '^Port' | awk '{print $2}')
```

**⚠️ 代理端口不固定**——取决于当前 VPN/代理工具配置。所有 yt-dlp 命令必须使用 `$PROXY` 变量。

### 🚨 关键规则：禁止并行 Whisper

**Whisper 会占满所有 CPU 核心（300%+），两个并行 Whisper 都会慢 2-3 倍，总耗时比顺序执行更差。**

**每次启动 Whisper 前：**
1. `process(action='list')` 检查是否有 python 进程在运行
2. 如果有 Whisper 进程，**等待它完成**再启动下一个
3. 3+ 个视频 → 使用 `batch_whisper.py`（模型只加载一次）

### 批处理策略

#### 大批量（10+ 个 Whisper 视频）：两阶段（推荐）
```
Phase 1: 下载所有音频（单个后台 for 循环）
Phase 2: batch_whisper.py 后台运行，同时用 delegate_task 处理字幕视频笔记
Phase 3: Whisper 全部完成 → 并行 delegate_task 生成所有笔记
```

#### 中批量（3-9 个）：batch_whisper.py + 增量笔记
```
Phase 1: 下载所有音频
Phase 2: batch_whisper.py（后台）
Phase 3: 每出现新 .txt → delegate_task 生成笔记
```

#### 小批量（1-2 个）：流水线
```
Whisper A 完成 → 同时：delegate_task(A) + Whisper B
```

### batch_whisper.py

`scripts/batch_whisper.py` — 批量 Whisper 转录脚本，模型只加载一次，顺序处理：

```bash
# 找出所有缺 .txt 的 mp3 文件
cd youtube_downloads
VIDEOS=$(for f in *.mp3; do vid="${f%.mp3}"; [ ! -f "${vid}.txt" ] && echo "$f"; done)

# 单后台进程运行
python3 SKILL_DIR/scripts/batch_whisper.py $VIDEOS \
  --language zh --model medium --device cpu --compute-type int8
```

后台运行：`background=true, notify_on_complete=true, timeout=3600`

### 子代理笔记生成模板

```python
goal: """读取 /path/to/VIDEO_ID.txt 转录文件，整理成结构化中文笔记。

视频信息：
- 标题：<video title>
- 时长：<duration>
- 频道：<channel name>

要求：
1. 读取完整转录文件（分段读取每次500行）
2. 整理成结构化笔记：📌核心主题、📊关键数据、🔍主要观点、💡关键洞察
3. 忠实原始内容，写入 /path/to/VIDEO_ID_notes.md"""
context: "读取转录文本并整理成结构化中文笔记"
toolsets: ["file"]
```

### 队列状态沟通

**紧凑格式**（默认）：`📊 队列更新：✅ N完成 | 🔄 1转录中 | ⏳ X排队`

**表格格式**（≤5项时）：
```
| # | ID | 标题 | 时长 | 状态 |
```

状态 emoji：✅ 完成、🔄 处理中、⏳ 排队、⚠️ 错误

## 错误处理

| 错误 | 处理 |
|------|------|
| 无字幕/字幕已禁用 | 自动走 Whisper 流程，无需确认 |
| 私有/不可用视频 | 告知用户验证 URL |
| Members-only | 告知用户需要频道会员，无法绕过 |
| "Sign in to confirm you're not a bot" | 更新 yt-dlp + `--remote-components ejs:github` |
| Whisper 产出空文件（0字节） | 删除重跑，已验证重跑通常成功 |
| Whisper 截断（覆盖率<90%） | 检查最后时间戳 vs 音频时长，不够则重跑 |

更多 yt-dlp/Whisper 坑点和解决方案见 `references/whisper-transcription.md`。

## 环境特定注意事项

- **macOS 代理**：yt-dlp 不继承系统代理，必须显式传 `--proxy`，且端口不固定
- **yt-dlp 双版本陷阱**：macOS 上有 Homebrew（旧）和 conda（新）两个版本，始终用 conda 版本
- **Chrome cookies**：`--cookies-from-browser chrome` 可能静默返回 0 cookies（解密失败），需检查

## 进阶功能

### 标题党检测

部分中文视频标题与内容不符（如标题"2026经济崩盘"实际讲乐观内容）。`delegate_task` 子代理通常能检测到这种不匹配，在笔记中加 ⚠️ 标记。

### 飞书知识库集成

大批量完成后，可整合写入飞书知识库（需 `lark-wiki` + `lark-doc` skills + user auth scopes）。
