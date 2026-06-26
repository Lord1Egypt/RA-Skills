---
name: 视频下载归档助手
slug: video-download-archive
version: 0.2.0
description: Validate single video URLs, download highest-quality files with yt-dlp, and archive results into a Feishu Bitable using platform tools.
---

## When to Use

- 用户发来单个视频链接，希望自动下载并归档
- 需要复用既有 yt-dlp 下载规则与元数据补全规则
- 需要把下载结果写入指定飞书多维表格
- 需要对已存在文件做补全、核对或补记录，而不是盲目重下

## Quick Reference

| Topic | File |
|------|------|
| 主流程 | `workflow.md` |
| 飞书表字段映射 | `bitable-mapping.md` |
| 错误与终止规则 | `error-handling.md` |
| 执行脚本 | `scripts/run_video_archive.py` |
| 使用说明 | `usage.md` |

## Core Rules

1. 只处理**单个视频链接**；不处理播放列表、频道页、多链接批量任务。
2. 必须先调用 `scripts/run_video_archive.py <url>` 完成预检、主键生成、本地查重、下载/补全和字段组装。
3. 主键固定为 `站点-视频ID`，同时写入“视频主键”和“视频唯一ID”。
4. 本地归档目录固定为 `~/Downloads/yt-dlp/<上传者目录>/`；优先用 `@handle` 作为上传者目录名。
5. 默认下载最高质量版本、优先 mkv、保留 `.info.json`，并沿用现有元数据补全规则。
6. 下载脚本只负责本地执行与生成 `record_fields`；飞书写表必须使用平台提供的 `feishu_bitable_app_table_record` 工具完成。
7. 写入飞书前若发现字段缺失、字段类型不匹配，或需要新增字段，必须暂停并先询问用户。
8. 已存在文件时优先补全与补记录，不要因为路径变化就直接重下。
