# Confirmed VI To Project Theme

Read this reference only after the customer has clearly confirmed the exact current static-reference board and the task records that conversation reference. This shared step compiles either one-image `reconstruct` or one-to-three-image `corporate_fidelity` into a deterministic theme for the current project. It does not add a fifth built-in visual system and does not authorize formal report production.

The `static-reference` environment profile must already have passed before the
reference images were processed. If compilation moves to another interpreter or
machine, rerun that profile before reading the bound VI/reference inputs; never assume
the earlier environment result transfers across machines.

## Contents

- Responsibility and handoff contract
- Fail-closed compilation
- Executable layout and provenance policy
- Shared Runtime rendering
- Corporate template-family shell boundary
- Verification and remaining model work

## Responsibility Boundary

- The model understands supported static inputs, identifies corporate source-page roles, and produces the confirmed VI JSON under `static-reference-vi.md`.
- The Skill maintains the observed / extension / unknown boundary and requires the confirmation handoff below.
- `scripts/compile_project_theme.py` validates the handoff and deterministically writes the project theme.
- `scripts/render_visual_system.py --project-theme ...` injects that theme into the existing shared Runtime shell.

In `corporate_fidelity`, the model identifies each source role, shared fixed assets, shell placements, and safe areas, but never recreates fixed pixels. `render_reference_vi.py` and `compile_project_theme.py` verify ordered source bindings and cropped canvases, crop shared assets, hash the crops, embed the bytes offline, and place them at each confirmed shell coordinate. Report DOM, layout, and reveal behavior stays inside the selected shell's editable region.

Never infer motion, transitions, timing, interaction, or sequential state from static inputs. The project manifest records motion as a TaoHtml Runtime and report-task decision with `observed_from_reference: false`.

## Minimal Handoff Contract

Create one UTF-8 JSON file beside the confirmed VI JSON and reference input(s).
New one-image handoffs use schema v2.0:

```json
{
  "schema_version": "2.0",
  "project": {
    "id": "urban-renewal-observation",
    "display_name": "城市更新观察｜项目专用主题"
  },
  "confirmation": {
    "status": "confirmed",
    "confirmation_ref": "current-conversation-turn-reference",
    "vi_contract_sha256": "<64 lowercase hex characters>",
    "reference_image_sha256": "<64 lowercase hex characters>"
  },
  "inputs": {
    "vi_contract": "reference-vi-contract.json",
    "reference_image": "reference.png"
  },
  "target_mode": "presentation",
  "customer_corrections": [
    "已并入当前 VI 的客户修正；没有修正时使用空数组。"
  ]
}
```

For VI schema v1.3/v1.4, use handoff v2.1 and replace the singular fields with ordered arrays:

```json
{
  "schema_version": "2.1",
  "project": {"id": "corporate-family", "display_name": "企业模板族｜项目专用主题"},
  "confirmation": {
    "status": "confirmed",
    "confirmation_ref": "current-conversation-turn-reference",
    "vi_contract_sha256": "<64 lowercase hex characters>",
    "reference_images_sha256": ["<cover hash>", "<toc hash>", "<section hash>"]
  },
  "inputs": {
    "vi_contract": "corporate-family-vi.json",
    "reference_images": ["cover.png", "toc.png", "section.png"]
  },
  "target_mode": "presentation",
  "customer_corrections": []
}
```

Use `reading` or `presentation` for `target_mode`. Use a lowercase hyphenated slug for `project.id`. Keep input paths relative to the handoff file and inside the same handoff directory. Array order must exactly match `reference_pages[]`. Compute SHA-256 after the current VI JSON and all reference inputs are final. `confirmation_ref` identifies the current conversation confirmation while the hashes bind it to exact bytes; changing any bound file invalidates the handoff and requires a new confirmation. Legacy v1.1/v1.2 VI contracts require a single-reference handoff (new schema v2.0); VI v1.3/v1.4 requires a family handoff (new schema v2.1).

Do not record an approval timestamp, machine path, or volatile build metadata in the contract. The minimal contract stays portable and produces byte-identical theme assets from identical inputs.

### Legacy handoff migration

Published handoff schemas v1.0 (single reference) and v1.1 (reference family) used
the exact `phrase` field instead of `confirmation_ref`. The compiler continues to
recognize those two historical shapes without changing what either version means;
their normalized provenance records `confirmation_method: legacy_phrase` and a null
`confirmation_ref`. This is read compatibility, not the rule for a new confirmation.

For any new confirmation or correction, create a new v2.0/v2.1 handoff from the
current files, replace `phrase` with the actual conversation `confirmation_ref`, and
recompute every bound digest. Do not put `confirmation_ref` into schema v1.0/v1.1 or
put `phrase` into schema v2.0/v2.1: exact-field validation rejects both unversioned
shapes rather than guessing a migration.

## Fail-Closed Gate

Compilation must stop before creating the output directory when any of these is true:

- confirmation status is not `confirmed`, a new v2.x `confirmation_ref` is
  empty/invalid, or a historical v1.x handoff does not match its published legacy
  shape;
- the handoff has missing or extra schema fields;
- an input path is absolute, leaves the handoff directory, is missing, or is not a regular file;
- any bound SHA-256 digest does not match the current file or ordered source arrays disagree;
- the VI JSON fails the validator in `render_reference_vi.py`;
- the reference image is unreadable, active SVG, or contains a non-offline SVG reference;
- a corporate source is not single-frame PNG/JPEG/WebP, its cropped canvas is below 960×540 or outside the 0.25% relative 16:9 tolerance, its hash/dimensions drift, or it yields a crop below 24×24;
- a normalized bbox leaves 0..1, a locked placement overlaps its shell's editable region, or the corporate family does not define exactly `cover/toc/section/content/data` shells;
- a source role is duplicated, an observed shell maps to the wrong source page, an extension shell claims a source, or a shared asset/source mapping is inconsistent;
- a locked element requests model redraw or any extraction other than `crop`, or an unseen page role is mislabeled `observed`;
- target mode, project id, or customer corrections violate the contract.

Never repair, downgrade, or silently regenerate the confirmed inputs inside the compiler.

## Compile

Run:

```bash
python scripts/compile_project_theme.py \
  --request /absolute/path/to/confirmed-vi-handoff.json \
  --output-theme /absolute/path/to/project-theme
```

The output directory contains exactly:

```text
project-theme/
├── theme.json
├── theme.css
├── templates.html
└── provenance.json
```

- `theme.json` contains the project identity, `reference_mode`, executable tokens, normalized `executable_layout`, per-field `structure_sources`, generated page roles, components, preserve/forbidden rules, target mode, input hashes, and explicit static-reference motion boundary. Corporate v1.3/v1.4 also records source roles/hashes/dimensions/canvas crops, shared-asset source and crop hashes, five shell variants, per-shell fixed/editable regions, extensions, limitations, `full_screenshot_background: false`, and `logo_redraw: false`. v1.4 additionally records every replaceable region, original source-crop/region hashes, cleaned crop hash, pixel bboxes, and sampled background RGBA.
- `theme.css` applies palette, type hierarchy, spacing/grid, border language, image crop/treatment, cards, panels, labels, data treatment, cover, content, evidence/data, and closing-page structures selected from the executable layout grammar.
- `templates.html` provides five reusable, grammar-selected DOM variants using the same placeholders and `fragment` / `data-step` syntax as the built-in systems. Corporate-family mode routes `cover`, `toc`, `section`, `content`, and `data` to the matching shell, embeds only that shell's fixed crops, and wraps report DOM in its confirmed editable region. It never embeds a complete source screenshot.
- `provenance.json` records every VI item, eligibility, actual compiled state, concrete usage targets, every neutral fallback, the source/crop hashes, and the motion boundary.

The output is project-local. Do not copy it into `assets/visual-systems/`, rename it to one of the eight built-in ids, add it to the built-in router, or treat it as a globally available style.

## Boundary Compilation Policy

- `eligible: true` means an `observed` or `extension` item may enter deterministic compilation. Eligibility alone never implies use.
- Set `compiled: true` only when the item actually enters a token, CSS rule, template DOM branch, manifest execution field, or explicit preserve/forbidden guardrail. Every compiled record must list concrete `usage` targets.
- An unused `observed` or `extension` item remains `eligible: true`, `compiled: false`, with an empty usage list. Descriptive layout, component, imagery, evidence, or miniature copy must not be promoted merely because it appears in the confirmed JSON.
- Compile `extension` items only as report adaptations and preserve their extension status in provenance.
- Retain `unknown` records with `eligible: false`, `compiled: false`, and no usage. Never use an unknown item as a token source or relabel it as observed.
- When runtime completeness requires a missing value, use a neutral reversible `fallback`. Record its token or executable-layout field, value, source, basis, and concrete usage in `fallback_records`; never describe it as reference evidence.

The compiler reads structure only from the exact `executable_layout` object defined in `static-reference-vi.md`. It uses those enums to choose cover split versus single-column DOM, card grid versus stack/single-focus content, row versus column process, evidence/data DOM, image placement/ratio/fit/treatment, module border/radius/shadow language, density, alignment, and focus. Natural-language descriptions remain review context and may supply parseable scalar tokens such as an explicit margin, but they are not the primary source of structural branching.

`scripts/project_theme_layout.py` is the machine single source for the enum sets, neutral fallbacks, and cover/image, content/columns, and data/columns compatibility matrices. Both VI validation and the production theme loader call it. Every accepted concrete value must reach a DOM branch, computed CSS geometry, manifest execution field, and accurate provenance usage; a class name or layout id alone does not count. Undefined combinations fail during VI validation with the incompatible fields and allowed values. Do not silently normalize a concrete contract. Compatibility-aware unknown fallbacks remain allowed only when they are separately recorded and the unknown boundary stays `compiled: false`.

The v1 image placement program is exact: split covers accept left/right, single-column covers accept top/bottom/background, and a source/chart split additionally requires left/right. Background creates an absolute visual layer and requires cover fit. Content stacks and single-focus pages are one-column; card grids accept one to three. Chart/table focus pages are one-column, source/chart splits are two-column, and metric grids apply one to three columns to their inner metric cards.

The compiler may derive a fixed pixel value from an explicit VI measurement, such as converting a confirmed five-percent outer margin against the 1600px theme canvas. Record that deterministic derivation in the token basis. Do not use free-form model judgment inside the script.

## Semantic Rhythm Policy

The project theme does not use heading margins to encode relationships. Its scoped low-level reset sets `h1`, `h2`, `h3`, and `p` margins to zero; the nearest semantic container owns the space between its direct children through CSS `gap`. This prevents a more-specific reset from silently collapsing an intended label-to-title distance.

The confirmed `executable_layout.density` enum deterministically selects five relationship tokens:

| Density | label → title | title → lede | page heading → content | card title → body | evidence → source |
|---|---:|---:|---:|---:|---:|
| `low` | 24px | 20px | 44px | 14px | 20px |
| `medium` | 18px | 16px | 32px | 12px | 18px |
| `high` | 12px | 10px | 24px | 8px | 12px |

These compile to `theme.json` tokens and `--pt-rhythm-*` CSS properties, with exact provenance usage targets attributed to `executable_layout.density`. An unknown density does not become observed; it uses the neutral `medium` scale and produces separate field and token fallback records.

Generated templates mark the relationship owner and its direct endpoints with `data-rhythm-check`, `data-rhythm-from`, and `data-rhythm-to`. Horizontal relationships additionally use `data-rhythm-axis="inline"`; vertical relationships default to the block axis. `check_html_deck.py` measures the computed browser rectangles and fails when the actual distance differs from the declared token. This check complements overflow QA: a page can fit its viewport and still have a broken visual relationship.

## Corporate Template-Family Shell Boundary

For v1.3/v1.4 `corporate_fidelity`, compile a role-routed shell family from the exact confirmed sources and regions:

- Crop every `canvas_bbox` first, then crop each shared asset with floor(left/top) and ceil(right/bottom) pixel bounds in that canvas. Encode each crop as deterministic offline PNG and record source-image, source-page, source bbox/pixel bbox, crop dimensions, and crop SHA-256.
- For each v1.4 replaceable region, verify it belongs to one declared shared asset, deterministically fill only the declared variable pixels from a sufficiently uniform sampled edge, and preserve both original and cleaned provenance. The loader decodes the compiled PNG and fails if any pixel in the declared region differs from the recorded fill. A missing declaration means no cleaning; the Compiler never searches for a page-number string or customer-specific coordinate.
- Route every report page by `data-shell-role` to exactly one of `cover/toc/section/content/data`; verify `data-source-page-id` for observed shells and the empty mapping for extensions.
- Place each shell's crop bytes at its exact normalized placement bbox. Mark fixed elements with locked-region id, asset id, source-page id, crop hash, and `data-fixed-motion="none"`.
- Wrap report content in that shell's one `data-editable-region`. Report DOM, layout changes, and Runtime fragments must remain descendants of that wrapper and use only the shell's allowed role.
- Apply `animation:none`, `transition:none`, and `transform:none` to every fixed shell and fixed crop. The loader parses actual HTML, decodes every `src` data URI, validates PNG MIME/decodability/dimensions, recomputes SHA-256, and requires exact equality between actual style/bbox and manifest placement. It also rejects role/source mapping drift, crop-count drift, editable-region drift, fixed-element fragment classes, or weakened fixed-motion CSS.
- Never embed the complete screenshot in `templates.html` or CSS. Example body text, charts, and numbers in the screenshot are extraction exclusions, not reusable background material. Corporate Report IR output removes the page-shell's derived page-number field and uses the Runtime's single global current/total indicator. When a v1.4 cleaned `runtime_page_number` region exists, this leaves one visible page number; an older crop with undeclared page-number pixels must be migrated and reconfirmed before making that claim.

The shell family promises screenshot-visible pixels and confirmed positions only. It does not reconstruct a source master, vectors, fonts, hidden page types, or movement. Roles absent from all supplied screenshots remain `extension/proposed` even after VI confirmation; confirmation accepts the proposal, not a false claim that it was observed.

## Render Through The Shared Runtime

Render a report explicitly with the compiled directory:

```bash
python scripts/render_visual_system.py \
  --content /absolute/path/to/content.json \
  --project-theme /absolute/path/to/project-theme \
  --source-image /absolute/path/to/local-visual.svg \
  --source-kind illustrative \
  --output /absolute/path/to/report.html
```

Use `--source-kind verified` only when the local image is grounded in confirmed source material. A generated image, ordinary local file, or missing source kind remains illustrative and receives the adjacent `示意 / 待核实` label. Project themes never weaken this fail-safe source contract.

The renderer validates the four project-theme files, rejects symlinks, extra files, remote assets, invalid selectors, and incomplete templates. For every machine-executed layout field it also checks that manifest value, structure source, provenance status/value/compiled flag/usage targets, neutral fallback when applicable, and template `data-layout` ids agree. It then injects project CSS and pages into `assets/html-deck-template/index.html`. Do not fork the Runtime or add a project-specific state machine.

The eight built-in calls remain unchanged:

```bash
python scripts/render_visual_system.py \
  --content /absolute/path/to/content.json \
  --theme rigorous-consulting-report \
  --output /absolute/path/to/report.html
```

## Corporate Profile Promotion

Keep every compiled result project-local by default. Only a `corporate_fidelity`
result with the current conversation-bound handoff schema, exact VI/reference hashes,
and a successful `theme_runtime.load_project_theme()` check may enter the explicit
profile workflow in `profile-memory.md`.

Use `profile_store.py create` for a new enterprise or `update` only after the customer
explicitly makes the new template permanent. The store validates this source theme,
recompiles the same confirmed VI/reference bytes under a profile-only identity with no
project corrections, verifies structural/CSS/template equivalence, and calls the same
project-theme loader again. It never adds profile output to `assets/visual-systems/`.

For a later project, load the live-validated binding's relative theme path through the
same renderer `--project-theme` route and pass the binding's current report mode with
`--target-mode reading|presentation`. The archived theme's compilation mode is
provenance, not a corporate-brand boundary; a mode-only change must not create v2.
Do not copy compiler/loader validation into a second profile-specific implementation
and do not silently replace a damaged profile with a built-in theme.

## Verification

For the compiled theme and at least one full sample deck:

1. Compile twice into separate directories and compare every output file hash.
2. Compile a second, schema-complete VI with an intentionally opposite layout grammar. Compare `templates.html`, key DOM classes, structural CSS, `layout_variants`, and `identity.composition`; all must differ.
3. Parameterize every allowed compatibility-matrix pair and every remaining scalar enum. Require an expected DOM order/branch or structural CSS value for each legal case, and a clear validation error for every illegal pair.
4. Inspect `provenance.json` for distinct observed, extension, unknown, and fallback records, concrete usage targets, and at least one eligible-but-unused record that remains `compiled: false`.
5. Run `check_assets.py --strict-offline` on the HTML.
6. Run `check_html_deck.py` at 1366×768, 1600×900, and 1920×1080; require empty overflow and semantic-rhythm failure lists on every page.
7. Build a contact sheet from the 1600×900 screenshots.
8. Compare all original references, the unified VI board, and the final themed sample. Confirm role routing, fixed crops, safe regions, composition, hierarchy, components, image treatment, and evidence language—not only colors—carry through.
9. Tamper one compiled copy at a time: fixed crop bytes, placement style, shell role, and source-page mapping. Require the project-theme loader to fail closed in every case.

Use fixed synthetic sample content for visual acceptance and label it as illustrative. Do not present the sample as customer evidence or achieved results.

## Remaining Model Work

The compiler does not understand images, choose report content, decide a narrative, verify evidence provenance, or create project-specific motion. Those remain model/Skill/report-task responsibilities within their existing confirmation and verification gates. This slice does not support video, dynamic-reference analysis, more than three corporate stills, multiple reconstruct references, dual-screen presentation, independent Logo upload, or an HTML editor.
