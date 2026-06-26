from __future__ import annotations

import time
import logging
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from ..interface import SpiritInterface

logger = logging.getLogger(__name__)


@dataclass
class HealthIssue:
    category: str = ""
    severity: str = "info"
    description: str = ""
    affected_ids: list[str] = field(default_factory=list)
    suggestion: str = ""
    auto_fixable: bool = False

    def to_dict(self) -> dict:
        return {
            'category': self.category,
            'severity': self.severity,
            'description': self.description,
            'affected_ids': self.affected_ids[:10],
            'suggestion': self.suggestion,
            'auto_fixable': self.auto_fixable,
        }


@dataclass
class HealthReport:
    overall_status: str = "healthy"
    score: float = 1.0
    issues: list[HealthIssue] = field(default_factory=list)
    checked_at: int = 0
    fix_results: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'overall_status': self.overall_status,
            'score': round(self.score, 2),
            'issue_count': len(self.issues),
            'issues': [i.to_dict() for i in self.issues],
            'checked_at': self.checked_at,
            'fix_results': self.fix_results,
        }


class HealthChecker:
    """Health checker for the memory system.

    Checks for:
    - Contradictions (numeric/entity conflicts)
    - Fragmentation (too many small memories on same topic)
    - Stale memories (not accessed in 30+ days)
    - Low quality memories (quality_score < 0.3)
    - Knowledge gaps (topics with very few memories)
    """

    STALE_DAYS = 30
    LOW_QUALITY_THRESHOLD = 0.3
    FRAGMENTATION_THRESHOLD = 5
    KNOWLEDGE_GAP_THRESHOLD = 3

    def __init__(self, interface: SpiritInterface, llm_layer=None):
        self.interface = interface
        self.llm_layer = llm_layer

    def check(self, fix: bool = False) -> HealthReport:
        report = HealthReport(checked_at=int(time.time()))

        # 委托给 MaintainEngine.diagnose() 统一诊断
        maintain = self.interface._maintain_engine
        if maintain:
            try:
                diag = maintain.diagnose()
                # 矛盾
                for c in diag.get("contradictions", [])[:10]:
                    report.issues.append(HealthIssue(
                        category='contradiction',
                        severity='warning',
                        description=f"矛盾记忆: {c.get('memory_a', '')} vs {c.get('memory_b', '')}",
                        affected_ids=[c.get('memory_a', ''), c.get('memory_b', '')],
                        suggestion="建议合并或标记旧记忆为 superseded",
                        auto_fixable=True,
                    ))
                # 碎片化
                for frag in diag.get("fragmentation", []):
                    report.issues.append(HealthIssue(
                        category='fragmentation',
                        severity='info',
                        description=f"主题 '{frag['topic']}' 有 {frag['count']} 条碎片化短记忆",
                        affected_ids=frag.get("ids", [])[:10],
                        suggestion="建议合并这些碎片记忆为一条完整记忆",
                        auto_fixable=True,
                    ))
                # 闲置
                stale = diag.get("stale", {})
                if stale.get("count", 0) > 0:
                    report.issues.append(HealthIssue(
                        category='stale',
                        severity='info',
                        description=f"发现 {stale['count']} 条超过 30 天的闲置记忆",
                        affected_ids=stale.get("ids", [])[:10],
                        suggestion="建议对这些记忆进行衰减处理或归档",
                        auto_fixable=True,
                    ))
                # 低质量
                for lq in diag.get("low_quality", []):
                    report.issues.append(HealthIssue(
                        category='low_quality',
                        severity='info',
                        description=f"低质量记忆: {lq.get('content', '')}",
                        affected_ids=[lq.get("memory_id", "")],
                        suggestion="建议清理或增强这些记忆的内容",
                        auto_fixable=False,
                    ))
                # 知识缺口
                gaps = diag.get("knowledge_gaps", [])
                if gaps:
                    gap_names = ", ".join(f"'{g['topic']}'({g['count']})" for g in gaps)
                    report.issues.append(HealthIssue(
                        category='knowledge_gap',
                        severity='info',
                        description=f"发现 {len(gaps)} 个知识薄弱主题: {gap_names}",
                        affected_ids=[],
                        suggestion="建议补充这些领域的知识",
                        auto_fixable=False,
                    ))
            except Exception as e:
                logger.warning("HealthChecker: diagnose failed, falling back to local checks: %s", e)
                # 回退到本地检查
                report.issues.extend(self._check_contradictions())
                report.issues.extend(self._check_fragmentation())
                report.issues.extend(self._check_stale_memories())
                report.issues.extend(self._check_low_quality())
                report.issues.extend(self._check_knowledge_gaps())
        else:
            # 无 MaintainEngine，使用本地检查（一次查询，共享数据）
            all_memories = None
            store = self.interface._store
            if store is not None:
                try:
                    all_memories = store.query(limit=5000)
                except Exception as e:
                    logger.debug("HealthChecker: failed to query store: %s", e)
            report.issues.extend(self._check_contradictions())
            report.issues.extend(self._check_fragmentation(all_memories))
            report.issues.extend(self._check_stale_memories(all_memories))
            report.issues.extend(self._check_low_quality(all_memories))
            report.issues.extend(self._check_knowledge_gaps(all_memories))

        severity_scores = {'critical': 0.0, 'warning': 0.3, 'info': 0.8}
        if report.issues:
            min_severity = min(
                severity_scores.get(i.severity, 0.5) for i in report.issues
            )
            report.score = min_severity
            if min_severity < 0.3:
                report.overall_status = 'critical'
            elif min_severity < 0.8:
                report.overall_status = 'warning'
            else:
                report.overall_status = 'healthy_with_notes'
        else:
            report.score = 1.0
            report.overall_status = 'healthy'

        if fix:
            report.fix_results = self._auto_fix(report.issues)

        return report

    def _check_contradictions(self) -> list[HealthIssue]:
        issues = []
        store = self.interface._store
        if store is None:
            return issues

        try:
            maintain = self.interface._maintain_engine
            if maintain and maintain.healing:
                contradictions = maintain.healing.detect_contradictions()
                for c in contradictions[:10]:
                    issues.append(HealthIssue(
                        category='contradiction',
                        severity='warning',
                        description=f"矛盾记忆: {c.get('memory_a', '')} vs {c.get('memory_b', '')}",
                        affected_ids=[c.get('memory_a', ''), c.get('memory_b', '')],
                        suggestion="建议合并或标记旧记忆为 superseded",
                        auto_fixable=True,
                    ))
        except Exception as e:
            logger.debug("HealthChecker.contradictions: %s", e)

        return issues

    def _check_fragmentation(self, all_memories=None) -> list[HealthIssue]:
        issues = []
        store = self.interface._store
        if store is None:
            return issues

        try:
            memories = all_memories if all_memories is not None else store.query(limit=5000)
            topic_groups: dict[str, list[dict]] = {}
            for mem in memories:
                for t in mem.get('topics', []):
                    code = t.get('code', '') if isinstance(t, dict) else str(t)
                    if code:
                        root = code.split('.')[0]
                        topic_groups.setdefault(root, []).append(mem)

            for topic, group in topic_groups.items():
                short_mems = [m for m in group if len(m.get('content', '')) < 30]
                if len(short_mems) >= self.FRAGMENTATION_THRESHOLD:
                    issues.append(HealthIssue(
                        category='fragmentation',
                        severity='info',
                        description=f"主题 '{topic}' 有 {len(short_mems)} 条碎片化短记忆",
                        affected_ids=[m.get('memory_id', '') for m in short_mems[:10]],
                        suggestion="建议合并这些碎片记忆为一条完整记忆",
                        auto_fixable=True,
                    ))
        except Exception as e:
            logger.debug("HealthChecker.fragmentation: %s", e)

        return issues

    def _check_stale_memories(self, all_memories=None) -> list[HealthIssue]:
        issues = []
        store = self.interface._store
        if store is None:
            return issues

        try:
            now = int(time.time())
            stale_threshold = now - self.STALE_DAYS * 86400

            memories = all_memories if all_memories is not None else store.query(limit=5000)
            stale = [
                m for m in memories
                if m.get('time_ts', now) < stale_threshold
                and m.get('importance', 'medium') != 'high'
                and m.get('lifecycle_state', 'active') == 'active'
            ]

            if stale:
                issues.append(HealthIssue(
                    category='stale',
                    severity='info',
                    description=f"发现 {len(stale)} 条超过 {self.STALE_DAYS} 天的闲置记忆",
                    affected_ids=[m.get('memory_id', '') for m in stale[:10]],
                    suggestion="建议对这些记忆进行衰减处理或归档",
                    auto_fixable=True,
                ))
        except Exception as e:
            logger.debug("HealthChecker.stale: %s", e)

        return issues

    def _check_low_quality(self, all_memories=None) -> list[HealthIssue]:
        issues = []
        store = self.interface._store
        if store is None:
            return issues

        try:
            memories = all_memories if all_memories is not None else store.query(limit=5000)
            low_quality = [
                m for m in memories
                if m.get('_quality_score', 1.0) < self.LOW_QUALITY_THRESHOLD
                or (m.get('importance') == 'low' and len(m.get('content', '')) < 10)
            ]

            if low_quality:
                issues.append(HealthIssue(
                    category='low_quality',
                    severity='info',
                    description=f"发现 {len(low_quality)} 条低质量记忆",
                    affected_ids=[m.get('memory_id', '') for m in low_quality[:10]],
                    suggestion="建议清理或增强这些记忆的内容",
                    auto_fixable=False,
                ))
        except Exception as e:
            logger.debug("HealthChecker.low_quality: %s", e)

        return issues

    def _check_knowledge_gaps(self, all_memories=None) -> list[HealthIssue]:
        issues = []
        store = self.interface._store
        if store is None:
            return issues

        try:
            memories = all_memories if all_memories is not None else store.query(limit=5000)
            topic_counts: dict[str, int] = {}
            for mem in memories:
                for t in mem.get('topics', []):
                    code = t.get('code', '') if isinstance(t, dict) else str(t)
                    if code:
                        root = code.split('.')[0]
                        topic_counts[root] = topic_counts.get(root, 0) + 1

            gap_topics = {
                topic: count for topic, count in topic_counts.items()
                if count < self.KNOWLEDGE_GAP_THRESHOLD
            }

            if gap_topics:
                gap_names = ", ".join(f"'{t}'({c})" for t, c in sorted(gap_topics.items(), key=lambda x: x[1]))
                issues.append(HealthIssue(
                    category='knowledge_gap',
                    severity='info',
                    description=f"发现 {len(gap_topics)} 个知识薄弱主题: {gap_names}",
                    affected_ids=[],
                    suggestion="建议补充这些领域的知识",
                    auto_fixable=False,
                ))
        except Exception as e:
            logger.debug("HealthChecker.knowledge_gaps: %s", e)

        return issues

    def _auto_fix(self, issues: list[HealthIssue]) -> list[dict]:
        results = []

        fixable = [i for i in issues if i.auto_fixable]
        if not fixable:
            return results

        for issue in fixable:
            try:
                if issue.category == 'contradiction':
                    result = self._fix_contradictions(issue)
                    results.append(result)
                elif issue.category == 'fragmentation':
                    result = self._fix_fragmentation(issue)
                    results.append(result)
                elif issue.category == 'stale':
                    result = self._fix_stale(issue)
                    results.append(result)
            except Exception as e:
                results.append({
                    'category': issue.category,
                    'status': 'error',
                    'error': str(e),
                })

        return results

    def _fix_contradictions(self, issue: HealthIssue) -> dict:
        maintain = self.interface._maintain_engine
        if not maintain:
            return {'category': 'contradiction', 'status': 'skipped', 'reason': 'no maintain engine'}

        try:
            result = maintain.maintain(operations=['heal'], dry_run=False)
            return {
                'category': 'contradiction',
                'status': 'fixed',
                'superseded': result.get('heal', {}).get('superseded', 0),
            }
        except Exception as e:
            return {'category': 'contradiction', 'status': 'error', 'error': str(e)}

    def _fix_fragmentation(self, issue: HealthIssue) -> dict:
        maintain = self.interface._maintain_engine
        if not maintain:
            return {'category': 'fragmentation', 'status': 'skipped', 'reason': 'no maintain engine'}

        try:
            result = maintain.maintain(operations=['consolidate'], dry_run=False)
            return {
                'category': 'fragmentation',
                'status': 'fixed',
                'merged': result.get('consolidate', {}).get('total_merged', 0),
            }
        except Exception as e:
            return {'category': 'fragmentation', 'status': 'error', 'error': str(e)}

    def _fix_stale(self, issue: HealthIssue) -> dict:
        maintain = self.interface._maintain_engine
        if not maintain:
            return {'category': 'stale', 'status': 'skipped', 'reason': 'no maintain engine'}

        try:
            result = maintain.maintain(operations=['decay'], dry_run=False)
            return {
                'category': 'stale',
                'status': 'fixed',
                'archived': result.get('decay', {}).get('archived', 0),
            }
        except Exception as e:
            return {'category': 'stale', 'status': 'error', 'error': str(e)}
