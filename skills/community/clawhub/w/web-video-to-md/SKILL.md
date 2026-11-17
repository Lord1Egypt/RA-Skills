---
name: web-video-to-md
slug: web-video-to-md
category: productivity
description: 从 B 站、YouTube 等视频网站下载视频或音频，再用 MarkItDown 在本机转写成 Markdown。当用户给出视频链接并提出“下载视频”“把视频/网课/会议录像/播客转成 md、文字稿、笔记”，或要批量整理在线课程时使用；不做媒体格式转码，也不代替网页搜索与研究。
displayName: "网络视频转成md"
displayNameEn: "Web Video to Markdown"
display_name: "网络视频转成md"
display_name_en: "Web Video to Markdown"
descriptionZh: "下载在线视频与音频，并在本机转写成可检索的 Markdown 文字稿。"
descriptionEn: "Download online video and audio, then transcribe it into searchable Markdown locally."
description_zh: "下载在线视频与音频，并在本机转写成可检索的 Markdown 文字稿。"
description_en: "Download online video and audio, then transcribe it into searchable Markdown locally."
version: "1.0.0"
author: "WorkBuddy"
agent_created: true
---

# 网络视频转成 md

把在线视频变成两样东西：一份留存用的媒体文件，一份可检索的 Markdown 文字稿。下载交给 yt-dlp，转写交给 MarkItDown 技能，全程在本机完成，原文件不上传。

## 何时使用

- 用户给出 B 站、YouTube、微博、西瓜、腾讯视频等站点的链接，要“下载下来”“存到本地”。
- 用户要把网课、讲座、会议录像、播客、访谈“转成 md / 文字稿 / 笔记 / 可搜索的文本”。
- 用户要批量整理一个合集、一个播放列表或多集课程。

## 何时不用

- 只需要网页正文或资料检索 → 用搜索/研究工具，不要下载视频。
- 只是把已有本地音视频转 md → 直接用 MarkItDown 技能的 `convert_batch.py`，跳过本技能的下载阶段。
- 需要压制、剪辑、转码、抽帧等媒体处理 → 本技能不负责（只保留源画质媒体，或用 `--audio-only` 抽音轨）。

## 决策要点

| 用户实际诉求 | 做法 |
|---|---|
| 只要媒体文件 | `fetch_videos.py`，或 `video_to_md.py --skip-md` |
| 只要文字稿/笔记 | `video_to_md.py --audio-only`（只下音轨，省约 90% 流量与时间） |
| 媒体和 md 都要 | `video_to_md.py`（默认保留视频） |
| 只想知道合集有几集 | `fetch_videos.py --probe` |
| 已有本地媒体文件 | 直接用 MarkItDown 技能，跳过下载 |
| 媒体已下好，只想重跑转写 | `video_to_md.py --skip-download` |
| 只要其中几集 | 加 `--playlist-items 1-9` 或 `1,3,5` |

## 快速开始

以下 `<skill>` 指本次实际加载的 SKILL.md 所在目录，不要假设固定路径。

```powershell
# 全流程：下载 9 集合集 + 转写成 md
python "<skill>/scripts/video_to_md.py" --url "https://www.bilibili.com/video/BV1bt421578n/" --work-dir "E:/课程/Efficiently-Serving-LLMs"

# 只要文稿：只下音轨
python "<skill>/scripts/video_to_md.py" --url "https://youtu.be/XXXX" --audio-only --work-dir "./out"

# 只下载，先不转写
python "<skill>/scripts/fetch_videos.py" --url "https://www.bilibili.com/video/BV1bt421578n/" --output-dir "E:/视频" --max-height 1080

# 先探路：看看这个链接有几集
python "<skill>/scripts/fetch_videos.py" --url "https://www.bilibili.com/video/BV1bt421578n/" --probe
```

产物布局：媒体在 `<work-dir>/media`，Markdown 在 `<work-dir>/markdown`，总回执是 `<work-dir>/web-video-to-md-receipt.json`。用户的原始文件夹不会被中间文件塞满。

## 阶段一：下载（yt-dlp）

`fetch_videos.py` 负责下载。它是长任务，用后台运行，日志落到 `<media>/_video-fetch.log`。

环境由脚本自动处理，不需要手工排查：

- **定位 yt-dlp**：`--ytdlp` 指定 → PATH → 用户 pip 脚本目录 → 任一 Python 的 `-m yt_dlp`。全都找不到时，先 `python -m pip install -U yt-dlp` 再重跑。
- **定位 ffmpeg**：`--ffmpeg-location` → PATH → WinGet 安装目录 → 常见安装路径。找不到时合并与抽音轨会失败，脚本会先打印警告。
- **版本保鲜**：yt-dlp 用日期版本号（如 `2026.03.17`）。超过 90 天判定过旧，**B 站会直接返回 HTTP 412 拒绝服务**。脚本先自动升级再下载；下载中再遇到 412 / 403 / 429 / “Sign in to confirm you’re not a bot” / “Unable to extract”，会自动再升级一次并重试一遍。要用固定版本时加 `--no-update`。
- **合集与分P**：默认 `--yes-playlist`。B 站“合集”常是单视频的多个分P（`?p=1..9`），会被正确展开成 9 个文件；只要单个视频用 `--no-playlist`。
- **文件名**：合集默认 `NN - 标题 [id].ext`（带两位序号便于排序），单视频默认 `标题 [id].ext`；要纯 ASCII 文件名加 `--restrict-filenames`。
- **清晰度**：默认上限 1080p，用 `--max-height 720` 降低；要精确控制用 `--format "bv*[height<=720]+ba/b"`。
- **需要登录的内容**：先让用户在浏览器登录该站点，再加 `--cookies-from-browser chrome:Default`（Edge 写 `edge`，Firefox 写 `firefox`）；也可用 `--cookies <Netscape 格式 cookies.txt>`。
- **字幕**：站点有字幕时用 `--sub-langs zh-Hans,en`，自动生成字幕加 `--write-auto-subs`。字幕单独存成 srt/vtt，用来校对 ASR 把专有名词听错的地方。

各站点差异见 [references/sites.md](references/sites.md)。

## 阶段二：转写成 Markdown（MarkItDown）

`video_to_md.py` 自动发现 MarkItDown 技能的 `scripts/convert_batch.py`（用户技能目录 → 工作区技能目录 → 插件缓存目录）。发现不到时，传 `--markitdown-skill-dir <技能目录>`，或直接从该技能目录调用。

- **模型选择**：`--whisper-model` 默认 `base`（均衡）；`tiny` 最快、`small` 更准但更慢。参考速度：base 在普通 x86 CPU 上约 12 倍实时，2 小时音频约 10 分钟。
- **已知语言**：英文音轨加 `--whisper-language en`、中文加 `zh`，能明显减少误判；不确定时保持默认 `auto`。
- **长媒体**：默认单项超时 1800 秒，超长录像用 `--media-timeout-seconds` 提高；单文件超过 180 分钟还需加 `--max-audio-minutes 300`。
- **续跑**：中断后用同一 `--work-dir` 加 `--resume`，已完成的转写段落会复用。
- **版本提醒**：MarkItDown 每次会检查版本，有新版时 `video_to_md.py` 以退出码 3 结束。此时按 MarkItDown 技能约定，**先询问用户是否更新**；用户同意就走平台技能更新入口安装 `@org-qu1qhx78/markitdown`；用户明确拒绝后，追加 `--allow-current-version` 重跑。
- 转写只在本机进行，媒体文件不上传。

## 阶段三：校验与交付

1. 读总回执 `<work-dir>/web-video-to-md-receipt.json` 与 `<work-dir>/markdown/markitdown-batch-receipt.json`。
2. 核对 Markdown 数量与媒体数量一致；`outcome` 不是 `committed` 的项要向用户说明具体原因（`error.message` 与 `error.suggestion`）。
3. 扫描残留 `.part` 文件：有残留说明某集没下完，补下那一集，不要整批重来。
4. **术语校对**：语音转写会把专有名词听错（产品名、模型名、人名）。交付时主动提醒用户，并结合字幕文件校正明显错误。
5. 交付：列出 Markdown 文件路径与内容要点摘要，不要只说“已完成”。

## 常见故障速查

| 现象 | 处理 |
|---|---|
| HTTP 412 Precondition Failed | yt-dlp 过旧 → 脚本自动升级重试；仍失败时加 `--cookies-from-browser` 或 `--proxy` |
| 403 / “Sign in to confirm you’re not a bot” | YouTube 限流 → 加浏览器 Cookie，或换时段、降清晰度 |
| 只下到 1 集，明明有 9 集 | 默认已展开合集；若之前加过 `--no-playlist`，去掉它 |
| 会员/付费内容下不动 | 用户需先登录再传 Cookie；不要尝试绕过付费 |
| 合并失败 “ffmpeg not found” | 传 `--ffmpeg-location <目录>` |
| 转写超时 | 提高 `--media-timeout-seconds`；超长文件加 `--max-audio-minutes` |
| 输出为空 / 没有 md | 媒体无音轨、静音或纯音乐 → 本就没有文字可提取，如实说明 |

更多细节见 [references/troubleshooting.md](references/troubleshooting.md)。

## 资源

- `scripts/video_to_md.py`：下载 + 转写的一体化入口。
- `scripts/fetch_videos.py`：只做下载（含 `--probe`、Cookie、字幕、跳过已下载）。
- `scripts/_vtmd_common.py`：yt-dlp / ffmpeg 发现与版本保鲜，被上面两个脚本共用。
- `references/sites.md`：各视频站点的取流要点。
- `references/troubleshooting.md`：故障定位与修复。
