# annotation.json 标注格式

`render_stream_whiteboard.py` 的揭示编排输入。一份文件对应**一幕**（一张线稿图）。

```json
{
  "canvas": {"width": 1536, "height": 864},
  "sceneDurationMs": 46000,
  "elements": [
    {
      "region": {"x": 100, "y": 80, "width": 600, "height": 120},
      "reveal": {
        "startMs": 0,
        "durationMs": 3000,
        "protectedRegions": []
      }
    },
    {
      "region": {"x": 100, "y": 240, "width": 500, "height": 200},
      "reveal": {
        "startMs": 3000,
        "durationMs": 4000,
        "protectedRegions": [{"x": 120, "y": 260, "width": 200, "height": 40}]
      }
    }
  ]
}
```

## 字段说明

- `canvas.width / height`：标注坐标系的画布尺寸，**必须与增强图 `*-enh.png` 的像素尺寸一致**（本项目统一 1536×864）。
- `sceneDurationMs`：**本幕**总时长（毫秒）。渲染器末尾会补一段「凝视」（展示完整原图）。合并后的成片总时长 = 各幕 `sceneDurationMs` 之和。
- `elements[]`：按**绘制顺序**排列的揭示区域。
  - `region`：矩形框，单位是画布坐标。渲染器只在框内揭示墨迹（「_allowed_mask = 本区 − 后续区域 − protectedRegions」，实现「后来者偷内容」的层级）。
  - `reveal.startMs`：**幕内相对时间**，从 0 起算。
  - `reveal.durationMs`：该区域揭示（起笔+添彩）耗时。
  - `protectedRegions`：本区域揭示时要保护的子区域（不被后画区域覆盖），例如某张牌上已先写好的小字。

## 两条铁律（见 lessons-learned）

1. **startMs 是幕内相对时间，不是成片绝对时间。** 写成绝对时间（如 105000）会把这一幕拉到几十秒，合并后成片虚高、音画错位。
2. **最后一个元素的 `startMs + durationMs` 必须 `< sceneDurationMs`**，否则结尾凝视被压缩、末段内容来不及展示。可以用 `make_annotation.py` 自动保证。

## 用 make_annotation.py 生成

见 `pipeline.md` 与 `annotation_spec_example.json`。给出区域顺序 + 画布尺寸，脚本自动算累计 `startMs` 和 `sceneDurationMs`，避免手写出错。
