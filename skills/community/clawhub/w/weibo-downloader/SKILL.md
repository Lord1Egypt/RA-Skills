---
name: weibo-downloader
description: |
  微博图片+视频下载器。纯 Python requests 实现，支持标准链接和 fx 分享链接，
  自动绕过新浪访客系统，一键下载图文和视频。
  GitHub: https://github.com/belingud/weibo-downloader-skill
version: "1.0.0"
author: belingud
source_repo: "https://github.com/belingud/weibo-downloader-skill"
base_dir: weibo-downloader-skill
---

# 微博下载器 / Weibo Downloader

📱 一键下载微博图文+视频，纯 Python 实现，无需外部工具。

## 功能

- **图片下载** — 支持微博图文（九宫格、多图），自动按原始尺寸下载
- **视频下载** — 支持微博视频，自动降级兜底（mp4_hd_url → mp4_720p_mp4 → stream_url）
- **链接自动识别** — 自动识别链接类型：单条微博 / fx 分享链接 / m.weibo.cn 移动端链接
- **访客绕过** — 自动通过新浪 passport 生成访客 cookie，无需登录微博账号
- **Cookie 持久化** — 访客 cookie 365 天有效，自动缓存到 `storage/weibo_cookies.pkl`
- **批量下载** — 支持 `--batch` 模式从文本文件批量读取链接

## 使用方法

### 单条下载

```bash
python3 scripts/download.py "https://weibo.com/6133795297/5319988795934006"
python3 scripts/download.py "https://weibo.com/6133795297/5319988795934006" /path/to/save
```

### 批量下载

```bash
# links.txt 每行一个链接
python3 scripts/download.py --batch links.txt
python3 scripts/download.py --batch links.txt /path/to/save
```

### 支持的链接格式

- `https://weibo.com/USER/STATUS_ID` — 标准网页链接
- `https://mapp.api.weibo.cn/fx/XXXX.html` — fx 分享链接
- `https://m.weibo.cn/status/STATUS_ID` — 移动端链接

## 输出结构

下载的内容按微博自动归类：

```
保存目录/
├── 微博用户名_微博描述_1.jpg
├── 微博用户名_微博描述_2.jpg
├── 微博用户名_微博描述_video.mp4
```

文件名自动 sanitize，去除特殊字符。

## 依赖

- Python 3.8+
- `requests`（标准 HTTP 请求库）

无其他外部依赖，无需 ffmpeg、gallery-dl 或浏览器。

## 技术原理

1. **访客绕过**: POST `passport.weibo.com/visitor/genvisitor2` → 解析 `tid/sub/subp` → 重定向获取 `SUB/SUBP` cookie（365 天有效）
2. **API 调用**: `weibo.com/ajax/statuses/show?id={status_id}` 获取微博详情
3. **媒体解析**: 同时支持新版 `mix_media_info` 和旧版 `pic_ids` 两种数据格式
4. **视频降级**: `mp4_hd_url` → `mp4_720p_mp4` → `stream_url` 三级兜底

## 许可证

MIT
