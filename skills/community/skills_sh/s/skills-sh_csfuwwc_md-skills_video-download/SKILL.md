---
name: video-download
description: Canonical social-video download skill for all supported platforms and table workflows. Always use this skill as the single download entrypoint when handling Douyin/抖音, Xiaohongshu/小红书, Bilibili/B站, TikTok, YouTube, Twitter/X, Instagram links, or when batch-processing Lark Base/Sheet rows that include social post URLs and need video files.
---

# 视频下载（抖音 / 小红书 / B站 + YouTube / Twitter 等）

## 统一入口原则（重要）

- 本 skill 是社媒视频下载的唯一入口。
- 当任务来自飞书多维表格（Base）/表格批处理时，下载动作也必须调用本 skill 的 `scripts/download.py`，不要在业务脚本里另写直连下载器。
- 需要正文/点赞/收藏时，可以在业务脚本里各自抓取；但“视频文件获取”必须复用本 skill 的下载链路与校验能力。

从分享链接下载视频到本地。抖音/小红书/B站使用 Playwright 无头浏览器，TikTok 优先使用真实浏览器 CDP 抓流，其他站点使用 yt-dlp。

## 下载流程

**重要：下载 B站视频前，必须先检查登录状态（未登录只能获取 480p）。**

先进入 skill 根目录后再执行以下命令（命令均使用相对路径）：

```bash
cd <your-skill-root>/video-download
```

### 步骤 1：检查登录状态（B站必须）

```bash
python3 ./scripts/download.py check-login bilibili
```

- 退出码 `0`（输出 `LOGIN_OK`）→ 直接跳到步骤 3 下载
- 退出码 `2`（输出 `LOGIN_REQUIRED`）→ 需要执行步骤 2 登录

### 步骤 2：交互式登录（需要时）

当 check-login 返回退出码 2 时，按以下流程操作：

1. **后台启动登录浏览器**（设置 block_until_ms: 0）：

```bash
python3 ./scripts/download.py login bilibili --signal-file /tmp/video_dl_login_done
```

2. **立即向用户展示确认按钮**，使用 AskQuestion 工具：
   - 提示：「已打开 B站 登录页面，请在浏览器中完成登录，完成后点击下方确认按钮。」
   - 选项 A：「已完成登录」
   - 选项 B：「跳过登录（使用低画质）」

3. **用户点击确认后**：
   - 选择 A：创建信号文件 `touch /tmp/video_dl_login_done`，等待登录脚本退出，然后继续下载
   - 选择 B：终止登录脚本进程，直接下载（低画质）

4. **兜底**：如果用户直接关闭了浏览器窗口，登录脚本会自动检测到并保存 cookie，无需信号文件。

### 步骤 3：下载视频

```bash
python3 ./scripts/download.py "<分享文本或链接>" [输出文件名.mp4]
```

## 平台支持

脚本自动识别平台，优先使用 Playwright，其余 fallback 到 yt-dlp：

| 平台 | 支持的链接格式 | 引擎 | 需要登录 | 备注 |
|------|---------------|------|---------|------|
| 抖音 | `v.douyin.com/xxx` 短链、`www.douyin.com/video/xxx`、`modal_id=xxx` | Playwright | 否 | 抓网络请求 |
| 小红书 | `xiaohongshu.com/discovery/item/xxx`、`explore/xxx`、`xhslink.com/xxx` | Playwright | 否 | 抓网络请求 |
| B站 | `bilibili.com/video/BVxxx`、`b23.tv/xxx` 短链 | Playwright | 推荐 | 解析 `__playinfo__`，需要 ffmpeg |
| TikTok | `tiktok.com/@user/video/xxx`、`vm.tiktok.com/xxx` | CDP→tikwm→yt-dlp | 推荐 | 优先真实浏览器 CDP；app-only/shop 场景自动尝试 tikwm 兜底 |
| YouTube | `youtube.com/watch?v=xxx`、`youtu.be/xxx` | yt-dlp | 否 | |
| Twitter/X | `x.com/xxx/status/xxx`、`twitter.com/...` | yt-dlp | 否 | |
| Instagram | `instagram.com/reel/xxx`、`instagram.com/p/xxx` | yt-dlp | 否 | 私密内容需登录 |
| 其他 | 任意视频链接 | yt-dlp | 视站点 | 支持 1700+ 站点 |

- 输出文件名可选，默认从视频标题生成
- 文件保存到 `~/Downloads/`
- 依赖：`playwright`（抖音/小红书/B站）、`yt-dlp`（其他站点）、`ffmpeg`

## TikTok 专项说明（CDP 优先）

脚本会优先尝试连接以下 CDP 端口抓取 `video/mp4` 响应体：
1. `VIDEO_DOWNLOAD_TIKTOK_CDP_ENDPOINT`（如果设置）
2. `http://127.0.0.1:9225`
3. `http://127.0.0.1:9222`

端口约定（团队规则）：
- 在 TikTok 批处理任务中，如果显式设置了 `VIDEO_DOWNLOAD_TIKTOK_CDP_ENDPOINT`，应把它视为唯一目标端口（例如 `9225`），不应在任务层再切换到其他端口进行重试。
- 当前团队默认 TikTok 端口为 `http://127.0.0.1:9225`。

若 CDP 抓取失败，会自动尝试 `tikwm` 解析；若仍失败，再按环境变量决定是否回退 `yt-dlp`。

失败重试策略（已内置）：
- 第一轮：`CDP -> tikwm`
- 第二轮（换路径重试一次）：`tikwm -> CDP`
- 仍失败时：按 `VIDEO_DOWNLOAD_TIKTOK_ALLOW_YTDLP_FALLBACK=1` 决定是否回退 `yt-dlp`

可通过环境变量指定端口：

```bash
VIDEO_DOWNLOAD_TIKTOK_CDP_ENDPOINT=http://127.0.0.1:9225 \
python3 ./scripts/download.py "<tiktok链接>" "output.mp4"
```

可选环境变量：

- `VIDEO_DOWNLOAD_TIKTOK_DISABLE_TIKWM=1`：禁用 tikwm 兜底
- `VIDEO_DOWNLOAD_TIKTOK_ALLOW_YTDLP_FALLBACK=1`：允许最终回退 yt-dlp

## TikTok 抓取元数据输出

每次 TikTok 成功下载后，会在视频旁边生成一个元文件：

- `<视频文件路径>.meta.json`

关键字段：
- `source`: `cdp` / `tikwm` / `ytdlp`
- `target_video_id`
- `resolved_video_id`
- `expected_duration`
- `actual_duration`
- `validation.id_ok`
- `validation.duration_ok`
- `validation.video_track_ok`

终端也会打印一行摘要，便于批处理写表：

`[TikTok/META] source=... id_ok=... duration_ok=... video_track_ok=...`

## 登录管理

```bash
# 登录（打开可见浏览器）
python3 ./scripts/download.py login bilibili

# 带信号文件的登录（Agent 交互模式用）
python3 ./scripts/download.py login bilibili --signal-file /tmp/video_dl_login_done

# 检查登录状态
python3 ./scripts/download.py check-login bilibili
```

Cookie 保存在 `~/.config/video-download/<平台>_cookies.json`，自动检测过期。

支持的平台: `bilibili` / `douyin` / `xiaohongshu`

## 依赖安装

```bash
pip3 install playwright && python3 -m playwright install chromium
brew install ffmpeg   # B站视频合并需要
brew install yt-dlp   # YouTube/Twitter/Instagram 等站点需要
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| SSL 证书错误 | 脚本已内置 `ssl._create_unverified_context` |
| 未捕获到视频地址 | 增加等待时间，或内容需要登录/是图文非视频 |
| curl/下载 403 | 检查 Referer 头是否匹配平台域名 |
| B站 ffmpeg 不存在 | `brew install ffmpeg` |
| B站画质低 | 执行 `login bilibili` 登录后重新下载 |
| CDN 地址过期 | 重新运行，URL 有几小时时效 |
| cookie 过期 | 重新执行 login 命令 |
| yt-dlp 未安装 | `brew install yt-dlp` 或 `pip3 install yt-dlp` |
