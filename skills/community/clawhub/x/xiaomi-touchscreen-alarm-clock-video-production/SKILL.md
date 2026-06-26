---
name: bilibili-video-download
description: B站视频下载裁剪压缩工具。下载bilibili视频、裁剪去除边框、压缩到指定大小时使用。支持b23.tv短链和BV号。别名：闹钟视频下载。
---

# 闹钟视频下载

## 依赖

- yt-dlp: `py -m pip install yt-dlp`
- bilix (备用): `pip install bilix --break-system-packages`
- ffmpeg/ffprobe: 需在PATH中

## 工作流

### 1. 下载视频

#### 方法A: yt-dlp（推荐，但可能遇到反爬虫）

固定下载720P分辨率视频（格式ID: 30064+30280），文件名使用BV号：
```
py -m yt_dlp -f "30064+30280" -o "PATH/%(id)s.%(ext)s" --merge-output-format mp4 URL
```
说明: 30064为720P视频流,30280为音频流。使用 `%(id)s` 自动提取BV号作为文件名，避免多个视频下载时文件名冲突。

**注意:** yt-dlp 可能遇到 HTTP 412 错误（B站反爬虫机制），此时使用方法B。

#### 方法B: bilix（备用，稳定性更好）

当 yt-dlp 返回 `HTTP Error 412: Precondition Failed` 时，使用 bilix 下载：
```bash
pip install bilix --break-system-packages
bilix get_video "https://www.bilibili.com/video/BV号" -d 输出目录
```

**b23.tv短链处理:** bilix 不直接支持短链，需先解析获取BV号：
```bash
curl -sI "https://b23.tv/短链ID" | grep -i location
# 从返回的location中提取BV号
```

### 2. 裁剪边框（可选）

使用裁剪参数去除B站视频边框，格式为 `宽:高:左:上`。

#### 720P视频固定参数

默认裁剪参数 `792:600:432:56`（针对1280x720视频）：
```
ffmpeg -y -i IN -vf "crop=792:600:432:56" -c:v libx264 -crf 18 -c:a copy OUT
```

#### 非720P视频裁剪参数计算

720P裁剪参数的比例：
| 参数 | 720P值 | 比例 |
|------|--------|------|
| 裁剪宽度 | 792 | 61.875% (0.61875) |
| 裁剪高度 | 600 | 83.33% (0.83333) |
| 左偏移 | 432 | 33.75% (0.3375) |
| 上偏移 | 56 | 7.78% (0.07778) |

**通用计算公式：**
```python
video_width = 852   # 实际视频宽度
video_height = 480  # 实际视频高度

crop_w = int(video_width * 0.61875)   # 裁剪宽度
crop_h = int(video_height * 0.83333)  # 裁剪高度
crop_x = int(video_width * 0.3375)    # 左偏移
crop_y = int(video_height * 0.07778)  # 上偏移

# 结果: crop=527:400:287:37
```

**常见分辨率适配参数：**

| 分辨率 | 裁剪参数 | 输出尺寸 |
|--------|---------|---------|
| 1280x720 (720P) | `792:600:432:56` | 792x600 |
| 1920x1080 (1080P) | `1188:900:648:84` | 1188x900 |
| 852x480 | `527:400:287:37` | 527x400 |
| 640x360 (360P) | `396:300:216:28` | 396x300 |

**裁剪命令示例（852x480视频）：**
```
ffmpeg -y -i IN -vf "crop=527:400:287:37" -c:v libx264 -crf 18 -c:a copy OUT
```

如无需裁剪，传入 `--no-crop`。

### 3. 剪切视频（可选，默认去除前后各10秒）

**步骤1: 去除前10秒**
```
ffmpeg -y -i IN -ss 00:00:10 -c:v libx264 -crf 18 -c:a copy TEMP
```

**步骤2: 获取剩余视频时长**
```
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 TEMP
```

**步骤3: 去除后10秒（总时长-10）**
```
ffmpeg -y -i TEMP -t (duration-10) -c:v libx264 -crf 18 -c:a copy OUT
```

说明: 固定去除片头10秒和片尾10秒，总时长减少20秒。如无需剪切，传入 `--no-trim`。

### 4. 压缩到目标大小

**目标：压缩到10MB以内**

**步骤1: 获取视频时长**
```
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 INPUT_VIDEO
```

**步骤2: 计算动态码率**
使用Python计算码率参数（以目标10MB为例）：
```python
target_MB = 10
duration = 217.345783  # 从步骤1获取的实际时长
vbr = max(int((target_MB * 0.9 * 8 * 1024) / duration - 64), 100)  # 视频码率
maxrate = int(vbr * 1.25)  # 最大码率
bufsize = int(vbr * 2.5)   # 缓冲大小
# 示例输出: vbr=275k, maxrate=344k, bufsize=688k
```

计算公式：
- 视频码率: `vbr = max(int((target_MB * 0.9 * 8 * 1024) / duration - 64), 100)`
- 最大码率: `maxrate = int(vbr * 1.25)`
- 缓冲大小: `bufsize = int(vbr * 2.5)`

**步骤3: 执行压缩**
```
ffmpeg -y -i INPUT_VIDEO -c:v libx264 -b:v 275k -maxrate 344k -bufsize 688k -c:a aac -b:a 64k -ar 44100 OUTPUT_VIDEO
```

**验证压缩结果:**
```
ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 OUTPUT_VIDEO
```

**实际案例参考:**
- 输入视频: 792x600, 时长217秒, 约22.4MB
- 压缩参数: vbr=275k, maxrate=344k, bufsize=688k
- 输出结果: 约9.0MB, 成功压缩到10MB以内

### 5. 一键脚本

```
py scripts/download_and_process.py URL [选项]
```

**必选参数:**
- `url` — B站视频URL（支持BV号、b23.tv短链）

**可选参数:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--format_id` | `30064+30280` | 下载格式ID |
| `--crop` | `792:600:432:56` | 裁剪参数（宽:高:左:上） |
| `--no-crop` | — | 跳过裁剪步骤 |
| `--no-trim` | — | 跳过去头尾步骤（默认去除前后各10秒） |
| `--max_size_mb` | `10` | 目标文件大小（MB） |
| `--filename` | 自动从URL提取 | 输出文件名（不含扩展名） |
| `--output_dir` | `Documents` | 输出目录 |

**使用示例:**
```bash
# 默认处理（下载→裁剪→去头尾→压缩）
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw"

# 不裁剪，直接去头尾并压缩
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw" --no-crop

# 不去头尾，只裁剪并压缩
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw" --no-trim

# 完全不裁剪也不去头尾
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw" --no-crop --no-trim

# 自定义裁剪区域
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw" --crop "800:600:240:60"

# 压缩到20MB以内
py scripts/download_and_process.py "https://www.bilibili.com/video/BV1m24y1d7xw" --max_size_mb 20
```

脚本自动依次执行：下载 → [裁剪] → [去头去尾] → 压缩到目标大小（中括号为可选步骤）

### 6. 手动处理流程（当脚本失败时）

当 yt-dlp 遇到反爬虫限制时，使用以下手动流程：

```bash
# 1. 安装 bilix
pip install bilix --break-system-packages

# 2. 解析短链获取BV号（如果是b23.tv短链）
curl -sI "https://b23.tv/短链ID" | grep -i location

# 3. 下载视频
bilix get_video "https://www.bilibili.com/video/BV号" -d 输出目录

# 4. 获取视频分辨率
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 视频文件

# 5. 计算裁剪参数（根据分辨率）
# 使用公式: crop_w=width*0.61875, crop_h=height*0.83333, crop_x=width*0.3375, crop_y=height*0.07778

# 6. 执行裁剪
ffmpeg -y -i 输入视频 -vf "crop=计算后的参数" -c:v libx264 -crf 18 -c:a copy 裁剪后视频

# 7. 去头尾各10秒
ffmpeg -y -i 裁剪后视频 -ss 00:00:10 -c:v libx264 -crf 18 -c:a copy 去头视频
# 获取时长后去尾
ffmpeg -y -i 去头视频 -t (时长-10) -c:v libx264 -crf 18 -c:a copy 最终视频

# 8. 压缩到目标大小
# 计算码率后执行压缩
ffmpeg -y -i 最终视频 -c:v libx264 -b:v 码率k -maxrate 码率*1.25k -bufsize 码率*2.5k -c:a aac -b:a 64k -ar 44100 输出视频
```

## 文件名约定

**所有视频文件必须以BV号命名，禁止使用固定文件名如 `bilibili_video.mp4`。**

- 下载时: `-o "PATH/%(id)s.%(ext)s"` → 生成 `BV1N14y1Y7uN.mp4`
- 中间文件: `{bvid}_raw.mp4`, `{bvid}_cropped.mp4`, `{bvid}_trimmed.mp4`, `{bvid}_trim_start.mp4`
- 最终输出: `{bvid}.mp4`

这样每个视频都有独立文件名，不会相互覆盖。

## 实际案例

### 案例: 852x480视频处理

**视频信息:**
- BV号: BV1XP411H7ZC
- 原始分辨率: 852x480
- 原始时长: 177秒
- 原始大小: 18.8MB

**处理步骤:**
1. bilix下载（yt-dlp返回412错误）
2. 裁剪参数计算: `crop=527:400:287:37`
3. 去头尾各10秒 → 时长157秒
4. 压缩码率: vbr=404k, maxrate=505k, bufsize=1010k

**最终结果:**
- 输出尺寸: 526x400
- 输出大小: 8.81MB
- 成功压缩到10MB以内