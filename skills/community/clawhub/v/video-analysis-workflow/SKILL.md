---
name: video-analysis-workflow
description: 视频案例分析助手（Video Analysis Workflow）：一键分析本地/在线视频，拆解并输出为视频案例。自动提取分镜、画面、旁白、结构，生成①案例分析 ②抽帧分镜 ③脚本模板 ④台词转写 四份报告，支持自动整理Obsidian案例库。适用于运营发行、竞品视频分析、视频编导、团队案例库沉淀。
metadata:
  short-description: 视频案例分析助手
  author: Orang3Moon
---

# 视频案例分析助手 🎬

> 把一个参考视频，变成一套可以反复调用的视频策划资产。

## 是什么

输入一个本地视频，或一个可下载的抖音/B站链接，自动完成：

```text
下载/读取视频
→ 抽帧看画面
→ Whisper 提取台词
→ 对齐画面与旁白
→ 拆解叙事框架
→ 提炼脚本模板
→ 生成复用 Prompt
→ 归档到视频案例库
```

最终输出一套标准化案例文档，方便策划、编导、运营、美术、AI Agent 后续反复调用。

它不是简单的“视频转文字”，而是把视频拆成：

```text
分镜怎么排
节奏怎么走
台词怎么写
框架怎么搭
亮点怎么复用
下次怎么改成自己的项目
```

## 核心卖点

- **全流程案例拆解**：一次性提取分镜、画面节奏、旁白台词、叙事结构、脚本句式。
- **本地视频/抖音/B站链接都能处理**：本地视频直接分析；抖音可配合专用下载 Skill，B站优先用 `yt-dlp` 下载后再分析。
- **自动生成案例报告**：输出适合 Obsidian 管理的 Markdown 笔记，方便搜索、归档、复用。
- **沉淀视频模板**：把参考片提炼成可改写的脚本骨架、镜头语言、节奏公式和 Prompt。
- **适合视频策划**：可以直接服务新皮肤、新角色、活动福利、世界观、品牌宣传等视频方案。
- **打造团队案例库**：按“一个视频 = 一个文件夹”的规范沉淀，越用越像内部视频灵感库。
- **支持扩展 HTML 交付**：默认输出 Markdown；如果用户需要，也可以额外生成 HTML 版案例报告，方便分享或演示。

## 适合谁用

- 游戏运营：拆活动、福利、版本宣发视频。
- 视频策划/编导：学习参考片结构，快速出新脚本。
- 市场/品牌：沉淀竞品视频案例和传播方法。
- 美术/动效：查看分镜、画面节奏、视觉关键词。
- AI 使用者：把案例变成后续可调用的 Prompt 和模板。

## 典型使用场景

- “这个游戏世界观视频为什么好看？”
- “拆一下这个新皮肤介绍视频的节奏。”
- “把这个福利活动视频变成我们后续能复用的模板。”
- “提取这条抖音的台词和分镜。”
- “帮我搭一个团队视频案例库。”
- “以后做视频策划时，能不能直接调用这些案例？”

## 触发词

`视频案例` `参考视频` `拆解视频` `抽帧分镜` `台词转写` `脚本模板` `视频策划` `视频案例库` `Obsidian案例库` `抖音链接分析` `B站链接分析` `无水印下载` `yt-dlp`

## 用户怎么说最方便

### 本地视频

```text
请用 video-analysis-workflow 分析这个视频：<本地视频路径>
保存到：<案例库路径>
案例名：某游戏-世界观介绍-260610
```

### 抖音 / B站链接

```text
请用 video-analysis-workflow 分析这个抖音/B站链接：<链接>
保存到：<案例库路径>
案例名：某游戏-皮肤介绍-260610
需要下载视频、台词转写、分镜和脚本模板。
```

如果环境中没有下载工具，先告诉用户：需要先安装或启用抖音下载能力；拿到本地视频后再进入本 Skill 的标准分析流程。

### 只给视频，不给案例名

如果用户没有提供案例名，自动按下面规则命名：

```text
项目名-视频类型-YYMMDD
```

无法判断项目名或视频类型时，先用简短问题确认，不要乱命名。

## 最小依赖

核心分析只需要：

1. **FFmpeg / FFprobe**：读取视频信息、抽帧、生成总览图。
2. **Python + openai-whisper**：本地提取旁白/字幕。
3. **Markdown / Obsidian**：保存案例报告与标签。

默认不依赖云 API，不强制依赖视频生成工具。

抖音/B站链接下载是可选前置能力；如果同事只有本地视频，不需要它。

## 新环境第一次使用

纯新电脑先跑安装脚本。

Codex：

```powershell
powershell -ExecutionPolicy Bypass -File <Skill目录>\scripts\setup-video-case-env.ps1
```

Claude：

```powershell
powershell -ExecutionPolicy Bypass -File <Skill目录>\scripts\setup-video-case-env.ps1
```

OpenClaw / Agents：

```powershell
powershell -ExecutionPolicy Bypass -File <Skill目录>\scripts\setup-video-case-env.ps1
```

脚本会准备：

- FFmpeg
- Python 3.13
- Whisper 本地环境：`%USERPROFILE%\.video-creator-toolkit\whisper-venv`
- Python 包：`openai-whisper`、`yt-dlp`


## 平台链接下载说明

### 抖音

抖音建议使用已有的 `douyin` 下载 Skill，先把无水印视频保存到案例文件夹，再进入抽帧、转写和分析流程。

### B站

B站优先使用 `yt-dlp`：

```powershell
$ytdlp="$env:USERPROFILE\.video-creator-toolkit\whisper-venv\Scripts\yt-dlp.exe"
& $ytdlp -o "<案例文件夹>\source.%(ext)s" "<B站视频链接>"
```

如果遇到需要登录、清晰度受限或会员内容：

- 先确认用户有合法观看权限。
- 需要浏览器 cookies 时，必须先获得用户明确授权。
- 下载后的本地视频再交给标准分析流程。

本 Skill 只用于分析和归档用户有权访问的视频内容。遵守平台规则和版权要求。
## 标准产物

默认输出 Markdown 案例库：

```text
<案例库根目录>/
  <案例名>/
    案例分析丨<案例名>.md
    抽帧分镜丨<案例名>.md
    台词转写丨<案例名>.md
    脚本模版丨<案例名>.md
    <原视频名>.json
    <原视频名>.srt
    <原视频名>.txt
    <原视频名>.vtt
    <原视频名>.tsv
    抽帧/
      contact-sheet.jpg
      contact-first60.jpg
      f-000.jpg
      f-002.jpg
      frame-075.jpg
```

可选输出：

```text
案例报告丨<案例名>.html
```

HTML 用于分享、演示或发给不使用 Obsidian 的同事。若用户没要求，默认不生成 HTML。

## 四份核心文档

### 1. 案例分析

回答：这个视频为什么成立？适合怎么复用？

包含：

- 一句话定位
- 快速调用关键词
- 视频基本信息
- 视觉风格
- 核心叙事框架
- 时间轴拆解
- 镜头语言拆解
- 文案策略
- 旁白结构拆解
- 适用/不适用场景
- 后续复用 Prompt

### 2. 抽帧分镜

回答：这个视频画面怎么排？节奏怎么走？

要求把图片直接贴进笔记：

```markdown
![抽帧总览](./抽帧/contact-sheet.jpg)
![前60秒细分](./抽帧/contact-first60.jpg)
![0秒关键帧](./抽帧/f-000.jpg)
```

必须包含“画面与旁白同步表”，把每段画面和台词对应起来。

### 3. 台词转写

回答：原片说了什么？文案怎么推进？

用表格整理：

```markdown
| 时间码 | 台词 | 结构功能 |
|---|---|---|
```

可以轻度校正 Whisper 错字，但要保留原始 `.json/.srt/.txt` 方便复查。

### 4. 脚本模版

回答：下次怎么照着这个结构写一个新视频？

包含：

- 模板用途
- 完整脚本骨架
- 原片旁白句式模板
- 视觉关键词
- 动效关键词
- 改写规则
- 后续生成 Prompt

## 标准流程

1. **确认输入**：本地视频路径或抖音链接、案例库位置、案例名。
2. **获取视频**：本地视频直接用；抖音链接先下载无水印视频。
3. **读取信息**：记录时长、分辨率、帧率、音频情况。
4. **抽帧分镜**：生成总览图、前段细分图和关键帧。
5. **转写台词**：用本地 Whisper 输出 `.json/.srt/.txt`。
6. **对齐分析**：把画面、旁白、节奏、剪辑结构放在一起看。
7. **生成文档**：输出案例分析、抽帧分镜、台词转写、脚本模版。
8. **沉淀模板**：提炼可复用 Prompt、句式和视频策划框架。

## Obsidian 标签规范

使用“双层属性”：

### 文首轻量标签

用于 Obsidian 标签检索：

```yaml
---
tags:
  - 视频案例/游戏世界观
  - 视频案例/悬疑纪录片
case_id: <案例名>
type: 视频案例分析
project: <项目名>
category: <视频类型>
---
```

### 文末完整属性

用于 AI 后续调用：

````markdown
## 笔记属性

```yaml
style:
  - 悬疑纪录片
structure:
  - 世界观填坑
visual_keywords:
  - 大字卡
motion_keywords:
  - 黑场停顿
script_keywords:
  - 玩家代入
source_video: <原视频路径>
local_frames: ./抽帧
source_transcript_json: ./<原视频名>.json
```
````

## 分析标准

不要只凭画面猜结构。完整分析必须结合：

```text
画面节奏
+ 抽帧时间轴
+ 旁白/字幕
+ 剪辑结构
+ 文案句式
= 完整视频案例分析
```

每个主要段落都要说明：

- 画面功能
- 旁白功能
- 观众感受
- 可复用结构
- 不适合套用的场景

## 第二案例验证后的关键规则

### 抖音下载器优先级

抖音链接不要只依赖一个下载器。推荐顺序：

1. **douyin-video-fetch**：优先用于抖音视频下载。实测短链可能失败，但 video_id 下载更稳。
2. **yt-dlp**：作为兜底下载器。实测可识别抖音短链并解析 video_id，但常提示需要 fresh cookies。
3. **旧 douyin Skill**：当前依赖 `nodriver-kit`，若 PyPI/GitHub 来源不可用，不作为默认方案。
4. 如果下载器都失败，请用户提供本地视频，继续走分析链路。

### 抖音短链 fallback

当输入是 `v.douyin.com` 短链时：

1. 先尝试下载器直接处理短链。
2. 如果失败，观察日志或用兜底解析工具拿到真实视频页，例如 `https://www.douyin.com/video/<video_id>`。
3. 提取 `video_id` 后，再调用 `douyin-video-fetch`。

~~~powershell
python <douyin-video-fetch>/scripts/fetch_video.py <video_id> --output-dir <案例文件夹>
~~~

实测案例：短链 `https://v.douyin.com/-kQU2CX_TAk/` 直接失败，但 `7637051403474586943` 下载成功。

### yt-dlp fallback 规则

如果 `yt-dlp` 报：

~~~text
Fresh cookies (not necessarily logged in) are needed
~~~

说明它已识别视频，但需要浏览器 cookies。读取 cookies 属于敏感操作，必须先询问用户是否授权。未获授权时，不要读取 cookies。

### douyin-video-fetch 依赖

`douyin-video-fetch` 使用 Playwright + aiohttp。新环境如缺依赖，需要安装：

~~~powershell
python -m pip install -U playwright aiohttp
python -m playwright install chromium
~~~

如果 OpenClaw 安装器在 Windows 上出现 `EPERM rename`，但用户已手动安装成功，可以直接读取 `%USERPROFILE%\.openclaw\workspace\skills\douyin-video-fetch`。

### 无旁白/低转写视频处理

如果 Whisper 只识别到片尾署名、BGM、空文本，说明视频可能是“画面字卡主导型”。此时不要硬编旁白，应改用视频画面大字卡、发布标题/分享文案、道具/奖励素材文字、抽帧中的可见信息。

在 `台词转写` 中明确说明：Whisper 未识别到有效旁白，本案例以画面字卡和发布文案作为文案结构来源。

### 中文路径与写入方式

Windows 中文路径下，避免使用 PowerShell heredoc 管道给 Python 写入 Markdown，例如 `@'...'@ | python -`，该方式可能导致中文路径变成问号。

写 Markdown 时优先使用：

~~~powershell
[System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
~~~

或使用 Node.js：

~~~js
await fs.writeFile(path, content, "utf8")
~~~

涉及中文文件夹、中文文件名、Obsidian 笔记时，必须使用稳定 UTF-8 写入方式。

## 交付前检查

- 案例文件夹是否完整？
- 原视频路径是否记录？
- 是否完成抽帧分镜？
- 是否完成 Whisper 台词转写？
- 是否有画面与旁白同步表？
- 是否生成脚本模板和 Prompt？
- 文首 YAML 是否能被 Obsidian 识别？
- Whisper 原始输出是否保留？
- 如果用户要求 HTML，是否额外生成 HTML 报告？

## 常见错误

- 只看画面，不转写旁白。
- 只输出台词，不分析文案结构。
- 只做案例报告，不沉淀脚本模板。
- 把标签只放文末，导致 Obsidian 不识别。
- 强行套模板，比如把世界观视频结构硬套到福利活动视频。
- 忘记保留 Whisper 原始文件，后续无法复查。

## 最短调用语

```text
请用 video-analysis-workflow 分析这个视频：<视频路径或抖音/B站链接>
保存到：<案例库路径>
案例名：<项目名-视频类型-日期>
输出：案例分析、抽帧分镜、台词转写、脚本模版；如方便，也生成 HTML 案例报告。
```

---

*Built for video planners, game marketers, and AI-assisted creative teams.*