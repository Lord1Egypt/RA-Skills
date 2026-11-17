"""Build the end-to-end fixtures in a scratch folder.

    python3 tests/e2e/prepare.py --out /some/scratch/dir

prints one `vl.py start` command per fixture (with that fixture's own log
folders, so the user's real ~/.claude and ~/.codex are never read)."""
from __future__ import annotations

import argparse
import base64
import json
import shlex
import shutil
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TESTS))
sys.path.insert(0, str(TESTS.parent / "scripts"))

from e2e.scenarios import SCENARIOS  # noqa: E402

APPS = TESTS / "fixtures" / "apps"
FAKE_OPENAI = "sk-proj-" + "Q7wE9rT1yU3iO5pA7sD9fG1hJ3kL5zX7"  # split so the repo never holds a key-shaped string


def _jwt(role: str) -> str:
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256", "typ": "JWT"}) + "." + enc({"iss": "supabase", "role": role}) + "." + "fakeSignatureFakeSig"


FILL = {"{{OPENAI_KEY}}": FAKE_OPENAI, "{{ANON_JWT}}": _jwt("anon")}


def prepare(out) -> dict:
    out = Path(out).resolve()
    result = {}
    for name, build in SCENARIOS.items():
        base = out / name
        if base.exists():
            shutil.rmtree(base)
        project = base / "project"
        shutil.copytree(APPS / name, project)
        for f in project.rglob("*"):
            if f.is_file():
                text = f.read_text(encoding="utf-8")
                filled = text
                for k, v in FILL.items():
                    filled = filled.replace(k, v)
                if filled != text:
                    f.write_text(filled, encoding="utf-8")
        (base / "claude" / "projects").mkdir(parents=True)
        (base / "codex" / "sessions").mkdir(parents=True)
        agent = build(project, base)
        result[name] = {"project": project, "claude_dir": base / "claude" / "projects",
                        "codex_dir": base / "codex" / "sessions", "agent": agent}
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    vl = TESTS.parent / "scripts" / "vl.py"
    for name, f in prepare(args.out).items():
        print(f"# {name} ({f['agent']})")
        print(" ".join(shlex.quote(str(x)) for x in ("python3", vl, "start", "--project", f["project"],
                                                      "--claude-dir", f["claude_dir"], "--codex-dir", f["codex_dir"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
