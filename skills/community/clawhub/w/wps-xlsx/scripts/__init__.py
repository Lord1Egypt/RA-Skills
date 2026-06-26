"""
XLSX Skill - Excel 公式重算工具（纯 Python，基于 formulas 库）

使用方式：
    import sys
    sys.path.insert(0, "cooffice/skills/xlsx/scripts")
    from recalc import recalc

    result = recalc("report.xlsx", timeout=60)
    print(result)  # {'status': 'success', 'total_errors': 0, 'total_formulas': 42, ...}
"""

from .recalc import recalc

__all__ = [
    "recalc",
]
