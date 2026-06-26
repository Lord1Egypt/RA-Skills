# 循环动画区间分析（为 spritesheet 服务）

> 用 video-analyzer 的 `--json` 模式分析视频的循环动画区间，输出结构化的 `loop_start`/`loop_end`，
> 供 spritesheet 的 `--loop-start`/`--loop-end` 使用。这是 video-analyzer `--json` 的典型用例。

## 为什么需要

spritesheet 的自动循环检测（主体感知全局接缝检测）对多数动画有效，但复杂动画（主体大小漂移、
多周期嵌套、非典型步态）可能不准。此时可用视觉大模型辅助判断区间，再手动指定给 spritesheet。
大模型分析能力归 video-analyzer，spritesheet 专注 CV 生成（职责分离）。

## Prompt 模板

把下面的模板作为 `--prompt` 传入（`--json` 会自动在前面附上视频的帧数/帧率/时长，模型据此返回帧序号）：

```text
你是一个 spritesheet 动画专家。我需要从这段视频中提取帧，制作流畅的循环动画。
请先完整观看视频，理解整体运动模式，然后判断哪段区间最适合做循环动画。

要求：
- 区间首帧和尾帧视觉上相似，能自然衔接形成循环
- 区间内运动足够丰富（均匀抽帧后帧间有明显变化，否则动画会卡顿）
- 优先选择运动最丰富的完整周期，扫描全视频找最佳区间（不要只看开头）

请返回 JSON：{"loop_start": 起始帧序号, "loop_end": 结束帧序号, "recommended_frames": 推荐帧数(≤16), "motion_description": 运动描述}
```

## 工作流

```bash
# 1. 用 video-analyzer 分析循环区间（--json 自动附帧数/帧率/时长，模型据此返回帧序号）
cd video-analyzer/scripts
uv run analyze.py --video /path/to/animation.mp4 --prompt "<上述模板>" --json
# 输出如：
# {
#   "loop_start": 0,
#   "loop_end": 30,
#   "recommended_frames": 8,
#   "motion_description": "一个完整的呼吸起伏周期"
# }

# 2. 用返回的 loop_start/loop_end 生成 spritesheet
cd ../../spritesheet/scripts
uv run spritesheet.py --video /path/to/animation.mp4 --loop-start 0 --loop-end 30 --frames 8
```

## 注意

- 帧序号准确性依赖模型对帧率/时长的换算；结果可用 spritesheet `--analyze` 复核（输出 MSE 曲线/周期候选/质心轨迹）。
- 模型偶尔不返回合法 JSON，video-analyzer 会降级打印原文，可人工读出区间。
- 若大模型结果不理想，spritesheet 的 `--loop-start`/`--loop-end` 仍可手动微调。
