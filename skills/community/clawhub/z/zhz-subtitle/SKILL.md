---
name: "zhz-subtitle"
description: "视频双语字幕生成与制作。触发词：transcribe、语音转文字、字幕、subtitle、双语字幕。Use when user asks to transcribe audio/video and generate bilingual subtitles."
homepage: http://openclaw.bjbook.net/
---

# 视频双语字幕生成器

为视频或音频文件自动生成中英文双语 SRT 字幕。

## 环境依赖

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| Python 3.12+ | 运行脚本 | 系统自带 |
| ffmpeg | 音频提取 | `winget install ffmpeg` / `brew install ffmpeg` |
| faster-whisper | 语音识别 | `pip install faster-whisper`（脚本自动安装） |

## 文件结构

输入文件：`{name}.{ext}`
工作目录：`subtitles/{name}/`（中间文件）
最终输出：`subtitles/{name}.srt`（双语字幕）

| 文件 | 位置 | 说明 |
|------|------|------|
| `{name}.mp3` | `subtitles/{name}/` | 提取的音频 |
| `{name}.transcript.json` | `subtitles/{name}/` | 转录结果（含时间戳） |
| `{name}_translated.json` | `subtitles/{name}/` | 翻译后的 JSON 段落 |
| `{name}.en.srt` | `subtitles/{name}/` | 英文字幕 |
| `{name}.chs.srt` | `subtitles/{name}/` | 中文字幕 |
| **`{name}.srt`** | **`subtitles/`** | **最终双语字幕文件** |

## 脚本调用说明

脚本目录：`{baseDir}/scripts/`（本 SKILL.md 同级的 `scripts/` 文件夹）。

**运行时不要读取脚本源码，直接按下表命令调用即可。** 每个脚本都是可直接执行的独立 Python 脚本。

| 脚本 | 用途 | 调用方式 | 参数说明 |
|------|------|----------|----------|
| `extract_audio.py` | 视频提取音频 | `python {baseDir}/scripts/extract_audio.py "<视频路径>" [输出路径]` | 省略输出路径时输出同名 `.mp3` |
| `transcribe.py` | 语音转文字 | `python {baseDir}/scripts/transcribe.py "<音频路径>" [模型大小] [语言]` | 模型：tiny/base/small/medium/large-v3（默认 base）；语言：zh/en（默认自动检测） |
| `json_to_srt.py` | 翻译 JSON 转 SRT | `python {baseDir}/scripts/json_to_srt.py "<翻译.json>" "<输出.srt>"` | 将 `segments` 字段转为 SRT |
| `build_translation.py` | 校验并规范化翻译 JSON | `python {baseDir}/scripts/build_translation.py "<转录.json>" "<翻译.json>" [输出.json]` | 校验条目数、强制对齐时间戳、重新序列化保证合法 JSON |
| `merge_srt.py` | 合并双语字幕 | `python {baseDir}/scripts/merge_srt.py "<第一.srt>" "<第二.srt>" "<输出.srt>" [译文在前]` | 传入 `yes` 表示译文在前（默认原文在前） |
| `verify_srt.py` | 验证字幕 | `python {baseDir}/scripts/verify_srt.py "<srt文件路径>"` | 校验格式、双语、时间戳 |

### 各脚本返回值（由 stdout 输出）

- `extract_audio.py`：输出 `音频提取完成：<路径>`
- `transcribe.py`：在 `subtitles/{name}/` 目录生成 `{name}.transcript.json` 和原始 SRT（`.chs.srt` 或 `.en.srt`，由检测语言决定）；stdout 输出「检测到的语言」「音频时长」「转录完成：共 N 个段落」
- `json_to_srt.py`：输出 `SRT 字幕已保存：<路径>（N 条）`
- `build_translation.py`：输出 `翻译 JSON 已规范化：<路径>（N 段）`；条目数不一致或 text 非字符串时输出 `[错误]` 并退出码 1
- `merge_srt.py`：输出 `双语 SRT 已保存：<路径>（N 条）`
- `verify_srt.py`：输出「✅ SRT 验证通过」及统计信息；失败则退出码为 1

## 工作流程

### 第一步：环境检查与验证

**完成标准：** 输入文件存在，依赖已就绪。

1. 验证输入文件存在（视频或音频）
2. 检查 ffmpeg 是否可用：`ffmpeg -version`
3. 创建输出目录 `subtitles/{name}/`
4. 记录输入文件的 name（不含扩展名），后续所有文件均使用此 name

### 第二步：提取音频（音频输入可跳过）

**完成标准：** MP3 音频文件已生成。

```bash
python {baseDir}/scripts/extract_audio.py "<视频路径>" "subtitles/{name}/{name}.mp3"
```

### 第三步：语音转文字

**完成标准：** 生成 `.transcript.json` 和原始 SRT。

```bash
python {baseDir}/scripts/transcribe.py "subtitles/{name}/{name}.mp3" [model_size] [language]
```

脚本自动输出到 `subtitles/{name}/` 目录：
- `{name}.transcript.json` — 含时间戳的转录数据
- 根据检测语言生成对应后缀的 SRT：
  - 英文原文 → `{name}.en.srt`
  - 中文原文 → `{name}.chs.srt`

**关键：** 记录检测到的语言（zh/en），第四步据此决定翻译方向。

> **中文一律使用简体**：`transcribe.py` 会在转录后自动将繁体中文转换为简体（Whisper 转写中文时默认输出繁体）。人工校对时也应保持简体，避免混入繁体字。

### 第四步：翻译

**完成标准：** 生成 `{name}_translated.json`。

翻译方向：
- 原文为中文 (zh) → 翻译为英文 (en)
- 原文为英文 (en) → 翻译为中文 (zh)

**执行方式：**

1. 读取 `subtitles/{name}/{name}.transcript.json`，逐段翻译，保持相同的 JSON 结构（`start`、`end`、`text` 字段）
2. 将翻译结果**直接写入 JSON 文件** `subtitles/{name}/{name}_translated.json`
3. 调用 `build_translation.py` 校验并规范化该 JSON：

```bash
python {baseDir}/scripts/build_translation.py "subtitles/{name}/{name}.transcript.json" "subtitles/{name}/{name}_translated.json"
```

`build_translation.py` 会校验条目数是否与转录一致、强制使用转录的 `start`/`end` 对齐时间戳，并用 `json.dump` 重新序列化，自动转义中文引号等特殊字符，保证输出为合法 JSON。若条目数不一致或 `text` 不是字符串，脚本会报错退出，此时需修正翻译 JSON 后重跑。

**⛔ 翻译结果必须符合严格 JSON 格式：** 模型生成的翻译数据必须是合法的 JSON，且结构与转录 JSON 完全一致。具体要求：

```json
{
  "language": "zh",
  "duration": 120.0,
  "segments": [
    {"start": 0.0, "end": 5.0, "text": "翻译文本"},
    {"start": 5.0, "end": 9.0, "text": "翻译文本"}
  ]
}
```

- `segments` 数组的条目数与原文**完全一致**，`start`、`end` 字段原样保留
- 每个 `text` 字段必须是字符串，不与 `start`/`end` 混在一行
- 不添加多余字段，不改变字段名，不写注释，不加 Markdown 围栏

* 翻译结果直接写成 JSON 文件即可，自动转义中文引号（“”）、书名号等特殊字符，保证输出合法 JSON。

**长视频分批翻译：** 当段落数超过 50 条时，将 segments 拆成多批（每批 30-50 条）翻译，最后合并为完整的 `subtitles/{name}/{name}_translated.json`，避免单次上下文过长导致遗漏或出错。

**纯数字段落不翻译：** 如果某段的 text 是纯数字（如 "1"、"1-20"、"1, 2, 3"），翻译后的 text 保持原文不变。

翻译原则：
- 保持原文语义和语气
- 字幕翻译应简洁，避免过长
- 保留专有名词（人名、地名）
- 教育内容保持术语准确
- 纯数字不翻译，直接保留原文
- 中文一律使用简体（不用繁体）

### 第五步：生成翻译字幕

**完成标准：** 生成翻译语言的 SRT 到 `subtitles/{name}/` 目录。

- 英文翻译 → `subtitles/{name}/{name}.chs.srt`
- 中文翻译 → `subtitles/{name}/{name}.en.srt`

```bash
python {baseDir}/scripts/json_to_srt.py "subtitles/{name}/{name}_translated.json" "subtitles/{name}/{name}.chs.srt"
```

中文翻译时后缀为 `.chs.srt`，英文翻译时为 `.en.srt`

### 第六步：合并双语字幕

**完成标准：** 生成最终 `subtitles/{name}.srt`，条目数一致。

```bash
python {baseDir}/scripts/merge_srt.py "subtitles/{name}/{name}.en.srt" "subtitles/{name}/{name}.chs.srt" "subtitles/{name}.srt" [translated_first]
```

默认：英文在前，中文在后。每条字幕显示为两行。合并时自动校验条目数，不一致时输出警告。

**最终文件名与输入文件完全一致，仅后缀从 `.mp4`/`.mp3` 变为 `.srt`，放在 `subtitles/` 目录下。**

### 第七步：验证

**完成标准：** 字幕文件通过格式和双语验证。

```bash
python {baseDir}/scripts/verify_srt.py "subtitles/{name}.srt"
```

验证内容：SRT 格式正确、时间戳无重叠、包含中英文、条目数一致。有错误则修复后重新验证，有警告则报告给用户。

### 第八步：完成报告

```
✅ 双语字幕生成完成！
文件：subtitles/{name}.srt
条目：{count} 条双语字幕
语言：中文 ↔ English
时长：{duration}
原文语言：{original_lang}
```

## 进度清单

```
字幕生成进度：
- [ ] 第一步：环境检查与验证
- [ ] 第二步：提取音频
- [ ] 第三步：语音转文字
- [ ] 第四步：翻译（纯数字不翻译）
- [ ] 第五步：生成翻译字幕
- [ ] 第六步：合并双语字幕
- [ ] 第七步：验证
- [ ] 第八步：完成报告
```

## 注意事项

- 脚本统一使用 Python `logging` 输出，`[错误]` 前缀表示 stderr 错误，INFO 输出到 stdout
- HF 镜像：脚本自动设置 `HF_ENDPOINT=https://hf-mirror.com`，解决国内访问问题
- 首次运行自动下载 Whisper 模型到 `~/.cache/huggingface/`
- 模型选择：`base` 适合大多数场景，长视频建议 `small` 或 `medium`
- 支持所有 ffmpeg 能处理的音视频格式
- **运行时直接调用上述脚本命令，无需读取脚本源码**

