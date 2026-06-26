#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from super_memori_common import validate_relation_target  # noqa: E402


def expect(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def main() -> int:
    ok, _ = validate_relation_target('refines', 'learn:abc123')
    expect(ok, 'learn: signature target should be valid')
    ok, _ = validate_relation_target('extends', 'chunk:deadbeef')
    expect(ok, 'chunk: target should be valid')
    ok, _ = validate_relation_target('confirms', 'path:/home/test/file.md')
    expect(ok, 'path: target should be valid')

    ok, reason = validate_relation_target('refines', 'semantic-spine')
    expect(not ok and 'must start' in reason, 'freeform target should be rejected')
    ok, reason = validate_relation_target('unknown', 'learn:abc')
    expect(not ok and 'non-canonical relation type' in reason, 'unknown relation type should be rejected')

    print('[OK] relation target validation cases passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
