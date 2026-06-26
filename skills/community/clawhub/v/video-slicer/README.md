# Video Slicer — 视频智能切片工具 用户手册

> **版本**: 1.2.0 | **作者**: Bill (米赋教育) | **兼容模型**: glm-5v-turbo / GPT-4o / Claude 3.5 Sonnet
>
> **ClawHub**: https://clawhub.ai/bill-mifu/video-slicer
>
> **许可证**: MIT-0

---

## 目录

1. [简介](#1-简介)
2. [快速开始](#2-快速开始)
3. [安装与环境配置](#3-安装与环境配置)
4. [完整工作流详解](#4-完整工作流详解)
5. [一键脚本使用指南](#5-一键脚本使用指南)
6. [API 参考](#6-api-参考)
7. [进阶技巧](#7-进阶技巧)
8. [常见问题 FAQ](#8-常见问题-faq)
9. [版本历史](#9-版本历史)
10. [贡献指南](#10-贡献指南)

---

## 1. 简介

### 1.1 这个 Skill 做什么？

**Video Slicer** 是一个面向 AI Agent 的视频智能切割技能。它能从数小时的长视频中，精准定位目标演讲/段落，自动分析内容结构，并按主题切割出适合在抖音、B站、小红书等平台发布的独立短视频（**每个 3-5 分钟，最长不超过 8 分钟**）。

### 1.2 核心技术栈

| 组件 | 技术选型 | 理由 |
|------|----------|------|
| 视频处理引擎 | **ffmpeg** | 业界标准，支持几乎所有格式 |
| 语音转文字 | **OpenAI Whisper (local)** | 本地运行，隐私安全，中文效果优秀 |
| GPU 加速 | **Apple MPS** (macOS) | Apple Silicon 原生加速，速度提升 3-5x |
| 繁简转换 | **OpenCC** | 自动将 Whisper 输出的繁体转为简体 |
| AI 模型推荐 | **GLM-5V-Turbo** | 多模态理解能力强，适合视觉+文本联合分析 |

### 1.3 典型应用场景

| 场景 | 示例 | 切片数量 |
|------|------|----------|
| 学术会议精剪 | 从 3h 会议中提取某教授的核心发言 | 4-8 个 |
| 课程视频分章 | 将 2h 录播课拆为知识点片段 | 6-12 个 |
| 播客/访谈分段 | 按话题切分长访谈 | 5-10 个 |
| 直播回放精华 | 提取直播中的高光时刻 | 3-6 个 |
| 个人录制剪辑 | 自己录制的教学/分享视频 | 自定义 |

---

## 2. 快速开始

### 2.1 最快上手（3 步）

```bash
# Step 1: 安装依赖（一次性）
pip install openai-whisper opencc-python-reimplemented torch
brew install ffmpeg   # macOS

# Step 2: 运行一键脚本
python3 scripts/video_slicer.py ~/Downloads/你的视频.mp4 ./输出目录

# Step 3: 查看采样帧 → 手动指定时间范围 → 获得切片结果
```

### 2.2 Agent 调用示例

当你对 AI Agent 说以下任一指令时，此 Skill 会被触发：

```
"帮我把这个视频切成短视频"
"从会议录像中提取张三的发言"
"把这个3小时的讲座按主题切一下"
"帮我做自媒体用的视频切片"
```

Agent 会自动执行完整的 4 阶段工作流。

---

## 3. 安装与环境配置

### 3.1 系统要求

| 要求 | 最低配置 | 推荐配置 |
|------|----------|----------|
| 操作系统 | macOS 12+ / Linux / Windows WSL2 | macOS 14+ (Apple Silicon) |
| Python | 3.10+ | 3.12+ |
| 内存 | 8 GB | 16 GB+ |
| 磁盘空间 | 2 GB 可用 | 10 GB+ (Whisper 模型缓存) |
| GPU | 无（CPU 可用） | Apple M1/M2/M3 (MPS) 或 NVIDIA CUDA |

### 3.2 依赖安装

#### macOS（推荐）

```bash
# Homebrew 安装 ffmpeg
brew install ffmpeg

# pip 安装 Python 依赖
pip3 install openai-whisper opencc-python-reimplemented torch torchvision

# 验证安装
ffmpeg -version        # 应显示 >= 5.0 版本
python3 -c "import whisper; print(whisper.__version__)"  # 应显示版本号
python3 -c "from opencc import OpenCC; print('OK')"       # 应打印 OK
```

#### Linux (Ubuntu/Debian)

```bash
# apt 安装 ffmpeg
sudo apt update && sudo apt install -y ffmpeg

# pip 安装 Python 依赖
pip3 install openai-whisper opencc-python-reimplemented torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### Windows (WSL2)

```bash
# 在 WSL2 中执行与 Linux 相同的操作
sudo apt update && sudo apt install -y ffmpeg
pip3 install openai-whisper opencc-python-reimplemented torch torchvision
```

### 3.3 Whisper 模型首次下载

首次运行时会自动下载模型（约 139MB for base）：

```
模型下载位置: ~/.cache/whisper/
模型大小:
  tiny    ~39 MB    (最快, 质量低)
  base    ~139 MB   (推荐默认)
  small   ~461 MB   (质量较好)
  medium  ~1.5 GB   (质量高, 很慢)
```

如需手动下载或更换路径：

```python
import whisper
model = whisper.load_model("base", download_root="/自定义/路径")
```

---

## 4. 完整工作流详解

### Phase 1: 快速预览 — 定位目标区域

**目标：在几分钟内找到视频中目标内容的起止时间范围**

#### Step 1: 获取视频元数据

```bash
ffmpeg -i your_video.mp4 2>&1 | grep -E "Duration|Stream"
```

期望输出：
```
Duration: 03:27:15.42  # 时长 3小时27分钟
Stream #0:0: Video: hevc ... 1024x576  # HEVC编码, 分辨率
Stream #0:1: Audio: aac ... 44100 Hz  # 音频信息
```

Agent 需要记录的关键信息：
- **总时长** → 决定采样策略
- **编码格式** → 决定是否需要转码（HEVC 需转为 H.264）
- **分辨率** → 影响关键帧可读性

#### Step 2: 粗粒度关键帧采样

每 **5 分钟**采一帧，快速浏览整体结构：

```bash
VIDEO="your_video.mp4"
OUT_DIR="./frames"
mkdir -p "$OUT_DIR"

# 计算采样点（每5分钟一个）
TOTAL_SEC=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO" | cut -d. -f1)

for t in $(seq 0 5 $(( TOTAL_SEC / 60 * 60 ))); do
  h=$((t / 3600))
  m=$(((t % 3600) / 60))
  s=$((t % 60))
  ts=$(printf "%02d:%02d:%02d" $h $m $s)
  ffmpeg -y -ss "$ts" -i "$VIDEO" -frames:v 1 -q:v 2 "${OUT_DIR}/frame_${ts//:/_}.jpg" 2>/dev/null &
done
wait
echo "[OK] 采样完成，共 $(ls ${OUT_DIR}/*.jpg | wc -l) 帧"
```

> **并行技巧**: 使用 `&` 和 `wait` 并行提取，速度提升 3-5 倍。

#### Step 3: Agent 视觉检查关键帧

AI Agent 使用视觉能力（Read 工具读取图片）逐帧分析：

```
frame_00_00_00.jpg → 开场画面，可能是主持人/赞助商
frame_00_05_00.jpg → 第一位演讲者开始
frame_00_40_00.jpg → ✅ 发现目标演讲者（陈丽教授）！
frame_01_07_00.jpg → 目标演讲者仍在台上
frame_01_10_00.jpg → 已切换到下一位演讲者
```

**结论**: 目标区间 ≈ `00:40:00` ~ `01:07:00`

### Phase 2: 精细定位 — 精确到秒级

#### Step 4: 过渡区间精细采样

在粗定位的边界前后每 **2 分钟**采一帧，找到精确的起止点：

```bash
VIDEO="your_video.mp4"

# 起始边界精细搜索 (35-45分钟区间)
for m in 36 38 40 42 44; do
  ffmpeg -y -ss "00:${m}:00" -i "$VIDEO" -frames:v 1 -q:v 2 "./frames/fine_start_${m}.jpg" 2>/dev/null
done

# 结束边界精细搜索 (1:05-1:10 区间)
for m in 65 67 69; do
  ffmpeg -y -ss "01:${m}:00" -i "$VIDEO" -frames:v 1 -q:v 2 "./frames/fine_end_${m}.jpg" 2>/dev/null
done
```

#### Step 5: 音频提取 + Whisper 转写

**这是整个工作流最核心的步骤。**

##### 为什么先提取音频再转写？

| 方式 | 27分钟音频处理时间 | 内存占用 | 稳定性 |
|------|-------------------|----------|--------|
| 直接喂视频给 Whisper | ~15-20 min | 高 (~4GB) | 容易 OOM |
| **先提取音频再转写** | **~2-3 min** | **低 (~500MB)** | **稳定** |

##### 执行步骤

```python
"""
transcribe_target_segment.py
功能：提取目标区间的音频并调用 Whisper 转写
"""

import os, sys, json, ssl, certifi, subprocess
from datetime import timedelta

# ================== 配置 ==================
VIDEO_PATH = "/path/to/your_video.mp4"
OUTPUT_DIR = "./transcript"
START_TIME = "00:40:00"      # 目标起始时间
END_TIME = "01:07:00"        # 目标结束时间
WHISPER_MODEL = "base"       # tiny/base/small/medium
INITIAL_PROMPT = "北京师范大学陈丽教授，未来学习中心，教育数字化转型"
# =========================================

def time_to_seconds(time_str):
    """将 HH:MM:SS 格式转换为秒数"""
    parts = time_str.split(":")
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

def main():
    # SSL 修复（macOS 必需）
    ssl._create_default_https_context = lambda: ssl.create_default_context(
        cafile=certifi.where()
    )
    os.environ['SSL_CERT_FILE'] = certifi.where()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # === Step A: 提取音频 ===
    audio_path = os.path.join(OUTPUT_DIR, "segment.aac")
    start_sec = time_to_seconds(START_TIME)
    end_sec = time_to_seconds(END_TIME)
    duration = end_sec - start_sec

    print(f"[Step 1/3] 提取音频: {START_TIME} ~ {END_TIME} ({duration}秒)")
    result = subprocess.run([
        "ffmpeg", "-y",
        "-i", VIDEO_PATH,
        "-ss", START_TIME,
        "-to", END_TIME,
        "-vn", "-acodec", "copy",
        audio_path
    ], capture_output=True, text=True)

    if not os.path.exists(audio_path):
        print(f"[ERROR] 音频提取失败: {result.stderr}")
        return None

    audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"         音频文件大小: {audio_size_mb:.1f} MB")

    # === Step B: Whisper 转写 ===
    import torch
    try:
        import whisper
    except ImportError:
        print("[ERROR] 未安装 whisper: pip install openai-whisper")
        return None

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"[Step 2/3] 加载 Whisper 模型 ({WHISPER_MODEL}, device={device})...")
    model = whisper.load_model(WHISPER_MODEL, device=device)

    print(f"[Step 3/3] 开始转写...")
    result = model.transcribe(
        audio_path,
        language="zh",
        verbose=False,
        initial_prompt=INITIAL_PROMPT,
        word_timestamps=True  # 启用词级时间戳（更精确）
    )

    # 繁简转换 + 时间戳校正
    from opencc import OpenCC
    cc = OpenCC('t2s')

    segments = []
    for seg in result["segments"]:
        segments.append({
            "id": len(segments) + 1,
            "start": round(seg["start"] + start_sec, 1),
            "end": round(seg["end"] + start_sec, 1),
            "text": cc.convert(seg["text"].strip()),
            "logprob": round(seg.get("avg_logprob", 0), 2)
        })

    # === 保存结果 ===
    json_path = os.path.join(OUTPUT_DIR, "speech.json")
    txt_path = os.path.join(OUTPUT_DIR, "speech.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "source_video": VIDEO_PATH,
                "audio_segment": f"{START_TIME} ~ {END_TIME}",
                "model": WHISPER_MODEL,
                "device": device,
                "total_segments": len(segments)
            },
            "segments": segments
        }, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        for seg in segments:
            sh, sm = divmod(int(seg["start"]), 60)
            eh, em = divmod(int(seg["end"]), 60)
            f.write(f"[{sh:02d}:{sm:02d} -> {eh:02d}:{em:02d}] {seg['text']}\n")

    total_dur = segments[-1]["end"] - segments[0]["start"]
    print(f"\n{'='*50}")
    print(f"[OK] 转写完成!")
    print(f"     片段数: {len(segments)}")
    print(f"     总时长: {int(total_dur // 60)}分{int(total_dur % 60)}秒")
    print(f"     JSON:   {json_path}")
    print(f"     TXT:    {txt_path}")
    print(f"{'='*50}")

    return json_path


if __name__ == "__main__":
    main()
```

运行方式：
```bash
python3 transcribe_target_segment.py
```

### Phase 3: 内容分析与切片规划

**这一步由 AI Agent 的智能分析能力完成。**

Agent 读取 `speech.json` 中的带时间戳文本后，需要：

1. **语义分段**：识别自然的话题转折点
2. **主题标注**：为每段提炼核心主题
3. **时长控制**：确保每段 3-8 分钟
4. **Hook 设计**：识别每段开头是否有吸引力
5. **方案输出**：生成结构化的切割计划

#### Agent 分析流程（伪代码）

```
输入: speech.json (357个带时间戳的句子片段)

PROCESS:
  1. 全文阅读 → 识别核心论点架构
  2. 按话题聚类 → 划分 4-6 个主题块
  3. 为每个主题块确定起止句号
  4. 计算每个块的时长
  5. 调整边界使时长落在 3-8min 范围内
  6. 为每个块拟定标题和 Hook

输出: clips_plan.json + clips_plan.md
```

#### 切片计划模板

```json
{
  "video_info": {
    "source": "~/Downloads/中关村「教育+科技」创新周_original.mp4",
    "total_duration": "03:27:15",
    "speaker": "陈丽教授 (北京师范大学)",
    "target_range": "00:40:00 - 01:07:00"
  },
  "clips": [
    {
      "clip_id": 1,
      "title": "教育为什么必须变",
      "theme": "开场震撼篇",
      "start": "00:40:00",
      "end": "00:45:12",
      "duration_sec": 312,
      "hook": "工业时代的教育体系已经过时了...",
      "key_points": ["学校不再是唯一的知识来源", "互联网重构知识传递方式"],
      "sentence_start_idx": 0,
      "sentence_end_idx": 45
    },
    {
      "clip_id": 2,
      "title": "未来学习中心到底是什么",
      "theme": "核心概念篇",
      "start": "00:45:08",
      "end": "00:50:43",
      "duration_sec": 335,
      "hook": "未来的学校会变成什么样？",
      "key_points": ["学习中心的三大特征", "从教到学的范式转移"],
      "sentence_start_idx": 43,
      "sentence_end_idx": 98
    }
  ],
  "summary": {
    "total_clips": 4,
    "total_duration_min": 19.3,
    "average_clip_min": 4.8
  }
}
```

### Phase 4: 执行切割

#### 单段切割命令

```bash
ffmpeg -y \
  -ss 00:40:00 \
  -to 00:45:12 \
  -i "/path/to/source.mp4" \
  -c:v libx264 \
  -preset fast \
  -crf 18 \
  -c:a aac \
  -b:a 128k \
  -movflags +faststart \
  "./output/clip1_教育为什么必须变.mp4"
```

> `-movflags +faststart` 让视频可以在网上边下边播（重要！）

#### 批量切割脚本

```bash
#!/bin/bash
# batch_cut.sh — 批量切割脚本
# 用法: bash batch_cut.sh <clips_plan.json>

PLAN_FILE="$1"
VIDEO="$HOME/Downloads/source_video.mp4"
OUT="./output"
mkdir -p "$OUT"

# 用 python 解析 JSON 并逐行输出切割参数
python3 << 'PYEOF'
import json, sys
plan = json.load(open(sys.argv[1]))
for c in plan["clips"]:
    print(f"{c['start']}|{c['end']}|clip{c['clip_id']}_{c['title']}.mp4")
PYEOF
"$PLAN_FILE" | while IFS='|' read -r start end filename; do
  echo ">>> 切割: $filename ($start -> $end)"
  ffmpeg -y -ss "$start" -to "$end" -i "$VIDEO" \
    -c:v libx264 -preset fast -crf 18 \
    -c:a aac -b:a 128k -movflags +faststart \
    "${OUT}/${filename}" 2>/dev/null
done

echo ""
echo "=== 切割完成 ==="
ls -lh "$OUT"/*.mp4
```

---

## 5. 一键脚本使用指南

Skill 附带的 `scripts/video_slicer.py` 提供基础自动化功能。

### 5.1 基本用法

```bash
# 最简单用法
python3 scripts/video_slicer.py <视频路径> [输出目录]

# 示例
python3 scripts/video_slicer.py ~/Downloads/lecture.mp4 ./my_output
```

### 5.2 脚本执行流程

```
启动
 ↓
[1] 获取视频信息（时长、分辨率）
 ↓
[2] 均匀采样关键帧（每5分钟一帧）→ frames/
 ↓
[3] 判断视频长度:
      ├─ ≤30min → 自动全量 Whisper 转写
      └─ >30min → 提示手动指定范围
 ↓
[4] 输出结构化数据
 ↓
完成 → 输出目录已准备就绪
```

### 5.3 在代码中导入使用

```python
from video_slicer import get_video_info, sample_frames, transcribe_segment, cut_clips

# 获取视频信息
info = get_video_info("~/Downloads/video.mp4")
print(info)  # {"duration": 12345, "path": "..."}

# 采样关键帧
frames_dir = sample_frames("~/Downloads/video.mp4", "./output", info["duration"])

# 转写指定段落
json_path = transcribe_segment(
    "~/Downloads/video.mp4",
    "./output",
    start_sec=2400,   # 00:40:00
    end_sec=4020      # 01:07:00
)

# 执行切割
cut_clips(
    "~/Downloads/video.mp4",
    "./output",
    clips_plan=[
        {"start": "00:40:00", "end": "00:45:00", "title": "开场震撼"},
        {"start": "00:45:00", "end": "00:50:30", "title": "核心概念"},
    ]
)
```

### 5.4 配置项说明

在 `video_slicer.py` 顶部可调整的常量：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SAMPLE_INTERVAL` | 300 | 关键帧采样间隔（秒），默认5分钟 |
| `MIN_CLIP` | 180 | 最短切片时长（秒），默认3分钟 |
| `MAX_CLIP` | 480 | 最长切片时长（秒），默认8分钟 |
| `WHISPER_MODEL` | `"base"` | Whisper 模型选择 |

---

## 6. API 参考

### 6.1 `get_video_info(path)` → dict

获取视频基本信息。

**参数**:
- `path` (str): 视频文件绝对路径

**返回值**:
```python
{
    "duration": 12345,     # 总时长（秒）
    "path": "/path/to/file.mp4"
}
```
**异常**: 视频无法读取时抛出 Exception

### 6.2 `sample_frames(video_path, out_dir, duration)` → str

均匀采样视频关键帧。

**参数**:
- `video_path` (str): 视频路径
- `out_dir` (str): 输出目录
- `duration` (int/float): 视频总时长（秒）

**返回值**: `str` — 帧保存目录路径

**输出**: 在 `{out_dir}/frames/` 下生成 `frame_HH-MM-SS.jpg` 文件

### 6.3 `transcribe_segment(video_path, out_dir, start_sec, end_sec)` → str | None

提取音频片段并执行 Whisper 转写。

**参数**:
- `video_path` (str): 视频路径
- `out_dir` (str): 输出目录
- `start_sec` (int): 起始时间（秒）
- `end_sec` (int): 结束时间（秒）

**返回值**: `str` — JSON 文件路径；失败时返回 `None`

**输出文件**:
- `{out_dir}/transcript/segment.aac` — 提取的音频
- `{out_dir}/transcript/speech.json` — 结构化转写结果
- `{out_dir}/transcript/speech.txt` — 纯文本格式

### 6.4 `cut_clips(video_path, out_dir, clips_plan)` → list[dict]

按计划批量切割视频。

**参数**:
- `video_path` (str): 源视频路径
- `out_dir` (str): 输出目录
- `clips_plan` (list[dict]): 切片计划列表，每项包含:
  - `"start"` (str): 起始时间 `"HH:MM:SS"`
  - `"end"` (str): 结束时间 `"HH:MM:SS"`
  - `"title"` (str): 切片标题

**返回值**: `list[dict]` — 每项包含 `"file"` 和 `"size_mb"`

---

## 7. 进阶技巧

### 7.1 处理超长视频（> 5 小时）

对于超长视频，建议采用**分层策略**：

1. 先用 **10 分钟间隔** 采样（而非 5 分钟）
2. 只对确认的目标区间进行精细采样和转写
3. 如果目标区间仍 > 30min，拆分为多个子区间分别转写

### 7.2 提高 Whisper 中文准确率

在 `initial_prompt` 参数中提供领域关键词：

```python
# 教育类视频
initial_prompt = "北京师范大学, 未来学习中心, 教育数字化, 知识服务, 互联网+教育"

# 医疗类视频
initial_prompt = "临床诊断, 病例讨论, 手术方案, 药物治疗, 预后评估"

# 法律类视频
initial_prompt = "民法典, 合同纠纷, 证据规则, 诉讼程序, 司法解释"
```

### 7.3 批量处理多段视频

```bash
# 对文件夹中所有 mp4 执行相同操作
for video in ~/Videos/*.mp4; do
    name=$(basename "$video" .mp4)
    echo "Processing: $name"
    python3 scripts/video_slicer.py "$video" "./output/${name}"
done
```

### 7.4 切片质量优化

| 优化项 | 默认值 | 更高质量选项 |
|--------|--------|-------------|
| CRF 质量 | 18 | `17`（更高质量，文件更大） |
| 编码预设 | fast | `medium`（更慢但压缩更好） |
| 音频码率 | 128k | `192k`（更高音质） |
| 分辨率 | 原始 | `-vf scale=1080:-2`（统一 1080p）|

### 7.5 与其他 Skill 协作

| 场景 | 协作 Skill | 方式 |
|------|-----------|------|
| 切片后加字幕 | 字幕生成 Skill | 将转写文本传入 |
| 切片后发社媒 | 小红书/微信 Skill | 将标题和摘要传入 |
| 切片封面图 | 图像生成 Skill | 根据主题生成封面 |

---

## 8. 常见问题 FAQ

### Q: 支持哪些视频格式？

A: ffmpeg 支持几乎所有主流格式：MP4、MKV、MOV、AVI、FLV、WMV 等。
对于特殊格式（如某些摄像机输出的 `.mts`），可能需要额外编解码器。

### Q: Whisper 转写不准确怎么办？

A: 尝试以下方法（按优先级排序）：
1. **换更大的模型**：`base` → `small` → `medium`
2. **优化 initial_prompt**：加入视频相关的专业术语
3. **提高音频质量**：确保源视频音质清晰，无背景噪音过大
4. **分段转写**：将长音频拆为 < 10min 的短段分别转写后再合并

### Q: 切割后的视频太大怎么办？

A: 调整编码参数：
- 提高 CRF 值（18 → 23，文件缩小约 50%）
- 降低分辨率：添加 `-vf scale=720:-2`（720p）
- 降低帧率：添加 `-r 24`（24fps 足够）

### Q: 可以在 Windows 上运行吗？

A: 可以，但有以下限制：
- 没有 MPS 加速（只有 CUDA 或 CPU）
- 需要 WSL2 或原生 Windows Python 环境
- 路径分隔符需要注意

### Q: 如何处理多人同时说话的视频？

A: Whisper 不支持说话人分离（diarization）。如果需要区分不同演讲者：
1. 结合关键帧视觉判断切换时间点
2. 使用 pyannote.audio 等工具做说话人分离
3. 或手动根据转写内容和画面切换划分归属

### Q: 发布新版本后用户如何更新？

A:
```bash
clawhub install bill-mifu/video-slicer --update
# 或
openclaw skills update video-slicer
```

---

## 9. 版本历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|----------|
| **1.2.0** | 2026-05-16 | Bill | ClawHub 发布版：完整用户手册、标准化 API 文档、进阶技巧、FAQ |
| 1.1.0 | 2026-05-16 | Bill | 增加 ClawHub 元数据规范，优化 description 触发词覆盖率 |
| **1.0.0** | 2026-05-16 | Bill | 初始版本，基于中关村「教育+科技」创新周实战验证 |

---

## 10. 贡献指南

欢迎提交 Issue 和 Pull Request！

### 反馈问题

请到 [ClawHub Issues](https://clawhub.ai/bill-mifu/video-slicer) 提交，包含：

1. **复现步骤**
2. **期望行为 vs 实际行为**
3. **环境信息**（OS、Python 版本、ffmpeg 版本）
4. **错误日志**

### 功能建议

我们特别希望看到以下方向的贡献：

- [ ] 支持更多语言（日文、韩文、英文等）
- [ ] 集成说话人分离（Speaker Diarization）
- [ ] 自动字幕生成（SRT 格式）
- [ ] Web UI 界面
- [ ] Docker 一键部署

---

## 致谢

- **OpenAI** — Whisper 语音识别模型
- **FFmpeg** — 多媒体处理框架
- **OpenCC** — 中文繁简转换
- **米赋教育** — 实战验证与应用场景

---

*本手册最后更新于 2026-05-16 by Bill (AI 分身)*
