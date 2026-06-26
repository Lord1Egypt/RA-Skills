---
name: 微信公众号媒体下载器 WeChat Media Downloader
description: 下载微信公众号文章（mp.weixin.qq.com）中的视频、音频和音乐卡片。适用于：用户想把公众号文章里的 1 个或多个视频、多个音频/音乐保存到本地；直接抓取被微信“环境异常/去验证”拦截；需要通过可见 Chrome + 人工验证 + 远程调试抓取真实媒体地址，再自动下载、提取标题、重命名并整理输出。优先用于中文微信公众号内容场景。
---

仅在用户有权访问和保存目标媒体时使用。

## 核心思路

不要和微信反爬硬碰硬。最稳的成功路径是：

1. 先试普通抓取。
2. 一旦页面返回“环境异常 / 去验证”，立即切换为：
   - 可见 Chrome
   - 用户手动完成验证
   - 通过 DevTools 远程调试连接已打开页面
   - 抓取真实视频/音频地址
   - 下载并按文章顺序重命名

## 执行流程

### 1) 先判定是否被拦截

- 直接请求文章链接。
- 若返回微信验证页，不继续 headless 硬爬，直接进入人工验证路线。

### 2) 安装最小工具

优先用户级安装，不要求 sudo。

需要：
- `playwright`
- `yt-dlp`（可选；有时直接 HTTP 下载更稳）

推荐命令：

```bash
python3 -m pip install --user playwright yt-dlp
```

### 3) 让用户启动可见 Chrome

让用户执行：

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/openclaw-wechat-debug
```

然后让用户：
- 打开目标公众号文章
- 完成微信验证/登录
- 确认页面中的视频和音频能正常显示

### 4) 连接真实浏览器会话抓 URL

使用：
- `scripts/capture_wechat_media.py`

做法：
- 先读取 `http://127.0.0.1:9222/json/version`
- 取其中 `webSocketDebuggerUrl`
- 用 CDP 连入 Chrome
- 监听 request / response
- 同时保存页面 HTML

若只抓到视频没抓到音频：
- 让用户把每个音频都点一次播放
- 重新抓取

### 5) 下载媒体

- 视频：优先使用抓到的 `mpvideo.qpic.cn` 直链
- 音频：使用 `https://res.wx.qq.com/voice/getvoice?mediaid=<voice_encode_fileid>`

注意：
- 某些 MP4 直链用 `yt-dlp` 可能卡收尾；这时直接用 Python HTTP 流式下载反而更稳。

### 6) 提取标题并重命名

从文章 HTML 中提取：
- 文章标题
- `<mp-common-mpaudio ... name="..." voice_encode_fileid="...">`

按文章顺序输出成：
- `00. <视频标题>.mp4`
- `01. <音频标题>.mp3`
- `02. <音频标题>.mp3`
- ...

### 7) 交付与清理

- 把最终文件放入一个干净的新目录
- 可以清理：临时 HTML、JSON、`.part`、乱码副本、抓取脚本输出
- 不要默认删除最终交付目录

## 经验规则

- 微信公众号抓取的关键不是“更强的爬虫”，而是“接管已通过验证的真实浏览器会话”。
- 纯 headless 路线经常失败。
- 音频 URL 经常只有播放后才出现。
- 如果 `connect_over_cdp('http://127.0.0.1:9222')` 返回 400，不要死磕；先取 `/json/version` 里的 websocket 地址再连接。

## 自带资源

- `scripts/capture_wechat_media.py`：连接 Chrome 调试端口，抓取视频/音频请求与页面 HTML
- `scripts/download_wechat_media.py`：下载视频和音频，并根据文章内容重命名
- `references/reusable-workflow.md`：可复用操作清单与故障处理
