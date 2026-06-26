# 🎬 video-merger
> 轻量级命令行工具，自动拼接多个分段短视频为完整长视频，专为AI短剧、分镜头视频批量拼接场景设计。

## About
`video-merger` 自动识别按数字前缀命名的视频片段，按顺序拼接为完整视频，支持自动统一音视频参数、淡入淡出转场、自定义分辨率，无Python第三方依赖，仅需系统安装ffmpeg即可使用。

## Installation
### 1. 安装依赖
仅需要ffmpeg：
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 2. 安装video-merger
```bash
# 从PyPI安装（后续支持）
pip install video-merger

# 从源码安装
git clone https://github.com/machunlin/video-merger.git
cd video-merger
pip install .
```
安装完成后即可全局使用 `video-merger` 命令。

## Configuration
无需额外配置，所有参数通过命令行传递即可。

## Usage
### 基础用法
将`./segments`目录下的视频按顺序拼接为`full_video.mp4`：
```bash
video-merger --input ./segments --output ./full_video.mp4
```

### 自定义参数
```bash
# 自定义输出分辨率1080x1920，转场1秒
video-merger -i ./segments -o ./1080p_output.mp4 -r 1080x1920 -t 1.0

# 更高质量输出
video-merger -i ./segments -o ./high_quality.mp4 --crf 18 --preset slow
```

### 所有参数
```
$ video-merger --help
Usage: video-merger [OPTIONS]

Options:
  -i, --input DIRECTORY     分镜头视频所在目录 [required]
  -o, --output FILE         输出视频文件路径 [required]
  -r, --resolution TEXT     自定义输出分辨率，如1080x1920，默认保持原始
  -t, --transition FLOAT    淡入淡出转场时长（秒）[default: 0.5]
  --fps INTEGER             输出帧率 [default: 24]
  --crf INTEGER             视频质量(0-51，越小质量越高)[default: 22]
  --preset TEXT             编码速度预设 [default: medium]
  --ffmpeg-path TEXT        自定义ffmpeg路径 [default: ffmpeg]
  --ffprobe-path TEXT       自定义ffprobe路径 [default: ffprobe]
  --help                    Show this message and exit.
```

### 输入文件命名规则
输入目录下的视频文件名必须以数字前缀开头，工具会自动按数字顺序拼接：
```
segments/
├── 001_开场.mp4
├── 002_中景.mp4
├── 003_对话.mp4
└── 004_结尾.mp4
```

## Examples
### 批量处理多集短剧
```python
from video_merger import VideoMerger

merger = VideoMerger()
episodes = ["./ep1", "./ep2", "./ep3"]
for i, ep_dir in enumerate(episodes, 1):
    merger.merge(input_dir=ep_dir, output_path=f"./output/ep{i}.mp4")
```

## License
MIT - see [LICENSE](LICENSE) for details.
