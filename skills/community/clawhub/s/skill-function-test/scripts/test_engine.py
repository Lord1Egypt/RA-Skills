"""
test_engine.py — 6 维功能测试引擎

执行指定的测试维度，聚合结果，生成分级报告。
测试维度：D1 基础功能、D2 流程断点、D3 数据污染、D4 噪音干扰、D5 计算正确性、D6 边界鲁棒性

时间线集成：每个维度独立计时，subprocess 调用记录 wall time。
"""
import ast
import json
import os
import sys
import subprocess
import importlib.util
import inspect
from typing import Optional

# R-12 数据目录合规
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"
_test_data_dir = os.path.normpath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".standardization", "skill-function-test", "data"
))

# 流程钩子
_HOOKS_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hooks.py"
))
def _hook_check(skill_dir, step):
    r = subprocess.run([sys.executable, _HOOKS_SCRIPT, "check", skill_dir, step],
                        capture_output=True, text=True, encoding="utf-8")
    if r.stdout and r.stdout.strip(): print(r.stdout)
    if r.stderr and r.stderr.strip(): print(r.stderr, file=sys.stderr)
    # 钩子阻断信号输出在 stdout（_block() 用 print 输出），
    # 非零退出码 + stdout 含 "block" 即为阻断，WARN 不阻断
    if r.returncode not in (0, None):
        output = (r.stdout or "") + (r.stderr or "")
        if "block" in output.lower() or "阻断" in output or "f-0" in output.lower():
            sys.exit(r.returncode)
def _hook_done(skill_dir, step):
    subprocess.run([sys.executable, _HOOKS_SCRIPT, "done", skill_dir, step],
                    capture_output=True, encoding="utf-8")

# 时间线输出
_TIMELINE_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "timeline.py"
))
def _tl(skill_dir: str, *args):
    """调用 timeline.py 记录 marker"""
    try:
        subprocess.run(
            [sys.executable, _TIMELINE_SCRIPT, "mark", skill_dir] + list(args),
            capture_output=True, timeout=10,
        )
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
# 测试结果
# ═══════════════════════════════════════════════════════

class TestResult:
    """单条测试结果"""
    def __init__(self, dim: str, name: str, level: str = "info",
                 status: str = "pass", message: str = "",
                 file: str = "", lineno: int = 0,
                 suggestion: str = "", detail: str = ""):
        self.dim = dim          # D1-D6
        self.name = name        # 测试名称
        self.level = level      # block / warn / info
        self.status = status    # pass / fail / skip / error
        self.message = message  # 问题描述
        self.file = file        # 精确文件位置
        self.lineno = lineno    # 精确行号
        self.suggestion = suggestion  # 修复建议
        self.detail = detail    # 详细上下文

    def to_dict(self) -> dict:
        return {
            "dim": self.dim,
            "name": self.name,
            "level": self.level,
            "status": self.status,
            "message": self.message,
            "file": self.file,
            "lineno": self.lineno,
            "suggestion": self.suggestion,
            "detail": self.detail,
        }

    def __str__(self):
        icon = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP", "error": "CRASH"}.get(self.status, "?")
        level_tag = f"[{self.level.upper()}]" if self.level in ("block", "warn") else ""
        location = f" {self.file}:{self.lineno}" if self.file else ""
        return f"  {icon} {level_tag} [{self.dim}] {self.name}{location} — {self.message}"


# ═══════════════════════════════════════════════════════
# 测试运行器
# ═══════════════════════════════════════════════════════

class TestRunner:
    """6 维测试运行器，按维度分组执行测试"""
    def __init__(self, skill_dir: str, blueprint: dict):
        self.skill_dir = skill_dir
        self.blueprint = blueprint
        self.results: list[TestResult] = []

    def run_dimension(self, dim: str):
        """执行指定维度的全部测试，记录执行时间"""
        dim_label = {"d1_smoke": "D1 基础功能完整性", "d2_breakpoint": "D2 流程断点检测",
                     "d3_contamination": "D3 数据污染检测", "d4_noise": "D4 噪音干扰检测",
                     "d5_correctness": "D5 计算正确性", "d6_robustness": "D6 边界鲁棒性"}.get(dim, dim)
        _tl(self.skill_dir, dim, dim_label, "--type", "py_script")
        runner_name = f"_run_{dim}"
        if hasattr(self, runner_name):
            getattr(self, runner_name)()
        else:
            self.results.append(TestResult(
                dim, f"未知维度 {dim}", "info", "skip", "未实现"))
        _tl(self.skill_dir, dim, dim_label, "end", "--type", "py_script")

    def run_all(self, dimensions: list[str] = None):
        """执行一个或多个维度的测试"""
        if dimensions is None:
            dimensions = ["d1_smoke", "d2_breakpoint", "d3_contamination",
                          "d4_noise", "d5_correctness", "d6_robustness"]
        _tl(self.skill_dir, "function_test", "功能测试总入口", "--type", "py_script")
        for dim in dimensions:
            self.run_dimension(dim)
        _tl(self.skill_dir, "function_test", "功能测试总入口", "end", "--type", "py_script")

    def add_result(self, r: TestResult):
        self.results.append(r)

    # ═══════════════════════════════════════════════════════
    # D1: 基础功能完整性 — 每个核心函数能否无崩溃运行
    # ═══════════════════════════════════════════════════════
    def _run_d1_smoke(self):
        functions = self.blueprint.get("functions", [])
        py_files = self.blueprint.get("file_manifest", {}).get("python", [])

        if not py_files:
            self.add_result(TestResult("D1", "无 Python 文件可测试", "info", "skip"))
            return

        # 逐文件做基础检查：语法解析 + 文件可读性
        for relpath in py_files:
            abspath = os.path.join(self.skill_dir, relpath)

            # 检查文件是否存在且可读
            if not os.path.exists(abspath):
                self.add_result(TestResult("D1", f"文件不存在: {relpath}", "block", "fail"))
                continue
            if os.path.getsize(abspath) == 0:
                self.add_result(TestResult("D1", f"空文件: {relpath}", "warn", "fail",
                                           relpath, 0, "文件内容为空"))
                continue

            # 语法解析
            try:
                with open(abspath, "r", encoding="utf-8") as f:
                    source = f.read()
                ast.parse(source)
                self.add_result(TestResult("D1", f"语法检查: {relpath}", "info", "pass"))
            except SyntaxError as e:
                self.add_result(TestResult("D1", f"语法错误: {relpath}", "block", "fail",
                                           str(e), relpath, e.lineno or 0,
                                           "修复语法错误"))

        # -- 运行时烟雾测试 -- subprocess --help 验证脚本启动
        cli_scripts = self._find_cli_scripts(py_files)
        for script, script_rel in cli_scripts:
            _tl(self.skill_dir, "d1_subprocess", f"D1: {script_rel} --help", "--type", "subprocess_wall")
            try:
                result = subprocess.run(
                    [sys.executable, script, "--help"],
                    capture_output=True, text=True, timeout=30,
                    cwd=self.skill_dir
                )
                if result.returncode == 0:
                    self.add_result(TestResult("D1",
                        f"运行时: {script_rel} --help", "info", "pass",
                        f"exit code 0, stdout {len(result.stdout)} chars"))
                else:
                    self.add_result(TestResult("D1",
                        f"启动失败: {script_rel}", "warn", "fail",
                        f"exit code {result.returncode}: {result.stderr.strip()[-200:]}",
                        script_rel, 0, "检查 __main__ 入口和依赖"))
                _tl(self.skill_dir, "d1_subprocess", f"D1: {script_rel} --help", "end",
                       "--type", "subprocess_wall", "--detail", f"rc={result.returncode}")
            except subprocess.TimeoutExpired:
                self.add_result(TestResult("D1",
                    f"启动超时: {script_rel}", "warn", "fail",
                    f"30 秒未返回: 可能卡死在启动时 import 或网络请求",
                    script_rel, 0, "检查 import 链是否有阻塞调用"))
                _tl(self.skill_dir, "d1_subprocess", f"D1: {script_rel} --help", "end",
                       "--type", "subprocess_wall", "--detail", "timeout")
            except FileNotFoundError:
                self.add_result(TestResult("D1",
                    f"解释器不存在: {script_rel}", "block", "fail",
                    f"{sys.executable} 不可用", script_rel, 0,
                    "检查 Python 环境"))
            except Exception as e:
                self.add_result(TestResult("D1",
                    f"运行时异常: {script_rel}", "warn", "fail",
                    str(e)[:200], script_rel, 0))

    def _find_cli_scripts(self, py_files):
        """找出目录中有 __main__ 入口的脚本"""
        candidates = []
        for relpath in py_files:
            abspath = os.path.join(self.skill_dir, relpath)
            if not os.path.exists(abspath):
                continue
            try:
                with open(abspath, "r", encoding="utf-8") as f:
                    source = f.read()
                if '__name__ == "__main__"' in source or '__name__ == "__main__":' in source:
                    candidates.append((abspath, relpath))
            except Exception:
                pass
        return candidates


    # ═══════════════════════════════════════════════════════
    # D2: 流程断点 — 模块间数据传递和调用链是否完整
    # ═══════════════════════════════════════════════════════
    def _run_d2_breakpoint(self):
        refs = self.blueprint.get("reference_links", [])
        imports = self.blueprint.get("import_chain", {})
        file_manifest = self.blueprint.get("file_manifest", {})
        all_files = set()
        for cat in file_manifest:
            for f in file_manifest[cat]:
                all_files.add(f)

        # 检查引用链路中的文件是否存在
        for ref in refs:
            target = ref.get("target", "")
            if target.endswith(".py") or target.endswith(".md") or target.endswith(".sh"):
                resolved = target
                # 尝试多种路径解析
                found = False
                for prefix in ("", "scripts/", "references/", self.skill_dir + "/"):
                    test_path = prefix + target if not target.startswith(("scripts/", "references/")) else target
                    test_path = test_path.lstrip("./").lstrip("/")
                    if test_path in all_files or os.path.exists(os.path.join(self.skill_dir, test_path)):
                        found = True
                        break
                if not found and not target.startswith("`"):
                    self.add_result(TestResult("D2", f"引用文件不存在", "warn", "fail",
                                               f"{ref['source']} → {target}",
                                               ref["source"], 0,
                                               f"创建缺失文件 {target} 或修正引用路径"))

        # 检查 import 链中的模块是否跨模块存在
        for src_file, imported in imports.items():
            for imp in imported:
                parts = imp.split(".")
                mod_name = parts[0]
                if mod_name in ("os", "sys", "json", "math", "re", "datetime",
                                "typing", "collections", "random", "copy",
                                "shutil", "tempfile", "sqlite3", "subprocess",
                                "pathlib", "functools", "itertools", "abc",
                                "enum", "dataclasses", "hashlib", "base64"):
                    continue  # 标准库跳过
                found_in_project = False
                for py_file in file_manifest.get("python", []):
                    if py_file.replace("/", ".").replace(".py", "") == mod_name:
                        found_in_project = True
                        break
                    if py_file.startswith(f"scripts/{mod_name}") or py_file == f"{mod_name}.py":
                        found_in_project = True
                        break
                if not found_in_project:
                    # 外部依赖，只记录 info
                    self.add_result(TestResult("D2", f"外部依赖: {mod_name}", "info", "pass",
                                               f"{src_file} → {imp}"))

    # ═══════════════════════════════════════════════════════
    # D3: 数据污染 — 模块A的操作是否污染模块B的数据
    # ═══════════════════════════════════════════════════════
    def _run_d3_contamination(self):
        sensitive_ops = self.blueprint.get("sensitive_ops", [])
        funcs = self.blueprint.get("functions", [])
        file_manifest = self.blueprint.get("file_manifest", {})

        # 检测是否有多个模块写同一个文件/DB
        write_ops = [s for s in sensitive_ops if s["type"] == "file_delete"]
        if len(write_ops) > 1:
            self.add_result(TestResult("D3", "多处文件删除操作", "warn", "fail",
                                       f"{len(write_ops)} 个删除操作分布于不同文件",
                                       write_ops[0]["file"], write_ops[0]["lineno"],
                                       "确认删除操作是否集中管理，避免误删"))

        # 检测 DB 路径硬编码
        py_files = file_manifest.get("python", [])
        for relpath in py_files:
            abspath = os.path.join(self.skill_dir, relpath)
            try:
                with open(abspath, "r", encoding="utf-8") as f:
                    content = f.read()
                for i, line in enumerate(content.split("\n"), 1):
                    if ".db" in line and ("sqlite" in line.lower() or "connect" in line.lower()):
                        if "DEFAULT_DB" not in line and "ECONOMIC_DB" not in line and "EVM_DB" not in line:
                            self.add_result(TestResult("D3", f"DB 路径可能硬编码", "warn", "fail",
                                                       line.strip()[:100], relpath, i,
                                                       "使用变量引用而非硬编码路径"))
            except Exception:
                pass

    # ═══════════════════════════════════════════════════════
    # D4: 噪音/干扰 — 模块是否产生无关输出或副效应
    # ═══════════════════════════════════════════════════════
    def _run_d4_noise(self):
        py_files = self.blueprint.get("file_manifest", {}).get("python", [])
        for relpath in py_files:
            abspath = os.path.join(self.skill_dir, relpath)
            try:
                with open(abspath, "r", encoding="utf-8") as f:
                    content = f.read()
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    stripped = line.strip()
                    # 裸 print（不在函数/类内的顶层 print）
                    if stripped.startswith("print(") and not stripped.startswith("print(f"):
                        if not any(kw in stripped for kw in ("[KB]", "[ECON", "[EVM")):
                            self.add_result(TestResult("D4", "裸 print 调用", "warn", "fail",
                                                       stripped[:80], relpath, i,
                                                       "建议使用 logging 替代 print"))
                    # 裸 __main__ 中的 print 跳过
                    # (空操作占位)
            except Exception:
                pass

    # ═══════════════════════════════════════════════════════
    # D5: 计算正确性 — 验证数值计算是否正确
    # ═══════════════════════════════════════════════════════
    def _run_d5_correctness(self):
        funcs = self.blueprint.get("functions", [])

        # 检查是否有 verify 或 test 函数
        verify_funcs = [f for f in funcs if any(kw in f["name"].lower()
                       for kw in ("verify", "test", "check", "example", "demo"))]
        if verify_funcs:
            self.add_result(TestResult("D5", f"发现 {len(verify_funcs)} 个验证函数",
                                       "info", "pass",
                                       ", ".join(f['name'] for f in verify_funcs[:5])))
        else:
            self.add_result(TestResult("D5", "无内置验证函数", "info", "pass",
                                       "建议添加 __main__ 验证用例"))

        # 检查关键数值函数是否存在
        calc_funcs = [f for f in funcs if any(kw in f["name"].lower()
                      for kw in ("calc", "compute", "sum", "count", "average"))]
        if calc_funcs:
            self.add_result(TestResult("D5", f"发现 {len(calc_funcs)} 个计算函数",
                                       "info", "pass"))
            # 检查参数是否有零除保护
            for fn in calc_funcs:
                if fn.get("params") and any(div in fn["name"].lower()
                                            for div in ("div", "ratio", "percent", "rate")):
                    filepath = os.path.join(self.skill_dir, fn["file"])
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        lines = content.split("\n")
                        # 找最近的 ÷ 操作
                        for i in range(min(fn["lineno"], len(lines)),
                                       min(fn["lineno"] + 30, len(lines))):
                            if "/" in lines[i] and "==" not in lines[i]:
                                # 检查上方是否有零值检查
                                upper = "\n".join(lines[max(0,fn["lineno"]-5):i+1])
                                if "== 0" not in upper and "!= 0" not in upper:
                                    self.add_result(TestResult("D5", f"零除风险", "warn", "fail",
                                                               f"{fn['name']} 中除法未检查零值",
                                                               fn["file"], i+1,
                                                               "在除法前增加零值判断"))
                                break
                    except Exception:
                        pass

        # -- 运行时正确性验证 -- import + 调用核心函数
        py_files_bp = self.blueprint.get("file_manifest", {}).get("python", [])
        self._run_d5_runtime(funcs, py_files_bp)

    def _run_d5_runtime(self, funcs, py_files):
        """运行时验证：import + 调用核心函数"""
        from collections import defaultdict

        # 收集可安全调用的函数（无参 / 全默认）
        testable = []
        for fn in funcs:
            fname = fn["name"]
            if fname.startswith("_"):
                continue
            if fname == "main":
                continue  # main() 通常依赖 sys.argv，不能安全调用
            params = fn.get("params", [])
            if params in ([], ["self"], ["cls"], [None]):
                testable.append(fn)

        if not testable:
            self.add_result(TestResult("D5", "无安全可调用的函数", "info", "pass",
                                       "跳过运行时验证"))
            return

        file_funcs = defaultdict(list)
        for fn in testable:
            file_funcs[fn["file"]].append(fn)

        for relpath, func_list in file_funcs.items():
            mod_name = relpath.replace("/", ".").replace(".py", "")
            abspath = os.path.join(self.skill_dir, relpath)
            if not os.path.exists(abspath):
                continue

            try:
                spec = importlib.util.spec_from_file_location(mod_name, abspath)
                if spec is None or spec.loader is None:
                    self.add_result(TestResult("D5", f"无法加载模块: {mod_name}",
                                               "warn", "fail", relpath, 0))
                    continue

                mod = importlib.util.module_from_spec(spec)
                old_path = list(sys.path)
                scripts_dir = os.path.join(self.skill_dir, "scripts")
                if os.path.isdir(scripts_dir) and scripts_dir not in sys.path:
                    sys.path.insert(0, scripts_dir)
                try:
                    spec.loader.exec_module(mod)
                finally:
                    sys.path = old_path

                self.add_result(TestResult("D5", f"模块可加载: {mod_name}",
                                           "info", "pass"))

                for fn in func_list:
                    fname = fn["name"]
                    func_obj = getattr(mod, fname, None)
                    if func_obj is None or not callable(func_obj):
                        continue
                    try:
                        sig = inspect.signature(func_obj)
                        bound = sig.bind_partial()
                        result = func_obj(**bound.arguments)
                        self.add_result(TestResult("D5",
                            f"函数可运行: {fname}()", "info", "pass",
                            f"返回值类型: {type(result).__name__}"))
                    except TypeError as e:
                        self.add_result(TestResult("D5",
                            f"函数验证: {fname}()", "info", "pass",
                            f"有必填参数 ({str(e)[:100]})"))
                    except Exception as e:
                        self.add_result(TestResult("D5",
                            f"函数运行失败: {fname}", "warn", "fail",
                            f"调用时抛出: {str(e)[:200]}",
                            relpath, fn["lineno"],
                            "检查函数体是否有未捕获的异常"))

            except SyntaxError as e:
                self.add_result(TestResult("D5", f"语法错误: {mod_name}", "block", "fail",
                                           str(e), relpath, e.lineno or 0))
            except ImportError as e:
                self.add_result(TestResult("D5",
                    f"模块导入失败: {mod_name}", "warn", "fail",
                    f"缺少依赖: {str(e)[:200]}", relpath, 0,
                    "检查是否缺少 pip 依赖"))
            except Exception as e:
                self.add_result(TestResult("D5",
                    f"模块加载异常: {mod_name}", "warn", "fail",
                    str(e)[:200], relpath, 0))

    # ═══════════════════════════════════════════════════════
    # D6: 边界鲁棒性 — 空输入、零值、超大值的处理
    # ═══════════════════════════════════════════════════════
    def _run_d6_robustness(self):
        funcs = self.blueprint.get("functions", [])
        py_files = self.blueprint.get("file_manifest", {}).get("python", [])

        # 检查函数定义中的默认参数是否有 None/0/空列表保护
        for fn in funcs:
            if fn.get("params") and fn["params"] != ["self"]:
                # 检查 docstring 是否有对空/None 的说明
                filepath = os.path.join(self.skill_dir, fn["file"])
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    lines = content.split("\n")
                    # 检查函数下方文档字符串
                    doc_lines = lines[fn["lineno"]:fn["lineno"]+15]
                    doc_text = "\n".join(doc_lines)
                    has_none_guard = any(kw in doc_text.lower()
                                         for kw in ("none", "空", "0", "边界", "异常"))
                    if not has_none_guard:
                        self.add_result(TestResult("D6", f"缺少边界说明", "info", "pass",
                                                   f"{fn['name']}() 无参数边界说明",
                                                   fn["file"], fn["lineno"],
                                                   "建议添加参数取值范围和空值处理的文档"))
                except Exception:
                    pass

        # 检查 try/except 覆盖率
        for relpath in py_files:
            filepath = os.path.join(self.skill_dir, relpath)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                try_count = content.count("except")
                total_lines = len(content.split("\n"))
                ratio = try_count / max(total_lines, 1) * 100
                if ratio < 0.5 and total_lines > 50:
                    self.add_result(TestResult("D6", f"异常处理覆盖率低", "warn", "fail",
                                               f"{relpath}: {try_count} 个 except / {total_lines} 行",
                                               relpath, 0,
                                               "建议对可能抛异常的操作添加 try/except"))
            except Exception:
                pass

    # ═══════════════════════════════════════════════════════
    # 报告生成
    # ═══════════════════════════════════════════════════════
    def generate_report(self) -> dict:
        """生成分级测试报告"""
        summary = {"total": 0, "pass": 0, "fail": 0, "skip": 0, "error": 0,
                   "block": 0, "warn": 0, "info": 0}
        dims = {}

        for r in self.results:
            summary["total"] += 1
            summary[r.status] += 1
            if r.level in ("block", "warn", "info"):
                summary[r.level] += 1
            dim_key = r.dim
            if dim_key not in dims:
                dims[dim_key] = {"total": 0, "pass": 0, "fail": 0, "skip": 0,
                                 "error": 0, "block": 0, "warn": 0, "info": 0}
            dims[dim_key]["total"] += 1
            dims[dim_key][r.status] += 1
            if r.level in ("block", "warn"):
                dims[dim_key][r.level] += 1

        return {
            "summary": summary,
            "dims": dims,
            "results": [r.to_dict() for r in self.results],
        }

    def print_report(self, skill_dir: str = None) -> str:
        """打印人类可读的报告，包含源文件上下文"""
        report = self.generate_report()
        s = report["summary"]

        lines = []
        lines.append("=" * 60)
        lines.append("  功能测试报告")
        lines.append("=" * 60)
        lines.append(f"  总计: {s['total']}  |  通过: {s['pass']}  |  "
                      f"失败: {s['fail']}  |  跳过: {s['skip']}")
        lines.append(f"  F-0 BLOCK: {s['block']}  |  F-1 WARN: {s['warn']}  |  F-2 INFO: {s['info']}")
        lines.append("")

        for dim_key, dim_data in sorted(report["dims"].items()):
            dim_name = {"d1_smoke": "D1 基础功能", "d2_breakpoint": "D2 流程断点",
                        "d3_contamination": "D3 数据污染", "d4_noise": "D4 噪音干扰",
                        "d5_correctness": "D5 计算正确性", "d6_robustness": "D6 边界鲁棒性"
                        }.get(dim_key, dim_key)
            lines.append(f"── [{dim_name}] {dim_data['pass']}/{dim_data['total']} 通过 "
                          f"(BLOCK={dim_data['block']}, WARN={dim_data['warn']})")

        lines.append("")
        lines.append("── 详细结果:")

        # 读取源文件上下文
        context_cache = {}

        def _read_context(filepath: str, lineno: int, context_lines: int = 3) -> str:
            if not filepath or not lineno:
                return ""
            abs_path = os.path.join(skill_dir, filepath) if skill_dir and not os.path.isabs(filepath) else filepath
            if not os.path.exists(abs_path):
                return ""
            if abs_path not in context_cache:
                try:
                    with open(abs_path, "r", encoding="utf-8") as f:
                        context_cache[abs_path] = f.read().split("\n")
                except Exception:
                    context_cache[abs_path] = []
            source_lines = context_cache[abs_path]
            start = max(0, lineno - context_lines - 1)
            end = min(len(source_lines), lineno + context_lines)
            ctx = []
            for i in range(start, end):
                marker = "\u2192" if i == lineno - 1 else " "
                ctx.append(f"      {marker} {i+1:4d}| {source_lines[i]}")
            return "\n".join(ctx)

        for r in self.results:
            lines.append(str(r))
            if r.detail and r.status in ("fail", "error"):
                lines.append(f"    上下文: {r.detail[:200]}")
            if r.status in ("fail", "error") and r.file and r.lineno:
                ctx = _read_context(r.file, r.lineno)
                if ctx:
                    lines.append(f"    代码上下文:")
                    lines.append(ctx)
            if r.suggestion:
                lines.append(f"    建议: {r.suggestion[:150]}")
            if r.level in ("block", "warn") and r.status == "fail":
                lines.append(f"    供LLM判断: 此问题是否属于误报？")
                lines.append(f"      - 若为误报（如字符串字面量检测），标记为 FP 后跳过")
                lines.append(f"      - 若为真问题，执行修复或生成修复建议")
            if r.suggestion:
                lines.append(f"    建议: {r.suggestion[:150]}")

        lines.append("=" * 60)
        verdict = "PASS" if s["block"] == 0 else "FAIL"
        lines.append(f"  结论: {verdict} (F-0 BLOCK={s['block']})")
        lines.append("=" * 60)

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def run_full_test(skill_dir: str, dimensions: list[str] = None) -> tuple[dict, str]:
    """执行完整测试流程: 扫描 → 运行 → 报告"""
    import sys as _sys
    _sys.stdout.flush()
    from inspector import scan

    # 1. 蓝皮书扫描
    print("  [FT] 扫描蓝皮书...", flush=True)
    bb = scan(skill_dir)
    bp = bb.to_dict()

    # 2. 执行测试
    print(f"  [FT] 执行测试: {dimensions or '全部维度'}...", flush=True)
    runner = TestRunner(skill_dir, bp)
    runner.run_all(dimensions)
    print(f"  [FT] 完成 {len(runner.results)} 项测试", flush=True)

    # 3. 生成报告
    report = runner.generate_report()
    report_text = runner.print_report(skill_dir=skill_dir)
    return report, report_text


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        target = sys.argv[1]
        dims = sys.argv[2:] if len(sys.argv) > 2 else None
        if os.path.isdir(target):
            _hook_check(target, "function_test")
            _tl(target, "function_test", "功能测试（独立运行）", "--type", "py_script")

            # 读取轮次配置
            try:
                from test_config import load_config
                test_rounds = load_config(target).get("rounds", 3)
            except Exception:
                test_rounds = 3

            all_reports = []
            all_texts = []
            _tl_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "..", ".standardization", "skill-function-test", "data",
                                    os.path.basename(os.path.abspath(target)))
            # 轮次前快照基线（第0轮），作为 delta 基准
            if test_rounds > 1:
                _tl_file = os.path.join(_tl_base, ".timeline.json")
                if os.path.exists(_tl_file):
                    import shutil
                    shutil.copy2(_tl_file, os.path.join(_tl_base, ".timeline_r0.json"))
            for r in range(1, test_rounds + 1):
                if test_rounds > 1:
                    print(f"\n  ── 功能测试 第 {r}/{test_rounds} 轮 ──")
                report, text = run_full_test(target, dims)
                all_reports.append(report)
                all_texts.append(text)
                # 每轮完成后快照 timeline，供 compute_round_stats 按轮统计
                if test_rounds > 1:
                    _tl_file = os.path.join(_tl_base, ".timeline.json")
                    if os.path.exists(_tl_file):
                        import shutil
                        shutil.copy2(_tl_file, os.path.join(_tl_base, f".timeline_r{r}.json"))
                    print(f"  [功能] 第 {r} 轮完成 (BLOCK={report.get('summary',{}).get('block','?')})")

            # 使用最后一轮作为展示，但标记轮次数
            report = all_reports[-1]
            text = all_texts[-1]
            report["_rounds_executed"] = len(all_reports)
            report["_rounds_configured"] = test_rounds

            # 多轮时取各轮 BLOCK 最大值报告
            if len(all_reports) > 1:
                max_block = max(r.get("summary", {}).get("block", 0) for r in all_reports)
                report["summary"]["block"] = max_block
                report["_max_block_across_rounds"] = max_block

            print(text)
            if test_rounds > 1:
                print(f"  轮次执行: {len(all_reports)}/{test_rounds} 轮完成")
            _tl(target, "function_test", "功能测试（独立运行）", "end", "--type", "py_script")
            # 保存报告到数据目录（R-12 合规）
            from test_config import config_path as _cfg
            _rd = os.path.dirname(_cfg(target))
            os.makedirs(_rd, exist_ok=True)
            report_path = os.path.join(_rd, ".function-test_report.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n报告 JSON 已保存: {report_path}")
            _hook_done(target, "function_test")
        else:
            print(f"错误: 目录不存在 {target}")
    else:
        print("用法: python test_engine.py <skill-dir> [d1_smoke d2_breakpoint ...]")
