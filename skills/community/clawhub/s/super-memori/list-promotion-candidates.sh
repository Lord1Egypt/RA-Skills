#!/usr/bin/env python3
# Exit codes: 0=ok, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'scripts'))
from super_memori_common import list_promotion_candidates


class CandidateParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(4)


def main() -> int:
    p = CandidateParser(description='List local promotion/evolution candidate signals')
    p.add_argument('--limit', type=int, default=10)
    p.add_argument('--json', action='store_true')
    args = p.parse_args()
    payload = {'status': 'ok', 'candidates': list_promotion_candidates(limit=args.limit)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f'list-promotion-candidates internal error: {exc}', file=sys.stderr)
        raise SystemExit(5)
