---
name: video-transition
version: 1.0.0
description: |
  视频转场效果工具。使用 ffmpeg xfade 滤镜实现多种转场效果，包括淡入淡出、滑动、擦除、圆形展开等。
  支持批量视频片段合并，自动添加转场效果。
author: "systiger"
tags: ["video", "transition", "ffmpeg", "xfade", "转场"]
---

# Video Transition / 视频转场

视频转场效果工具，使用 ffmpeg xfade 滤镜实现平滑转场。

## 支持的转场效果

| 转场类型 | 英文名 | 效果描述 |
|----------|--------|----------|
| 淡入淡出 | `fade` | 画面逐渐过渡 |
| 左滑 | `slideleft` | 新画面从右侧滑入 |
| 右滑 | `slideright` | 新画面从左侧滑入 |
| 上滑 | `slideup` | 新画面从下方滑入 |
| 下滑 | `slidedown` | 新画面从上方滑入 |
| 圆形展开 | `circleopen` | 圆形遮罩展开 |
| 左擦除 | `wipeleft` | 从右向左擦除 |
| 右擦除 | `wiperight` | 从左向右擦除 |
| 距离 | `distance` | 距离渐变 |
| 像素化 | `pixelize` | 像素化过渡 |
| 对角线 | `diagtl`/`diagtr` | 对角线擦除 |
| 矩形 | `rectcrop` | 矩形裁剪 |

## 快速使用

### 1. 合并视频带转场

```python
from video_transition import concat_with_transitions

# 合并视频片段，自动添加转场
concat_with_transitions(
    video_paths=["clip1.mp4", "clip2.mp4", "clip3.mp4"],
    output_path="output.mp4",
    transition_duration=0.5
)
```

### 2. 单个转场效果

```python
from video_transition import apply_transition

# 在两个视频之间应用特定转场
apply_transition(
    video1="intro.mp4",
    video2="main.mp4",
    output="merged.mp4",
    transition="fade",
    duration=0.5
)
```

### 3. 批量添加淡入淡出

```python
from video_transition import add_fade_to_clips

# 为所有片段添加淡入淡出
add_fade_to_clips(
    input_dir="clips/",
    output_dir="faded/",
    fade_in=0.3,
    fade_out=0.3
)
```

## 参数说明

### `concat_with_transitions()`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video_paths` | list | - | 视频路径列表 |
| `output_path` | str | - | 输出路径 |
| `transition_duration` | float | 0.5 | 转场时长（秒） |
| `transitions` | list | 循环使用所有 | 转场类型列表 |
| `auto_fade` | bool | True | 是否自动添加淡入淡出 |

### `apply_transition()`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `video1` | str | - | 第一个视频 |
| `video2` | str | - | 第二个视频 |
| `output` | str | - | 输出路径 |
| `transition` | str | "fade" | 转场类型 |
| `duration` | float | 0.5 | 转场时长 |
| `offset` | float | 自动计算 | 转场起始时间 |

## 依赖

```
ffmpeg >= 4.0
```

## 技术原理

使用 ffmpeg 的 `xfade` 滤镜实现视频转场：

```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=5[outv]" \
  -map "[outv]" output.mp4
```

## 触发词

`视频转场`、`转场效果`、`xfade`、`视频合并`、`淡入淡出`

## 文件结构

```
video-transition/
├── SKILL.md              # 技能说明
├── README.md             # 详细文档
├── video_transition.py   # 核心模块
├── example.py            # 使用示例
└── package.json          # 包信息
```

## License

MIT

## Author

systiger
