---
name: video-viral-replicate
description: "视频爆款拆解与二创文案生成。输入一个短视频（抖音/B站/小红书/视频号等），通过 ffmpeg 抽取音轨与关键帧、whisper 转录带时间戳文案、OCR 提取画面字幕，按时间戳对齐成视听时间线，再基于拆解结果生成二创爆款文案。适用于：拆解爆款视频结构、仿写爆款文案、视频拆条分析、视听内容理解、二创脚本生成。当用户提到拆解视频、二创、爆款文案、视频视听分析、仿写爆款、视频拆条、分析这个视频为什么火时触发。"
agent_created: true
---

# Video Viral Replicate - 视频爆款拆解与二创文案生成

## Overview

将一个爆款短视频拆解为「画面 + 文案 + 字幕」对齐的视听时间线，再基于拆解结果提炼爆款公式并生成可落地的二创文案。核心管道由 `scripts/pipeline.py` 完成（ffmpeg + faster-whisper + OCR + yt-dlp），文案生成部分由对话中的 LLM 基于 `references/prompt_templates.md` 的模板完成。

**支持链接直传**：除本地视频文件外，直接传入抖音/B站/小红书/视频号/YouTube 等平台的分享链接，pipeline 会用 yt-dlp 自动下载后再拆解，无需手动下载视频。

**零配置设计**：首次运行自动建 venv、装依赖、提供 ffmpeg 二进制，用户装完 skill 直接跑即可，无需手动配环境。

## When to use

触发场景：
- 用户给出视频文件路径，要求"拆解这个视频""分析它为什么火""仿写一版文案"
- 需要把视频的视听内容结构化（画面、台词、字幕按时间轴对齐）
- 需要基于爆款视频产出二创文案、改写脚本、提炼爆款公式

不适用：纯音频转录（直接用 whisper 即可）、纯视频剪辑（用剪辑工具）、需要精确到帧的视觉检测（用专用 CV 模型）。

## 前置条件

- **Python 3.8+**：用户系统已有即可（WorkBuddy 自带 Python 3.13，满足）
- **无需系统 ffmpeg**：pipeline 用 `imageio-ffmpeg` 包自带的 ffmpeg 二进制，pip 装完就有
- **无需手动装 Python 包**：首次运行自动建隔离 venv 并装依赖
- **首次下载体积**：whisper 模型约 1.5GB + easyocr 模型约 100MB，走 HuggingFace/网络，首次下载后走本地缓存
- **磁盘空间**：venv + 依赖 + 模型缓存合计约 3-4GB

## 工作流程

### Step 1: 运行 pipeline 拆解视频（首次自动配置环境）

核心命令——用任意可用的 Python 启动，首次运行会自动切换到隔离 venv：
```bash
"C:/Users/qjw/.workbuddy/binaries/python/versions/3.13.12/python.exe" "{SKILL_DIR}/scripts/pipeline.py" \
  --input {VIDEO_PATH} \
  --workdir {OUTPUT_DIR} \
  [--model medium] \
  [--device auto] \
  [--ocr] \
  [--scene-threshold 0.3] \
  [--fps 0]
```

其中 `{SKILL_DIR}` 为本 skill 所在目录（通常为 `C:/Users/qjw/.workbuddy/skills/video-viral-replicate`）。

**首次运行会发生什么**（全自动，用户无需干预）：
1. 在 skill 目录下建隔离 venv：`{SKILL_DIR}/.venv/`
2. 升级 pip，用清华源装依赖（faster-whisper + easyocr + imageio-ffmpeg）
3. 自动重启脚本，切到 venv 的 python 继续
4. 下载 whisper 模型（首次约 1.5GB，之后走缓存）
5. 正常执行拆解流程

耗时：首次约 5-10 分钟（含下载），之后每次几十秒到几分钟（取决于视频长度与有无 GPU）。

参数说明：
- `--input`：视频文件路径**或分享链接**（必填）。支持抖音/B站/小红书/视频号/YouTube/TikTok 等，链接自动用 yt-dlp 下载后再拆解
- `--workdir`：工作目录，存放中间产物与最终 JSON（必填）
- `--model`：whisper 模型大小，可选 `tiny/base/small/medium/large-v3`，默认 `medium`（平衡速度与准确度）
- `--device`：`auto/cpu/cuda`，默认 `auto`（自动检测 GPU）
- `--ocr`：开启画面字幕 OCR（默认开启，加 `--no-ocr` 关闭）
- `--scene-threshold`：场景切换检测阈值 0-1，默认 0.3；越高抽帧越稀疏
- `--fps`：固定抽帧帧率（如 `1` 表示每秒一帧）；设为 0 则只用场景切换检测，默认 0

脚本执行后输出 `{WORKDIR}/analysis.json`，结构见下方"输出格式"。

### Step 2: 基于拆解 JSON 生成二创文案

读取 `{WORKDIR}/analysis.json`，按 `references/prompt_templates.md` 中的流程生成二创文案：

1. 加载 `references/prompt_templates.md` 到上下文
2. 读取 analysis.json，提取：时间线、全文文案、关键画面描述
3. 按"爆款公式提炼"模板分析原视频结构（钩子、冲突、节奏、CTA）
4. 按"二创文案生成"模板产出 3 个版本的二创文案（不同角度/风格）

详细 prompt 模板见 `references/prompt_templates.md`。

## 输出格式

`analysis.json` 结构：

```json
{
  "video": "path/to/video.mp4",
  "duration": 60.5,
  "model": "medium",
  "device": "cpu",
  "language": "zh",
  "timeline": [
    {
      "start": 0.0,
      "end": 3.2,
      "narration": "你以为这就结束了？",
      "subtitle": "你以为这就结束了？",
      "frame": "frames/frame_0001.jpg",
      "frame_time": 0.0
    }
  ],
  "full_text": "完整转录文本...",
  "segments_count": 15,
  "frames_count": 8
}
```

字段说明：
- `timeline`：按时间排序的视听片段，每个片段包含该时间段的旁白（whisper）、字幕（OCR）、代表帧路径
- `full_text`：whisper 转录的完整文本，便于整体理解
- `frame`：相对于 workdir 的路径，可直接打开查看画面

中间产物（在 workdir 下）：
- `audio.wav`：16kHz 单声道音频
- `frames/frame_XXXX.jpg`：关键帧图片

## ffmpeg 策略

pipeline 按以下优先级查找 ffmpeg，无需用户配置：
1. **imageio-ffmpeg 包自带的二进制**（推荐，pip 装完即用，零系统配置）
2. **系统 PATH 中的 ffmpeg**（回退，适合已装 ffmpeg 的用户）

这样无论用户电脑有没有装 ffmpeg，skill 都能跑。

## 常见问题与调优

**whisper 幻觉（纯音乐段凭空生成文字）**：pipeline 已集成 silero-vad 做静音过滤。如仍有幻觉，将 `--model` 降为 `small`。

**长视频显存不足**：whisper 对超长视频显存敏感。若 OOM，设 `--device cpu` 或降 `--model`。

**OCR 漏抓字幕**：短视频字幕样式多变。若漏抓率高，设 `--fps 2` 增加抽帧密度。

**抽帧太少**：场景切换检测对缓慢变化的画面不敏感。设 `--fps 1`（每秒一帧）兜底，或降低 `--scene-threshold` 到 0.2。

**没有 GPU**：`--device auto` 会自动回退 CPU。`large-v3` 在 CPU 上极慢，无 GPU 时建议 `--model small`。

**首次配置失败（网络问题）**：pip 源默认走清华镜像。若仍失败，可手动跑：
```bash
"{SKILL_DIR}/.venv/Scripts/python" -m pip install -r "{SKILL_DIR}/requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 资源说明

- `scripts/pipeline.py`：视听拆解主脚本，首次运行自动配置环境
- `references/prompt_templates.md`：二创爆款文案的 prompt 模板（爆款公式提炼 + 文案生成）
- `requirements.txt`：Python 依赖（faster-whisper、easyocr、imageio-ffmpeg）
