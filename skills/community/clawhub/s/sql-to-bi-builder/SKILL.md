---
name: sql-to-bi-builder
description: Convert a markdown file containing SQL queries (for example `sql.md`) into a BI dashboard specification and UI scaffold. Use when user asks to build analytics dashboards, chart pages, or BI interfaces from existing SQL statements, including query parsing, metric/dimension inference, chart recommendation, filter design, and layout generation.
---

# SQL To BI Builder

## Overview
Use this skill to transform `sql.md` query collections into a service-based BI prototype.
This skill must generate both backend and frontend services from SQL-derived artifacts.

## Workflow
1. Parse markdown SQL blocks into a normalized query catalog.
2. Infer query semantics (metrics, dimensions, time columns, grain hints).
3. Extract P0 filter candidates from SQL DSL (`WHERE` predicates) into structured filter metadata (`dsl_ast` first, regex fallback).
4. Recommend chart types from inferred semantics.
5. Build a dashboard specification with layout coordinates.
6. Generate a UI scaffold that renders the dashboard structure.
7. Generate service bundle (`services/backend` + `services/frontend`) that depends on generated SQL artifacts.

## Input Contract
Expect one markdown file with one or more SQL fenced blocks.
Use this pattern for best results:

```md
# Sales Dashboard

## card: Daily GMV
- id: daily_gmv
- datasource: mysql_prod
- refresh: 5m
- chart: auto
- filters: date, region

```sql
SELECT DATE(pay_time) AS dt, SUM(amount) AS gmv
FROM orders
WHERE pay_status = 'paid'
GROUP BY 1
ORDER BY 1;
```
```

Rules:
- Keep one logical query per SQL fenced block.
- Provide stable `id` metadata when possible.
- Keep aliases explicit (`AS alias`) to improve semantic inference.

## Python Environment Setup (Required)
Run from the skill folder.

1. Ensure `python3.11` is installed and available in `PATH`.
   If missing, follow `references/install_python311.md`.
2. Create virtual environment:

```bash
bash scripts/setup_venv.sh
```

3. Activate and verify:

```bash
source .venv/bin/activate
python --version
```

Expected version: `Python 3.11.x`.

Use `--with-dev` when dev dependencies are needed:

```bash
bash scripts/setup_venv.sh --with-dev
```

## Run Commands
After activating `.venv`, run pipeline and service generation:

```bash
python scripts/run_pipeline.py \
  --input /abs/path/sql.md \
  --out /abs/path/out \
  --with-services
```

Run each step separately when debugging:

```bash
python scripts/parse_sql_md.py --input /abs/path/sql.md --output /abs/path/out/query_catalog.json
python scripts/infer_semantics.py --input /abs/path/out/query_catalog.json --output /abs/path/out/semantic_catalog.json
python scripts/recommend_chart.py --input /abs/path/out/semantic_catalog.json --output /abs/path/out/chart_plan.json
python scripts/build_dashboard_spec.py --queries /abs/path/out/query_catalog.json --semantics /abs/path/out/semantic_catalog.json --charts /abs/path/out/chart_plan.json --output /abs/path/out/dashboard.json
python scripts/generate_ui_scaffold.py --dashboard /abs/path/out/dashboard.json --out /abs/path/out/ui
python scripts/generate_service_bundle.py --artifacts /abs/path/out --output /abs/path/out/services
```

Start generated services:

```bash
bash /abs/path/out/services/start_backend.sh
bash /abs/path/out/services/start_frontend.sh
```

## Runtime And Version Control
- Use Python `3.11.x` only.
- Keep `.python-version` at `3.11`.
- Keep `pyproject.toml` `requires-python = ">=3.11,<3.12"`.
- Install dev dependency before running upstream validator: `pip install -r requirements-dev.txt`.
- Commit changes by scope: parser, semantics, chart rules, layout rules, scaffold.
- Tag stable milestones using semantic version tags such as `v0.1.0`, `v0.2.0`.

## Outputs
- `query_catalog.json`: Parsed query units and metadata.
- `semantic_catalog.json`: Field roles, grain hints, and `dsl_filters` extracted from SQL conditions.
  `dsl_filters` includes `value_type` and `value_format`, with date support for:
  `yyyy-mm-dd`, `yyyy/mm/dd`, `yyyymmdd`, `yyyy-mm-dd hh:mm:ss`, ISO-8601, `yyyymmdd_int`, unix second/ms integers.
- `chart_plan.json`: Recommended chart type per query.
- `dashboard.json`: Final dashboard definition for rendering, including page-level `global_filters`.
- `ui/`: Static UI scaffold (`index.html`, `app.js`, `style.css`).
- `services/backend`: FastAPI backend service using generated artifacts.
- `services/frontend`: Frontend service consuming backend API.
- `services/start_backend.sh` and `services/start_frontend.sh`: service start scripts.

### UI Upgrade Notes (2026-03)
When using repo-level service UI (`services/frontend`), the upgraded experience includes:
- KPI summary strip (click-to-focus widgets)
- Layout switch (`Classic` / `Focus`)
- New `Midnight Ops` theme preset
- stronger visual hierarchy for demos

## Heuristic References
Load only the file needed for the current issue:
- SQL parsing and naming constraints: `references/sql_style.md`
- Chart mapping rules: `references/chart_rules.md`
- BI layout and widget sizing: `references/layout_rules.md`
- Python 3.11 installation and venv setup: `references/install_python311.md`

## Limits And Escalation
Treat current scripts as heuristic MVP.
Escalate for manual review when SQL includes nested CTE chains, window-heavy ranking logic, or unions with incompatible column semantics.
Fallback to `table` visualization when chart confidence is low.
