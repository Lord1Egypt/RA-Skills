#!/usr/bin/env python3
"""Scaffold a minimal SN94 autoresearch competition task repo."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from textwrap import dedent


def write(path: Path, text: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | 0o111)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="Output repo directory")
    parser.add_argument("--slug", required=True, help="Competition slug")
    parser.add_argument("--title", required=True, help="Human title")
    parser.add_argument("--hardware", default="cpu", help="cpu, cuda, or another declared target")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.out).expanduser().resolve()
    if root.exists() and any(root.iterdir()) and not args.overwrite:
        raise SystemExit(f"{root} is not empty; pass --overwrite to replace scaffolded files")
    root.mkdir(parents=True, exist_ok=True)

    problem = {
        "slug": args.slug,
        "title": args.title,
        "version": 1,
        "hardware": args.hardware,
        "submission_type": "patch",
        "allowed_patch_paths": ["submission/**"],
        "setup_command": "./scripts/setup.sh",
        "benchmark_command": "./scripts/benchmark.sh",
        "result_path": "results/result.json",
        "max_patch_bytes": 65536,
        "timeout_seconds": 300,
        "objective": {
            "metric_name": "score",
            "higher_is_better": True,
            "acceptance_floor": 0.0,
            "tie_breakers": ["artifact_size_bytes", "runtime_seconds"],
        },
    }

    write(
        root / "README.md",
        dedent(
            f"""\
            # {args.title}

            This is an SN94 autoresearch task repo skeleton. Replace the
            placeholder benchmark with the actual scorer for your problem.

            Miners may only edit files under `submission/`. Validators replay
            from a pinned ref, apply the miner patch, run `./scripts/setup.sh`,
            then run `./scripts/benchmark.sh` and read `results/result.json`.

            Reward-active validation should use hidden data, seeds, or manifests
            supplied by the backend or mounted by the validator host. Public
            examples here are only for local development and smoke checks.
            """
        ),
    )
    write(root / "problem.yaml", _yaml(problem))
    write(
        root / "submission/solution.py",
        dedent(
            """\
            def solve(example):
                """ + '"""Starter solution. Replace with the task-specific artifact."""' + """
                return example
            """
        ),
    )
    write(root / "results/.gitkeep", "")
    write(root / "src/task_harness/__init__.py", '"""Task harness placeholder."""\n')
    write(
        root / "scripts/setup.sh",
        dedent(
            """\
            #!/usr/bin/env bash
            set -euo pipefail
            python3 --version >/dev/null
            """
        ),
        executable=True,
    )
    write(
        root / "scripts/validate_submission.py",
        dedent(
            """\
            #!/usr/bin/env python3
            import sys
            from pathlib import Path

            MAX_BYTES = 65536
            FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".so", ".dylib", ".dll"}
            FORBIDDEN_PARTS = {"__pycache__", ".git", ".env"}

            def main() -> int:
                root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
                submission = root / "submission"
                if not submission.exists():
                    raise SystemExit("submission/ is missing")
                total = 0
                for path in submission.rglob("*"):
                    if not path.is_file():
                        continue
                    parts = set(path.parts)
                    if parts & FORBIDDEN_PARTS or path.suffix in FORBIDDEN_SUFFIXES:
                        raise SystemExit(f"forbidden generated/binary file: {path}")
                    total += path.stat().st_size
                if total > MAX_BYTES:
                    raise SystemExit(f"submission too large: {total} > {MAX_BYTES}")
                return 0

            if __name__ == "__main__":
                raise SystemExit(main())
            """
        ),
        executable=True,
    )
    write(
        root / "scripts/benchmark.py",
        dedent(
            """\
            #!/usr/bin/env python3
            import hashlib
            import json
            import time
            from pathlib import Path

            start = time.perf_counter()
            files = sorted(p for p in Path("submission").rglob("*") if p.is_file())
            payload = b"".join(p.read_bytes() for p in files)
            digest = hashlib.sha256(payload).hexdigest()

            # Placeholder deterministic score. Replace with the real task scorer.
            artifact_size = len(payload)
            score = round(1.0 / (1.0 + artifact_size / 100000.0), 8)
            result = {
                "score": score,
                "primary_metric": score,
                "valid": True,
                "metrics": {
                    "artifact_size_bytes": artifact_size,
                    "runtime_seconds": round(time.perf_counter() - start, 6),
                    "submission_sha256": digest,
                },
            }
            Path("results").mkdir(exist_ok=True)
            Path("results/result.json").write_text(json.dumps(result, indent=2) + "\\n")
            """
        ),
        executable=True,
    )
    write(
        root / "scripts/benchmark.sh",
        dedent(
            """\
            #!/usr/bin/env bash
            set -euo pipefail
            python3 scripts/validate_submission.py .
            python3 scripts/benchmark.py
            """
        ),
        executable=True,
    )
    write(
        root / "tests/test_replay_contract.py",
        dedent(
            """\
            import json
            from pathlib import Path

            def test_problem_contract_mentions_submission_surface():
                text = Path("problem.yaml").read_text()
                assert "submission/**" in text
                assert "results/result.json" in text

            def test_result_contract_after_benchmark():
                result = Path("results/result.json")
                if result.exists():
                    data = json.loads(result.read_text())
                    assert "score" in data
                    assert data.get("valid") is True
            """
        ),
    )

    print(root)
    return 0


def _yaml(value: object, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(_yaml(item, indent + 2).rstrip())
            elif isinstance(item, bool):
                lines.append(f"{pad}{key}: {'true' if item else 'false'}")
            else:
                lines.append(f"{pad}{key}: {json.dumps(item) if isinstance(item, str) else item}")
        return "\n".join(lines) + "\n"
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(_yaml(item, indent + 2).rstrip())
            elif isinstance(item, bool):
                lines.append(f"{pad}- {'true' if item else 'false'}")
            else:
                lines.append(f"{pad}- {json.dumps(item) if isinstance(item, str) else item}")
        return "\n".join(lines) + "\n"
    return f"{pad}{value}\n"


if __name__ == "__main__":
    raise SystemExit(main())
