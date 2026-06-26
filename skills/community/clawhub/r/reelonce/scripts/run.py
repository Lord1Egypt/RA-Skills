#!/usr/bin/env python3

try:
    from reelonce.cli.reelonce_skill import main
except ImportError as exc:
    raise SystemExit(
        "无法导入已安装的 ReelOnce Python 包。"
        "请先在仓库根目录执行 `pip install .` 或 `pip install -e \".[dev]\"`。"
    ) from exc


if __name__ == "__main__":
    raise SystemExit(main())
