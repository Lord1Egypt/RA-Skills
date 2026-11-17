# video-to-text

把常见视频网站的链接一键转成**中文文字稿**（带时间轴 + 纯文字两版）的 Agent Skill。
兼容 [SKILL.md 标准](https://github.com/anthropics/skills)，可在 Claude Code、Codex CLI、Cursor、OpenClaw 等 20+ 代理中直接使用。

## 支持的站点

| 站点 | 链接形式 | 下载方式 |
|---|---|---|
| 抖音 | `v.douyin.com` 短链 / 长链 | yt-dlp 被拒后自动回退无头 Chromium 捕获直链 |
| B站 | `b23.tv` 短链 / BV 号 | yt-dlp 直接下载 |
| YouTube | `youtu.be` / `watch` 链接 | yt-dlp 直接下载 |
| 快手及其他 | 短链或长链 | yt-dlp 优先，失败自动浏览器回退 |

## 安装

```bash
pip install -r requirements.txt
python -m playwright install chromium   # 仅抖音类站点需要回退浏览器时用到
faster-whisper 首次运行会自动下载 small 模型（约 500MB）
```

## 用法

### 作为 Agent Skill

把本目录复制到 `~/.claude/skills/video-to-text/`（或对应代理的 skills 目录），
然后直接对代理说："提取这个视频的内容 https://v.douyin.com/xxxx"

### 命令行

```bash
python scripts/video_to_text.py "<视频链接>" [输出目录] [--model small] [--keep-media]
```

产出：
- `文字稿.txt` — 带时间轴 + 纯文字两版
- `meta.json` — 站点、标题等元信息

转写完成后自动清理中间音视频文件。

## 特性

- **双通道下载**：yt-dlp 优先，抖音等反爬站点自动切无头 Chromium 捕获媒体直链（优先纯音频轨，省 90% 流量）
- **长视频分段**：>8 分钟自动建议分段转写策略，段间重叠去重（见 SKILL.md）
- **中文优化**：VAD 过滤静音，常见同音术语校正（DeFi/NFT/区块链 等）
- **跨平台**：Windows / Linux / macOS，自动发现 Playwright Chromium

## 依赖

- Python 3.10+
- requests、imageio-ffmpeg（完整版 ffmpeg 二进制）、faster-whisper、yt-dlp、playwright

## License

MIT
