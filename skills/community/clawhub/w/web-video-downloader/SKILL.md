---
name: web-video-downloader
description: |
  通用网页视频下载器。输入任意包含视频的网页URL，自动检测视频源（直链MP4/M3U8/分段流/Blob），抓取并下载为完整MP4文件。
  支持搜狐、B站、优酷等分段流视频，也支持直接MP4/M3U8链接。
  触发词：下载视频、download video、抓取视频、保存视频、视频下载、网页视频下载
keywords:
  - "下载视频"
  - "video download"
  - "抓取视频"
  - "分段视频"
  - "m3u8"
  - "mp4"
  - "合并视频"
  - "ffmpeg"
  - "blob video"
  - "stream download"
metadata:
  openclaw:
    emoji: "🎬"
---

# 通用网页视频下载器

## 功能

输入任意网页URL，自动检测视频源并下载为完整MP4文件。

支持的视频类型：
- **直链MP4**：`<video src="xxx.mp4">`
- **M3U8/HLS**：分片流，自动下载所有TS并合并
- **分段MP4**：搜狐等平台的分片流式传输，通过CDN调度API获取
- **Blob URL**：`blob:https://...`，通过CDP抓取实际网络请求

## 完整工作流

### 第一步：分析页面，识别视频类型

```bash
# 1. 初始化浏览器
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs init

# 2. 打开页面
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default --headed open '<URL>'

# 3. 等待加载
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default wait --load networkidle

# 4. 获取页面快照，检查视频元素
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default snapshot -i
```

### 第二步：根据视频类型选择下载策略

#### 策略A：直接MP4链接

```bash
# 提取video标签的src
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default eval "document.querySelector('video')?.src || document.querySelector('video source')?.src"

# 如果src是http直接链接，直接下载
curl -L -o output.mp4 "<video_url>"
```

#### 策略B：M3U8/HLS流

```bash
# 1. 通过CDP监听网络请求，找到m3u8地址
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default get cdp-url

# 用CDP WebSocket监听Network.requestWillBeSent事件，过滤.m3u8请求

# 2. 用ffmpeg下载m3u8（最可靠）
ffmpeg -i "<m3u8_url>" -c copy -movflags +faststart output.mp4
```

#### 策略C：分段MP4流（搜狐等）

```bash
# 1. 通过CDP监听网络请求，找到视频API或分片地址
# 2. 如果发现API模式（如sohu的play/videonew.do），调用API获取分片列表
# 3. 逐个下载分片，每5个刷新token
# 4. 合并：MP4→TS→concat protocol→MP4

bash scripts/download_segmented.sh <api_url_or_vid> <output_path>
```

#### 策略D：Blob URL + CDP网络监听（万能方案）

当视频src是blob:URL时，无法直接下载。必须通过CDP监听网络请求抓取实际的视频分片。

```bash
# 1. 获取CDP连接URL
node ~/Library/Application\ Support/QClaw/openclaw/config/skills/xbrowser/scripts/xb.cjs run --browser default get cdp-url

# 2. 用Node.js脚本通过CDP WebSocket监听网络请求
node scripts/cdp_capture.js <cdp_ws_url>

# 3. 在浏览器中播放视频（可能需要点击播放按钮）
# 4. CDP脚本会自动捕获所有.mp4/.m3u8/.ts请求URL

# 5. 播放完毕后，用捕获的URL下载
bash scripts/download_from_urls.sh <captured_urls_file> <output_path>
```

### 第三步：合并与验证

```bash
# 合并（如果是分段视频）
bash scripts/merge.sh <segments_dir> <output_path>

# 验证
ffmpeg -i output.mp4 -hide_banner 2>&1 | grep Duration
```

## CDP网络监听脚本详解

`scripts/cdp_capture.js` 是核心工具，通过Chrome DevTools Protocol监听浏览器的所有网络请求，过滤出视频相关的URL。

工作原理：
1. 连接到浏览器的CDP WebSocket
2. 启用Network域
3. 监听`Network.requestWillBeSent`事件
4. 过滤URL包含`.mp4`、`.m3u8`、`.ts`、`video`、`media`的请求
5. 同时捕获请求的Headers（含Referer和Cookie，下载时需要）
6. 输出捕获结果到JSON文件

**重要**：必须在视频播放期间运行CDP监听。对于长视频，建议：
- 让视频以1.5x-2x速度播放
- 或跳转到不同时间点触发各分片的加载
- 确保所有分片URL都被捕获

## 分段MP4合并原理

分段视频合并的关键问题是**moov atom**：

| 方案 | 结果 | 原因 |
|------|------|------|
| 二进制拼接MP4 | ❌ 只播第一段 | 每个分片有独立moov |
| ffmpeg concat demuxer | ❌ 可能无moov | 不保证正确生成索引 |
| **MP4→TS→concat protocol→MP4** | **✅** | **TS无容器头问题，concat protocol可靠拼接，最终正确生成moov** |

关键命令：
```bash
# MP4 → TS
ffmpeg -i seg.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts seg.ts

# concat protocol 合并
ffmpeg -i "concat:seg0.ts|seg1.ts|...|segN.ts" -c copy -bsf:a aac_adtstoasc -movflags +faststart output.mp4
```

## CDN Token过期处理

很多CDN（搜狐、优酷等）的视频URL带有时效性token，有效期通常20-30秒。

解决方案：
- **顺序下载**，每N个分片（建议5个）重新请求API获取新token
- 不要并行下载多个分片，token会同时过期
- 如果单个分片下载超时，刷新token后重试

## 依赖

- curl（下载）
- ffmpeg（合并/转码，脚本会自动下载静态版本）
- python3（辅助脚本）
- node（CDP监听脚本）

## 文件结构

```
web-video-downloader/
├── SKILL.md                    # Skill说明
├── scripts/
│   ├── cdp_capture.js          # CDP网络监听脚本
│   ├── download_segmented.sh   # 分段视频下载脚本
│   ├── download_from_urls.sh   # 从URL列表下载
│   └── merge.sh                # 视频合并脚本
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 只能播放5分钟 | moov atom缺失 | 重新用concat protocol合并 |
| 下载的分片为0字节 | CDN token过期 | 减少每批下载数量，更频繁刷新token |
| blob:URL无法下载 | blob是内存对象 | 用CDP监听网络请求 |
| M3U8下载卡住 | 网络或加密 | 尝试加`-headers`参数传Referer |
| 合并后花屏 | 时间戳不连续 | 重新编码：`-c:v libx264 -c:a aac`（慢但可靠） |