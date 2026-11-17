"""A generated ~100-file Vite + React project for the folder-collapse checks.

    python3 tests/e2e/medium.py --out <folder>"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

COUNTS = {"pages": 12, "components": 30, "lib": 20, "api": 8, "utils": 30}  # 100 files + src/main.tsx


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_medium(root) -> Path:
    root = Path(root)
    _write(root, "index.html", '<!doctype html><div id="root"></div><script type="module" src="/src/main.tsx"></script>\n')
    _write(root, "package.json", '{"dependencies": {"react": "18.3.1", "openai": "4.60.0", "@supabase/supabase-js": "2.45.0"}}\n')
    _write(root, "src/main.tsx", "".join(f'import "./pages/p{i}";\n' for i in range(COUNTS["pages"])))
    for i in range(COUNTS["pages"]):
        _write(root, f"src/pages/p{i}.tsx",
               f'import {{ C{i} }} from "../components/c{i}";\nimport {{ L{i} }} from "../lib/l{i}";\n'
               f"export default function Page{i}() {{\n  return C{i}(L{i}());\n}}\n")
    for i in range(COUNTS["components"]):
        _write(root, f"src/components/c{i}.tsx",
               f'import {{ u{i} }} from "../utils/u{i}";\nexport function C{i}(x) {{\n  return u{i}(x);\n}}\n')
    for i in range(COUNTS["lib"]):
        api = f'import {{ ask{i % COUNTS["api"]} }} from "../api/a{i % COUNTS["api"]}";\n'
        _write(root, f"src/lib/l{i}.ts", f"{api}export function L{i}() {{\n  return ask{i % COUNTS['api']}('q');\n}}\n")
    for i in range(COUNTS["api"]):
        sdk = 'import OpenAI from "openai";\n' if i % 2 == 0 else 'import { createClient } from "@supabase/supabase-js";\n'
        _write(root, f"src/api/a{i}.ts", f"{sdk}\n\nexport async function ask{i}(q) {{\n  return q;\n}}\n")
    for i in range(COUNTS["utils"]):
        _write(root, f"src/utils/u{i}.ts", f"export const u{i} = (x) => x;\n")
    return root


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    print(make_medium(Path(ap.parse_args().out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
