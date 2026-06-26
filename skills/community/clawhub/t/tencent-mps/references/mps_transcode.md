# 转码参数与示例 — `mps_transcode.py`

**功能**：视频转码、压缩、格式转换，支持 H264/H265/H266/AV1/VP9 等视频编码格式，以及 MP3/M4A 纯音频格式输出。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--local-file` | 本地文件路径，自动上传到 COS 后处理（与 `--cos-input-*` 互斥）|
| `--url` | 视频 URL 地址（HTTP/HTTPS）|
| `--cos-input-bucket` | 输入 COS Bucket 名称（与 `--cos-input-region`/`--cos-input-key` 配合，推荐）|
| `--cos-input-region` | 输入 COS Bucket 区域（如 `ap-guangzhou`）|
| `--cos-input-key` | 输入 COS 对象 Key（如 `/input/video.mp4`，**推荐**）|
| `--codec` | 视频编码格式：`h264` / `h265` / `h266` / `av1` / `vp9` |
| `--width` | 视频宽度/长边（px），如 1920、1280 |
| `--height` | 视频高度/短边（px），0=按比例缩放 |
| `--bitrate` | 视频码率（kbps），0=自动 |
| `--fps` | 视频帧率（Hz），0=保持原始 |
| `--container` | 封装格式：`mp4` / `hls` / `flv` / `mp3` / `m4a` |
| `--audio-codec` | 音频编码：`aac` / `mp3` / `copy` |
| `--audio-bitrate` | 音频码率（kbps）|
| `--compress-type` | 压缩类型：`ultra_compress` / `standard_compress` / `high_compress` / `low_compress` |
| `--scene-type` | 场景类型：`normal` / `pgc` / `ugc` / `e-commerce_video` / `educational_video` / `materials_video` |
| `--notify-url` | 任务完成回调 URL |
| `--output-bucket` | 输出 COS Bucket 名称（默认取 `TENCENTCLOUD_COS_BUCKET` 环境变量）|
| `--output-region` | 输出 COS Bucket 区域（默认取 `TENCENTCLOUD_COS_REGION` 环境变量）|
| `--output-dir` | 输出目录，默认 `/output/transcode/` |
| `--output-object-path` | 输出文件路径模板，如 `/output/{inputName}_transcode.{format}` |
| `--no-wait` | 仅提交任务，不等待结果（默认自动轮询）|
| `--poll-interval` | 轮询间隔（秒），默认 10 |
| `--max-wait` | 最长等待时间（秒），默认 1800（30 分钟）|
| `--download-dir` | 任务完成后将输出文件下载到指定本地目录（默认仅打印预签名 URL）|
| `--compare [路径]` | 任务完成后自动生成效果对比 HTML 页面；可选指定输出路径，省略则自动命名 |
| `--verbose` / `-v` | 输出详细信息 |
| `--region` | MPS 服务区域（优先读取 `TENCENTCLOUD_API_REGION` 环境变量，默认 `ap-guangzhou`）|
| `--dry-run` | 只打印参数，不调用 API |

## 强制规则

- **默认行为**：未指定任何编码参数时，脚本使用默认模板（H265 编码，MP4 封装），无需追问，直接执行
- **纯音频提取**：用户说"提取音频"、"转为 MP3/M4A" → 使用 `--container mp3` 或 `--container m4a`，不需要指定视频编码参数
- **压缩场景选择**：
  - 用户说"极致压缩"、"最大压缩"、"带宽优先" → `--compress-type ultra_compress`
  - 用户说"平衡压缩"、"综合最优" → `--compress-type standard_compress`
  - 用户说"码率优先"、"控制码率" → `--compress-type high_compress`
  - 用户说"画质优先"、"存档" → `--compress-type low_compress`
- **流媒体场景**：用户说"HLS 切片"、"流媒体播放" → 使用 `--container hls`

## 示例命令

```bash
# 最简用法：URL 输入 + 默认模板（极速高清-H265-MP4-1080P）
python scripts/mps_transcode.py --url https://example.com/video.mp4

# COS 路径输入（推荐，本地上传后使用）
python scripts/mps_transcode.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou \
    --cos-input-key /input/video.mp4

# 自定义参数：H265 编码 + 1080P + 3000kbps + 30fps
python scripts/mps_transcode.py --url https://example.com/video.mp4 \
    --codec h265 --width 1920 --height 1080 --bitrate 3000 --fps 30

# 极致压缩（ultra_compress）：最大程度压缩码率，适合带宽敏感场景
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type ultra_compress

# HLS 切片（用于流媒体播放）
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container hls

# 综合最优（standard_compress）：平衡画质与码率
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type standard_compress

# 码率优先（high_compress）：保证可接受画质的前提下尽量降低码率
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type high_compress

# 画质优先（low_compress）：保证画质的前提下适度压缩，适合存档
python scripts/mps_transcode.py --url https://example.com/video.mp4 --compress-type low_compress

# 提取音频（转为 MP3）
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container mp3

# 提取音频（转为 M4A，高质量）
python scripts/mps_transcode.py --url https://example.com/video.mp4 --container m4a --audio-bitrate 192

# 异步提交后查询任务状态
python scripts/mps_transcode.py --url https://example.com/video.mp4 --no-wait
python scripts/mps_get_video_task.py --task-id 1250017490-20260318152230-abcdef123456
```
