---
name: zhz-video-logo
description: 视频批量加 logo/水印。递归扫描目录或处理单个视频，用 ffmpeg 把图片 logo（PNG/JPG）或文字水印（Pillow 渲染，支持中文）叠加到固定位置，标识来源版权、防盗用。触发词：给视频加logo/加水印/打水印/文字水印/版权标识/video logo/watermark。给课程加logo。Use when user asks to add a logo, text watermark, or copyright mark to videos, batch-brand a video folder, or protect course/product videos from reuse.
homepage: http://openclaw.bjbook.net/
---

# 视频批量加 logo/水印

给教学/产品视频固定位置加公司 logo 或文字水印，标识版权、防盗用。水印来源两种：图片 logo（PNG/JPG，推荐透明 PNG）或文字（Pillow 渲染成透明 PNG，支持中文）。

核心脚本 `scripts/video_logo.py` 为纯 Python 标准库实现，只依赖 `ffmpeg`/`ffprobe`（文字模式额外需 Pillow），可脱离 OpenClaw 独立运行。

位置有 9 个预设方位或自定义坐标，透明度 0~100%，尺寸可按像素或视频宽度百分比自适应。
自动跳过已加过水印的文件（comment 标志 + 台账），先写临时文件校验通过才落盘，默认保留原片，失败保留原件。支持 dry-run 预览、`--out-dir` 输出、`--replace` 原地替换。

## 前置检查

1. ffmpeg 可用：`ffmpeg -version`。缺失则 `winget install ffmpeg`，或用 `FFMPEG_PATH`/`FFPROBE_PATH` 指定。
2. 水印来源：图片存在且扩展名合法；文字模式能 `python -c "import PIL"`（缺失则 `pip install pillow`）。
3. 目标路径存在，磁盘空间足够（约等于源文件大小）。

## 标准流程

先 **dry-run 预览**，确认无误再执行。脚本路径相对本 SKILL.md 解析。

1. 问清三件事：用图片还是文字、放哪个位置、要多透明。没说就用默认（图片/文字右下角、80% 透明、原始大小）。

2. 预览：
   ```bash
   # 图片 logo
   python {baseDir}/scripts/video_logo.py "D:\Videos" --logo "D:\assets\company.png" --dry-run
   # 文字水印
   python {baseDir}/scripts/video_logo.py "D:\Videos" --text "张老师课程" --dry-run
   ```
   完成标准：打印待加水印/跳过清单（分辨率、编码、体积、时长）及生效的水印来源、位置、透明度。

3. 确认后正式执行（**默认保留原片**，输出同目录 `*_watermark` 文件）：
   ```bash
   python {baseDir}/scripts/video_logo.py "D:\Videos" --logo "D:\assets\company.png" --position bottomright --opacity 70
   python {baseDir}/scripts/video_logo.py "D:\Videos" --text "内部资料" --position center --opacity 25
   python {baseDir}/scripts/video_logo.py "D:\Videos" --logo "D:\assets\company.png" --out-dir "E:\Branded"  # 输出到指定目录
   python {baseDir}/scripts/video_logo.py "D:\Videos" --logo "D:\assets\company.png" --replace  # 原地替换（覆盖原片）
   ```
   完成标准：退出码 0，汇总行显示"完成 N | 跳过 M | 失败 0"。

4. 报告：转述完成/跳过/失败数量、体积变化、耗时，说明 logo 位置与透明度。

## 关键行为（无需配置即生效）

- **已加过不再重复加**：命中 comment 标志（metadata `comment` 字段追加 `zhz-video-logo|...`，跟随文件本身）或台账 `.video_logo_ledger.json`（扫描根目录，size+duration 指纹）任一即跳过；`--force` 只更新标志、不重复堆叠。
- **安全优先**：先写临时文件 `.vlogo_tmp_*`，校验通过（可解析、含视频流、时长一致）才落盘，失败保留原片；`--replace` 也需校验通过才覆盖。
- 音轨 AAC/MP3 直接复制，其余转 AAC；字幕 MP4 转 mov_text、MKV 直接复制。
- 支持 14 种常见视频扩展名，可用 `--extensions` 追加。

## 参数速查

**位置与透明度**

| 场景 | 命令片段 |
|------|----------|
| 右下角（默认） | `--position bottomright` |
| 左上角 | `--position topleft` |
| 居中水印（半透明覆盖） | `--position center --opacity 25` |
| 精确像素坐标 | `--position 100,50`（相对左上角） |
| 与边缘距离 | `--margin 20`（预设方位生效，默认 12px） |
| 半透明水印 | `--opacity 50`（0~100，100=不透明） |
| 固定宽度 | `--logo-width 160` |
| 随分辨率自适应 | `--logo-scale 12`（宽=视频宽 12%，优先于 `--logo-width`） |

9 个预设方位：`topleft` `top` `topright` `left` `center` `right` `bottomleft` `bottom` `bottomright`

**文字水印**（`--text` 指定内容，此时忽略 `--logo`）

| 场景 | 命令片段 |
|------|----------|
| 基本文字水印 | `--text "张老师课程"` |
| 指定字体 | `--font C:/Windows/Fonts/simhei.ttf` |
| 指定字号 | `--font-size 64` |
| 指定颜色 | `--font-color yellow` / `#FF0000` / `255,0,0,128` |
| 版权符号 | `--text "©2026 公司名"` |

字体未指定自动探测：微软雅黑 → 雅黑粗体 → 黑体 → 等线 → 宋体 → Arial（macOS 用 PingFang，Linux 用 Noto CJK）。

**画质档位**（加水印必须重新编码，档位封装底层参数）

| 场景 | 命令片段 |
|------|----------|
| 最佳画质 | `--quality best`（H264） |
| 默认平衡 | `--quality balanced`（H264，默认） |
| 体积优先 | `--quality small`（H265） |
| 最小体积 | `--quality smallest`（H265） |

**其他**

| 场景 | 命令片段 |
|------|----------|
| 输出到指定目录 | `--out-dir "D:\Branded"` |
| 原地替换原片 | `--replace`（谨慎，覆盖原视频） |
| 强制重加水印 | `--force`（忽略 comment 标志与台账） |
| 查看是否已加水印 | `ffprobe -v quiet -show_entries format_tags=comment -of csv=p=0 文件.mp4` |

## 注意事项

- 加水印必须完整转码，耗时明显长于纯压缩。大量视频建议后台运行（`exec` 起任务 + `process poll` 跟进）。
- 默认 `--quality balanced`（H264）以画质优先；要瘦身改用 `small`/`smallest` 或配合 `zhz-video-compress` 分两步。
- 混有不同分辨率素材时优先用 `--logo-scale`（scale2ref 按宽度换算，视觉比例一致），而非固定 `--logo-width`。
- 水印宽度建议不超过视频宽度的 1/4。
- 文字字号 `--font-size` 为固定像素，不随分辨率缩放；跨分辨率批量建议用 `--logo-scale` 或分两批处理。
- `--out-dir` 不能位于扫描目录内部（避免重复扫描输出）。
- `--replace` 下源容器与目标不一致（如 `.avi`→`.mp4`）会替换为新扩展名文件；默认始终保留原片。
- 台账勿删；即使丢失，comment 标志仍保证"已加过不再加"。第三方转码可能去掉 comment，必要时用 `--force`。

## 验证

1. 汇总行无"失败"，或失败项逐条说明原因（原片完好）。
2. 抽一帧确认 logo 可见（不能只看退出码）：
   ```bash
   ffmpeg -y -v error -ss 2 -i "输出文件.mp4" -frames:v 1 "$env:TEMP\check.png"
   ```
   用 `read`/`view_image` 查看该 PNG，确认位置与透明度符合预期。
3. 相同命令再跑一遍，应全部显示"跳过"（幂等性验证）。
