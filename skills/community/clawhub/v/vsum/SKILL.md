---
name: vsum
description: 视频 summarizer，支持 YouTube 和 Bilibili 视频自动获取字幕并 AI 总结，输出为 md 格式。适用于：用户给出一个视频链接，希望总结内容。
---

# Vsum

快速获取 YouTube/Bilibili 视频字幕并进行 AI 总结，输出 md 文件。

## 支持的平台

- YouTube
- Bilibili

## 依赖工具

- `yt-dlp` - 用于获取视频字幕
- AI API - 用于总结（支持 OpenAI、Anthropic、Google 等）

## 字幕获取命令

### YouTube

```bash
# 获取自动字幕（推荐）
yt-dlp --write-auto-subs --sub-lang en --skip-download "视频链接"

# 或者明确指定语言
yt-dlp --write-subs --sub-lang en --skip-download "视频链接"

# 列出可用字幕
yt-dlp --list-subs "视频链接"
```

**注意**: YouTube 需要使用 `--write-auto-subs` 才能下载自动生成的字幕。

### Bilibili

```bash
# 需要登录 cookie（浏览器需已登录 B站）
yt-dlp --cookies-from-browser chrome --write-subs --sub-lang ai-zh,zh-CN --skip-download "视频链接"

# 列出可用字幕
yt-dlp --cookies-from-browser chrome --list-subs "视频链接"
```

**注意**: B站字幕需要用户登录，需要使用 `--cookies-from-browser chrome` 从浏览器读取 cookie。

## 工作流程

1. **获取视频链接** - 用户提供 YouTube 或 Bilibili 链接
2. **识别平台** - 自动判断是 YouTube 还是 Bilibili
3. **获取字幕** - 使用 yt-dlp 获取字幕
4. **AI 总结** - 调用 AI API 对字幕进行总结
5. **输出 md** - 将总结保存为 md 文件

## 字幕语言选择

### YouTube
- 优先: `en` (英语), `en-orig` (原始英语)
- 其他: 根据视频内容选择

### Bilibili
- 优先: `ai-zh` (AI 中文字幕), `zh-CN` (中文字幕)

## 常见问题

**Q: 视频没有字幕怎么办？**
A: 
- 尝试其他语言字幕
- 或告知用户该视频无法获取字幕

**Q: B站提示需要登录怎么办？**
A: 确保浏览器已登录 B站，使用 `--cookies-from-browser chrome` 读取 cookie

**Q: YouTube 下载失败怎么办？**
A: 尝试添加 `--write-auto-subs` 而非 `--write-subs`

**Q: 支持哪些 AI 提供商？**
A: 支持任何 OpenAI 兼容格式的 API（如 OpenAI、Anthropic、OpenRouter、jiekou.ai 等）。

## 输出格式

```markdown
# [视频标题]

> 来源: YouTube/Bilibili | 时长: XX:XX

## 总结

[AI 生成的视频总结]

## 关键要点

- 要点 1
- 要点 2
- 要点 3

---

*总结时间: YYYY-MM-DD*
```

## 长视频处理

对于长视频（字幕内容较多）：
1. **先做预览** - 只总结视频开头部分（约 30前% 内容）
2. **询问用户** - "这是视频的开头总结，需要我继续总结完整内容吗？"
3. **如需完整** - 可以分段处理，或使用支持长上下文的 AI

### 分段总结（可选）

如果用户需要完整总结，可以：
1. 将字幕分成 2-3 个部分
2. 分别发送 AI 总结
3. 最后合并成一个完整的总结

## 示例对话

用户："帮我总结这个视频 https://youtu.be/xxx"

1. 识别为 YouTube 视频
2. 使用 yt-dlp 获取字幕（加 --write-auto-subs）
3. 调用 AI 总结
4. 询问用户保存路径或直接保存到桌面/下载目录
