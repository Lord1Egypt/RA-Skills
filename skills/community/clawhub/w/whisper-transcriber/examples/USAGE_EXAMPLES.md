# 使用示例

## 🎯 常见场景

### 1. 转写会议录音

```bash
# 转写并生成带时间戳的文本
./transcribe.sh meeting_20260306.ogg -v

# 输出为 SRT 字幕（可用于视频字幕）
./transcribe.sh meeting_20260306.ogg -s

# 输出到文件
./transcribe.sh meeting_20260306.ogg -o meeting_notes.txt
```

### 2. 批量处理采访录音

```bash
# 批量转写整个目录
./transcribe.sh ./interviews/ -b

# 批量转写并生成 SRT
./transcribe.sh ./interviews/ -b -s

# 批量转写到指定输出目录
./transcribe.sh ./interviews/ -b -o ./transcripts/
```

### 3. 视频字幕生成

```bash
# 生成 SRT 字幕文件
./transcribe.sh video_audio.ogg -s

# 然后可以用 ffmpeg 合并到视频
ffmpeg -i video.mp4 -i video_audio.srt -c copy -c:a aac -strict experimental video_with_subs.mp4
```

### 4. 播客/音频节目转文字

```bash
# 使用 large 模型提高精度
./transcribe.sh podcast_ep01.mp3 -m large -t

# 输出 JSON 格式（便于后续处理）
./transcribe.sh podcast_ep01.mp3 -j
```

### 5. 语音备忘录整理

```bash
# 快速转写（使用 tiny 模型）
./transcribe.sh memo.ogg -m tiny

# 清理临时文件
./transcribe.sh memo.ogg -c
```

### 6. 多语言内容

```bash
# 自动检测语言
./transcribe.sh mixed_language.ogg -l auto

# 指定英语
./transcribe.sh english_audio.ogg -l en

# 翻译成英语（从其他语言）
whisper-cli -m ./assets/models/ggml-base.bin -l zh --translate audio.ogg
```

---

## 🔧 高级用法

### 性能优化

```bash
# 使用 GPU 加速（默认已启用）
./transcribe.sh audio.ogg -v

# 指定线程数
whisper-cli -m model.bin -t 4 audio.wav

# 禁用 GPU（调试用）
whisper-cli -m model.bin --no-gpu audio.wav
```

### 精度优化

```bash
# 使用更大的 beam size
whisper-cli -m model.bin -bs 10 -bo 5 audio.wav

# 使用温度退火
whisper-cli -m model.bin -tp 0.2 -tpi 0.2 audio.wav
```

### 输出格式定制

```bash
# 纯文本（无时间戳）
./transcribe.sh audio.ogg -t -n

# SRT 字幕
./transcribe.sh audio.ogg -s

# JSON 格式
./transcribe.sh audio.ogg -j

# LRC 歌词格式
whisper-cli -m model.bin -olrc audio.wav
```

---

## 📊 脚本集成

### 在 Shell 脚本中使用

```bash
#!/bin/bash

# 转写并处理结果
transcript=$(./transcribe.sh audio.ogg -t 2>/dev/null)

# 保存到文件
echo "$transcript" > transcript.txt

# 发送到其他工具处理
echo "$transcript" | grep "关键词"
```

### 在 Python 中使用

```python
import subprocess

def transcribe(audio_file):
    result = subprocess.run(
        ['./transcribe.sh', audio_file, '-t'],
        capture_output=True,
        text=True
    )
    return result.stdout

# 使用
text = transcribe('audio.ogg')
print(text)
```

### 在 OpenClaw 中使用

```bash
# 自动处理 inbound 语音消息
./examples/openclaw-integration.sh test /path/to/voice.ogg
```

---

## 🎨 实际案例

### 案例 1：每日站会记录

```bash
# 每天自动转写站会录音
for file in ./standup/2026-03-*.ogg; do
    ./transcribe.sh "$file" -o "./notes/$(basename "$file" .ogg).txt" -t
done
```

### 案例 2：课程录像字幕

```bash
# 批量生成课程字幕
for video in ./lectures/*.mp4; do
    # 提取音频
    ffmpeg -i "$video" -q:a 0 -map a "/tmp/$(basename "$video" .mp4).ogg"
    
    # 生成字幕
    ./transcribe.sh "/tmp/$(basename "$video" .mp4).ogg" -s
    
    # 移动字幕文件
    mv "/tmp/$(basename "$video" .mp4).srt" "./subtitles/"
done
```

### 案例 3：语音日记搜索

```bash
# 转写所有日记
./transcribe.sh ./diary/ -b -t -o ./diary-text/

# 搜索特定内容
grep -r "重要关键词" ./diary-text/
```

---

## 💡 技巧与最佳实践

1. **选择合适的模型**
   - 日常使用：base（平衡）
   - 重要内容：large（高精度）
   - 快速测试：tiny（速度优先）

2. **音频质量**
   - 确保音频清晰，背景噪音小
   - 16kHz 以上采样率
   - 单声道即可

3. **批量处理**
   - 使用 `-b` 参数批量处理
   - 指定输出目录便于管理
   - 使用 `-c` 清理临时文件

4. **结果验证**
   - 重要内容人工校对
   - 使用 `-v` 查看详细输出
   - 对比不同模型的结果

---

_更多示例请参考 `SKILL.md` 和官方文档_
