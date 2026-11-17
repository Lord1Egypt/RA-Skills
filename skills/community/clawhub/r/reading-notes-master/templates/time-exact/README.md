# templates/time-exact/ — 完全复刻模板

`reading-notes-master` v2.13.0 · `exact-replication`（完全复刻模式）的最小可运行骨架。
把原刊每一页当作不可变矢量底版，只替换「文字 / 图片 / 图表数据」三类内容槽位，槽位外像素要求 100% 相同。

**先读**：`references/exact-replication-contract.md`（契约/管线/API/字体/碰撞/验收）、
`references/journal-dna-cards.md`（按刊选档案卡，常规周刊 vs 特辑不可混用）。

## 文件清单

| 文件 | 作用 |
|---|---|
| `slots.example.json` | 三类槽位定义示例：`text` / `image` / `chart`，含 `align` / `max_width` / `uniform_font` / `bbox` / `design` |
| `content_pack.example.json` | 两套内容包示例（A 英文 / B 中文），`values` 以 `slot.id` 为键 |
| `build.example.py` | 最小构建脚本：probe → models → collision_report → `ExactEditor.apply_pack` → save → verify → 打印摘要 |
| `README.md` | 本文 |

引擎在技能包 `scripts/exact_replication.py`（`build.example.py` 会自动把它加入 `sys.path`）。

## 快速开始

1. **复制**本目录 4 个文件到工作目录。
2. **选对档案卡**：比对原刊画布 pt 与图像覆盖——`567.03×756 / 全量 med_cover≈0.35` → `TIME_WEEKLY`（常规周刊）；
   `576×783 / 1.00` → `TIME_SPECIAL_EDITION`（满版特辑）。**两条不可混用**。
   注意：`~0.35` 是原刊 DNA 全量中位口径，仅用于判线；该卡 J3 参数是
   `margin_l=25.3 / margin_r=45.3 / cols=2 / cov_ref=0.471`（12 页采样口径），两者不可混用。
3. **把槽位换成实测值**：`slots.example.json` 里 `spans[].bbox/text` 全是占位示例，必须用
   `build_page_models(doc)` 的真实 span 替换（Span 八字段：`x0/y0/x1/y1/font/size/color/text`）；
   `image.bbox` 取 `images[].bbox` 实测值。否则 `collision_report` 会命中真实非槽位文字。
4. **备素材**：`content_pack` 里 `image` 槽位的值是文件名，放到 `ASSETS_DIR` 目录；
   新图先按原 `bbox` 比例裁好（不改 bbox、不拉伸）。
5. **替换占位常量**：`build.example.py` CONFIG 区全部 `"<...>"`（`SRC` / `OUT_DIR` / `ASSETS_DIR` / `PACK_KEY`）。
6. **运行**：`python3 build.example.py`。`verdict=PASS` 才交付；报告 `zero_drift_<PACK>.json` 随交付归档。

## 槽位字段（`slots.example.json`）

| 字段 | 适用 | 说明 |
|---|---|---|
| `id` | 全部 | 唯一键，与内容包 `values` 的键对应 |
| `type` | 全部 | `text` / `image` / `chart` / `chart-redraw` |
| `page` | 全部 | 1-based 页码 |
| `spans` | text / chart | span 列表（八字段），顺序即行顺序 |
| `bbox` | image / chart-redraw | `[x0,y0,x1,y1]` |
| `align` | text / chart | `left` / `center` / `right` |
| `max_width` | text / chart | `fit_text` 按此截断，绝不越栏宽 |
| `uniform_font` | text / chart | 整槽位字体策略统一，避免行内字形/字重混杂 |
| `extra_width` | text / chart | 附加到 `x1-x0` 的额外宽度 |
| `bg` | chart-redraw | 遮盖底色 |
| `design` | text / chart | 固定设计参数快照，注入时只读不改 |
| `original` / `archetype` | 全部 | 审计/说明用 |

`ExactEditor.apply_pack(slots, pack)` 按 `type` 自动分派：
`text`/`chart` → `apply_text_slot`（值=行文字数组）、`image` → `apply_image_slot`（值=图片路径）、
`chart-redraw` → `apply_chart_redraw`（值=图片路径）。
**铁律**：text/chart 的 `values` 数组长度必须严格等于该槽位 `spans` 数，否则 `apply_text_slot` 抛 `ValueError`。

## 内容包（`content_pack.example.json`）

```json
{
  "A": {
    "name": "内容包 A · 英文新内容",
    "values": {
      "P08.quote": ["行1", "行2", "..."],
      "P09.photo": "slot_photo_A.png",
      "P12.rankings": ["Novartis", "U.S.", "97.51", "..."]
    }
  },
  "B": { "...": "中文新内容" }
}
```

同一套冻结槽位可注入多套内容包（A/B 切换 `PACK_KEY`），证明「设计层恒定、只换内容」。
中文内容会触发 T3 CJK 字形扩展（`china-s`）——这是内容承载资源，设计参数（字号/字重/颜色/基线）不变，
交付说明必须登记，不得宣称「字体 100% 不变」。

## 关键纪律（踩过的坑）

- **碰撞预检必做**：`collision_report(models, slots)` 有冲突就中止。P08 首字下沉大 `W`
  （bbox `30,90.4-86.7,147.7`）与正文首行 `y0=139` 相交，redact 会削掉 W 下半部墨迹——
  这类槽位外破坏**不能靠扩大验收 mask 掩盖**，只能收缩矩形/改选行（`y0>150` 起选）。
- **字体三档**：T1 目标页自身 Type1/PFA 子集复用 / T2 按字重映射 Base14（`fallback_font`）/ T3 `china-s`。
  **跨页子集不可混用**；基线必须用**原页面字体 ascender**，用替代字体的会让文字下溢出槽位。
- **零偏差验收**：`verify(src, edited, masks, matrix=2.0, pad_px=3)`；
  槽位外像素 100% 相同、未改动页 100% 相同、`canvas_all_equal`、只有 `PASS`/`FAIL`。
- **不要改原刊**：`SRC` 只读；`ExactEditor` 在副本上操作，产物另存 `OUT_PDF`。

## 占位常量一览（`build.example.py` CONFIG 区）

`SRC`（原刊 PDF）、`OUT_DIR`（产物目录）、`ASSETS_DIR`（新图片素材目录）、
`SLOTS_JSON`、`PACK_JSON`、`PACK_KEY`（`A`/`B`）、`BASE_PDF`、`OUT_PDF`、`REPORT`。
全部替换成真实绝对路径后运行；未替换会因文件不存在报错（预期行为）。

## 相关路径

- 引擎：`scripts/exact_replication.py`
- 契约文档：`references/exact-replication-contract.md`
- DNA 卡：`references/journal-dna-cards.md`
- 四门验收脚本（风格近似复刻用，非本模式）：`scripts/journal_4k_check.py`
