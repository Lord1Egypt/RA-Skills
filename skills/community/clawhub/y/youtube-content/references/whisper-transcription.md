# Whisper Transcription Reference

Whisper 音频转录的详细参考文档。本文档记录所有已知的坑点和解决方案，供实际操作时查阅。

## Setup

```bash
pip install faster-whisper
```

faster-whisper 比原版 openai-whisper 快 4 倍，内存占用更少。依赖 ctranslate2（自动安装）。

## 模型选择

| Model | VRAM | 速度 | 质量 | 适用场景 |
|-------|------|------|------|----------|
| base | ~1GB | 最快 | 一般 | 快速检查、英文 |
| small | ~2GB | 快 | 良好 | 英文内容 |
| medium | ~5GB | 中等 | 很好 | **中文、多语言**（推荐） |
| large-v3 | ~10GB | 慢 | 最佳 | 精度关键任务 |

## 已验证的性能数据（medium, CPU int8, macOS）

**单进程（solo）运行：**
- 24.6min 音频 → ~12-15min
- 47.9min 音频 → ~22-25min
- 平均比率：~0.5-0.8x 实时

**⚠️ 并行灾难（实测 2026-05-30，46视频批次）：**
- 两个 Whisper 并行：每个进程变为 1.5-1.7x 实时（3倍慢于 solo）
- 24.6min → 42min（vs solo 15min = **3倍惩罚**）
- 47.9min → 66min（vs solo 25min = **2.6倍惩罚**）
- 33个视频 + 2并行：总耗时 ~3小时（vs 顺序 ~1.5小时）
- 额外浪费 ~16分钟模型重载（33 × ~30s，batch_whisper.py 可避免）

**结论：永远顺序执行 Whisper。**

## faster-whisper 用法模式

### 基础转录

```python
from faster_whisper import WhisperModel

model = WhisperModel('medium', device='cpu', compute_type='int8')
segments, info = model.transcribe('audio.mp3', language='zh', beam_size=5, vad_filter=True)

for seg in segments:
    print(f'[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text}')
```

### 关键参数

- `language`: 显式设置（'zh', 'en'）跳过语言检测，更快更准
- `beam_size`: 5 是好的默认值，越高越慢但更准
- `vad_filter=True`: 跳过静音段，对有停顿的语音显著加速
- `compute_type`: CPU 用 `int8`（最快），GPU 用 `float16`

## ⚠️ 已知坑点

### 后台脚本的 Import 陷阱

`terminal(background=true)` 的 `python3 -c` 脚本是独立进程，不继承 session 的 import。**两种正确写法：**

```bash
# ✅ Option A — from-import
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('medium', device='cpu', compute_type='int8')
"

# ✅ Option B — module-qualified
python3 -c "
import faster_whisper
model = faster_whisper.WhisperModel('medium', device='cpu', compute_type='int8')
"
```

**三种错误写法：**
- ❌ 没写 import → `NameError: name 'WhisperModel' is not defined`
- ❌ `import faster_whisper` 但用了 `WhisperModel(...)` 而非 `faster_whisper.WhisperModel(...)`
- ❌ 复制粘贴时丢失 import 行

### `info.num_segments` 不存在

`TranscriptionInfo` 对象没有 `num_segments` 属性。可用属性：
- `info.language` — 检测到的语言代码
- `info.language_probability` — 置信度
- `info.duration` — 音频时长（秒）

计数需要手动遍历 segments。

### stdout 缓冲

后台模式下 Python stdout 是全缓冲的，`print()` 不会立即显示。用 `flush=True` 缓解，但底层 ctranslate2 进度回调可能仍然内部缓冲。

**建议：** 不要依赖实时进度。用音频时长 × 1x 作为估算。

## 截断转录（静默部分失败）

Whisper 可能提前终止（OOM kill、信号、资源压力），产出合法但只覆盖部分音频的文件。**无错误信息。**

**验证方法：** 检查最后 segment 的结束时间 vs `info.duration`。覆盖率 <90% 则重跑。

## 空文件转录（静默完全失败）

Whisper 可能正常退出（exit code 0）但产出 0 字节的 `.txt` 文件。（已验证：`ruTdFsbPHgk`，2026-05-30）

**验证方法：**
```bash
if [ ! -s "${VID}.txt" ]; then echo "⚠️ EMPTY: ${VID}.txt — re-run needed"; fi
```

**恢复：** 删除空文件并重跑，重试通常成功。

## yt-dlp 详细坑点

### macOS 代理问题

yt-dlp **不继承** macOS 系统代理设置。YouTube 从本网络不可达，必须显式传 `--proxy`。

```bash
# 检查当前代理端口
networksetup -getwebproxy Wi-Fi
# → Enabled: Yes / Server: 127.0.0.1 / Port: 64251
```

**端口不固定**，取决于 VPN/代理工具。不用代理时 yt-dlp 无限挂起。

### 双版本陷阱

macOS 上有两个 yt-dlp 安装：
- `/opt/homebrew/bin/yt-dlp` — Homebrew 版，**旧**（2025.11.12）
- `/opt/homebrew/Caskroom/miniconda/base/bin/yt-dlp` — pip 版，**新**（2026.03.17+）

裸 `yt-dlp` 命令解析到旧的 Homebrew 版本。**始终用 conda 版本：**
```bash
/opt/homebrew/Caskroom/miniconda/base/bin/python3 -m yt_dlp ...  # 最安全
/opt/homebrew/Caskroom/miniconda/base/bin/yt-dlp ...             # 也可
```

### YouTube 反爬："Sign in to confirm you're not a bot"

两种子问题：

**1. 无 cookies（公开视频被当 bot）**
修复：conda yt-dlp + `--cookies-from-browser chrome` + `--remote-components ejs:github`

**2. 视频需要登录（LOGIN_REQUIRED）**
无 cookies 绕过方案。`--cookies-from-browser chrome` 是唯一可靠方法。

**Chrome cookie 解密可能静默失败**（返回 0 cookies）。验证 Chrome 已登录 YouTube。

### Members-only 内容

```
ERROR: [youtube] VIDEO_ID: Join this channel to get access to members-only content
```
无法绕过，立即告知用户需要频道会员。

### 不要尝试的方案

| 方案 | 问题 |
|------|------|
| 手动解密 Chrome v10 cookies | `security find-generic-password` 一致性失败 |
| cobalt.tools | 不支持 LOGIN_REQUIRED，被 bot 检测拦截 |
| pytube | 不支持 LOGIN_REQUIRED |
| Invidious 实例 | 从中国不可达 |

## 文件命名约定

```
youtube_downloads/
  {VIDEO_ID}.zh-CN.srt    # 字幕
  {VIDEO_ID}.mp3           # 音频
  {VIDEO_ID}.txt           # Whisper 转录
  {VIDEO_ID}_notes.md      # 结构化笔记
```
