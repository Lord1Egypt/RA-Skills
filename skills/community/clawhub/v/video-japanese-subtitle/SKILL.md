---
name: video-subtitle
description: 日语视频自动翻译烧录技能。将日语视频转换为中文硬字幕，完整流程：ffmpeg 提取音频 → Whisper 日语转录 → LLM 翻译日→中 → SRT 转 ASS → ffmpeg NVENC 烧录硬字幕 → 验证。触发条件：用户提到视频字幕、硬字幕、字幕烧录、日语视频翻译、whisper 字幕、ass 字幕、或要求处理 .mp4 视频加字幕。
---

# 视频字幕翻译烧录技能

## 工作流程（6 步）

```
📦 原始视频.mp4
  → 🎵 提取音频（ffmpeg，~10s）
  → 📝 Whisper 转录日语（~3-5min，base 模型）
  → 📝 LLM 翻译日→中（~2-3min，QClaw 网关）
  → 📝 SRT 转 ASS（<1s）
  → 🎬 NVENC GPU 烧录（~3-6min）
  → ✅ ffprobe 验证
```

## 运行方式

```powershell
# 默认路径运行
python C:\Users\liket\.agents\skills\video-subtitle\scripts\subtitle_translate.py

# 自定义路径（修改脚本顶部的配置变量）
# VIDEO_DIR      视频目录
# OUTPUT_DIR     输出目录
# FFMPEG_DIR     ffmpeg bin 目录
# QCLAW_GATEWAY  LLM 网关地址
# QCLAW_TOKEN    LLM 网关 Token
```

**环境要求：** ffmpeg（已加 PATH）、Python openai-whisper、Python deep-translator（MyMemory 回退用）

## 踩坑速查

| # | 错误 | 原因 | 解决 |
|---|------|------|------|
| 1 | `WinError 2 ffmpeg not found` | Whisper 内部调 ffmpeg 但 PATH 里没有 | 脚本开头 `os.environ["PATH"]` 加入 ffmpeg 目录 |
| 2 | `Unable to parse` SRT | ffmpeg ass 滤镜不支持 SRT | 先转 ASS（Step 4） |
| 3 | `Unable to parse original_size` | Windows `C:` 冒号被当分隔符 | **用相对路径 + `cwd=ass_dir`**（脚本已内置） |
| 4 | Whisper translate 质量差 | ja→zh 用 Whisper 翻译效果差 | 只转录，翻译交给 Step 3 LLM |
| 5 | **烧录后视频无字幕** | ffmpeg 静默失败（路径问题） | **必须用 ffprobe 抽检画面**，不能只看文件大小 |
| 6 | LLM 翻译条目数不匹配 | 输出格式不稳定 | 脚本内置兜底补空逻辑 |
| 7 | GBK 解码错误 | Windows 控制台默认 GBK | Python 脚本开头设 `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` |

## 关键实现细节

**Whisper PATH 修复（脚本内置）：**
```python
os.environ["PATH"] = r"E:\ffmpeg\SCP\ffmpeg-master-latest-win64-gpl\bin" + os.pathsep + os.environ["PATH"]
```

**烧录相对路径 + cwd（脚本内置）：**
```python
ass_dir = os.path.dirname(os.path.abspath(ass_path))
ass_filename = os.path.basename(ass_path)
subprocess.run(cmd, cwd=ass_dir)  # cwd 切到字幕目录，相对路径才有效
```

**ASS 字幕样式：** Microsoft YaHei UI，白字黑边（PrimaryColour `&H00FFFFFF`，Outline=2），底部居中。

**NVENC 自动回退 CPU：** GPU 编码失败时自动降级到 `libx264 -preset ultrafast`。

## 性能参考（RTX 4060）

| 步骤 | 30min 视频 |
|------|-----------|
| 提取音频 | ~10s |
| Whisper base | ~3-5min |
| LLM 翻译（~700条） | ~2-3min |
| SRT→ASS | <1s |
| NVENC 烧录 | ~3-6min |
| **合计** | **~10-15min/视频** |

## 验证命令

```bash
# 检查时长（必须，但不够）
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "output.mp4"

# 截帧验证字幕真的烧进去了（必须！）
ffmpeg -ss 00:05:00 -i "output.mp4" -vframes 1 -q:v 2 frame.jpg
# 然后用图片查看器确认画面底部有字幕
```

## 目录结构

```
视频目录\
 ├── 原始视频.mp4
 ├── output\                   ← 脚本输出目录（可自定义）
 │   ├── video_xxx_subtitled.mp4   成品
 │   ├── xxx_audio.wav              中间音频
 │   ├── xxx_subs.srt              日语原文
 │   ├── xxx_subs_zh.srt           中文翻译
 │   └── xxx_subs_zh.ass           中文 ASS
 └── final\                     ← 可手动建此目录存放成品
```

## 脚本特性

- 断点续传：每步检查文件是否存在，已完成则跳过
- 短 hash 文件名：绕过 Windows 260 字符路径限制
- NVENC/CPU 自动切换
- LLM + MyMemory 双翻译引擎（LLM 失败自动回退）

## 已知局限

- Whisper base 模型对混合音频（BGM+语音+音效）识别一般
- `--task translate`（ja→zh）翻译质量差，不用
- 当前只支持日语→中文，其他语言需修改 Whisper language 参数
- faster-whisper 替代 openai-whisper 可提升速度和内存效率（未来改进方向）
