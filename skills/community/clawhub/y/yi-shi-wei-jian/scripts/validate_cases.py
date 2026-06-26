from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from case_store import CaseStore, CaseValidationError  # noqa: E402


def main() -> int:
    store = CaseStore(REPO_ROOT / "data" / "historical_cases.json", REPO_ROOT / "data" / "user_cases.json")

    try:
        core_cases = store.load_core_cases()
        user_cases = store.load_user_cases()
        all_cases = store.load_all_cases()
    except CaseValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"案例校验通过，基础案例 {len(core_cases)} 条，用户案例 {len(user_cases)} 条，共 {len(all_cases)} 条。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
