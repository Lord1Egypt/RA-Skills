# Skill: video_to_skill_extractor

## 1. Skill 名称

video_to_skill_extractor

## 2. Skill 目标

把技术教程视频自动转换为可复用的 AI 工作流 Skill。

本 Skill 用于让 OpenClaw / Codex / AI Agent 自动理解一个视频的内容，包括：

- 视频标题
- 视频简介
- 视频字幕
- 视频人声文案
- 视频画面
- 屏幕录制内容
- 代码截图
- 终端报错
- PPT文字
- 网页操作过程
- 作者讲解的方法论
- 可以沉淀为 Skill 的规则、流程、提示词和检查清单

最终输出一个新的 Skill 文档，用于指导后续 AI Agent 执行相同类型的任务。

典型用途：

- 从 Bilibili / YouTube / 抖音 / 小红书技术教程中提取方法论
- 把“Vibecoding 修 Bug 教程”变成 Codex Debug Skill
- 把“AI 编程经验视频”转化为 OpenClaw 工作流
- 把“网站开发教程”转化为项目开发规范
- 把“材料实验视频”转化为实验记录或实验分析 Skill

---

## 3. 触发条件

当用户提出以下请求时，应调用本 Skill：

- “帮我理解这个视频内容”
- “把这个视频总结成 skill”
- “把这个 B 站视频变成 OpenClaw skill”
- “让 AI 自己看视频并提炼方法论”
- “从视频里提取提示词”
- “从视频教程生成 Codex 提示词”
- “把视频里的操作流程整理出来”
- “根据这个视频生成自动化工作流”
- “分析视频里的画面和文案”
- “提取视频里的 debug 方法”
- “把这个教程沉淀为一个可复用 skill”

---

## 4. 输入

用户至少需要提供以下一种输入：

```text
视频网址
````

例如：

```text
https://www.bilibili.com/video/BV1p8DeBtEbH/
```

也可以提供：

```text
本地视频文件路径
音频文件路径
字幕文件路径
视频截图目录
视频标题
视频主题
用户希望生成的 Skill 方向
```

推荐输入格式：

```json
{
  "video_url": "https://www.bilibili.com/video/BV1p8DeBtEbH/",
  "video_theme": "Vibecoding 遇到 Bug 怎么修？新手必看的 AI 改bug指南",
  "target_skill_name": "vibecoding_bugfix_debug_skill",
  "target_user": "Codex / OpenClaw / AI Agent",
  "output_language": "zh-CN"
}
```

---

## 5. 输出

本 Skill 必须在输出目录中生成以下文件：

```text
output/
├── 01_video_metadata.json
├── 02_transcript_raw.txt
├── 03_transcript_clean.md
├── 04_visual_notes.md
├── 05_ocr_notes.md
├── 06_timeline.json
├── 07_extracted_principles.md
├── 08_generated_skill.md
├── 09_evidence_map.json
└── 10_debug_report.md
```

其中最重要的是：

```text
08_generated_skill.md
```

这是最终可以安装到 OpenClaw 的 Skill 文件。

---

## 6. 核心原则

### 6.1 不允许只看标题就总结

AI 不得仅根据视频标题、简介或用户描述编造 Skill。

必须尽可能提取：

* 字幕
* 音频转写
* 画面关键帧
* OCR文字
* 屏幕操作过程

如果某部分无法获取，必须在报告中说明。

### 6.2 不允许一次性把所有内容塞给大模型

长视频必须分段处理。

推荐策略：

```text
视频 → 分段 → 每段摘要 → 每段提取规则 → 全局合并 → 生成 Skill
```

### 6.3 必须区分“视频明确提到”和“AI推断”

输出内容中必须区分：

```text
【视频明确提到】
【画面证据显示】
【AI合理推断】
【无法确认】
```

### 6.4 必须生成可执行的 Skill

最终 Skill 不能只是普通摘要。

必须包含：

* 触发条件
* 输入要求
* 执行步骤
* 禁止行为
* 检查清单
* 提示词模板
* 验证方法
* 输出格式

---

## 7. 工作目录规范

执行任务时，应创建如下目录结构：

```text
video_to_skill_workspace/
├── raw/
│   ├── video.mp4
│   ├── audio.wav
│   ├── subtitle.srt
│   ├── subtitle.vtt
│   ├── info.json
│   └── thumbnail.jpg
├── frames/
│   ├── frame_00001.jpg
│   ├── frame_00002.jpg
│   └── ...
├── ocr/
│   ├── frame_00001.json
│   ├── frame_00002.json
│   └── ...
├── transcript/
│   ├── transcript_raw.txt
│   ├── transcript_clean.md
│   └── transcript_segments.json
├── timeline/
│   └── timeline.json
├── notes/
│   ├── visual_notes.md
│   ├── extracted_principles.md
│   └── evidence_map.json
└── output/
    ├── generated_skill.md
    └── debug_report.md
```

---

## 8. 执行流程

## Step 1：解析任务

首先读取用户输入，识别：

```json
{
  "video_url": "",
  "local_video_path": "",
  "target_skill_name": "",
  "target_domain": "",
  "output_language": "",
  "user_goal": ""
}
```

如果用户没有指定 Skill 名称，则根据视频主题自动生成。

示例：

视频主题：

```text
Vibecoding 遇到 Bug 怎么修？新手必看的 AI 改bug指南
```

自动生成 Skill 名称：

```text
vibecoding_bugfix_debug_skill
```

---

## Step 2：获取视频元信息

优先尝试获取：

* 标题
* 作者
* 发布时间
* 视频时长
* 视频简介
* 分 P 信息
* 标签
* 封面
* 字幕信息

推荐命令：

```bash
yt-dlp \
  --cookies-from-browser chrome \
  --write-info-json \
  --write-thumbnail \
  --skip-download \
  -o "video_to_skill_workspace/raw/%(id)s.%(ext)s" \
  "<VIDEO_URL>"
```

如果失败，记录错误到：

```text
output/debug_report.md
```

错误记录格式：

```markdown
## Video Metadata Fetch Failed

- URL:
- Command:
- Error:
- Possible reason:
- Suggested fallback:
```

---

## Step 3：下载视频或使用本地视频

优先使用 yt-dlp：

```bash
yt-dlp \
  --cookies-from-browser chrome \
  --write-info-json \
  --write-thumbnail \
  --write-subs \
  --write-auto-subs \
  --sub-lang "zh-Hans,zh-CN,zh,en" \
  -f "bv*+ba/best" \
  -o "video_to_skill_workspace/raw/video.%(ext)s" \
  "<VIDEO_URL>"
```

如果 Bilibili 下载失败，尝试：

```bash
yt-dlp \
  --cookies-from-browser chrome \
  -f "best" \
  -o "video_to_skill_workspace/raw/video.%(ext)s" \
  "<VIDEO_URL>"
```

如果仍然失败，则生成 fallback 指南：

```markdown
# fallback_manual_steps.md

视频无法自动下载。

请用户手动执行以下任一方式：

1. 使用浏览器下载视频
2. 使用 Bilibili 客户端缓存视频
3. 使用录屏工具录制视频
4. 将视频保存为：

video_to_skill_workspace/raw/video.mp4

然后重新运行本 Skill。
```

---

## Step 4：提取音频

使用 ffmpeg 从视频中提取 16kHz 单声道音频：

```bash
ffmpeg -y \
  -i video_to_skill_workspace/raw/video.mp4 \
  -vn \
  -ac 1 \
  -ar 16000 \
  video_to_skill_workspace/raw/audio.wav
```

如果视频格式不是 mp4，应自动识别实际文件：

```bash
find video_to_skill_workspace/raw -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \)
```

---

## Step 5：提取字幕

优先级：

```text
1. 视频自带字幕
2. 平台自动字幕
3. Whisper / WhisperX ASR 转写
4. 其他本地 ASR
```

如果存在 `.srt` 或 `.vtt` 文件，则先转换为纯文本：

```bash
python3 scripts/clean_subtitle.py \
  --input video_to_skill_workspace/raw/subtitle.srt \
  --output video_to_skill_workspace/transcript/transcript_raw.txt
```

如果没有字幕，使用 ASR。

推荐 WhisperX：

```bash
whisperx \
  video_to_skill_workspace/raw/audio.wav \
  --language zh \
  --output_dir video_to_skill_workspace/transcript \
  --output_format json srt txt
```

如果 WhisperX 不可用，尝试 Whisper：

```bash
whisper \
  video_to_skill_workspace/raw/audio.wav \
  --language Chinese \
  --output_dir video_to_skill_workspace/transcript
```

---

## Step 6：清洗转写文本

清洗内容包括：

* 去除重复字幕
* 修复明显错别字
* 合并断句
* 保留时间戳
* 保留专业术语
* 保留代码名、工具名、模型名
* 不得改变作者原意

清洗后输出：

```text
transcript/transcript_clean.md
```

格式：

```markdown
# Transcript Clean

## 00:00 - 00:30

作者介绍本视频主题：Vibecoding 遇到 Bug 后如何让 AI 高效修复。

## 00:31 - 01:20

作者指出新手常见问题：让 AI 直接扫描整个项目，导致 token 消耗巨大，并且容易改坏无关代码。
```

---

## Step 7：抽取关键帧

### 7.1 固定间隔抽帧

默认每 5 秒抽一帧：

```bash
ffmpeg -y \
  -i video_to_skill_workspace/raw/video.mp4 \
  -vf "fps=1/5,scale=1280:-1" \
  video_to_skill_workspace/frames/frame_%05d.jpg
```

### 7.2 场景变化抽帧

如果支持 scene detection，则额外抽取画面变化明显的帧：

```bash
ffmpeg -y \
  -i video_to_skill_workspace/raw/video.mp4 \
  -vf "select='gt(scene,0.3)',scale=1280:-1" \
  -vsync vfr \
  video_to_skill_workspace/frames/scene_%05d.jpg
```

---

## Step 8：OCR识别画面文字

对每张关键帧执行 OCR。

重点识别：

* 代码
* 报错信息
* 文件路径
* 终端命令
* 网页标题
* AI 对话框内容
* PPT标题
* 列表项
* 表格
* UI按钮
* URL
* 模型名称
* 工具名称

输出格式：

```json
{
  "frame": "frame_00001.jpg",
  "time_estimate": "00:00:05",
  "ocr_text": "...",
  "contains_code": true,
  "contains_error": false,
  "contains_terminal": true,
  "contains_ai_chat": true
}
```

保存到：

```text
ocr/frame_00001.json
```

---

## Step 9：视觉模型分析关键帧

对每张关键帧生成结构化分析。

提示词模板：

```text
你正在分析一个技术教程视频的关键帧。

请根据图片内容输出结构化 JSON。

重点关注：
1. 画面中是否有代码？
2. 画面中是否有终端命令？
3. 画面中是否有报错信息？
4. 画面中是否有 AI 编程工具界面？
5. 画面中是否有网页、后台、编辑器或项目目录？
6. 画面中是否显示某种操作步骤？
7. 这张画面对理解视频方法论有什么帮助？

输出 JSON：

{
  "frame": "",
  "estimated_time": "",
  "scene_type": "",
  "visible_objects": [],
  "visible_text": "",
  "code_or_error": "",
  "operation": "",
  "teaching_point": "",
  "possible_skill_rule": "",
  "confidence": "high | medium | low"
}
```

输出到：

```text
notes/visual_notes.md
```

---

## Step 10：建立时间轴

把以下信息按时间合并：

* 字幕 / 转写文本
* OCR文字
* 关键帧描述
* 视频元信息
* 画面操作
* AI推断

输出：

```text
timeline/timeline.json
```

格式：

```json
[
  {
    "start": "00:00",
    "end": "00:30",
    "speech_summary": "",
    "visual_summary": "",
    "ocr_summary": "",
    "main_topic": "",
    "teaching_point": "",
    "candidate_skill_rule": "",
    "evidence": {
      "transcript": "",
      "frames": [],
      "ocr": []
    },
    "confidence": "high"
  }
]
```

---

## Step 11：提取方法论

从 timeline 中提取可复用原则。

必须分类：

```markdown
# Extracted Principles

## 1. 核心观点

## 2. 操作流程

## 3. 常见错误

## 4. 推荐做法

## 5. 禁止做法

## 6. 可转化为 Skill 的规则

## 7. 可转化为提示词的表达

## 8. 仍不确定的信息
```

每条原则必须带证据来源：

```markdown
### 原则 1：不要让 AI 一开始扫描整个项目

- 类型：视频明确提到 / AI推断
- 证据：00:35-01:20 的讲解 + 画面中出现项目目录
- 可转化规则：Debug 时先读取报错日志和相关文件，不允许全项目扫描
- 置信度：高
```

---

## Step 12：生成最终 Skill

最终 Skill 文件必须符合以下结构：

```markdown
# Skill: <skill_name>

## 1. Purpose

## 2. When to Use

## 3. Inputs

## 4. Outputs

## 5. Core Rules

## 6. Workflow

## 7. Forbidden Actions

## 8. Checklist

## 9. Prompt Templates

## 10. Verification

## 11. Failure Handling

## 12. Output Format
```

生成文件：

```text
output/08_generated_skill.md
```

---

## 13. 证据映射

生成：

```text
output/09_evidence_map.json
```

格式：

```json
{
  "skill_rule": "不要让 AI 一开始扫描整个项目",
  "source_type": "transcript + visual",
  "time_range": "00:35-01:20",
  "evidence_text": "",
  "frame_ids": ["frame_00007.jpg", "frame_00008.jpg"],
  "confidence": "high"
}
```

---

## 14. Debug Report

每次执行结束必须生成：

```text
output/10_debug_report.md
```

内容包括：

```markdown
# Debug Report

## Input

- Video URL:
- Local file:
- Target Skill:

## Environment

- yt-dlp:
- ffmpeg:
- ASR:
- OCR:
- Vision model:

## Steps Completed

- [ ] Metadata fetched
- [ ] Video downloaded
- [ ] Audio extracted
- [ ] Transcript generated
- [ ] Frames extracted
- [ ] OCR completed
- [ ] Visual notes completed
- [ ] Timeline generated
- [ ] Principles extracted
- [ ] Skill generated

## Errors

## Fallbacks Used

## Final Output

## Remaining Risks
```

---

## 15. 禁止行为

执行本 Skill 时禁止：

1. 禁止只根据标题生成 Skill。
2. 禁止没有字幕或转写就假装看完视频。
3. 禁止没有画面分析就声称理解了视频画面。
4. 禁止编造作者没有提到的方法。
5. 禁止把不确定内容写成确定结论。
6. 禁止把视频原文大段复制到最终 Skill。
7. 禁止输出侵犯版权的完整逐字稿。
8. 禁止绕过付费、登录或访问限制。
9. 禁止下载、传播、二次发布用户无权处理的视频内容。
10. 禁止一次性把长视频全部塞进大模型。
11. 禁止忽略报错。
12. 禁止失败后不生成 debug_report。

---

## 16. 合规要求

本 Skill 仅用于：

* 用户个人学习
* 技术研究
* 方法论提炼
* 内部工作流建设
* AI Agent Skill 生成

不得用于：

* 未授权转载视频
* 批量搬运内容
* 生成侵权课程
* 绕过平台付费限制
* 绕过登录权限
* 传播完整字幕或完整视频内容

最终输出应以“摘要、方法论、规则、流程、提示词”为主，避免复刻原视频内容。

---

## 17. 默认生成 Skill 的写作风格

最终生成的 Skill 应该：

* 清晰
* 可执行
* 面向 AI Agent
* 面向 Codex / OpenClaw
* 少废话
* 多步骤
* 多检查清单
* 多禁止项
* 多验证命令
* 适合直接放进 skills 目录

不要写成普通文章。

---

## 18. 生成 Skill 时的提示词模板

当完成 transcript、visual notes、timeline 后，使用以下提示词生成最终 Skill：

```text
你是一个 OpenClaw / Codex Skill 设计专家。

我已经从一个技术教程视频中提取了以下内容：

1. 视频元信息
2. 清洗后的字幕
3. 关键帧视觉分析
4. OCR结果
5. 时间轴 timeline
6. 提取出的方法论 principles
7. 证据映射 evidence map

请你基于这些材料生成一个可安装到 OpenClaw 的 Skill。

要求：

1. Skill 必须是 Markdown 格式。
2. Skill 名称为：<TARGET_SKILL_NAME>
3. Skill 面向对象：OpenClaw / Codex / AI Agent。
4. Skill 必须可执行，不要写成普通总结。
5. 必须包含：
   - Purpose
   - When to Use
   - Inputs
   - Outputs
   - Core Rules
   - Workflow
   - Forbidden Actions
   - Checklist
   - Prompt Templates
   - Verification
   - Failure Handling
   - Output Format
6. 每条关键规则必须能追溯到视频证据。
7. 视频明确讲到的内容，标注为【视频明确提到】。
8. 由画面推断出的内容，标注为【画面推断】。
9. AI补充的工程化建议，标注为【AI工程化补充】。
10. 不要编造视频中没有的信息。
11. 不要输出完整视频逐字稿。
12. 最终 Skill 使用中文。
```

---

## 19. 针对“Vibecoding 修 Bug 视频”的默认 Skill 生成方向

如果视频主题与 Vibecoding、AI 编程、修 Bug、Debug 有关，则最终 Skill 应重点提取以下方向：

```text
AI 修 Bug 的正确流程
如何减少 token 消耗
如何避免 AI 扫描整个项目
如何让 AI 先读日志
如何让 AI 做最小修改
如何让 AI 验证修复结果
如何形成 Debug Report
如何沉淀经验
```

生成的目标 Skill 可以命名为：

```text
vibecoding_bugfix_debug_skill
```

---

## 20. 针对 Debug 类视频的 Skill 模板

如果最终要生成的是 Debug Skill，则结构建议如下：

```markdown
# Skill: vibecoding_bugfix_debug_skill

## Purpose

指导 AI Agent 在 Vibecoding 项目中高效修复 Bug，减少 token 浪费，避免无目标扫描整个项目。

## When to Use

- 网站报错
- 构建失败
- 页面空白
- API失败
- 登录失败
- 后台配置无法影响前端
- 用户反馈某功能异常
- AI 修改代码后引入新 Bug

## Core Rules

1. 先看错误日志，不要先扫全项目。
2. 先看最近修改，不要重构系统。
3. 先提出假设，再读取文件。
4. 只读取最小相关文件集合。
5. 每次只修一个问题。
6. 修改前说明将修改哪些文件。
7. 修改后必须运行验证命令。
8. 失败后生成 Debug Report。

## Workflow

### Step 1: Collect Evidence

读取：

- 报错日志
- build log
- browser console
- network error
- git diff
- package.json

### Step 2: Classify Bug

判断属于：

- frontend
- backend
- database
- auth
- API
- config
- dependency
- deployment

### Step 3: Select Minimal Files

只读取与 bug 直接相关的文件。

### Step 4: Create Hypothesis

输出：

{
  "bug": "",
  "likely_cause": "",
  "files_to_read": [],
  "files_to_modify": [],
  "verification": ""
}

### Step 5: Patch

只做最小修复。

### Step 6: Verify

运行：

npm run build
npm run lint
npm test

### Step 7: Report

输出 Debug Report。
```

---

## 21. 安装后测试提示词

安装本 Skill 后，可以用以下提示词测试：

```text
请调用 video_to_skill_extractor skill，分析这个视频并生成一个 OpenClaw/Codex 可用的 debug skill：

视频地址：
https://www.bilibili.com/video/BV1p8DeBtEbH/

视频主题：
Vibecoding 遇到 Bug 怎么修？新手必看的 AI 改bug指南

目标：
把视频中的方法论提炼成一个用于 AI 编程项目修 Bug 的 skill，重点解决：
1. AI 修 Bug 时 token 消耗过大
2. AI 盲目扫描整个项目
3. AI 修改无关代码
4. AI 不验证修复结果
5. AI 无法沉淀 debug 经验

请输出：
1. 视频内容摘要
2. 时间轴
3. 方法论提取
4. 最终 Skill：vibecoding_bugfix_debug_skill.md
5. debug_report.md
```

---

## 22. 失败处理策略

如果视频无法下载：

```text
不要终止任务。
生成 fallback_manual_steps.md。
要求用户手动放入 video.mp4 后继续。
```

如果没有字幕：

```text
使用 ASR。
```

如果 ASR 失败：

```text
只基于画面 OCR 和用户提供的视频主题生成低置信度分析，并明确标注“不完整”。
```

如果画面分析失败：

```text
只基于字幕生成 Skill，并明确标注“未完成画面分析”。
```

如果字幕和画面都无法获取：

```text
不得生成最终 Skill。
只能输出失败报告。
```

---

## 23. 最终响应格式

执行完成后，回复用户：

```markdown
已完成 video_to_skill_extractor 处理。

生成文件：

1. output/03_transcript_clean.md
2. output/04_visual_notes.md
3. output/06_timeline.json
4. output/07_extracted_principles.md
5. output/08_generated_skill.md
6. output/09_evidence_map.json
7. output/10_debug_report.md

最终 Skill：

output/08_generated_skill.md

注意：
以下部分为视频明确提到：
- ...

以下部分为画面推断：
- ...

以下部分为 AI 工程化补充：
- ...
```

---

## 24. Skill 自检清单

在结束前，必须检查：

```text
[ ] 是否获取了视频标题？
[ ] 是否获取了视频时长？
[ ] 是否提取了字幕或 ASR？
[ ] 是否清洗了文案？
[ ] 是否抽取了关键帧？
[ ] 是否做了 OCR？
[ ] 是否生成了视觉分析？
[ ] 是否建立了时间轴？
[ ] 是否提取了方法论？
[ ] 是否区分了明确内容与推断内容？
[ ] 是否生成了最终 Skill？
[ ] 是否生成了 debug_report？
[ ] 是否避免大段复制原视频内容？
[ ] 是否标记了不确定信息？
```

---

## 25. 推荐依赖

本 Skill 可以调用以下工具，但不强制全部存在：

```text
yt-dlp
ffmpeg
python3
whisper
whisperx
pytesseract
opencv-python
Pillow
Playwright
本地或远程视觉大模型
本地或远程文本大模型
```

---

## 26. install.sh 推荐内容

如果需要自动安装依赖，可生成：

```bash
#!/usr/bin/env bash
set -e

echo "Installing video_to_skill_extractor dependencies..."

if command -v brew >/dev/null 2>&1; then
  brew install yt-dlp ffmpeg tesseract
fi

python3 -m pip install --upgrade yt-dlp openai-whisper pillow opencv-python pytesseract playwright

python3 -m playwright install chromium

echo "Done."
```

注意：

```text
在受 PEP 668 限制的 Python 环境中，不要强行全局 pip install。
应使用 venv。
```

推荐 venv 安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install yt-dlp openai-whisper pillow opencv-python pytesseract playwright
python -m playwright install chromium
```

---

## 27. 本 Skill 的一句话总结

把技术视频变成 AI Agent 能执行、能复用、能沉淀的工作流 Skill，而不是只做普通视频摘要。

````

---

安装完成后，你可以直接对 OpenClaw 说：

```text
请调用 video_to_skill_extractor，分析这个 B 站视频：
https://www.bilibili.com/video/BV1p8DeBtEbH/

目标是生成一个用于 Codex / OpenClaw 修复网站 Bug 的 debug skill。
不要只总结视频，要提取可执行流程、禁止行为、提示词模板和验证步骤。
`