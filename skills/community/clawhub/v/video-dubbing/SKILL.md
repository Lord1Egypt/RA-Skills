---
name: voxcpm-chinese-dubbing
description: "🎯 **唯一使用VoxCPM的中文配音技能** - 外语视频一键中文配音，支持硬字幕检测、断点续传、智能BGM。触发场景：(1) 用户需要给外语视频配音 (2) 视频翻译需求 (3) 多语言内容本地化"
version: 1.1.0
author: newaiguy
tags: [video, dubbing, voxcpm, chinese, translation, whisper, tts]
credentials:
  - name: TRANSLATE_API_KEY
    description: 翻译API密钥（SiliconFlow/兼容OpenAI格式的API）
    required: true
  - name: VOXCPM_DIR
    description: VoxCPM模型目录路径
    required: true
endpoints:
  - name: TRANSLATE_API_URL
    description: 翻译API端点
    default: https://api.siliconflow.cn/v1/chat/completions
  - name: VISION_API_URL
    description: 硬字幕检测API端点（支持Vision模型）
    default: https://api.siliconflow.cn/v1/chat/completions
paths:
  - name: WORK_DIR
    description: 工作目录
    default: ./workspace
  - name: REFERENCE_AUDIO
    description: TTS参考音频路径
    default: ./reference_audio/speaker.wav
external_calls:
  - description: 翻译API调用（批量翻译英文到中文）
    trigger: 自动调用（配音流程中必需）
  - description: Vision API调用（硬字幕检测）
    trigger: 自动调用（可选，检测视频是否有烧录字幕）
---

# 🎬 VoxCPM中文视频配音

> **唯一使用VoxCPM开源模型的中文配音技能**
> 
> 生产环境验证 ✅ | 断点续传 ✅ | 智能BGM ✅

## 🌟 核心卖点

| 特性 | 说明 |
|------|------|
| 🎯 **VoxCPM独家** | 唯一集成VoxCPM开源TTS模型的中文配音技能 |
| ✅ **生产验证** | 已在B站成功发布4个视频 |
| 🔄 **断点续传** | 中断后可继续，无需重新生成 |
| 🔍 **硬字幕检测** | AI自动检测并覆盖原字幕 |
| 🎵 **智能BGM** | 自动循环、交叉淡入淡出 |

## 📋 完整流程

```
1. Whisper转写    → medium模型转写 + 时间戳
2. AI翻译        → 腾讯混元MT翻译模型
3. 分组TTS       → VoxCPM配音（按组生成，保持连贯）
4. 音频匹配      → 智能拉伸/加静音
5. 硬字幕检测    → AI自动检测是否需要遮盖
6. 字幕生成      → 中文字幕（自动换行）
7. 视频合并      → GPU加速编码
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python依赖
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install openai-whisper soundfile scipy librosa requests

# VoxCPM（从官方获取）
git clone https://github.com/modelscope/VoxCPM.git
```

### 2. 配置

复制配置模板：
```bash
cp config.example.json config.json
```

编辑 `config.json`：
```json
{
  "work_dir": "./workspace",
  "voxcpm_dir": "./VoxCPM",
  "ffmpeg_path": "ffmpeg",
  "translate": {
    "api_url": "https://api.siliconflow.cn/v1/chat/completions",
    "api_key": "YOUR_API_KEY",
    "model": "tencent/Hunyuan-MT-7B"
  },
  "vision": {
    "api_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "Qwen/Qwen2.5-VL-72B-Instruct"
  },
  "tts": {
    "reference_audio": "./reference_audio/speaker.wav",
    "reference_text": "参考音频对应的文本"
  }
}
```

> **注意**: 所有配置项均可通过环境变量覆盖，优先级：环境变量 > config.json > 默认值
```

### 3. 运行

```bash
python scripts/dubbing.py your_video.mp4
```

输出：
- `workspace/output/your_video_dubbed.mp4` - 配音视频
- `workspace/output/your_video.srt` - 字幕文件

## ⚙️ 参数说明

### Whisper参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `whisper.model` | medium | Whisper模型大小 |
| `whisper.language` | en | 源语言 |

### TTS参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `tts.max_group_duration` | 15.0 | 每组最大时长（秒） |
| `tts.inference_timesteps` | 10 | 推理步数 |
| `tts.cfg_value` | 2.0 | CFG值 |

### 字幕参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `subtitle.fontsize` | 16 | 字体大小 |
| `subtitle.fontname` | SimHei | 字体名称 |
| `subtitle.outline` | 2 | 描边宽度 |

## 🎵 BGM添加

```bash
python scripts/add_bgm.py <视频> [BGM文件] [输出文件]
```

特性：
- BGM自动循环（交叉淡入淡出3秒）
- 音量控制（默认12%）
- 自动淡入淡出

## 🔧 高级用法

### 测试模式

只处理前30秒：
```bash
python scripts/dubbing.py video.mp4 --test 30
```

### 指定输出名

```bash
python scripts/dubbing.py video.mp4 --output my_video
```

### 自定义配置

```bash
python scripts/dubbing.py video.mp4 --config my_config.json
```

## 📁 文件结构

```
video-dubbing/
├── SKILL.md              # 本文档
├── config.example.json   # 配置模板
├── scripts/
│   ├── dubbing.py       # 主流程脚本
│   ├── add_bgm.py       # BGM添加
│   └── upload_bilibili.py # B站上传
└── reference_audio/      # TTS参考音频
    └── speaker.wav
```

## 🔑 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TRANSLATE_API_KEY` | 翻译API密钥（必需） | - |
| `VOXCPM_DIR` | VoxCPM目录 | `./VoxCPM` |
| `WORK_DIR` | 工作目录 | `./workspace` |
| `REFERENCE_AUDIO` | TTS参考音频路径 | `./reference_audio/speaker.wav` |
| `REFERENCE_TEXT` | 参考音频对应文本 | - |
| `TRANSLATE_API_URL` | 翻译API端点 | SiliconFlow |
| `TRANSLATE_MODEL` | 翻译模型 | `tencent/Hunyuan-MT-7B` |
| `VISION_API_URL` | 硬字幕检测API端点 | SiliconFlow |
| `VISION_MODEL` | Vision模型 | `Qwen/Qwen2.5-VL-72B-Instruct` |
| `WHISPER_MODEL` | Whisper模型 | `medium` |
| `WHISPER_LANGUAGE` | 源语言 | `en` |
| `FFMPEG_PATH` | ffmpeg路径 | `ffmpeg` |

## 📊 音频匹配质量

| ratio范围 | 方法 | 质量 |
|-----------|------|------|
| < 0.85 | 加静音 | ✅ 无损 |
| 0.85-1.15 | resample | ✅ 轻微调整 |
| > 1.15 | librosa加速 | ⚠️ 轻微失真 |

**实测：60%+组无损音质**

## ⚠️ 注意事项

### AV1编码视频

AV1编码视频需要重新编码：
```bash
# 使用GPU编码
-c:v h264_nvenc

# 或CPU编码
-c:v libx264
```

### VoxCPM模型

需要从ModelScope获取VoxCPM模型：
```bash
# 下载模型到指定目录
modelscope download --model modelscope/VoxCPM --local_dir ./VoxCPM
```

## 📜 许可证

MIT License

## 🙏 致谢

- [VoxCPM](https://github.com/modelscope/VoxCPM) - 高质量中文TTS
- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别
- [Hunyuan-MT](https://huggingface.co/tencent/Hunyuan-MT-7B) - 翻译模型

---

**🎯 选择VoxCPM中文配音的理由：**
1. 开源免费，无商业限制
2. 中文效果最佳，自然流畅
3. 支持声音克隆（参考音频）
4. 本地运行，数据安全