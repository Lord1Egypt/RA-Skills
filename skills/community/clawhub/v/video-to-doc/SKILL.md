---
name: video-to-doc
description: 将操作视频自动转换为图文并茂的Word操作指南文档，支持智能截图、语音转录、LLM内容提炼和流程图生成
version: 1.0.0
---

# Video to Doc 技能

将视频教程转换为图文并茂的Word操作指南文档。

## 功能描述

本技能能够：
1. 自动分析视频文件，提取关键帧截图
2. **使用扣子平台内置 read_image 工具识别截图中的界面元素**
3. 生成结构化的图文操作指南Word文档

## 适用场景

- 软件操作教程视频 → 操作指南文档
- 系统演示视频 → 用户手册
- 培训视频 → 培训材料
- 产品演示视频 → 产品说明文档

## 使用前提

### 必需依赖

```bash
# 安装 ffmpeg（视频处理）
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# 安装 Python 依赖
pip install python-docx pillow faster-whisper
```

### 可选配置

语音转录支持多种方案：
- **方案A（推荐）**：使用扣子平台官方「语音转文本」插件（免费配额每日20次）
- **方案B**：本地 faster-whisper 模型（首次运行自动下载，约75MB）
- **方案C**：OpenAI Whisper API（需要API Key）

LLM内容提炼使用扣子平台内置大模型能力，无需额外配置。

## 工作流程

### 新版流程（使用 read_image）

本版本采用**主对话分析 + 脚本合并**的架构，充分利用扣子平台内置的 read_image 视觉理解能力：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Python脚本      │    │  主对话         │    │  Python脚本      │
│  提取截图/语音   │ →  │  read_image分析 │ →  │  合并生成文档    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### 步骤1：提取截图和语音（Python 脚本）

```bash
python video_to_doc.py video.mp4
```

脚本自动完成：
1. 智能截图（根据视频时长自适应）
2. 音频提取
3. 语音转录

完成后输出：
```
[3/6] 等待截图分析...
截图目录: video_frames
分析结果保存到: video_frames_analysis.json
```

并打印标记：
```
[MARKER_FOR_MAIN_AGENT]
WAIT_FOR_FRAME_ANALYSIS
frames_dir=video_frames
analysis_output=video_frames_analysis.json
frame_count=15
[/MARKER_FOR_MAIN_AGENT]
```

#### 步骤2：截图分析（主对话用 read_image）

主对话收到 `WAIT_FOR_FRAME_ANALYSIS` 标记后：

1. **读取截图列表**：`glob.glob("video_frames/*.jpg")`
2. **逐个分析**：使用 `read_image` 工具分析每张截图
3. **汇总结果**：按格式生成 JSON

**read_image 分析提示词模板**：
```
分析截图中的：
1. UI元素：按钮、表单、菜单等（text + type）
2. 文本内容：界面上显示的主要文字
3. 操作提示：根据画面推断下一步操作

格式要求：
- ui_elements: [{"text": "文字", "type": "按钮/输入框/菜单项/..."}]
- text_content: 界面主要内容摘要
- action_hint: 简短的步骤描述（如"点击确定按钮"）
```

**输出格式**（保存到 `video_frames_analysis.json`）：
```json
{
  "frames": [
    {
      "timestamp": 0,
      "ui_elements": [
        {"text": "新增", "type": "按钮"},
        {"text": "请输入名称", "type": "输入框"}
      ],
      "text_content": "员工管理页面，显示新增和删除按钮",
      "action_hint": "点击新增按钮添加员工"
    },
    {
      "timestamp": 6,
      "ui_elements": [
        {"text": "确定", "type": "按钮"},
        {"text": "取消", "type": "按钮"}
      ],
      "text_content": "新增员工对话框",
      "action_hint": "填写信息后点击确定"
    }
  ]
}
```

#### 步骤3：继续生成文档

主对话分析完成后，运行：
```bash
python video_to_doc.py --continue
```

脚本自动完成：
1. 合并截图分析和语音转录
2. 时间戳对齐
3. 生成Word文档

### 调用方式汇总

```bash
# 完整流程
python video_to_doc.py video.mp4           # 步骤1：提取截图和语音
# [主对话用 read_image 分析截图]
python video_to_doc.py --continue          # 步骤3：生成文档

# 可选参数
python video_to_doc.py video.mp4 -o my.docx      # 指定输出文件
python video_to_doc.py video.mp4 -m 20            # 最多20张截图
python video_to_doc.py video.mp4 --no-audio      # 跳过语音转录
```

## 智能截图策略

### 自动策略选择

系统根据视频特征自动选择最优截图策略：

| 视频时长 | 自动策略 | 预计帧数 |
|---------|---------|---------|
| ≤30秒 | 每3秒一帧 | ~10张 |
| 30-60秒 | 每4秒一帧 | ~15张 |
| 1-3分钟 | 每6秒一帧 | ~20张 |
| 3-10分钟 | 每10秒一帧 | ~30张 |
| >10分钟 | 每15秒一帧 或 场景检测 | 自适应 |

### 场景变化检测（自动触发）

- 当预计帧数超过30张时，自动切换到场景变化检测
- 只截取画面明显变化的帧，避免冗余
- 如果检测帧数太少，自动回退到间隔模式

### 用户可强制指定

```bash
# 固定间隔
python smart_extract.py video.mp4 -s interval_5

# 场景检测
python smart_extract.py video.mp4 -s scene

# 限制最大帧数
python smart_extract.py video.mp4 -m 20
```

## 截图分析说明

### read_image 分析要点

主对话使用 `read_image` 分析截图时，关注：

1. **UI元素识别**
   - 按钮（确定、取消、新增、删除等）
   - 输入框、复选框、下拉菜单
   - 导航菜单、标签页
   - 图标（带文字提示的）

2. **文本内容提取**
   - 表格内容（关键字段）
   - 表单标签
   - 提示信息
   - 错误信息

3. **操作推断**
   - 根据按钮位置推断操作顺序
   - 根据表单字段推断填写顺序
   - 根据上下文推断下一步

### 分析质量提升技巧

- **批量分析**：可一次性分析多张截图
- **保持一致性**：使用统一的分析格式
- **时间上下文**：考虑相邻帧的关系

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `video_to_doc.py` | 主入口，流程控制 |
| `scripts/smart_extract.py` | 智能截图 |
| `scripts/transcribe_audio.py` | 语音转录 |
| `scripts/merge_and_generate.py` | 合并截图分析和语音转录 |
| `scripts/generate_docx.py` | 生成Word文档 |

## LLM内容提炼

### 提炼目标

将口语化的语音转录内容转换为规范的操作说明：
- "然后我们点这个" → "点击【XX】按钮"
- "先去输入" → "在「XX」输入框填写"
- 去除口头禅、重复表述
- 精简步骤数量

### 提炼流程

1. **读取分析数据**：截图分析结果 + 语音转录结果
2. **合并时间戳**：将语音内容与截图对应
3. **LLM提炼**：将口语化描述转为规范操作说明
4. **合并步骤**：将多个小步骤合并为核心步骤

### 提炼提示词

```
将以下操作视频的内容提炼为规范的操作指南：

截图分析：{frames_analysis}
语音转录：{audio_transcript}

要求：
1. 提取核心操作步骤（控制在4-6步）
2. 使用规范表述：
   - 点击操作：【按钮名称】
   - 输入字段：「字段名称」
   - 示例值：直接文本
3. 去除口语化表达和重复内容
4. 每个步骤包含：标题 + 操作描述
```

## 流程图生成

### 流程图格式

在文档开头添加横向箭头流程图，使用表格实现：

```
进入系统 → 填写信息 → 拍照上传 → 查询管理 → 完成
```

### 实现方式

```python
# Word中用表格实现横向流程图
table = doc.add_table(rows=1, cols=9)
flow_steps = ['进入系统', '→', '填写信息', '→', '拍照上传', '→', '查询管理', '→', '完成']
```

### 节点数量

- 核心步骤 ≤ 4个：直接展示
- 核心步骤 5-6个：合并相似步骤
- 核心步骤 > 6个：提取主要流程

## 文档输出规范

### 文档结构

```
一、操作概述
二、操作流程图
三、详细操作步骤
四、注意事项
```

### 操作标记规范

| 标记类型 | 格式 | 颜色 | 示例 |
|----------|------|------|------|
| 按钮 | 【名称】 | 蓝色加粗 | 【拍照】【上传】 |
| 输入框 | 「名称」 | 绿色加粗 | 「合同号」「备注」 |
| 示例值 | 直接文本 | 紫色 | DFD-BH20251226CSXT01 |

### 内容精简原则

- 每个步骤控制在2-3句话
- 只保留核心操作，去除冗余描述
- 截图选择：每个步骤配1张关键截图
- 注意事项：控制在3-5条

## 技术架构

```
video_to_doc.py
├── 提取截图 → smart_extract.py
├── 语音转录 → transcribe_audio.py
├── [主对话] → read_image 分析截图
├── [主对话] → LLM 提炼内容
└── 合并生成 → merge_and_generate.py → generate_docx.py
```

**关键设计**：
- Python 脚本负责：文件处理、音频处理、数据合并、文档生成
- 主对话负责：视觉理解、截图分析、内容提炼、操作推断
- 分工明确，优势互补

## 常见问题

### Q: 为什么截图分析要在主对话做？
A: read_image 是扣子平台的内置视觉理解工具，可以直接理解截图内容，无需额外调用 API 或模型。

### Q: 可以跳过语音转录吗？
A: 可以，使用 `--no-audio` 参数。但建议保留语音，可以让操作说明更准确。

### Q: 分析结果文件是什么格式？
A: JSON 格式，包含 `frames` 数组，每个帧包含 `timestamp`、`ui_elements`、`text_content`、`action_hint`。

### Q: 如何调整截图数量？
A: 使用 `-m` 参数，如 `-m 20` 表示最多20张截图。
