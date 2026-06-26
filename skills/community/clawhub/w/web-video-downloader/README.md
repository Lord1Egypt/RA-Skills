# 通用网页视频下载器 (Web Video Downloader)

输入任意包含视频的网页URL，自动检测视频源并下载为完整MP4文件。

## 支持的视频类型

| 类型 | 检测方式 | 下载方式 |
|------|----------|----------|
| 直链MP4 | `<video src="*.mp4">` | curl直接下载 |
| M3U8/HLS | 网络请求中`.m3u8` | ffmpeg下载合并 |
| 分段MP4 | CDP监听/API分析 | 逐段下载+concat protocol合并 |
| Blob URL | `blob:https://...` | CDP网络监听抓取实际请求 |

## 快速开始

### 方式一：一键下载（搜狐等已知API站点）

```bash
bash scripts/download_segmented.sh <vid> <output.mp4> --site sohu
```

### 方式二：CDP监听模式（通用，适用于任何网站）

```bash
# 1. 用浏览器打开视频页面
# 2. 获取CDP连接URL
# 3. 启动CDP监听
node scripts/cdp_capture.js <cdp_ws_url>

# 4. 在浏览器中播放视频（CDP会自动捕获请求）
# 5. 播放完毕后 Ctrl+C 停止监听

# 6. 从捕获的URL下载
bash scripts/download_from_urls.sh /tmp/captured_video_urls.json output.mp4
```

### 方式三：手动合并分片

```bash
# 下载分片后
bash scripts/merge.sh /tmp/segments output.mp4
```

## 核心技术：分段MP4合并

分段视频的最大问题是**moov atom缺失**——每个分片有独立moov，直接合并只有第一段可播。

**正确方案**：MP4→TS→concat protocol→MP4

```bash
# MP4 → TS（去除容器头）
ffmpeg -i seg.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts seg.ts

# concat protocol 合并（比concat demuxer更可靠）
ffmpeg -i "concat:seg0.ts|seg1.ts|...|segN.ts" \
  -c copy -bsf:a aac_adtstoasc \
  -movflags +faststart output.mp4
```

**为什么concat protocol而不是concat demuxer？** concat demuxer可能生成无moov的MP4文件，播放器只能识别第一段。concat protocol对TS流的字节级拼接更可靠。

## CDN Token过期处理

许多CDN的视频URL带有时效性token（20-30秒有效期）：

- ✅ 顺序下载，每5个分片刷新API获取新token
- ❌ 并行下载（token会同时过期）

## 文件结构

```
web-video-downloader/
├── SKILL.md                    # OpenClaw Skill定义
├── README.md                   # 说明文档
├── LICENSE                     # MIT License
└── scripts/
    ├── cdp_capture.js          # CDP网络监听脚本
    ├── download_segmented.sh   # 分段视频下载（支持sohu等API站点）
    ├── download_from_urls.sh   # 从URL列表下载（CDP捕获后使用）
    └── merge.sh                # 视频合并脚本
```

## 依赖

- curl
- ffmpeg（脚本自动下载静态版本）
- python3
- node（CDP监听需要）
- ws npm包（CDP WebSocket连接）

## 扩展新站点

在 `download_segmented.sh` 中添加新的站点处理函数：

```bash
download_yoursite() {
  # 1. 调用站点API获取分片列表
  # 2. 下载分片到 $OUTPUT_DIR/seg_XX.mp4
  # 3. 主流程会自动调用 merge_video() 合并
}
```

## License

MIT