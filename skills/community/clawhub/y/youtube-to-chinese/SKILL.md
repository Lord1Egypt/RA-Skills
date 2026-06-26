---
name: youtube-to-chinese
description: 将 YouTube 视频转成中文稿，包含完整中文转录、内容摘要和核心亮点。当用户提供 YouTube 链接并要求转录、翻译、生成中文稿、摘要或笔记时触发。Trigger phrases: YouTube转中文, 视频转文字, 转录视频, 生成中文笔记, 视频摘要, youtube transcript chinese.
---

# YouTube → 中文稿

将 YouTube 视频音频下载后，用 AI 转录并整理为结构化中文输出。

## 工作流程

### 第一步：下载音频

```bash
bash <skill_dir>/scripts/download_audio.sh "<YouTube_URL>" /tmp/yt-audio
```

脚本输出文件路径（stdout），失败时输出错误说明（stderr）并退出非零码。

**可选参数：**
- 第 3 参数传 cookies 文件路径（`/path/to/cookies.txt`）或 `browser:chrome`（从 Chrome 读取 cookies）
- 若遇到 bot 检测错误，见下方「常见问题」

### 第二步：AI 转录

用 `audios_understand` 工具转录音频文件：

```
audios_understand([{
  "file": "<第一步输出的文件路径>",
  "prompt": "请完整转录这段音频的所有内容，保留说话者的原意，不要遗漏任何部分。输出语言为中文。"
}])
```

> **注意：** `audios_understand` 是 OpenClaw 内置工具，直接传本地文件路径即可，无需上传。

### 第三步：整理输出

拿到转录文本后，整理为以下格式：

---

## 📝 完整中文稿

逐段输出，每段保留自然段落结构，确保语义完整、表达流畅（可适当润色，但不改变原意）。

---

## 📋 内容摘要

3-5 句话概括视频核心内容，包括主题、主要观点和结论。

---

## ✨ 核心亮点

- 亮点 1
- 亮点 2
- 亮点 3
- ...（5-8 条，每条一句话）

---

## 常见问题

**YouTube 下载失败（bot 检测 / 地区限制）**

1. 更新 yt-dlp：`curl -sL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /tmp/yt-dlp && chmod +x /tmp/yt-dlp`
2. 用浏览器 cookies：在第 3 参数传 `browser:chrome`（需在有 YouTube 登录状态的机器上运行）
3. 导出 cookies 文件：在 Chrome 安装 [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally) 扩展，导出后传路径

**视频过长（> 2小时）**

`audios_understand` 对超长音频可能截断。建议：
- 优先处理 < 60 分钟的视频
- 超长视频可用 `ffmpeg` 分段：`ffmpeg -i input.mp3 -t 3600 -c copy part1.mp3`

**音频文件清理**

处理完成后删除临时文件：`rm -rf /tmp/yt-audio /tmp/yt-test`
