# 抖音竞品拆解 & 数据监控

抖音模块由两个独立脚本组成，服务两类需求。它们不合并、各跑各的。

| 需求 | 脚本 | 输入 | 产出 |
| --- | --- | --- | --- |
| 竞品/自号**数据**拆解 | [scrape_douyin.py](../../scripts/scrape_douyin.py) | 用户主页 URL | 账号+全部视频指标+评论的 JSON 与分析报告 md |
| 竞品**文风/内容**拆解、自号选题复盘 | [douyin_transcript.py](../../scripts/douyin_transcript.py) | 单条视频分享链接 | 口播稿 txt（转写+LLM 纠错）+ 转写原文 |

## 两个用途

**一、借鉴竞品**：想模仿某账号的文风、拆解其成功方法时——
先用 `scrape_douyin.py` 抓该账号全景（哪些选题数据最好、标题/评论规律），
再对数据最好的几条视频用 `douyin_transcript.py` 取回**口播稿原文**，喂给文稿/标题模块做风格分析。没有原文就谈不上模仿文风，这是关键一环。

**二、监控自己**：内容发布后，定期用 `scrape_douyin.py` 抓自己主页，
对比各条视频的完播/点赞/评论走势，反哺工作流迭代（哪类选题、哪种标题打法数据更好）。

## 怎么跑

```bash
pip install -r scripts/requirements-douyin.txt
playwright install chromium          # 仅 scrape_douyin 需要

# 数据抓取（扫码登录一次，session 会缓存）
python scripts/scrape_douyin.py --url https://www.douyin.com/user/MS4w...

# 单条视频 → 口播稿
python scripts/douyin_transcript.py "<抖音分享链接>"
```

Windows 控制台若报 GBK 编码错，加 `PYTHONUTF8=1` 前缀跑。

## 前置条件与红线

- **ffmpeg** 必须系统安装（`douyin_transcript` 抽音频用）。
- **TikTokDownloader**（GPL，未纳入本仓库）需单独 `git clone`，并把 `.env` 的 `TIKTOK_DOWNLOADER_DIR` 指向它；它需要一份**有效的抖音 cookie**（填在其 `Volume/settings.json`）。
- **凭证**：复制 [.env.example](../../.env.example) 为 `.env` 填入阿里云 AK/OSS/NLS 与 LLM 网关 key。`.env` 已被 gitignore，勿提交。
- **封号风险**：用个人 cookie 批量抓取竞品有风控风险，控制频率、自行评估。
- **成本**：`douyin_transcript` 每条视频都会调用 OSS+ASR+LLM，按量计费，不要无脑批量跑。
- **合规**：仅处理你有权处理的内容；竞品拆解用于学习方法，不是搬运。
