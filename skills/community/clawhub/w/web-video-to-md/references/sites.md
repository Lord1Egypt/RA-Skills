# 各视频站点取流要点

按站点记录真正会影响下载成败的细节，避免每次都靠试错。

## B 站（bilibili.com）

- **合集 = 单视频多分P**。B 站的“合集”页面常指向一个 BV 号，其下是 `?p=1..9` 多个分P。yt-dlp 识别为 9 条 playlist，必须带 `--yes-playlist`（本技能默认带上），否则只下第 1 集。
- **HTTP 412 的头号原因不是 Cookie，而是 yt-dlp 版本过旧**。B 站会拒绝过期版本的播放地址接口，报 `HTTP Error 412 Precondition Failed`，且 9 集全军覆没。升级 yt-dlp 到当天版本即可恢复。`fetch_videos.py` 已内置这个判断与自动升级重试。
- 链接常带 `?vd_source=...&spm_id_from=...` 等跟踪参数，直接传给 yt-dlp 无害；出错时可截到 `https://www.bilibili.com/video/BVxxxx/` 再试。
- 清晰度：正式番号 BV 支持到 1080P（需登录）/ 4K（需大会员）。未登录时通常只给 360P–720P，要高清就加 `--cookies-from-browser chrome:Default`。
- 番剧、影视等 `ep` / `ss` 类链接支持不完整，常需要 Cookie 且仍可能失败；此时如实告知用户。
- 弹幕：`--write-subs` 取到的是字幕不是弹幕；弹幕需另用 `--write-comments`（得到 xml，MarkItDown 不解析，仅供人工参考）。

## YouTube

- 播放列表 URL 带 `list=PLxxxx`，默认展开全部；单视频 URL 只下 1 个。
- 部分客户端会触发 “Sign in to confirm you’re not a bot” → 加 `--cookies-from-browser`。
- 年龄限制内容必须登录并传 Cookie。
- 高分辨率（4K/8K）常是 DASH 分离流，必须合并 → 依赖 ffmpeg；只要音轨时用 `--audio-only` 更稳。
- 自动字幕：加 `--write-auto-subs --sub-langs en,zh-Hans`，质量一般，但适合给 ASR 结果做术语校对。

## 抖音 / 西瓜 / 快手等国内短视频

- 单个作品 URL 通常可直接下载；用户主页是 playlist，条目很多，先 `--probe` 确认数量再决定是否全下。
- 抖音的分享短链（`v.douyin.com/xxxx`）需先跟随跳转，yt-dlp 一般能处理；失败时让用户在浏览器打开后复制最终 URL。
- 图集类链接没有视频流，会返回无可下载格式，属正常。

## 微博 / 腾讯视频 / 爱奇艺等

- 微博视频一般可直接下载，清晰度有限。
- 腾讯视频、爱奇艺、优酷的长视频支持不稳定，会员与 DRM 内容下不动。**只下载用户自己有权访问的内容**，不要尝试绕过付费与版权保护。

## 通用建议

- 先用 `fetch_videos.py --probe` 看条目数与站点，再决定全量还是挑几集，避免一次拉几百个文件。
- 大批下载加 `--download-archive <归档文件>`，重跑时自动跳过已下过的条目。
- 网络不稳或间歇 412 时，先降清晰度（`--max-height 720`），再考虑 `--limit-rate 2M` 限速。
- 需要走代理时加 `--proxy http://127.0.0.1:7890`。
- 只做文字稿时一律加 `--audio-only`：省约 90% 流量，合并步骤更少，转写效果不受影响。
