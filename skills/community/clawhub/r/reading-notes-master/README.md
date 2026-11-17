# reading-notes-master

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-2.14.0-blue.svg)](./SKILL.md)
[![Format](https://img.shields.io/badge/format-AgentSkill-orange.svg)](./SKILL.md)

**Publication-grade visual reading-notes generator** — turn any book's key ideas into beautiful, slide-style reading notes (HTML / PDF / PPTX / long image).

出版级可视化读书笔记生成器 —— 把任何一本书的精华转化为精美排版的幻灯片式读书笔记（HTML / PDF / PPTX / 长图）。

> Every design rule in this skill is **measured, not guessed**: distilled from 31 high-quality real-world reading-notes decks (~2,500 pages) via programmatic analysis (pypdf font/size mining, pypdfium2 color quantization, image-density metrics), then upgraded with publication-grade design tokens from awesome-design-md (Notion × Claude design systems).

## Features

- **9 page modules** — cover / author timeline / endorsements / why-read / TOC / part divider / content pages / golden-quote page / mindmap & review
- **6 narrative archetypes** — A Narrative · B Tool & Method · C Structured Doc (8-block exam template) · D Data Recap · E Endorsement-led · F Thematic Grouping, with a decision tree
- **20 measured theme palettes** mapped to book genres (investing red, finance-history teal, strategy blue, psychology warm-earth, dark-mode sci-fi …)
- **10+6 chart components** — timeline, stage band, side-by-side duel, framework diagram, numbered cards, mindmap, quadrant, data chart … with a selection decision tree; v2.1 adds 6 emotion-marketing components (toggle-switch panel / five-color spectrum band / value ladder / virality loop / weight tree / six-fear word tags)
- **v2 design tokens** (Stitch 9-section format) — warm ink `rgba(30,26,22,.95)`, whisper borders, 3-level soft shadow stack (≤5% per layer), progressive negative letter-spacing, 4-weight type system, radius ladder 8/12/16, warm-paper alternation `.alt`, pill badges, serif golden quotes (weight 500)
- **16:9 HTML template v2.0** — one `:root` swap to re-skin (theme layer), tokens locked (texture layer)
- **v2.1 emotion-marketing knowledge base** — five emotional switches (痛点 pain / 痒点 itch / 爽点 joy / 燃点 burn / 爆点 boom) × five-color emotion spectrum (wine-red / warm-orange / gold / scarlet / violet) × proven case library (Wanglaoji 200×, Meituan 3-in-1, Snow Flower replica …) × 5×4 observation matrix — in `references/emotion-marketing.md`
- **v2.2 consulting-grade page craft** — four narrative storylines with per-page `adds` discipline / judgment-sentence title rules + strong-word list / page-role table / five-zone page skeleton with single-takeaway & density tiers / relation→chart selection table with data contracts / 13 anti-pattern red lines / waterfall reconciliation contract / diagram semantic contracts / module-fill P-D-F-X-V protocol / 16:9 capacity-first hard grid / 4-gate acceptance + 12-question page audit — distilled from consulting-report-forge v1.8.0 (Apache-2.0) and reorganized for argumentative reading-notes pages — in `references/consulting-craft.md`
- **Export pipelines** — Chrome headless → PDF, python-pptx → PPTX, long-image, A4 variant
- **v2.3 graphics asset pipeline** — replicate-or-generate dual track for any chart/diagram/image in your notes: Path A replication (PyMuPDF layered extraction → sn-image-base VLM vision → Real-ESRGAN 4× super-resolution via `scripts/superres.sh` → bitmap→vector tracing via `scripts/bitmap2vector.sh`, vtracer color / potrace B&W) and Path B generation (mermaid→SVG/PNG/PDF via `scripts/mermaid-export.sh`, markdown→mindmap via markmap, text→SVG charts via `scripts/clip-chart.sh`, plus cognigraph-mcp-server integration for MCP hosts — 4 tools: mindmap / relationship graph / knowledge graph); all tools version-pinned with SHA256-verified test artifacts and a 10-pitfall ops library — in `references/graphics-toolchain.md`
- **v2.4 design-intelligence front-loading (Step 0)** — full ingestion of four design skills (92 files / 1.5 MB) under `references/design-intelligence/`: ① **ui-ux-pro-max** BM25 search engine (67 UI styles / 161 palettes / 57 font pairings / 13 stack rulebooks / UX guidelines / chart selection / landing patterns + `--design-system` generator; pure-stdlib local CSV engine, English-keyword search) ② **ui-ux-pro-max-cn** Chinese localization rules (Chinese font stacks / color culture / WeChat mini-program specs / Element Plus·Ant Design·Vant stacks / 5 industry rules / Chinese delivery checklist) ③ **awesome-design-md** 54 real-brand DESIGN.md specs (Vercel / Stripe / Linear / Notion / Claude / Apple / BMW / SpaceX …) ④ **awesome-design** 20+ design-skill selection navigator. Tone-setting upgrades from "look up the built-in mapping table" to "search the design-intelligence library first, then decide" — see `references/design-intelligence/INDEX.md`
- **v2.5 mental-models composition library + text-to-image spec** — full ingestion of 《万物皆模型》100 thinking models (each with one-line definition / content signal words / composition key points) organized into **10 canonical diagram families** (PY pyramid / MX matrix / CY cycle / CV curve / FL flow / CP contrast / NW network / MC mechanism / DK decision / TR tree); when note content hits a model's signal, the skill calls that model's standard diagram composition (signal → model → diagram-type three-step routing, full 101-entry signal quick-reference covering all 100 models, "diagram-content contract" QA). New text-to-image spec: five-element prompt formula (subject imagery + diagram geometry + style tokens + theme color + negative constraints), 10 family prompt templates, hard cap of ≤5 generated images per deck (cover 1 + hero ≤2 + quote background ≤2) — structured diagrams stay HTML/SVG, text-to-image only for atmosphere assets (cover / hero / quote background / section divider) — see `references/mental-models-library/INDEX.md` and `models-catalog.md`
- **v2.6 NG portrait magazine layout** — a full **magazine-grade portrait** pipeline for photography / nature / history / biography / art books, reverse-engineered from a real 148-page wildlife photography book → 60-page published-grade delivery (0 broken images / 0 clipping / 0 squeeze, PDF+PPTX 11.1MB each): 660×960px canvas (=495×720pt = 6.875×10in), NG yellow-box palette (ink `#231F20` + yellow `#FFD201` + gold/bronze/wine/red + 3-step warm paper), serif-headline / sans-label / DIN-numeral three-font-stack, black-bar+gold-star running heads; **12 magazine page templates** (cover / black TOC / chapter divider / full-bleed photo / article page with 2-column serif body + drop cap / anatomy annotation / statgrid / field-guide entries / timeline / price bars / mindmap / black quote page); **page-map method** (finished pages = ⅓~½ of source book); **Python generator sharding** (≤20KB per fragment to survive Write truncation); **6-step build pipeline** (merge → Playwright triple validation broken-img/clipping/squeeze → @2x screenshots → PDF with `in` units → PPTX with JPEG q87 rebuild −75% size → package) with a 6-entry pitfall library — see `references/ng-magazine-layout.md` and `templates/ng-magazine/` (mag.css + build-template.py + generator-template.py)
- **v2.7 HBR landscape magazine layout** — a full **magazine-grade landscape** pipeline for business journals / magazine anthologies / multi-theme collections, reverse-engineered from a real 88-page *Harvard Business Review 2025 Best-Of* delivery (source 12 issues / 2,291 pages → 88 pages = 46% of single-issue average, 0 overflow / 0 empty page / constant MediaBox, PDF 11.7MB + 88-page PPTX 16:9 dual acceptance): 612×756pt canvas (=8.5×10.5in US magazine trim), masthead-red `#E41824` + art-gold `#F09C18` + ink `#231F20` + cream `#F4F1EA` four-color DNA, sans+serif two-font-stack; **12 magazine page types** (full-bleed cover with 6-cell cover strip / 150pt giant-number chapter divider with vertical EN / asymmetric editorial opener 310pt photo column / full-page chart from original magazine / 100pt giant stat / two-column text / full-bleed photo feature / full-bleed quote / grouped TOC / 4×3 issue-overview grid + 3 SVG mega-chart components); **11-page fixed chapter rhythm** (divider→editorial→chart→stat→text×3→photo→quote→editorial flip→text); **Chrome headless print pipeline** (gradient scrims MUST be pre-rendered PNG — CSS linear-gradient over photos forces Chrome to rasterize photos into tiling Patterns, ×2.4 size); **PDF triple acceptance** (MediaBox constant / zero text overflow / zero empty page) + XObject content-hash dedup slimming (18.3→11.7MB, no in-page lossy recompression) + **PPTX same-source 16:9 rebuild**; 8-entry pitfall library — see `references/hbr-magazine-layout.md` and `templates/hbr-magazine/` (mag.css + generator-template.py + build-template.py + scrim/)
- **v2.10 magazine design corpus (31 measured journal PDFs)** — a measured **journal design-language corpus** reverse-engineered from 31 real 2026 English periodicals (NG main/History/Traveller/Little Kids, Bloomberg Businessweek, Barron's, Science, New Scientist, SciAm, Vogue, Cosmo, Time special, How It Works, 青年文摘 …, ~12 sampled pages each, PyMuPDF font/size/color/image-density/margin/columns mining): **vector-vs-image-type discrimination gate** (7 bitmap/scanned titles identified and routed to visual-reference-only, 24 vector titles fully profiled); **12 category design-language profile cards** with measured font DNA and signature palettes (NG GrosvenorBook+Geograph official fonts & orange `#E77741` / BBW 5-column 23-img-page & caramel `#AD6B42` / Science academic-blue 3-column / New Scientist magenta `#CC1D4C` big-block / Vogue Saol three-stack 84pt narrow margin / 青年文摘 227 Type3 CJK fonts …); **7 empirical design laws** (body-dominance / accent-color budget ≤1 per page / big-block signature / serif+sans(+display) three-stack / grid divide 3–5 col vs 1 col / margin personality / image-density three modes); **10-scenario task routing table** (which language to borrow for which task); **IMA knowledge-base hook** (kb `ima_kb_rDzPwmRH`, 31 PDFs + 2 md archived, re-run analyzer for incremental profiling) — in `references/magazine-design-corpus-2026-10.md`
- **v2.11 journal 4K replication closed loop (four-gate acceptance J1–J4)** — "**measure twice with the same ruler**": the corpus miner (`analyze_mags.py`) and the deliverable acceptance script (`scripts/journal_4k_check.py`) use *identical* measurement parameters (12-page sampling, 30pt-bin column clustering, `^[A-Z]{6}\+` font cleaning, 1.6 coverage cap), so profile cards and gate results are numerically comparable — no more eyeballing: **J1 font DNA** (serif+sans stacks hit official-or-substitute font prefixes) / **J2 signature palette** (≥1 signature color in vector-fill top-8, RGB distance ≤36; full-bleed titles degrade to text/pixel colors) / **J3 grid & margins** (margin-ratio Δ≤12pp, columns Δ≤1, density type unchanged — collage ≥5 imgs/page, full-bleed/restraint/balance/photo coverage bands) / **J4 4K pixels** (bitmap long ≥3840 & short ≥2160, same ruler as v2.9 G5; vector PDF equivalent with per-embedded-image effective-DPI back-calculation gated on main images ≥25% page width → `superres.sh` 4× first if short). 14 profile cards embedded in the script (`--list`), 4K DPI formula `ceil(3840 / page-long-inches)` (NG 384 / HBR 366 / 16:9 @3x), two render paths (PNG device-scale-factor / PDF vector + superres), six-step replication workflow + 8-entry pitfall library, `--json` report archived with delivery — in `references/journal-4k-replication.md`
- **v2.12 IMA knowledge-base full absorption: seven design dimensions + universal ebook pipeline** — the full absorption of the IMA "Overseas Journals" knowledge base (kb `ima_kb_rDzPwmRH`, 31 journal PDFs + 2 measured summaries) into **seven reusable design dimensions**, distilled from the 31-magazine measured corpus: **① design thinking** (five layout philosophies A–E: chart-first / photo-immersive / density-authority / balanced / full-bleed-declaration, mapped on a 0.25→145 imgs/page spectrum) / **② design models** (grid model: columns = content-width ÷ target-col-width with margin-columns negative correlation 1-col 436pt ↔ 5-col 214pt; density model: five types mapped to J3 DENSITY_TOL; color model: one-signature-color + neutral black/white skeleton, signature 3–15%; type model: display/body dual-track, special-issue display ×6) / **③ chart language** (three paradigms: BBW 23-img-page array / Barron's table authority / Science evidence figures; same-page chart colors one family) / **④ layout grid** (symmetry law Δ<40pt = authority / offset law Δ>150pt = visual-gravity design, Cosmo L92/R367 / newspaper law 30pt margins) / **⑤ photo direction** (four coverage bands: >90% single-hero type-over / 60–90% photo-essay immersion / 30–60% evidence figures / <30% garnish; 160% bleed peak legal) / **⑥ financial breakdown** (three paradigms routed: weekly narrative→BBW array / stock & earnings deep-dive→Barron's table / portfolio newsletter→MoneyWeek; Chinese finance = BBW skeleton + red-up/green-down) / **⑦ cover design** (masthead typology: color-block frame / wordmark / newspaper head; type-over-image color rules white-on-photo, black-on-paper, signature-color accent; 60-second type-selection quick route) — plus the **universal ebook→journal replication pipeline** (`references/universal-ebook-pipeline.md`): format matrix (epub/docx/pdf incl. OCR branch for scans/html/md/txt/mobi via ebook-convert) → unified IR → **dual-source separation** (content source ≠ style source) → auto mode (content-signal probing → seven-dimension selection report for user confirmation) / custom mode (named title loads profile card) / hybrid mode (body from journal A, cover from journal B) → five-step pipeline (parse → style tokens → structure mapping → render → J1–J4 gates) → batch mode — SKILL gains the IMA MCP access chain (`search_knowledge` semantic retrieval / `get_knowledge_list` / `get_media_info`, local mirror `magcorpus/` as offline fallback)

- **v2.13 exact-replication mode (pixel-zero-drift full replication)** — a new top-level mode for the strict contract "everything identical except text / image / chart content, which must be updatable": each source page becomes an immutable Form XObject base (`show_pdf_page`), so canvas, page order, archetypes, grid, margins, running heads, folios, decorative vectors, image/chart placement, font family / size / weight / tracking / leading / color / baseline are all fixed, while only three **content slots** (`text` span-by-span, `image` same-bbox overlay, `chart` data text with vector artwork preserved) can change. Six-stage pipeline: `build_page_models` → `classify_archetype` → `replicate_1to1` → slot definition + **`collision_report` preflight** → `ExactEditor.apply_pack` → `verify` (2.0x render, mask = deletion ∪ drawing area, slot-exterior pixels 100% identical, untouched pages 100% identical). Measured on real *Time* 2026-09-28 (74 pages): Stage A 74/74 pages pixel-identical / MAE 0; Stage B two content packs (English / Chinese) each edit only P08/P09/P12, both `verdict=PASS` with `worst_outside_change_ratio=0.0` and 71/71 untouched pages identical. Three hard-won constraints: redaction must use `fill=None, cross_out=False` with `images=0/graphics=0/text=0`; drop-cap bbox collisions must be preflighted (cannot be hidden by widening the mask); baselines must reuse the **source-page font ascender** (≈0.743) not the substitute font's (≈1.05). Font tiers `T1` own-page PFA subset / `T2` weight-mapped Base14 (`tibo`/`hebo`) / `T3` CJK `china-s`; **cross-page glyph pooling is rejected** because subset `/Encoding` remapping makes WinAnsi byte writes resolve to wrong glyphs. Also fixes a root-cause profile-card error: `TIME_WEEKLY` (567.03×756, text-led, J3 measured margin_l 25.3 / margin_r 45.3 / cols 2 / cov 0.471 / dpi 300) is now a separate card from `TIME_SPECIAL_EDITION` (576×783, full-bleed degraded); the legacy `TIME_SPECIAL` key stays for backward compatibility but must never be used for a regular weekly. New: `scripts/exact_replication.py`, `references/exact-replication-contract.md`, `references/journal-dna-cards.md`, `templates/time-exact/`

- **v2.14 practical hardening: exact-content engineering + detail QA gates** — reverse-engineered from five consecutive real deliveries (140-page NG full replication, 4K full-bleed upgrade, right-brain composition overhaul, 40-page NG portrait visual notes, and a **four-journal 1:1 exact-replication** delivered at `verdict=PASS / worst_outside=0.0 / 40 pages edited / zero reverted`): ① **overlay replacement replaces `apply_redactions`** (same-bbox opaque cover + write-back at original coordinates) because redaction has non-local content-stream/clip side effects on transparency-group pages; ② **exact sampled-median cover color** instead of 1/8 quantization (visible color blocks 15.1% → measured offset median 1/255, P90 2/255); ③ **WCAG relative-luminance text color** (low-contrast slots 13.7% → 1.1%, median 16.79); ④ **CJK `insert_textbox` silent-failure guard** (line-height ≈1.2×font-size, negative return writes nothing → step-down font sizes + PDF text-layer audit, after "stats said 530 OK but only 26/40 pages had Chinese"); ⑤ **graded local degradation `full→images→text→none`** for 3 transparency-composite-drift pages, keeping 40/40 pages with content; ⑥ **content engineering** (strip copyright/front-matter/appendix, split 200,476 chars into 26,331 ≤10-char semantic phrases, 40 equal whole-book windows, tail-completion with queue pushback → coverage 3.2% → 0–97%, semantic chars 77.7%); ⑦ **right-brain quantification + multi-journal quota** (image coverage 28%→67%, dark pixels 74%, `photo 4 / mix 4 / text 2` per journal, edge-color PPTX padding); ⑧ **eight detail gates + build-report contract + IMA archive SOP**; ⑨ **skill-evolution governance** (McKinsey MECE/pyramid/hypothesis-driven × GCCEO self-improving cadence, "measure three times with the same ruler"). Ships `references/exact-content-engineering.md`, `references/visual-detail-qa.md`, `references/skill-evolution-governance.md`, `scripts/semantic_stream.py`, `scripts/detail_audit.py`, `templates/quad-exact/`.

## Changelog

### v2.14.0 — 实战反哺 · 零偏差内容工程与细节门禁
- **定位**：v2.13 定义完全复刻契约，v2.14 固化大规模落地时的工程坑，并补齐 v2.13 缺失的内容层与视觉细节门禁。全部数字来自四刊合璧 40 页实跑（非示例数据）。
- **五层 MECE 升级**：A 渲染几何 / B 内容工程 / C 资产构图 / D 验收治理 / E 版本治理，互不重叠、完全穷尽。
- **新增文件**：
  - `references/exact-content-engineering.md`（覆盖式替换 / 精确中位色 / WCAG 文字色 / CJK 行高 / mask 契约 / 分级降级 / 多画布留白 / 内容流四步 / 文本层审计 / 12 条踩坑）
  - `references/visual-detail-qa.md`（右脑优势四刊量化 / 选页配额 / 4K 资产池 / 细节体检八门 / 构建报告契约 / IMA 归档 / 结构验证）
  - `references/skill-evolution-governance.md`（麦肯锡 MECE·金字塔·假设驱动 × GCCEO 持续进化·四维质量 / 同一把尺量三次 / 六步反哺闭环）
  - `scripts/semantic_stream.py`（内容流语义化库 + `--self-test`）
  - `scripts/detail_audit.py`（细节体检八门独立门禁）
  - `templates/quad-exact/`（四刊合璧 1:1 全复刻构建模板 + README）
- **实测改善**：文字槽 8→530 / 图片槽 81→106 / 中文页 26→39（40 页中 1 页竖排信息图按契约硬保护）/ 低对比槽位 13.7%→1.1% / 覆盖色偏差中位 1/255 / 全书内容覆盖 3.2%→0–97% / 零回退页；零偏差始终 `PASS / 0.0`。
- 版本：2.13.0 → 2.14.0。

### v2.13.0 — exact-replication（完全复刻模式）
- **新增能力**：`exact-replication` 完全复刻模式——以原刊每页为不可变矢量底版，只替换「文字 / 图片 / 图表数据」三类内容槽位；六阶段管线 + 碰撞预检 + 零偏差验收；与「风格近似复刻（四门验收）」用不同尺子，决策表见 `SKILL.md`。
- **新增文件**：
  - `scripts/exact_replication.py`（通用引擎：`build_page_models` / `classify_archetype` / `replicate_1to1` / `collision_report` / `ExactEditor` / `verify` / `fallback_font`）
  - `references/exact-replication-contract.md`（完全复刻契约技术文档）
  - `references/journal-dna-cards.md`（六刊实测 DNA 卡 + 按刊/子产品线抽契约步骤）
  - `templates/time-exact/`（`slots.example.json` / `content_pack.example.json` / `build.example.py` / `README.md`）
- **破坏性认知修正**：`scripts/journal_4k_check.py` 旧 `TIME_SPECIAL` 档案卡实测描述的是「Time Special Edition（满版特辑）」却被当常规周刊用，是已确认根因错误。v2.13 保留该键向后兼容并标注「不适用于常规周刊」，另立 `TIME_WEEKLY`（常规周刊，text-led）与 `TIME_SPECIAL_EDITION`（特辑语义别名，fullbleed）两条独立卡；`DENSITY_TOL` 同步补 `text-led` 分型。原有 14 卡、自定义模式直载档案卡、四门验收行为全部不变。
- 版本：2.12.0 → 2.13.0。

## Install

**ClawHub:**

```bash
clawhub install reading-notes-master
```

**Manual (WorkBuddy / OpenClaw / any AgentSkills runtime):**

```bash
git clone https://github.com/yjkj999999/reading-notes-master.git
cp -r reading-notes-master ~/.workbuddy/skills/   # or ~/.openclaw/skills/
```

## Usage

Say any trigger phrase to your agent: **读书笔记 / 生成笔记 / 可视化读书笔记 / reading notes / 读书笔记PPT / 读书报告 / 精华笔记 / 营销笔记 / 情绪开关 / marketing notes / 咨询级笔记 / consulting-grade notes / 设计系统 / 品牌风格 / 中文产品设计 / design system / brand style / 竖版笔记 / 杂志风笔记 / 国家地理风格 / magazine layout / portrait notes / 横版杂志 / 商业杂志版式 / 哈佛商业评论风格 / HBR风 / 期刊复刻 / landscape magazine / HBR layout / 期刊设计语言 / 杂志风格复刻 / Bloomberg风 / Science风 / Time风 / Vogue风 / New Scientist风 / 期刊语料 / journal corpus / 图片型PDF / 期刊知识库 / 4K 复刻 / 期刊级 4K / 高保真模仿 / 复刻验收 / journal 4K replication / IMA 知识库 / 七维设计 / seven dimensions / 任意格式复刻 / 电子书复刻 / ebook replication / 期刊设计思维 / 财经拆解 / financial breakdown / 封面设计 / cover design / 完全复刻 / exact replication / 1:1 复刻 / 逐页建模 / 零偏差验收**, then provide the book's raw materials (key points, golden quotes, structure).

Seven-step workflow (v2.4 adds Step 0, v2.6 adds Step 0.5 format routing, v2.7 upgrades Step 0.5 to three-way routing, v2.10 adds a journal-design-language layer to Step 0/0.5, v2.11 adds the four-gate J1–J4 acceptance to Step 4/5, v2.12 adds seven-dimension type selection + the universal ebook pipeline ahead of Step 4, v2.13 adds the exact-replication (1:1 vector base + 3 content slots + zero-drift acceptance) mode, v2.14 adds overlay replacement + semantic whole-book content distribution + eight detail gates + build-report contract before delivery):

0. **Design-intelligence front-load** — detect language/audience → run `references/design-intelligence/ui-ux-pro-max/scripts/search.py "<english query>"` → load brand DESIGN.md if specified → produce a **Design Decision Sheet** (style / palette / fonts / do's & don'ts); full routing & fallbacks in `references/design-intelligence/INDEX.md`
0.5. **Pick format (v2.7 three-way)** — photography / nature / history / biography books with rich imagery → **NG portrait magazine pipeline** (`references/ng-magazine-layout.md`); business journals / magazine anthologies / multi-theme collections wanting an "original-issue replica / best-of" feel → **HBR landscape magazine pipeline** (`references/hbr-magazine-layout.md`: 612×756pt, 12 page types, 11-page chapter rhythm, Chrome headless build); single-thread methodology / data books for projection → 16:9 slides workflow below
1. **Pick archetype** — `references/content-framework.md` §3 decision tree
2. **Set tone** — Design Decision Sheet first, then `references/design-system.md` §3.2 (20-palette mapping table); marketing / emotion content → `references/emotion-marketing.md` §1 five-color spectrum directly; Chinese audience → `design-intelligence/ui-ux-pro-max-cn/SKILL.md` rules
3. **Lay out pages** — copy sections from `templates/reading-notes-template.html` (12 page types), alternate `.alt` warm-paper pages every 2–3 content pages; match content signals against the mental-models library (`references/mental-models-library/`) and compose the standard diagram for each hit model; plan ≤5 atmosphere assets (cover / hero / quote background / section divider) per the v2.5 text-to-image spec
4. **Fill components** — pick charts via `references/chart-catalog.md` decision tree (cross-validate data charts with `--domain chart`)
5. **Export** — follow `templates/output-pipelines.md`

## Structure

```
reading-notes-master/
├── SKILL.md                          # entry: workflow, checklist, error handling
├── references/
│   ├── design-tokens.md              # v2 publication-grade tokens (Stitch 9 sections)
│   ├── design-system.md              # layout / fonts / type ladder / 20 theme palettes
│   ├── visual-grammar.md             # v2 chart-first visual grammar (text budgets, text→chart mapping)
│   ├── content-framework.md          # 9 modules / 8-block template / 6 archetypes
│   ├── chart-catalog.md              # 10+6 chart components + decision trees
│   ├── case-patterns.md              # 31-corpus style archive + reuse rules
│   ├── emotion-marketing.md          # v2.1 emotion-marketing methodology library (5 switches × cases × matrix)
│   ├── consulting-craft.md           # v2.2 consulting-grade page craft (storylines × titles × data contracts × QA gates)
│   ├── graphics-toolchain.md         # v2.3 graphics asset pipeline (dual track × 7-tool registry × MCP × pitfalls)
│   ├── ng-magazine-layout.md         # v2.6 NG portrait magazine layout handbook (params / 12 page templates / page-map / generator sharding / build pipeline / pitfalls)
│   ├── hbr-magazine-layout.md        # v2.7 HBR landscape magazine layout handbook (three-way routing / 612x756pt anchors / 12 page types / 11-page chapter rhythm / Chrome headless build / pitfalls)
│   ├── magazine-design-corpus-2026-10.md  # v2.10 measured journal design-language corpus (31 PDFs: type gate / 12 profile cards / 7 design laws / task routing / IMA hook)
│   ├── journal-4k-replication.md     # v2.11 journal 4K replication handbook (J1–J4 gates / DPI formula + 14-card table / 2 render paths / profile cards / 6-step workflow / 8 pitfalls)
│   ├── journal-design-seven-dimensions.md  # v2.12 seven design dimensions (thinking A–E / grid-density-color-type models / chart paradigms / grid laws / photo bands / finance routing / cover masthead)
│   ├── universal-ebook-pipeline.md   # v2.12 universal ebook→journal pipeline (format matrix / dual-source separation / auto-custom-hybrid / 5-step / batch)
│   ├── exact-replication-contract.md # v2.13 exact-replication contract (fixed design layer vs 3 slots / 6-stage pipeline / zero-drift acceptance / font tiers / pitfalls)
│   ├── journal-dna-cards.md          # v2.13 per-title per-product-line DNA cards (6 measured journals / weekly-vs-special split / new-title onboarding)
│   ├── exact-content-engineering.md  # v2.14 overlay replacement / exact cover color / WCAG text / CJK line-height / graded degradation / content stream
│   ├── visual-detail-qa.md           # v2.14 right-brain metrics / multi-journal quota / eight detail gates / build-report contract / IMA archive
│   ├── skill-evolution-governance.md # v2.14 McKinsey MECE x GCCEO continuous evolution / measure three times / six-step feedback loop
│   └── design-intelligence/          # v2.4 full ingestion of four design skills (INDEX.md is the entry)
│       ├── INDEX.md                  # four-layer architecture / Step 0 routing / commands / fallbacks / provenance
│       ├── ui-ux-pro-max/            # BM25 design-intelligence engine (scripts + 31 CSVs + upstream refs)
│       ├── ui-ux-pro-max-cn/         # Chinese localization design rules (pure markdown)
│       ├── awesome-design-md/        # 54 real-brand DESIGN.md specs
│       └── awesome-design/           # 20+ design-skill selection navigator
│   └── mental-models-library/        # v2.5 100 thinking models composition library (INDEX.md is the entry)
│       ├── INDEX.md                  # four-step usage / 30 signal quick-reference / text-to-image prompt spec
│       └── models-catalog.md         # 100 model profiles (definition/signals/family/composition) + 10 family templates
├── scripts/                          # v2.3 ready-to-run wrappers (auto tool discovery)
│   ├── bitmap2vector.sh              # bitmap→SVG tracing (vtracer color / potrace B&W)
│   ├── superres.sh                    # Real-ESRGAN 4× super-resolution (upscayl-bin)
│   ├── mermaid-export.sh              # mermaid→SVG/PNG/PDF (reuses local Chrome, no Chromium download)
│   ├── clip-chart.sh                  # .clp text→SVG charts (asmuth/clip)
│   └── journal_4k_check.py            # v2.11 four-gate acceptance (J1–J4; 14 embedded profiles; --json / --list)
│   ├── exact_replication.py           # v2.13 exact-replication engine (page models / 1:1 base / editor / zero-drift verify)
│   ├── figure-bridge.py               # v2.8–v2.9 academic chart bridge (38 types / default 4K / G1–G5)
│   ├── semantic_stream.py             # v2.14 front-matter strip / semantic phrases / N equal whole-book windows
│   └── detail_audit.py                # v2.14 eight detail gates (Chinese landing / semantics / contrast / color bias / 4K)
├── templates/
│   ├── reading-notes-template.html   # 16:9 publication-grade HTML skeleton v2.0
│   ├── output-pipelines.md           # PDF / PPTX / long-image export commands
│   ├── ng-magazine/                  # v2.6 NG portrait magazine assets
│   │   ├── mag.css                   # full design system (palette / 3 font stacks / 12 page components, battle-tested)
│   │   ├── build-template.py         # 6-step build pipeline (validate / screenshot / PDF / PPTX / package, pitfalls fixed)
│   │   └── generator-template.py     # generator skeleton (HD/FT/FOLIO + P.append, ≤20KB sharding)
│   └── hbr-magazine/                 # v2.7 HBR landscape magazine assets
│       ├── mag.css                   # full design system (masthead 4 colors / 2 font stacks / 12 page types / print rules)
│       ├── generator-template.py     # 12 page-type builders + 3 SVG mega-charts + P.append pattern
│       ├── build-template.py         # 6-step build (merge inline CSS / Chrome headless / triple acceptance / dedup slim / PPTX / package)
│       └── scrim/                    # 4 pre-rendered scrim PNGs (anti-Pattern key asset) + make_scrims.py regenerator
│   ├── academic-charts.css           # v2.8 academic chart design tokens (9 palettes / 9 journals)
│   ├── time-exact/                   # v2.13 exact-replication starter (slots / content pack / build example)
│   └── quad-exact/                   # v2.14 four-journal 1:1 replication template (build.example.py + README)
├── demo/
│   └── toyota-one-page-thinking-notes.html   # 12-page full demo (v2 tokens)
├── LICENSE                           # MIT-0
└── README.md
```

## Demo

Open `demo/toyota-one-page-thinking-notes.html` in Chrome — a 12-page publication-grade reading note of *《丰田一页纸极简思考法》* (One Page Thinking @ Toyota), built entirely with the v2 token set. Print to PDF via `Cmd+P` (page size pre-configured via `@page`).

## Author

**WANG DONG JIE (yjkj999999)** · [ClawHub profile](https://clawhub.com/yjkj999999) · CFO-level expert system builder, 30+ MIT-0 agent skills published.

## License

MIT-0 (MIT No Attribution) — free to use, modify, redistribute, no attribution required.
