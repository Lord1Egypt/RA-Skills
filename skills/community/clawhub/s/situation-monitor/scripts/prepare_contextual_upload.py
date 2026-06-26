from __future__ import annotations

from pathlib import Path
import json
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "docs" / "context"
OUTPUT_DIR = ROOT / "dist" / "contextual-upload"
RUNBOOKS_DIR = OUTPUT_DIR / "runbooks"

REQUIRED_FILES = [
    "bad-image-deploy.md",
    "cluster-network-degradation.md",
    "gke-control-plane-degradation.md",
    "high-memory-pressure.md",
    "ingress-502-errors.md",
    "pod-crashloopbackoff.md",
]

SAMPLE_QUERIES = [
    "payment-processor pods entering CrashLoopBackOff after deploy",
    "user-service rollout stuck with ImagePullBackOff on broken image tag",
    "Multiple GCP products are experiencing Service issues in us-east1",
    "GKE control plane is degraded and rollouts are stuck",
    "Ingress is returning 502s across production",
]


def main() -> None:
    missing = [name for name in REQUIRED_FILES if not (SOURCE_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing required Contextual runbooks: {', '.join(missing)}")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    RUNBOOKS_DIR.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        target = RUNBOOKS_DIR / path.name
        shutil.copy2(path, target)
        copied.append(path.name)

    manifest = {
        "bundle": "situation-monitor-contextual-upload",
        "source_dir": str(SOURCE_DIR.relative_to(ROOT)),
        "runbooks": copied,
        "recommended_agent_name": "Situation Monitor KubeWatch Runbooks",
        "sample_queries": SAMPLE_QUERIES,
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (OUTPUT_DIR / "README.md").write_text(_bundle_readme(copied))

    print(f"Prepared Contextual upload bundle at {OUTPUT_DIR}")
    for name in copied:
        print(f"- {name}")


def _bundle_readme(runbooks: list[str]) -> str:
    lines = [
        "# Contextual Upload Bundle",
        "",
        "Upload every markdown file in `runbooks/` into the single Contextual agent or knowledge base used by Situation Monitor.",
        "",
        "## Files to upload",
        "",
    ]
    lines.extend(f"- `{name}`" for name in runbooks)
    lines.extend(
        [
            "",
            "## Recommended setup",
            "",
            "- Put all runbooks in one Contextual corpus so retrieval can rank across failure modes.",
            "- Keep filenames intact. The app surfaces retrieved `document_name` values directly in the report.",
            "- Do not upload unrelated repo docs as grounding material for KubeWatch.",
            "",
            "## Sample verification queries",
            "",
        ]
    )
    lines.extend(f"- `{query}`" for query in SAMPLE_QUERIES)
    lines.extend(
        [
            "",
            "Expected matches:",
            "high-memory-pressure.md for OOM or CrashLoop memory issues",
            "bad-image-deploy.md for ImagePullBackOff incidents",
            "cluster-network-degradation.md for regional cloud networking incidents",
            "gke-control-plane-degradation.md for control-plane or API availability incidents",
            "ingress-502-errors.md for gateway and ingress failures",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
