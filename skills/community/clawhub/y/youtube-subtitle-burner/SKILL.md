---
name: youtube-subtitle-burner
slug: youtube-subtitle-burner
displayName: YouTube 视频字幕烧录器
version: 1.1.0
summary: 下载 YouTube 视频，转录中文字幕并烧录到视频画面，支持抗锯齿渲染
license: MIT
description: 下载 YouTube 视频到本地，提取 word-level 时间轴，翻译为中文，用 PIL 逐帧烧录字幕到视频画面。支持 2x 超采样抗锯齿消除文字锯齿。适用于横屏和竖屏视频。最终输出带中文字幕的 H.264 MP4 文件，可直接上传到国内平台。
allowed-tools: Bash(uv:*), Bash(yt-dlp:*), Bash(ffmpeg:*), Bash(ffprobe:*)
---

# YouTube 视频字幕烧录器

下载 YouTube 视频 → 提取字幕时间轴 → 翻译为中文 → 烧录到视频画面（含抗锯齿）。

## 环境准备

### 必需依赖

```bash
# macOS
brew install ffmpeg yt-dlp

# uv（Python 环境管理，自动处理依赖）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Python 脚本使用 PEP 723 内联依赖声明（`# /// script`），`uv run` 会自动创建虚拟环境并安装依赖（如 Pillow），用户无需手动管理 Python 环境。

### 代理设置（中国大陆）

Clash Verge fake-ip 模式下 yt-dlp 必须显式设置代理：

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

代理不通时用 Clash unix socket 切换节点：

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock \
  -X PUT 'http://localhost/proxies/%F0%9F%93%B9%20YouTube' \
  -H "Content-Type: application/json" \
  -d '{"name":"⚡ 最快线路"}'
```

## 工作流程

### 第一步：下载视频

```bash
# 设代理（中国大陆必需）
export http_proxy=http://127.0.0.1:7890 https_proxy=http://127.0.0.1:7890

# 下载最高画质（mp4 容器通常已是 H.264）
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best" \
  --merge-output-format mp4 \
  -o "%(id)s_h264.mp4" \
  "YOUTUBE_URL"
```

⚠️ **不要用 `-f best`**，会拿到 360p。必须用 bestvideo+bestaudio 分流下载。

⚠️ **不要用 `--recode-video h264`**，新版 yt-dlp 报 `invalid recode video format "h264"`。下载后用 ffprobe 检查编码，如非 H.264 再单独 ffmpeg 转码：

```bash
codec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 VIDEO.mp4)
if [ "$codec" != "h264" ]; then
  ffmpeg -i VIDEO.mp4 -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart -y VIDEO_h264.mp4
fi
```

### 第二步：提取字幕时间轴（关键步骤）

⚠️ **必须用 json3 格式**，不能用 VTT。VTT 格式有 rolling cues（滚动字幕重复），直接解析会丢失开头字幕段，导致字幕延迟 2 秒以上。

```bash
# 下载 json3 格式自动字幕（word-level 精确时间轴）
yt-dlp --skip-download \
  --write-auto-subs \
  --sub-langs en \
  --sub-format json3 \
  -o "VIDEO_ID_json3.%(ext)s" \
  "YOUTUBE_URL"
```

然后运行解析脚本，将 json3 的 word-level 时间轴提取为句子段落：

```bash
uv run SKILL_DIR/scripts/parse_json3_subs.py \
  INPUT.json3 \
  OUTPUT_segments.json
```

输出格式：`[{"start": 0.00, "end": 3.26, "text_zh_src": "English sentence"}, ...]`

**参数说明：**
- 字幕按句号/问号/感叹号或 5 秒间隔分组
- 每段起始时间精确到该段第一个词的出现时间
- 首段从 0 秒开始（不会丢失开头内容）

### 第三步：翻译字幕

使用 LLM 将英文翻译为中文。批量处理（每批 20 条），规则：

- 译文简洁，适合视频字幕（≤20 中文字/段）
- 去除 `[music]` 等标签
- 专有名词保持原文（Claude, YouTube, Reddit 等）
- 输出在每段添加 `text_zh` 字段

```bash
uv run SKILL_DIR/scripts/translate_subs.py \
  INPUT_segments.json \
  OUTPUT_translated.json
```

> 注意：`translate_subs.py` 是批量调用 LLM 的辅助脚本。也可以直接用 agent/LLM 内联翻译，将 `text_zh_src` 翻译为 `text_zh`。

### 第四步：烧录字幕到视频（含抗锯齿）

这是核心步骤。ffmpeg 8.x 的 subtitles/ass filter 在某些平台不渲染，改用 Python PIL 逐帧绘制。

**字幕参数（已验证）：**

| 参数 | 横屏 (1920x1080) | 竖屏 (1080x1920) |
|------|:-:|:-:|
| 字体 | STHeiti Medium | STHeiti Medium |
| 字号 | 56px | 58px |
| 文字颜色 | 黑色 | 黑色 |
| 背景色 | 黄色半透明 (255,220,0,180) | 同左 |
| 每行最大字数 | 15 | 15 |
| 底部边距 | 60px | 200px |
| 圆角半径 | 8px | 8px |
| 超采样倍数 | 2x | 2x |

**字体路径：** `/System/Library/Fonts/STHeiti Medium.ttc`
（PingFang.ttc 在 PIL 中不可用，用 STHeiti Medium 替代）

**抗锯齿原理（2x 超采样）：**
1. 将每帧放大到 2 倍分辨率（如 1920x1080 → 3840x2160）
2. 在 2x 画布上用 2x 字号（112px）渲染字幕
3. 用 LANCZOS 算法缩回原始分辨率
4. 效果：文字边缘平滑，无锯齿

```bash
# 烧录字幕（含音频，流式管道不写临时文件）
uv run SKILL_DIR/scripts/burn_subtitles.py \
  --video INPUT_h264.mp4 \
  --subs INPUT_translated.json \
  --output OUTPUT_burned.mp4 \
  --font-size 56 \
  --supersample 2
```

**处理流程（流式管道）：**

```
ffmpeg 解码 → Python PIL 逐帧渲染字幕 → ffmpeg 编码
         （rawvideo pipe，不写临时文件）
```

⚠️ **不要写临时 raw 文件**，1080p × 30fps × 7分钟 ≈ 85GB，磁盘会满。

### 第五步（可选）：生成预览

烧录完整视频前，先做 10-15 秒预览让用户确认字幕效果：

```bash
uv run SKILL_DIR/scripts/burn_subtitles.py \
  --video INPUT_h264.mp4 \
  --subs INPUT_translated.json \
  --output /tmp/preview.mp4 \
  --font-size 56 \
  --supersample 2 \
  --preview 15
```

## 完整示例

```bash
# 1. 下载视频
export http_proxy=http://127.0.0.1:7890 https_proxy=http://127.0.0.1:7890
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best" \
  --merge-output-format mp4 -o "VIDEO_h264.mp4" "URL"

# ⚠️ 不要用 --recode-video h264（新版 yt-dlp 报错），下载后用 ffprobe 检查编码

# 2. 下载 json3 字幕
yt-dlp --skip-download --write-auto-subs --sub-langs en \
  --sub-format json3 -o "VIDEO_json3.%(ext)s" "URL"

# 3. 解析时间轴
uv run SKILL_DIR/scripts/parse_json3_subs.py VIDEO_json3.en.json3 VIDEO_segments.json

# 4. 翻译（用 LLM 翻译 text_zh_src → text_zh）
# ... agent 内联翻译或用 translate_subs.py ...

# 5. 预览（15秒）
uv run SKILL_DIR/scripts/burn_subtitles.py \
  --video VIDEO_h264.mp4 --subs VIDEO_translated.json \
  --output /tmp/preview.mp4 --font-size 56 --supersample 2 --preview 15

# 6. 烧录完整视频
uv run SKILL_DIR/scripts/burn_subtitles.py \
  --video VIDEO_h264.mp4 --subs VIDEO_translated.json \
  --output VIDEO_burned.mp4 --font-size 56 --supersample 2
```

## 常见问题

### 字幕延迟 / 不同步
原因：使用了 VTT 格式字幕。YouTube VTT 有 rolling cues（每段重复前一段内容），解析时会丢失开头段落。
解决：必须用 json3 格式（`--sub-format json3`），它包含 word-level 的 `tOffsetMs` 时间戳。

### 字幕有锯齿
原因：PIL 直接在原分辨率画布渲染文字，边缘有像素锯齿。
解决：启用 `--supersample 2`，在 2x 分辨率渲染后用 LANCZOS 缩回。

### 字幕太小看不清
横屏 1080p 用 56px（之前 22px 太小已废弃）。竖屏用 58px。

### ffmpeg subtitles filter 不工作
ffmpeg 8.x 的 subtitles/ass filter 在某些平台（macOS）不渲染。
解决：用 PIL 逐帧绘制（本方案已内置）。

### 磁盘空间不足
1080p 视频逐帧写 raw 临时文件约 85GB。
解决：burn_subtitles.py 使用流式管道（decode pipe → PIL → encode pipe），不写临时文件。

### 4K/高分辨率视频烧录极慢
2x 超采样在 4K 视频（2160x3840）上会放大到 4320x7680 处理，每帧约 100MB 内存，57 秒视频约需 10 分钟。
解决：如不需要 4K 输出，先降分辨率到 1080p 再烧录（快 10 倍以上）：
```bash
ffmpeg -i INPUT.mp4 -vf scale=1080:1920 -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 128k -y INPUT_1080p.mp4
```
然后再对 1080p 版本烧录字幕。

### yt-dlp `--recode-video h264` 报错
新版 yt-dlp 报 `invalid recode video format "h264"`。不要用 `--recode-video`，下载后用 ffprobe 检查编码，非 H.264 再单独 ffmpeg 转码。
