# Static Reference Dual Mode To VI Board

Read this reference only when the customer chooses “use my reference”. The shared route accepts one static PNG/JPEG/WebP screenshot for `reconstruct`, or one to three same-family static screenshots for `corporate_fidelity`; it turns the supported inputs into one customer-viewable VI design standards board, waits for clear confirmation of the exact current board, and only then hands the hash-bound contract to project-theme compilation.

Before opening, decoding, or visually analyzing any reference image, run the
`static-reference` profile in `environment-preflight.md`. Both reference modes depend
on the same Pillow, PyYAML, Python Playwright, and Chromium chain. On failure, stop
before image processing and apply that reference's two-choice recovery contract.
Never offer manual corporate fidelity or describe `reconstruct` as a technical
downgrade.

## Contents

- Scope, one-time mode routing, and readability gate
- Boundary labels and extraction dimensions
- Shared structured contract, corporate regions, and executable layout grammar
- Deterministic render and confirmation
- Confirmed-VI handoff

## Scope Boundary

Analyze only visual properties visible in the supplied static frames. Do not inspect, infer, or write rules for movement, animation, transitions, timing, or sequential states. Multiple stills establish a template family, not a timeline.

Route `reconstruct` only for exactly one raster still. Route `corporate_fidelity` for one to three representative raster stills from the same template family; one still remains valid, while additional stills improve role coverage. A PPT, webpage, dynamic HTML, video, state sequence, more than three corporate stills, or multiple stills for reconstruct is unsupported, not “no clear reference.” State the boundary and ask for a supported representative input. Never infer movement or route a clear but unsupported reference to the eight built-in systems unless the customer explicitly abandons it. Legacy v1.1 reconstruct fixtures may still use safe offline SVG for backward compatibility; do not offer SVG as new intake.

The model performs visual understanding, identifies each supplied corporate page role, and fills the descriptive and machine-executable contract. Ask about a role only when genuine ambiguity remains; otherwise expose the automatic identification in the VI board for correction. `scripts/render_reference_vi.py` validates data and static frames, crops every declared `canvas_bbox`, enforces the documented 16:9 tolerance, deterministically extracts fixed assets, embeds local bytes, renders the fixed HTML/CSS board, and exports PNG. It never redraws a Logo or understands an image.

## One-Time Reference Mode Routing

| Customer intent | `reference_mode` | Promise |
|---|---|---|
| 参考风格重构 | `reconstruct` | Extract design language; allow recomposition and visual innovation. Preserve the existing behavior. |
| 企业模板保真 | `corporate_fidelity` | Use 1–3 same-family stills; lock screenshot-visible corporate elements per page role and design only the editable safe regions. |

If the customer already says “企业模板保真”, “公司模板原样采用”, or equivalent, record `corporate_fidelity` without asking again. If intent is unclear, ask exactly one binary question using the two labels and promises above. Count it inside the existing six-question maximum. Do not repeat it after the mode is known.

Both modes use the same readability check, observed/extension/unknown boundary, VI board, artifact-bound confirmation gate, and project-theme compiler. Do not create a second customer flow or a fifth built-in visual system.

`corporate_fidelity` means screenshot-visible fidelity only. It does not recover an original PPT master, vector Logo, font file, hidden layout, or unseen page asset. Never model-redraw a Logo. Prefer the clearest supplied screenshot when cropping a Logo or other shared asset. If every supplied screenshot is insufficient, stop and request a clearer screenshot; this stage does not promise independent Logo upload.

## Current-Session Readability Gate

Treat model choice as a platform or session-entry decision, not a mid-task TaoHtml workflow. Never claim that an Agent can switch models automatically inside the current task, never maintain a cross-platform model matrix, and never recommend a named model here.

- On first use in WorkBuddy, say only that Auto is recommended. Do not ask which model is active and do not ask the customer to switch repeatedly during the task.
- In Codex and Claude Code, continue with the current session model without recommending another model.

Before analysis, perform only a minimal readability check in the current session: verify that every input opens and accurately identify a few locatable static facts, such as where the main heading sits, which large color fields are visible, or where a hard border appears. Also verify that corporate inputs plausibly belong to one template family. This is a capability check, not customer-facing VI analysis and not a scoring system.

If those facts can be located reliably, continue. If they cannot, stop and say exactly:

> 当前会话无法可靠读取参考图

Then offer only two recovery paths: the customer may manually change the model at the platform/session entry and restart the reference task, or downgrade to TaoHtml's eight built-in visual systems. Do not guess, do not create a partial VI board, and do not turn the failure into a model-selection interview.

## Boundary Labels

Assign one explicit `status` to every item. Never default or silently promote a status.

| Status | Customer label | Use |
|---|---|---|
| `observed` | 直接观察 | The property is visibly supported by a named region of the reference. |
| `extension` | 报告适配建议 | The property is a reversible proposal for adapting the observed language to a report. |
| `unknown` | 参考中无法判断 | The category is absent, cropped, illegible, or otherwise unsupported by the reference. |

For every item, write a concise `basis`. Point `observed` items to the visible region or repeated feature, explain the adaptation logic for `extension`, and state exactly why the reference cannot support an `unknown` item. An absent category must remain `unknown`; never fill it with an invented observation.

## Required Extraction Dimensions

Create one board that includes all of these dimensions. A dimension not shown by the supported reference inputs still appears as an `unknown` item so the omission is visible rather than silently fabricated.

1. Reference thumbnail and a plain-language scope label.
2. Palette with only the exact hex values that can be sampled or carefully estimated from the visible image. One or two supported colors are sufficient; never invent a third color to fill the board.
3. Typography hierarchy with level, visible sample, size/weight/line-height description, and boundary status.
4. Grid, whitespace, outer margin, column, alignment, and spacing rhythm.
5. Cards, panels, labels, borders, rules, corners, shadows, and other visible component language.
6. Image crop, aspect ratio, masking, color treatment, captions, and annotation treatment.
7. Only chart or evidence language actually visible in the image; otherwise mark the category `unknown` and keep any report adaptation separate as `extension`.
8. Cover, content, and data-page miniatures. These are report adaptations unless the corresponding page type is directly visible in the reference.
9. Preserve and avoid guardrails, each tied to observed evidence or clearly labeled adaptation logic.
10. Executable layout grammar for page axis/alignment, cover structure, content organization, image position/ratio/treatment, data structure, module organization, density, and visual focus. Assign status and basis field by field; never derive these values later by keyword-matching prose descriptions.

For `corporate_fidelity`, the same unified board must additionally show:

- all one to three source thumbnails, their automatically identified `cover/toc/section/content/data` roles, and each explicit `canvas_bbox`;
- each observed shell with locked-region and editable-region overlays;
- one crop preview for every shared Logo, header, footer, brand bar, fixed decoration, or complex fixed composition;
- every shell's exact editable safe-area preview and fixed-element list;
- the extensible design language for content inside the safe area;
- all five corporate-frame miniatures: `cover`, `toc`, `section`, `content`, and `data`; every supplied role is `observed`, while every unseen role is `extension/proposed`, never `observed`;
- unknowns and limits, including unrecoverable master/vector/font assets or insufficient screenshot evidence.

Do not reduce the result to a prose “visual DNA summary.” The PNG board is the primary customer deliverable; the JSON is an internal rendering contract.

## Minimal Structured Contract

The following exact v1.1 contract remains accepted as the backward-compatible `reconstruct` path:

```json
{
  "schema_version": "1.1",
  "board": {
    "title": "VI 设计标准图",
    "subtitle": "基于单张静态参考的视觉语言确认稿",
    "reference_label": "客户静态参考"
  },
  "palette": [
    {"name": "主墨色", "value": "#111111", "role": "标题与边框", "status": "observed", "basis": "标题与粗边框"},
    {"name": "强调色", "value": "#C84B3F", "role": "标签与关键数据", "status": "observed", "basis": "页首标签与数据柱"},
    {"name": "纸张色", "value": "#F4EFE5", "role": "画布与卡片底色", "status": "observed", "basis": "整页底色与卡片留白"}
  ],
  "typography": [
    {"level": "H1", "sample": "结论先行", "spec": "约 64px / 粗黑 / 紧行距", "status": "observed", "basis": "左上主标题"},
    {"level": "BODY", "sample": "正文说明", "spec": "约 20px / 常规 / 宽松行距", "status": "observed", "basis": "主标题下方说明文字"}
  ],
  "layout": [
    {"label": "外边距", "value": "约画布宽度的 6%", "status": "observed", "basis": "四周稳定留白"},
    {"label": "模块间距", "value": "约 24px", "status": "extension", "basis": "把可见间距适配为报告节奏"}
  ],
  "executable_layout": {
    "page_axis": {"value": "row", "status": "observed", "basis": "主要模块沿横向展开"},
    "alignment": {"value": "start", "status": "observed", "basis": "标题与正文统一左对齐"},
    "cover_structure": {"value": "split", "status": "extension", "basis": "把标题和主图分区适配为封面"},
    "cover_split": {"value": "7:5", "status": "observed", "basis": "标题区明显宽于主图区"},
    "content_structure": {"value": "card-grid", "status": "extension", "basis": "把可见模块适配为内容卡片组"},
    "content_columns": {"value": "3", "status": "observed", "basis": "参考呈现三列等距模块"},
    "image_placement": {"value": "right", "status": "observed", "basis": "主图位于标题右侧"},
    "image_aspect_ratio": {"value": "4:3", "status": "extension", "basis": "以可见主图比例适配报告图片"},
    "image_fit": {"value": "cover", "status": "observed", "basis": "主图填满矩形面板"},
    "image_treatment": {"value": "muted", "status": "extension", "basis": "将克制色彩延展为轻度降饱和"},
    "data_structure": {"value": "source-chart-split", "status": "extension", "basis": "适配为来源与图表并列页"},
    "data_columns": {"value": "2", "status": "extension", "basis": "数据页按来源与图表形成两列"},
    "module_organization": {"value": "hard-grid", "status": "observed", "basis": "粗线和直角形成硬网格"},
    "density": {"value": "medium", "status": "observed", "basis": "标题与模块保持中等密度"},
    "visual_focus": {"value": "headline-and-image", "status": "observed", "basis": "标题与主图共同形成焦点"}
  },
  "components": [
    {"name": "结论标签", "description": "实色底、短文本、硬边", "status": "observed", "basis": "标题上方标签"},
    {"name": "证据卡片", "description": "细边框、短结论、来源脚注", "status": "extension", "basis": "把参考模块适配为报告证据卡"}
  ],
  "imagery": [
    {"label": "图片裁切", "description": "横向硬裁切并保留主体", "status": "observed", "basis": "右侧主图"}
  ],
  "evidence_language": [
    {"label": "数据图表", "description": "参考中未出现，不能识别图表语法", "sample": "none", "status": "unknown", "basis": "整张参考没有图表或数值证据"}
  ],
  "mini_pages": [
    {"kind": "cover", "title": "代表性封面", "description": "延展主标题、标签与主图比例", "status": "extension", "basis": "把已观察层级适配为报告封面"},
    {"kind": "content", "title": "代表性内容页", "description": "延展网格与卡片节奏", "status": "extension", "basis": "把已观察模块适配为正文页"},
    {"kind": "data", "title": "代表性数据页", "description": "仅定义信息区，不声称参考已有图表语法", "status": "extension", "basis": "数据页是报告需要，图表样式仍待后续定义"}
  ],
  "guardrails": [
    {"mode": "preserve", "title": "保留", "description": "保持大标题与硬边框的对比", "status": "observed", "basis": "两者在参考中反复出现"},
    {"mode": "avoid", "title": "禁用", "description": "不加入柔和渐变和玻璃拟态", "status": "extension", "basis": "避免冲淡已观察的硬朗语言"}
  ]
}
```

For one-image reconstruct and backward-compatible single-shell corporate inputs, schema v1.2 keeps every v1.1 base field and adds these exact top-level fields:

| Field | Exact contract |
|---|---|
| `reference_mode` | `reconstruct` or `corporate_fidelity` |
| `source_image` | `{sha256, width, height}`; digest is lowercase SHA-256 and dimensions are positive integers |
| `locked_regions[]` | `{id, type, bbox, status, basis, extraction}`; type is `logo/header/footer/brand_bar/decoration/composition`, status is `observed`, extraction is `crop` |
| `editable_regions[]` | `{id, bbox, allowed_content, basis}`; the first vertical slice requires exactly one region allowing `cover/content/process/data/closing` |
| `extension_pages[]` | two or three `{role, status, basis}` records; role is `cover/section/data`, status is always `extension` |
| `limitations[]` | one to six `{item, status, basis}` records with `status: unknown` |

Every `bbox` is `[x, y, width, height]` in normalized 0..1 coordinates. Width and height must be positive; the rectangle must remain inside the source; the editable rectangle must not overlap any locked rectangle. IDs are unique lowercase hyphenated strings. `corporate_fidelity` requires at least one locked region and the exact safe region above; `reconstruct` keeps all four mode-specific arrays empty.

The source-image digest and dimensions are verified against the current raster before rendering and compilation. Corporate mode fails before output if the source is below 960×540, a crop is below 24×24 pixels, a bbox is invalid or conflicts with the editable region, the source is missing or changed, or a fixed element requests anything other than exact cropping. Request a clearer screenshot rather than weakening the contract.

For corporate template families, use schema v1.4. It extends the v1.3 family contract with an explicit variable-pixel boundary instead of creating a second pipeline. v1.3 remains read-compatible and normalizes to an empty `replaceable_regions` list. Replace the v1.2 single-source corporate fields with:

| Field | Exact contract |
|---|---|
| `reference_pages[]` | 1–3 unique `{id, role, source_image, canvas_bbox, status, basis}` records; `role` is `cover/toc/section/content/data`, supplied pages are `observed` |
| `shared_assets[]` | `{id, type, source_page_id, source_bbox, status, basis, extraction}`; pixels bind to one source page, status is `observed`, extraction is `crop` |
| `replaceable_regions[]` | Zero to twelve `{id, source_page_id, source_bbox, replacement, replacement_strategy, status, basis}` records; currently `replacement` is `runtime_page_number`, strategy is `sampled_edge_fill`, and status is `observed` |
| `shell_variants[]` | Exactly five unique roles; each has `{role, status, reference_page_id, locked_regions, editable_region, basis}` |
| `shell_variants[].locked_regions[]` | `{id, type, asset_id, bbox, status, basis}`; `asset_id` points to a shared crop and `bbox` is its fixed placement in this shell |
| `shell_variants[].editable_region` | `{id, bbox, allowed_content, basis}`; `allowed_content` is exactly that shell role |
| `shared_brand_grammar` | Exact static safety rules: 16:9, source crops only, no complete screenshot background, no Logo redraw, fixed motion `none`, content motion only inside editable regions |
| `extension_pages[]` | Exactly the unobserved family roles, each with `status: extension` |
| `limitations[]` | One to six explicit unknowns or fidelity limits |

For each source, `canvas_bbox` is measured against the supplied screenshot before any other normalization. Crop the screenshot border/background first; validate the resulting canvas as 16:9 with relative error no greater than `0.0025` (0.25%), and reject instead of stretching when it exceeds that tolerance. The cropped canvas must be at least 960×540. PNG, JPEG, and WebP inputs must decode as exactly one raster frame; reject animated PNG/WebP/JPEG when the decoder reports multiple frames.

An observed shell binds to the source page with the same role and must use at least one asset from that page. An extension shell has `reference_page_id: null` and may reuse confirmed shared assets, but its role remains proposed. Every shared asset must be used, every locked placement must stay outside its editable region, and complex fixed visual groups may use `type: composition`. Never define an asset as the complete screenshot or include example body content merely to simplify extraction.

Each `replaceable_regions[].source_bbox` must sit inside exactly one shared asset from the same source page and may not overlap another replaceable region. Do not infer one from OCR, a particular number string, filename, company, or known customer coordinates: the upstream VI JSON must explicitly mark the observed variable-pixel region. Extraction samples the region's immediate edge, requires a dominant uniform RGBA background, records the original crop/region hashes and pixel bboxes, then fills only that region. Non-uniform edges fail closed instead of erasing uncertain brand pixels. The fixed header, Logo, bar, footer line, and every pixel outside the declared region remain byte-identical to the source crop. A v1.3 contract has no such authorization and therefore performs no pixel replacement; migrate by adding the explicit list, recomputing the VI digest, rerendering the board, and obtaining confirmation again.

Every list must be non-empty. `palette` accepts one to six items, so one or two supported colors are valid. A palette item with `observed` or `extension` status must carry a six-digit hex value. An `unknown` palette item must use the literal value `unknown`; the renderer shows a neutral hatched placeholder and “未识别色值”, never a real color swatch. Do not add an unknown palette item when the supported colors already express the category clearly.

`executable_layout` is an exact object, not a prose summary. Every field uses exactly `value`, `status`, and `basis`. Use these enums:

| Field | Values before `unknown` |
|---|---|
| `page_axis` | `row`, `column` |
| `alignment` | `start`, `center`, `end` |
| `cover_structure` | `split`, `single-column` |
| `cover_split` | `7:5`, `5:7`, `1:1`, `none` |
| `content_structure` | `card-grid`, `stack`, `single-focus` |
| `content_columns`, `data_columns` | `1`, `2`, `3` |
| `image_placement` | `left`, `right`, `top`, `bottom`, `background` |
| `image_aspect_ratio` | `16:9`, `4:3`, `3:2`, `1:1`, `3:4` |
| `image_fit` | `cover`, `contain` |
| `image_treatment` | `natural`, `muted`, `monochrome`, `high-contrast` |
| `data_structure` | `source-chart-split`, `chart-focus`, `table-focus`, `metrics-grid` |
| `module_organization` | `hard-grid`, `soft-stack`, `open-field` |
| `density` | `low`, `medium`, `high` |
| `visual_focus` | `headline-and-image`, `image-first`, `balanced` |

Every enum also accepts `unknown`, but only together with `status: unknown`; an unknown field cannot carry a concrete value. The upstream model must select these values from the confirmed static observation and explicitly labeled report adaptation. Descriptive `layout`, `components`, and `mini_pages` remain useful review material, but they are not the compiler's primary structural input.

The grammar has exact compatibility matrices. A contract outside them is invalid; the compiler never repairs a concrete incompatible value:

| `cover_structure` | Allowed `cover_split` | Allowed `image_placement` | Executed meaning |
|---|---|---|---|
| `split` | `7:5`, `5:7`, `1:1` | `left`, `right` | Copy and image are separate horizontal grid children. Ratios mean copy:image, so physical columns reverse when the image is left. |
| `single-column` | `none` | `top`, `bottom`, `background` | Top/bottom reverse actual DOM order; background creates an absolute visual layer behind a foreground copy panel. |

| `content_structure` | Allowed `content_columns` | Executed meaning |
|---|---|---|
| `card-grid` | `1`, `2`, `3` | Card and closing grids use that exact column count. |
| `stack` | `1` | One vertical sequence of line items. |
| `single-focus` | `1` | One focal lead followed by one vertical sequence of supporting points. |

| `data_structure` | Allowed `data_columns` | Executed meaning |
|---|---|---|
| `source-chart-split` | `2` | Local source and chart/table panel occupy two grid columns; image placement must be `left` or `right` and controls their DOM order. |
| `chart-focus` | `1` | One chart panel occupies the data grid. |
| `table-focus` | `1` | One table panel occupies the data grid. |
| `metrics-grid` | `1`, `2`, `3` | The outer data panel stays single-column while metric cards use the declared inner column count. |

`image_placement: background` additionally requires `image_fit: cover`. `inline`, `headline-only`, and `data-first` are intentionally absent: v1 has no distinct, generally valid program for those labels. Unknown fields use compatibility-aware neutral fallbacks recorded separately in provenance; for example, an unknown split on a confirmed split cover becomes `1:1`, while the original unknown boundary remains uncompiled.

Choose `density` from the visible relationship between labels, titles, explanatory copy, and major modules—not from the number of words in the eventual report. Use `low` for conspicuous whitespace and one dominant focal group, `medium` for a balanced report rhythm, and `high` for deliberately compact information groupings. The compiler turns this enum into semantic relationship spacing; the model must not invent pixel gaps. If the static reference does not establish density, use `unknown` so the compiler can record its neutral medium fallback separately.

`mini_pages` must contain exactly one each of `cover`, `content`, and `data`. `guardrails` must contain at least one `preserve` and one `avoid`. Across the whole contract, all three boundary statuses must appear at least once. Use an `unknown` item for a missing category instead of omitting the category. For `evidence_language`, set `sample` to `bar`, `line`, `table`, `metric`, or `citation` only when that language is directly observed or explicitly proposed as an `extension`; an `unknown` item must use `none`, which renders an explicit “参考中未出现” state instead of a fabricated chart.

## Deterministic Render

Render the contract and the verified local source image with:

```bash
python scripts/render_reference_vi.py \
  --data /absolute/path/to/reference-vi.json \
  --source-image /absolute/path/to/reference.png \
  --output /absolute/path/to/reference-vi-board
```

For corporate v1.3/v1.4, repeat `--source-image` in the same order as `reference_pages[]`:

```bash
python scripts/render_reference_vi.py \
  --data /absolute/path/to/corporate-family-vi.json \
  --source-image /absolute/path/to/cover.png \
  --source-image /absolute/path/to/toc.png \
  --source-image /absolute/path/to/section.png \
  --output /absolute/path/to/corporate-family-vi-board
```

The command creates HTML and a 3200×2400 PNG. New raster intake accepts readable single-frame PNG, JPEG, or WebP only; legacy v1.1 reconstruct remains readable with safe offline SVG. It embeds review sources as `data:` URIs only in the VI board. Corporate mode additionally verifies every source hash, dimensions, role binding, and `canvas_bbox`; extracts every shared asset to deterministic PNG bytes; displays crop hashes and shell overlays; and fails closed on invalid/conflicting bboxes, wrong aspect ratio, low resolution, source drift, multi-frame input, unreliable extraction, or non-crop fixed assets. Boundary statements such as “静态” or “无动态” remain valid; positive rules inferred from movement, timing, sequences, easing, keyframes, or morphing do not.

Run `check_assets.py --strict-offline` on the rendered HTML. Open the HTML in a real browser, verify the status labels and all sections, and inspect the PNG at original resolution for Chinese text, hex values, type hierarchy, component samples, and representative page miniatures. A corporate-family board must show all five `cover/toc/section/content/data` shells.

## Customer Confirmation Gate

Show the PNG as the primary deliverable, optionally provide the HTML, and end with:

> 请确认或修正这张《VI 设计标准图》中的直接观察、报告适配建议和参考中无法判断三类边界。当前版本得到明确确认后，TaoHtml 才会把它作为项目专用主题生成的输入；确认前不会开始正式报告制作。

Treat only a clear confirmation of the current board as VI authorization and record its current conversation reference; do not match a fixed phrase. If the customer corrects a source role, color, boundary label, crop rule, locked element, editable region, extension page, component, or guardrail, update the JSON, rerender the whole board, and request confirmation again. In corporate fidelity, confirmation freezes source roles, canvas crops, shared assets, shell placements, editable regions, and hashes. Production must not change them without invalidating confirmation and returning to this gate. Earlier approval to use the reference is not VI confirmation, and VI confirmation is not Report Design Brief confirmation.

## Confirmed-VI Handoff Boundary

After confirmation, retain these inputs and read `project-theme-compiler.md`:

- confirmed VI JSON contract;
- exact source-image path(s) or packaged local copies;
- rendered board HTML and PNG for comparison and human review;
- customer corrections incorporated into the current contract;
- target reading/presentation mode and any confirmed accessibility or brand constraints.

For v1.2 corporate fidelity, also retain the exact `source_image`, `locked_regions`, and `editable_regions`. For v1.3/v1.4, retain `reference_pages`, `shared_assets`, `replaceable_regions`, `shell_variants`, `shared_brand_grammar`, `extension_pages`, and `limitations`. Do not retain any complete screenshot as a reusable page background; each remains a confirmation and extraction source only.

Create the machine-checkable handoff in `project-theme-compiler.md`, bind the confirmation to the exact VI JSON and ordered reference-image hashes, and compile the project-specific manifest, CSS, templates, and provenance. The compiler is a separate deterministic step: this reference renderer still does not compile theme assets. The result does not substitute or extend the eight built-in themes and does not authorize report production without the remaining Report Design Brief gate.
