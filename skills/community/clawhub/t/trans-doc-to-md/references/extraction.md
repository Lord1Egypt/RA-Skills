# 提取：文字 + 图表/表格/卡片

## 一、提取文字（pymupdf）

```python
import fitz
doc = fitz.open("paper.pdf")
text = "".join(page.get_text() for page in doc)
open("paper.txt", "w").write(text)
print(f"Pages: {doc.page_count}, chars: {len(text)}")
```

`get_text()` 只抽纯文字——矢量图（流程图/柱状图）和表格结构会丢，这是预期；图形走下方单独处理。

## 二、图形分两类，提取方式不同

| 类型 | 判断 | 提取 |
|---|---|---|
| 光栅图（嵌入 PNG/JPEG） | `page.get_images()` 有结果 | `page.get_image_rects(xref)` 取坐标 → `clip=Rect` 裁剪 |
| 矢量图（流程图/柱状图，绘图命令） | `get_images()` 空、`get_drawings()` 有数据 | `get_drawings()` bbox + caption 坐标推断边界 → `clip` 截图 |

**⚠️ 关键**：
- 绝不能 `get_pixmap()` 不传 `clip`——会截整页含正文。
- `get_image_rects()` 只对光栅图有效；矢量图只能靠 `get_drawings()` bbox + caption 推断。
- 裁完用 Read 工具预览 PNG，确认干净（只含图形+caption）。
- 报告类页面宽约 1120pt，clip 右边界要到 `page.width - margin`（~1060），**别只裁到中线（~555）**，否则条形图右侧百分比被截掉。

## 三、「卡片检测」裁剪整张图表（报告类首选）

报告图表常由几十个矢量/光栅碎片拼成，逐张提取无法还原。改用「最大填充矩形 = 卡片背景」检测：

```python
import fitz
def crop_card(page, mat=fitz.Matrix(2.4, 2.4), pad=7):
    W, H = page.rect.width, page.rect.height
    best = None
    for d in page.get_drawings():
        r = d["rect"]
        if r.width <= 0 or r.height <= 0:
            continue
        af = (r.width * r.height) / (W * H)
        # 卡片背景：占页 10%~78%、宽度过半的最大填充矩形（排除整页背景 af≈1.0）
        if 0.10 < af < 0.78 and r.width > 0.5 * W and r.height > 0.10 * H:
            if best is None or r.width * r.height > best.width * best.height:
                best = r
    if best:
        clip = fitz.Rect(best.x0-pad, best.y0-pad, best.x1+pad, best.y1+pad)
        return page.get_pixmap(matrix=mat, clip=clip)
    return None
```

> ⚠️ 卡片检测对**纯文字卡片**（文字表格、说明段落）也会命中——务必渲染成图后**目视核对**（拼成 contact sheet 一次看多张），只留真数据图表。封面/作者合影用固定区域裁剪。

## 四、按「分数带」精确裁剪（按页面比例）

已知某图在某页的纵向区间时，用比例裁剪 + 自动收紧白边最稳：

```python
import fitz
from PIL import Image
import numpy as np
def crop_band(doc, idx, top_frac, bot_frac, out, left_frac=0.06, right_frac=0.94, dpi=200, pad=16):
    pix = doc[idx].get_pixmap(dpi=dpi)
    full = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    W, H = full.size
    band = full.crop((int(W*left_frac), int(H*top_frac), int(W*right_frac), int(H*bot_frac)))
    arr = np.asarray(band.convert("L")); m = arr < 245
    rs = np.where(m.any(axis=1))[0]; cs = np.where(m.any(axis=0))[0]
    if len(rs) and len(cs):
        band = band.crop((max(cs[0]-pad,0), max(rs[0]-pad,0),
                          min(cs[-1]+pad,band.width), min(rs[-1]+pad,band.height)))
    band.save(out); print(out, band.size)
```

## 五、🚨 全本扫描 + 完整性两方对账（核心，别抽查！）

抽查式"彻查"会反复漏图。两个高频盲点：
1. **一页多图**——同一页可能放 2 张图表，只取第一张会漏第二张（其图注常被解析成孤立 `##` 标题、后面没图）。
2. **页码空档藏图**——按"已知图表页码"反推会跳过空档里的图。

**一次到位法**：
1. 逐页低 DPI 渲染整本 PDF（`get_pixmap(dpi=70)`），拼 contact sheet 目视扫一遍。
2. 用**颜色特征**识别图表页（如品牌色条形图含粉+紫双色像素的页）。
3. 对图表页统计某色条的**纵向像素聚类**，≥2 簇 = 多图页，逐张裁剪（命名加后缀 `chart_pNNb`、`chart_pNNc`）。
4. **硬验收两方对账**：`PDF 实际图表数 == 本地 md 的 ![ 引用数`，不等就逐页定位。

> 归档阶段会再加一道「md ↔ 线上块」对账，凑成完整三方对账——那一步属于 `fetch-archive-to-lexiang`。

## 六、装饰元素甄别（解析器会过度识别）

若有上游解析（如把每个视觉元素标成 `[IMAGE]`），其中混有封面图案、作者头像、箭头/图标、孤立数字色块——这些数据已在正文文字里，**无需单独成图**。只保留描述了**多组可比数据**的真图表。判断：对应 PDF 页渲染后是否为独立图表卡片。

## 七、脚本封装

`scripts/pdf_extract.py` 封装了上述能力：

```bash
python3 scripts/pdf_extract.py paper.pdf --text   --out-dir out          # 抽文字 → out/paper.txt
python3 scripts/pdf_extract.py paper.pdf --thumbs --out-dir out          # 全本缩略图 → out/thumbs/
python3 scripts/pdf_extract.py paper.pdf --crop 46 --band 0.13 0.26 --out out/images/chart_p47.png
python3 scripts/pdf_extract.py paper.pdf --card 35 --out out/images/card_p36.png   # 卡片检测裁剪
```
