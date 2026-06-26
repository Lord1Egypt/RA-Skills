from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from .interface import SpiritInterface
from .llm_layer import SpiritLLMLayer
from .reports.daily import DailyReportGenerator, WeeklyReportGenerator, MonthlyReportGenerator
from .health.checker import HealthChecker, HealthReport
from .commands.parser import CommandParser, ParsedCommand
from .commands.executor import CommandExecutor, ExecutionResult

logger = logging.getLogger(__name__)


class Spirit:
    """The unified Spirit (器灵/管家) system.

    Combines the "butler" (管家) functionality with the "awareness" (器灵)
    functionality into one cohesive system.

    - Generates daily/weekly/monthly reports
    - Performs health checks
    - Parses natural language commands
    - Executes operations with confirmation
    - Provides the cognition bridge (access to CognitionEngine)
    - Implements the dual-LLM safety protocol
    """

    def _check_llm_budget(self) -> bool:
        """Check if LLM budget allows another call."""
        try:
            from agent_memory.config.settings import settings
            limit = settings.get("cost.llm_daily_call_limit", 500)

            today = datetime.now().strftime("%Y-%m-%d")
            if not hasattr(self, '_llm_call_counter'):
                self._llm_call_counter = {}
                self._llm_call_date = today

            if self._llm_call_date != today:
                self._llm_call_counter = {}
                self._llm_call_date = today

            current_count = self._llm_call_counter.get("total", 0)
            if current_count >= limit:
                logger.warning(f"LLM daily call limit reached ({current_count}/{limit})")
                return False
            return True
        except Exception:
            return True

    def __init__(
        self,
        store,
        recall_engine,
        maintain_engine,
        cognition_engine,
        embedding_store,
        llm_client=None,
    ):
        self.interface = SpiritInterface(
            store, recall_engine, maintain_engine, cognition_engine, embedding_store,
        )
        self.llm_layer = SpiritLLMLayer(llm_client)

        self.daily = DailyReportGenerator(self.interface, self.llm_layer)
        self.weekly = WeeklyReportGenerator(self.interface, self.llm_layer)
        self.monthly = MonthlyReportGenerator(self.interface, self.llm_layer)

        self.health = HealthChecker(self.interface, self.llm_layer)
        self.parser = CommandParser(self.llm_layer)
        self.executor = CommandExecutor(self.interface, self.llm_layer)

    def report(self, report_type: str = 'daily', date: int = None, format: str = 'markdown', discover_causal: bool = True) -> str:
        """Generate report (daily/weekly/monthly).

        Args:
            report_type: 'daily', 'weekly', or 'monthly'
            date: Unix timestamp for the target date (default: today)
            format: 'markdown' or 'json'
            discover_causal: If True, include causal chain discoveries

        Returns:
            Formatted report string
        """
        generators = {
            'daily': self.daily,
            'weekly': self.weekly,
            'monthly': self.monthly,
        }

        generator = generators.get(report_type)
        if generator is None:
            return f"[错误] 未知报告类型: {report_type}。请使用: daily, weekly, monthly"

        try:
            result = generator.generate(date=date, format=format)

            if self.llm_layer and report_type == 'daily':
                if not self._check_llm_budget():
                    logger.warning("LLM budget exceeded, skipping report summary")
                else:
                    summary = self.llm_layer.generate_report_summary(result)
                    if summary:
                        self._llm_call_counter["total"] = self._llm_call_counter.get("total", 0) + 1
                        result = result + "\n\n## 📋 今日记忆摘要\n" + summary

            # Add causal discoveries
            if discover_causal:
                days_map = {'daily': 1, 'weekly': 7, 'monthly': 30}
                causal = self._discover_causal_chains(days=days_map.get(report_type, 7))
                if causal:
                    if format == 'json':
                        import json
                        try:
                            data = json.loads(result)
                            data["causal_discoveries"] = causal
                            result = json.dumps(data, ensure_ascii=False, indent=2)
                        except (json.JSONDecodeError, TypeError):
                            result = result + "\n\n" + self._format_causal_markdown(causal)
                    else:
                        result = result + self._format_causal_markdown(causal)

            return result
        except Exception as e:
            logger.error("Spirit.report(%s): %s", report_type, e)
            return f"[错误] 报告生成失败: {e}"

    def _format_causal_markdown(self, causal: list) -> str:
        """Format causal discoveries as markdown section."""
        lines = [
            "",
            "## 🔗 因果发现",
            "",
            f"> 发现了 {len(causal)} 条潜在的因果关系",
            "",
        ]
        for i, d in enumerate(causal, 1):
            lines.append(f"### 因果链 {i}")
            lines.append(f"- **原因**: {d['cause']}")
            lines.append(f"- **结果**: {d['effect']}")
            lines.append(f"- **置信度**: {d['confidence']}")
            lines.append(f"- **时间间隔**: {d.get('time_gap_hours', '?')} 小时")
            lines.append("")
        return "\n".join(lines)

    def check_health(self, fix: bool = False) -> HealthReport:
        """Run health check, optionally auto-fix.

        Args:
            fix: If True, automatically fix fixable issues

        Returns:
            HealthReport with status, score, and issues
        """
        try:
            return self.health.check(fix=fix)
        except Exception as e:
            logger.error("Spirit.check_health: %s", e)
            return HealthReport(
                overall_status='error',
                score=0.0,
                issues=[],
                checked_at=0,
            )

    def execute(self, command_text: str, confirm: bool = True) -> ExecutionResult:
        """Parse and execute a natural language command.

        Args:
            command_text: Natural language command
            confirm: If True, auto-confirm write operations.
                     If False, return preview for user confirmation.

        Returns:
            ExecutionResult with success status and output
        """
        logger.info("Spirit execute: command=%r, confirm=%s", command_text[:100], confirm)

        try:
            parsed = self.parser.parse(command_text)

            if parsed.intent == 'unknown':
                return ExecutionResult(
                    success=False,
                    intent='unknown',
                    error=f"无法理解命令: {command_text}",
                )

            if parsed.intent in CommandExecutor.WRITE_INTENTS and not confirm:
                logger.warning("Write operation requires confirmation: intent=%s", parsed.intent)
                confirm = True

            if parsed.intent == 'report':
                report_type = parsed.params.get('report_type', 'daily')
                report_output = self.report(report_type=report_type)
                return ExecutionResult(
                    success=True,
                    intent='report',
                    action_taken='executed',
                    output=report_output,
                )

            return self.executor.execute(parsed, confirm=confirm)

        except Exception as e:
            logger.error("Spirit.execute: %s", e)
            return ExecutionResult(
                success=False,
                error=str(e),
            )

    def get_profile(self) -> dict:
        """Get self-profile from cognition engine.

        Returns:
            SelfProfile dict with personality, style, emotion, cognitive data
        """
        cognition = self.interface._cognition_engine
        if cognition is None:
            return {"status": "no_cognition_engine"}

        try:
            profile = cognition.build_self_profile()
            return profile.to_dict()
        except Exception as e:
            logger.error("Spirit.get_profile: %s", e)
            return {"status": "error", "error": str(e)}

    def query_awareness(self, topic: str) -> dict:
        """Query knowledge awareness about a topic.

        Returns confidence, status, gaps, and recommendations.
        """
        if not topic:
            return {"status": "no_topic", "confidence": 0.0}

        try:
            result = self.interface.query_awareness(topic)
            return {
                'content': result.content,
                'confidence': result.confidence,
                'source_count': result.source_count,
                'unverified': result.unverified,
            }
        except Exception as e:
            logger.error("Spirit.query_awareness: %s", e)
            return {"status": "error", "error": str(e), "confidence": 0.0}

    def get_stats(self) -> dict:
        """Get overall system statistics."""
        try:
            result = self.interface.get_stats()
            return {
                'content': result.content,
                'confidence': result.confidence,
                'source_count': result.source_count,
            }
        except Exception as e:
            logger.error("Spirit.get_stats: %s", e)
            return {"status": "error", "error": str(e)}

    def _discover_causal_chains(self, days=7):
        """Proactively discover potential causal relationships in recent memories.

        Scans recent memories for patterns like:
        - Action followed by observable change
        - Configuration change followed by metric shift
        - Event A consistently precedes event B

        Args:
            days: Number of days to look back (default 7)

        Returns:
            list of {"cause": str, "effect": str, "confidence": float, "evidence_count": int}
        """
        store = self.interface._store
        if not store:
            return []

        discoveries = []

        try:
            import time
            now = int(time.time())
            time_from = now - days * 86400

            recent = store.query(time_from=time_from, limit=100)
            if len(recent) < 5:
                return []

            # Simple pattern: look for action-result pairs
            # Action memories contain verbs like "deployed", "changed", "updated"
            # Result memories contain metrics like "increased", "decreased", "error"
            action_keywords = ["deploy", "change", "update", "config", "release", "启动", "部署", "修改", "更新", "配置"]
            result_keywords = ["increase", "decrease", "error", "fail", "improve", "增加", "减少", "错误", "失败", "改善", "延迟", "latency"]

            actions = []
            results = []

            for mem in recent:
                content = (mem.get("content") or "").lower()
                ts = mem.get("time_ts", 0)

                is_action = any(kw in content for kw in action_keywords)
                is_result = any(kw in content for kw in result_keywords)

                if is_action and not is_result:
                    actions.append({"content": mem.get("content", ""), "ts": ts, "id": mem.get("memory_id", "")})
                elif is_result and not is_action:
                    results.append({"content": mem.get("content", ""), "ts": ts, "id": mem.get("memory_id", "")})

            # Find action-result pairs where result follows action within 24 hours
            for action in actions:
                for result in results:
                    time_diff = result["ts"] - action["ts"]
                    if 0 < time_diff < 86400:  # Within 24 hours
                        # Simple confidence based on time proximity
                        confidence = max(0.3, 1.0 - (time_diff / 86400))
                        discoveries.append({
                            "cause": action["content"][:100],
                            "effect": result["content"][:100],
                            "confidence": round(confidence, 2),
                            "evidence_count": 1,
                            "time_gap_hours": round(time_diff / 3600, 1),
                        })

            # Deduplicate similar discoveries
            seen = set()
            unique = []
            for d in discoveries:
                key = (d["cause"][:30], d["effect"][:30])
                if key not in seen:
                    seen.add(key)
                    unique.append(d)

            # Sort by confidence
            unique.sort(key=lambda x: x["confidence"], reverse=True)
            return unique[:10]  # Top 10

        except Exception as e:
            logger.debug("Causal discovery failed: %s", e)
            return []

    def get_llm_usage(self) -> dict:
        """Get LLM usage statistics."""
        return self.llm_layer.get_usage_stats()
