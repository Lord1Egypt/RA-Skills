"""零稀泥模式 — 项目环境检测器 env_detector.py

SKILL.md §0.5 声明的自动环境检测流程的实现。
在 Phase 0 自动运行，消除手动传入环境参数的需求。

Usage:
    from env_detector import EnvironDetector
    detector = EnvironDetector()
    env = detector.detect()
"""

import os, sys, json, subprocess, logging

log = logging.getLogger("env_detector")


class EnvironDetector:
    """项目环境检测器 — 自动推断 project_type / test_cmd / vcs / lang"""

    def __init__(self, workspace_root: str = ""):
        self.root = workspace_root or os.getcwd()

    # ── 项目类型检测 ──

    def detect_project_type(self) -> str:
        if os.path.exists(os.path.join(self.root, "gateway.py")):
            return "gateway_project"
        for marker in ("pyproject.toml", "setup.py", "pytest.ini", "tox.ini"):
            if os.path.exists(os.path.join(self.root, marker)):
                return "python"
        if os.path.exists(os.path.join(self.root, "package.json")):
            return "node"
        return "unknown"

    def detect_lang(self) -> str:
        pt = self.detect_project_type()
        return {"python": "python", "node": "node", "gateway_project": "python"}.get(pt, "unknown")

    # ── 测试命令检测 ──

    def detect_test_command(self) -> str:
        pt = self.detect_project_type()
        if pt == "gateway_project":
            return "gateway.py dispatch()"
        if pt == "python":
            pyproject = os.path.join(self.root, "pyproject.toml")
            if os.path.exists(pyproject):
                return "python -m pytest tests/ -v --tb=short"
            return "pytest tests/ -v --tb=short"
        if pt == "node":
            pj = os.path.join(self.root, "package.json")
            if os.path.exists(pj):
                try:
                    with open(pj, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                    scripts = cfg.get("scripts", {})
                    for key in ("test", "ci", "check"):
                        if key in scripts:
                            return scripts[key]
                except (json.JSONDecodeError, OSError):
                    pass
            return "npx jest"  # default for node projects
        return ""  # unknown → no default

    # ── VCS 检测 ──

    def detect_vcs(self) -> str:
        for marker in (".git", ".svn", ".hg"):
            if os.path.isdir(os.path.join(self.root, marker)):
                return {"git": "git", "svn": "svn", "hg": "hg"}.get(marker.lstrip("."), marker.lstrip("."))
        return "none"

    # ── 全量检测 ──

    def detect(self) -> dict:
        return {
            "project_type": self.detect_project_type(),
            "test_cmd": self.detect_test_command(),
            "vcs": self.detect_vcs(),
            "lang": self.detect_lang(),
        }

    def detect_and_apply(self, config) -> dict:
        """检测环境并应用到类似 PipelineConfig 的对象"""
        env = self.detect()
        if hasattr(config, "project_type") and (not config.project_type or config.project_type == "unknown"):
            config.project_type = env["project_type"]
        if hasattr(config, "test_cmd") and not config.test_cmd:
            config.test_cmd = env["test_cmd"]
        if hasattr(config, "vcs") and (not config.vcs or config.vcs == "none"):
            config.vcs = env["vcs"]
        if hasattr(config, "lang") and not config.lang:
            config.lang = env["lang"]
        return env


if __name__ == "__main__":
    d = EnvironDetector()
    env = d.detect()
    print(f"Project type: {env['project_type']}")
    print(f"Test command: {env['test_cmd']}")
    print(f"VCS: {env['vcs']}")
    print(f"Lang: {env['lang']}")
