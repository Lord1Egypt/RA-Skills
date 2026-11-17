---
name: zhz-transcript-summarize
description: "本地音视频转文字 + 要点摘要。触发词：转录音频、转录视频、语音转文字、音频总结、会议纪要、录音摘要、总结视频内容、transcribe、transcript、summarize podcast。Use when user asks to transcribe a local audio/video file and summarize its key points, or to re-summarize the same recording from a different angle."
homepage: http://openclaw.bjbook.net/
---

# 本地转写 + 要点摘要（两阶段）

把本地视频、音频或播客文件在本机转成文字，再提炼成要点摘要。转录稿按内容哈希缓存，换角度重新总结时跳过转录阶段。

## 环境依赖

| 依赖 | 用途 | 版本 |
|------|------|------|
| Python | 运行脚本 | 3.12+ |
| ffmpeg | 提取音频 | 6.1.1 |
| faster-whisper | 语音识别（本地） | 1.2.1（脚本自动安装） |

## 阶段一：转录（缓存命中则跳过）

**完成标准：** 得到转录稿缓存（JSON 及同目录 `.txt`）。

```bash
python "{baseDir}/scripts/transcribe.py" "<音频/视频路径>" [--model base] [--lang auto] [--force]
```

| 选项 | 默认 | 说明 |
|------|------|------|
| `--model` | `base` | Whisper 模型：tiny / base / small / medium / large-v3 |
| `--lang` | `auto` | 强制语言（zh/en/...）；auto 自动检测 |
| `--force` | — | 忽略缓存，强制重新转录 |
| `--device` | `auto` | auto / cpu / cuda |
| `--print` | — | 把转录全文打印到 stdout |
| `--cache-dir` | `~/.cache/zhz-transcript` | 缓存目录 |

模型默认 `base` 适合多数场景；长内容或要求更高准确度用 `small` 或 `medium`。

## 阶段二：摘要 / 总结

**完成标准：** 生成摘要文件 `summary.md` **和** `summary.html`。

换角度重新总结只需重跑本阶段，用不同 `--focus` / `--format` / `--length` 参数，完全跳过转录。

### 第一步：准备摘要输入

```bash
python "{baseDir}/scripts/summarize.py" "<原始文件路径>" \
  --focus "云原生架构选型理由与踩坑经验" \
  --audience "开发者" \
  --format key_summary \
  --length medium \
  --lang zh \
  [--glossary glossary.txt] [--format-sub srt] [--out-dir DIR]
```

| 选项 | 默认 | 说明 |
|------|------|------|
| `--model` | `base` | 用于定位缓存的模型名，须与转录时一致 |
| `--focus` | 空 | 总结焦点（空表示全面总结） |
| `--audience` | `通用读者` | 目标受众 |
| `--format` | `key_summary` | 摘要模板：key_summary / meeting / analysis / custom |
| `--template` | — | 自定义模板文件（`--format custom` 时必填） |
| `--length` | `medium` | 摘要长度：short / medium / detailed |
| `--lang` | `zh` | 摘要输出语言：zh / en |
| `--glossary` | — | 术语表 glossary.txt 路径 |
| `--timeline` | `auto` | on / off / auto；auto 表示 >20 分钟自动生成 |
| `--format-sub` | — | 导出字幕：srt / vtt |
| `--out-dir` | 默认 `summaries/<name>/<焦点slug>-<时间戳>/` | 输出目录 |
| `--cache-json` | — | 直接指定转录稿 JSON 路径 |
| `--cache-dir` | `~/.cache/zhz-transcript` | 缓存目录 |

### 第二步：生成摘要

1. 读取运行目录下的 `context.md`（转录稿全文）——路径以 `summarize.py` 结尾打印的「输出目录」为准。
2. 读取同目录下的 `summary_prompt.md`（模板与参数）。
3. 由当前代理会话的模型按模板生成摘要。
4. 用 `write` 工具写入 `summaries/<name>/summary.md`。

### 第三步：输出 HTML（必做）

```bash
python "{baseDir}/scripts/render_html.py" "<运行目录>" --title "会议记录"
```

| 选项 | 默认 | 说明 |
|------|------|------|
| `--title` | 第一个一级标题或文件名 | 页面标题 |
| `--out` | 同目录同名 `.html` | 输出 HTML 路径 |
| `--meta` | — | 标题下方元信息 |
| `--lang` | `zh` | HTML lang 属性 |

生成的 `.html` 双击即可用浏览器独立打开。

## 术语表 glossary.txt

格式：每行一条 `错误词 -> 正确词`，`#` 开头为注释。支持分隔符：Tab、`->`、`=>`、`→`、`=`、`：`（全角冒号）。示例见 `examples/glossary.example.txt`。

## 长内容时间轴

内容 >20 分钟自动生成 `timeline.md`（5 分钟一段的骨架）。生成摘要时，为每个时间段补一句要点，使长内容摘要带时间定位。

## 典型用法

```bash
# 1) 转写并缓存（首次）
python "{baseDir}/scripts/transcribe.py" "D:/pony/podcast-ep12.mp3" --model small

# 2) 总结（聚焦云原生选型与踩坑）→ 输出到 summaries/podcast-ep12/云原生架构选型理由与踩坑经验-<时间戳>/
python "{baseDir}/scripts/summarize.py" "D:/pony/podcast-ep12.mp3" \
  --focus "云原生架构选型理由与踩坑经验" --format key_summary --lang zh

# 3) 换角度（只提取行动项），完全跳过转录，且不会覆盖步骤 2 的摘要
python "{baseDir}/scripts/summarize.py" "D:/pony/podcast-ep12.mp3" \
  --focus "只提取行动项" --format meeting --glossary glossary.txt --format-sub srt

# 4) 摘要转 HTML（可独立打开）——路径用脚本结尾打印的「输出目录」
python "{baseDir}/scripts/render_html.py" "summaries/podcast-ep12/<运行目录>/summary.md"
```

每次换角度总结，脚本都会从缓存命中转录稿，只需修改 `--focus` / `--format` / `--length` 重跑 `summarize.py`，重新运行「阶段二」。
