---
name: xhs-to-obsidian
description: "Extract Xiaohongshu (小红书) posts into Obsidian notes. Use when user shares a Xiaohongshu link and wants to save it as a markdown note. Supports single posts, batch extraction, and video transcription via whisper. Activates on: 小红书链接, xhs链接, 小红书帖子, RedNote links, or any URL from xiaohongshu.com."
---

# xhs-to-obsidian

把小红书帖子一键提取为 Obsidian Markdown 笔记。

## 核心流程

1. **检查 Cookies** → 2. **提取内容** → 3. **视频转录（如有）** → 4. **保存笔记**

## 常量定义

| 常量 | 默认值 |
|------|--------|
| Cookies | `~/.openclaw/xhs-cookies.json` |
| Obsidian 目录 | `~/Documents/Obsidian Vault/xhs` |

## Step 0: 检查并设置 Cookies

Cookie 文件不存在时，引导用户从 Chrome 导出：

1. 在 Chrome 打开 [xiaohongshu.com](https://www.xiaohongshu.com) 并登录
2. 打开 DevTools (F12) → Console
3. 运行以下代码复制 cookies：

```javascript
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return { name, value: rest.join('='), domain: '.xiaohongshu.com', path: '/',
    expires: Date.now()/1000 + 86400*30, size: name.length + rest.join('=').length,
    httpOnly: false, secure: false, session: false, priority: 'Medium',
    sameParty: false, sourceScheme: 'Secure', sourcePort: 443 };
})))
```

4. 保存到 `~/.openclaw/xhs-cookies.json`

## Step 1: 提取帖子

```bash
python3 {baseDir}/scripts/extract_post.py "<小红书URL>" --cookies ~/.openclaw/xhs-cookies.json --output ~/Documents/Obsidian\ Vault/xhs
```

输出为 JSON，包含 `success`、`filepath`、`type`（image/video）、`video_url` 等字段。

**错误处理：**
- `COOKIES_NOT_FOUND` → 引导用户导出 cookies（见 Step 0）
- `POST_NOT_AVAILABLE` → 帖子不可见（可能需要重新登录）
- `COOKIES_EXPIRED` → cookies 过期，重新导出

## Step 2: 视频转录（如帖子为视频）

如果返回 `type: video` 且包含 `video_url`，执行转录：

```bash
bash {baseDir}/scripts/video_transcribe.sh "<video_url>" "<post_id>" "<output_dir>"
```

转录完成后，将文本追加到笔记的 `## 视频转录` 段落。

**依赖（可选）：**
- `ffmpeg` — 音频提取
- `mlx-whisper` 或 `whisper` — 语音识别

安装：`brew install ffmpeg && pip install mlx-whisper`

## Step 3: 保存笔记

extract_post.py 已自动保存。如需手动整理，格式如下：

```markdown
# 标题（一句话洞察，非描述）

内容...

---

> **来源**: 小红书 · 作者名
> **日期**: YYYY-MM-DD
> **互动**: N赞 / N收藏 / N评论
> **标签**: tag1, tag2
> **链接**: https://www.xiaohongshu.com/explore/...
```

## 批量提取

多链接用换行分隔：

```bash
while read -r url; do
  python3 {baseDir}/scripts/extract_post.py "$url"
done <<EOF
https://www.xiaohongshu.com/explore/...
https://www.xiaohongshu.com/explore/...
EOF
```
