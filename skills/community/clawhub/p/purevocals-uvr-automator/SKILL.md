---
name: PureVocals-UVR-Automator
description: |-
  当用户想要**一键批量从音频文件中提取超干净纯人声（干声 / Vocals Only）**、去除伴奏/背景音乐时，自动调用此技能。
  一键音频人声分离工具。专门从音频文件（.mp3/.wav/.flac等）中提取超干净干声（Acapella）或去除背景音制作伴奏。

  核心用途：支持单个音频文件或整个文件夹批量处理（.mp3/.wav/.flac 等格式），输出高质量无杂音干声，自动在输入同级创建 [输入文件夹]_vocals 文件夹，完美保留原目录结构。

  高频触发场景包括：
  - 翻唱练习、翻唱视频制作、B站/抖音/小红书演唱素材清洗
  - 卡拉OK 伴奏制作（只保留人声）
  - 音乐制作中的人声分离（vocal isolation / stem separation）
  - 音频素材清洗、原音轨提取、去背景音处理
  - 翻唱素材制作、卡拉OK伴奏生成、音频后期清洗。

  用户常用自然语言表述：
  “帮我提取干声”“把这首歌的伴奏去掉，只留清唱”“批量分离文件夹里的所有人声”“做翻唱要纯人声”“卡拉OK 干声提取”“vocal remover”“UVR 人声分离”“去除伴奏”“音频人声隔离”“stem 分离 vocals”等。

  支持顶级 UVR 模型，默认推荐速度最快且干净度最高的 shibing624-chinese-kenlm-klm，也支持卡拉OK 专用模型。自动检测 GPU（CUDA 加速）或 CPU，自动创建并管理虚拟环境，无需用户手动配置。
metadata:
  openclaw:
    requires:
      bins:
        - python
  user-invocable: true
---

# PureVocals-UVR-Automator

**功能概述**：一键将带伴奏的音频文件批量转换为超干净的纯人声（Vocals Only）。专为翻唱、卡拉OK、音乐素材清洗等场景设计，输出质量高、速度快、操作零门槛。

## 支持的模型（推荐顺序）
1. **shibing624-chinese-kenlm-klm** —— 默认推荐（速度最快 + 干净度最高，适合中文歌曲）
2. **6_HP_Karaoke-UVR.pth** —— 高质量卡拉OK 模式（你原来的常用设置）
3. **UVR-MDX-NET-Karaoke_2.onnx** —— 极致速度，适合超大批量处理

## 执行步骤
1. **输入解析**：支持单个音频文件路径，或整个文件夹路径（会递归处理所有支持格式）。
2. **输出位置**：若未指定输出目录，默认在输入路径同级自动创建 `[输入文件夹名]_vocals` 文件夹，保持原文件夹结构不变。
3. **启动命令**（Agent 会自动选择优先级）：
   ```bash
   (python3 scripts/purevocals.py "<输入路径>" ["<输出目录>"] [--model <模型名>] [--window_size <数值>] [--aggression <数值>] [--chunk_duration <秒数>] [--sample_mode]) || (python scripts/purevocals.py "<输入路径>" ["<输出目录>"] [--model <模型名>] [--window_size <数值>] [--aggression <数值>] [--chunk_duration <秒数>] [--sample_mode])