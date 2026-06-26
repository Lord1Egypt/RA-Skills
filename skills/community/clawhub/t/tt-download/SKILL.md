---
name: tt-download
description: "解析巨量引擎素材中心 video_player 页面背后的签名视频地址，并可选下载为 MP4。"
homepage: https://docs.openclaw.ai/
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3"] },
        "primaryEnv": "",
        "install":
          [
            {
              "id": "brew-python",
              "kind": "brew",
              "formula": "python@3.11",
              "bins": ["python3"],
              "label": "Install Python 3 (brew)",
            },
          ],
      },
  }
---

# tt-download

解析巨量引擎素材中心 `video_player` 页面（`https://ad.oceanengine.com/material_center/outer/video_player?token=...`）背后隐藏的真实签名视频地址。该页面是 React SPA，通过 JS 注入 `<video src=...>`。工具可选将视频流保存到本地。

## 何时使用

当用户分享的 URL 匹配 `https://ad.oceanengine.com/material_center/outer/video_player?token=...` 时触发（或用户要求保存 / 获取 / 解析真实地址 / 下载该类视频时）。**不要**用于通用视频下载——yt-dlp / video-frames 已覆盖那些场景。

## 为什么需要专门的技能

`curl` / `requests` / `yt-dlp` 都无法获取真实地址：该页面是 React SPA，解析后的 `cc.oceanengine.com` 地址会设置一个 `vck_*` Cookie，最终 CDN 必须携带该 Cookie（否则返回 403 `X-Moat-Code 4119`），而且签名后的 `video-cn.oceanengine.com` URL 有效期仅约 5 分钟。本工具在 Headless Chrome 中渲染 SPA，手动跟随 302 以保留 Cookie，然后流式下载——整个过程端到端在同一个进程中完成。

## 快速开始

```bash
# 仅打印解析后的 URL（stdout，一行）
{baseDir}/scripts/tt-download 'https://ad.oceanengine.com/material_center/outer/video_player?token=...'

# 下载到本地文件
{baseDir}/scripts/tt-download '...token=...' -o video.mp4

# 从文件读取 URL（长 token 在命令行中不方便）
{baseDir}/scripts/tt-download @url.txt -o video.mp4

# 同时输出中间 cc.oceanengine.com 地址（stderr）
{baseDir}/scripts/tt-download @url.txt -o video.mp4 --show-intermediate
```

## 输出约定

- **stdout**：解析后的 `https://video-cn.oceanengine.com/...` URL（一行）。失败时为空。
- **stderr**：进度和错误信息。启用 `--show-intermediate` 时输出 `intermediate: <cc-url>`。下载成功时输出 `✅ 已下载 16.4 MB → video.mp4`。
- **退出码 0** = 成功；**1** = 提取或下载失败（token 过期、浏览器缺失、网络错误、CDN 返回 4xx/5xx）；**2** = 命令行参数错误。

如果用户只需要 URL，不带 `-o` 运行，将 stdout 返回给用户。如果需要文件，使用 `-o`。

## 文件结构

```
tt-download/
├── SKILL.md                     # 本文件（面向 Agent 的技能说明）
├── scripts/
│   ├── tt_download.py           # 核心工具（仅使用标准库）
│   └── tt-download              # Bash 启动包装 → exec python3
├── references/
│   ├── usage.json               # CLI 参数的机器可读描述 + 示例
│   ├── chrome-paths.json        # 各操作系统的浏览器发现路径（用于审计/扩展）
│   └── troubleshooting.md       # 故障排除矩阵（按需加载）
├── agents/
│   └── openai.yaml              # OpenClaw Skills UI 的界面元数据
└── LICENSE
```

## 参考文档（按需加载）

- 完整的参数规范、退出码和调用示例（机器可读格式）：读取 `{baseDir}/references/usage.json`。
- macOS / Linux / Windows 上的浏览器发现路径，或添加自定义浏览器位置：读取 `{baseDir}/references/chrome-paths.json`。
- 故障模式和恢复方法：读取 `{baseDir}/references/troubleshooting.md`。

## 注意事项

- 需要本机安装 Headless Chrome / Edge（自动检测默认安装路径）。唯一的硬性依赖是 `python3`。
- 无需 `pip install`——纯 Python 3.7+ 标准库实现。
- 签名 URL 中包含 `policy=` JWT 风格 token，有效期约 5 分钟。**提取和下载必须在同一进程中完成**——切勿缓存 URL 稍后使用。

## 发布到 ClawHub

```bash
clawhub publish ./tt-download --slug tt-download --name "tt-download" --version 1.0.0 --changelog "Initial release"
```

用户通过 `openclaw skills install tt-download`（或 `clawhub install tt-download`）安装。
