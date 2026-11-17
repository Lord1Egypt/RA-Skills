---
name: video-to-article
description: 将视频、字幕文件或大型课程目录转换为结构化图文笔记。仅当用户明确要求执行完整的视频转文章工作流，例如下载视频、生成图文文章、写入 Obsidian 或批量导入课程时使用；如果用户只想做摘要、问答、术语提取或轻量分析，应优先采用只读分析流程。
allowed-tools: Read, Write, Terminal, File, Vision, Search
---

# Video to Article 全能视频转图文工作流

这个技能用于把视频内容转换成可读、可复用的图文笔记，偏重实际可落地的生产流程。

## 安全边界与执行原则

默认先走**只读预览模式**，不要一上来就下载、写文件、执行脚本或提交 Git。

### 只读预览模式

适用于用户只想：
- 看视频是否可下载
- 获取元信息
- 评估转录方案
- 规划截图和文章结构
- 基于字幕做总结、问答、术语提取

在这个模式下：
- 不下载视频
- 不写入 Vault 或仓库
- 不执行生成脚本
- 不做 `git commit` 或 `git push`

### 执行模式

只有在用户**明确确认**后，才允许执行以下有副作用的操作：
- 下载视频或字幕
- 使用 Cookie / 登录态
- 写入 Obsidian Vault、课程目录或仓库
- 执行 `_batch_screenshots.sh` 这类生成脚本
- 修改 `index.md`、写日志、`git commit`
- `git push`

### 明确限制

- 如果用户没有明确给出输出目录，不要擅自写入默认路径
- 如果内容涉及付费、私有或登录后资源，先确认用户有权访问
- 不要在回复、日志、笔记或仓库中泄露 Cookie、Token 或其他认证信息
- 对任何将要执行的 shell 脚本，先展示用途、输出路径和关键命令，再执行
- `git push` 必须单独确认，不能视为默认收尾步骤

## 核心能力矩阵

| 模式 | 输入 | 输出 | 适用场景 |
|------|------|--------|---------|
| **A: 单视频笔记** | 视频 URL 或本地视频文件 | 图文混排 Obsidian 笔记，可选 Git 推送 | 影评、教程、做饭视频、Vlog |
| **B: 字幕学习** | 已有字幕文件（`.srt` / `.vtt`） | 摘要、测验、词汇表、章节笔记、问答 | 基于已有转录内容学习 |
| **C: 大课程导入** | 含大量视频的课程文件夹 | Section 级图文文章和索引 | Udemy / 慕课 / 培训课程批量导入 |

## 模式 A：单视频转图文笔记

### 常见触发词

只有在用户明确表达“要落盘执行”时再触发完整工作流，例如：

- “把这个视频整理成可落盘的图文笔记”
- “下载视频并生成 Obsidian 图文文章”
- “把整个课程目录批量导入成文章”
- “基于字幕生成学习材料，但不要修改本地文件”

如果用户只是说“总结一下视频”或“帮我看看讲了什么”，优先走只读分析，不要自动进入下载和写文件流程。

### 工作流

#### Step 1：识别平台和认证需求

| 平台 | 是否通常需要 Cookie | 格式策略 | 备注 |
|------|------|------|------|
| Bilibili (`b23.tv` / `bilibili.com`) | 通常需要 | 先跑 `-F`，再显式选择格式 ID | BV 号视频，可能遇到 `412` 反爬 |
| YouTube (`youtube.com` / `youtu.be`) | 通常不需要 | 优先 `bestvideo[height<=720]+bestaudio` | 下载相对直接 |
| TED / Coursera / Udemy | 视情况 | 先跑 `-F` | 付费内容可能要求登录 |
| 抖音 / TikTok / 小红书 | 通常不需要 | 自动选择通常够用 | 短视频居多 |
| 其他 1700+ 平台 | 视情况 | 先跑 `-F` | 需要时用平台特定兜底策略 |

Bilibili Cookie 导出示例：

```bash
# 将浏览器 Cookie 导出成 Netscape 格式
python3 path/to/bili_cookie_to_netscape.py
```

Cookie 安全要求：
- Cookie 属于敏感认证信息，等同于登录态
- 仅在用户明确授权访问其账号可见内容时使用
- 不要把 Cookie 写入仓库、笔记、日志或聊天输出
- 如果只是公开内容预览，优先先尝试无 Cookie 方案

#### Step 2：解析视频 ID 并获取元信息

```bash
# 解析 Bilibili 短链
VIDEO_ID=$(curl -sL "https://b23.tv/XXXXX" -o /dev/null -w "%{url_effective}" | sed 's/.*\/video\///;s/[\/?].*//')

# 不下载直接读取元信息
yt-dlp --no-download --print "%(title)s|%(duration)s|%(uploader)s" "<URL>"
```

#### Step 3：下载视频

这是**有副作用操作**。只有在用户明确同意下载，并且已经确认输出目录后再执行。

实用默认策略：
- 小于 4 分钟：优先 1080p
- 大于等于 4 分钟：优先 720p

```bash
# 先查看可用格式
yt-dlp -F "<URL>"

# 下载（Bilibili 需要时加 --cookies）
mkdir -p "<TEMP_DIR>/<VIDEO_ID>"
yt-dlp -o "<TEMP_DIR>/<VIDEO_ID>/video.%(ext)s" \
  -f "<chosen-format-id>" --merge-output-format mp4 "<URL>"
```

#### Step 4：用 Whisper 转录

如果用户只是要摘要或问答，优先复用现有字幕或已有转录，不要默认重新下载并转录整段视频。

```bash
python3 << 'PYEOF'
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="float32",
                     download_root="<CACHE_DIR>")
segments, _ = model.transcribe("<TEMP_DIR>/<ID>/video.mp4", language="zh", beam_size=5)
with open("<TEMP_DIR>/<ID>/transcript.txt", "w") as f:
    for seg in segments:
        f.write(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text.strip()}\n")
PYEOF
```

语言建议：
- 中文：`language="zh"`
- 英文：`language="en"`
- 自动识别：省略语言参数

模型取舍：
- `tiny`：最快
- `base`：推荐默认
- `small`：更准但更慢

Apple Silicon 加速：
- `device="mps", compute_type="float16"`

#### Step 5：先分类内容，再规划截图

先根据转录内容判断视频类型，再决定截图密度。

| 视频类型 | 特征 | 截图数量 | 密度规则 |
|------|------|------|------|
| **讲演 / 影评 / 长分析** | 论点推进，口播为主 | 8-12 | 大约每 30-40 秒 1 张 |
| **教程 / 实操演示** | 步骤递进，UI 或代码变化明显 | 3-8 | 每个关键步骤 1 张 |
| **论坛 / 对谈** | 多人发言，话题切换明显 | 5-8 | 说话人切换或话题转折时截 |
| **Vlog / 随口杂谈** | 叙事松散 | 3-5 | 按场景变化截 |
| **30 秒以内** | 单点信息 | 1 | 开头帧即可 |
| **30-120 秒** | 短内容分段明显 | 3-5 | 按段落切分 |

截图时间点经验：
- 讲演类：标题画面、引出核心概念、每个主要论点首帧、金句时刻、结尾
- 教程类：每个关键步骤变化、UI 切换、结果展示画面
- 避免截图：填充性口播、画面没变化的 talking head、重复画面

命名规范：
- 使用英文 kebab-case
- 使用两位数字前缀
- 例如：`01-intro.jpg`、`02-core-concept.jpg`

#### Step 6：批量抽帧

这是**文件写入操作**。执行前先确认截图输出目录和命名规则。

```bash
VIDEO="<TEMP_DIR>/<ID>/video.mp4"
OUTDIR="<TEMP_DIR>/<ID>/screenshots"
mkdir -p "$OUTDIR"
ffmpeg -y -ss <seconds> -i "$VIDEO" -frames:v 1 "$OUTDIR/01-intro.jpg"
```

#### Step 7：生成图文笔记

这是**持久化写入操作**。只有在用户明确要求写入 Vault 或指定目录后再执行。

```bash
mkdir -p "<VAULT>/assets/video/<VIDEO_ID>"
cp <TEMP_DIR>/<ID>/screenshots/*.jpg "<VAULT>/assets/video/<VIDEO_ID>/"
```

推荐笔记结构：

```markdown
---
title: <核心主题>
source: <Bilibili|YouTube|...>
author: <作者>
type: 文献笔记
tags: [视频笔记, <主题标签>]
created: <YYYY-MM-DD>
---

# <作者>：<标题>

> **来源**：<平台> @<作者>

## 核心洞见
1-2 段概括

![[../../../assets/video/<ID>/02-xxx.jpg]]

## <分节标题>
...
![[../../../assets/video/<ID>/xxx.jpg]]
> "<转录中的引用原文>"

## 行动清单
- [ ] ...

## 金句
> ...

## 相关笔记
- [[已有笔记]] - 关联原因
```

图片引用格式：

```markdown
![[../../../assets/video/<ID>/<filename>.jpg]]
```

#### Step 8：把笔记接入知识库

默认只给出关联建议。只有在用户明确要求更新知识库时，才执行全文搜索和实际写入动作。

```bash
find "<VAULT>" -name "*.md" | xargs grep -li "<core keyword>"
```

#### Step 9：提交并推送

这一步必须拆开处理：
- `git add` / `git commit` 仅在用户明确要求版本化本次结果时执行
- `git push` 必须单独确认，不能默认执行

```bash
cd "<VAULT>" && git add -A && git commit -m "video note: <title>" && git push
```

## 模式 B：基于字幕学习

### 常见触发词

“学习这个字幕”、“总结这个转录”、“根据这个字幕出题”、“整理术语”、“考考我这个视频”

### 输入来源

| 来源 | 获取方式 | 预处理 |
|------|------|------|
| 自带 `.srt` / `.vtt` 字幕 | 直接读取 | 优先使用 |
| 下载的视频但没有字幕 | 用 `yt-dlp` 字幕下载或 Whisper | 先去时间码转纯文本 |
| 用户直接粘贴字幕 | 直接使用 | 清洗后可直接分析 |

### 学习模式

#### B1：知识提取（默认）

输出结构化学习指南，包括：
- Key Concepts
- Key Takeaways
- Examples
- Glossary

#### B2：章节摘要

按主题切换拆章，每章总结 2-3 句。

主题切换信号：
- 过渡语，例如 “Now let's talk about...”
- 大于 5 秒的长停顿
- 突然引入大量新术语

#### B3：关键词汇表

提取领域术语、高频词、明确定义的概念和缩写。输出表格包含：
- 术语
- 需要时的翻译
- 上下文解释
- 出现位置

### 字幕预处理

原始字幕文件通常大部分都是元数据，先清理再分析。

```python
import re
def strip_srt(srt_text):
    lines = srt_text.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line): continue
        if re.match(r'^\d{2}:\d{2}:\d{2}', line): continue
        if not line: continue
        result.append(line)
    return ' '.join(result)
```

### 常见陷阱

- **字幕非常大**：分块读取，单次最好不超过 1500 行
- **ASR 误识别**：标记为 `[possible transcription error]`
- **内容强依赖视觉**：标记为 `[visual content here]`
- **多人对话**：自动字幕可能会把说话人混在一起

## 模式 C：大型课程批量导入

### 六阶段流程

| Phase | 目的 | Token 策略 |
|------|------|------|
| 1. 目录分析 | 建立 section 和 lesson 树 | Token 很低 |
| 2. 字幕预处理 | 把字幕批量转成纯文本 | 终端脚本，零 token |
| 3. 截图规划 | 预计算 slug 和 `ffmpeg` 命令 | 终端脚本，零 token |
| 4. 批量截图 | 后台运行 `ffmpeg` | 终端脚本，零 token |
| 5. 并行写文章 | 最多 3 个子代理并发处理 section | 只传纯文本和 slug 表 |
| 6. 收尾 | 生成 `index.md` 和导入日志 | Token 很低 |

### Phase 1：目录分析

遍历课程目录，建立如下结构：

```text
{Section: [video list]}
```

课程名和课时名要按数字前缀精确匹配。

### Phase 2：字幕预处理

使用 `scripts/preprocess-srt.py`：
1. 修改课程配置
2. 运行脚本
3. 读取 `_preprocessed/section-<slug>.txt`

如果用户只想先评估课程结构或输出效果，先展示计划，不要立即批量写文件。

### Phase 3：截图规划

使用 `scripts/plan-screenshots.py` 根据时长和内容类型决定截图点。

预期输出：
- `_screenshot_plan.json`
- `_batch_screenshots.sh`

### Phase 4：批量截图

`_batch_screenshots.sh` 属于生成脚本。执行前必须：
1. 预览脚本内容
2. 确认输出目录仅落在预期课程或资源目录
3. 获得用户对执行批处理命令的明确确认

```bash
bash _batch_screenshots.sh
```

顺序运行更稳。`ffmpeg` 比较吃 CPU，不建议并发抽帧；如果用户未确认，也不要默认后台启动。

### Phase 5：并行写文章

子代理上下文写法会强烈影响 token 浪费情况，遵守这三条：

1. 明确说明截图已经准备好，不要重复验证
2. 提供完整的 slug 到 label 映射，不让子代理自己算名字
3. 明确列出哪些课不放截图

示例上下文：

```python
context = """
用英文写课程笔记。

Input: _preprocessed/section-01.txt

All screenshots are already prepared. Do not verify files.
Reference them directly as:
  ![[../../../assets/<course>/<slug>-<label>.jpg]]

Slug table (each slug has overview/detail/result unless noted otherwise):
- Installation -> installation (3 images)
- Intro -> intro (no screenshots)

Density: Intro gets no screenshots. Other lessons get 3 screenshots each.

Output: sources/<course>/section-01-xxx.md
"""
```

并行分配建议：
- 最多 3 个子代理
- 每个子代理最多 4 个 section

### Phase 6：收尾

1. 只允许主代理更新 `index.md`
2. 写导入日志
3. 如用户明确要求，再提交到 Git

这里涉及仓库文件修改，默认应先展示将要变更的文件范围，再执行实际写入。

## 前置条件

- `yt-dlp`：下载视频
- `ffmpeg`：音频处理和截图
- `faster-whisper`：语音转录
- 一个最好由 Git 管理的 Obsidian Vault
- `git`：版本控制和同步

环境检查：

```bash
which yt-dlp ffmpeg 2>&1
python3 -c "from faster_whisper import WhisperModel; print('OK')" 2>&1
```

## 路径约定

| 变量 | 用途 | 示例 |
|------|------|------|
| `<TEMP_DIR>` | 临时下载和处理目录 | 项目内临时目录 |
| `<VAULT>` | Obsidian 库根目录 | `~/Documents/Obsidian` |
| `<ATTACH_DIR>` | Vault 内截图目录 | `<VAULT>/assets/video/<VIDEO_ID>/` |
| `<NOTE_DIR>` | 笔记输出目录 | `<VAULT>/reference-notes/` |

## 排错

| 问题 | 解决方式 |
|------|------|
| Bilibili `412` 反爬 | 刷新 Cookie 并重新登录 |
| Bilibili 格式 ID 失效 | 先跑 `-F`，因为每个视频的 ID 可能不同 |
| YouTube 下载失败 | 处理地区限制，或降级到 `-f "best[height<=720]"` |
| Whisper 太慢 | 切到 `tiny`，或在 Apple Silicon 上用 `device="mps"` |
| 截图文件名导致链接混乱 | 使用英文 kebab-case |
| Git push 失败 | 先确认用户仍然希望推送，再试 `git pull --rebase && git push` |
| 子代理反复验证截图 | 硬编码 slug 表，并明确写 `do not verify files` |
