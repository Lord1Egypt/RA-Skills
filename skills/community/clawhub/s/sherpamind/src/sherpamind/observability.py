from __future__ import annotations

from pathlib import Path
import json

from .analysis import get_api_usage_summary, get_dataset_summary, get_enrichment_coverage
from .freshness import get_sync_freshness
from .vector_index import get_vector_index_status
from .vector_exports import get_retrieval_readiness_summary
from .paths import ensure_path_layout
from .sync_state import get_json_state


def generate_runtime_status_artifacts(db_path: Path) -> dict:
    paths = ensure_path_layout()
    runtime_dir = paths.docs_root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    coverage = get_enrichment_coverage(db_path)
    freshness = get_sync_freshness(db_path)
    usage = get_api_usage_summary(db_path)
    dataset = get_dataset_summary(db_path)
    vector = get_vector_index_status(db_path)
    retrieval = get_retrieval_readiness_summary(db_path)
    cold_bootstrap = get_json_state(db_path, "service.cold_bootstrap", default={}) or {}

    status_md = [
        "# SherpaMind Runtime Status",
        "",
        "## Dataset summary",
        "```json",
        json.dumps(dataset, indent=2),
        "```",
        "",
        "## Enrichment coverage",
        "```json",
        json.dumps(coverage, indent=2),
        "```",
        "",
        "## Sync freshness",
        "```json",
        json.dumps(freshness, indent=2),
        "```",
        "",
        "## API usage",
        "```json",
        json.dumps(usage, indent=2),
        "```",
        "",
        "## Cold bootstrap status",
        "```json",
        json.dumps(cold_bootstrap, indent=2),
        "```",
        "",
        "## Vector index status",
        "```json",
        json.dumps(vector, indent=2),
        "```",
        "",
        "## Retrieval readiness",
        "```json",
        json.dumps(retrieval, indent=2),
        "```",
    ]
    out = runtime_dir / "status.md"
    out.write_text("\n".join(status_md) + "\n")
    return {"status": "ok", "output_path": str(out)}
