# Reference

Detailed reference for installation, capability boundaries, CLI usage, programmatic API, and delivery annotation. For the contract, hard constraints, chart type table, and transform templates, see [SKILL.md](../SKILL.md).

---

## Installation

```bash
pip install -r requirements.txt
```

Dependencies (compatible ranges, no longer `==` pinned): `pandas>=3.0.1,<4.0.0`, `numpy>=2.4.3,<3.0.0`, `openpyxl>=3.1.5,<4.0.0`, `xlrd>=2.0.1,<3.0.0`. ECharts JS is bundled in `assets/` (no CDN, fully offline).

Environment self-check: `python {skill_base}/scripts/cli.py --doctor` — prints a version matrix (Python / pandas / numpy / openpyxl / xlrd: required minimum vs installed vs `ok`) plus `assets/` integrity, as JSON. Read-only: parses no data and writes no files. Run it before blaming the skill when versions have drifted; to reproduce an exact old environment, `pip install pkg==<installed version from --doctor>`.

Self-test (developer): `python {skill_base}/scripts/regression_check.py` — end-to-end regression suite (real CLI subprocesses): validator unit tests incl. sandbox escape PoCs, all parsers, 32 chart types, multi-chart mode, flags/themes/lang, transform golden patterns, error paths, plus the P0/P1/P2 fix cases (sandbox closure, total-row exclusion, trend ordering, gauge target, grain reconciliation, column-name collision). Test data goes to a temp dir; exit 0 = all pass.

---

## Capability Boundaries

**Supported:** CSV (.csv=comma / .tsv=tab / .txt=auto-detect delimiter), Excel (.xlsx/.xls), JSON (.json，支持 1 层嵌套对象，自动展开为「父.子」点分列，列名规范化后为「父_子」); 32 chart types (see SKILL.md); 3 themes (`--theme default|classic|dark`); multi-file auto-merge (recommended ≤ 10 files); single file ≤ 100 MB (≤ 50 MB recommended); auto-detects UTF-8/GBK/GB2312/UTF-16/Latin-1.

**Not supported:** Databases (export to CSV first), real-time/streaming data, >100 MB files, nested JSON >1 level, non-tabular data (images/audio/video). Auto-merge requires ≥50% column overlap.

**Map capability (map / lines):** only the offline **China province-level** GeoJSON is bundled (`assets/china.json`, auto-registered as `map: "china"`). Region names must be Chinese province full names or common short names (北京/广东/新疆/内蒙古…), normalized via `_REGION_ALIASES`; non-matching names are skipped and disclosed in `plot_stats.extra.unmatched`. World maps, city-level maps, or custom regions are **not supported** (would require bundling additional GeoJSON, which is out of scope).

**Network requirement:** None. ECharts JS is bundled in `assets/` and inlined into each HTML output; charts render fully offline with no external dependencies.

**Security:** transform 代码由沙箱强制校验（关键字黑名单 + AST 白名单 + 安全 builtins + 危险属性名/模块路径封禁），违规会返回带 `suggestion` 的结构化错误，按提示修正重试即可，无需用户确认。除裸名关键字外，`pd.read_csv`/`np.save`/`to_pickle` 这类属性名，以及 `pd.io.*` / `np.lib.*` 整棵子树（`pd.io.common.get_handle`、`np.lib.format.open_memmap` 等文件与网络句柄工厂）均在 AST 层被拦。机制细节见下方 Transform Code Generation。

---

## Data Parsing — CLI Reference

> `{skill_base}` = root directory of this skill (contains `SKILL.md`).

```bash
# Single file
python {skill_base}/scripts/data_parser.py <file_path> [--summary] [--skiprows N] [--header-row N] [--sheet <name|index>]

# Multiple files
python {skill_base}/scripts/data_parser.py <file1> <file2> ... [--summary]

# Multiple files with auto-merge
python {skill_base}/scripts/data_parser.py <file1> <file2> ... [--merge] [--summary]
```

**Flags:**
- `--summary` — output a JSON data summary (shape, columns, dtypes, missing, sample, stats) instead of a text preview.
- `--merge` — attempt to merge multiple files into one DataFrame.
- `--skiprows N` / `--header-row N` *(single-file only)* — **these two are the same operation, not two decisions**: both make the 0-indexed row N the header and drop everything above it (`skiprows=N` → pandas `skiprows=N`; `header_row=N` → pandas `header=N`; when both are passed, `header-row` wins). Always go straight to `--header-row N` — pick the row you want as column names and count from 0. Use when the file has leading junk rows (notes, blanks) or multi-row headers (merged cells, sub-headers).
- `--sheet <name|index>` *(single-file only)* — pick an Excel sheet by name or 0-indexed position (default: 0). An explicitly named/numbered sheet that does not exist returns a structured `DATA_PARSE_ERROR` listing `available_sheets`; only the default sheet 0 falls back automatically (first non-empty sheet is used when sheet 0 is empty).
- N must be determined by inspecting the actual data (run `data_parser.py` once without flags to see the raw layout). Never assume a fixed N.

**Merge behavior:**
- Identical columns → vertical concat (adds a `source_file` column to indicate each row's origin file — 下游 transform 代码必须考虑这个额外列).
- ≥50% overlap → horizontal join on shared key. Overlapping non-key columns from later files are merged back with `combine_first` (non-null values from both files survive); genuinely `_dup`-suffixed source column names are preserved untouched.
- No common structure → error (advise analyzing separately).
- `--merge --summary` 模式下 stdout 为纯 JSON，合并方式体现在 JSON 的 `merge_type` 字段（不打印额外文本行，保证机器可读）。

**ID-column protection:** columns named id/编号/学号/工号/邮编/电话/... or containing leading-zero values (e.g. `007`) are kept as strings — never silently coerced to numbers (which would destroy the leading zeros). The ASCII hints (`id`, `code`) match on non-alphanumeric boundaries, so `student_id`/`user_code` still count as IDs while `width`/`valid`/`paid`/`android` do not. All other numeric-looking string columns are still auto-converted.

**Numeric coercion is observable:** string columns are cleaned (currency symbols → thousands separators → `%` → Chinese magnitude suffixes `亿`/`万`/`千`, so `8.5万` → `85000`) and then coerced. If only *some* cells fail to parse but ≥50% succeed, the column still becomes numeric with the failures set to missing, and an advisory is emitted naming the column and the number of discarded cells. Below 50% the column is left as text. Previously a single stray `-` silently degraded a whole column to string with no warning.

**Total/subtotal rows are excluded:** rows whose label cell is exactly 合计/小计/总计/共计/total/subtotal/grand total/sum/all are dropped before statistics and plotting (a hand-added total row double-counts the sum and reports itself as the max). The exclusion is never silent — it appears in `data_parser.py --summary` as `warnings`, and in chart output as an `advisories` entry.

**Column-name collisions are de-duplicated:** after normalization, colliding names get `_2`, `_3` suffixes (e.g. `Sales Amount` + `sales-amount` → `sales_amount`, `sales_amount_2`). Previously the collision made `df[col]` return a DataFrame and crashed with `'DataFrame' object has no attribute 'dtype'`.

**Delimited files are read as strings** (`dtype=str`) and numerified in one cleaning pass — this is what makes leading-zero protection possible; missing-value tokens (`NA`, empty, etc.) are still normalized to NaN by pandas.

**Argparse CLI:** both `data_parser.py` and `cli.py` parse arguments with argparse; unknown flags / missing values / bad types return the same structured JSON error (`code_name` + `details.suggestion`) instead of bare usage text.

**Formats:** .csv (comma) / .tsv (tab) / .txt (auto-detect delimiter: `,`/`\t`/`;`/`|`) + auto-detect encoding (UTF-8/UTF-8-BOM/GBK/GB2312/UTF-16/Latin-1, single shared fallback list), .xlsx/.xls (first non-empty sheet), .json (array format; 1-level nested objects are flattened into `parent.child` columns, which become `parent_child` after column-name normalization — reference the normalized names in `--x-axis`/`--y-axis`/transform code. Nested depth ≥2 or array-valued fields are rejected with a structured error).

**Column name normalization:** Parsed column names are normalized by `_normalize_col`:
1. Non-word characters (anything except letters, digits, `_`, and whitespace) are replaced with `_`. CJK characters count as word characters and are preserved.
2. Consecutive spaces/underscores collapse into a single `_`.
3. Leading/trailing `_` are stripped, then the name is lowercased.
4. Empty or NaN names become `unnamed`.

| Input | Normalized |
|-------|-----------|
| `Sales Amount` | `sales_amount` |
| `Revenue($)` | `revenue` |
| `销售-额%` | `销售_额` |
| `A/B` | `a_b` |
| `  Total  ` | `total` |
| (blank / NaN) | `unnamed` |

`--x-axis`, `--y-axis`, and transform code must use the **normalized** column names, not the raw header text.

**Error output:** When a `SmartChartsError` occurs, the CLI prints a JSON object to stderr:
```json
{"error": "<message>", "code": <int>, "code_name": "<NAME>", "details": {...}}
```
The `details` field always includes a `suggestion` for recovery. Any other exception is wrapped as `UNKNOWN_ERROR` (9999) JSON on stderr — in both `cli.py` and `data_parser.py`.

**Error codes:**

| Code | Name | Meaning |
|------|------|---------|
| 1001 | FILE_NOT_FOUND | File path does not exist |
| 1002 | FILE_NOT_REGULAR | Path is not a regular file |
| 1003 | FILE_FORMAT_INVALID | Unsupported file extension |
| 1004 | FILE_SIZE_EXCEEDED | File exceeds 100 MB limit |
| 2001 | DATA_PARSE_ERROR | Parsing failed (encoding, structure, sheet missing, etc.) |
| 2002 | DATA_MERGE_ERROR | Auto-merge impossible (no common structure between files) |
| 2003 | DATA_EMPTY | File or cleaned data is empty |
| 3001 | TRANSFORM_EXEC_ERROR | Transform code execution failed (blacklist/AST/timeout) |
| 3002 | TRANSFORM_NO_RESULT | Transform code did not produce `result` variable |
| 3003 | TRANSFORM_INVALID_RESULT | `result` is not a DataFrame |
| 3004 | TRANSFORM_EMPTY_RESULT | `result` DataFrame is empty |
| 4001 | CHART_GENERATION_ERROR | Chart generation failed |
| 4002 | CHART_TYPE_UNSUPPORTED | Unsupported chart type |
| 4003 | CHART_CONFIG_ERROR | Axis field does not exist in DataFrame |
| 9999 | UNKNOWN_ERROR | Unclassified error |

---

## Chart Generation — CLI Reference

```bash
python {skill_base}/scripts/cli.py \
  <file_path> <chart_type> \
  --title "Chart Title" \
  --x-axis "date" \
  --y-axis "revenue profit" \
  --transform-code "<pandas code>" \
  --annotation "<delivery text>" \
  --subtitle "<time range / filter / source>" \
  --x-name "<X axis display name>" \
  --y-name "<Y axis display name>" \
  --series-name "<series display name>" \
  --sort none|value --y-scale --label auto|all|key \
  --skiprows N --header-row N --sheet <name|index> \
  --lang zh|en \
  --theme default|classic|dark \
  --output-dir "./output" \
  --width 900 --height 560
```

**Parameters:**
- `file_path` (required) — path to the data file.
- `chart_type` (required) — one of the 32 types listed in SKILL.md.
- `--title` (default follows `--lang` / data language) — chart title.
- `--x-axis` (auto-detected if omitted) — column name for x-axis.
- `--y-axis` (space-separated; defaults to first 5 numeric columns, or first 3 other columns if none numeric) — column name(s) for y-axis.
- `--transform-code` (optional) — LLM-generated pandas code, validated + executed before rendering.
- `--annotation "<text>"` (optional) — delivery annotation text injected into the HTML below the chart（「图表说明」区块）. Pass it on the single generating call — you do **not** need a prior `--dry-run` (see 交付解读规范 below). The success output's `annotation_source` is `'user'` when you supplied it and `'default'` when the built-in template was substituted (a `default` value also raises an advisory).
- `--subtitle "<text>"` (optional) — context line under the title: time range, filter conditions, data source. Rendered as `<subtitle> · Smart Charts · <timestamp>`; omitted → the default `Smart Charts · <timestamp>` line is kept unchanged. Pairs with a conclusion-style `--title` (标题写结论，副标题补口径).
- `--x-name "<text>"` (optional) — X 轴显示名，覆盖列名。缺省时轴名 = `--x-axis` 列名。仅对**显示轴名的图表**生效（line/bar/area/stacked_bar/pie/scatter/effect_scatter/pictorial_bar/waterfall/histogram/pareto/combo 等有 `axisName-x` graphic 的图）；heatmap/gauge/sankey/map/lines/calendar/theme_river 等本就无轴名的图不受影响（也不报错）。
- `--y-name "<text> ..."` (optional) — Y 轴显示名，可多个，按 `--y-axis` 顺序对应；缺省时回退到列名。多 y 轴（combo 双轴等）可传多个：`--y-name "营收额" "利润率"`。
- `--series-name "<text>"` (optional) — 系列显示名，覆盖**第一个可见系列**。适用于单系列图（bar/line/gauge/heatmap/treemap/sankey 等），也覆盖原本写死默认文本的 B 类图（如 heatmap 的「热力图」、gauge 的「仪表盘」）。多系列请用 `--series-names`。
- `--series-names "<text> ..."` (optional) — 系列显示名，按**可见系列顺序**对应覆盖（combo 的柱/线、boxplot 的箱线图/异常值、pareto 的柱/累计线等）。waterfall 的透明底座是内部系列，自动跳过、不占名额。缺省时回退到列名（A 类图）或默认文本（B 类图）。
- `--sort none|value` (default: `none`) — category ordering for bar/stacked_bar. `value` sorts categories by the first numeric y column, descending; `none` keeps data order (月份/流程阶段等自然顺序不会被误动). Pie is always frequency-descending already.
- `--y-scale` (optional, off by default) — lets the line chart's y-axis start at a non-zero baseline to amplify fluctuation (仅 `line` 生效；`area` 恒为零基线——面积编码量级，非零基线会扭曲面积占比). Bar/stacked_bar never use a non-zero baseline.
- `--label auto|all|key` (default: `auto`) — bar value labels. `auto` labels every bar when categories ≤ 20 and switches to key values only beyond that; `all` forces full labeling; `key` labels only top-3 + max/min (其余靠 tooltip；交互 HTML 悬停可读全量数值).
- `--skiprows` / `--header-row` / `--sheet` (optional) — same semantics as `data_parser.py`; passed through to the parsing step so chart generation works directly on messy-header files.
- `--lang zh|en` (optional) — force the chart text language. If omitted, the CLI auto-detects from the data: CJK character ratio > 5% in column names + string cells → `zh`, otherwise `en`. Pass `--lang` only when the user explicitly requests a specific language.
- `--label-col` (optional) — identity column (e.g. name/title). Its values become each point's `name` and appear as the tooltip title. Applies to scatter/bubble/boxplot (boxplot uses it for outlier points). If omitted, an unused string column is auto-detected (columns named 姓名/name/id/... preferred) and the choice is reported in the `assumptions` field of the success output.
- `--color-by` (optional) — color-encoding column for scatter/bubble. Numeric column → continuous coloring via `visualMap`; categorical column → one series per category with legend. Off by default — 无分析意义的着色只是视觉噪音.
- `--output-dir` (default: `./smart_charts_output`) — output directory for HTML files. **Always pass it explicitly** and point it at a user-visible location; the default lands next to whatever the current working directory happens to be, so the user may never find the files.
- `--width` / `--height` (default: 900 / 560) — HTML canvas size in px.
- `--theme` (default: `default`) — theme preset unifying the series palette and page colors: `default` (Okabe-Ito color-blind-safe palette), `classic` (ECharts native palette, blue accents), `dark` (dark background, light text; ECharts text/labels switch to light colors automatically). Applies to all 32 chart types including venn/mindmap/orgchart/liquid/spreadsheet/map/lines. Pass the same theme across a batch for visual consistency.
- `--target <float>` (optional) — business target for `gauge`/`liquid`. `plot_stats.extra.achievement` = mean ÷ target; **without `--target` it is `null`** (the auto-inferred dial scale is not a business target, so calling the ratio "达成率" would be meaningless) and an advisory is raised. Also settable per chart as `target` inside a `--charts` item.
- `--geo <name>` (optional, default `china`) — built-in map for `map`/`lines`: loads `assets/<name>.json` offline. Built-in only ships `china` (中国省级，含港澳台); any other name raises a structured error with a hint to use `--geo-path`.
- `--geo-path <path>` (optional) — self-supplied GeoJSON file for `map`/`lines`, for **any region** (world, countries, cities, districts). Takes priority over `--geo`; the map name is the file's stem (e.g. `world.json` → `registerMap("world")`). Region-name matching is **exact only** (no 简称 aliases), so the data's region column must equal the GeoJSON `properties.name` values verbatim (or normalize with `transform_code`). The GeoJSON is inlined into the HTML, keeping the output self-contained; larger/finer maps inflate the file size accordingly.
- `--doctor` (optional) — environment self-check: prints the Python/dependency/asset version matrix as JSON and exits. Parses no data, writes no files.
- `--dry-run` (optional) — stats-only mode: outputs `plot_stats`/`data_preview` with `dry_run: true` and `html_path: null`, without rendering or writing HTML. Use it only for probing column names or aggregation scripts — **not** as a required step before writing the annotation, since the real (non-`--dry-run`) output already carries `plot_stats`. Works in both single- and multi-chart mode.
- `--charts-file <path>` (multi-chart mode, recommended) — read the `--charts` JSON array from a UTF-8 file instead of a shell argument; avoids shell-escaping corruption when transform code contains CJK text or quotes. Missing/unreadable file returns a structured `FILE_NOT_FOUND` error on stderr (exit 1).
- `spreadsheet` file naming — hash covers full table content (columns + values), so two same-schema tables with different data never overwrite each other.

**Output:** On success, prints a JSON object to stdout and exits with code 0:
```json
{"chart": {"success": true, "dry_run": false, "html_path": "./output/Title_abc123.html", "chart_type": "bar", "title": "Title", "source_rows": 34, "plotted_rows": 2, "unique_entities": 2, "data_rows": 2, "data_preview": [{"name": "兼职", "value": 20}, {"name": "专职", "value": 12}], "annotation_source": "user", "plot_stats": {"family": "A", "x_col": "name", "x_cardinality": 2, "series": [{"name": "value", "max": {"value": 20, "at": "兼职"}, "min": {"value": 12, "at": "专职"}, "mean": 16.0, "sum": 32.0, "top3": [], "bottom3": []}]}}}
```
**Note `plot_stats` is present in the normal (non-dry-run) response** — there is no need for a separate `--dry-run` call to obtain it.

`data_rows` is the number of rows fed into plotting (after transform); `data_preview` is the first 10 rows of the final plotting data (the same data the renderer consumed, with NaN → null). Use them to sanity-check aggregation grain in-band — no need to open the HTML to verify values.

**Grain reconciliation triple** — `source_rows` (rows before transform) / `plotted_rows` (rows actually plotted) / `unique_entities` (distinct entities, from `--label-col` if given else the x column). Mechanical check for the "forgot to de-duplicate" trap: if `plotted_rows == source_rows` nothing was aggregated, and if each series' values sum to `source_rows` rather than `unique_entities`, the aggregation counted rows instead of entities.
On failure, prints a structured JSON and exits with code 1:
- **File-level errors** (file not found, parse error, etc.): error JSON printed to **stderr**.
- **Chart-level errors** (unsupported type, transform failure, axis field missing, etc.): result JSON with `"success": false` printed to **stdout**.

Both include a `details.suggestion` field for recovery. Other exceptions are printed as plain text to stderr.

**Multi-chart mode:** when generating **2+ charts**, pass `--charts` instead of a positional `chart_type`. The file is parsed once and all charts are generated in a single process (several times faster than repeated single-chart calls):

```bash
python {skill_base}/scripts/cli.py data.csv \
  --charts '[{"type":"bar","title":"Revenue","x_axis":"city","y_axis":["revenue"]},
             {"type":"line","title":"Trend","x_axis":"date","y_axis":["revenue","profit"]}]' \
  --output-dir "./output"
```

- Each item requires `type`; optional per-chart keys: `title`, `subtitle`, `x_axis`, `y_axis` (string or array), `transform_code` (per-chart), `label_col`, `color_by`, `annotation` (per-chart delivery text), `sort`, `y_scale` (boolean), `label`, `width`, `height`, `geo`, `geo_path` (per-chart map source, same semantics as `--geo`/`--geo-path`).
- A global `--transform-code` (optional) is applied to the DataFrame once before all charts; each chart may also carry its own `transform_code`.
- Output shape: `{"charts": [{...}, ...], "summary": {"total": N, "succeeded": M, "failed": K}}` — each item has the same structure as the single-chart `chart` object (including `success`, `html_path`, and `error.details.suggestion` on failure).
- Exit code 1 only when **all** charts fail; partial failure exits 0 with per-chart errors in the `charts` array.
- Invalid `--charts` JSON (malformed, empty array, or an item missing `type`) prints a `CHART_CONFIG_ERROR` JSON with a `suggestion` to stderr and exits 1.
- `--dry-run` 同样适用于多图模式：输出各图 `plot_stats`/`data_preview`（`dry_run: true`、`html_path` 为 null），不渲染不落盘。

**多文件并行**: 各文件配置已确定且互不依赖时，用 shell 后台并行（墙钟时间 ≈ 最慢一个文件）：

```bash
for f in data/*.xlsx; do
  python {skill_base}/scripts/cli.py "$f" --charts-file "cfg_$(basename "$f" .xlsx).json" --output-dir ./out &
done; wait
```

**Language behavior:** every piece of chart text — title, series names, tooltip labels, action buttons, scroll hint, footer, and the HTML `lang` attribute — is rendered in a single consistent language. By default that language follows the data; pass `--lang zh` or `--lang en` to override (e.g. when the user explicitly asks for an English chart on Chinese data).

**Overflow behavior:** when data points exceed the zoom threshold (default 15), the HTML enables ECharts `dataZoom` (slider + inside-drag) and a horizontal scrollbar on the chart container. Users can drag the slider, scroll horizontally, or click the fullscreen button to inspect all data points. No agent action needed.

**Inline title editing:** every generated HTML title is `contenteditable`. Users can double-click the title in the browser, type a new name, and press Enter — the ECharts chart title and the saved image filename update immediately. No backend round-trip needed.

**Visualization contracts（渲染层保证的视觉规范）:**
- **Zero baseline**: bar/stacked_bar（含 combo 的 bar 系列）在数据全非负时显式锁定 y 轴 `min: 0`——从 95 画到 100 会夸大差异，零基线是柱状图的准确性红线。数据含负值时不锁定，负值柱照常显示。line 默认含 0 基线，仅显式传 `--y-scale` 才允许非零基线；area 恒为零基线。
- **`advisories` field（建议性提醒，非错误）**: 当某张图成功生成、但存在更优呈现方式或存在agent必须知道的口径改动时，成功输出的 chart 对象里会出现 `advisories: [...]` 数组。`success` 仍为 `true`、`html_path` 正常落盘——**是否换图由 agent 按语境判断，禁止机械重试**（刻意不叫 `suggestion`，避免与错误恢复语义混淆）。触发点：

  | 触发条件 | 含义 | agent 该做什么 |
  |---|---|---|
  | 饼图类别数 > 8 | 人眼难以比较角度 | 改用 `bar --sort value`，或用 transform 聚合小类 |
  | `gauge`/`liquid` 未传 `--target` | `achievement`（达成率）不可计算，已置 `null` | 需要达成率就补 `--target <目标值>`；不需要就别在解读里提这个指标 |
  | `annotation` 未由 `--annotation` 提供 | 图表说明是代码模板填充的（`annotation_source: 'default'`） | 按交付规范补写解读并重新生成 |
  | 解析期排除了合计/小计/总计行 | 这些行未计入统计与绘图 | 若本就要画合计，改用 transform 单独构造 |
  | 数值列部分单元格无法解析（成功率 ≥ 50% 时转数值） | 被丢弃的单元格数已在 advisory 中披露 | 核对列口径；要保留为分类就用 transform 显式处理 |
- **Heatmap gradient semantics**: 全非负数据（顺序型）用主题单色渐变（浅→深）；含负值数据（发散型，如相关矩阵 -1~1）自动切换双色渐变 + 中性中点，负值不再被错误地压进单色渐变。渐变取色随 `--theme` 走。
- **Title & subtitle（标题写结论）**: `--title` 应写结论而非名词短语——「营收同比增长 23%」优于「各月营收」；口径与范围信息（时间范围、筛选条件、数据来源）放 `--subtitle`，不要塞进标题。

---

## Programmatic API

```python
from scripts.chart_generator import ChartGenerator

# Single chart — returns {'chart': {'success', 'html_path'/'error', ...}}
# lang=None auto-detects from data; pass 'zh'/'en' to override (only when user asks).
# theme: 'default' | 'classic' | 'dark'（默认 default）
result = ChartGenerator(output_dir="./output", theme="default").generate_chart(
    df=df, chart_type="bar", title="Regional Revenue",
    x_axis="region", y_axis=["revenue"], lang=None,
)

# Batch — returns {'charts': [...]}，每项结构与单图一致
result = ChartGenerator(output_dir="./output").generate_multi_charts(
    df=df,
    chart_configs=[
        {"type": "bar",  "title": "Regional Revenue", "x_axis": "region", "y_axis": ["revenue"]},
        {"type": "line", "title": "Monthly Trend",   "x_axis": "month",  "y_axis": ["revenue", "profit"]},
    ],
    lang=None,
)
```

失败时 `success` 为 `False`、`error` 为结构化错误字典，不抛异常——检查 `success` 决定下一步。

---

## 交付解读规范（完整）

技能只负责算事实（`plot_stats`），解读文字由 agent 读 `plot_stats` 后自己写，再用 `--annotation` 注入 HTML（图表下方「图表说明」区块）。

流程（**一步**）：直接带 `--annotation` 生成 → 读该次输出里的 `plot_stats` 写解读。**正式输出已包含 `plot_stats`，不需要先跑 `--dry-run`。**（`--dry-run` 只在试错列名/聚合脚本时才用，见 CLI Reference。）

**事实锚点**：解读的每个数字都必须能在 `plot_stats` 或 `data_preview` 里找到出处——不得凭印象编造。注意 `plot_stats` 里的 `x_cardinality` 是 x 轴去重后的个数，写解读时要结合 x 列语义说清（如 x 是「姓名」则说「59 名学生」，而不是笼统的「59 个类别」）。

**最小结构**（2~4 句）：

1. 这张图是什么：图表类型 + 标题 + 覆盖范围（结合 x 列语义，如「59 名学生」「5 个分数段」）。
2. 最显著的事实：基于 `plot_stats` 挑 1~2 个能支持结论的点（最大/最小/趋势方向/占比/离群/累计），给出具体数值与对应标签。
3. 口径说明：一句话交代取值口径，与 `assumptions` 字段呼应。

**硬边界**：

* 只陈述 `plot_stats`/`data_preview` 能支撑的事实，不夸大、不推测数据之外的原因。
* 深度业务解读（为什么/怎么办）不是硬性要求，属结合上下文的额外发挥。

**示例**（agent 读 `plot_stats` 后写，再用 `--annotation` 注入）：

```bash
python {skill_base}/scripts/cli.py data.csv bar --title "学生总成绩对比" \
  --x-axis 姓名 --y-axis 总成绩 \
  --annotation "本图展示 59 名学生的总成绩分布。韩家芯以 98.84 分居首，马云飞 59.96 分垫底，全班平均 76.91 分。"
```

---

## Transform Code Generation

When raw data doesn't match the target chart's input format, the LLM should generate pandas code following the template in [SKILL.md](../SKILL.md). The code is validated (keyword blacklist + AST whitelist) and executed in a sandbox before chart rendering.

**Safety rules enforced:**
- Only allowed variables: `df`, `pd`, `np`
- Must produce a `result` variable (pd.DataFrame)
- Do not modify `df` in-place
- No `import`, `open`, `exec`, `eval`, `os`, `sys`, `subprocess`, file I/O, or network calls
- Only safe builtins exposed (`len`, `range`, `sorted`, etc.); `open`/`exec`/`eval`/`__import__` removed
- File/network I/O blocked at the AST attribute level, including the whole `pd.io.*` / `np.lib.*` subtrees
- **Single namespace execution**: top-level assignments, lambdas, generator expressions and nested `def`s all see the same variables, so `k = 2; df.assign(x=lambda d: d['a'] * k)` works
- Execution timeout: 10 seconds
- Max recursion depth: 500

On violation, a `CodeValidationError` is raised with `details.violations` listing the offending keywords or AST nodes, and `details.reason` explaining why.

---

## FAQ — Common Data Issues

**Q: The Excel file has multi-row headers (merged cells, sub-headers). How do I parse it?**

First run `data_parser.py` without flags to inspect the raw layout:
```bash
python {skill_base}/scripts/data_parser.py data.xls
```
Look at the printed `head(5)` to count how many rows are headers. Then re-run with `--header-row N` (0-indexed) where row N is the one you want as column names:
```bash
python {skill_base}/scripts/data_parser.py data.xls --header-row 2
```
Rows above N are dropped. The value of N depends on the actual file — never assume a fixed number.

**Q: After `--header-row`, the columns are still messy (e.g. `score_a`, `unnamed_3`). What next?**

Use `--transform-code` at chart generation to rename columns:
```bash
python {skill_base}/scripts/cli.py data.xls bar \
  --header-row 2 \
  --transform-code "result = df.rename(columns={'unnamed_0':'student_id','unnamed_1':'name','score_a':'homework','score_b':'exam'})" \
  --x-axis student_id --y-axis homework exam
```

**Q: The Excel file has multiple sheets. How do I pick one?**

```bash
python {skill_base}/scripts/data_parser.py data.xlsx --sheet "Sheet2"
# or by index
python {skill_base}/scripts/data_parser.py data.xlsx --sheet 1
```

**Q: Some cells are blank because of merged cells (only the first row of a group is filled).**

Forward-fill in transform code:
```bash
--transform-code "result = df.ffill()"
```

**Q: The data has leading note rows / blank rows before the actual header.**

Use `--skiprows N` to skip the first N rows, then read the next row as the header:
```bash
python {skill_base}/scripts/data_parser.py data.csv --skiprows 2
```

**Q: The chart shows mixed languages (e.g. Chinese data but English buttons, or vice versa).**

The CLI auto-detects the data language and renders all chart text (title, series names, tooltip, buttons, footer, HTML `lang`) in that language. If the auto-detection is wrong (e.g. a Chinese dataset with mostly English column names), force the language explicitly:
```bash
python {skill_base}/scripts/cli.py data.csv bar --lang zh
# or
python {skill_base}/scripts/cli.py data.csv bar --lang en
```
Only pass `--lang` when the user explicitly requests a specific language; otherwise let the data drive the choice.
