# video-notes

> 把任何 YouTube 视频变成一份精美的结构化笔记

粘贴一个 YouTube 链接，几分钟后你会得到一份带图表、截图和逐字稿的精美文档——不需要手动记一个字。

## 效果预览

输入：一个 YouTube 链接
输出：一份自包含的 HTML 文档，包含：

- **核心论点总结**（~300 字）：一句话主张 + 三条主线论据 + 关键预言
- **章节结构笔记**：SVG 图表、对比卡片、时间线
- **关键帧画廊**：自动截取重要时刻的视频截图，点击跳回 YouTube 原位置
- **全文字幕搜索**：实时高亮，点击任意一行跳到对应时间点

## 使用方式

在 Claude Code 里说：

```
帮我给这个视频做笔记 https://youtube.com/watch?v=...
```

## 依赖

- Python 3.8+
- `yt-dlp`（脚本自动安装）
- `ffmpeg`（关键帧截图需要，可选）

macOS 安装 ffmpeg：

```bash
brew install ffmpeg
```

## 适用场景

| 场景 | 说明 |
|---|---|
| 技术演讲 / 大会分享 | AI Ascent、TED、Google I/O 等 |
| 网课 / 公开课 | Coursera、MIT OpenCourseWare |
| 播客 / 长访谈 | Lex Fridman、各类深度对话 |
| 产品发布会 | WWDC、OpenAI DevDay 等 |
| 论文解读 | 作者在 YouTube 讲自己的论文 |
| 公司内部分享 | 录制视频归档为可搜索文档 |

## 文件结构

```
video-notes/
├── SKILL.md                    # Claude Code skill 定义和工作流
├── skill.json                  # ClawHub 元数据
├── scripts/
│   ├── extract_subtitles.py    # 字幕提取和去重
│   └── capture_keyframes.py    # 关键帧识别和截取
└── assets/
    └── note-template.html      # HTML 文档模板
```

## 迭代历程

- **v1**：字幕提取 + AI 结构化总结
- **v2**：SVG 图表 + 精美 HTML 文档 + 侧边导航
- **v3**：关键帧自动截图（仅下载关键片段，不下载完整视频）
- **v4**：执行摘要 + 完整阅读层次

## License

MIT
