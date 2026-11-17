from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lygo-tool")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("out.json"))
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.out.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
