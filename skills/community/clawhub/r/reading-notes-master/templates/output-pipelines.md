# 输出管线 — HTML → PDF / PPTX / 长图

> 模板产出 1280×720px 幻灯片式 HTML 后，按以下管线导出多格式交付物。

## 1. HTML → PDF（保真首选）

**Chrome / Edge headless 打印（版式 100% 保真）：**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="读书笔记-【书名】.pdf" \
  --no-margins "file:///path/to/notes.html"
```

- 模板已内置 `@page{size:1280px 720px;margin:0}`，导出即为 16:9 逐页 PDF。
- 每页一个 `<section class="slide">`，打印自动分页（`page-break-after:always`）。
- 若打印尺寸偏差，追加 `--print-to-pdf` 前设置 `--window-size=1280,720`。

## 2. HTML → PPTX（可编辑交付）

**方案 A（推荐）· 截图嵌入：** 先用 Chrome headless 逐页截图，再以 python-pptx 组装 16:9 演示文稿：

```bash
# 逐页截图（-H 按页数×720 递增，或用 puppeteer 逐 section 截图）
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=1280,720 \
  --screenshot="slide-01.png" "file:///path/to/notes.html#page1"
```

```python
# venv: /Users/wdj/.workbuddy/binaries/python/envs/default/bin/python
from pptx import Presentation
from pptx.util import Inches
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
for png in sorted(glob("slide-*.png")):
    prs.slides.add_slide(blank).shapes.add_picture(png, 0, 0, prs.slide_width, prs.slide_height)
prs.save("读书笔记-【书名】.pptx")
```

**方案 B · 结构化重建（文字可编辑）：** 按 `references/content-framework.md` 的页面序列，用 python-pptx 原生重建（每 slide 对应一个模块），主题色/字号直接取 `design-system.md` 阶梯（封面 96pt / 页标题 36pt / 正文 22pt / 注释 16pt）。适合需要二次编辑的场合。

## 3. HTML → 长图（社交分享）

- 浏览器逐页截图后纵向拼接（PIL `Image.new + paste`），或直接整页截图：
  `--window-size=1280,720*N`（N=页数）一次成图。
- 长图导出注意每页边界留 1px 分隔线，方便读者感知翻页。

## 4. A4 文档型变体（原型 C）

- 结构化八模块模板（考试脑科学范式）输出 A4 竖排时：正文 12pt、节标 36pt、行距 1.5–1.75。
- HTML 中将 `.slide` 改为 `width:794px;height:1123px`（A4@96dpi），`@page{size:A4}`。

## 5. 交付物清单（出版级标配）

| 格式 | 用途 | 命名规范 |
|---|---|---|
| `notes.html` | 源文件、在线预览 | `读书笔记-【书名】-v1.0.html` |
| `notes.pdf` | 打印、分发 | `读书笔记-【书名】-v1.0.pdf` |
| `notes.pptx` | 演讲、二次编辑 | `读书笔记-【书名】-v1.0.pptx` |
| `longimage.png` | 社交分享（可选） | `读书笔记-【书名】-长图.png` |

> 所有交付物落盘到统一输出目录，并用 present_files 一次性呈现 HTML 预览 + PDF/PPTX。
