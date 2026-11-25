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
  - `reveal.maskPaddingPx`：**可选**，region 揭示时的向外扩张量，老标注默认 **22**。渲染器会把 region 外扩这么多像素再取墨，因此「落在 padding 环带里的墨迹其实是显示了的」。`check_layout.py` 已解析该字段并外扩后再做归属判断——**不要手改这个值**，改了会让体检与渲染的判定不一致。
  - `protectedRegions`：本区域揭示时要保护的子区域（不被后画区域覆盖），例如某张牌上已先写好的小字。

## 两条铁律（见 lessons-learned）

1. **startMs 是幕内相对时间，不是成片绝对时间。** 写成绝对时间（如 105000）会把这一幕拉到几十秒，合并后成片虚高、音画错位。
2. **最后一个元素的 `startMs + durationMs` 必须 `< sceneDurationMs`**，否则结尾凝视被压缩、末段内容来不及展示。可以用 `make_annotation.py` 自动保证。

## 用 make_annotation.py 生成

见 `pipeline.md` 与 `annotation_spec_example.json`。给出区域顺序 + 画布尺寸，脚本自动算累计 `startMs` 和 `sceneDurationMs`，避免手写出错。

## region 怎么定才不会「文字显示不全」

渲染器的可见范围 = `region` 矩形 − 后续 region − protectedRegions。因此 region 必须**兜住**它负责揭示的
全部墨迹（含手绘抖动、便签胶带、折角），否则超出部分**永远不显示**——源图 PNG 是完整的，看 PNG 查不出来。

三条规则：

1. **region 是「墨迹的外接矩形 + 8px 内边距」**，不是「设计上的那行字的位置」。
2. **相邻 region 不要重叠**（后面的会挖掉前面的）。留 4~8px 缝隙即可。
3. **不要手写两遍坐标**。推荐用 `enhance_toolkit.LAYOUT` 在绘制时登记 bbox，再由 `make_spec.py` 生成 spec：

```python
LAYOUT.begin(im)
draw_title(d, "标题", 768, 80, 64, INK)          # 自动登记
draw_label_card(d, (120, 240, 620, 360), "要点", f_yahei(40))   # 自动登记
LAYOUT.save("layout-01.json")
```
```bash
python make_spec.py --layout layout-01.json --out spec-01.json --dur 4000 --title-dur 3000 --gaze 1200
```

生成后仍要跑一次体检：

```bash
python check_layout.py --image scene-01-xxx-enh.png --spec spec-01.json --margin 32
# 有 -base.png 时建议显式指定，只量新增墨迹：
python check_layout.py --image scene-01-xxx-enh.png --spec spec-01.json --base auto --margin 32
```

`check_layout` 会把 `region` 并集之外的墨迹逐块列出来（bbox、面积、最近 region、溢出方向），
`--fix` 可以自动外扩（不侵入相邻 region）。三类判据：**贴边**（距四边 < margin）、
**入字幕带**（`y1 > 762`）、**永不揭示**（在所有 region+padding 之外）。

> ⚠️ 别把 `--margin` 当装饰。画布 1536→成片 1080 的缩放比是 0.703，画布侧 32px 只等于成片 22.5px；
> 想要成片留 24px，画布侧必须 ≥34px（`enhance_toolkit.SAFE_MARGIN` 就是 34）。
