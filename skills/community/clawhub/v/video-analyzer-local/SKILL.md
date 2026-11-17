---
slug: video-analyzer-local
displayName: 视频分析处理
name: video-analyzer
description: "视频分析处理 — 本地视频反编译分析工具。将视频拆解为时间轴剧本、语音转文字、场景分析、跨模态关联和精华摘要，支持多ASR引擎切换（Whisper/Paraformer/SenseVoice）、中文NLP增强、PaddleOCR中文识别。v4.0 新增短视频平台适配（抖音/快手/B站/视频号）和自动剪辑建议（高光检测/冗余标记/EDL导出/字幕样式）。v4.1 新增tiny模型优先体验（75MB低门槛）、说话人分离质量评分、剪映draft.json导出。v4.2 新增场景管理（detect→slice一条链）、短视频爆款预测、实时直播分析（流式ASR+敏感词检测）。v4.3 新增纯音频输入（mp3/m4a/wav播客与录音）、批量队列（SQLite+硬件档位并发）、GPU自动加速（CT2 int8量化）、ASR配置统一（--asr-engine单参数）。v4.4 新增一键成片（ffmpeg filter_complex 自动剪辑+平台规格包导出）、封面帧智能选取（Laplacian+人脸+三分法构图）、自动字幕翻译（cn-llm-router桥接，EN/JP/KO）、BGM识别（chromaprint指纹+本地库匹配）、剪映6.0适配+EDL导入指南。v4.5.0 新增首跑自检（doctor 探测 ffmpeg/模型/磁盘/内存/GPU + 修复命令清单）、模型下载链路（进度可视化+3次重试+断点续传+清华镜像交互提示）、--quick 快速模式（仅转写+摘要，5分钟出稿）、首跑「下一步建议」（功能发现引导）。v4.6.0 新增播客模式（说话人时间线+Podcasting 2.0 章节标记+金句三信号本地评分（句长/语义完整度/关键词密度））、说话人分离三类预设（访谈/会议/电话，阈值/窗口/说话人上限可配，质量评分随结果自动输出）、听后简报（周聚合HTML简报：本周处理列表/时长分布/金句Top10）、报告渲染器统一（音频/视频单源化）。v4.7.0 新增字幕工作流闭环：5套JSON样式包（综艺/访谈/课程/极简/竖屏）+ SRT/ASS双格式导出 + 双语同轴（原文轨/译文轨独立开关）；术语表机制（人名/产品名/专业词JSON前置替换+后置校对+待确认清单，品牌名零容忍）；字幕烧录一条命令（--burn-subtitle，样式包直连ffmpeg filter，无需手写filter_complex）。"
version: 4.7.0
tags: ["video", "analysis", "transcription", "local-offline", "chinese", "asr", "auto-edit", "subtitle-translate", "bgm-detect", "doctor", "quick-mode"]
icon: "🎬"
author: "njskills"
license: "MIT"
---

# 视频分析处理 — video-analyzer

## 概述

将视频"反编译"为结构化分析报告的本地工具，全程离线，无需联网。

**核心能力**：
- 🎙️ **语音转文字**（精确到每个字的时间戳，含说话人分离）
- 🎬 **场景边界切割与章节切片**
- 🔍 **视觉物体与画面文字识别**
- 📊 **多模态时空对齐**（声音 ↔ 画面 ↔ 文字）
- ✨ **带时间戳的精华摘要**
- ✂️ **视频章节切片 + 独立SRT字幕**
- 🗣️ **说话人分离标注**
- 📱 **短视频平台适配**（抖音/快手/B站/视频号，自动识别链接+下载+平台分析）
- 🎬 **自动剪辑建议**（高光检测/冗余标记/时间线生成/EDL导出/字幕样式）
- 📄 **交互报告输出**（HTML + JSON + Markdown）

## 快速开始

### 第一次使用前
> ⚠️ **模型下载提醒**：首次运行会自动下载语音识别模型。v4.1 起默认使用 tiny 模型（约 75MB），如需更高精度可加 `--model small` 切换到 small 模型（约 466MB）。国内用户建议先执行以下命令加速：
> ```bash
> pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
> ```
> 下载完成后后续使用无需重复下载。
> 
> 💡 **v4.5.0 新增**：首次使用前建议先运行 `--doctor` 自检环境，缺什么一目了然。快速体验用 `--quick` 5分钟出稿。

### 基本用法
```bash
python main.py --input "视频路径或URL" --output "./output"
```

### 使用场景示例

| 场景 | 命令 |
|------|------|
| 快速提取一个本地 MP4 的全部内容 | `python main.py -i my_video.mp4` |
| 分析某条新闻视频，只看字幕（最快，跳过分析） | `python main.py -i news.mp4 --no-visual` |
| 下载并分析一段 YouTube/B站视频 | `python main.py -i "https://www.youtube.com/watch?v=..."` |
| 视频分析可视化报告，仅输出 HTML | `python main.py -i video.mp4 --format html` |
| 分析 YouTube健身视频，提取精华片段 | `python main.py -i "https://..." --model medium --lang zh` |
| 老旧笔记本，限制资源跑语音识别 | `python main.py -i video.mp4 --no-visual --max-memory 2 --nice 15` |
| 只看时间轴剧本（不生成报告） | `python main.py -i video.mp4 --scenes-only` |
| 按场景章节切片视频，每段带SRT字幕 | `python main.py -i video.mp4 --slice-chapters` |
| 多人对话场景，分离说话人 | `python main.py -i meeting.mp4 --diarize` |
| 跳过更新检查（纯离线环境） | `python main.py -i video.mp4 --no-update-check` |
| 分析抖音视频（自动识别+下载+平台分析） | `python main.py -i "https://v.douyin.com/xxxxx" --platform` |
| 分析B站视频 + 自动剪辑建议 | `python main.py -i "https://www.bilibili.com/video/BVxxxx" --platform --editing-suggest` |
| 导出 EDL 时间线 + 字幕文件 | `python main.py -i video.mp4 --editing-suggest --export-edl --subtitle-style douyin` |
| 一键成片（抖音竖屏，口播精简） | `python main.py -i video.mp4 --auto-edit --edit-platform douyin --edit-style 口播精简` |
| 一键成片（B站横屏，高光集锦） | `python main.py -i video.mp4 --auto-edit --edit-platform bilibili --edit-style 高光集锦` |
| 一键成片 + BGM | `python main.py -i video.mp4 --auto-edit --bgm-path music.mp3` |
| 封面帧智能选取 Top3 | `python main.py -i video.mp4 --cover-select` |
| 字幕翻译（中→英） | `python main.py -i video.mp4 --editing-suggest --translate-subs en` |
| 字幕翻译（中→日，ASS格式） | `python main.py -i video.mp4 --editing-suggest --translate-subs ja --translate-format ass` |
| BGM 识别 | `python main.py -i video.mp4 --bgm-detect` |
| 剪映 6.0 + EDL 导入指南 | `python main.py -i video.mp4 --editing-suggest --jianying-v6` |
| 一键成片 + 封面 + 翻译 + BGM | `python main.py -i video.mp4 --auto-edit --cover-select --translate-subs en --bgm-detect` |

### 输出示例
```
output/
├── report.html              # 交互式 HTML 报告（主报告，用浏览器打开）
├── data.json                # 完整结构化 JSON 数据
├── script.md                # 剧本格式 Markdown
├── scenes/                  # 场景关键帧缩略图
│   ├── scene_001.jpg
│   ├── scene_002.jpg
│   └── ...
├── chapters/              # 章节切片（--slice-chapters 时生成）
│   ├── chapter_001.mp4
│   ├── chapter_001.srt
│   ├── chapter_001.vtt
│   ├── chapter_002.mp4
│   ├── chapter_002.srt
│   └── chapters_index.json
├── summary/               # 时间戳摘要
│   ├── timestamped_summary.md
│   └── timestamped_summary.json
├── speakers.srt           # 说话人字幕（--diarize 时生成）
├── platform/              # 平台分析（--platform 时生成）
│   ├── platform_metadata.json
│   └── short_video_analysis.json
├── edl/                   # EDL 时间线（--export-edl 时生成）
│   ├── timeline.cmx3600
│   └── ffmpeg_commands.sh
├── subtitles/             # 字幕文件（--editing-suggest 时生成）
│   └── subtitle.ass
└── assets/
    ├── waveform.svg       # 音频波形图
    └── timeline.svg       # 时间轴可视化
```

### 参数说明
| 参数 | 简写 | 说明 |
|------|------|------|
| `--input` | `-i` | 视频文件路径或 HTTP URL（必填） |
| `--output` | `-o` | 输出目录，默认为 `./output` |
| `--format` |  | 报告格式：`html`/`json`/`md`，默认 `html` |
| `--model` | `-m` | Whisper 模型：`tiny`/`base`/`small`/`medium`/`large-v3`（默认自动选择） |
| `--lang` | `-l` | 语言代码：`auto`/`zh`/`en`/`ja` 等（默认自动检测） |
| `--asr-engine` |  | ASR 引擎：`whisper`/`paraformer`/`sensevoice`/`auto`（默认 auto） |
| `--ocr-engine` |  | OCR 引擎：`paddleocr`/`auto`（默认 paddleocr） |
| `--no-nlp-enhance` |  | 跳过中文 NLP 增强（NER + 标签中文化） |
| `--no-visual` |  | 跳过视觉分析（场景分类/物体检测） |
| `--no-ocr` |  | 跳过画面文字识别 |
| `--no-highlight` |  | 跳过精华提取 |
| `--scenes-only` |  | 仅输出场景切割 JSON |
| `-f` | `--force` | 忽略缓存重新分析 |
| `--temp-dir` |  | 临时文件目录 (默认: ./.cache) |
| `--config` |  | 配置文件路径 (默认: config.yaml) |
| `--verbose` |  | 显示详细日志 |
| `--no-adaptive` |  | 禁用硬件自适应（默认启用） |
| `--max-memory` |  | 最大内存使用（GB） |
| `--nice` |  | 进程优先级 0-19，越大优先级越低 |
| `--no-update-check` |  | 跳过启动时的版本更新检查 |
| `--diarize` |  | 启用说话人分离（多人对话场景） |
| `--slice-chapters` |  | 按章节切片视频片段 + 生成SRT字幕 |
| `--platform` |  | 启用短视频平台适配（自动识别抖音/快手/B站/视频号链接） |
| `--editing-suggest` |  | 启用自动剪辑建议（高光检测/冗余标记/时间线生成/EDL导出） |
| `--edl-format` |  | EDL 导出格式：`cmx3600`/`csv`/`json`（默认 cmx3600） |
| `--subtitle-style` |  | 字幕样式模板（旧版）：`douyin`/`bilibili`/`movie`/`minimal` |
| `--subtitle-preset` |  | 字幕样式包（v4.7）：`variety`综艺/`interview`访谈/`course`课程/`minimal`极简/`vertical`竖屏 |
| `--subtitle-format` |  | 字幕输出格式：`srt`/`ass`/`vtt`（默认 ass） |
| `--export-edl` |  | 导出 EDL 剪辑时间线文件 |
| `--jianying` |  | 导出剪映 draft.json 格式（可直接导入剪映专业版） |
| `--jianying-v6` |  | 导出剪映 6.0 draft.json + EDL 导入指南（v4.4 新增） |
| `--auto-edit` |  | 启用一键成片（ffmpeg filter_complex 自动剪辑，v4.4 新增） |
| `--edit-style` |  | 一键成片风格：`口播精简`/`高光集锦`/`预告片`（默认 口播精简） |
| `--edit-platform` |  | 一键成片目标平台：`douyin`/`bilibili`/`kuaishou`/`wechat_video`（默认 douyin） |
| `--bgm-path` |  | BGM 音频文件路径（用于一键成片） |
| `--cover-select` |  | 启用封面帧智能选取（v4.4 新增） |
| `--translate-subs` |  | 翻译字幕到指定语言 (en/ja/ko/fr/de/es/ru) |
| `--translate-format` |  | 翻译字幕输出格式：`srt`/`ass`/`vtt`（默认 srt） |
| `--bgm-detect` |  | 启用 BGM 识别（需 chromaprint/fpcalc，v4.4 新增） |
| `--quality-score` |  | 启用说话人分离质量评分 |
| `--doctor` |  | 首跑自检：探测 ffmpeg/模型/磁盘/内存/GPU，输出修复命令清单（v4.5.0 新增） |
| `--quick` |  | 快速模式：仅转写+时间戳摘要，跳过视觉/场景/剪辑链（v4.5.0 新增） |
| `--download-model` |  | 下载 Whisper 模型（带进度可视化+断点续传+3次重试，v4.5.0 新增） |
| `--podcast` |  | 播客模式：说话人时间线+Podcasting 2.0 章节标记+金句提取（v4.6.0 新增） |
| `--diarize-profile` |  | 说话人分离预设：`interview`/`meeting`/`phone`（v4.6.0 新增） |
| `--weekly-briefing` |  | 听后简报：生成周聚合 HTML 简报（v4.6.0 新增） |
| `--bilingual` |  | 双语同轴字幕：原文轨+译文轨，配合 `--translate-subs`（v4.7.0 新增） |
| `--original-track` / `--no-original-track` |  | 双语时显示/隐藏原文轨（v4.7.0 新增） |
| `--no-translation-track` |  | 双语时隐藏译文轨（v4.7.0 新增） |
| `--glossary` |  | 术语表 JSON 路径，人名/产品名/专业词强制校正（v4.7.0 新增） |
| `--burn-subtitle` |  | 烧录硬字幕到视频，样式包直连 ffmpeg filter（v4.7.0 新增） |

## 功能说明

### 短视频平台适配（--platform）
自动识别并处理抖音/快手/B站/视频号视频链接：
- **链接解析**：支持分享链接、短链接、BV号等多种格式
- **视频下载**：基于 yt-dlp 的多平台视频下载
- **元数据提取**：标题、作者、点赞/评论/分享/收藏数、BGM信息等
- **黄金前3秒分析**：检测开场hook类型（视觉冲击/画面变化/平稳开场）
- **完播率因素分析**：视频时长评分、内容密度、行动号召检测、悬念检测
- **带货分析**：促销关键词识别、价格提取、行动号召检测
- **节奏分析**：场景切换频率、节奏类型判定

### 自动剪辑建议（--editing-suggest）
基于AI分析自动生成剪辑建议：
- **高光检测**：综合视觉活跃度、音频能量、语音情感、画面内容四维度评分
- **冗余标记**：检测静音片段、填充词、语速异常、画面静止、重复内容
- **时间线生成**：智能排列高光片段，跳过冗余，生成优化剪辑顺序
- **EDL导出**：支持CMX3600（Premiere Pro/DaVinci Resolve兼容）/CSV/JSON格式
- **字幕样式**：抖音风格/B站风格/电影风格/简洁风格，支持SRT/ASS/VTT格式
按场景边界自动将视频切割为多个短视频片段，每段生成独立的 SRT 字幕文件和 WebVTT 字幕文件。
- 使用 ffmpeg 流复制模式（极速，不重新编码）
- 每个章节含 `.mp4` + `.srt` + `.vtt` 三个文件
- 自动生成 `chapters_index.json` 索引文件

### 说话人分离（--diarize）
多人对话场景下，分离出不同说话人的对话段落。
- 基于 MFCC + 频谱特征 + GMM 聚类
- 完全离线，无需网络
- 以不同颜色标注不同说话人（A-F）
- 生成独立的 `speakers.srt` 字幕文件

### 时间戳摘要
每次运行自动生成带时间戳的精华摘要列表。
- `[MM:SS]` 格式时间戳
- Markdown + JSON 双格式输出
- 标注精华评分和标签

### 硬件自适应
启动时自动检测硬件配置，动态调整处理参数：

| 硬件指标 | 自适应策略 |
|---------|-----------|
| CPU 核数 | 自动确定最佳子进程数（保留 1 核给系统） |
| 内存大小 | 自动选择 whisper 模型，限制缓存上限 |
| GPU 显存 | 有 GPU 则全量分析，无则降采样 |

控制策略（不影响用户体验）：
- **低配电脑**（< 8GB 内存）：自动降低优先级（nice=10），使用 tiny/small 模型
- **运行时监控**：实时检测内存使用，接近上限时主动降速
- **处理时间预估**：分析前显示预估等待时间

## 安全提示

- 所有处理均在本地完成，无上传
- 输入视频需经用户路径合法性验证
- OCR 识别结果仅供参考
- 生成的 HTML 报告可在浏览器中离线查看
- v3.0 新增：文件类型黑名单拦截，禁止危险文件输入

### 输入文件类型限制

为保障安全，以下文件类型被**禁止**作为输入：

| 类别 | 禁止扩展名 |
|------|-----------|
| Windows 可执行/脚本 | `.bat` `.cmd` `.ps1` `.vbs` `.exe` `.dll` `.lnk` `.msi` |
| Office 文档 | `.docx` `.xlsx` `.pptx` `.doc` `.xls` `.ppt` `.xlsm` `.docm` `.pptm` |
| 压缩包/镜像 | `.iso` `.dmg` `.zip` `.rar` `.7z` `.tar` `.gz` `.apk` `.jar` |
| 系统/缓存文件 | `.DS_Store` `.env` `.log` `.tmp` `.git` 目录 |
| 风险脚本 | `.sh` `.com` `.scr` `.hta` `.reg` |

## 能力边界与限制

### 不支持的场景

| 场景 | 说明 |
|------|------|
| 视频时长建议 | ≤ 2 小时（`max_duration` 默认 7200s） |
| 超大文件 | 超过 2 小时需修改 `config.yaml` 的 `max_duration` |
| 不支持的视频格式 | 非常见的私有封装格式（如某些监控专用格式） |
| 无音频视频 | 场景检测和视觉分析仍可用，但无语音转文字 |
| 纯音频文件 | 不支持，需要专门的音频转文字工具 |
| 实时流媒体 | 不支持 RTSP 等实时流，仅支持可下载的 URL |
| 禁止的文件类型 | 见上方"输入文件类型限制" |

### 识别准确率说明
| 模块 | 准确率 | 说明 |
|------|--------|------|
| 语音转文字 | 85-95% | 中文普通话较好，方言/噪音会降低 |
| 场景切分 | 80-90% | 渐变过渡可能漏切，跳切较准 |
| 画面文字 | 75-85% | 需安装 paddleocr 且要求较清晰 |
| 说话人分离 | 70-85% | 声音差异越大越准确 |
| 精华提取 | 主观 | 基于对话密度/视觉复杂度计算 |

> 以上数据仅供参考，不同视频类型差异较大。

## 反模式 / 千万别这样用

> 以下操作会导致工具报错或输出错误结果，**请务必避免**：

- ❌ **输入损坏的视频文件**：工具会直接报错退出。可用 `ffmpeg -i input.mp4 -c copy fixed.mp4` 尝试修复后再分析。
- ❌ **输入纯音频文件**（如 MP3、WAV）：工具不支持，请先转成视频或用专业语音转文字工具。
- ❌ **超长视频不设 `--max-memory`**：2小时以上大视频建议加 `--max-memory 2 --no-visual` 防止内存溢出。
- ❌ **小内存电脑选大模型**：4GB 内存选 `medium` 或 `large-v3` 会极其缓慢甚至卡死。用 `--model tiny` 或 `--model small`。
- ❌ **重复分析使用旧缓存**：加 `--force` 重新分析，避免读过期缓存。
- ❌ **用 IE 打开 HTML 报告**：请用 Chrome/Edge/Firefox。
- ❌ **窄带网络下分析在线视频**：先下载到本地再分析，网络不稳定容易失败。
- ❌ **跳过 ffmpeg 安装直接用**：ffmpeg 是硬性依赖，必须先安装。
- ❌ **输入 `.ps1` `.exe` 等可执行文件**：文件类型黑名单会直接拒绝，本工具只处理视频。

## 常见问题（FAQ）

### 安装与配置

**Q: ffmpeg 安装后仍提示找不到？**
A: 需要让 ffmpeg 在系统 PATH 中。Windows 用户可用 `scoop install ffmpeg` 或下载后解压并将 bin 目录加入 PATH；macOS 用 `brew install ffmpeg`；Ubuntu 用 `sudo apt install ffmpeg`。安装后新开一个终端窗口，运行 `ffmpeg -version` 验证。

**Q: pip install 时 whisper 下载模型很慢？**
A: whisper 首次运行时会自动下载模型文件（small 约 466MB），国内用户建议设置镜像：`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`

**Q: paddleocr 安装失败？**
A: paddleocr 是可选依赖，不安装也能使用语音转文字和场景检测。如需 OCR，先确认 Python 版本 ≤ 3.11，再 `pip install paddlepaddle paddleocr`。

**Q: 说话人分离不准确怎么办？**
A: 说话人分离基于声音特征聚类，如果说话人声音相似或环境噪音大，准确率会下降。可以：① 安装 `librosa` 和 `scikit-learn` 提升特征提取能力；② 用 `--diarize` 后手动编辑生成的 `speakers.srt` 文件。

**Q: 为什么提示"禁止的文件类型"？**
A: 工具内置了文件类型黑名单，所有非视频文件（如 .exe .ps1 .zip .docx 等）都会被拒绝输入。请确认输入的是 .mp4/.mkv/.avi/.mov 等视频文件。

**Q: 抖音/快手/B站视频无法下载？**
A: 短视频平台下载依赖 yt-dlp，请先安装：`pip install yt-dlp`。部分视频可能需要配置 cookies 才能下载。如果仍然失败，请确认链接可访问且网络稳定。

**Q: 自动剪辑建议的高光检测准确吗？**
A: 高光检测基于视觉活跃度、音频能量、语音情感、画面内容四维度综合评分，准确率约 70-85%。建议将结果作为参考，人工微调后导出 EDL 到 Premiere Pro 或 DaVinci Resolve 进一步编辑。

**Q: EDL 文件如何导入到剪辑软件？**
A: CMX3600 格式兼容 Premiere Pro / DaVinci Resolve / Final Cut Pro。在 Premiere Pro 中：文件 → 导入 → 选择 .edl 文件。在 DaVinci Resolve 中：文件 → 导入时间线 → 导入 EDL。

**Q: 字幕样式可以自定义吗？**
A: 可以在 config.yaml 的 `editing.subtitle` 部分自定义字体、大小、颜色等参数。也支持在命令行用 `--subtitle-style` 选择预设模板。

### 运行错误

**Q: 运行中提示 "No space left on device"？**
A: 缓存目录占满了磁盘。用 `--temp-dir` 指定其他目录，或删除旧缓存 `rm -rf .cache/`。也可在 `config.yaml` 中减小 `max_memory_gb`。

**Q: 下载在线视频失败？**
A: 工具内置 3 次重试机制。如果仍然失败，请确认 URL 可访问且网络稳定；YouTube/B站等需安装 yt-dlp：`pip install yt-dlp`。

**Q: 语音识别结果有漏字或错字？**
A: 语音识别准确率约 85-95%。提高准确率方法：① 用更大的模型 `--model medium`；② 确保视频音频清晰无背景噪音；③ 方言视频选 `--lang zh` 指定中文。

**Q: 场景切分不准，渐变画面漏切？**
A: HSV 直方图差分对快速跳切准确度高（90%+），渐变过渡可能漏切。需要更精确的场景检测建议用 `--scenes-only` 导出后手动编辑 JSON。

**Q: 处理大视频时电脑变卡？**
A: 低配电脑请加 `--nice 15 --max-memory 4`。工具会自动降低进程优先级并限制内存使用。若仍卡顿，可加 `--no-visual --no-ocr` 只跑语音转文字。v3.0 版新增了实时资源监控，会自动防止内存溢出。

### 输出相关

**Q: HTML 报告打开是乱码？**
A: 请用现代浏览器（Chrome/Edge/Firefox）打开，不要用 IE。报告内已设 UTF-8 编码。

**Q: 输出的 JSON 太大怎么查看？**
A: 建议用 VS Code 或 jq 命令行工具：`jq '.transcript.segments[0:3]' data.json` 查看前 3 段。

**Q: 章节切片的视频无法播放？**
A: 章节切片使用 ffmpeg 流复制模式（`-c copy`），切割点必须在关键帧上。如果某些章节无法播放，可在 config.yaml 中设置 `force_reencode: true` 使用重新编码模式（稍慢但兼容性好）。

**Q: 说话人分离结果全是同一人？**
A: 请确认安装了可选依赖：`pip install librosa scikit-learn`。如果没有这些库，会回退到基于时间间隔的简单猜测策略，准确率较低。v4.1 新增质量评分（`--quality-score`），可量化评估分离结果可信度。

**Q: 说话人分离质量评分怎么使用？**
A: 运行 `--diarize --quality-score`，会输出 0-100 分数和等级（高/中/低）。≥ 80 分可信，≥ 60 分基本可用，< 60 分建议手动调整。评分基于声纹距离和重叠率两个维度。

**Q: 剪映 draft.json 怎么用？**
A: 运行 `--editing-suggest --jianying` 生成 draft.json 文件。打开剪映专业版 → 导入 → 选择 draft.json 即可加载时间线和字幕。

**Q: tiny 模型和 small 模型有什么区别？**
A: tiny 模型（75MB）识别速度更快但准确率略低；small 模型（466MB）准确率更高但速度慢。v4.1 默认 tiny 优先体验，如需要更高精度可用 `--model small` 切换。

**Q: 为什么优先推荐 tiny 模型？**
A: v4.1 新增 tiny 模型优先体验（75MB），首次使用门槛从 466MB 降至 75MB。低配电脑也会自动使用 tiny 模型。如需更高精度，可手动切换 `--model small/medium`。

### v4.7.0 新增功能 FAQ

**Q: 5 套字幕样式包怎么选？**
A: 通过 `--subtitle-preset` 指定：`variety`（综艺，大字亮黄黑描边）、`interview`（访谈，白字细描边稳重）、`course`（课程，白字深色底框长时间阅读）、`minimal`（极简，白字极细描边）、`vertical`（竖屏 9:16，底部留白抬高避开平台 UI）。样式定义为 JSON，存放于 `templates/subtitle_styles/`，可自行新增或改造。

**Q: 双语同轴字幕怎么用？**
A: 配合翻译使用：`--translate-subs en --bilingual`。工具会先翻译，再生成原文轨+译文轨同轴 ASS 字幕（`subtitle_bilingual.ass`），两轨用不同样式错位显示。默认两轨都显示，可用 `--no-original-track` 或 `--no-translation-track` 单独关闭某一轨。

**Q: 术语表怎么配置？品牌名错译能强制纠正吗？**
A: 用 `--glossary 术语表.json` 指定，JSON 格式为 `{"源词": "目标词"}`，也支持按语言分表 `{"en": {"源词": "目标词"}, "ja": {...}}`。翻译前用占位符隔离受保护术语（机翻不会改写），翻译后还原并按术语表校对。命中率统计输出到日志；未命中的术语写入 `待确认清单` JSON。人名/产品名/专业词均可纳入。

**Q: 字幕烧录怎么用？需要手写 filter_complex 吗？**
A: 不需要。加 `--burn-subtitle` 即可，工具会自动把样式包直连 ffmpeg `subtitles` filter 的 `force_style` 参数完成硬字幕压制。双语 ASS 用内嵌样式渲染，保证与预览一致。低配机自动用 ultrafast 编码档位，不拖累电脑。需要本机安装 ffmpeg。

**Q: 术语命中率 100% 怎么保证？**
A: 有术语表时，源术语在翻译前被替换为私有区占位符，机翻原样保留，翻译后强制还原为目标词——因此命中率可达 100%。若个别占位符被机翻破坏，会自动列入待确认清单供人工复核，不会静默错译。

### v4.6.0 新增功能 FAQ

**Q: 播客模式怎么用？**
A: 运行 `--podcast` 即可。工具会执行完整的播客流水线：说话人分离 → Podcasting 2.0 章节标记 → 金句提取。输出包含 `chapters.json`（可直接导入播客平台）、`highlights.json`（金句+时间戳+置信度）、`speaker_timeline.json`（逐说话人时间线）。

**Q: 三类说话人分离预设有什么区别？**
A: `interview`（访谈/播客：2-3人，中等间隔，merge_gap=1.0秒）；`meeting`（会议/讨论：3-6人，短间隔，merge_gap=0.8秒）；`phone`（电话/对讲：2人，长间隔，merge_gap=2.0秒）。通过 `--diarize-profile` 指定。质量评分自动输出，无需额外参数。

**Q: 金句评分原理是什么？**
A: 纯本地三信号评分（无API）：句长（15-80字最佳，占25%权重）+ 语义完整度（是否含动词/主语/判断词，占45%权重）+ 关键词密度（命中核心观点词如"关键""方法""经验"等，占30%权重）。置信度≥0.5的才会输出。

**Q: 听后简报怎么用？**
A: 运行 `--weekly-briefing` 即可。工具会查询 queue_manager 的 SQLite 队列，按周聚合生成 HTML 简报。简报包含：本周处理文件数、每日处理分布、总时长、金句 Top10。适合"每周等报告"的使用习惯。

**Q: Podcasting 2.0 标准是什么？**
A: Podcasting 2.0 是播客行业的现代标准，支持章节标记、章节图片、链接、字幕等。本工具生成的 `chapters.json` 遵循该标准，可直接导入 Apple Podcasts、Overcast、Pocket Casts 等平台，让听众可以按章节跳转。

### v4.5.0 新增功能 FAQ

**Q: 首跑自检怎么用？**
A: 运行 `--doctor` 即可。工具会一次性探测 ffmpeg 可用性、whisper 模型缓存、磁盘剩余空间、内存水位和 GPU 可用性，输出检查报告。如果有问题项，会给出「缺什么→给什么」的修复命令清单，但不会自动执行写操作（先清单后确认）。

**Q: 模型下载失败怎么办？**
A: 使用 `--download-model tiny` 下载。工具会自动重试 3 次，支持断点续传（HTTP Range），并显示进度条和下载速度。国内用户建议先执行 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`。

**Q: --quick 模式有什么用？**
A: 快速模式仅做语音转文字 + 时间戳摘要，跳过视觉分析、场景切割和剪辑链，5 分钟内产出单文件 Markdown。适合低配机与新用户快速体验，末尾自动附加 3 条「下一步建议」引导发现更多功能。

**Q: 医生模式会修改我的系统吗？**
A: 不会。doctor 模式只读探测，输出修复命令清单供用户参考。所有写操作（安装 ffmpeg、下载模型等）都需要用户手动执行或使用 `--download-model` 参数。

### v4.4.0 新增功能 FAQ

**Q: 一键成片怎么用？**
A: 运行 `--auto-edit` 即可。工具会自动检测高光片段，通过 ffmpeg filter_complex 链生成成片视频。支持 3 种风格：`口播精简`（去除冗余保留核心）、`高光集锦`（精选高光片段）、`预告片`（悬念感强）。输出包含成片视频、EDL 映射表和平台规格包。

**Q: 一键成片支持哪些平台？**
A: 支持抖音（9:16 竖屏 1080x1920）、B站（16:9 横屏 1920x1080）、快手（9:16 竖屏）、微信视频号（9:16 竖屏）。通过 `--edit-platform` 指定。

**Q: 字幕翻译需要什么依赖？**
A: 需要安装 cn-llm-router skill。未安装时工具会降级为仅输出中文字幕，并提示安装。翻译通过 subprocess 调用 router.py 的 translate 任务，支持 EN/JP/KO/FR/DE/ES/RU 七种语言。

**Q: BGM 识别准确吗？**
A: BGM 识别基于 chromaprint 音频指纹，匹配本地参考库。需要用户提供常见 BGM 样本建立参考库。无依赖时该功能自动隐藏，不阻塞主流程。未知 BGM 会标记为高风险。

**Q: 封面帧选取的原理是什么？**
A: 综合 Laplacian 锐度（清晰度）、人脸数量/位置（居中优先）、三分法构图评分和亮度适中度四个维度，从场景边界候选帧中选出 Top3。

**Q: 剪映 6.0 适配是什么？**
A: 升级了 draft.json 生成器以对齐剪映 6.0 新 schema（materials/tracks/segments）。如果生成失败会自动降级为 SRT+EDL 格式，并输出 Premiere Pro/DaVinci Resolve/Final Cut Pro 的 EDL 导入指南文档。

## 更新提醒
启动时会自动检查 GitHub 上的新版本，发现更新时会显示提醒。使用 `--no-update-check` 可跳过此检查。

## 联系方式
如有更好建议：njskills@agent.qq.com

## 更新日志

| v4.7.0 | 2026-11-16 | 增加：字幕样式包（5套JSON样式：综艺/访谈/课程/极简/竖屏，SubtitleStylist 升级为样式包加载器，SRT/ASS/VTT 双格式多格式导出，内置兜底降级）；增加：双语同轴字幕（原文轨/译文轨独立开关，ASS 用 Orig/Trans 双样式错位显示）；增加：术语表引擎（GlossaryEngine 占位符前置替换+后置校对+命中率统计+待确认清单JSON，SubtitleTranslator 集成，品牌名零容忍）；增加：字幕烧录一条命令（SubtitleBurner 封装 ffmpeg 硬字幕压制，样式包直连 force_style，按硬件档位选编码 preset）；增加：--subtitle-preset / --bilingual / --glossary / --burn-subtitle / --original-track 等参数；补充：config.yaml 样式包/术语表/烧录/双语配置段与 FAQ |
| v4.6.0 | 2026-11-02 | 增加：播客模式（core/podcast 模块：PodcastPipeline 整合说话人时间线+Podcasting 2.0 章节标记+金句提取，HighlightExtractor 三信号本地评分（句长/语义完整度/关键词密度），输出 chapters.json/highlights.json/speaker_timeline.json）；增加：说话人分离三类预设（interview/meeting/phone，阈值/窗口/说话人上限可配，v4.1 质量评分改为随结果自动输出）；增加：听后简报（WeeklyBriefing 复用 queue_manager SQLite + 周聚合视图，HTML 简报含本周处理/时长分布/金句Top10）；增加：报告渲染器统一（合并音频/视频重复分支到统一渲染器，删除旧音频 JSON 路径）；增加：--podcast / --diarize-profile / --weekly-briefing 参数 |

<details>
<summary>历史版本</summary>

### v4.4.0 增加：一键成片（ffmpeg filter_complex 链，含片段拼接+转场+ASS字幕烧录+BGM+人声闪避，3种成片风格：口播精简/高光集锦/预告片，导出平台规格包：抖音9:16/B站横屏/快手/视频号，含BGM建议库与EDL映射表，仅导出不自动发布）；增加：封面帧智能选取（Laplacian锐度+人脸数量/位置+三分法构图+亮度评分，输出Top3 PNG并附理由）；增加：自动字幕翻译（白名单桥接 cn-llm-router 翻译任务，subprocess 调用 router.py chat --task translate --json，按字幕批量+术语表约束，生成EN/JP/KO/FR/DE/ES/RU的SRT/ASS/VTT，未安装则降级为仅输出中文字幕+提示安装）；增加：BGM识别（可选依赖 chromaprint/fpcalc 计算音频指纹，匹配本地小参考库，输出版权风险提示：low/medium/high/unknown，无依赖则隐藏）；优化：剪映6.0适配+EDL导入指南（升级 draft.json 生成器对齐新schema：materials/tracks/segments，失败自动降级为SRT+EDL，输出Premiere Pro/DaVinci Resolve/Final Cut Pro导入指南文档）；增加：--auto-edit / --edit-style / --edit-platform / --bgm-path / --cover-select / --translate-subs / --translate-format / --bgm-detect / --jianying-v6 参数 |

<details>
<summary>历史版本</summary>

### v4.3.0
- 增加：纯音频输入（mp3/m4a/wav 播客与录音，ffmpeg 探测后直接转 16k 单声道 wav 进 ASR）
- 合并：场景检测+章节切片为「场景管理」模块（detect→slice 一条链）
- 增加：短视频爆款预测（多模态特征+爆款样本对比，概率评分+改进建议）
- 增加：实时直播分析（流式ASR+滑动窗口+敏感词检测+实时告警）
- 增加：--scene-management / --viral-predict / --live-analyze 参数
- 优化：HTML/JSON/Markdown 报告新增爆款预测和直播分析板块
- 增加：tiny 模型优先体验（75MB 低门槛，首次使用从 466MB 降至 75MB）
- 增加：说话人分离质量评分（声纹距离 + 重叠率，0-100 分 + 高/中/低等级）
- 增加：剪映 draft.json 导出（可直接导入剪映专业版）
- 增加：--jianying / --quality-score 参数
- 优化：硬件自适应默认 tiny 模型，低配电脑友好

<details>
<summary>历史版本</summary>

### v2.2.0
- 增加：使用场景示例表格（7个常见场景 + 对应命令）
- 增加：反模式 / 千万别这样用警告（7条）
- 增加：识别准确率说明表格（4个模块）
- 增加：首次使用前模型下载提醒（加速镜像命令）
- 增加：场景切分不准、文字识别漏字的原因说明
- 优化：触发方式 -> 使用场景示例，附场景+命令速查表
- 优化：文档结构新增前置提示
- 优化：准确率自检列表现已内置

### v2.1.0
- 增加：网络下载 3 次自动重试机制
- 增加：能力边界与限制表格
- 增加：FAQ 常见问题（安装/运行/输出三类）
- 优化：错误提示改为中文，附带修复建议
- 优化：网络不稳定时自动重试，不再直接退出

### v2.0.0
- 增加：硬件自适应（自动检测 CPU/内存/GPU，动态调整并行参数）
- 增加：进程优先级控制（nice_level），低配电脑自动降低优先级
- 增加：缓存自动清理（限制缓存目录大小，防 OOM）
- 增加：`--max-memory`、`--nice`、`--no-adaptive` 参数
- 修复：`scene_tags`/`scene_types` 拼写错误
- 修复：highlights 类型不匹配问题

### v1.0.0
- 首个稳定版本
- 支持本地视频和 HTTP URL 输入
- HTML/JSON/Markdown 三格式输出
- 模块化设计，便于扩展

</details>
