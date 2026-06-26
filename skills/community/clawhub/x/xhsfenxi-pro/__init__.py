"""
xhsfenxi-pro v2.1.1
小红书博主全链路分析 Skill

⭐ v2.1 升级（2026-05-01）：
- formula.py: 添加路线分支（B_HEALING / BA_IRONY / A / C），新增 6 个 B+A 反讽系专属模型
- reverse_engineer.py: 量化数据驱动逆向工程（主题矩阵 / Top10vsBottom10 / 反常识 / 温度 / 内容结构）
- analyzer.py: 新增 analyze_with_reverse_engineering() 一站式入口
- archetypes.json: B+A 温度子分化（治愈系 vs 反讽系）
- build_docx_with_toc.py: docx 默认带目录

🔒 v2.1.1 隐私清理（2026-05-02）：
- 清空 bloggers.json 数据库中的具体博主分析数据
- archetypes.json 的 examples 数组清空
- 全部文档将历史博主名替换为抽象代号（B 治愈系代表 / B+A 反讽系代表 / A 荒诞美学代表 / C 现实策略代表）
- 用户 ID hex 占位符化（USER_ID_HEX_HERE）
- skill 现在是纯方法论 / 公式库，不携带任何分析过的真实博主数据
"""

from .client import XhsClient
from .analyzer import (
    analyze_account,
    analyze_with_reverse_engineering,
    classify_archetype,
    compute_stats,
    build_five_layers,
)
from .formula import (
    generate_formula_report,
    detect_route,
    get_models_for_route,
    B_HEALING_MODELS,
    BA_IRONY_MODELS,
    A_MODELS,
    C_MODELS,
)
from .reverse_engineer import (
    full_reverse_engineering,
    theme_matrix,
    top_vs_bottom,
    detect_findings,
    detect_temperature,
    infer_content_structures,
    format_findings_md,
)
from .archetype_registry import (
    save_blogger,
    get_blogger,
    list_bloggers,
    list_archetypes,
    add_archetype,
    update_archetype_signals,
)
from .utils import check_cookies, get_best_cookies, print_cookie_status

__all__ = [
    # Core
    "XhsClient",
    # Analyzer
    "analyze_account", "analyze_with_reverse_engineering",
    "classify_archetype", "compute_stats", "build_five_layers",
    # Formula (v2.1 路线分支)
    "generate_formula_report", "detect_route", "get_models_for_route",
    "B_HEALING_MODELS", "BA_IRONY_MODELS", "A_MODELS", "C_MODELS",
    # Reverse engineering (v2.1 新增)
    "full_reverse_engineering", "theme_matrix", "top_vs_bottom",
    "detect_findings", "detect_temperature", "infer_content_structures",
    "format_findings_md",
    # Registry
    "save_blogger", "get_blogger", "list_bloggers",
    "list_archetypes", "add_archetype", "update_archetype_signals",
    # Utils
    "check_cookies", "get_best_cookies", "print_cookie_status",
]
__version__ = "2.1.4"
