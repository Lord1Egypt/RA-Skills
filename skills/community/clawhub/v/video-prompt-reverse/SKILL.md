---
name: video-prompt-reverse
description: 视频提示词反推工具链。通过下载短视频 → 提取关键帧 → 批量上传豆包(PC)分析 → 输出结构化镜头语言提示词的全流程自动化。当用户提到"反推视频提示词"、"分析视频镜头语言"、"把视频转成AI绘图提示词"、"逆向视频分镜"时使用此技能。
---

# Video Prompt Reverse - 视频提示词反推

## 核心能力

将任意短视频（快手/抖音/本地视频）反推出 AI 绘图级别的结构化提示词，
覆盖：景别 / 机位 / 运镜 / 服装 / 色调 / 构图 / 场景氛围。

## 完整工作流（4步）

### Step 1 · 下载视频
**输入：** 视频URL或本地视频路径

```powershell
# 安装 yt-dlp（首次）
pip install -U yt-dlp

# 下载（默认 mp4，最长3分钟）
yt-dlp --max-duration 180 -f "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]" -o "video.%(ext)s" "URL"
```

> **注意：** PowerShell 执行含中文的 yt-dlp 命令前加 `$env:PYTHONIOENCODING="utf-8"`

### Step 2 · 提取关键帧
**输入：** 视频文件路径，输出：帧图目录

```powershell
# 分析视频参数（时长/帧率）
ffprobe -v quiet -print_format json -show_streams video.mp4

# 均匀提取关键帧（间隔 = fps × 建议秒数，推荐 40帧@29fps ≈ 1.4秒）
ffmpeg -i video.mp4 -vf "select='not(mod(n\,40))',scale=1280:-1" -vsync vfr "frames/f_%03d.jpg" -hide_banner
```

**帧文件命名规范：** `f_XXX.jpg`（XXX = 帧号，必须是 40 的倍数）
**帧目录：** 建议 `.\frames\`，先 `mkdir .\frames`

### Step 3 · 批量分析（豆包PC版 CDP）
**输入：** 帧图目录 + CDP Tab ID，输出：豆包文字回复

使用 `scripts/doubao_cdp.py` 脚本，上传多帧（至少4-5张，覆盖片头/中段/片尾），触发"解释图片"按钮批量分析。

**关键参数：**
- CDP Tab ID: `E7C2FA5DB0FB60DDD01D97EFAB45BCD8`（豆包PC版 Edge DevTools）
- 批量上传帧：选 `f_000 / f_080 / f_160 / f_200 / f_280` 等，覆盖全片
- 点击按钮用 JS 查找：`document.querySelectorAll('button')` 遍历匹配文字

**CDP 连接（scripts/cdp_client.py）：**
- 连接地址：`ws://127.0.0.1:9222/devtools/browser/...`
- 脚本文件路径统一用正斜杠（Python 可识别）

### Step 4 · 提取提示词
**输入：** 豆包回复文本，输出：结构化提示词

从豆包回复中提取关键元素，拼装为分镜格式：
```
[景别] [主体] in [场景], wearing [服装], [色调], [光线], [构图], shot on [设备], [运镜]
```
参考 `references/output_patterns.md` 中的提示词模板。

## 重要教训

- **PowerShell 中文编码：** 含中文的 Python 代码必须写成 `.py` 文件再执行，不要在 `-c "..."` 里直接写中文
- **CDP ref 失效：** `click_by_ref()` 的 ref 易过期，改用 JS 查找点击：`document.querySelectorAll('button')`
- **帧号必须是倍数：** `f_060` / `f_180` 不存在，正确是 `f_040 / f_080 / f_120 ...`

## 详细参考

| 参考文件 | 内容 |
|---------|------|
| `references/full_workflow.md` | 完整流程详解 + 工具参数 |
| `references/output_patterns.md` | 提示词输出格式模板 |
| `references/troubleshooting.md` | 常见问题排查指南 |
