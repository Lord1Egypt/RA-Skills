---
name: qwen-video-generator
version: 1.0.2
description: 阿里云百炼文生视频工具。使用 wan2.2-t2v-plus 模型将文本描述生成视频。**当以下情况时使用此 Skill**：(1) 用户需要根据文字描述生成视频 (2) 用户提到"文生视频"、"生成视频"、"AI视频"、"text to video" (3) 需要创建短视频内容 (4) 需要可视化场景描述。支持自定义分辨率、时长(1-15秒)、自动prompt扩展。
license: MIT
---

# Qwen Video Generator - 百炼文生视频

将文本描述转换为视频内容。

## 环境变量配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY_VIDEO` | 视频专用 API Key (优先) | - |
| `DASHSCOPE_API_KEY` | 通用 API Key (备用) | - |
| `VIDEO_OUTPUT_DIR` | 视频输出目录 | workspace/videos/ |
| `VIDEO_OUTPUT_SIZE` | 分辨率: 480=832×480, 1080=1920×1080 | 480 |
| `VIDEO_OUTPUT_LENGTH` | 视频秒数 (1-15) | 5 |

**推荐配置 (~/.zshenv):**
```bash
export DASHSCOPE_API_KEY_VIDEO=your_api_key
export VIDEO_OUTPUT_DIR=/path/to/videos
export VIDEO_OUTPUT_SIZE=1080
export VIDEO_OUTPUT_LENGTH=5
```

## 快速开始

```bash
# 使用环境变量配置，简洁调用
python3 scripts/generate_video.py --prompt "你的视频描述"
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt, -p` | 视频描述文本 (必填) | - |
| `--size, -s` | 分辨率: 480/1080 或完整格式 | 环境变量 |
| `--length, -l` | 视频时长 (1-15秒) | 环境变量 |
| `--model, -m` | 模型名称 | wan2.2-t2v-plus |
| `--no-prompt-extend` | 禁用prompt自动扩展 | False |
| `--timeout, -t` | 最大等待秒数 | 600 |

## 使用示例

```bash
# 基础用法 (使用环境变量)
python3 scripts/generate_video.py --prompt "一只猫在草地上奔跑"

# 命令行覆盖分辨率和时长
python3 scripts/generate_video.py \
  --prompt "日落时分的海滩" \
  --size 1080 \
  --length 10

# 详细场景描述
python3 scripts/generate_video.py --prompt "低对比度，复古70年代地铁站，街头音乐家穿旧式夹克弹吉他，通勤者匆匆走过，镜头慢慢向右移动"
```

## 支持的分辨率

| 简写 | 完整格式 | 说明 |
|------|----------|------|
| 480 | 832×480 | 默认，适合快速预览 |
| 1080 | 1920×1080 | 高清，推荐使用 |

其他支持: 1080×1920, 1440×1440, 1632×1248, 1248×1632, 480×832, 624×624

## Prompt 编写建议

1. **描述场景**: 包含地点、时间、氛围
2. **主体动作**: 清晰描述主体在做什么
3. **视觉风格**: 光线、色彩、质感
4. **镜头运动**: 推拉摇移等
5. **细节元素**: 背景中的物品、人物

## 输出

- 输出目录: `$VIDEO_OUTPUT_DIR` 或 `workspace/videos/`
- 文件命名: `video_YYYYMMDD_HHMMSS_hash.mp4`
- 最后一行输出 `VIDEO_PATH:完整路径` 供程序解析
