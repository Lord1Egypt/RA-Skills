# 完全复刻契约（Exact Replication Contract）

> 适用技能：`reading-notes-master` · 引入版本 **v2.13.0** · 引擎 `scripts/exact_replication.py`
> 触发：用户要求「完全复刻 / 1:1 复刻 / 逐页建模 / 内容槽位替换 / 把这本换成新内容 / 其他杂志也一样」。
> 配套：`references/journal-dna-cards.md`（按刊抽取的实测 DNA 卡）、`templates/time-exact/`（可运行模板骨架）。

**一句话定义**：以原刊**每一页为不可变的矢量底版**，只替换「文字 / 图片 / 图表数据」三类内容槽位；
**槽位外像素必须 100% 与原刊相同**（零偏差），任何设计层改动即判定复刻失败。

---

## 0. 与「风格近似复刻」的本质区别

这是两条完全不同的产线，验收尺子也不同，不可混谈。

| 维度 | 完全复刻（`exact-replication`，v2.13） | 风格近似复刻（v2.10–v2.12 四门验收） |
|---|---|---|
| 底版 | 原刊每页整页作为 Form XObject 嵌入，**逐像素保留** | 从零用 CSS/HTML 重建一套「相似」设计 |
| 页面数量/页序 | 与原刊**完全一致**（页数、顺序、原型绑定冻结） | 按内容重排，成品页数为原书 1/3~1/2 |
| 可变部分 | 仅三类内容槽位（text / image / chart） | 整个版面、文字、配色、器型都可重新组织 |
| 不可变部分 | 固定设计层全锁（见 §1.1） | 只取「字体 DNA / 色板 / 栏数 / 密度」等风格参数 |
| 验收 | **零偏差验收**：槽位外像素 100% 相同、未改动页 100% 相同 | **四门验收 J1–J4**（字体 DNA / 色板签名 / 栅格边距 / 4K 像素），容差式相似度 |
| 交付物 | 与原刊同开本、同页数的 PDF（可注入多套内容包） | 重建版式的 HTML/PDF/PPTX |
| 典型问法 | 「照着这期 TIME 逐页复制，只把文章和图片换成新的」 | 「做一份像 Bloomberg Businessweek 的读书笔记」 |

> 决策表见 `SKILL.md`「完全复刻模式」章节。判据一句话：**要「长得像」→ 四门验收；要「逐像素一样、只换内容」→ 零偏差验收。**

---

## 1. 「完全复刻」定义

**完全复刻契约 = 固定设计层（锁定） + 三类内容槽位（可更新） + 字体资源边界声明 + 零偏差验收协议**，
且契约必须**逐页绑定到具体页码与原型**，不能只写刊级平均值；一条契约只对应**一个刊物的一条子产品线**
（常规周刊 ≠ 特辑，见 `references/journal-dna-cards.md` §2）。

### 1.1 固定设计层（immutable，逐项锁定，任一变动即失败）

| 类别 | 固定要素 |
|---|---|
| 画布 | 每页 `width` / `height` / `MediaBox`（pt） |
| 页序 | 页数、顺序、页与页面原型的绑定关系 |
| 页面原型 | 每页 archetype（`FEATURE` / `DEPARTMENT` / `SECTION OPENER` / `FULL-BLEED AD/IMAGE` …） |
| 栅格 | 栏位边界、分栏数、栏宽 |
| 边距 | 左右边距、正文区几何 |
| 页眉页脚 / 页码 | 文本、位置、字体 |
| 装饰矢量 | `drawings` 的 `rect` / `type` / `fill` / `stroke`（色块、细线、规则框） |
| 图片位置 | `images[].bbox`（尺寸/位置/裁剪框固定，只有像素内容可换） |
| 图表图形 | 图表区 bbox、轴线、图例位置、色带、行框、序号块等矢量图形 |
| 字体参数 | **字体族名 / 字号 / 字重 / 字距 / 行距 / 颜色 / 文本基线位置** |

> 注意「字体族名」固定 ≠ 「字体文件」固定：字形资源是内容载体，见 §6。

### 1.2 三类可更新内容槽位（slot）

| 槽位 `type` | 可更新 | 不可更新 | 引擎方法 |
|---|---|---|---|
| `text` | 字符串内容（逐行 span 原位替换） | 字体族名/字号/字重/字距/行距/颜色/bbox/对齐 | `ExactEditor.apply_text_slot` |
| `image` | 图像像素（同 bbox 覆盖） | bbox / 裁剪框 / 层级 / 蒙版结构 | `ExactEditor.apply_image_slot` |
| `chart` | 图表数据文字（矢量图形 100% 保留，只换数据） | 图形、轴、图例、配色 | `ExactEditor.apply_chart_slot` |
| `chart-redraw`（扩展） | 整块遮盖后贴入重绘的新图表位图 | 图表区 bbox | `ExactEditor.apply_chart_redraw` |

`ExactEditor.apply_pack(slots, pack)` 按 `type` 自动分派上述方法；`pack["values"]` 以 `slot["id"]` 为键，
text/chart 值为**行文字数组**（长度必须等于该槽位 `spans` 数），image/chart-redraw 值为**图片路径**。

---

## 2. 六阶段管线（顺序不可颠倒）

| 阶段 | 名称 | 输入 → 产出 | 引擎 / 关键动作 | 门禁 |
|---|---|---|---|---|
| S1 | 探查 | 原刊 PDF → 画布/字体矩阵/色板/密度/字号分布 | `fitz.open` + `build_page_models` 前的量测；跨刊对照见 DNA 卡 | 画布唯一值、页数、字体族、色板落表 |
| S2 | 逐页建模 | 原刊 PDF → 元素级模型 `list[model]` | `build_page_models(doc)` | 元素总数可复算、`n_*` 与列表长度自洽 |
| S3 | 原型分类 | S2 模型 → 每页 archetype | `classify_archetype(pm, canvas_area)` | 全部页归类、分布合计 = 页数 |
| S4 | 1:1 矢量底版 | 原刊 PDF → 零偏差底版 PDF | `replicate_1to1(src, out)`（`show_pdf_page` 整页 Form XObject） | 画布/文本层一致、像素 100%、MAE 0 |
| S5 | 槽位定义 + 碰撞检测 | S2 模型 + 槽位表 → 冻结槽位 | `collision_report(models, slots)` 预检 | **零冲突**才能开槽（见 §7） |
| S6 | 内容注入 + 零偏差验收 | 底版 + 槽位 + 内容包 → 复刻 PDF + 报告 | `ExactEditor.apply_pack(slots, pack).save(out)` → `verify(...)` | 槽位外像素 100% 相同、未改动页 100% 相同、verdict=PASS |

**红线**：S1→S4 是「完全复制不走样」，S5→S6 才是「可更新」。不得跳过建模与底版直接改内容；
不得在 S6 用「扩大验收 mask」掩盖 S5 未解决的碰撞（§7）；报告只有 `PASS` / `FAIL`，**没有「WARN 可交付」**。

---

## 3. 逐页模型 schema（对齐 `build_page_models` 真实返回结构）

`build_page_models(doc, include_drawings=True)` 返回 `list[dict]`，每页一项（1-based `page`）。

### 3.1 顶层字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `page` | `int` | 1-based 页码 |
| `canvas` | `[float, float]` | 该页 `[width, height]`（pt） |
| `n_spans` / `n_images` / `n_drawings` | `int` | 本页 span / 图片块 / 矢量绘图数 |
| `chars` | `int` | 本页文本字符数 |
| `spans` | `list[Span]` | 文本 span 元素级列表（见 3.2） |
| `images` | `list[Image]` | 图片块列表（见 3.2） |
| `drawings` | `list[Drawing]` | 矢量绘图列表（`include_drawings=True` 时） |
| `header` | `str` | 页眉文本（`y0 < 45` 的 span，`\|` 分隔，截断 200） |
| `footer` | `str` | 页脚文本（`y0 > height-45` 的 span，`\|` 分隔，截断 200） |
| `size_ladder` | `dict[str,int]` | 字号 → span 计数 |
| `font_ladder` | `dict[str,int]` | 字体名 → span 计数 |
| `color_ladder` | `dict[str,int]` | 文字色 → span 计数 |
| `x0_hist` | `dict[str,int]` | span 左边界 12pt 分箱 → 计数（栏位推断用） |

### 3.2 子结构

**Span**（8 字段，来自 `page.get_text("dict")`）：
`x0, y0, x1, y1`（bbox, pt，四舍五入 2 位）、`font`（族名，未带子集前缀）、
`size`（pt，2 位）、`color`（`#RRGGBB`）、`text`（原文）。

**Image**：`bbox`（`[x0,y0,x1,y1]`，2 位）、`w`、`h`（原始像素）、`ext`（编码格式）。

**Drawing**：`rect`（`[x0,y0,x1,y1]`）、`type`（`f` 填充 / `s` 描边 / `fs`）、`fill`（`#RRGGBB` 或 `null`）、`stroke`（同）。

### 3.3 ladder / hist 用途

- `size_ladder` → 标题/正文/图注分层，文字槽位分组键；
- `font_ladder` → 校验字体族锁定，注入新文字必须命中该页原有字体名；
- `color_ladder` → 校验色板锁定，注入颜色取自本页 `color_ladder` 键；
- `x0_hist` → 推断栏位起点，与 `cols` 互相印证。

### 3.4 原型分类 `classify_archetype(pm, canvas_area)`

按 `chars` / 图片覆盖率 `cov` / `n_drawings` / `header` 启发式返回：
`FULL-BLEED AD/IMAGE`、`SHORT/IMAGE`、`INFOGRAPHIC/AD`、`SECTION OPENER`、
`FEATURE/DEPARTMENT (DENSE)`、`AD`、`CONTENTS`、`FEATURE`。

```python
import fitz
from exact_replication import build_page_models, classify_archetype

doc = fitz.open(SRC)
models = build_page_models(doc)                       # S2
area = models[0]["canvas"][0] * models[0]["canvas"][1]
archetypes = [classify_archetype(m, area) for m in models]   # S3
assert len(models) == doc.page_count
```

---

## 4. 引擎 API 速查（`scripts/exact_replication.py`）

| API | 作用 |
|---|---|
| `build_page_models(doc, include_drawings=True)` | S2 逐页建模，返回 §3 的 `list[model]` |
| `classify_archetype(pm, canvas_area)` | S3 单页原型分类 |
| `replicate_1to1(src_path, out_path)` | S4 1:1 矢量零偏差底版（`show_pdf_page` Form XObject，`garbage=4, deflate=True`） |
| `collision_report(models, slots, pad=0.4)` | S5 检测 redact 矩形是否误删非槽位文字，返回冲突清单 |
| `ExactEditor(src_path, models=None)` | 打开原刊副本，`self.masks` 记录每页「删除区∪绘制区」 |
| `ExactEditor.apply_pack(slots, pack)` | 按 `type` 分派注入，返回 `slot_log` |
| `ExactEditor.save(out_path)` | 保存（`garbage=3, deflate=True`） |
| `verify(src, edited, masks, matrix=2.0, pad_px=3, out_json=None)` | S6 零偏差验收，返回 `report`（见 §8） |
| `fallback_font(short, cjk)` | T2/T3 字体回退：按字重映射 Base14 / CJK（见 §6） |
| `render_array(page, matrix=2.0, clip=None)` | 渲染为 `(H,W,3)` uint8，正确处理 pixmap stride |
| `sha256(path)` | 文件哈希，用于资源清单比对 |

---

## 5. 三类槽位实现要点与代码片段

### 5.1 槽位定义字段（对齐 `templates/time-exact/slots.example.json` 与 `build_slot_demo.py`）

| 字段 | 适用 | 说明 |
|---|---|---|
| `id` | 全部 | 唯一键，与内容包 `values` 的键对应 |
| `type` | 全部 | `text` / `image` / `chart` / `chart-redraw` |
| `page` | 全部 | 1-based 页码 |
| `archetype` | 全部 | 标注原型（说明用） |
| `spans` | text / chart | span 列表（§3.2 八字段），**顺序即行顺序** |
| `original` | text / chart / image | 原内容快照（审计用） |
| `bbox` | image / chart-redraw | `[x0,y0,x1,y1]` |
| `align` | text / chart | `left` / `center` / `right`（默认 `left`） |
| `max_width` | text / chart | 可用宽度上限，`fit_text` 按此截断，绝不越栏宽 |
| `uniform_font` | text / chart | 整槽位字体策略统一；任一行的字形不达标则整槽位回退，避免行内字形/字重混杂 |
| `extra_width` | text / chart | 附加到 `x1-x0` 的额外宽度 |
| `bg` | chart-redraw | 遮盖底色（`#RRGGBB`） |
| `design` | text / chart | 固定设计参数快照（族名/字号/颜色/对齐/行数），**注入时只读不改** |

### 5.2 text — 文字槽位

`apply_text_slot` 流程：① 对每个 span 加 `±0.4pt` 外扩的 redact 矩形，
`apply_redactions(images=NONE, graphics=NONE, text=REMOVE)` **只删文字、不碰图片与矢量**；
② 整槽位判定字体档位（§6）；③ 用原 span 的 `size / color / bbox` 与原页面字体 `ascender` 计算基线，
`insert_text` 原位写回；④ mask 覆盖「删除区 + 实际绘制区」。

```python
slot = dict(id="P08.quote", type="text", page=8,
            spans=quote_spans, original=[s["text"] for s in quote_spans],
            align="center", max_width=210.0, uniform_font=True,
            design=dict(font_family="HaffnerTIMEDisplay-Black", size=26.9,
                        color="#ED1C24", align="center", lines=len(quote_spans)))
ed.apply_text_slot(slot, ["‘A layout is a ", "promise readers ", ...])   # 行数必须 == len(spans)
```

`fit_text` 用真实嵌入字体的 `text_length` 量测按 `max_width` 截断；基线公式：
`baseline = s["y0"] + asc_design * s["size"]`（`asc_design` 取自**原页面字体**，见 §6）。
`align=center/right` 时按实际文本宽度回算 `x_start`。

### 5.3 image — 图片槽位

`apply_image_slot` 直接 `pg.insert_image(fitz.Rect(bbox), filename=..., overlay=True, keep_proportion=False)`，
**bbox 不变**，只换像素。新图长宽比不同时应在素材侧先按 bbox 比例裁好，避免拉伸改变版面结构。

```python
slot = dict(id="P09.photo", type="image", page=9,
            bbox=[25.0, 25.0, 542.0, 400.0], original="原刊 P09 顶部主图")
ed.apply_image_slot(slot, "/abs/assets/slot_photo_A.png")
```

### 5.4 chart — 图表数据文字槽位（矢量图形保留）

`apply_chart_slot(slot, values)` 内部转调 `apply_text_slot(dict(slot, type="chart"), values)`：
只替换排行榜/表格里的**数据文字**，色带、行框、序号块等矢量图形全部原样保留。

```python
slot = dict(id="P12.rankings", type="chart", page=12, spans=rank_spans,
            original=[s["text"] for s in rank_spans], align="left", uniform_font=True,
            design=dict(font_family="ITCFranklinGothicStd", size=7.8, color="#000000",
                        note="仅数据文字替换，表格色带/行框/序号块等矢量图形全部保留"))
ed.apply_chart_slot(slot, ["Novartis", "U.S.", "97.51", ...])
```

### 5.5 chart-redraw — 重绘型图表（扩展）

`apply_chart_redraw` 先用 `bg` 填满 bbox，再贴入新图；适合标签已转曲、无法做文字级更新的图表。

### 5.6 一次性注入（推荐）

```python
from exact_replication import ExactEditor, collision_report, verify

slots = json.load(open("slots.json", encoding="utf-8"))["slots"]
conflicts = collision_report(models, slots)          # S5 必须先预检
if conflicts:
    raise SystemExit("[abort] 槽位会误删非槽位文字，先调整槽位选择")

pack = json.load(open("content_pack.json", encoding="utf-8"))["A"]   # {name, values}
ed = ExactEditor(SRC, models=models)
ed.apply_pack(slots, pack)
ed.save(OUT_PDF)
rep = verify(SRC, OUT_PDF, ed.masks, matrix=2.0, pad_px=3, out_json=REPORT)
```

---

## 6. 字体物理约束（必须写进交付说明，不可省略）

**事实**：原刊字体是**页级嵌入的 Type1/PFA 子集**，仅含该页用到的 glyph（TIME 常规周刊
`time_original_dna.json` 实测 `embedded_fonts` 共 **379** 项、`type=Type1`、`ext=pfa`、名称形如
`XVHNVY+HaffnerTIME-Regular`，`pages` 多为 1）。单页对常用字符覆盖有限，**中文完全不含 CJK glyph**；
本地通常没有商业字体 Haffner / FranklinGothic 完整版。

**三档字形资源策略**（引擎 `tier` 字符串）：

| 档 | 引擎 tier | 做法 | 适用 |
|---|---|---|---|
| T1 | `T1-original-subset` | `FontResolver.resolve` 只取**目标页自身**嵌入子集，`Font.has_glyph` 逐字校验后直接复用，字形 100% 原样 | 新文案为拉丁字符且落在当页字形集内 |
| T2 | `T2-visual-fallback` | `fallback_font(short, cjk=False)` 按**字重**映射 Base14：`tibo`/`tiro`/`tiit`/`tibi`（衬线）、`hebo`/`helv`/`heit`/`hebi`（无衬线） | 超出单页子集；**必须匹配字重**，否则 Display-Black 会掉成 Times-Roman 细体，违反「字重不变」 |
| T3 | `T3-cjk-extension` | `china-s`（或系统 `Songti.ttc`）承载 CJK | 任何中文/日文新内容 |

**四条硬约束**：

1. **跨页子集不可混用**：子集化后 `/Encoding` 被重排，按 WinAnsi 写字节会取错 glyph。
   引擎 `FontResolver` 只从**目标页自身** `get_fonts()` / `extract_font()` 取子集，绝不用别页子集。
2. **字形属内容载体，设计参数必须固定**：族名、字号、字重、字距、行距、颜色、基线全部锁定；
   「用哪个字体文件承载字符」属内容承载资源，可扩但必须在交付说明登记，**不得宣称「字体 100% 不变」**。
3. **基线必须用原页面字体 ascender**：`asc_design = fo.ascender if hit else 0.78`。
   若误用替代字体自身 ascender（`tiro≈1.05`、`china-s≈1.04`，而 `HaffnerTIME≈0.743`），
   文字会向下溢出槽位，造成槽位外像素破坏。
4. **字重不变**：中文只有 Regular 内置字形，遇原刊 `Black/Hvy` 字重时，引擎用
   `render_mode=2, border_width=0.022` 的 fill+stroke 描边补足视觉字重。

> 任何省略上述声明、把 CJK 降级伪装成「字体完全一致」的交付，视为契约违规。

---

## 7. 碰撞检测教训（必须预检，不能靠 mask 掩盖）

**事故**：TIME 常规周刊 **P08 首字下沉大 `W`**（bbox `30, 90.4 – 86.7, 147.7`）与正文首行
`y0=139` 相交。若把正文首行纳入文字槽位，`apply_redactions` 按矩形删除字符 ink，会**削掉 W 的下半部墨迹**——
被削的像素落在**槽位之外**，属于固定设计层破坏；这类破坏**不能靠扩大验收 mask 掩盖**（那等于把设计层
划进「允许变化」区域，契约失真）。

**正确做法**（`build_slot_demo.py` 实战）：

- 槽位从 `y0 > 150` 起选，避开首字下沉 W；
- 构建前必跑 `collision_report(models, slots)`：它把每个槽位 span 的 redact 矩形外扩 `pad=0.4`，
  检查是否与**非槽位** span 的 bbox 相交面积 `> 0.5`，返回 `victim_bbox / victim_text / victim_size` 冲突清单；
- 有冲突 → 收缩矩形 / 改选行 / 重建元素，**构建前处理**，不是事后调验收参数。

```python
conflicts = collision_report(models, slots)
print("槽位碰撞检测: %d 处冲突" % len(conflicts))
if conflicts:
    raise SystemExit("[abort] 槽位会误删非槽位文字，请调整槽位选择")
```

---

## 8. 零偏差验收协议（`verify`）

| 项 | 规定 |
|---|---|
| 渲染矩阵 | `matrix=2.0`（2x），双方同引擎 PyMuPDF、同参数、`alpha=False` |
| mask | `删除区 ∪ 绘制区`（`ExactEditor.masks[pno]`，已按 `±1.5/±2.5pt` 外扩容纳抗锯齿） |
| `pad_px` | `3`：mask 在像素域再外扩 3px |
| 槽位外像素 | **100% 相同**：`outside_changed == 0`（`zero_drift=True`），比率 `outside_change_ratio == 0` |
| 槽位内 | 必须发生可测变化（`inside_changed > 0`），证明内容确实被替换 |
| 未改动页 | **100% 相同**：`untouched_pages_identical`（以 `matrix=0.75` 全页比对） |
| 画布/页数 | `canvas_all_equal`：页数相等且逐页 `rect` 相等 |
| 结论 | `verdict = PASS iff (size_ok and worst_outside_change_ratio==0 and all(unchanged))`；只有 PASS/FAIL |

`report` 关键字段：
`canvas_all_equal`、`pages[]`（`page / n_slots / outside_pixels / outside_changed / outside_change_ratio /
outside_identical_pct / inside_changed / inside_change_ratio / full_page_identical_pct / mae / zero_drift`）、
`summary`（`edited_pages / all_edited_pages_zero_drift / worst_outside_change_ratio /
untouched_pages_checked / untouched_pages_identical / verdict`）。

```python
rep = verify(SRC, OUT_PDF, ed.masks, matrix=2.0, pad_px=3, out_json=REPORT)
assert rep["summary"]["verdict"] == "PASS"
```

> 与「四门验收」的分工：四门验收（J1–J4）是**风格近似复刻**的容差式尺子；完全复刻这里用**零偏差**尺子。
> 两者不互相替代，决策表见 `SKILL.md`。

---

## 9. 已知边界与失败模式

| # | 边界 / 症状 | 原因 | 处置 |
|---|---|---|---|
| B1 | 商业字体授权 | 原刊仅页级子集、本地无完整版 | 优先沿用底版原 xref；中文走 T3 并登记；不分发字体文件 |
| B2 | 中文显示方框 / `.notdef` | 用了原子集但缺 glyph | 走 `china-s`；检查 `Font.has_glyph` |
| B3 | 文字向下溢出槽位 | 用替代字体自身 ascender 定位基线 | 基线必须用**原页面字体** ascender（§6.3） |
| B4 | 字重变细 | T2 未按字重映射 | `fallback_font` 按 `black/hvy/heavy/bold/dem` 取 `tibo/hebo` 等 |
| B5 | 跨页字形错乱 | 混用了别页子集 | 只用目标页自身子集（§6.1） |
| B6 | 槽位外大面积像素差 | redact 误删图片/矢量 / `fill≠None` / mask 越界 | 检查三个 `*_NONE/*_REMOVE` 常量与 `fill=None` |
| B7 | 首字下沉/跨栏大标题被削 | 槽位矩形与固定设计层相交（§7） | `collision_report` 预检 + 收缩/改选行，**不扩大 mask** |
| B8 | 边缘 1~2px 像素差 | 抗锯齿余量不足 | 确认 `±0.4pt` + `pad_px=3` 两级外扩 |
| B9 | 图片型 PDF（整页位图/扫描） | 无文本层，建不出 span 模型 | 先判型：只作视觉参考或改走风格近似复刻 |
| B10 | Type3 中文字体不可读 | 中文刊以 Type3 嵌入、字体名不可提取 | 归入已知限制，设计令牌改走中文规则层 |
| B11 | 图表标签已转曲 | 无对应 span，文字级更新不可行 | 判为 `chart-redraw` / 图片式图表槽位整体替换 |
| B12 | 透明图 / 裁剪图 | `png` 可能含 alpha、`cover` 可 >1 | 注入前解析 `smask` / 裁剪路径，保留 bbox 与层级 |
| B13 | 渲染假阳性 FAIL | 不同引擎 / matrix / alpha | 双方强制同引擎、同参数 |
| B14 | 契约套错刊 | 同品牌子产品线混用（常规周刊 vs 特辑） | 先比对画布与 `med_cover`，见 `journal-dna-cards.md` §2 |

---

## 10. 引用路径（v2.13 新增资产）

| 路径 | 作用 |
|---|---|
| `scripts/exact_replication.py` | 完全复刻通用引擎（建模/底版/槽位/碰撞/验收，本文全部 API 的来源） |
| `references/exact-replication-contract.md` | 本文：契约定义、六阶段管线、模型 schema、字体/碰撞/验收协议 |
| `references/journal-dna-cards.md` | 六刊实测 DNA 卡、常规周刊/特辑拆卡、新刊接入步骤 |
| `templates/time-exact/slots.example.json` | 三类槽位定义示例（含 `align/max_width/uniform_font/bbox`） |
| `templates/time-exact/content_pack.example.json` | 两套内容包示例（英文 / 中文） |
| `templates/time-exact/build.example.py` | 可运行的最小构建骨架（probe→models→collision→apply_pack→save→verify） |
| `templates/time-exact/README.md` | 模板用法与字段说明 |
| `scripts/journal_4k_check.py` | 四门验收脚本（风格近似复刻用）；v2.13 新增 `TIME_WEEKLY` / `TIME_SPECIAL_EDITION` 档案卡 |
