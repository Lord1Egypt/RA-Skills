# 🎤 语音转文字工作流

## 环境准备（只需一次）

### 1. 安装 Whisper
```bash
pip3 install openai-whisper
```

### 2. 安装 ffmpeg（如果还没有）
```bash
brew install ffmpeg
```

---

## 使用方法

### 快速转录（默认 small 模型 + 中文）

```bash
# 复制下面这条命令，把 /path/to/xxx.wav 换成你的文件路径
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/your/audio.wav"
```

### 指定模型和语言

| 命令 | 说明 |
|------|------|
| `python3 ...transcribe.py "文件.wav"` | 默认 small 模型，自动检测语言 |
| `python3 ...transcribe.py "文件.wav" txt zh` | 指定输出 txt，语言中文 |
| `python3 ...transcribe.py "文件.wav" srt en` | 输出字幕格式，语言英文 |

### 输出格式

| 格式 | 说明 |
|------|------|
| `txt` | 纯文本（默认） |
| `srt` | 字幕文件（带时间戳） |
| `json` | 结构化数据（含置信度） |

### 可用模型

| 模型 | 大小 | 速度 | 准确度 |
|------|------|------|--------|
| `tiny` | ~75MB | 最快 | 较低 |
| `base` | ~140MB | 快 | 中等 |
| `small` | ~470MB | 中等 | 较好 |
| `medium` | ~1.5GB | 慢 | 好 |
| `large` | ~2.9GB | 最慢 | 最好 |

**推荐：** 音质好选 `large`，追求速度选 `small`

---

## 修改默认模型

如果想换默认模型，编辑文件：
```bash
nano ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py
```

找到这行：
```python
model = whisper.load_model('small')
```
改成你想要的模型名称，如 `'large'`

---

## 完整示例

### 示例 1：转录中文音频（默认配置）
```bash
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/Users/gg/Desktop/wav/audio_260522_170301_32bit_orig.wav"
```

### 示例 2：转录英文音频，输出字幕
```bash
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/english_audio.wav" srt en
```

### 示例 3：用 large 模型转录
```bash
# 先修改 transcribe.py 里的 model='large'
python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py "/path/to/audio.wav"
```

---

## 输出文件

转录结果会保存在音频文件同目录下，文件名加上 `_transcript` 后缀：

```
/path/to/audio.wav          →  /path/to/audio_transcript.txt
/path/to/audio.wav          →  /path/to/audio_transcript.srt
/path/to/audio.wav          →  /path/to/audio_transcript.json
```

---

## 快捷命令（推荐）

在 `~/.zshrc` 或 `~/.bashrc` 里加个别名，用起来更方便：

```bash
# 编辑配置文件
nano ~/.zshrc

# 添加别名（选一个你喜欢的名字）
alias trans="python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py"
alias transcribe="python3 ~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py"

# 生效
source ~/.zshrc
```

之后直接用：
```bash
trans "/path/to/audio.wav"
transcribe "/path/to/audio.wav" srt zh
```

---

## 故障排查

| 问题 | 解决 |
|------|------|
| `ffmpeg not found` | `brew install ffmpeg` |
| `whisper not found` | `pip3 install openai-whisper` |
| 转录太慢 | 换 smaller 模型，或用 GPU |
| 准确度低 | 音频质量差，换 better 模型 |

---

## 最佳实践

1. **音频质量决定转录质量** — 清晰的麦克风录音效果最好
2. **手机扬声器录制 → 再转录** — 效果会很差，如非必要别这样
3. **长音频会分段处理** — 耐心等待，不要中断
4. **首次运行会下载模型** — 需要网络，耗时约 1-5 分钟

---

## 文件位置

- Skill 脚本：`~/.openclaw/workspace/skills/audio-transcribe/scripts/transcribe.py`
- 本文档：`~/.openclaw/workspace/skills/audio-transcribe/README.md`