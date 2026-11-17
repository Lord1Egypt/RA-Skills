"""
_path_detector.py — 统一路径定义检测层

所有审计规则中涉及"是否路径定义"的判断，统一调用此模块。
避免 R-12 / R-25 C-20 / R-23 各写一套模式匹配逻辑导致结果不一致。

检测准则：
  - 字面量路径：含 "skills/" 或 ".standardization/" 或平台绝对路径
  - 变量推导路径：赋值含 Path(__file__) / os.path.join / parent 链
  - *_DIR / *_PATH / *_ROOT 赋值

v2.99.0: 新增 _find_shared_path_file() — 自动检测共享路径文件（不限于 _paths.py）
"""

import ast, os, re


# ── 路径特征识别 ──

_PATH_LITERAL_PATTERNS = [
    r'skills/',
    r'\.standardization/',
    r'os\.path\.join\(',
    r'Path\s*\(',
    r'__file__',
    r'\.parent',
]

_BLOCKED_FIX_KEYS = {"workflow_completeness", "example_quality",
                     "capability_boundary", "section_names"}


def has_path_feature(text: str) -> bool:
    """判断文本是否包含路径特征（字面量、os.path.join、Path等）"""
    for pat in _PATH_LITERAL_PATTERNS:
        if pat in text:
            return True
    # 平台绝对路径（Windows / Unix）
    if re.search(r'[A-Za-z]:[\\/]', text) or re.search(r'^/[^/]', text):
        return True
    # 变量名含 _DIR / _PATH / _ROOT
    if re.search(r'\b[A-Z_]+_(?:DIR|PATH|ROOT)\s*=', text):
        return True
    return False


def is_path_definition(line: str) -> bool:
    """判断一行是否为路径定义赋值（模块级）"""
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        return False
    # 赋值模式：VAR = ...
    if '=' not in stripped:
        return False
    # 变量名含 _DIR / _PATH / _ROOT
    if not re.search(r'^[A-Za-z_]+_(?:DIR|PATH|ROOT)\s*=', stripped):
        # 或包含路径字面量特征
        if not has_path_feature(stripped):
            return False
    # 右侧包含路径特征
    val = stripped.split('=', 1)[1].strip()
    return has_path_feature(val) or bool(re.search(r'_[A-Z]+\s*/(?:|/)', val))


def detect_path_type(line: str) -> str:
    """识别路径定义的类型：literal / derived / argv / unknown"""
    stripped = line.strip()
    # sys.argv + 文件操作
    if 'sys.argv[' in stripped and has_path_feature(stripped):
        return 'argv'
    # 硬编码字面量
    if re.search(r'"(?:skills/|\.standardization/|\.workbuddy)', stripped):
        return 'literal'
    if re.search(r"'(?:skills/|\.standardization/|\.workbuddy)", stripped):
        return 'literal'
    # 变量推导（Path / os.path.join / parent 链）
    if re.search(r'Path\s*\(|os\.path\.join|\.parent', stripped):
        return 'derived'
    return 'unknown'


def is_llm_only_fix(fix_key: str) -> bool:
    """判断一个 fix key 是否属于 LLM 手动修复（非 auto-fix）"""
    return fix_key in _BLOCKED_FIX_KEYS or False


def get_standardized_dirs(skill_name: str):
    """返回标准数据目录字典（按 R-11/R-12 规范）"""
    return {
        "STD_ROOT": f"skills/.standardization/",
        "STD_DIR": f"skills/.standardization/{skill_name}/",
        "DATA_DIR": f"skills/.standardization/{skill_name}/data/",
        "OUTPUTS_DIR": f"skills/.standardization/{skill_name}/outputs/",
        "BACKUP_DIR": f"skills/.standardization/{skill_name}/backup/",
        "CACHE_DIR": f"skills/.standardization/{skill_name}/cache/",
        "TEMP_DIR": f"skills/.standardization/{skill_name}/temp/",
    }


def _find_shared_path_file(scripts_dir):
    """
    自动检测共享路径文件（不限于 _paths.py）。
    
    检测逻辑：
    1. 扫描所有 .py 文件（排除 __init__.py）
    2. 记录每个文件被其他脚本 import 的次数（from <basename> import）
    3. 被最多脚本引用的文件 → 共享文件候选
    4. 回溯兼容：如果没找到，检查 _paths.py 是否存在
    
    返回 (filename_or_None, set_of_declared_vars, imported_by_count)
    """
    if not os.path.isdir(scripts_dir):
        return None, set(), 0

    py_files = [f for f in os.listdir(scripts_dir)
                if f.endswith('.py') and f != '__init__.py']
    if not py_files:
        return None, set(), 0

    import_graph = {}
    for f in py_files:
        import_graph[f] = set()

    for candidate in py_files:
        base = candidate[:-3]
        for f in py_files:
            if f == candidate:
                continue
            try:
                with open(os.path.join(scripts_dir, f), 'r', encoding='utf-8', errors='replace') as fh:
                    content = fh.read()
                if re.search(rf'from\s+(?:scripts\.)?{re.escape(base)}\s+import', content):
                    import_graph[candidate].add(f)
            except Exception:
                continue

    sorted_files = sorted(py_files, key=lambda f: len(import_graph[f]), reverse=True)
    best = sorted_files[0]
    best_count = len(import_graph[best])

    if best_count == 0:
        if os.path.isfile(os.path.join(scripts_dir, "_paths.py")):
            best = "_paths.py"
            best_count = 1

    # ★ v2.101.7: 当选中的 shared file 不含路径变量声明时，
    #   优先改选 _paths.py（grid_builder 等业务文件虽然import多，
    #   但不适合作为路径定义来源）
    if best and best != "_paths.py":
        try:
            best_path = os.path.join(scripts_dir, best)
            with open(best_path, 'r', encoding='utf-8') as f:
                best_content = f.read()
            # 只检查变量声明行（=左侧），不检查值引用（=右侧）
            has_path_var = bool(re.search(
                r'^[A-Z_]+(?:DATA|STORAGE|DB|CACHE|CONFIG)[A-Z_]+_(?:DIR|PATH|RAW)\s*=',
                best_content, re.MULTILINE
            ))
            paths_py_path = os.path.join(scripts_dir, "_paths.py")
            if not has_path_var and os.path.isfile(paths_py_path):
                best = "_paths.py"
                best_count = 1
        except Exception:
            pass

    declared_vars = set()
    if best:
        try:
            with open(os.path.join(scripts_dir, best), 'r', encoding='utf-8') as f:
                content = f.read()
            declared_vars = set(re.findall(r'^([A-Z_]+)\s*=', content, re.MULTILINE))
        except Exception:
            pass

    return best, declared_vars, best_count
