---
name: video-merger
description: 多片段短视频自动拼接工具，支持按文件名排序、统一音视频参数、淡入淡出转场、分块/完整拼接，适合短剧、分镜头视频批量拼接
---

# 视频拼接工具 (video-merger)
自动将分镜头/分段短视频按顺序拼接为长视频的OpenClaw技能，支持工程化批量处理。

## 功能特性
✅ 严格按文件名数字序号排序，保证剧情顺序正确  
✅ 自动统一分辨率、帧率、编码，保证播放流畅  
✅ 支持淡入淡出转场效果（整体/片段间可选）  
✅ 自动同步音轨，完整保留原音频  
✅ 支持两种输出模式：分块输出（每段1分钟左右）、完整长视频输出  
✅ 支持保持原始分辨率或自定义输出参数  

## 依赖要求
- ffmpeg (>= 5.0)
- Python 3.8+

## 安装
```bash
# 自动安装依赖
./install.sh
```

## 使用方法
### 拼接为完整长视频（默认保持原始分辨率）
```bash
python3 scripts/merge.py --input /path/to/segments --output ./full_video.mp4
```

### 自定义输出分辨率
```bash
python3 scripts/merge.py --input /path/to/segments --output ./full_video.mp4 --resolution 1080x1920
```

### 自定义转场时长
```bash
python3 scripts/merge.py --input /path/to/segments --output ./full_video.mp4 --transition 1.0
```

### 分块输出模式（每块60秒）
```bash
python3 scripts/merge.py --mode chunk --input /path/to/segments --output ./output_chunks/
```

### 自定义分块时长
```bash
python3 scripts/merge.py --mode chunk --chunk-duration 120 --input /path/to/segments --output ./output_chunks/
```

## 参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 分镜头视频所在目录 | 必填 |
| `--output` | 输出文件/目录 | 必填 |
| `--transition` | 转场时长（秒） | 0.5 |
| `--chunk-duration` | 分块模式每段目标时长（秒） | 60 |
| `--resolution` | 自定义输出分辨率，如 `864x480` | 保持原始 |

## 适用场景
- AI生成短剧分镜头批量拼接
- 录制的分段视频自动合并
- 短视频批量处理生产
