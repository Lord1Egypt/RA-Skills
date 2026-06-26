#!/usr/bin/env python3
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
INIT = SKILL_DIR / "init_task.py"
BRIEF = SKILL_DIR / "generate_subagent_brief.py"


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def require(path: Path):
    if not path.exists():
        raise SystemExit(f"Missing expected file: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="scc-smoke-") as tmp:
        base = Path(tmp)
        task = "smoke test task"
        slug = "smoke-test-task"

        run([sys.executable, str(INIT), task, str(base)], cwd="/tmp")
        run([
            sys.executable,
            str(BRIEF),
            task,
            "auth, http client, retry-related files",
            "pytest -k login_timeout -q",
            str(base),
        ], cwd="/tmp")

        require(base / "notes" / slug / "plan.md")
        require(base / "notes" / slug / "todo.md")
        require(base / "notes" / slug / "checkpoint.md")
        require(base / "notes" / slug / "subagents" / "investigation.brief.md")
        require(base / "notes" / slug / "subagents" / "implementation.brief.md")
        require(base / "notes" / slug / "subagents" / "test.brief.md")

        print("small-context-coding smoke test: OK")
        print(f"workspace: {base}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
