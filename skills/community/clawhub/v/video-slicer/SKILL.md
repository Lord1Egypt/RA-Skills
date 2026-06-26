---
name: video-slicer
version: "1.2.0"
description: >
  视频智能切片工具。从长视频中按主题切割出3-5分钟（最长8分钟）的独立完整短视频片段，
  适用于自媒体内容制作、演讲精华提取、课程视频剪辑、会议录像精剪等场景。
  完整工作流：关键帧采样→视觉定位→Whisper音频转写→内容分析→ffmpeg精准切割。
  支持中文语音识别（Whisper + MPS加速）。
  当用户提到"视频切割""视频切片""切短视频""演讲精华""截取视频片段""视频剪辑"
  "自媒体视频""提取演讲片段""会议精剪"时触发此技能。
trigger:
  - 视频切割
  - 视频切片
  - 切短视频
  - 演讲精华
  - 自媒体视频
  - 截取视频片段
  - 会议录像精剪
  - 课程视频剪辑
author: Bill (米赋教育 / @bill-mifu)
homepage: https://clawhub.ai/bill-mifu/video-slicer
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - python3
      pip:
        - openai-whisper
        - opencc-python-reimplemented
      env: []
  compatible_models:
    - glm-5v-turbo
    - gpt-4o
    - claude-3.5-sonnet
    - any-multimodal-agent
tags:
  - video
  - audio
  - whisper
  - ffmpeg
  - content-creation
  - chinese
  - social-media
agent_created: true
---

# Video Slicer — 视频智能切片 Skill

> **从长视频中自动定位目标演讲/段落，切割出适合自媒体发布的独立短视频（3-5min，最长8min）**
>
> **推荐模型**: `glm-5v-turbo` | **兼容**: 所有多模态 Agent

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 关键帧采样 | 均匀/精细两种模式，快速定位目标时间段 |
| Whisper 转写 | 本地中文语音识别，MPS GPU 加速，支持繁简转换 |
| 内容智能分析 | 基于转写文本自动设计切片方案（主题+时间戳） |
| 精准切割 | ffmpeg H.264 重编码，句子边界对齐，高质量输出 |
| 批量处理 | 支持一次规划多个切片，一键批量输出 |

## 适用场景

- 自媒体账号运营：从长演讲/直播中截取金句片段
- 教育内容制作：课程视频分章节剪辑
- 会议纪要精剪：从3h+会议录像中提取核心发言
- 播客/访谈剪辑：按话题分段发布
- 个人知识管理：录制内容归档整理

## 工作流程（4个 Phase）

### Phase 1: 快速预览（~2min）— 定位目标区域

**Step 1 — 获取视频信息**

```bash
# 获取时长、分辨率、编码格式
ffmpeg -i <video.mp4> 2>&1 | grep -E "Duration|Stream|Video"
```

**Step 2 — 粗粒度关键帧采样**（每5分钟一帧，把握整体结构）

```bash
VIDEO="path/to/video.mp4"
OUT_DIR="./frames"
mkdir -p "$OUT_DIR"

for t in $(seq 0 5 200); do
  ts=$(printf "%02d:%02d:00" $((t/60)) $((t%60)))
  ffmpeg -y -ss "$ts" -i "$VIDEO" -frames:v 1 -q:v 2 "${OUT_DIR}/frame_${ts}.jpg" 2>/dev/null
done
```

**Step 3 — 目视检查关键帧** → 用 Read 工具查看每帧图片 → 定位目标演讲者的大致时间段

### Phase 2: 精细定位（~3-5min）— 精确起止点

**Step 4 — 过渡区间精细采样**（每2分钟一帧）

```bash
# 在疑似起始/结束区间前后精细采样
for m in 38 40 42 44 46; do
  ffmpeg -y -ss "00:${m}:00" -i "$VIDEO" -frames:v 1 -q:v 2 "./frames/fine_00_${m}.jpg" 2>/dev/null
done
```

**Step 5 — 提取音频 + Whisper 转写**

这是**最关键的步骤**。对于长视频（>30min），**必须先提取音频片段再转写**：

```bash
# 5A: 先用 ffmpeg 提取目标区间的音频（比直接喂视频快10倍）
ffmpeg -y -i "$VIDEO" -ss 00:40:00 -to 01:07:00 \
  -vn -acodec copy ./transcript/segment.aac
```

```python
# 5B: Whisper 转写音频（Python）
import os, ssl, certifi, json, torch, whisper
from opencc import OpenCC

# macOS SSL 必需修复
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
os.environ['SSL_CERT_FILE'] = certifi.where()

AUDIO = "./transcript/segment.aac"
START_OFFSET = 2400  # 音频起点对应的全视频偏移量(秒)

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = whisper.load_model("base", device=device)
result = model.transcribe(AUDIO, language="zh", verbose=False,
    initial_prompt="根据视频主题设置关键词提示")

# 繁简转换 + 时间戳校正
cc = OpenCC('t2s')
segments = []
for seg in result["segments"]:
    segments.append({
        "start": round(seg["start"] + START_OFFSET, 1),
        "end": round(seg["end"] + START_OFFSET, 1),
        "text": cc.convert(seg["text"].strip())
    })

# 保存结构化结果
with open("./transcript/speech.json", "w", encoding="utf-8") as f:
    json.dump(segments, f, ensure_ascii=False, indent=2)

print(f"[OK] 转写完成! {len(segments)} 个片段")
```

### Phase 3: 内容分析与切片规划

**Step 6 — 分析转写文本，设计切片方案**

基于 `speech.json` 中的带时间戳文本，Agent 需要设计合理的切片方案：

#### 切片设计原则

| 原则 | 说明 |
|------|------|
| 时长控制 | 每段 **3-5 分钟**，最长 **不超过 8 分钟** |
| 单一主题 | 每段聚焦一个明确的核心论点/概念 |
| 开头 Hook | 以金句/故事/数据冲击开头，前3秒抓住注意力 |
| 结尾完整 | 在句子自然结束处切断，不截断语义 |
| 可选过渡 | 段间允许 5-10 秒重叠，保证衔接自然 |

#### 常见切片模式参考

| 类型 | 时长 | 适用场景 |
|------|------|----------|
| 开场震撼篇 | 4-5min | 背景、问题引入、数据冲击 |
| 核心概念篇 | 5-6min | 主要论点、定义解释、框架介绍 |
| 高观点/新观点篇 | 4-5min | 哲学思考、范式转换、认知升级 |
| 实践指南篇 | 4-5min | 原则、方法论、操作步骤、案例 |
| 展望总结篇 | 3-4min | 未来趋势、行动呼吁、价值升华 |

#### 切片方案输出格式

将方案保存为 JSON 供切割脚本使用：

```json
[
  {
    "clip_id": 1,
    "start": "00:40:00",
    "end": "00:45:00",
    "title": "教育为什么必须变",
    "theme": "开场震撼",
    "hook": "工业时代的教育体系已经过时了...",
    "duration_sec": 300
  }
]
```

同时生成人类可读的 `clips_plan.md` 文档。

### Phase 4: 执行切割

**Step 7 — ffmpeg 逐段精准切割**

```bash
V="/path/to/source.mp4"
O="./output"
mkdir -p "$O"

# 单段切割命令模板（H.264重编码确保精确切割点）
ffmpeg -y -ss <START_TIME> -to <END_TIME> -i "$V" \
  -c:v libx264 -preset fast -crf 18 \
  -c:a aac -b:a 128k \
  "${O}/clipN_<标题>.mp4"
```

**参数说明：**

| 参数 | 值 | 含义 |
|------|-----|------|
| `-c:v libx264` | H.264 | 兼容性最好的视频编码 |
| `-preset fast` | fast | 编码速度与质量平衡点 |
| `-crf 18` | 18 | 高质量（越小越好，0-51，推荐 17-23） |
| `-c:a aac` | AAC | 通用音频编码 |
| `-b:a 128k` | 128kbps | 音频质量足够好 |

**批量切割脚本：**

```bash
#!/bin/bash
V="$HOME/Downloads/source_video.mp4"
OUT="./output"
mkdir -p "$OUT"

# 从 clips_plan.json 读取并切割
while IFS=',' read -r start end filename title; do
  echo ">>> 切割: $title ($start -> $end)"
  ffmpeg -y -ss "$start" -to "$end" -i "$V" \
    -c:v libx264 -preset fast -crf 18 \
    -c:a aac -b:a 128k \
    "${OUT}/${filename}.mp4" 2>/dev/null
done < clips.csv

echo "=== 全部完成 ==="
ls -lh "$OUT"/*.mp4
```

## 一键脚本用法

Skill 附带 Python 一键脚本，支持基础自动化：

```bash
# 完整工作流（采样帧 + 转写短视频 + 输出结构化数据）
python3 {baseDir}/scripts/video_slicer.py <视频文件路径> [输出目录]

# 示例
python3 {baseDir}/scripts/video_slicer.py ~/Downloads/演讲视频.mp4 ./my_output
```

> **注意**: 对于超过 30 分钟的视频，脚本会跳过全量转写（避免超时），需要 Agent 手动指定时间范围后调用 `transcribe_segment()` 函数。

## 环境依赖

| 工具 | 版本要求 | 用途 | 安装方式 |
|------|----------|------|----------|
| **ffmpeg** | >= 5.0 | 视频/音频处理核心引擎 | `brew install ffmpeg` |
| **Python** | >= 3.10 | Whisper 运行环境 | 系统 / conda |
| **openai-whisper** | >= 20231117 | OpenAI 本地语音转文字模型 | `pip install openai-whisper` |
| **opencc-python-reimplemented** | >= 0.1.2 | 繁体中文→简体转换 | `pip install opencc-python-reimplemented` |
| **PyTorch** | >= 2.0 | Whisper 底层依赖（含 MPS 支持） | `pip install torch` |

### 一键安装依赖

```bash
pip install openai-whisper opencc-python-reimplemented torch
brew install ffmpeg   # macOS
```

## Whisper 模型选择指南

| 模型 | 大小 | MPS速度* | 中文质量 | 推荐场景 |
|------|------|----------|----------|----------|
| `tiny` | 39MB | 最快 (~5x) | 差 | 仅用于粗略定位，不推荐生产使用 |
| `base` | 139MB | 快 (~1x) | 中等良好 | **日常使用推荐** ✅ 默认选择 |
| `small` | 461M | 中等 (~0.5x) | 较好 | 需要高精度转写时 |
| `medium` | 1.5GB | 慢 (~0.15x) | 好 | 专业级（慎用，非常慢） |

*\* MPS 速度为相对于 base 模型在 Apple M 系列芯片上的大致倍率*

## 文件输出规范

完成后的标准输出目录结构：

```
project_output/
├── output/                  # ✅ 最终切片视频（交付物）
│   ├── clip1_<主题>.mp4     # 每个 3-8 min，H.264 编码
│   ├── clip2_<主题>.mp4
│   └── clipN_<主题>.mp4
├── frames/                  # 采样关键帧（调试/定位用）
│   ├── frame_00:00:00.jpg
│   ├── frame_00:05:00.jpg
│   └── fine_00_40.jpg       # 精细采样帧
├── transcript/              # 转写文本数据
│   ├── speech.json          # 结构化 JSON（含精确时间戳）
│   ├── speech.txt           # 可读纯文本
│   └── segment.aac          # 提取的音频片段
└── clips_plan.md            # 切片方案文档（人工可审阅）
```

## 常见问题与避坑指南

### Q1: 全视频太长（3h+），Whisper 处理超时怎么办？

**A: 这是新手最容易踩的坑！** 核心优化技巧——先提取音频再转写：

```bash
# ❌ 错误：直接喂 3 小时视频给 Whisper（可能需要 30min+ 或直接 OOM）
whisper long_video.mp4 --model base --language zh

# ✅ 正确：先用 ffmpeg 提取 27 分钟音频片段，再转写（只需 2-3min）
ffmpeg -y -i long_video.mp4 -ss 00:40 -to 01:07 -vn -acodec copy segment.aac
whisper segment.aac --model base --language zh
```

### Q2: 切割后视频开头有黑屏/画面滞后？

**A:** 使用 re-encoding 模式（`-c:v libx264`）而非 stream copy（`-c:v copy`）。重编码模式能确保切割点的帧级精确度。

### Q3: 如何保证每个切片在完整句子处结束？

**A:** 利用 Whisper 转写的 sentence-level 时间戳（`segments[].end`），找到最近的句子结束时间作为切割终点。**不要**用任意秒数切割。

### Q4: Whisper 转出的中文是繁体字？

**A:** 这是正常现象（Whisper 训练数据包含大量繁体文本）。使用 OpenCC 的 `t2s` 模式即可自动转换为简体。

### Q5: macOS 上运行报 SSL Certificate 错误？

**A:** 在导入 whisper 之前添加以下代码：
```python
import ssl, certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
os.environ['SSL_CERT_FILE'] = certifi.where()
```

### Q6: 视频是 HEVC/H.265 编码，切割后不兼容？

**A:** 使用 `-c:v libx264` 重编码为 H.264 即可解决兼容性问题。

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2026-05-16 | 初始版本，基于中关村「教育+科技」创新周实战验证 |
| 1.1.0 | 2026-05-16 | 增加 ClawHub 元数据规范，优化 description 触发词 |
| 1.2.0 | 2026-05-16 | 完整用户手册，标准化输出格式，兼容性增强 |

## 相关文档

- 详细用户手册: `{baseDir}/README.md`
- 一键脚本源码: `{baseDir}/scripts/video_slicer.py`
