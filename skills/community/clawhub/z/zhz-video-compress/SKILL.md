---
name: zhz-video-compress
description: 视频整理与高效压缩。当用户要求"压缩视频""视频瘦身""整理视频目录""video compress""批量转 H265""节省磁盘空间"时使用。Use when user asks to compress videos, batch-transcode a video folder, or organize/slim down video files.
homepage: http://openclaw.bjbook.net/
---

# 视频整理与高效压缩

递归扫描目录或处理单个视频，用 ffmpeg 转 H.265/H.264 大幅压缩体积。自动跳过已压缩文件与小文件，压缩后校验时长与流，无收益或失败自动保留原片。默认保留原片，支持 `--replace` 原地替换与按拍摄年月归档整理。

核心脚本 `scripts/video_compress.py` 可独立运行（仅依赖 ffmpeg/ffprobe）。

## 前置检查

1. `ffmpeg -version` 与 `ffprobe -version` 均能输出版本号，否则先安装 ffmpeg。
2. 目标路径存在，磁盘空间充足。

## 标准流程

始终**先 dry-run 预览，确认无误再实际执行**。脚本路径相对本 SKILL.md 解析。

1. 预览将要处理的文件：

   ```
   python {baseDir}/scripts/video_compress.py "D:\Videos" --dry-run
   ```

   - 打印待压缩/跳过清单及每个文件的分辨率、编码、体积、码率。

2. 确认参数后正式执行（**默认保留原片**，输出到同目录 `*_compressed` 文件）：

   ```
   python {baseDir}/scripts/video_compress.py "D:\Videos"
   python {baseDir}/scripts/video_compress.py "D:\Videos" --out-dir "E:\Compressed"
   python {baseDir}/scripts/video_compress.py "D:\Videos" --replace   # 仅显式要求时才原地替换
   ```

   - 完成标准：退出码 0，汇总行显示"压缩完成 N | 跳过 M | 失败 0"，并打印节省空间。

3. 报告结果：转述汇总（完成/跳过/无收益/失败数量、总节省空间与百分比、耗时）。

## 关键行为（默认生效，无需额外配置）

- **已压缩不再压缩**：comment 标志 + 台账 + 小文件(<10MB)/低码率(<300kbps)过滤，命中任一即跳过；`--force` 可强制重压。
- **安全优先**：先写临时文件，校验通过才落盘；压缩收益 <5% 或校验失败一律保留原片。**默认不替换原片**，仅 `--replace` 才原地替换。

## 画质与速度档位

| 场景 | 命令片段 |
|------|----------|
| 体积优先（默认，最常用） | `--quality small`（H265） |
| 画质与体积平衡 | `--quality balanced`（H265） |
| 最小体积 | `--quality smallest`（H265） |
| 最佳画质（兼容性最好） | `--quality best`（H264） |
| 压缩更快，体积略增 | `--speed fast` |
| 更省体积，耗时更长 | `--speed slow` |

## 常用参数选择

| 场景 | 命令片段 |
|------|----------|
| 4K 降到 1080p | `--max-height 1080` |
| 输出到指定目录（默认保留原片） | `--out-dir "E:\Compressed"` |
| 原地替换原片（谨慎，会覆盖原视频） | `--replace` |
| 按拍摄年月整理归档 | `--organize` |
| 强制重压已跳过的文件 | `--force` |
| 查看文件是否已被压缩过 | `ffprobe -v quiet -show_entries format_tags=comment -of csv=p=0 文件.mp4` |

## 验证

任务结束后确认：汇总行无"失败"，或失败项已逐条说明原因（原片均完好）。
