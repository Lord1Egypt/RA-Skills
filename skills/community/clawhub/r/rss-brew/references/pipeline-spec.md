# RSS-Brew Pipeline Specification

This file details the procedural logic of the RSS-Brew pipeline, which is orchestrated by `scripts/run_pipeline_v2.py`.

## 1. Execution Entrypoint
The main entry point is: `scripts/run_pipeline_v2.py`.
When executing, the script resolves all sub-steps relative to the skill's root directory (the directory containing this `references/` folder).

## 2. Core Pipeline Stages (Called by Orchestrator)

### Step 1: Fetch & De-duplication (via `core_pipeline.py`)
- **Goal:** Fetch feeds, compare against `processed-index.json`, output new articles to `new-articles.json`.
- **Input:** `sources.yaml`, `processed-index.json`
- **Output:** `new-articles.json` (staged)

### Step 2: Scoring (via `phase_a_score.py`)
- **Model:** CHEAP (configurable via env var `RSS_BREW_PHASE_A_LIMIT`)
- **Goal:** Score new articles based on heuristics/keywords.
- **Output:** `scored-articles.json` (staged)

### Step 3: Deep Analysis (via `phase_b_analyze.py`)
- **Model:** GLM (Default)
- **Goal:** Generate English summary, Chinese abstract, and Deep Analysis/Quotes.
- **Output:** `deep-set.json` and per-category markdown files (staged)

## 3. Resilience & State Management (Phase 1/2 Logic)

### 3.1 Per-Run Manifest (`<run_id>.json`)
Every run generates a manifest at `run-records/<date>/<run_id>.json`, tracking:
- `status`: running -> staged -> finalize_in_progress -> committed/failed
- `new_articles`, `deep_set_count`
- `staging_path`, `published_path`
- `delivery_status` (separate from pipeline status)

### 3.2 Winner Selection Logic
Winner is selected from **committed** manifests on the same day, ranked by:
1. `new_articles` (desc)
2. `deep_set_count` (desc)
3. `finalize_finished_at` (asc)

### 3.3 Guardrail
If an existing committed winner has `new_articles > 0`, any subsequent run on the same day with `new_articles = 0` will skip scoring/analysis, setting its failure reason to `guardrail_nonzero_committed_winner_preserved`.

### 3.4 Finalize & Publish (Transactional Step)
- Protected by `daily/<date>/.finalize.lock` (fcntl.flock)
- **Promotion:** Only the winner's staged contents (including index/metadata snapshots) are copied to top-level outputs and versioned paths (`daily/<date>/<run_id>/`).
- **CURRENT Pointer:** Final step writes `daily/<date>/CURRENT` pointing to the winning `run_id`.

## 4. Model Routing

| Stage | Default Model | Alias | Notes |
|-------|---------------|-------|-------|
| Phase A | `CHEAP` | CHEAP | Configurable via environment variable for testing. |
| Phase B | `GLM` | GLM | Used for complex summarization/analysis. |
- Model configuration is hardcoded within Phase A/B scripts, not configurable via SKILL.md or environment variables (except for Phase A limit).

## 5. Output Artifacts
- Final digests: `daily/<date>/<run_id>/digests/daily-digest-YYYY-MM-DD.md`
- Next Draft PDF: Rendered via `scripts/render_digest_pdf_nextdraft.py` using template in `assets/`.
