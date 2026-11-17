"""零稀泥模式 — 测试执行器 test_runner.py

Security: v1.0.1 — fix shell=True command injection.
Use shlex.split() + list-based subprocess to avoid shell metacharacter parsing.
"""

import os, shlex, subprocess, logging
from .config import SUB_PROCESS_TIMEOUT
from .contracts import TestResultContract

log = logging.getLogger("test_runner")


def parse_test_summary(output: str) -> dict:
    """解析测试输出，返回 {pass, fail, total}"""
    import re
    fails = 0
    passes = 0
    m = re.search(r"(\d+)\s+failed", output, re.IGNORECASE)
    if m:
        fails = max(fails, int(m.group(1)))
    m = re.search(r"(\d+)\s+passed", output, re.IGNORECASE)
    if m:
        passes = max(passes, int(m.group(1)))
    if fails == 0 and "FAILED" in output:
        fails = max(fails, len(re.findall(r"\bFAILED[\s!]", output)))
    if "Ran" in output and passes == 0 and fails == 0:
        m = re.search(r"Ran\s+(\d+)\s+tests", output)
        total = int(m.group(1)) if m else 0
        m = re.search(r"FAILED\s*\(.*failures=(\d+)", output)
        if m:
            fails = max(fails, int(m.group(1)))
        elif "OK" in output:
            passes = max(passes, total)
    return {"pass": passes, "fail": fails, "total": passes + fails}


class TestResult(TestResultContract):
    """测试结果 — 继承 Pydantic TestResultContract，保留兼容接口

    属性:
        cmd, returncode, stdout, stderr, timed_out (来自 TestResultContract)
        success (property, 兼容旧代码)
        output (property, stdout + stderr)
    """

    def summary(self) -> dict:
        """解析测试输出摘要 — 兼容旧 API"""
        return parse_test_summary(self.output)


class TestRunner:
    """测试执行器"""

    def __init__(self, workspace_root="", timeout=SUB_PROCESS_TIMEOUT):
        self.root = workspace_root or os.getcwd()
        self.timeout = timeout

    def run(self, cmd, cwd=None, env=None) -> TestResult:
        """Execute a command securely — list-based subprocess (no shell injection).

        cmd can be a str (auto shlex.split) or a list.
        """
        actual_cwd = cwd or self.root
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = list(cmd)
        log.info("Exec: %s (cwd=%s)", cmd_list, actual_cwd)
        try:
            proc = subprocess.run(
                cmd_list, capture_output=True, text=True,
                timeout=self.timeout, cwd=actual_cwd, env=env,
            )
            return TestResult(
                cmd=" ".join(cmd_list), returncode=proc.returncode,
                stdout=proc.stdout, stderr=proc.stderr,
                timed_out=False,
            )
        except subprocess.TimeoutExpired:
            log.warning("Timeout: %s", cmd_list)
            return TestResult(cmd=" ".join(cmd_list), returncode=-1, stdout="", stderr="", timed_out=True)
        except Exception as e:
            log.error("Exec failed: %s", e)
            return TestResult(cmd=" ".join(cmd_list), returncode=-2, stdout="", stderr=str(e), timed_out=False)

    def run_pytest(self, test_path, extra_args=""):
        """Safely run pytest — list-based, no shell parsing."""
        cmd = ["python", "-m", "pytest", test_path, "-v", "--tb=short"]
        if extra_args:
            cmd.extend(shlex.split(extra_args))
        return self.run(cmd)

    def run_custom(self, cmd):
        return self.run(cmd)
