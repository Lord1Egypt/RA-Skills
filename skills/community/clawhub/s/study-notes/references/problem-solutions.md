# Problem Solutions Reference (MODE B / MODE C)

How to turn homework problems into HTML — the always-visible problem + figure, the collapsible solution, and the figure decision (draw SVG vs. embed the original image). Read this together with `design-system.md`.

---

## 1. Reading problem images

Homework arrives as: pasted text, photos of a worksheet, or a PDF.

- **Text / pasted**: use it directly.
- **Photo / screenshot (PNG/JPG)**: open it with the Read tool and transcribe the problem text faithfully. Keep the figure for embedding (Section 4).
- **PDF worksheet**: extract text + render pages, then crop each problem's figure:

```bash
python3 scripts/extract_pdf.py text homework.pdf -o hw.txt
python3 scripts/extract_pdf.py images homework.pdf -o hw_pages/ --dpi 200   # to view layout
# crop one figure (bbox = fractions of the page: x0,y0,x1,y1 from top-left):
python3 scripts/extract_pdf.py crop homework.pdf --page 2 --bbox 0.08,0.18,0.92,0.52 -o fig_q3.png
```

Transcribe **exactly** — same given numbers, same symbols, same units. Never silently "fix" a problem; if something is missing or contradictory, state the assumption you make.

---

## 2. The MODE C problem card

One `.card` per problem. Structure: **题号 + 题目文字 (visible) → 图 (visible) → `<details>` 解答 (hidden)**.

```html
<div class="sec-blue" id="q3">
<div class="section">
  <div class="section-header">
    <div class="section-num">3</div>
    <h2>第 3 题</h2>
  </div>

  <div class="card">
    <h3 id="q3-stmt">题目</h3>
    <p>质量 $m_1 = 2\,\text{kg}$ 的滑块以 $v_0 = 3\,\text{m/s}$ 撞上静止的 $m_2 = 4\,\text{kg}$ 滑块并粘连，求碰后共同速度与机械能损失。</p>

    <!-- FIGURE: either inline SVG (simple) or embedded <img> (complex/photo). See §3–§4. -->
    <div style="text-align:center;margin:12px 0;">
      <svg viewBox="0 0 360 120" width="360" xmlns="http://www.w3.org/2000/svg"><!-- simple diagram --></svg>
    </div>

    <details>
      <summary>解答</summary>
      <div class="details-body">
        <p><strong>(1) 动量守恒</strong>（碰撞瞬间外力冲量可忽略）：</p>
        <div class="fbox"><div class="frow">$$m_1 v_0 = (m_1+m_2)\,v$$</div></div>
        <p>解得</p>
        <div class="answer-box"><p>$v = \dfrac{m_1 v_0}{m_1+m_2} = 1\,\text{m/s}$</p></div>

        <p><strong>(2) 机械能损失</strong>：</p>
        <div class="fbox"><div class="frow">$$\Delta E = \tfrac12 m_1 v_0^2 - \tfrac12 (m_1+m_2)v^2$$</div></div>
        <div class="answer-box"><p>$\Delta E = 9 - 3 = 6\,\text{J}$</p></div>

        <div class="callout tip">
          <div class="callout-icon"></div>
          <div class="callout-body"><strong>检验</strong>
            <p>完全非弹性碰撞必损失能量，$\Delta E>0$ ✓；末速度介于 0 与 $v_0$ 之间 ✓。</p></div>
        </div>
      </div>
    </details>
  </div>
</div>
</div>
```

Rules:
- `<summary>` says only `解答` (or `解答 (1)(2)` for parts) — never reveal the answer in the summary.
- Every solution **step** shown; final result(s) in `.answer-box`. Multi-part → one `.answer-box` per part, labelled `(1) (2) (3)`.
- Add a short **检验 (sanity check)** as a `.tip` callout at the end of each solution: units, limits, sign, magnitude.
- TOC lists `第 1 题 / 第 2 题 / …` (one `.toc-l1` per problem). Cycle section colors per problem or per group.

---

## 3. Figure decision — SVG vs. embed original (the core MODE C rule)

> **If the problem already came with a figure (photo, scanned diagram, plotted graph, circuit, geometry with many elements) → embed the ORIGINAL image. Only draw SVG when the figure is simple enough that a clean redraw is clearly better and faithful.**

Decision checklist — **embed the original image** if ANY is true:
- [ ] The figure is a photo, scan, or screenshot (not line art).
- [ ] It contains a data plot / curve / experimental graph.
- [ ] It has many elements (≳ 6 labeled parts), fine geometry, or precise proportions that matter.
- [ ] It's a circuit, a complex mechanism, a map, an anatomical/structural diagram.
- [ ] Redrawing risks changing the problem (angles, lengths, topology must be exact).

**Draw inline SVG** only if ALL are true:
- [ ] A few lines/shapes (block on incline, two blocks + spring, a single triangle of forces, a simple ray diagram).
- [ ] No photographic content and no quantitative curve.
- [ ] You can reproduce it faithfully with the SVG rules in `design-system.md`.

When in doubt → **embed the original.** Never omit a figure the problem depends on, and never invent a figure that wasn't given.

---

## 4. Embedding the original figure (standalone, base64)

The HTML must remain a single self-contained file, so embed images as base64 data-URIs (no external `src`).

**Option A — crop straight from a PDF page** (best when the worksheet is a PDF):

```bash
# bbox is fractional (x0,y0,x1,y1) measured from the top-left of the page
python3 scripts/extract_pdf.py crop homework.pdf --page 2 --bbox 0.08,0.18,0.92,0.52 -o fig_q3.png
python3 scripts/embed_images.py datauri fig_q3.png      # prints: data:image/png;base64,iVBORw0...
```

**Option B — from a photo/PNG/JPG the user uploaded**:

```bash
python3 scripts/embed_images.py datauri /path/to/photo.jpg
```

Paste the printed string into the `src`:

```html
<div style="text-align:center;margin:12px 0;">
  <img src="data:image/png;base64,iVBORw0KGgo..." alt="第3题图"
       style="max-width:100%;border:1px solid var(--border);border-radius:8px;">
</div>
```

**Option C — write `<img src="fig_q3.png">` first, inline everything at the end**: keep local file refs while drafting, then run once before presenting:

```bash
python3 scripts/embed_images.py inline final.html   # replaces every local <img src> with base64 in place
```

Image hygiene:
- Add `style="max-width:100%; border:1px solid var(--border); border-radius:8px;"` so figures never overflow and match the design.
- Always give a meaningful `alt` (e.g. `第3题图`).
- Crop tightly to the figure; don't include surrounding problem text in the crop (the text is already transcribed above the image).
- Prefer PNG for line art/diagrams; JPG is fine for photos. Keep crops ≤ ~1600px wide to keep the file small.

---

## 5. MODE B — homework as a worked-example card

In MODE B the homework problem lives **inside the concept section that teaches it**, as a collapsible worked example (not a standalone problem card). Same figure rule applies.

```html
<div class="card">
  <h3 id="s2-3-ex">应用：作业题精讲</h3>
  <div class="example-block">
    <div class="example-header">
      <span class="badge b-amber">作业 3</span> 两滑块完全非弹性碰撞
    </div>
    <div class="example-body">
      <p>质量 $m_1=2\,\text{kg}$ 的滑块以 $v_0=3\,\text{m/s}$ 撞上静止的 $m_2=4\,\text{kg}$ 并粘连，求共同速度与能量损失。</p>
      <!-- figure here if any (SVG or embedded <img>) -->
      <details>
        <summary>解答与思路</summary>
        <div class="details-body">
          <p><strong>思路：</strong>先判定碰撞类型→选守恒律→列式→检验。</p>
          <div class="fbox"><div class="frow">$$m_1 v_0=(m_1+m_2)v$$</div></div>
          <div class="answer-box"><p>$v=1\,\text{m/s}$，$\Delta E=6\,\text{J}$</p></div>
        </div>
      </details>
    </div>
  </div>
</div>
```

Difference from MODE C: the summary may say `解答与思路`, and the solution should **point back to the concept just taught** ("用刚才 §2.3 的动量守恒") so the problem reinforces the lesson. End the chapter with a `本章习题自测` card listing each 作业 题 + a one-line `考点` tag.
