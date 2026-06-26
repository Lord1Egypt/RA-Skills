#!/usr/bin/env python3
"""
Skills Monitor — AI Skills 一站式监控评估平台
SkillsHUB 入口文件

提供统一的命令式接口，支持以下操作:
  - init: 初始化身份
  - status: 查看系统状态
  - list: 列出已安装 Skills
  - evaluate: 7因子综合评估
  - benchmark: 基准评测
  - baseline: 查询大模型基准分数
  - compare: 对比分析
  - recommend: 智能推荐
  - report: 生成综合日报
  - diagnose: 诊断报告
  - upload: 数据上报
  - dashboard: 启动 Web 面板
  - server: 启动中心化服务器
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── 自动定位项目根目录 ──
SKILL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SKILL_DIR

# 确保核心包可导入（支持两种安装方式：独立 skill 包 or 项目内引用）
for candidate in [SKILL_DIR, SKILL_DIR.parent]:
    init_file = candidate / "skills_monitor" / "__init__.py"
    if init_file.exists():
        PROJECT_ROOT = candidate
        break

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── 核心导入 ──
from skills_monitor.core.identity import IdentityManager
from skills_monitor.core.interceptor import configure, run_skill_function
from skills_monitor.core.implicit_feedback import ImplicitFeedbackEngine
from skills_monitor.core.benchmark import BenchmarkRunner
from skills_monitor.core.comparator import SkillComparator
from skills_monitor.core.evaluator import SkillEvaluator
from skills_monitor.core.recommender import SkillRecommender
from skills_monitor.core.reporter import ReportGenerator
from skills_monitor.core.diagnostic import DiagnosticReporter
from skills_monitor.core.uploader import DataUploader
from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.adapters.runners import SkillRunner, get_adapter

# ── 默认路径 ──
DEFAULT_SKILLS_DIR = str(PROJECT_ROOT / "skills")
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.skills_monitor")
REPORTS_DIR = str(PROJECT_ROOT / "reports")


class SkillsMonitor:
    """Skills Monitor 统一入口类，封装所有命令。"""

    def __init__(self, config_dir=None, skills_dir=None):
        self.config_dir = config_dir or DEFAULT_CONFIG_DIR
        self.skills_dir = skills_dir or DEFAULT_SKILLS_DIR
        self._mgr = None
        self._store = None
        self._registry = None

    @property
    def manager(self) -> IdentityManager:
        if self._mgr is None:
            self._mgr = IdentityManager(self.config_dir)
        return self._mgr

    @property
    def store(self) -> DataStore:
        if self._store is None:
            self._store = DataStore(self.config_dir)
        return self._store

    @property
    def registry(self) -> SkillRegistry:
        if self._registry is None:
            self._registry = SkillRegistry(self.skills_dir)
        return self._registry

    @property
    def is_initialized(self) -> bool:
        return self.manager.is_initialized

    # ──────── 命令实现 ────────

    def init(self, force=False) -> dict:
        """初始化身份"""
        result = self.manager.initialize(force=force)
        self.manager.set_skills_dir(self.skills_dir)
        summary = self.registry.summary()
        return {
            "success": True,
            "status": result["status"],
            "agent_id": result.get("agent_id"),
            "summary": summary,
        }

    def status(self) -> dict:
        """查看系统状态"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化，请先运行 init"}

        config = self.manager.get_config()
        today = datetime.now().strftime("%Y-%m-%d")
        runs = self.store.get_runs(agent_id=self.manager.agent_id, limit=1000)
        today_runs = [r for r in runs if r["start_time"].startswith(today)]
        success_runs = [r for r in today_runs if r["status"] == "success"]

        return {
            "success": True,
            "agent_id": config.get("agent_id"),
            "initialized_at": config.get("created_at"),
            "skills_dir": config.get("skills_dir"),
            "registry_summary": self.registry.summary(),
            "today_runs": len(today_runs),
            "today_success": len(success_runs),
        }

    def list_skills(self) -> dict:
        """列出已安装 Skills"""
        categories = self.registry.get_skills_by_category()
        result = {}
        for cat, skills in sorted(categories.items()):
            result[cat] = [
                {
                    "slug": s.slug,
                    "version": s.version,
                    "entry_type": s.entry_type,
                    "description": s.description,
                    "runnable": s.entry_type != "none",
                }
                for s in skills
            ]

        runnable = self.registry.get_runnable_skills()
        total = len(self.registry.list_skills())
        return {
            "success": True,
            "categories": result,
            "total": total,
            "runnable": len(runnable),
        }

    def evaluate(self, skill_slug=None, verbose=False) -> dict:
        """7因子综合评估"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        evaluator = SkillEvaluator(self.store, self.manager.agent_id)

        if skill_slug:
            scores = [evaluator.evaluate_skill(skill_slug)]
        else:
            skill_ids = [s.slug for s in self.registry.get_runnable_skills()]
            scores = evaluator.evaluate_all(skill_ids)

        if not scores:
            return {"success": True, "scores": [], "message": "暂无可评估数据"}

        results = []
        for s in scores:
            item = {
                "skill_id": s.skill_id,
                "total_score": round(s.total_score, 1),
                "grade": s.grade,
                "factors": s.factors,
            }
            if verbose:
                item["report"] = s.format_report()
            results.append(item)

        return {"success": True, "scores": results}

    def benchmark(self, skill_slug, runs=10, simulate=False) -> dict:
        """基准评测"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        runner = BenchmarkRunner(
            registry=self.registry,
            store=self.store,
            agent_id=self.manager.agent_id,
            cache_dir=os.path.join(self.config_dir, "benchmark_cache"),
        )

        if simulate:
            stats = runner.run_simulated_benchmark(skill_slug, n_runs=runs)
        else:
            stats = runner.run_benchmark(
                skill_id=skill_slug, task_name="", n_runs=runs, delay_between=0.5
            )

        return {
            "success": True,
            "skill_slug": skill_slug,
            "summary": stats.summary_line(),
            "runs": runs,
            "simulated": simulate,
        }

    def compare(self, skill_slug) -> dict:
        """对比分析"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        comparator = SkillComparator(self.store, self.manager.agent_id)
        runner = BenchmarkRunner(
            registry=self.registry,
            store=self.store,
            agent_id=self.manager.agent_id,
            cache_dir=os.path.join(self.config_dir, "benchmark_cache"),
        )

        cached = runner.load_cached_stats(skill_slug)
        if cached:
            bench_stats = cached
        else:
            bench_stats = runner.run_simulated_benchmark(skill_slug, n_runs=10)

        comp = comparator.compare_with_benchmark(skill_slug, bench_stats)
        return {
            "success": True,
            "skill_slug": skill_slug,
            "report": comp.format_report(),
        }

    def recommend(self, category=None, top_n=5) -> dict:
        """智能推荐"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        recommender = SkillRecommender(self.registry, self.store, self.manager.agent_id)
        recs = recommender.get_all_recommendations(max_per_type=top_n)

        if not recs:
            return {"success": True, "recommendations": [], "message": "你的 skills 配置很完善！暂无推荐。"}

        results = []
        for rec in recs[:top_n * 3]:
            results.append({
                "name": getattr(rec, "name", ""),
                "slug": getattr(rec, "slug", ""),
                "category": getattr(rec, "category", ""),
                "reason_type": getattr(rec, "reason_type", ""),
                "reason_detail": getattr(rec, "reason_detail", ""),
                "recommendation_score": getattr(rec, "recommendation_score", 0),
                "description": getattr(rec, "description", ""),
                "formatted": rec.format_line() if hasattr(rec, "format_line") else str(rec),
            })

        return {"success": True, "recommendations": results}

    def report(self, format="markdown") -> dict:
        """生成综合日报"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        evaluator = SkillEvaluator(self.store, self.manager.agent_id)
        skill_ids = [s.slug for s in self.registry.get_runnable_skills()]
        scores = evaluator.evaluate_all(skill_ids)

        recommender = SkillRecommender(self.registry, self.store, self.manager.agent_id)
        recs = recommender.get_all_recommendations(max_per_type=3)

        reporter = ReportGenerator(
            store=self.store,
            registry=self.registry,
            agent_id=self.manager.agent_id,
            reports_dir=os.path.join(REPORTS_DIR, "monitor"),
        )
        filepath = reporter.generate_and_save_daily(scores=scores, recommendations=recs)

        return {"success": True, "filepath": filepath, "format": format}

    def diagnose(self, send=False, trigger="manual", context=None) -> dict:
        """生成诊断报告"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        diag = DiagnosticReporter(
            store=self.store,
            registry=self.registry,
            agent_id=self.manager.agent_id,
            reports_dir=os.path.join(REPORTS_DIR, "diagnostic"),
        )

        content, filepath = diag.generate_and_save(
            trigger=trigger,
            extra_context=context,
        )

        result = {"success": True, "filepath": filepath, "trigger": trigger}

        if send:
            try:
                from wecom_bot.sender import sender as wecom_sender
                summary = diag.generate_wecom_summary(content)
                ok, push_result = wecom_sender.send_to_webhook(summary, msgtype="markdown")
                result["push_success"] = ok
                result["push_result"] = str(push_result) if not ok else "已推送"
            except Exception as e:
                result["push_success"] = False
                result["push_error"] = str(e)

        return result

    def upload(self, server="http://localhost:5100", report_type="daily", register=False, name="") -> dict:
        """上报数据到中心化服务器"""
        if not self.is_initialized:
            return {"success": False, "error": "未初始化"}

        uploader = DataUploader(server)
        uploader.init(self.manager.agent_id, self.manager.api_key)

        result = {"success": True, "server": server}

        if register:
            ok, reg_result = uploader.register(name=name)
            result["register"] = {"ok": ok, "detail": reg_result}

        if report_type == "diagnostic":
            ok, upload_result = uploader.upload_diagnostic()
        else:
            ok, upload_result = uploader.upload_daily()

        result["upload"] = {"ok": ok, "detail": upload_result}
        return result


# ── SkillsHUB 标准入口 ──

def run(command: str = "status", **kwargs) -> dict:
    """
    SkillsHUB 统一入口函数。

    Args:
        command: 命令名 (init/status/list/evaluate/benchmark/compare/recommend/report/diagnose/upload)
        **kwargs: 命令参数

    Returns:
        dict: 命令执行结果
    """
    monitor = SkillsMonitor(
        config_dir=kwargs.pop("config_dir", None),
        skills_dir=kwargs.pop("skills_dir", None),
    )

    commands = {
        "init": lambda: monitor.init(force=kwargs.get("force", False)),
        "status": lambda: monitor.status(),
        "list": lambda: monitor.list_skills(),
        "evaluate": lambda: monitor.evaluate(
            skill_slug=kwargs.get("skill_slug"),
            verbose=kwargs.get("verbose", False),
        ),
        "benchmark": lambda: monitor.benchmark(
            skill_slug=kwargs.get("skill_slug", ""),
            runs=kwargs.get("runs", 10),
            simulate=kwargs.get("simulate", False),
        ),
        "compare": lambda: monitor.compare(skill_slug=kwargs.get("skill_slug", "")),
        "recommend": lambda: monitor.recommend(
            category=kwargs.get("category"),
            top_n=kwargs.get("top_n", 5),
        ),
        "report": lambda: monitor.report(format=kwargs.get("format", "markdown")),
        "diagnose": lambda: monitor.diagnose(
            send=kwargs.get("send", False),
            trigger=kwargs.get("trigger", "manual"),
            context=kwargs.get("context"),
        ),
        "upload": lambda: monitor.upload(
            server=kwargs.get("server", "http://localhost:5100"),
            report_type=kwargs.get("type", "daily"),
            register=kwargs.get("register", False),
            name=kwargs.get("name", ""),
        ),
    }

    cmd_func = commands.get(command)
    if not cmd_func:
        return {
            "success": False,
            "error": f"未知命令: {command}",
            "available_commands": list(commands.keys()),
        }

    try:
        return cmd_func()
    except Exception as e:
        return {"success": False, "error": str(e), "command": command}


# ── CLI 入口（兼容直接运行） ──

def main():
    """CLI 入口，供直接 python main.py <command> 使用。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Skills Monitor — AI Skills 监控评估平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py init                    # 初始化身份
  python main.py status                  # 查看系统状态
  python main.py list                    # 列出已安装 Skills
  python main.py evaluate               # 评估所有 Skills
  python main.py evaluate --skill xxx   # 评估指定 Skill
  python main.py recommend              # 智能推荐
  python main.py diagnose --send        # 诊断报告 + 企微推送
  python main.py upload --server URL    # 上报数据
        """,
    )
    parser.add_argument("command", choices=[
        "init", "status", "list", "evaluate", "benchmark",
        "compare", "recommend", "report", "diagnose", "upload",
    ], help="要执行的命令")
    parser.add_argument("--skill", type=str, help="指定 Skill slug")
    parser.add_argument("--runs", type=int, default=10, help="基准评测运行次数")
    parser.add_argument("--simulate", action="store_true", help="模拟基准评测")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--send", action="store_true", help="推送到企微")
    parser.add_argument("--trigger", type=str, default="manual", help="诊断触发方式")
    parser.add_argument("--server", type=str, default="http://localhost:5100", help="服务器地址")
    parser.add_argument("--type", type=str, default="daily", help="上报类型")
    parser.add_argument("--register", action="store_true", help="注册 Agent")
    parser.add_argument("--force", action="store_true", help="强制初始化")
    parser.add_argument("--format", type=str, default="markdown", help="报告格式")

    args = parser.parse_args()

    result = run(
        command=args.command,
        skill_slug=args.skill,
        runs=args.runs,
        simulate=args.simulate,
        verbose=args.verbose,
        send=args.send,
        trigger=args.trigger,
        server=args.server,
        type=args.type,
        register=args.register,
        force=args.force,
        format=args.format,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
