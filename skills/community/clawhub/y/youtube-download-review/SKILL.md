---
name: youtube-download-review
description: 处理 YouTube 链接的视频下载与音乐向解读。只要用户提供 YouTube 链接，并提到下载视频、合并 MP4、下载封面、字幕处理（内嵌/忽略）、推荐理由、内容简介时，都应优先使用本技能。默认下载 1080p 视频 + 最高品质 m4a，自动合并为 mp4，并按视频标题创建目录输出全部产物。（此Skill 依赖系统软件包：yt-dlp 和 ffmpeg）
---

# YouTube 下载 + 硬字幕压制 + 音乐媒体解读

当用户给出 YouTube 链接并希望下载视频时，按本技能执行完整流程：
- 下载视频与音频并合并为 MP4
- 下载封面并转为 JPG
- 根据标题目录归档
- 生成音乐媒体视角的推荐理由与约 50 字简介

## 目标
- 视频分辨率上限 1080p，优先 MP4 容器
- 音频优先最高品质 m4a
- 自动生成可播放的 MP4 文件
- 若用户选择字幕，执行简体中文字幕优先并硬字幕压制
- 每个视频单独目录保存，目录名为视频标题

## 输入要求
- 必须是 YouTube 链接（`youtube.com` 或 `youtu.be`）
- 可单条或多条链接；多条时逐条处理

## 输出目录与文件规范
默认在当前工作目录输出，单条视频目录结构如下：

```text
<视频标题>/
  <视频标题>.source.mp4
  <视频标题>.mp4
  <视频标题>.jpg
  <视频标题>.srt                 # 仅字幕流程中可得时保留
  推荐解读.md
```

说明：
- `<视频标题>.source.mp4`：音视频合并后的原始版（不带硬字幕）
- `<视频标题>.mp4`：最终交付版（若做硬字幕则为压制后文件）
- 按用户确认，默认保留上述两个视频文件，便于回退和二次处理

## 必须执行的交互（字幕选项）
在处理每个链接时，先探测可用字幕能力，然后提醒用户选择：
- `硬字幕压制（默认推荐）`
- `忽略字幕`

规则：
- 用户选“硬字幕压制”：执行字幕下载与烧录流程
- 用户选“忽略字幕”：直接输出 `<视频标题>.source.mp4` 并复制/重命名为 `<视频标题>.mp4`
- 若字幕不可用或不可翻译为简中：明确告知，并继续产出无字幕版 `<视频标题>.mp4`

## 标准工作流

### 1) 校验与取元信息
1. 校验链接是否为 YouTube。
2. 用 `yt-dlp --dump-single-json` 获取：
   - `title`
   - `description`
   - `subtitles` / `automatic_captions`
3. 依据 `title` 创建目录。

示例命令：

```bash
yt-dlp --dump-single-json "<YOUTUBE_URL>"
```

### 2) 下载音视频并合并为 source MP4
格式策略（按顺序回退）：
1. `bestvideo[height<=1080][ext=mp4] + bestaudio[ext=m4a]`
2. `best[height<=1080][ext=mp4]`
3. `best[height<=1080]`

示例命令：

```bash
yt-dlp \
  -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "%(title)s/%(title)s.source.%(ext)s" \
  "<YOUTUBE_URL>"
```

### 3) 下载封面为 JPG

```bash
yt-dlp \
  --skip-download \
  --write-thumbnail \
  --convert-thumbnails jpg \
  -o "%(title)s/%(title)s.%(ext)s" \
  "<YOUTUBE_URL>"
```

### 4) 字幕处理（用户选“硬字幕压制”时）
字幕语言优先级：
1. 简体中文（`zh-Hans`、`zh-CN`）
2. 其他中文（`zh`、`zh-TW`）后转简体
3. 非中文字幕自动翻译为简体中文（平台支持时）

建议先尝试：

```bash
yt-dlp \
  --skip-download \
  --write-sub \
  --write-auto-sub \
  --sub-langs "zh-Hans,zh-CN,zh,zh-TW,*" \
  --sub-format "srt/best" \
  -o "%(title)s/%(title)s.%(ext)s" \
  "<YOUTUBE_URL>"
```

拿到字幕后，确保最终用于烧录的是简体中文 `.srt`（必要时做繁转简）。

### 5) 硬字幕压制到最终 MP4
使用 ffmpeg 将字幕烧录进画面（重编码）：

```bash
ffmpeg -y \
  -i "<视频标题>/<视频标题>.source.mp4" \
  -vf "subtitles='<视频标题>/<视频标题>.srt'" \
  -c:v libx264 -crf 20 -preset medium \
  -c:a copy \
  "<视频标题>/<视频标题>.mp4"
```

注意：
- 硬字幕不可关闭
- 会重编码视频，耗时更长、体积可能变化

若用户选“忽略字幕”，则：
- 将 `<视频标题>.source.mp4` 复制或重命名为 `<视频标题>.mp4`

### 6) 生成音乐媒体视角解读
基于 `title` + `description` 输出两部分内容：
- 推荐理由：以资深音乐媒体人口吻，聚焦音乐性、编曲/制作、情绪表达、文化语境或舞台表现
- 内容简介：约 50 字，信息密度高，避免空泛褒奖

写入 `<视频标题>/推荐解读.md`，并在终端同步展示同内容。

## 推荐解读.md 模板

```markdown
# 推荐解读

## 视频信息
- 链接：<YouTube URL>
- 标题：<视频标题>

## 推荐理由
<1 段，音乐媒体人视角>

## 内容简介（约50字）
<约 50 字>
```

## 终端输出模板

```text
[完成] 已处理：<视频标题>
- 最终视频：<视频标题>/<视频标题>.mp4
- 原始合并：<视频标题>/<视频标题>.source.mp4
- 封面：<视频标题>/<视频标题>.jpg
- 解读：<视频标题>/推荐解读.md

推荐理由：
<同文件内容>

内容简介（约50字）：
<同文件内容>
```

## 异常与兜底
- 链接不可访问：说明原因并提示检查链接或网络
- 1080p 不可用：回退到可用最高画质（仍优先 MP4）
- m4a 不可用：回退最佳可用音频，并在结果中说明
- 封面转换失败：保留原始缩略图格式并说明
- 字幕不可得或不可翻译：说明并继续产出无字幕 MP4
- ffmpeg 不可用：明确提示安装 ffmpeg，并保留 `.source.mp4` 与字幕文件

## 质量要求
- 不删除用户已有文件
- 不覆盖无关目录内容
- 多链接任务按“一个链接一个目录”稳定输出
- 文案避免模板腔，保持专业、克制、可读
