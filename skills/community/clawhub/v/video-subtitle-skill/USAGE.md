# 视频字幕生成器 - 使用指南

## 快速开始

### 1. 环境准备

```bash
# Python 依赖
pip install requests

# 系统依赖
sudo apt install ffmpeg            # 音频提取 & 字幕烧入
sudo apt install fonts-noto-cjk    # 中日韩字幕字体（烧入时需要）

# 配置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export SENSEAUDIO_API_KEY="你的 SenseAudio API 密钥"

source ~/.bashrc
```

> SenseAudio API 密钥在 https://senseaudio.cn 注册后获取。

### 2. 在 Claude Code 中使用

Skill 安装完成后，直接用自然语言对话即可：

**生成字幕：**
```
帮我给 ~/videos/lecture.mp4 加字幕
```

**翻译字幕：**
```
把 ~/videos/interview_en.mp4 翻译成中文字幕
```

**烧入视频：**
```
给 ~/videos/vlog.mp4 生成字幕并烧入视频
```

**会议记录（多人场景）：**
```
帮我把 ~/meeting.mp4 转成文字，区分不同说话人
```

**总结视频内容：**
```
帮我总结一下 ~/videos/news.mp4 讲了什么
```

Claude 会自动识别你的需求，选择合适的参数运行脚本。如需内容总结，Claude 会直接读取转写文本进行分析。

### 3. 手动命令行使用

```bash
# 基础字幕生成
python scripts/video_subtitle.py ~/videos/lecture.mp4

# 指定语言 + 输出目录
python scripts/video_subtitle.py ~/videos/lecture.mp4 --language zh --output ~/subtitles/

# 翻译：中文视频 → 英文字幕
python scripts/video_subtitle.py ~/videos/lecture.mp4 --language zh --translate en

# 字幕烧入视频（指定字体大小）
python scripts/video_subtitle.py ~/videos/vlog.mp4 --burn --font-size 28

# 说话人分离（会议/访谈场景，推荐用 pro 模型）
python scripts/video_subtitle.py ~/meeting.mp4 --model pro --speaker

# 同时生成 SRT + VTT 格式
python scripts/video_subtitle.py ~/videos/lecture.mp4 --format both
```

## 输出文件

每次运行会在输出目录下生成以下文件（按需）：

| 文件 | 说明 | 何时生成 |
|------|------|---------|
| `文件名.srt` | SRT 格式字幕 | 始终 |
| `文件名.vtt` | VTT 格式字幕 | `--format vtt` 或 `both` |
| `文件名.txt` | 纯文本转写 | 始终 |
| `文件名_detail.json` | 详细识别结果（时间戳、说话人等） | 始终 |
| `文件名_subtitled.mp4` | 烧入字幕的视频 | `--burn` |

## ASR 模型选择

| 模型 | 参数 | 速度 | 精度 | 推荐场景 |
|------|------|------|------|---------|
| 极速版 | `--model lite` | 最快 | 一般 | 批量转写、对精度要求不高 |
| 标准版 | `--model standard` | 快 | 良好 | **日常视频字幕（默认推荐）** |
| 专业版 | `--model pro` | 中等 | 高 | 会议记录、多人对话、访谈 |
| 深度版 | `--model deepthink` | 慢 | 最高 | 方言、专业术语、口音较重 |

## 常见问题

**Q: 字幕烧入后显示方块/乱码**
A: 安装中日韩字体：`sudo apt install fonts-noto-cjk`，然后重新运行。

**Q: 字幕和语音对不上**
A: 建议使用 `--model pro` 或 `--model deepthink` 获取更精确的时间戳。

**Q: 报错 `积分不足`**
A: SenseAudio API 积分用完了，到 https://senseaudio.cn 充值或等待每日免费额度刷新。

**Q: 报错 `ffmpeg: command not found`**
A: 安装 ffmpeg：`sudo apt install ffmpeg`
