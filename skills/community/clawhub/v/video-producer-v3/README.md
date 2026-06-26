# 🎬 短视频一键生成器 v3.0 (标准付费版)

> **输入主题，5分钟AI自动生成完整竖屏短视频**

## 📦 包含文件

```
video-producer-v3/
├── video_producer.py    # 主程序 (直接运行)
├── SKILL.md             # OpenClaw Skill 配置 (可选)
├── README.md            # 本文件
└── .env.example         # 配置文件模板
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip install requests pillow

# FFmpeg (如果没有)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco install ffmpeg
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
# 编辑 .env 文件
```

或者直接设置环境变量：

```bash
export MINIMAX_API_KEY="你的MiniMax Key"
```

### 3. 运行

```bash
python3 video_producer.py \
  --topic "AI会取代程序员吗？" \
  --points '[
    {"text":"AI不是取代程序员，而是成为他们的超级工具", "emoji":"🤖", "title":"认清本质"},
    {"text":"掌握AI工具的程序员薪资涨了30%", "emoji":"📈", "title":"数据说话"},
    {"text":"10年后不会AI = 今天不会用电脑", "emoji":"🎯", "title":"残酷现实"}
  ]' \
  --style tech \
  --output ./my_video
```

### 4. 输出

```
my_video/
├── storyboard.json         # AI分镜规划
├── materials/              # AI生成的场景图片
├── audio/                  # TTS配音文件
├── output.mp4              # 无字幕版
└── final_subtitled.mp4     # ✅ 最终成品 (带字幕)
```

## ⚙️ 多后端支持

本工具支持 **3种TTS后端 + 3种图片后端**，用哪个由用户决定：

### TTS 配音

| 后端 | 环境变量 | 价格 | 质量 |
|------|---------|------|------|
| `minimax` (默认) | `MINIMAX_API_KEY` | MiniMax付费 | ⭐⭐⭐ |
| `openai` | `OPENAI_API_KEY` | OpenAI TTS付费 | ⭐⭐⭐⭐⭐ |
| `edge` (免费) | 无需Key | **免费** | ⭐⭐ |

设置方式：

```bash
# 使用 OpenAI TTS
export TTS_BACKEND="openai"
export OPENAI_API_KEY="sk-xxx"

# 或使用免费的 Edge TTS (需安装 edge-tts)
# pip install edge-tts
export TTS_BACKEND="edge"
```

### 图片生成

| 后端 | 环境变量 | 价格 | 质量 |
|------|---------|------|------|
| `minimax` (默认) | `MINIMAX_API_KEY` | MiniMax付费 | ⭐⭐⭐ |
| `openai` | `OPENAI_API_KEY` | DALL-E 3付费 | ⭐⭐⭐⭐⭐ |
| `placeholder` | 无需Key | **免费** | 占位图 |

设置方式：

```bash
export IMAGE_BACKEND="openai"
export OPENAI_API_KEY="sk-xxx"
```

## 🎨 视觉风格

| 风格 | 适用场景 | 色调 |
|------|---------|------|
| `tech` | 科技、AI、数码 | 蓝紫色调 |
| `warm` | 教育、情感、生活 | 暖色调 |
| `business` | 营销、干货、职场 | 商务白蓝 |

## 📝 命令行参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic` | ✅ | 视频主题 |
| `--points` | ✅ | 要点JSON：`[{"text":"...","emoji":"...","title":"..."}]` |
| `--style` | ❌ | 视觉风格：`tech` / `warm` / `business` (默认: tech) |
| `--output` | ❌ | 输出目录 (默认: ./output_时间戳) |
| `--no-subtitles` | ❌ | 不添加字幕 |

## 🔧 环境变量大全

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TTS_BACKEND` | `minimax` | TTS后端: minimax / openai / edge |
| `IMAGE_BACKEND` | `minimax` | 图片后端: minimax / openai / placeholder |
| `MINIMAX_API_KEY` | `` | MiniMax API Key |
| `MINIMAX_TTS_VOICE` | `female-yujie` | MiniMax 配音角色 |
| `OPENAI_API_KEY` | `` | OpenAI API Key |
| `OPENAI_BASE` | `https://api.openai.com/v1` | OpenAI API 地址 (可换代理) |
| `OPENAI_TTS_VOICE` | `alloy` | OpenAI 配音: alloy/echo/fable/nova/shimmer |
| `OPENAI_IMAGE_MODEL` | `dall-e-3` | OpenAI 图片模型 |

## 📊 技术规格

- **输出分辨率:** 1080 × 1920 (竖屏)
- **视频编码:** H.264 + AAC
- **字幕格式:** SRT 硬字幕
- **帧率:** 自动适配
- **总时长:** 约 20-30 秒 (取决于要点数量)

## ℹ️ 常见问题

**Q: 我没有 API Key 怎么办？**
A: 设置 `TTS_BACKEND=edge` 和 `IMAGE_BACKEND=placeholder` 可以免费测试流程。完整功能需要至少一个 TTS 或文生图 API。

**Q: 可以用到商业项目吗？**
A: 标准版允许个人和商业使用，但不能二次销售。

**Q: 生成的视频能直接在抖音/小红书发吗？**
A: 可以，1080×1920 竖屏格式，直接上传。

---

**版本:** 3.0.0 | **类型:** 标准付费款 | **定价:** ¥29.9
