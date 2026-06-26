# 视频转文档操作指南

本文档详细介绍如何使用 video-to-doc 技能将视频转换为图文并茂的操作指南文档。

## 完整工作流程

### 1. 准备视频文件

确保视频文件格式支持：
- 常见格式：mp4, wmv, avi, mov, mkv
- 建议时长：1-5分钟（过长视频会产生过多截图）
- 建议分辨率：1080p或以上（确保截图清晰）

### 2. 智能提取关键帧（推荐）

使用 `scripts/smart_extract.py` 脚本，自动选择最优策略：

```bash
# 自动模式（推荐）
python scripts/smart_extract.py video.mp4

# 指定输出目录
python scripts/smart_extract.py video.mp4 -o ./frames

# 限制最大帧数
python scripts/smart_extract.py video.mp4 -m 20

# 强制使用场景检测
python scripts/smart_extract.py video.mp4 -s scene

# 强制每5秒一帧
python scripts/smart_extract.py video.mp4 -s interval_5
```

**智能策略说明：**

| 视频时长 | 自动策略 | 原因 |
|---------|---------|------|
| ≤30秒 | 每3秒一帧 | 短视频需要密集采样 |
| 30-60秒 | 每4秒一帧 | 中等密度 |
| 1-3分钟 | 每6秒一帧 | 标准密度 |
| 3-10分钟 | 每10秒一帧 | 稀疏采样 |
| >10分钟 | 每15秒一帧 或 场景检测 | 避免帧数过多 |

**场景变化检测：**
- 当预计帧数 > 30张时自动启用
- 只截取画面变化明显的帧
- 检测阈值默认 0.3（可调整）
- 如果帧数 < 5，自动回退间隔模式

### 2.5 提取并转录音频（重要）

**为什么需要音频转录？**
- 很多操作视频有语音讲解
- 画面可能遗漏关键操作细节
- 语音解说能补充重要注意事项

**步骤1：提取音频**
```bash
# 提取音频（16kHz单声道，适合语音识别）
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav -y
```

**步骤2：选择ASR服务并转录**

使用 `scripts/transcribe_audio.py` 脚本：

```bash
# 方案A：本地 Whisper（免费，但需要等待）
pip install openai-whisper
python transcribe_audio.py audio.wav local

# 方案B：OpenAI Whisper API（快速，需要API Key）
pip install openai
python transcribe_audio.py audio.wav openai --api-key YOUR_KEY

# 方案C：使用更大的本地模型（更准确）
python transcribe_audio.py audio.wav local --model small
# 可选模型: tiny, base, small, medium, large
```

**转录结果格式**：
```json
{
  "segments": [
    {"start": 0.0, "end": 5.2, "text": "现在我们进入预期到货通知模块"},
    {"start": 6.0, "end": 12.5, "text": "点击新增按钮创建一个新的通知"},
    {"start": 13.0, "end": 20.0, "text": "类型选择生产退料"}
  ]
}
```

**步骤3：音频与截图对齐**
- 每张截图有时间戳（如 frame_01.jpg 对应 0-6秒）
- 根据时间戳匹配对应的转录文字
- 在文档中结合画面信息和语音说明

### 3. 分析截图内容与整合音频

使用 `read_image` 工具分析截图：

```
read_image(["./frames/frame_01.jpg", "./frames/frame_02.jpg"])
```

**分析要点**：
- 识别界面类型（表单、列表、对话框等）
- 提取关键文字信息
- 理解操作逻辑和流程
- 记录重要字段和参数

**同时读取音频转录结果**：
```bash
# 读取转录文件
cat audio_transcript.json
```

**整合画面与音频信息**：
| 截图 | 时间段 | 画面信息 | 语音说明 |
|-----|-------|---------|---------|
| frame_01.jpg | 0-6秒 | 进入预期到货通知模块 | "现在我们进入预期到货通知模块" |
| frame_02.jpg | 6-12秒 | 点击新增按钮 | "点击新增按钮创建新通知" |
| frame_03.jpg | 12-18秒 | 填写表单 | "类型选择生产退料，注意..." |

**注意**：`read_image` 有调用频率限制，建议分批处理：
- 每次处理 3-4 张截图
- 遇到频率限制时等待几秒再继续

### 4. 编写文档内容

使用 `scripts/create_doc_template.js` 作为模板：

```javascript
// 修改配置项
const CONFIG = {
  title: "XXX操作指南",
  framesDir: "./frames",
  frameFiles: ['frame_01', 'frame_02', ...],
  outputName: "操作指南.docx"
};

// 定义步骤
const STEPS = [
  {
    title: "步骤1：xxx",
    description: "操作说明文字",
    imageFile: "frame_01",
    imageCaption: "图1：xxx界面",
    bullets: [
      { label: "要点1：", content: "详细说明" }
    ]
  }
];
```

### 5. 生成Word文档

```bash
# 安装依赖（首次使用）
npm install docx

# 运行脚本
node create_doc_template.js
```

## 文档结构规范

### 推荐结构

```
一、操作概述
   - 简要说明操作目的和适用场景
   - 1-2段话即可

二、系统信息（如适用）
   - 表格形式展示系统名称、模块、版本等

三、操作步骤详解
   步骤1：xxx
   - 操作说明
   - 截图（居中）
   - 图片说明（斜体灰色）
   - 要点列表（可选）

   步骤2：xxx
   ...

四、注意事项
   - 编号列表形式
   - 每条简洁明了

五、关键字段说明（如适用）
   - 表格形式
   - 列：字段名称、说明、示例值
```

### 样式规范

| 元素 | 字体 | 大小 | 颜色 |
|-----|------|-----|------|
| 标题 | 微软雅黑 | 48pt(24号) | #1F4E79 |
| 一级标题 | 微软雅黑 | 32pt(16号) | #2E75B6 |
| 二级标题 | 微软雅黑 | 28pt(14号) | #5B9BD5 |
| 正文 | 微软雅黑 | 24pt(12号) | #000000 |
| 图片说明 | 微软雅黑 | 20pt(10号) | #666666(斜体) |

## 常见问题

### Q: 截图太多怎么办？
A: 筛选关键步骤的截图，一个文档控制在6-10张图片为宜。

### Q: 视频太长怎么办？
A: 可以增加帧间隔，比如设为10秒或15秒一帧。

### Q: 截图不清晰怎么办？
A: 提高视频分辨率，或在 ffmpeg 中使用 `-q:v 1` 参数（最高质量）。

### Q: 如何处理多语言？
A: 在文档样式中修改默认字体，如英文文档使用 Arial。

## 最佳实践

1. **视频准备**
   - 确保操作演示完整、流畅
   - 避免无关操作或中断
   - 重要界面适当停留

2. **截图筛选**
   - 选择操作转折点的截图
   - 避免重复或相似的截图
   - 确保每张截图都有说明价值

3. **文档编写**
   - 步骤标题用动词开头
   - 描述简洁、准确
   - 要点列表补充细节
   - 图片说明概括内容

4. **质量检查**
   - 检查图片是否正确显示
   - 检查文字是否有错别字
   - 检查格式是否一致
