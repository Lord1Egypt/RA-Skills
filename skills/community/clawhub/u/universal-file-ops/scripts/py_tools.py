"""py_tools.py - Python code quality tools for universal-file-ops skill.

Provides: normalize, review, oo-ify, gen-test, sandbox-test subcommands.
All output in standardized JSON format with error codes (UFO-XXXX).
"""

import ast
import os
import re
import sys
import json
import subprocess
import tempfile
import venv
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any


# --- Constants ---
ENCODING = "utf-8"
MAX_FORMAL_LINES = 600
INDENT_CHARS = "    "
SHEBANG_SYSTEM_PATHS = ["/usr/local/bin", "/usr/bin"]

# ── Self-referential I/O ──
# 所有文件写入操作必须通过技能自身的 text_crud.py / file_ops.py 或 atomic_write 完成
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from utils import atomic_write


# --- Helpers ---
def _read_file_safe(path: str) -> List[str]:
    """Read file with encoding fallback."""
    for enc in (ENCODING, "gbk", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.readlines()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError("Cannot decode file: {} (not utf-8/GBK/Latin-1)".format(path))


def _detect_script_type(file_path: str, lines: List[str]) -> str:
    """Detect if script is formal tool or temporary script."""
    abs_path = str(Path(file_path).resolve())

    # 1. Path contains skills/ -> formal
    if "/skills/" in abs_path.replace("\\", "/"):
        return "formal"

    # 2. Shebang in system path -> formal
    if lines and lines[0].startswith("#!"):
        shebang = lines[0].strip()
        if any(p in shebang for p in SHEBANG_SYSTEM_PATHS):
            return "formal"

    # 3. Header comment mentions temporary -> temporary
    head = "".join(lines[:20]).lower()
    if "temporary" in head or "temp script" in head or "ad-hoc" in head:
        return "temporary"

    # 4. In temp directory -> temporary
    temp_dirs = ["/tmp/", "/temp/"]
    if any(td in abs_path for td in temp_dirs):
        return "temporary"

    # 5. Default: formal
    return "formal"


def cmd_normalize(args):
    """Normalize Python file (utf-8, indent, trailing whitespace, etc.)."""
    target = args.file
    dry_run = args.dry_run

    try:
        lines = _read_file_safe(target)
    except Exception as e:
        print(json.dumps({"error_code": "UFO-1001", "script": "py_tools.py", "line": 0, "message": str(e), "suggestion": "Check file path and encoding"}))
        return 1

    fixed = 0
    new_lines = []

    for i, line in enumerate(lines):
        original = line

        # Fix 1: Tab indent -> 4 spaces
        if line.startswith("\t"):
            line = line.replace("\t", INDENT_CHARS)
            fixed += 1

        # Fix 2: Trailing whitespace
        if line.endswith(" \n") or line.endswith("\t\n"):
            line = line.rstrip() + "\n"
            fixed += 1

        new_lines.append(line)

    # Fix 3: Ensure final newline
    if new_lines and not new_lines[-1].endswith("\n"):
        new_lines[-1] = new_lines[-1] + "\n"
        fixed += 1

    if dry_run:
        print(json.dumps({"fixed": fixed, "dry_run": True}))
        return 0

    # 用原子写入而非直接 open（符合技能自身 I/O 规范）
    atomic_write(target, new_lines, ENCODING)

    print(json.dumps({"fixed": fixed, "file": target}))
    return 0


def cmd_review(args):
    """Review Python file for common issues."""
    target = args.file
    issues = []

    try:
        lines = _read_file_safe(target)
        content = "".join(lines)
        tree = ast.parse(content)
    except SyntaxError as e:
        issues.append({"line": e.lineno, "type": "syntax", "message": str(e.msg)})
        print(json.dumps({"issues": issues, "error_code": "UFO-2001"}))
        return 1
    except Exception as e:
        issues.append({"line": 0, "type": "error", "message": str(e)})
        print(json.dumps({"issues": issues}))
        return 1

    # Check: functions too long (>50 lines)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            body_lines = node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0
            if body_lines > 50:
                issues.append({"line": node.lineno, "type": "long-func", "name": node.name, "lines": body_lines})

    print(json.dumps({"issues": issues, "status": "ok"}))
    return 0


def cmd_oo_ify(args):
    """Suggest OO refactoring for large Python files."""
    target = args.file

    try:
        lines = _read_file_safe(target)
        content = "".join(lines)
    except Exception as e:
        print(json.dumps({"error_code": "UFO-1001", "message": str(e)}))
        return 1

    total_lines = len(lines)
    script_type = _detect_script_type(target, lines)

    if script_type == "temporary":
        print(json.dumps({"script_type": "temporary", "oo_required": False, "reason": "Temporary scripts are exempt from 600-line OO requirement"}))
        return 0

    if total_lines < MAX_FORMAL_LINES:
        print(json.dumps({"script_type": "formal", "oo_required": False, "reason": "File is under {} lines".format(MAX_FORMAL_LINES)}))
        return 0

    # Suggest OO: group functions by prefix
    funcs = []
    try:
        tree = ast.parse(content)
        funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    except:
        pass

    suggestions = []
    if funcs:
        # Group by prefix (before _)
        groups = {}
        for f in funcs:
            parts = f.split("_", 1)
            prefix = parts[0] if len(parts) > 1 else "misc"
            groups.setdefault(prefix, []).append(f)

        for prefix, members in groups.items():
            if len(members) >= 2:
                suggestions.append({"type": "group-to-class", "class_name": prefix.capitalize(), "methods": members})

    print(json.dumps({"script_type": "formal", "total_lines": total_lines, "oo_required": True, "suggestions": suggestions}))
    return 0


def cmd_gen_test(args):
    """Generate pytest-style test skeleton for a Python file."""
    target = args.file
    output = args.output

    try:
        content = "".join(_read_file_safe(target))
        tree = ast.parse(content)
    except Exception as e:
        print(json.dumps({"error_code": "UFO-1001", "message": str(e)}))
        return 1

    imports = ["import pytest"]
    test_code = ""

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            fn = node.name
            test_fn = "test_" + fn
            test_code += "\ndef {}(mocker):\n".format(test_fn)
            test_code += "    # TODO: setup\n"
            test_code += "    result = {}\n".format(fn)
            test_code += "    assert result is not None\n\n"

        elif isinstance(node, ast.ClassDef):
            cls = node.name
            test_code += "\nclass Test{}:\n".format(cls)
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    test_code += "    def test_{}(self):\n".format(item.name)
                    test_code += "        assert True\n\n"

    full_test = "\n".join(imports) + "\n\n" + test_code

    if output:
        with open(output, "w", encoding=ENCODING) as f:
            f.write(full_test)
        print(json.dumps({"generated": output, "framework": "pytest"}))
    else:
        print(full_test)

    return 0


# --- Sandbox Test ---

def _get_venv_python(venv_dir: str) -> str:
    """Get the python executable path inside a venv (cross-platform)."""
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")


def _get_venv_pip(venv_dir: str) -> str:
    """Get the pip executable path inside a venv (cross-platform)."""
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    return os.path.join(venv_dir, "bin", "pip")


def cmd_sandbox_test(args):
    """Run generated tests in an isolated sandbox virtual environment.

    Creates a temp directory, copies target and test files, builds a venv,
    installs pytest (and optional --require packages), executes tests,
    reports structured results, then cleans up.
    """
    target = os.path.abspath(args.file)
    test_file = os.path.abspath(args.test_file)
    extra_pkgs = args.require or []

    # Validate inputs
    if not os.path.exists(target):
        err = {"error_code": "UFO-1001", "script": "py_tools.py", "line": 0,
               "message": "被测文件不存在: " + target,
               "suggestion": "检查文件路径是否正确"}
        print(json.dumps(err))
        return 1
    if not os.path.exists(test_file):
        err = {"error_code": "UFO-1001", "script": "py_tools.py", "line": 0,
               "message": "测试文件不存在: " + test_file,
               "suggestion": "先运行 gen-test 生成测试文件"}
        print(json.dumps(err))
        return 1

    sandbox_dir = None
    start_ts = time.time()

    try:
        # 1. Create sandbox directory
        sandbox_dir = tempfile.mkdtemp(prefix="ufo_sandbox_")
        target_basename = os.path.basename(target)
        test_basename = os.path.basename(test_file)

        shutil.copy2(target, os.path.join(sandbox_dir, target_basename))
        shutil.copy2(test_file, os.path.join(sandbox_dir, test_basename))

        # Write conftest.py so the target module is importable from the sandbox dir
        conftest_content = (
            "import sys\n"
            "import os\n"
            "_this_dir = os.path.dirname(os.path.abspath(__file__))\n"
            "if _this_dir not in sys.path:\n"
            "    sys.path.insert(0, _this_dir)\n"
        )
        with open(os.path.join(sandbox_dir, "conftest.py"), "w", encoding="utf-8") as f:
            f.write(conftest_content)

        # 2. Build venv
        venv_dir = os.path.join(sandbox_dir, "venv")
        venv.create(venv_dir, with_pip=True, clear=False)

        python_exe = _get_venv_python(venv_dir)
        pip_exe = _get_venv_pip(venv_dir)

        # 3. Install dependencies
        pkgs_to_install = ["pytest"] + extra_pkgs
        pip_result = subprocess.run(
            [pip_exe, "install"] + pkgs_to_install,
            capture_output=True, text=True, timeout=120
        )
        if pip_result.returncode != 0:
            err = {"error_code": "UFO-4001", "script": "py_tools.py", "line": 0,
                   "message": "沙箱中安装依赖失败: " + pip_result.stderr.strip(),
                   "suggestion": "检查网络连接或包名是否正确"}
            print(json.dumps(err))
            return 1

        # 4. Run pytest from the sandbox directory so conftest.py is picked up
        test_path = os.path.join(sandbox_dir, test_basename)
        pytest_result = subprocess.run(
            [python_exe, "-m", "pytest", test_path, "-v", "--tb=short"],
            capture_output=True, text=True, timeout=120,
            cwd=sandbox_dir
        )

        duration = round(time.time() - start_ts, 2)

        # 5. Parse pytest output for counts
        stdout_lower = pytest_result.stdout.lower()
        stderr_lower = pytest_result.stderr.lower()

        # Parse summary line like "3 passed, 1 failed in 0.45s"
        passed = 0
        failed = 0
        errors = 0
        total = 0

        for line in (pytest_result.stdout + pytest_result.stderr).split("\n"):
            line = line.strip()
            # Match pytest summary: "3 passed, 1 failed, 1 error in 0.45s"
            if "passed" in line or "failed" in line or "error" in line:
                import re as _re
                passed_m = _re.search(r"(\d+)\s+passed", line)
                failed_m = _re.search(r"(\d+)\s+failed", line)
                errors_m = _re.search(r"(\d+)\s+error", line)
                if passed_m:
                    passed = int(passed_m.group(1))
                if failed_m:
                    failed = int(failed_m.group(1))
                if errors_m:
                    errors = int(errors_m.group(1))
                total = passed + failed + errors
                if total > 0:
                    break

        # If pytest summary not found, try getting test count from output
        if total == 0:
            test_items = [l for l in pytest_result.stdout.split("\n") if l.strip().startswith("test_")]
            total = len(test_items)
            if pytest_result.returncode == 0:
                passed = total

        status = "passed" if pytest_result.returncode == 0 else "failed"

        result = {
            "status": status,
            "tests_run": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "duration_seconds": duration,
            "stdout_preview": pytest_result.stdout[:500],
            "stderr_preview": pytest_result.stderr[:500] if pytest_result.stderr else ""
        }

        if status == "failed" and total == 0 and not pytest_result.stdout.strip():
            # Possible compilation/import error
            result["status"] = "failed"
            result["error_detail"] = pytest_result.stderr[:500] if pytest_result.stderr else "no output"

        print(json.dumps(result))
        return 0 if status == "passed" else 1

    except subprocess.TimeoutExpired:
        err = {"error_code": "UFO-4001", "script": "py_tools.py", "line": 0,
               "message": "沙箱运行测试超时（120秒）",
               "suggestion": "检查测试是否有死循环或过长等待"}
        print(json.dumps(err))
        return 1
    except Exception as e:
        err = {"error_code": "UFO-9001", "script": "py_tools.py", "line": 0,
               "message": "沙箱执行异常: " + str(e),
               "suggestion": "检查 Python 环境和依赖是否正常"}
        print(json.dumps(err))
        return 1
    finally:
        if sandbox_dir and os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir, ignore_errors=True)


# --- Main ---
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Python Code Quality Tools")
    sub = parser.add_subparsers(dest="command")

    p_norm = sub.add_parser("normalize", help="Normalize Python file")
    p_norm.add_argument("file", help="Target .py file")
    p_norm.add_argument("--dry-run", action="store_true", help="Preview only")
    p_norm.set_defaults(func=cmd_normalize)

    p_review = sub.add_parser("review", help="Review Python file")
    p_review.add_argument("file", help="Target .py file")
    p_review.set_defaults(func=cmd_review)

    p_oo = sub.add_parser("oo-ify", help="Suggest OO refactoring")
    p_oo.add_argument("file", help="Target .py file")
    p_oo.set_defaults(func=cmd_oo_ify)

    p_test = sub.add_parser("gen-test", help="Generate test skeleton")
    p_test.add_argument("file", help="Target .py file")
    p_test.add_argument("-o", "--output", help="Output test file")
    p_test.set_defaults(func=cmd_gen_test)

    p_sbx = sub.add_parser("sandbox-test", help="Run tests in isolated sandbox venv")
    p_sbx.add_argument("--file", required=True, help="Target .py file to test")
    p_sbx.add_argument("--test-file", required=True, help="Generated test .py file")
    p_sbx.add_argument("--require", action="append", default=[], help="Extra pip packages to install in sandbox (repeatable)")
    p_sbx.set_defaults(func=cmd_sandbox_test)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
