"""零稀泥模式 — 假数据检测 fake_data_detector.py

多层级检测策略（L1 静态扫描 / L2 覆盖率 / L3 启发式）。

Usage:
    python fake_data_detector.py l1 <file_path> [lang]
    python fake_data_detector.py full <file_path> [lang]
"""

import re, sys, os, ast, subprocess, json
import logging

# P1-3: 标准库集合，用于自动检测项目模块
_STANDARD_LIBS = {"os", "sys", "json", "re", "time", "datetime",
                 "typing", "logging", "collections", "pathlib",
                 "subprocess", "io", "math", "random", "ast",
                 "functools", "itertools", "hashlib", "copy",
                 "dataclasses", "argparse", "textwrap", "string",
                 "threading", "concurrent", "importlib", "inspect",
                 "unittest", "pytest", "tempfile", "shutil",
                 "platform", "weakref", "abc", "enum", "struct"}

log = logging.getLogger("fake_data")

# L1: 关键词列表（Python）
L1_PATTERNS_PYTHON = [
    r'MagicMock',
    r'mock\.patch',
    r'Mock\(',
    r'fake_data',
    r'@patch',
    r'AsyncMock',
    r'mock_open',
    r'unittest\.mock\.ANY',
    r'FactoryBoy',
    r'Faker\(\)',
    r'MagicMock\(spec',
    r'create_autospec',
    r'PropertyMock',
    r'patch\.object',
    r'patch\.multiple',
    r'\bANY\b',
    r'sentinel',
    r'DEFAULT',
    r'NonCallableMock',
    r'pytest\.mocker',
    r'mocker\.patch',
    r'mocker\.mock',
    r'MagicMock\(return_value',
    r'MagicMock\(side_effect',
    r'MagicMock\(spec_set',
]

# L1: 关键词列表（JS/TS）
L1_PATTERNS_JSTS = [
    r'jest\.fn\(\)',
    r'jest\.mock\(\)',
    r'jest\.spyOn\(',
    r'vi\.fn\(\)',
    r'vi\.mock\(\)',
    r'vi\.spyOn\(',
    r'createMock',
    r'fakeData',
    r'MockClass',
    r'\.mockImplementation',
    r'\.mockReturnValue',
    r'\.mockResolvedValue',
    r'\.mockRejectedValue',

    r'test\.mock\(',
    r'sinon\.stub\(\)',
    r'sinon\.mock\(\)',
    r'sinon\.fake',
    r'createMockInstance',
    r'autoMock',
    r'__mocks__',
    r'td\.function',
    r'td\.when',
    r'td\.verify',
    r'testdouble',
    r'proxyquire',
]

HARDCODED_ASSERT = re.compile(
    r'assert\s+\w+\s*==\s*'
    r'(?:'
    r'[\{\[]'                    # dict/list 字面量
    r'|"[^"]*"'                  # 双引号字符串
    r"|'[^']*'"                  # 单引号字符串
    r'|\d+'                       # 数字
    r'|True|False|None'            # 布尔/None
    r')',
    re.MULTILINE
)


def _has_variable_reference(node):
    """检查 AST 节点中是否包含变量引用或函数调用"""
    if isinstance(node, ast.Call):
        return True
    if isinstance(node, ast.Name) and node.id not in ("True", "False", "None"):
        return True
    if isinstance(node, ast.Attribute):
        return True
    if isinstance(node, ast.Subscript):
        return _has_variable_reference(node.value) or _has_variable_reference(node.slice)
    if isinstance(node, ast.BinOp):
        return _has_variable_reference(node.left) or _has_variable_reference(node.right)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return any(_has_variable_reference(el) for el in node.elts)
    if isinstance(node, ast.Dict):
        return any(_has_variable_reference(k) for k in node.keys if k) or \
               any(_has_variable_reference(v) for v in node.values)
    return False


def l1_detect(source_code, lang="python"):
    """L1 静态扫描：检测假数据关键词（排除注释行和AST文档字符串）

    P0-D: 使用 AST 替代行级状态机追踪文档字符串。
    只跳过函数/类/模块的 ast.Expr(ast.Constant(str)) 文档字符串，
    字符串字面量中的三引号不会影响状态。
    """
    if lang == "python":
        patterns = L1_PATTERNS_PYTHON
    elif lang in ("javascript", "js", "typescript", "ts", "node"):
        patterns = L1_PATTERNS_JSTS
    else:
        patterns = []

    matches = []
    lines = source_code.split("\n")

    # P0-D: 用 AST 构建文档字符串行号集合
    doc_lines = set()
    if lang == "python":
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                # 只处理模块/函数/类第一行作为文档字符串的 ast.Expr
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                    if isinstance(node.value.value, str):
                        start = node.lineno
                        end = getattr(node, 'end_lineno', start)
                        for ln in range(start, end + 1):
                            doc_lines.add(ln)
        except SyntaxError:
            pass  # AST 解析失败时退化为全部扫描（无文档字符串排除）

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 注释行跳过
        if stripped.startswith(("#", "//", "/*")):
            continue
        # P0-D: AST 文档字符串行跳过
        if i in doc_lines:
            continue
        for pat in patterns:
            if re.search(pat, stripped):
                matches.append({"line": i, "pattern": pat, "context": stripped[:80]})
                break

    hard_asserts = []
    for m in HARDCODED_ASSERT.finditer(source_code):
        lineno = source_code[:m.start()].count("\n") + 1
        hard_asserts.append({"line": lineno, "context": m.group()[:60]})

    return {
        "L1_keyword_matches": matches,
        "L1_keyword_count": len(matches),
        "hardcoded_asserts": hard_asserts,
        "hardcoded_assert_count": len(hard_asserts),
        "blocking": False,
    }


def _detect_project_modules(test_path):
    """自动检测测试文件导入的项目模块（P1-3）"""
    modules = []
    try:
        with open(test_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                top = node.module.split(".")[0]
                if top not in _STANDARD_LIBS and top not in modules:
                    modules.append(top)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in _STANDARD_LIBS and top not in modules:
                        modules.append(top)
    except (SyntaxError, Exception):
        pass
    return modules


def _is_cov_available():
    """检测 pytest-cov 是否可用（P6-GLOBAL: 移除缓存，直接检测）。"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--cov", "--version", "--no-header", "-q"],
            capture_output=True, text=True, timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False


def l2_detect(test_path):
    """L2 活代码验证 — 通过 pytest --cov 分析覆盖率"""
    # P2-v2-1: 预检测 pytest-cov 可用性
    if not _is_cov_available():
        return {
            "L2_coverage": None,
            "details": "pytest-cov 不可用，L2 跳过（需安装 pytest-cov）",
            "blocking": False,
        }
    try:
        # P1-3: 自动检测项目模块，传入 --cov=module 限制覆盖率范围
        project_modules = _detect_project_modules(test_path)
        cov_args = []
        for mod in project_modules:
            cov_args.extend(["--cov", mod])
        if not cov_args:
            cov_args = ["--cov", "."]
        cmd = [sys.executable, "-m", "pytest"] + cov_args + [test_path, "--no-header", "-q"]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=30,
        )
        cov_match = re.search(r'(\d+)%', result.stdout + result.stderr)
        coverage_pct = int(cov_match.group(1)) if cov_match else None
        if coverage_pct == 0:
            return {"L2_coverage": 0,
                    "details": "覆盖率为 0% — 测试未调用任何被测代码",
                    "blocking": True}
        elif coverage_pct is not None and coverage_pct < 30:
            return {"L2_coverage": coverage_pct,
                    "details": f"覆盖率 {coverage_pct}% — 可能为假数据测试",
                    "blocking": False}
        elif coverage_pct is not None:
            return {"L2_coverage": coverage_pct,
                    "details": f"覆盖率 {coverage_pct}% — 正常",
                    "blocking": False}
        return {"L2_coverage": None,
                "details": "无法解析覆盖率输出",
                "blocking": False}
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
        log.warning("L2 跳过: %s", e)
        return {"L2_coverage": None, "details": "pytest-cov 不可用, L2 跳过",
                "blocking": False}


def l3_detect(test_path):
    """L3 启发式检测 — AST 分析 assert 中是否含变量引用

    P1-2 修复：只标记 assert 两侧都不是函数/变量引用的场景（字面量 vs 字面量）。
    不再将 assert result == {"a": 1} 误报（result 是变量引用）。
    """
    try:
        with open(test_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"L3_literal_assert_pct": None,
                "details": f"无法解析 AST: {e}",
                "blocking": False}

    total_asserts = 0
    suspicious_asserts = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            total_asserts += 1
            if isinstance(node.test, ast.Compare):
                left_has_ref = _has_variable_reference(node.test.left)
                right_has_ref = any(
                    _has_variable_reference(c) for c in node.test.comparators
                )
                # 只有两边都没有变量引用时才算可疑（纯字面量 assert）
                if not left_has_ref and not right_has_ref:
                    suspicious_asserts += 1

    if total_asserts == 0:
        return {"L3_literal_assert_pct": 0, "total_asserts": 0,
                "details": "无 assert 语句", "blocking": False}

    pct = suspicious_asserts / total_asserts
    return {
        "L3_literal_assert_pct": round(pct, 2),
        "total_asserts": total_asserts,
        "suspicious_count": suspicious_asserts,
        "details": f"{suspicious_asserts}/{total_asserts} 纯字面量 assert",
        "blocking": pct >= 0.8,
    }


def l3_detect_from_code(source_code):
    """基于代码字符串的 L3 检测（P2-v7.2: 避免二次文件读取）"""
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"L3_literal_assert_pct": None,
                "details": f"语法错误: {e}",
                "blocking": False}

    total_asserts = 0
    suspicious_asserts = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            total_asserts += 1
            if isinstance(node.test, ast.Compare):
                left_has_ref = _has_variable_reference(node.test.left)
                right_has_ref = any(
                    _has_variable_reference(c) for c in node.test.comparators
                )
                if not left_has_ref and not right_has_ref:
                    suspicious_asserts += 1

    if total_asserts == 0:
        return {"L3_literal_assert_pct": 0, "total_asserts": 0,
                "details": "无 assert 语句", "blocking": False}

    pct = suspicious_asserts / total_asserts
    return {
        "L3_literal_assert_pct": round(pct, 2),
        "total_asserts": total_asserts,
        "suspicious_count": suspicious_asserts,
        "details": f"{suspicious_asserts}/{total_asserts} 纯字面量 assert",
        "blocking": pct >= 0.8,
    }


def detect(test_path, lang="python", run_l2=True):
    """全量检测 — lang 可自动从测试文件内容推断"""
    with open(test_path, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()
    # 自动推断 lang: 如果文件含 jest/vi/describe/test 关键词 -> node
    if lang == "auto":
        import keyword as _kw
        test_keywords = ["jest.fn", "vi.fn", "vi.mock", "jest.mock", "describe", "it(", "test("]
        if any(k in code for k in test_keywords):
            lang = "node"
        elif "def test_" in code or "class Test" in code:
            lang = "python"

    result = {"path": test_path, "language": lang}
    result["L1"] = l1_detect(code, lang)
    if run_l2:
        result["L2"] = l2_detect(test_path)
    result["L3"] = l3_detect_from_code(code)

    all_asserts = len(re.findall(r'\bassert\b', code))
    hard_asserts = result["L1"]["hardcoded_assert_count"]
    if all_asserts > 0 and hard_asserts / all_asserts >= 0.8:
        result["L1"]["blocking"] = True

    # 返回值通过 Pydantic 契约校验
    from .contracts import FakeDataResult
    try:
        FakeDataResult(**result)
    except Exception as e:
        log.warning("FakeDataResult 契约校验失败: %s", e)

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="假数据检测器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("l1", help="L1 静态扫描")
    p.add_argument("file_path")
    p.add_argument("lang", nargs="?", default="python")

    p = sub.add_parser("full", help="全量检测")
    p.add_argument("file_path")
    p.add_argument("lang", nargs="?", default="python")

    args = parser.parse_args()

    try:
        if args.command == "l1":
            with open(args.file_path, "r", encoding="utf-8",
                      errors="replace") as f:
                code = f.read()
            result = l1_detect(code, args.lang)
            print(f"L1 关键词匹配: {result['L1_keyword_count']}")
            for m in result["L1_keyword_matches"]:
                print(f"  第{m['line']}行: {m['context']}")
            print(f"硬编码断言: {result['hardcoded_assert_count']}")
            for a in result["hardcoded_asserts"]:
                print(f"  第{a['line']}行: {a['context']}")
        elif args.command == "full":
            result = detect(args.file_path, args.lang)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
