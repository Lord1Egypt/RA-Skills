---
name: extract-audio
description: "异步提取视频音频并返回可直接用于 ASR 的音频 URL。用户提到从视频抽音轨、提取人声/旁白、先抽音频再识别字幕、加速字幕识别时必须使用本技能；在 llm-asr 前置检测到视频输入时也应优先触发。"
---

# Extract Audio Skill

用于把视频 URL 异步提取为音频 URL（`public_url`），常作为 `llm-asr` 前置步骤，减少视频解复用开销并提升识别吞吐。

接口文档（参考）：
- https://docs.vectcut.com/443403596e0

## 何时使用

- 用户明确要求“提取音频/抽音轨/导出音轨”
- 用户说“先抽音频再转字幕/先抽音频再 ASR”
- `llm-asr` 前置判断输入是视频 URL，希望优先用音频做识别

## 前置条件

- Python 3
- 已安装 `requests`
- `VECTCUT_API_KEY` 已设置且可用
- 若缺失或失效，先调用 `vectcut-login` 技能

## 执行方式

```bash
python <skill-path>/scripts/extract_audio_async.py "https://example.com/video.mp4" --output "./extracted_audio.json"
```

可选参数：
- `--poll-interval`：轮询间隔秒数，默认 `2.0`
- `--timeout`：总超时秒数，默认 `600`

## 处理流程

1. `POST /process/extract_audio/submit_task/submit_extract_audio_task` 提交任务，获得 `task_id`
2. `GET /process/extract_audio/submit_task/task_status?task_id=...` 轮询状态
3. 任务 `success` 后读取 `result.public_url`
4. 输出标准化结果 JSON，供 `llm-asr` 或其他技能消费

## 输出结果

默认文件 `extracted_audio.json`：

- `meta.source_video_url`
- `meta.task_id`
- `meta.status`
- `audio.public_url`
- `audio.raw_result`

## 与 llm-asr 的衔接

- 若该技能成功，优先把 `audio.public_url` 传给 `llm-asr`
- 若提取失败，可回退直接用原视频 URL 跑 `llm-asr`，并向用户说明降级原因

## 失败处理建议

- `video_url` 非法：提示补充可访问的 `http/https` 链接
- `task_id` 不存在/过期：提示重新提交提取任务
- 超时：建议增大 `--timeout` 或检查源视频可访问性
