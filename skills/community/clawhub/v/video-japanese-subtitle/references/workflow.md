# 视频字幕工作流（日→中硬字幕）

> 从日语视频到中文硬字幕的完整流水线，基于 2026-04-25 实战经验
> 环境：Windows 10 · RTX 4060 · Python 3.12

---

## 流程图

```
📦 原始视频.mp4
 │
 ▼  Step 1 — 提取音频
🎵 _audio.wav（16kHz 单声道 PCM）
 │
 ▼  Step 2 — 语音转录
📝 _subs.srt（日语原文，Whisper base）
 │
 ▼  Step 3 — LLM 翻译
📝 _subs_zh.srt（中文翻译，QClaw 网关）
 │
 ▼  Step 4 — 格式转换
📝 _subs_zh.ass（ASS 字幕，ffmpeg 必需）
 │
 ▼  Step 5 — 烧录硬字幕
🎬 video_xxx_subtitled.mp4（NVENC GPU 加速）
 │
 ▼  Step 6 — 验证
✅ ffprobe 确认时长 + 画面抽检
```

---

## 各步骤详解

### Step 1 · 提取音频

```bash
ffmpeg -i "视频.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 -y "audio.wav"
```

| 参数 | 含义 |
|------|------|
| `-vn` | 忽略视频轨 |
| `-acodec pcm_s16le` | 16 位 PCM 无压缩 |
| `-ar 16000` | 16kHz 采样率（Whisper 要求） |
| `-ac 1` | 单声道 |

⏱ ~10 秒 / 30 分钟视频

---

### Step 2 · Whisper 转录日语

**前置：把 ffmpeg 加进 PATH（Whisper 内部要调用）**

```python
import os
os.environ["PATH"] = r"E:\ffmpeg\SCP\ffmpeg-master-latest-win64-gpl\bin" + os.pathsep + os.environ["PATH"]
```

**转录**

```python
import whisper
model = whisper.load_model("base")
result = model.transcribe("audio.wav", language="ja", task="transcribe")
# task="transcribe" 只转录原文，不用 "translate"（ja→zh 质量极差）
```

**模型选择**

| 模型 | 显存 | 30min 耗时 | 日语质量 | 场景 |
|------|------|-----------|----------|------|
| base | ~1 GB | 3-5 min | 一般 ✅ | 批量处理（当前） |
| small | ~2 GB | 6-10 min | 较好 | 单视频精校 |
| large-v3 | ~10 GB | 20+ min | 最好 | 终极质量 |

⚠️ 不要用 `task="translate"` 做日→中，翻译交给 Step 3 的 LLM

⏱ ~3-5 分钟 / 30 分钟视频（base 模型）

---

### Step 3 · LLM 翻译日→中

把 SRT 条目按批发给 LLM，翻译后写回新 SRT（时间戳不变）。

- **翻译引擎**：QClaw 本地网关 `http://127.0.0.1:28789/v1/chat/completions`
- **批次大小**：每批 15 条
- **回退**：LLM 失败 → MyMemory API

```
SRT 条目 → 按 15 条分批 → 每批发给 LLM → 解析编号行 → 拼回 SRT
```

Prompt 模板：

```
System: 你是日语到简体中文的专业翻译器。只输出翻译结果，不加解释。保留编号格式。

User:
请将以下日语逐行翻译为简体中文，保留编号格式（1. 2. 3. ...），只输出翻译结果：

1. こんにちは
2. ありがとう
...
```

⚠️ LLM 输出条目数可能不匹配，需兜底补空

⏱ ~2-3 分钟 / 691 条字幕（47 批次）

---

### Step 4 · SRT → ASS 格式转换

**为什么必须转？** ffmpeg 的 `ass` 滤镜不认 SRT，直接用会报 `Unable to parse`

转换要点：
- SRT 时间 `00:00:05,000` → ASS 时间 `0:00:05.00`
- 换行符 `\n` → `\\N`
- 附加 ASS 头部（样式定义）

字幕样式：
- 字体：`Microsoft YaHei UI`，字号 36
- 白字黑边（PrimaryColour=`&H00FFFFFF`，Outline=2）
- 底部居中（Alignment=2）

⏱ <1 秒

---

### Step 5 · ffmpeg 烧录硬字幕

**⚠️ 最关键的一条：Windows 路径冒号问题**

ffmpeg 的 `ass` 滤镜会把 `C:\path` 里的冒号当参数分隔符，导致静默失败。

**解决方案：用相对路径 + `cwd` 切到字幕所在目录**

```python
ass_filename = os.path.basename(ass_path)   # 只取文件名
ass_dir = os.path.dirname(os.path.abspath(ass_path))  # 目录单独给 cwd

# GPU 加速（推荐）
cmd = [FFMPEG, "-y", "-i", video_path,
       "-vf", f"ass={ass_filename}",      # ← 相对文件名，不含盘符
       "-c:v", "h264_nvenc", "-preset", "p4", "-cq", "23",
       "-c:a", "copy",
       output_path]

subprocess.run(cmd, cwd=ass_dir)  # ← 关键：cwd 切到字幕目录
```

| 编码器 | 速度 | 质量 | 30min 耗时 |
|--------|------|------|-----------|
| `h264_nvenc`（GPU）| 6-10x 实时 | 好 | 3-6 min |
| `libx264 -preset ultrafast`（CPU）| 1-2x 实时 | 可接受 | 15-30 min |

GPU 不可用时自动回退 CPU。

⏱ ~3-6 分钟 / 30 分钟视频（GPU NVENC）

---

### Step 6 · 验证

```bash
# 检查时长
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "output.mp4"

# ⚠️ 不能只看时长！还要抽检画面确认字幕真的烧进去了
# （之前踩过坑：文件正常生成但画面无字幕）
```

---

## 踩坑速查表

| # | 问题 | 原因 | 解法 |
|---|------|------|------|
| 1 | `WinError 2 ffmpeg not found` | Whisper 内部调 ffmpeg 但 PATH 里没有 | 脚本开头 `os.environ["PATH"]` 加 ffmpeg |
| 2 | `Unable to parse` SRT | ffmpeg 不支持 SRT 格式 | 先转 ASS（Step 4） |
| 3 | `Unable to parse original_size` | Windows `C:` 冒号被当分隔符 | 相对路径 + `cwd` |
| 4 | PowerShell 日语文件名乱码 | 编码问题 | 用 Python 调 ffmpeg |
| 5 | 路径超 260 字符 | Windows MAX_PATH | 短 hash 文件名 |
| 6 | 进程 SIGKILL | 超时/内存 | 检查输出时长是否完整 |
| 7 | `\xa0` 空格 | non-breaking space | `.replace('\xa0', ' ')` |
| 8 | Whisper translate 质量差 | ja→zh 翻译不行 | 只转录 + LLM 翻译 |
| 9 | **烧录后视频无字幕** | ffmpeg 静默失败 | **必须抽检画面**，不能只看文件大小 |
| 10 | LLM 翻译条目数不匹配 | 输出格式不稳定 | 兜底补空 |
| 11 | GBK 解码错误 | Windows 控制台默认 GBK | `io.TextIOWrapper(encoding='utf-8')` |

---

## 性能参考（RTX 4060）

| 步骤 | 30min 视频 | 9 个视频 |
|------|-----------|---------|
| 提取音频 | ~10s | ~2 min |
| Whisper base | ~3-5 min | ~30-45 min |
| LLM 翻译 | ~2-3 min | ~15-25 min |
| SRT→ASS | <1s | ~5s |
| NVENC 烧录 | ~3-6 min | ~30-55 min |
| **合计** | **~10-15 min** | **~1.5-2 h** |

---

## 目录结构

```
D:\Users\liket\Desktop\000\
 ├── 原始视频.mp4            ← 不动
 ├── final\                  ← 成品
 │   └── video_xxx_subtitled.mp4
 └── temp\                   ← 中间文件（可删）
     ├── video_xxx_audio.wav
     ├── video_xxx_subs.srt         日语原文
     ├── video_xxx_subs_zh.srt      中文翻译
     └── video_xxx_subs_zh.ass      中文 ASS
```

---

## 一键运行

```powershell
python C:\Users\liket\.qclaw\workspace\subtitle_translate_v1.py
```

特性：自动扫描 · 断点续传 · NVENC/CPU 自动切换 · LLM+MyMemory 双翻译引擎

---

## 待改进

- [ ] 用 **faster-whisper**（CTranslate2 后端）替代原版 Whisper，更快更省内存
- [ ] 用 **large-v3** 模型提升混合音频（BGM+语音）识别率
- [ ] 烧录验证改为**截帧抽检**（当前只查时长，不够）
- [ ] 支持**双语字幕**（日语+中文上下排列）
- [ ] 封装为 QClaw Skill 一键调用
