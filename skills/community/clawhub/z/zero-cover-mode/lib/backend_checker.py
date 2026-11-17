"""零稀泥模式 — 活代码验证后端检查 backend_checker.py

SKILL.md §Phase 2 要求的 4 项活验证：
1. 调用真实 dispatch() 函数
2. 连接真实 Ollama 后端（或检测是否在线）
3. 使用真实的项目数据（从 checkpoints/ 加载）
4. 检测结果基于实际返回值

Usage:
    python backend_checker.py check [--test-file <path>] [--test-cmd <cmd>]
"""

import os, sys, subprocess, json, logging, re, platform

log = logging.getLogger("backend")

# Ollama API 端点
OLLAMA_ENDPOINTS = [
    "http://localhost:11434",
    "http://127.0.0.1:11434",
]
OLLAMA_TIMEOUT = 5  # seconds
OLLAMA_CACHE_TTL = 30  # seconds
_OLLAMA_CACHE = None
_OLLAMA_CACHE_AT = 0.0


# ── 1. 后端在线检测 ──

def check_ollama_online(force_refresh: bool = False) -> dict:
    """检测 Ollama 后端是否在线（P1-G: 并发检查所有端点）"""
    import time
    now = time.time()
    global _OLLAMA_CACHE, _OLLAMA_CACHE_AT
    if not force_refresh and _OLLAMA_CACHE is not None and now - _OLLAMA_CACHE_AT < OLLAMA_CACHE_TTL:
        return _OLLAMA_CACHE

    import urllib.request, urllib.error
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _check_one(ep):
        try:
            req = urllib.request.Request(f"{ep}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    models = [m.get("name", "?") for m in data.get("models", [])]
                    return {"online": True, "endpoint": ep, "models": models}
        except (urllib.error.URLError, urllib.error.HTTPError,
                ConnectionError, TimeoutError, OSError):
            pass
        return None

    result = {"online": False, "endpoint": None, "models": []}
    with ThreadPoolExecutor(max_workers=len(OLLAMA_ENDPOINTS)) as ex:
        futures = {ex.submit(_check_one, ep): ep for ep in OLLAMA_ENDPOINTS}
        for f in as_completed(futures):
            r = f.result()
            if r and r.get("online"):
                result = r
                break

    _OLLAMA_CACHE = result
    _OLLAMA_CACHE_AT = now
    return result


def check_gateway_available() -> dict:
    """检测 gateway.py 是否可导入"""
    try:
        # 尝试从 CWD 上层或标准路径导入
        import importlib, sys
        gateway_paths = [
            os.path.join(os.getcwd(), "gateway.py"),
            os.path.abspath("gateway.py"),
        ]
        for gp in gateway_paths:
            if os.path.exists(gp):
                spec = importlib.util.spec_from_file_location("gateway", gp)
                if spec is None or spec.loader is None:
                    log.warning("gateway.py 存在但无法加载 spec: %s — 文件可能损坏", gp)
                    continue
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                has_dispatch = hasattr(mod, "dispatch")
                return {"available": True, "path": gp, "has_dispatch": has_dispatch}
    except Exception as e:
        log.warning("gateway 加载失败: %s", e)
    return {"available": False, "path": None, "has_dispatch": False}


# ── 2. 测试代码的实效性检查 ──

def check_test_calls_real_backend(test_code: str) -> dict:
    """检查测试代码是否调用真实后端而非 mock

    对纯 Python 库测试（直接 import 模块函数），如果没有任何 mock 且
    测试的是纯逻辑函数，标记为 LIBRARY_TEST 而非 MOCKED（P3-v7.2: AST 导入分析）。
    """
    import ast

    # P1-2: 使用单词边界精确匹配函数名，避免误配 redis_dispatcher()、ollama_endpoint 等
    has_dispatch = bool(re.search(r'\bdispatch\s*\(', test_code))
    has_ollama = bool(re.search(r'\bollama\b', test_code, re.IGNORECASE))
    has_real_call = "requests.post" in test_code or "urllib" in test_code
    has_mock = any(p in test_code for p in [
        "Mock(", "mock.patch", "@patch", "MagicMock",
        "vi.fn", "jest.fn",
    ])

    # AST 分析本地导入（通用方案，不写死模块名）
    STANDARD_LIBS = {"os", "sys", "json", "re", "time", "datetime",
                     "typing", "logging", "collections", "pathlib",
                     "subprocess", "io", "math", "random", "ast",
                     "functools", "itertools", "hashlib", "copy",
                     "dataclasses", "argparse", "textwrap", "string"}
    local_imports = []
    try:
        tree = ast.parse(test_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in STANDARD_LIBS:
                        local_imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top not in STANDARD_LIBS:
                        local_imports.append(node.module)
    except SyntaxError:
        pass

    mock_lines = sum(1 for l in test_code.split("\n") if "mock" in l.lower())
    total_lines = max(1, len([l for l in test_code.split("\n") if l.strip()]))
    mock_ratio = round(mock_lines / total_lines, 2)

    # P0-v11-4: 先检查后端调用存在性，再判断是否为 LIBRARY_TEST
    # 避免有 dispatch/http/Ollama 调用时被纯库测试判定短路掩盖
    has_real_backend_call = has_dispatch or has_ollama or has_real_call
    is_library_test = local_imports and not has_mock and not has_real_backend_call
    if is_library_test:
        log.info("LIBRARY_TEST — 仅导入本地模块，无后端调用")
        return {
            "has_dispatch_call": False,
            "has_ollama_call": False,
            "has_real_http_call": False,
            "has_mock": False,
            "mock_line_ratio": 0,
            "local_imports": local_imports[:5],
            "verdict": "LIBRARY_TEST",
        }

    return {
        "has_dispatch_call": has_dispatch,
        "has_ollama_call": has_ollama,
        "has_real_http_call": has_real_call,
        "has_mock": has_mock,
        "mock_line_ratio": mock_ratio,
        "verdict": "LIVE" if (has_dispatch or has_ollama or has_real_call) and mock_ratio < 0.5 else "MOCKED",
    }


# ── 3. 项目数据加载检查 ──

def check_project_data(workspace_root: str = "") -> dict:
    """检查项目是否有真实的业务数据

    搜索 checkpoints/、data/、tests/fixtures/ 等目录。
    """
    root = workspace_root or os.getcwd()
    data_sources = []

    # 标准数据目录
    for data_dir in ["checkpoints", "data", "tests/fixtures", "fixtures"]:
        dp = os.path.join(root, data_dir)
        if os.path.isdir(dp):
            files = [f for f in os.listdir(dp)
                     if f.endswith((".json", ".yaml", ".yml", ".csv", ".pkl"))]
            if files:
                data_sources.append({"dir": data_dir, "files": files[:10]})

    # 真实项目判断
    # 真实项目判断：检查 workspace 根 + 当前技能目录 + 子目录
    search_roots = [root]
    skill_dir = os.path.join(root, "skills", "zero-cover-mode")
    if os.path.isdir(skill_dir):
        search_roots.append(skill_dir)
        # 也检查技能目录的子目录
        for d in os.listdir(skill_dir):
            dp = os.path.join(skill_dir, d)
            if os.path.isdir(dp):
                search_roots.append(dp)

    has_project_files = any(
        os.path.exists(os.path.join(p, f))
        for p in search_roots
        for f in ["pyproject.toml", "setup.py", "package.json",
                  "pytest.ini", "tox.ini", "__init__.py",
                  "requirements.txt", "SKILL.md"]
    )

    return {
        "has_project_structure": has_project_files,
        "data_directories": data_sources,
        "total_data_files": sum(len(d["files"]) for d in data_sources),
    }


# ── 4. 输出质量验证 ──

def check_test_output(test_output: str, test_cmd: str = "") -> dict:
    """检查测试输出的质量"""
    issues = []
    quality_ok = True

    # 检查是否有错误
    error_patterns = [
        (r"FAILED!", "测试失败"),  # pytest 输出格式: FAILED test.py::test_name or FAIL!
        (r"ERROR:", "执行错误"),
        (r"ModuleNotFoundError", "模块缺失"),
        (r"ImportError", "导入错误"),
        (r"Timeout|timed out", "超时"),
        (r"exit code [1-9]", "非零退出码"),
    ]
    for pat, desc in error_patterns:
        if re.search(pat, test_output, re.IGNORECASE):
            issues.append(desc)
            quality_ok = False

    # 检查是否真的有测试被运行
    if "passed" not in test_output.lower() and "ok" not in test_output.lower():
        if not issues:  # 没有错误也没有通过记录
            issues.append("未检测到测试执行结果")
            quality_ok = False

    return {
        "quality_ok": quality_ok,
        "issues": issues,
        "output_length": len(test_output),
        "has_coverage": "coverage" in test_output.lower(),
    }


# ── 全量检查 ──

def full_check(test_file: str = "", test_cmd: str = "",
               workspace_root: str = "") -> dict:
    """执行 4 项全部检查

    返回类型遵循 BackendCheckResult 契约（dict 兼容）。
    """
    from .contracts import BackendCheckVerdict

    result = {
        "backend_online": check_ollama_online(),
        "gateway_available": check_gateway_available(),
        "test_code_check": {},
        "project_data": check_project_data(workspace_root),
        "test_output_check": {},
        "overall_verdict": BackendCheckVerdict.PASS,
        "blocking_issues": [],
    }

    # 测试代码检查
    test_code = ""
    if test_file and os.path.exists(test_file):
        with open(test_file, "r", encoding="utf-8", errors="replace") as f:
            test_code = f.read()
    if test_code:
        result["test_code_check"] = check_test_calls_real_backend(test_code)
        verdict = result["test_code_check"].get("verdict")
        if verdict == "MOCKED":
            result["blocking_issues"].append("测试代码疑似使用 mock 而非真实后端")
            result["overall_verdict"] = BackendCheckVerdict.WARN
        elif verdict == "LIBRARY_TEST":
            pass  # 纯库级单元测试，无需 dispatch/http

    # 关键检查
    if not result["backend_online"]["online"]:
        # 检测测试是否实际依赖 Ollama
        needs_ollama = False
        if test_code:
            needs_ollama = bool(re.search(
                r'\bollama\b|localhost:11434|api/tags|api/generate',
                test_code, re.IGNORECASE
            ))
        result["blocking_issues"].append("Ollama 后端不可用")
        verdict = result.get("test_code_check", {}).get("verdict")
        if verdict == "LIBRARY_TEST" or not needs_ollama:
            result["blocking_issues"][-1] += "（测试不依赖，降级为 WARN）"
            result["overall_verdict"] = BackendCheckVerdict.WARN
        else:
            result["overall_verdict"] = BackendCheckVerdict.BLOCKING

    verdict = result.get("test_code_check", {}).get("verdict")
    if verdict != "LIBRARY_TEST":
        if (not result["project_data"]["has_project_structure"]
                and not result["project_data"]["data_directories"]):
            result["blocking_issues"].append("未检测到项目结构和业务数据")
            result["overall_verdict"] = BackendCheckVerdict.BLOCKING

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="活代码验证后端检查器")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check", help="全量检查")
    p.add_argument("--test-file", help="测试文件路径")
    p.add_argument("--test-cmd", help="测试命令")
    p.add_argument("--workspace", help="工作区根目录")

    args = parser.parse_args()

    try:
        result = full_check(
            test_file=args.test_file or "",
            test_cmd=args.test_cmd or "",
            workspace_root=args.workspace or "",
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["overall_verdict"] == "BLOCKING":
            sys.exit(1)
    except Exception as e:
        log.error("检查失败: %s", e)
        sys.exit(1)
