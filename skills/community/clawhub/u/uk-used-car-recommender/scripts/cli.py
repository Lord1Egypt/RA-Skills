"""Direct script entrypoint — delegates to the installable CLI."""

from __future__ import annotations

import sys
from pathlib import Path

# 确保项目根目录在 sys.path 中，方便直接 python scripts/cli.py 运行
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gt_car_search.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
