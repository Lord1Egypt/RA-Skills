"""
本地 Agent 数据上报模块 — 增量同步到中心化服务器
===============================================
与 skills_monitor 核心包对接，读取本地 SQLite 数据并上报。

使用方式:
  from skills_monitor.core.uploader import DataUploader
  uploader = DataUploader(server_url="https://your-server.com")
  uploader.register()      # 注册 Agent
  uploader.upload_daily()  # 上报每日数据
"""

import platform
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List, Tuple

import requests


class DataUploader:
    """
    本地 Agent 数据上报器
    - 自动发现身份 (agent_id + token)
    - 读取本地 SQLite 数据
    - 增量上报到中心化服务器
    """

    def __init__(self, server_url: str = "http://localhost:5100", skills_dir: str = "skills"):
        self.server_url = server_url.rstrip("/")
        self.skills_dir = skills_dir
        self._agent_id = None
        self._token = None
        self._identity = None

    # ──────── 初始化 ────────

    def init(self, agent_id: str = None, token: str = None) -> "DataUploader":
        """初始化身份（从参数或本地配置读取）"""
        if agent_id and token:
            self._agent_id = agent_id
            self._token = token
        else:
            self._load_identity()

        return self

    def _load_identity(self):
        """从本地 skills_monitor 配置加载身份"""
        try:
            from skills_monitor.core.identity import IdentityManager
            mgr = IdentityManager()
            self._agent_id = mgr.agent_id
            self._token = mgr.api_key
        except ImportError:
            raise RuntimeError("未安装 skills_monitor 包，请先运行 pip install -e .")

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "X-Agent-ID": self._agent_id or "",
            "X-Agent-Token": self._token or "",
            "Content-Type": "application/json",
        }

    # ──────── 注册 ────────

    def register(self, name: str = None) -> Tuple[bool, Dict]:
        """向中心服务器注册/更新 Agent"""
        import skills_monitor

        payload = {
            "agent_id": self._agent_id,
            "token": self._token,
            "name": name or f"Agent-{platform.node()}",
            "os_info": f"{platform.system()} {platform.release()}",
            "python_version": platform.python_version(),
            "monitor_version": getattr(skills_monitor, "__version__", "0.4.0"),
        }

        try:
            from skills_monitor.adapters.skill_registry import SkillRegistry
            registry = SkillRegistry(self.skills_dir)
            skills = registry.list_skills()
            payload["total_skills"] = len(skills)
            payload["runnable_skills"] = len(registry.get_runnable_skills())
        except Exception:
            pass

        try:
            resp = requests.post(
                f"{self.server_url}/api/agent/register",
                json=payload,
                timeout=15,
            )
            data = resp.json()
            return data.get("ok", False), data
        except requests.RequestException as e:
            return False, {"error": str(e)}

    # ──────── 心跳 ────────

    def heartbeat(self) -> Tuple[bool, Dict]:
        """发送心跳"""
        try:
            resp = requests.post(
                f"{self.server_url}/api/agent/heartbeat",
                headers=self._headers,
                timeout=10,
            )
            data = resp.json()
            return data.get("ok", False), data
        except requests.RequestException as e:
            return False, {"error": str(e)}

    # ──────── 上报 ────────

    def upload_daily(self, report_date: date = None, trigger: str = "manual") -> Tuple[bool, Dict]:
        """采集并上报每日数据"""
        self.ensure_initial_diagnostic_uploaded()
        report_day = report_date or date.today()
        report_data = self._collect_daily_data(report_day, trigger=trigger)
        return self._upload(report_data, "daily", report_day)

    def upload_diagnostic(self, diagnostic_data: dict = None, trigger: str = "manual") -> Tuple[bool, Dict]:
        """上报诊断数据，外部传入 markdown 时自动补齐结构化字段"""
        if diagnostic_data:
            structured = self._collect_diagnostic_data(
                trigger=diagnostic_data.get("trigger", trigger),
                extra_context=diagnostic_data.get("extra_context"),
            )
            merged = dict(structured)
            merged.update({k: v for k, v in diagnostic_data.items() if v is not None})
            diagnostic_data = merged
        else:
            diagnostic_data = self._collect_diagnostic_data(trigger=trigger)
        report_day = self._extract_report_date(diagnostic_data)
        return self._upload(diagnostic_data, "diagnostic", report_day)

    def upload_custom(self, data: dict, report_type: str = "custom") -> Tuple[bool, Dict]:
        """上报自定义数据"""
        return self._upload(data, report_type)

    def ensure_initial_diagnostic_uploaded(self) -> Tuple[bool, Dict]:
        """若服务端还没有诊断报告，则自动补传一次首次诊断报告"""
        ok, reports = self.get_reports(report_type="diagnostic", limit=1)
        if ok and reports:
            return True, {"ok": True, "skipped": True, "reason": "diagnostic_exists"}

        fallback_data = self._collect_diagnostic_data(
            trigger="first_sync_fallback",
            extra_context="首次运行诊断报告缺失，自动兜底补传",
        )
        report_day = self._extract_report_date(fallback_data) or date.today()
        return self._upload(fallback_data, "diagnostic", report_day)

    def _upload(self, data: dict, report_type: str, report_date: date = None) -> Tuple[bool, Dict]:
        """通用上传（发送前自动脱敏）"""
        try:
            from skills_monitor.core.sanitizer import DataSanitizer
            sanitizer = DataSanitizer()
            data = sanitizer.sanitize(data)
        except ImportError:
            pass

        payload = {
            "data": data,
            "report_type": report_type,
        }
        if report_date:
            payload["report_date"] = report_date.isoformat()

        try:
            resp = requests.post(
                f"{self.server_url}/api/agent/report",
                headers=self._headers,
                json=payload,
                timeout=30,
            )
            result = resp.json()
            return result.get("ok", False), result
        except requests.RequestException as e:
            return False, {"error": str(e)}

    # ──────── 数据采集 ────────

    def _collect_daily_data(self, report_day: date, trigger: str = "manual") -> dict:
        """从本地 SQLite 采集每日数据"""
        from skills_monitor.data.store import DataStore
        from skills_monitor.adapters.skill_registry import SkillRegistry
        from skills_monitor.core.recommender import SkillRecommender
        from skills_monitor.core.reporter import ReportGenerator
        from skills_monitor.core.diagnostic import DiagnosticReporter

        store = DataStore()
        registry = SkillRegistry(skills_dir=self.skills_dir)
        all_skills = registry.list_skills()
        runnable = registry.get_runnable_skills()
        skill_ids = [s.slug for s in runnable]

        evaluator = self._build_evaluator(store, skill_ids)
        scores = evaluator.evaluate_all(skill_ids)
        recommender = SkillRecommender(registry, store, self._agent_id)
        recommendations = recommender.get_all_recommendations(max_per_type=3)

        all_runs = self._get_all_runs(store)
        today_runs = self._runs_for_day(all_runs, report_day)
        week_runs = self._runs_since(all_runs, days=7)
        user_runs = self._exclude_benchmark_runs(today_runs)
        user_week_runs = self._exclude_benchmark_runs(week_runs)

        diag = DiagnosticReporter(store, registry, self._agent_id, reports_dir="reports/diagnostic")
        health_score = diag._calculate_health_score(
            all_skills,
            runnable,
            scores,
            user_runs,
            user_week_runs,
            recommendations,
        )

        overview = self._build_overview(
            all_skills=all_skills,
            runnable=runnable,
            runs=user_runs,
            week_runs=user_week_runs,
            health_score=health_score,
        )
        installed_skills = self._build_installed_skills(store, all_skills, scores)
        report_markdown = ReportGenerator(
            store=store,
            registry=registry,
            agent_id=self._agent_id,
        ).generate_daily_report(
            scores=scores,
            recommendations=recommendations,
            date=report_day.isoformat(),
        )

        return {
            "collected_at": datetime.now().isoformat(),
            "report_date": report_day.isoformat(),
            "trigger": trigger,
            "agent_id": self._agent_id,
            "health_score": health_score,
            "overview": overview,
            "scores": [s.to_dict() for s in scores],
            "recommendations": [r.to_dict() for r in recommendations],
            "installed_skills": installed_skills,
            "skill_details": installed_skills,
            "report_markdown": report_markdown,
        }

    def _collect_diagnostic_data(self, trigger: str = "manual", extra_context: str = None) -> dict:
        """采集诊断数据并补齐结构化字段"""
        from skills_monitor.data.store import DataStore
        from skills_monitor.adapters.skill_registry import SkillRegistry
        from skills_monitor.core.recommender import SkillRecommender
        from skills_monitor.core.diagnostic import DiagnosticReporter

        store = DataStore()
        registry = SkillRegistry(skills_dir=self.skills_dir)
        all_skills = registry.list_skills()
        runnable = registry.get_runnable_skills()
        skill_ids = [s.slug for s in runnable]

        evaluator = self._build_evaluator(store, skill_ids)
        scores = evaluator.evaluate_all(skill_ids)
        recommender = SkillRecommender(registry, store, self._agent_id)
        recommendations = recommender.get_all_recommendations(max_per_type=3)

        all_runs = self._get_all_runs(store)
        today_runs = self._runs_for_day(all_runs, date.today())
        week_runs = self._runs_since(all_runs, days=7)
        user_runs = self._exclude_benchmark_runs(today_runs)
        user_week_runs = self._exclude_benchmark_runs(week_runs)

        diag = DiagnosticReporter(store, registry, self._agent_id, reports_dir="reports/diagnostic")
        report_markdown = diag.generate_diagnostic_report(trigger=trigger, extra_context=extra_context)
        health_score = diag._calculate_health_score(
            all_skills,
            runnable,
            scores,
            user_runs,
            user_week_runs,
            recommendations,
        )

        return {
            "collected_at": datetime.now().isoformat(),
            "report_date": date.today().isoformat(),
            "trigger": trigger,
            "agent_id": self._agent_id,
            "health_score": health_score,
            "overview": self._build_overview(
                all_skills=all_skills,
                runnable=runnable,
                runs=user_runs,
                week_runs=user_week_runs,
                health_score=health_score,
            ),
            "scores": [s.to_dict() for s in scores],
            "recommendations": [r.to_dict() for r in recommendations],
            "installed_skills": self._build_installed_skills(store, all_skills, scores),
            "diagnostics": self._build_diagnostics_payload(
                registry=registry,
                scores=scores,
                all_skills=all_skills,
                runnable=runnable,
                recommendations=recommendations,
                week_runs=user_week_runs,
            ),
            "report_markdown": report_markdown,
        }

    def _build_evaluator(self, store, skill_ids: List[str]):
        from skills_monitor.core.evaluator import SkillEvaluator
        from skills_monitor.adapters.clawhub_client import ClawHubClient

        community_data = {}
        if skill_ids:
            try:
                client = ClawHubClient()
                metadata = client.batch_fetch(skill_ids)
                for slug, meta in metadata.items():
                    community_data[slug] = {
                        "downloads": meta.get("installs") or 0,
                        "stars": meta.get("stars") or 0,
                        "current_installs": meta.get("installs") or 0,
                    }
            except Exception:
                community_data = {}

        return SkillEvaluator(store, self._agent_id, community_data=community_data)

    def _get_all_runs(self, store) -> List[dict]:
        try:
            return store.get_runs(agent_id=self._agent_id, limit=5000)
        except Exception:
            try:
                return store.get_all_runs(days=30)
            except Exception:
                return []

    def _runs_for_day(self, runs: List[dict], day: date) -> List[dict]:
        prefix = day.isoformat()
        return [r for r in runs if str(r.get("start_time", "")).startswith(prefix)]

    def _runs_since(self, runs: List[dict], days: int = 7) -> List[dict]:
        cutoff = datetime.now() - timedelta(days=days)
        result = []
        for run in runs:
            start_time = str(run.get("start_time", ""))
            if not start_time:
                continue
            try:
                run_time = datetime.fromisoformat(start_time.replace("Z", ""))
            except ValueError:
                continue
            if run_time >= cutoff:
                result.append(run)
        return result

    def _exclude_benchmark_runs(self, runs: List[dict]) -> List[dict]:
        return [r for r in runs if not str(r.get("task_name", "")).startswith("[benchmark]")]

    def _build_overview(
        self,
        all_skills: List[Any],
        runnable: List[Any],
        runs: List[dict],
        week_runs: List[dict],
        health_score: float,
    ) -> Dict[str, Any]:
        total_runs = len(runs)
        success_runs = sum(1 for r in runs if self._is_success_run(r))
        success_rate = round(success_runs / total_runs * 100, 1) if total_runs else 0.0
        durations = [r.get("duration_ms") for r in runs if r.get("duration_ms")]
        avg_duration = round(sum(durations) / len(durations), 1) if durations else 0.0
        active_today = len({r.get("skill_id") for r in runs if r.get("skill_id")})
        active_week = len({r.get("skill_id") for r in week_runs if r.get("skill_id")})

        return {
            "health_score": round(health_score, 1),
            "total_installed": len(all_skills),
            "total_runnable": len(runnable),
            "total_runs": total_runs,
            "success_rate": success_rate,
            "avg_duration_ms": avg_duration,
            "active_skills": active_today,
            "active_skills_7d": active_week,
        }

    def _build_installed_skills(self, store, all_skills: List[Any], scores: List[Any]) -> List[Dict[str, Any]]:
        score_map = {score.skill_id: score for score in scores}
        items: List[Dict[str, Any]] = []

        for skill in all_skills:
            summary = store.get_skill_summary(skill.slug, self._agent_id)
            score = score_map.get(skill.slug)
            score_payload = score.to_dict() if score else None
            item = {
                "slug": skill.slug,
                "name": skill.name,
                "category": skill.category,
                "description": skill.description,
                "version": skill.version,
                "entry_type": skill.entry_type,
                "runnable": skill.entry_type != "none",
                "total_runs": summary.get("total_runs", 0),
                "success_rate": summary.get("success_rate"),
                "avg_rating": summary.get("avg_rating"),
                "score": score_payload,
            }
            if score_payload:
                item["total_score"] = score_payload.get("total_score")
                item["grade"] = score_payload.get("grade")
                item["raw_factors"] = score_payload.get("raw_factors", {})
                item["factors"] = score_payload.get("factors", {})
            items.append(item)

        items.sort(
            key=lambda x: (
                -(x.get("total_score") or -1),
                -(x.get("total_runs") or 0),
                x.get("slug", ""),
            )
        )
        return items

    def _build_diagnostics_payload(
        self,
        registry,
        scores: List[Any],
        all_skills: List[Any],
        runnable: List[Any],
        recommendations: List[Any],
        week_runs: List[dict],
    ) -> Dict[str, Any]:
        issues = self._collect_issue_items(scores, all_skills, runnable, recommendations)
        suggestions = self._collect_suggestion_items(scores, runnable, recommendations, week_runs)
        coverage = []
        for category, skills in sorted(registry.get_skills_by_category().items()):
            total = len(skills)
            runnable_count = len([s for s in skills if s.entry_type != "none"])
            coverage.append({
                "category": category,
                "total": total,
                "runnable": runnable_count,
                "coverage_rate": round(runnable_count / max(total, 1) * 100, 1),
            })

        usage_top = []
        counter: Dict[str, Dict[str, Any]] = {}
        for run in week_runs:
            skill_id = run.get("skill_id")
            if not skill_id:
                continue
            counter.setdefault(skill_id, {"skill_id": skill_id, "runs": 0, "success": 0})
            counter[skill_id]["runs"] += 1
            if self._is_success_run(run):
                counter[skill_id]["success"] += 1

        for item in sorted(counter.values(), key=lambda x: x["runs"], reverse=True)[:5]:
            item["success_rate"] = round(item["success"] / max(item["runs"], 1) * 100, 1)
            usage_top.append(item)

        runnable_slugs = {s.slug for s in runnable}
        used_slugs = set(counter.keys())
        unused_runnable = sorted(runnable_slugs - used_slugs)

        return {
            "issues": issues,
            "suggestions": suggestions,
            "coverage": coverage,
            "usage_top": usage_top,
            "unused_runnable": unused_runnable,
        }

    def _collect_issue_items(
        self,
        scores: List[Any],
        all_skills: List[Any],
        runnable: List[Any],
        recommendations: List[Any],
    ) -> List[str]:
        issues: List[str] = []

        low_scores = [s for s in scores if s.total_score < 60]
        for score in low_scores:
            issues.append(
                f"{score.skill_id} 综合评分仅 {score.total_score:.1f} 分，等级 {score.grade.split('(')[0].strip()}"
            )

        for score in scores:
            raw_success = score.factors.get("success_rate", 100)
            if raw_success is not None and raw_success < 80 and score not in low_scores:
                issues.append(f"{score.skill_id} 成功率仅 {raw_success:.0f}%，建议排查")

        non_runnable = len(all_skills) - len(runnable)
        if non_runnable > len(runnable):
            issues.append(f"不可运行 skills 达到 {non_runnable} 个，可运行率偏低")

        complement_recs = [r for r in recommendations if r.reason_type == "complement"]
        if complement_recs:
            categories = sorted({r.skill_info.get("category", "未分类") for r in complement_recs})
            issues.append(f"能力覆盖存在缺口，建议补齐 {', '.join(categories)}")

        upgrade_recs = [r for r in recommendations if r.reason_type == "upgrade"]
        for rec in upgrade_recs:
            issues.append(f"{rec.related_installed} 建议升级为 {rec.skill_info['name']}")

        return issues

    def _collect_suggestion_items(
        self,
        scores: List[Any],
        runnable: List[Any],
        recommendations: List[Any],
        week_runs: List[dict],
    ) -> List[str]:
        suggestions: List[str] = []
        priority = 1

        low_scores = [s for s in scores if s.total_score < 60]
        if low_scores:
            names = ", ".join(f"`{s.skill_id}`" for s in low_scores[:3])
            suggestions.append(
                f"P{priority} 关注低评分 skills：{names}，优先排查成功率与稳定性"
            )
            priority += 1

        needs_data = [s for s in scores if s.factors.get("satisfaction") is None]
        if needs_data:
            names = ", ".join(f"`{s.skill_id}`" for s in needs_data[:3])
            suggestions.append(
                f"P{priority} 以下 skills 还缺少满意度数据：{names}，建议增加真实使用样本"
            )
            priority += 1

        used_week = {r.get("skill_id") for r in week_runs if r.get("skill_id")}
        runnable_slugs = {s.slug for s in runnable}
        unused = runnable_slugs - used_week
        if len(unused) > 3:
            suggestions.append(
                f"P{priority} 过去 7 天有 {len(unused)} 个可运行 skills 未被调用，建议评估保留价值"
            )
            priority += 1

        if recommendations:
            top_names = ", ".join(rec.skill_info["name"] for rec in recommendations[:3])
            suggestions.append(
                f"P{priority} 优先关注推荐安装：{top_names}"
            )

        return suggestions

    def _is_success_run(self, run: dict) -> bool:
        return bool(run.get("success") or run.get("status") == "success")

    def _extract_report_date(self, data: dict) -> Optional[date]:
        report_date = data.get("report_date")
        if isinstance(report_date, date):
            return report_date
        if isinstance(report_date, str):
            try:
                return date.fromisoformat(report_date)
            except ValueError:
                return None
        return None

    # ──────── 生成绑定二维码 ────────

    def get_bind_qrcode(self) -> Tuple[bool, Dict]:
        """请求服务器生成带参二维码（用于微信扫码绑定）"""
        try:
            resp = requests.post(
                f"{self.server_url}/api/agent/bind-qrcode",
                headers=self._headers,
                json={"agent_id": self._agent_id, "token": self._token},
                timeout=10,
            )
            data = resp.json()
            return data.get("ok", False), data
        except requests.RequestException as e:
            return False, {"error": str(e)}

    # ──────── 查询历史 ────────

    def get_reports(self, report_type: str = None, limit: int = 30) -> Tuple[bool, list]:
        """查询服务器上的历史报告"""
        params = {"limit": limit}
        if report_type:
            params["type"] = report_type

        try:
            resp = requests.get(
                f"{self.server_url}/api/agent/reports",
                headers=self._headers,
                params=params,
                timeout=10,
            )
            data = resp.json()
            return data.get("ok", False), data.get("reports", [])
        except requests.RequestException:
            return False, []
