# zhz-video-compress 使用说明（README）

本文档收录脚本的实现细节、关键行为说明与注意事项。日常使用时直接看 `SKILL.md` 即可，遇到特殊场景或需要理解底层逻辑时再查阅本文档。

## 脚本概览

`scripts/video_compress.py` 是**纯 Python 标准库**实现，只依赖系统里的 `ffmpeg`/`ffprobe`，**可脱离 OpenClaw 独立运行**（直接 `python video_compress.py <路径>` 即可）。

用 ffmpeg 转 H.265(默认)/H.264 大幅压缩体积，支持 dry-run 预览、默认保留原片（输出到同目录 `_compressed` 文件或 `--out-dir`）、`--replace` 原地替换、按拍摄年月归档整理。

## 前置检查细节

1. 确认 ffmpeg 可用：`ffmpeg -version`。缺失则先安装（Windows: `winget install ffmpeg`），或用环境变量 `FFMPEG_PATH`/`FFPROBE_PATH` 指定可执行文件。
   - **完成标准**：`ffmpeg -version` 与 `ffprobe -version` 均能输出版本号。
2. 确认目标路径存在，且有足够磁盘空间（保留原片输出时需约等于源文件大小的临时空间；`--replace` 原地替换也需约等于源文件大小的临时空间）。

## 关键行为（无需额外配置即生效）

- **已压缩不再压缩**：三重判定，命中任一即跳过
  - **comment 标志**（最可靠）：压缩时向文件 metadata 的 `comment` 字段追加
    `zhz-video-compress|v1|h265|crf28|preset|时间戳`（原有 comment 内容会保留，用 `;` 拼接；
    `--force` 重压只更新标志、不重复堆叠）。comment 跟随文件本身，MP4/MOV/MKV 均原生支持，
    跨目录/跨机器也能识别；
  - 台账 `.video_compress_ledger.json`（记录于扫描根目录）中已有该文件的 size+duration 指纹；
  - 文件小于 `--min-size`（默认 10MB）或码率低于 `--skip-below-kbps`（默认 300kbps）。
- **安全优先**：先写临时文件 `.vcompress_tmp_*`，压缩后校验（能否解析、是否含视频流、时长是否一致），
  通过才落盘；失败或**压缩收益 <5%** 一律保留原片。中途 Ctrl+C 不会损坏原件。
  **默认保留原片**，不会替换原视频；只有 `--replace` 才会原地替换原片（且仍需临时文件校验通过才覆盖）。
- 音频为 AAC/MP3 时直接复制不转码，其余转 AAC；字幕在 MP4 中转 mov_text，MKV 中直接复制。
- 支持 15 种常见视频扩展名，含 `.dav` 等可用 `--extensions` 追加。

## 底层编码参数对应关系

压缩必须重新编码视频。脚本把底层编码参数封装成语义化档位，无需了解 ffmpeg 选项：

| 档位 | codec | crf | ffmpeg preset |
|------|-------|-----|---------------|
| `--quality small`（默认） | h265 | 28 | medium |
| `--quality balanced` | h265 | 24 | medium |
| `--quality smallest` | h265 | 32 | medium |
| `--quality best` | h264 | 18 | medium |
| `--speed fast` | — | — | fast |
| `--speed balanced`（默认） | — | — | medium |
| `--speed slow` | — | — | slow |

> 高级用户仍可用 `--codec` / `--crf` / `--preset` 覆盖档位，但一般无需使用。
> 显式指定 `--codec` 但未指定 `--crf` 时，使用该编码的默认 crf（h265=28，h264=23）。

## 输出与归档规则

- 输出扩展名规则：源为 `.mp4`/`.mov`/`.m4v` 时保留原容器；源为 `.mkv` 时保留 `.mkv`；其余容器在含字幕时转 `.mkv`，不含字幕时转 `.mp4`。
- `--organize`：按拍摄时间（优先 `creation_time`，回退文件修改时间）归档到 `YYYY-MM/` 子目录，重名自动加序号。
- `--out-dir` 不能位于扫描目录内部（脚本会拒绝，避免重复扫描输出）。

## 注意事项

- H.265 压缩速度约为 H.264 的 1/2~1/3，大量视频建议后台运行，用 `exec` 起任务后通过 `process poll` 跟进，不要空转轮询。
- **长时间视频务必禁用超时**：本机实测 H.265 CRF=28 编码约 0.54 倍实时速度，约 21 分钟片长需约 38 分钟。后台运行时应将超时设为 0（禁用），否则进程超时被终止会留下 moov atom 未写入的损坏临时文件（需手动删除 `*_compressed` 文件后重跑）。
- 长任务先告知用户预计耗时（可从 dry-run 的文件总体积估算），再开始执行。
- `--replace` 原地替换模式下若源容器与目标不一致（如 `.avi`→`.mp4`），原文件会被替换为新扩展名的文件。默认（不 `--replace`）时原片始终保留，不会替换。
- 台账文件请勿删除，它是本目录压缩历史的记忆；但即使丢失，文件 comment 标志仍可保证"已压缩不再压缩"。
- 注意：若用第三方工具重新转码压缩过的文件，comment 可能被去掉或保留，行为取决于该工具；必要时用 `--force` 显式控制。

## 验证

任务结束后确认：
1. 汇总行无"失败"，或失败项已逐条说明原因（原片均完好）。
2. 压缩产物可被 ffprobe 正常解析（时长与源一致），未留下 `.vcompress_tmp_*` 临时文件。
