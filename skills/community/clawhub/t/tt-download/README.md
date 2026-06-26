# tt-download 🎬

从巨量引擎（Oceanengine）素材中心 `video_player` 页面中提取真实视频地址并下载。

## 为什么需要这个工具？

素材中心的视频播放页（`https://ad.oceanengine.com/material_center/outer/video_player?token=...`）是一个 React SPA，真实视频地址由 JavaScript 动态注入到 `<video>` 标签中。直接用 `curl`、`requests` 或 `yt-dlp` 是拿不到的：

- 页面是 SPA，静态 HTML 中没有 `<video>` 标签
- 中间地址 `cc.oceanengine.com` 在 302 跳转时会下发 `vck_*` Cookie，最终 CDN 必须携带这个 Cookie，否则返回 `403`
- 最终的 `video-cn.oceanengine.com` 签名 URL 有效期仅 **约 5 分钟**，提取和下载必须一气呵成

本工具通过 Headless Chrome 渲染页面 → 手动跟随 302 保留 Cookie → 流式下载，端到端一次完成。

## 前置要求

- **Python 3.7+**（仅使用标准库，无需 `pip install`）
- **Chrome / Chromium / Edge** 浏览器（109+ 版本，自动检测默认安装路径）

支持的平台：macOS、Linux、Windows。

## 快速开始

```bash
# 仅打印解析后的真实视频地址（stdout 输出一行 URL）
./scripts/tt-download 'https://ad.oceanengine.com/material_center/outer/video_player?token=...'

# 下载到本地文件
./scripts/tt-download '...token=...' -o video.mp4

# 从文件读取 URL（token 很长时方便操作）
./scripts/tt-download @url.txt -o video.mp4

# 同时打印中间 cc.oceanengine.com 地址（输出到 stderr）
./scripts/tt-download @url.txt -o video.mp4 --show-intermediate
```

## 命令行参数

| 参数 | 说明 |
|---|---|
| `url` | 完整的 `video_player?token=...` URL，也支持 `@<文件路径>` 从文件读取 |
| `-o, --output <路径>` | 保存视频到指定文件；不传则只打印 URL |
| `--show-intermediate` | 同时输出中间 `cc.oceanengine.com` 地址（stderr） |
| `-h, --help` | 显示帮助信息 |

## 退出码

| 退出码 | 含义 |
|---|---|
| `0` | 成功（URL 已解析，如指定了 `-o` 则文件已下载） |
| `1` | 提取或下载失败（token 过期、浏览器缺失、网络错误等） |
| `2` | 命令行参数错误（URL 缺失或为空） |

## 输出说明

- **stdout**：解析后的 `https://video-cn.oceanengine.com/...` URL（一行），失败时为空
- **stderr**：进度和错误信息。下载成功时会显示 `✅ 已下载 16.4 MB → video.mp4`

## 工作原理

```
video_player?token=...  ──→  Headless Chrome 渲染 SPA
        │
        ▼
  <video src="cc.oceanengine.com/anm/...">  ← 从 DOM 中提取
        │
        ▼  手动跟随 302（保留 Set-Cookie: vck_*）
        │
video-cn.oceanengine.com/...  ← 签名视频 URL（有效期 ~5 分钟）
        │
        ▼
    流式下载到文件（携带 Cookie）
```

## 常见问题

### `未找到 Chrome / Chromium / Edge`

系统上没有安装受支持的浏览器。请安装 [Google Chrome](https://www.google.com/chrome/) 或 [Microsoft Edge](https://www.microsoft.com/edge)。

### `页面渲染后未找到 <video src=...> 标签`

Token 已过期或页面结构已变更。请在素材中心刷新页面，重新复制 `video_player?token=...` 链接。Token 有效期约 5 分钟。

### `HTTP Error 403: Forbidden`

下载时缺少 `vck_*` Cookie。正常情况下不会出现此问题，如遇到请提交 Issue。

### `HTTP Error 404`

签名 URL 已过期。重新运行即可。如反复出现，请检查系统时钟是否偏移过大，校正 NTP。

### Chrome 超时（`subprocess.TimeoutExpired`）

页面渲染卡住。可尝试降低脚本中的 `--virtual-time-budget` 参数值，或检查页面是否存在 JS 死循环。

## 项目结构

```
tt-download/
├── README.md                    # 本文件
├── LICENSE                      # MIT 许可证
├── SKILL.md                     # Agent 技能描述（供 AI 工具使用）
├── scripts/
│   ├── tt_download.py           # 核心脚本（纯标准库）
│   └── tt-download              # Bash 启动包装
├── references/
│   ├── usage.json               # CLI 参数的机器可读描述
│   ├── chrome-paths.json        # 浏览器发现路径（跨平台）
│   └── troubleshooting.md       # 故障排除详情
└── agents/
    └── openai.yaml              # OpenClaw UI 元数据
```

## 许可证

[MIT](LICENSE)
