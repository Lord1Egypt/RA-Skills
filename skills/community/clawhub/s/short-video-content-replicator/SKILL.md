---
name: short-video-content-replicator
description: |
  当用户想要**一键复制抖音或B站短视频内容**、**把短视频转成带标点的高质量文字**、**提取视频干声和转录文本**、**端到端处理短视频内容**时自动触发。
  这是一个复合工作流技能：输入抖音/B站视频URL或本地视频目录，按严格6步顺序执行全流程（或从指定步骤断点续跑）。
  步骤包括：1. 下载视频（link-resolver-engine）；2. 提取MP3；3. 提取干声；4. Whisper转录；5. 文本纠错；6. 标点恢复。
  支持自定义输出目录、从任意步骤开始。
  
  常见触发口语：
  - “帮我复制这个抖音视频的内容”
  - “把这个B站短视频转成文字”
  - “一键提取这个视频的干声和转录”
  - “短视频内容复制工作流”
  - “把视频做成文本稿”
  - “抖音视频转文字带标点”
  - “端到端处理这个短视频”
  - “从下载到文本一键搞定这个视频”
  - “replicate 这个视频链接”
  
  只处理短视频内容复制全流程或子流程，其他无关任务不触发。
metadata:
  openclaw:
    requires:
      bins:
        - python
    user-invocable: true
---

# Short Video Content Replicator

## Overview
这是一个严格顺序执行的短视频内容复制复合 Skill。  
它会按指定的 6 步，依次调用各原子 Skill 的 CLI 脚本，完成从视频下载到最终高质量带标点文本的完整流程。

支持从任意步骤开始（断点续跑）和自定义各步骤输出目录。

## 触发时机（Triggers）
- 用户提供抖音/B站视频URL，想一键完成下载→干声提取→转录→文本优化的全流程。
- 用户有本地视频/MP3/音频/文本文件，想从中间步骤继续处理。
- 用户说“一键”“端到端”“复制内容”“转成文字稿”“提取干声转录”等意图。
- 支持批量或单个视频处理。

## Workflow Decision Tree
**输入支持**：
- 视频URL → 从 Step 1 开始
- 本地视频目录 → 从 Step 2 开始
- MP3 目录 → 从 Step 3 开始
- .wav 目录 → 从 Step 4 开始
- .txt 目录 → 从 Step 5 或 Step 6 开始

**严格执行顺序**（默认全流程）：
1. 视频下载（link-resolver-engine）
2. MP4 → MP3（mp4-to-mp3-extractor）
3. 人声分离（purevocals-uvr-automator）
4. Whisper 转录（turbo-whisper-local-stt）
5. 文本纠错（llm-text-correct）
6. 标点恢复（funasr-punctuation-restore）

## Step 1: 视频下载
使用 `link-resolver-engine`  
命令：`python ./skills/link-resolver-engine/scripts/video_snapper.py -u "<视频链接>" [-p "<文件名前缀>"] [-d "<下载目录>"] [-f "<格式代码>"]`

## Step 2: MP4 转 MP3
使用 `mp4-to-mp3-extractor`  
命令：`python ./skills/mp4-to-mp3-extractor/scripts/extract.py "<源目录>" "[目标目录]"`

## Step 3: 人声分离（提取干声）
使用 `purevocals-uvr-automator`  
命令：`python ./skills/purevocals-uvr-automator/scripts/purevocals.py "<输入路径>" ["<输出目录>"] [--model <模型名>] [--window_size <数值>] [--aggression <数值>] [--chunk_duration <秒数>] [--sample_mode]`

## Step 4: 本地转录
使用 `turbo-whisper-local-stt`  
命令：`python ./skills/turbo-whisper-local-stt/scripts/transcribe.py  --audio_path "<音频路径>" [--output_dir "<输出目录>"] [--language <zh/en>] [--model_path "<模型路径>"] [--output <json/text>] [--beam_size 5] [--separator " "]`

## Step 5: 文本纠错
使用 `llm-text-correct`  
命令：`python ./skills/llm-text-correct/scripts/correct_text.py ["<输入文本/路径>"] [--refine] [--model-path "<模型路径>"]`

## Step 6: 标点恢复
使用 `funasr-punctuation-restore`  
命令：`python ./skills/funasr-punctuation-restore/scripts/punctuation_restore.py (--text "<文本内容>" | --file "<文件路径>" | --dir "<目录路径>")`

## Usage Examples
```bash
# 1. 最常用：输入URL，一键完整6步
replicate https://v.douyin.com/xxxxxx/ --output ./my_project/

# 2. 处理本地视频文件夹（从Step 2开始）
replicate ./videos/ --start-from step2 --output ./my_project/

# 3. 自定义输出目录 + 参数
replicate https://v.douyin.com/xxxxxx/ \
  --videos-dir ./videos \
  --mp3-dir ./audio/mp3 \
  --vocals-dir ./audio/vocals \
  --final-dir ./result/text