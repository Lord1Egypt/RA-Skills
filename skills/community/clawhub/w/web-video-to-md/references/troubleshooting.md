# 故障定位与修复

先判断失败发生在**下载阶段**还是**转写阶段**：看 `<work-dir>/media/_video-fetch.log`（下载）与 `<work-dir>/web-video-to-md-receipt.json`（转写）。

## 下载阶段

### HTTP 412 Precondition Failed

- 出现在 B 站，逐集全报。原因是 yt-dlp 过旧，不是 Cookie 问题。
- 处理：脚本会自动升级并重试一次；手动处理时 `python -m pip install -U yt-dlp`。
- 确认版本：`yt-dlp --version`（日期版本号）。超过 90 天即视为过期。

### 403 / “Sign in to confirm you’re not a bot”

- YouTube 的反爬限流。加 `--cookies-from-browser chrome:Default`（浏览器须已登录）；仍失败就换时段或降清晰度。
- 同一主机短时间大量请求容易被限流，大批下载时加 `--limit-rate 2M` 并分批。

### 只下到 1 集

- 检查是否传了 `--no-playlist`。默认会展开合集。
- 链接本身若是单视频（不含分P），那 1 集就是正确结果，先用 `--probe` 确认条目数。

### 格式合并 / 抽音轨失败

- 报 “ffmpeg not found” 或 “Postprocessing: ffmpeg exited” → 传 `--ffmpeg-location <ffmpeg 所在目录>`（含 ffmpeg.exe 的目录，不是 exe 本身）。
- 只要文稿时用 `--audio-only`，避免高清流的合并环节。

### 会员 / 付费 / 版权内容

- 只能让用户先登录后传 Cookie 下载其**有权访问**的内容。不要尝试绕过付费墙或 DRM。

### 残留 .part 文件

- 说明该集没下完。回执 `partialFiles` 会列出。补下该集即可，不要整批重来；同一命令重跑时，已完成的条目会被跳过。

## 转写阶段

### 转写超时

- 默认单项超时 1800 秒。长录像加 `--media-timeout-seconds 3600`；单文件超过 180 分钟还要加 `--max-audio-minutes 300`（MarkItDown 的预检上限）。
- 想更快：换 `--whisper-model tiny`，或用 GPU 环境。

### 没有产出 Markdown / 输出为空

- 检查媒体是否真的有音轨：无音轨、静音、纯音乐的音视频本就没有文字可提取，MarkItDown 会给出对应结论，如实告知用户即可，不要编造内容。
- 视频文件很大但音轨正常却失败时，先单独转成音频（`--audio-only`）再转写，能绕开解复用问题。

### MarkItDown 报版本可用（退出码 3）

- 先询问用户是否更新；同意则走平台技能更新入口安装 `@org-qu1qhx78/markitdown`；用户明确拒绝后追加 `--allow-current-version` 重跑。

### 转写质量

- 专有名词（产品名、模型名、人名、缩写）容易被听错。有字幕时用 `--sub-langs` 取官方字幕交叉校对；没有字幕时，交付摘要里主动提示用户抽查术语。
- 已知语言显式指定 `--whisper-language en` / `zh`，能减少语种误判。
