"""Agent Memory CLI — command-line interface for agent memory management."""

from __future__ import annotations

import sys
import os
import sqlite3
import argparse

# 抑制库级别的 logger 输出，避免污染 CLI JSON 输出
from agent_memory.logging_config import configure_cli_logging
configure_cli_logging()

# ── Import all command handlers from sub-modules ──────────

from agent_memory.cli._core import (
    cmd_init,
    cmd_remember,
    cmd_recall,
    cmd_context,
    cmd_stats,
    cmd_maintain,
    cmd_compress,
    cmd_graph,
    cmd_feedback,
    cmd_feedback_v2,
    cmd_learn,
    cmd_forget,
    cmd_restore,
    cmd_purge_deleted,
    cmd_flush,
    cmd_heal,
    cmd_sync,
    cmd_auto_context,
    cmd_export,
    cmd_conflicts,
    cmd_notifications,
    cmd_reactor_scan,
    cmd_batch_remember,
    cmd_echo,
    cmd_bookmark,
    cmd_bookmarks,
    cmd_milestones,
)

from agent_memory.cli._knowledge import (
    cmd_entities,
    cmd_topic_summaries,
    cmd_encyclopedia,
    cmd_doc,
    cmd_distill,
    cmd_distill_stats,
)

from agent_memory.cli._temporal import (
    cmd_snapshot,
    cmd_snapshots,
    cmd_diff,
    cmd_blame,
    cmd_timeline_stats,
)

from agent_memory.cli._identity import (
    cmd_whoami,
    cmd_identity,
    cmd_narrative,
    cmd_worldview,
    cmd_self_concept,
    cmd_self,
    cmd_mood,
    cmd_gaps,
    cmd_curious,
    cmd_confidence,
    cmd_reflect,
    cmd_uncertainty,
)

from agent_memory.cli._recall import (
    cmd_meta_recall,
    cmd_evaluate,
    cmd_traces,
    cmd_trace_detail,
    cmd_trace_log,
    cmd_awareness,
)

from agent_memory.cli._persona import (
    cmd_persona,
    cmd_persona_get,
    cmd_roles,
    cmd_role_get,
    cmd_role_apply,
    cmd_role_create,
    cmd_role_delete,
    cmd_role_from_media,
    cmd_personality,
)

from agent_memory.cli._spirit import (
    cmd_spirit,
    cmd_daily_report,
    cmd_weekly_report,
    cmd_health,
)

from agent_memory.cli._system import (
    cmd_curiosity_dispatch,
    cmd_validate,
    cmd_validate_all,
    cmd_model_server,
    cmd_update,
    cmd_versions,
)

from agent_memory.cli._growth import (
    cmd_annual_report,
    cmd_achievements,
    cmd_growth_feedback,
    cmd_share_card,
)

from agent_memory.cli._distributed import (
    cmd_sync_peers,
    cmd_sync_with,
    cmd_sync_all,
    cmd_sync_checkpoint,
    cmd_sync_stats,
    cmd_federation,
)

from agent_memory.cli._utils import _check_model_server


def _cmd_serve():
    """启动统一 API 服务器"""
    from agent_memory.unified_api import main as serve_main
    serve_main()


def _cmd_repl():
    """启动交互式 REPL"""
    from agent_memory.cli._repl import start_repl
    start_repl()


def main():
    parser = argparse.ArgumentParser(description="Agent Memory CLI")
    parser.add_argument("--trace", action="store_true", help="启用详细追踪日志（JSON Lines 格式）")
    parser.add_argument("--trace-module", default=None, help="只追踪指定模块（recall/maintain/metacognition）")
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", help="首次运行引导 — 初始化记忆系统")

    # remember
    p = sub.add_parser("remember", help="写入记忆")
    p.add_argument("content", help="记忆内容")
    p.add_argument("--importance", "-i", default=None, help="high/medium/low")
    p.add_argument("--topics", "-t", default=None, help="主题列表（逗号分隔）")
    p.add_argument("--nature", "-n", default=None, help="性质 code")
    p.add_argument("--force", "-f", action="store_true", help="跳过过滤")
    p.add_argument("--review", action="store_true", help="审核模式：预览内容但不写入，需确认后再写入")

    # recall
    p = sub.add_parser("recall", help="检索记忆")
    p.add_argument("query", help="查询内容")
    p.add_argument("--topic", default=None, help="主题过滤")
    p.add_argument("--importance", default=None, help="重要度过滤")
    p.add_argument("--significance", default=None,
                    choices=["trivial", "notable", "important", "breakthrough", "crisis", "milestone"],
                    help="情感显著性过滤")
    p.add_argument("--limit", type=int, default=10, help="返回条数")

    # context
    p = sub.add_parser("context", help="组装上下文")
    p.add_argument("query", help="当前对话内容")
    p.add_argument("--max-tokens", type=int, default=1500, help="token 预算")
    p.add_argument("--style", default="structured", help="structured/narrative/compact/xml")

    # stats
    sub.add_parser("stats", help="查看统计")

    # maintain
    sub.add_parser("maintain", help="执行维护")

    # compress
    p = sub.add_parser("compress", help="压缩记忆")
    p.add_argument("--topic", default=None, help="指定主题")
    p.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")
    p.add_argument("--force", "-f", action="store_true", help="强制压缩")

    # graph
    p = sub.add_parser("graph", help="生成图谱")
    p.add_argument("--topic", default=None, help="指定主题")
    p.add_argument("--format", default="ascii", help="mermaid/dot/json/ascii")

    # feedback
    p = sub.add_parser("feedback", help="记录反馈")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("--useful", action="store_true", help="有用")
    p.add_argument("--not-useful", action="store_true", help="没用")
    p.add_argument("--note", default=None, help="备注")

    # feedback-v2 (FeedbackLearner)
    p = sub.add_parser("feedback-v2", help="记录反馈 v2（持续学习）")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("feedback_type", choices=["helpful", "unhelpful", "corrected", "ignored"], help="反馈类型")
    p.add_argument("--correction-id", default=None, help="修正记忆 ID（corrected 时使用）")
    p.add_argument("--query", default=None, help="关联查询")

    # learn
    p = sub.add_parser("learn", help="应用反馈学习（调整质量/重要度）")
    p.add_argument("--dry-run", action="store_true", help="仅分析不写入")

    # forget
    p = sub.add_parser("forget", help="删除单条记忆（含关联和向量清理）")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("--reason", default=None, help="删除原因")
    p.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")
    p.add_argument("--permanent", action="store_true", help="永久删除（硬删除，不可恢复）")

    # restore
    p = sub.add_parser("restore", help="恢复软删除的记忆")
    p.add_argument("memory_id", help="记忆 ID")

    # purge-deleted
    p = sub.add_parser("purge-deleted", help="永久清理软删除的记忆")
    p.add_argument("--older-than-days", type=int, default=30, help="清理多少天前的软删除记录（默认 30 天）")
    p.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")

    # flush
    sub.add_parser("flush", help="L1→L2 沉淀")

    # heal
    sub.add_parser("heal", help="自我修复")

    # sync
    p = sub.add_parser("sync", help="从 MEMORY.md 同步记忆")
    p.add_argument("source", help="源文件路径（如 MEMORY.md）")
    p.add_argument("--force", "-f", action="store_true", help="跳过过滤强制写入")

    # auto-context
    p = sub.add_parser("auto-context", help="自动组装上下文（智能检索+摘要）")
    p.add_argument("query", help="当前对话内容")
    p.add_argument("--max-tokens", type=int, default=1500, help="token 预算")
    p.add_argument("--style", default="structured", help="structured/narrative/compact/xml")

    # export
    p = sub.add_parser("export", help="导出为 Markdown")
    p.add_argument("--output", "-o", default="memories_export.md", help="输出文件路径")
    p.add_argument("--topic", default=None, help="按主题过滤")
    p.add_argument("--importance", default=None, help="按重要度过滤")
    p.add_argument("--limit", type=int, default=1000, help="最多导出条数")

    # conflicts
    p = sub.add_parser("conflicts", help="检测记忆冲突")
    p.add_argument("--hours", type=int, default=168, help="检查时间窗口（小时）")
    p.add_argument("--limit", type=int, default=100, help="最大扫描记忆数（默认 100，O(n²) 复杂度）")

    sub.add_parser("notifications", help="查看待处理的主动通知")
    sub.add_parser("reactor-scan", help="手动触发 reactor 全量扫描")

    # v5.3: 蒸馏命令
    p = sub.add_parser("distill", help="执行记忆蒸馏（对话碎片→知识库）")
    p.add_argument("--force", action="store_true", help="强制全量重新蒸馏")

    sub.add_parser("distill-stats", help="查看蒸馏系统统计")

    p = sub.add_parser("encyclopedia", help="查看个人百科")
    p.add_argument("--category", type=str, default=None,
                   help="按类别过滤 (decisions/tools/projects/concepts/people/facts)")
    p.add_argument("--search", type=str, default=None, help="搜索百科条目")
    p.add_argument("--export", type=str, default=None, help="导出百科到文件")

    p = sub.add_parser("entities", help="查看知识实体")
    p.add_argument("--type", type=str, default=None, help="按类型过滤")
    p.add_argument("--name", type=str, default=None, help="按名称搜索")

    p = sub.add_parser("topic-summaries", help="查看主题摘要")
    p.add_argument("--topic", type=str, default=None, help="按主题过滤")

    # v5.4: 时间旅行命令
    p = sub.add_parser("snapshot", help="创建记忆快照（保存某一时刻的认知状态）")
    p.add_argument("--label", "-l", default=None, help="快照标签（默认: 当前日期）")
    p.add_argument("--at", default=None, help="快照时间点（支持: YYYY-MM-DD, 7d, 1m, today, yesterday）")
    p.add_argument("--description", "-d", default=None, help="描述")

    p = sub.add_parser("snapshots", help="列出所有快照")
    p.add_argument("--limit", type=int, default=20, help="显示数量")

    p = sub.add_parser("diff", help="对比两个时间点的记忆差异（这段时间学到了什么）")
    p.add_argument("from_date", help="起始时间（YYYY-MM-DD / 7d / 1m / today / yesterday）")
    p.add_argument("to_date", nargs="?", default="today", help="结束时间（默认: today）")
    p.add_argument("--topic", default=None, help="按主题过滤")
    p.add_argument("--from-snapshot", default=None, help="起始快照 ID")
    p.add_argument("--to-snapshot", default=None, help="结束快照 ID")
    p.add_argument("--natural", "-n", action="store_true", help="自然语言输出")

    p = sub.add_parser("blame", help="追溯记忆来源（这条记忆是怎么来的）")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("--natural", "-n", action="store_true", help="自然语言输出")

    sub.add_parser("timeline-stats", help="时间旅行系统统计")

    # Phase 2: 自我指涉命令
    p = sub.add_parser("traces", help="查看推理追踪历史")
    p.add_argument("--limit", type=int, default=20, help="显示数量")
    p.add_argument("--topic", default=None, help="按查询内容过滤")

    p = sub.add_parser("trace-detail", help="查看单次推理的详细步骤")
    p.add_argument("trace_id", help="追踪 ID")

    p = sub.add_parser("trace-log", help="查看结构化追踪日志（--trace 启用）")
    p.add_argument("--module", default=None, help="按模块过滤（recall/maintain/metacognition）")
    p.add_argument("--limit", type=int, default=50, help="显示数量")
    p.add_argument("--clear", action="store_true", help="清空追踪日志")

    p = sub.add_parser("confidence", help="查看置信度历史/概览")
    p.add_argument("--topic", default=None, help="按主题过滤")
    p.add_argument("--limit", type=int, default=50, help="显示数量")
    p.add_argument("--overview", "-o", action="store_true", help="显示各主题置信度概览")

    p = sub.add_parser("reflect", help="查看自我反思历史")
    p.add_argument("--limit", type=int, default=20, help="显示数量")

    p = sub.add_parser("uncertainty", help="查看不确定因素模式分析")
    p.add_argument("--limit", type=int, default=100, help="分析范围")

    # Phase 3: 元认知命令
    p = sub.add_parser("meta-recall", help="带反思的检索（不确定时自动修正查询重试）")
    p.add_argument("query", help="查询内容")
    p.add_argument("--limit", type=int, default=10, help="返回条数")
    p.add_argument("--max-rounds", type=int, default=2, help="最大反思轮数")

    p = sub.add_parser("evaluate", help="评估检索结果质量（多维度分析）")
    p.add_argument("query", help="查询内容")

    # Phase 4: 内在动机命令
    p = sub.add_parser("mood", help="查看 Agent 当前内在状态")
    p.add_argument("--detail", "-d", action="store_true", help="显示详细分析（无聊度 + 知识空白）")

    sub.add_parser("gaps", help="查看知识空白")
    sub.add_parser("curious", help="查看好奇驱动的探索任务")

    # Phase 5: 叙事自我命令
    sub.add_parser("whoami", help="我是谁 — 第一人称自我叙述")

    p = sub.add_parser("identity", help="查看身份画像")
    p.add_argument("--raw", "-r", action="store_true", help="JSON 格式输出")

    p = sub.add_parser("narrative", help="构建叙事（时间线/主题）")
    p.add_argument("--topic", default=None, help="按主题构建叙事")
    p.add_argument("--from-date", default=None, help="起始日期 (YYYY-MM-DD)")
    p.add_argument("--to-date", default=None, help="结束日期")
    p.add_argument("--limit", type=int, default=50, help="最大记忆数")

    sub.add_parser("worldview", help="查看世界观（信念/价值观/原则）")
    sub.add_parser("self-concept", help="查看完整自我概念")

    # Phase 6: 数字孪生命令
    sub.add_parser("persona", help="构建数字孪生人格画像")
    sub.add_parser("persona-get", help="获取最新的数字孪生人格画像")

    # Phase 7: 个人风格 Agent 命令
    sub.add_parser("roles", help="列出所有可用的角色模板")

    p = sub.add_parser("role-get", help="获取特定角色模板")
    p.add_argument("role_id", help="角色 ID")

    p = sub.add_parser("role-apply", help="应用角色风格到个人人格")
    p.add_argument("role_id", help="角色 ID")
    p.add_argument("--weight", type=float, default=0.4, help="角色风格权重 (0-1)")

    p = sub.add_parser("role-create", help="创建新角色模板")
    p.add_argument("role_id", help="角色 ID")
    p.add_argument("--name", required=True, help="角色名称")
    p.add_argument("--prompt", required=True, help="提示词模板")
    p.add_argument("--traits", required=True, help="人格特质 JSON")
    p.add_argument("--speaking-style", default="", help="说话风格")
    p.add_argument("--topics", default="", help="主题偏好（逗号分隔）")
    p.add_argument("--emotional-tone", default="", help="情感基调")

    p = sub.add_parser("role-delete", help="删除角色模板")
    p.add_argument("role_id", help="角色 ID")
    p.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")

    p = sub.add_parser("role-from-media", help="从媒体文件创建角色模板")
    p.add_argument("file_path", help="媒体文件路径")
    p.add_argument("--name", required=True, help="角色名称")

    # Phase 6: 统一自我入口
    p = sub.add_parser("self", help="统一自我状态仪表盘")
    p.add_argument("--mood", action="store_true", help="仅显示内在状态")
    p.add_argument("--narrative", "-n", action="store_true", help="仅显示身份叙事")
    p.add_argument("--confidence", "-c", action="store_true", help="仅显示置信度概览")
    p.add_argument("--gaps", "-g", action="store_true", help="仅显示知识空白")
    p.add_argument("--recent-thinking", "-t", action="store_true", help="仅显示最近推理")

    # v6.0: 记忆版本化命令
    p = sub.add_parser("update", help="更新记忆内容（版本化，保留历史）")
    p.add_argument("memory_id", help="要更新的记忆 ID")
    p.add_argument("--content", "-c", required=True, help="新内容")
    p.add_argument("--reason", "-r", default=None, help="变更原因")
    p.add_argument("--importance", "-i", default=None, help="新重要度 (high/medium/low)")
    p.add_argument("--topics", "-t", default=None, help="新主题列表（逗号分隔）")

    p = sub.add_parser("versions", help="查看记忆的版本历史")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("--json", dest="as_json", action="store_true", help="JSON 输出")

    # 模型守护进程管理
    p = sub.add_parser("model-server", help="管理模型守护进程（避免冷启动）")
    p.add_argument("action", choices=["start", "stop", "status", "restart"], help="操作")

    # V9.2: 文档精读命令
    p = sub.add_parser("doc", help="文档精读（上传/检索/列表/回溯）")
    p.add_argument("doc_subcmd", choices=["upload", "search", "list", "locate"], help="子命令")
    p.add_argument("file_path", nargs="?", default=None, help="文件路径 (upload 子命令)")
    p.add_argument("--title", default=None, help="文档标题 (upload)")
    p.add_argument("--strategy", default="auto", choices=["auto", "structure", "fixed", "sentence"], help="分段策略 (upload)")
    p.add_argument("--importance", default="high", choices=["high", "medium", "low"], help="重要度 (upload)")
    p.add_argument("--query", default=None, help="查询内容 (search)")
    p.add_argument("--top-k", type=int, default=5, help="返回条数 (search)")
    p.add_argument("--expand-context", type=int, default=1, help="上下文展开段数 (search)")
    p.add_argument("--doc-id", default=None, help="限定文档 ID (search/list)")
    p.add_argument("--memory-id", default=None, help="记忆 ID (locate)")
    p.add_argument("--json", action="store_true", help="JSON 输出 (locate)")

    # V9.3: 人格分析命令
    p = sub.add_parser("personality", help="人格分析（分析/查看/版本/证据/删除）")
    p.add_argument("personality_subcmd", choices=["analyze", "show", "versions", "evidence", "delete"], help="子命令")
    p.add_argument("--text", default=None, help="聊天记录文本 (analyze)")
    p.add_argument("--file", default=None, help="聊天记录文件路径 (analyze)")
    p.add_argument("--self-name", default=None, help="自己的昵称 (analyze)")
    p.add_argument("--source-type", default="wechat_txt", help="数据源类型 (analyze)")
    p.add_argument("--privacy-level", default="team", choices=["private", "team", "public"], help="隐私级别 (analyze)")
    p.add_argument("--person-id", default="main", help="人格 ID (show/versions/evidence/delete)")
    p.add_argument("--access-level", default="team", help="访问级别 (show)")
    p.add_argument("--trait", default=None, help="特质名称过滤 (evidence)")

    # v10.0: Spirit 器灵/管家命令
    p = sub.add_parser("spirit", help="自然语言指令 — 通过 Spirit 管家解析并执行")
    p.add_argument("command", help="自然语言指令")

    p = sub.add_parser("daily-report", help="生成每日记忆报告")
    p.add_argument("--date", default=None, help="指定日期 (YYYY-MM-DD，默认今天)")

    sub.add_parser("weekly-report", help="生成每周记忆报告")

    p = sub.add_parser("health", help="运行健康检查")
    p.add_argument("--fix", action="store_true", help="自动修复可修复的问题")

    p = sub.add_parser("awareness", help="查询知识感知度（系统对某主题的认知状况）")
    p.add_argument("topic", help="查询主题")

    # Level 6.0: Curiosity Engine 命令
    p = sub.add_parser("curiosity", help="好奇心引擎（探索知识空白）")
    p.add_argument("curiosity_subcmd", choices=["targets", "suggestions", "explore"], help="子命令")
    p.add_argument("topic", nargs="?", default=None, help="探索主题 (explore)")
    p.add_argument("--limit", type=int, default=10, help="返回数量 (targets/suggestions)")

    # Level 6.0: Knowledge Validation 命令
    p = sub.add_parser("validate", help="验证单条记忆（交叉引用、时效性、置信度衰减）")
    p.add_argument("memory_id", help="记忆 ID")

    p = sub.add_parser("validate-all", help="验证所有记忆并输出摘要")
    p.add_argument("--limit", type=int, default=100, help="最大验证数量")

    # Batch remember
    p = sub.add_parser("batch-remember", help="批量写入记忆（高性能单事务模式）")
    p.add_argument("file", help="JSON 文件路径（内容为记忆数组）")

    # echo — 主动推荐
    p = sub.add_parser("echo", help="主动推荐相关记忆")
    p.add_argument("context", nargs="?", default="", help="当前上下文")
    p.add_argument("--limit", type=int, default=3, help="推荐数量")

    # bookmark — 收藏记忆
    p = sub.add_parser("bookmark", help="收藏一条记忆")
    p.add_argument("memory_id", help="记忆 ID")

    # bookmarks — 查看收藏
    p = sub.add_parser("bookmarks", help="查看所有收藏的记忆")
    p.add_argument("--limit", type=int, default=20, help="返回数量")

    # milestones — 查看成就
    sub.add_parser("milestones", help="查看成就和解锁状态")

    # v10.1: 联邦知识命令
    p = sub.add_parser("federation", help="跨 Agent 知识联邦")
    p.add_argument("federation_subcmd", choices=["peers", "search", "conflicts", "resolve"], help="子命令")
    p.add_argument("--query", default=None, help="查询内容 (search)")
    p.add_argument("--topics", default=None, help="主题过滤，逗号分隔 (search)")
    p.add_argument("--max-per-peer", type=int, default=5, help="每个对等 Agent 最多返回条数 (search)")
    p.add_argument("--limit", type=int, default=20, help="总返回条数 (search)")
    p.add_argument("--topic", default=None, help="冲突主题过滤 (conflicts) / 冲突主题 (resolve)")
    p.add_argument("--agent-a", default=None, help="Agent A ID (resolve)")
    p.add_argument("--agent-a-claim", default="", help="Agent A 观点 (resolve)")
    p.add_argument("--agent-b", default=None, help="Agent B ID (resolve)")
    p.add_argument("--agent-b-claim", default="", help="Agent B 观点 (resolve)")
    p.add_argument("--strategy", default="higher_confidence",
                   choices=["higher_confidence", "newer_wins", "merged", "both_kept"],
                   help="冲突解决策略 (resolve)")

    # v6.0 Phase 4: 分布式一致性同步命令
    sub.add_parser("sync-peers", help="列出所有同步对等节点")

    p = sub.add_parser("sync-with", help="与指定对等节点同步")
    p.add_argument("peer_id", help="对等节点 ID")

    sub.add_parser("sync-all", help="与所有对等节点同步")
    sub.add_parser("sync-checkpoint", help="创建同步检查点")
    sub.add_parser("sync-stats", help="查看同步引擎统计")

    # Growth & Gamification 命令
    p = sub.add_parser("annual-report", help="生成记忆年报（Spotify Wrapped 风格）")
    p.add_argument("--year", type=int, default=None, help="年份（默认: 今年）")
    p.add_argument("--html", action="store_true", help="生成 HTML 报告")
    p.add_argument("--share-card", action="store_true", help="生成分享卡片")
    p.add_argument("--output", "-o", default=None, help="输出文件路径")

    p = sub.add_parser("achievements", help="查看成就徽章")
    p.add_argument("--check", action="store_true", help="检查并解锁新成就")

    p = sub.add_parser("growth-feedback", help="提交检索反馈（影响未来检索排序）")
    p.add_argument("memory_id", help="记忆 ID")
    p.add_argument("--useful", action="store_true", help="标记为有用")
    p.add_argument("--not-useful", action="store_true", help="标记为没用")
    p.add_argument("--query", default=None, help="关联的查询文本")
    p.add_argument("--stats", action="store_true", help="同时显示反馈统计")

    p = sub.add_parser("share-card", help="生成可分享的洞察卡片")
    p.add_argument("--query", default=None, help="生成检索结果分享卡片")
    p.add_argument("--output", "-o", default=None, help="输出文件路径")

    # Unified API server
    sub.add_parser("serve", help="启动统一 API 服务器（REST API + Playground + 健康检查）")

    # Interactive REPL
    sub.add_parser("repl", help="启动交互式命令行")

    args = parser.parse_args()

    # 启用追踪日志
    if args.trace:
        from trace_logger import get_tracer, enable_tracing
        tracer = get_tracer()
        tracer.enable(True)
        if args.trace_module:
            tracer.set_module_filter(*args.trace_module.split(","))
        print(f"[TRACE] 追踪已启用 (module_filter={args.trace_module or 'all'})", file=sys.stderr)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "init": cmd_init,
        "remember": cmd_remember,
        "recall": cmd_recall,
        "context": cmd_context,
        "stats": cmd_stats,
        "maintain": cmd_maintain,
        "compress": cmd_compress,
        "graph": cmd_graph,
        "feedback": cmd_feedback,
        "feedback-v2": cmd_feedback_v2,
        "learn": cmd_learn,
        "forget": cmd_forget,
        "restore": cmd_restore,
        "purge-deleted": cmd_purge_deleted,
        "flush": cmd_flush,
        "heal": cmd_heal,
        "sync": cmd_sync,
        "auto-context": cmd_auto_context,
        "export": cmd_export,
        "conflicts": cmd_conflicts,
        "notifications": cmd_notifications,
        "reactor-scan": cmd_reactor_scan,
        "distill": cmd_distill,
        "distill-stats": cmd_distill_stats,
        "encyclopedia": cmd_encyclopedia,
        "entities": cmd_entities,
        "topic-summaries": cmd_topic_summaries,
        # 时间旅行
        "snapshot": cmd_snapshot,
        "snapshots": cmd_snapshots,
        "diff": cmd_diff,
        "blame": cmd_blame,
        "timeline-stats": cmd_timeline_stats,
        "update": cmd_update,
        "versions": cmd_versions,
        "model-server": cmd_model_server,
        # Phase 2: 自我指涉
        "traces": cmd_traces,
        "trace-detail": cmd_trace_detail,
        "trace-log": cmd_trace_log,
        "confidence": cmd_confidence,
        "reflect": cmd_reflect,
        "uncertainty": cmd_uncertainty,
        # Phase 3: 元认知
        "meta-recall": cmd_meta_recall,
        "evaluate": cmd_evaluate,
        # Phase 4: 内在动机
        "mood": cmd_mood,
        "gaps": cmd_gaps,
        "curious": cmd_curious,
        # Phase 5: 叙事自我
        "whoami": cmd_whoami,
        "identity": cmd_identity,
        "narrative": cmd_narrative,
        "worldview": cmd_worldview,
        "self-concept": cmd_self_concept,
        # Phase 6: 数字孪生
        "persona": cmd_persona,
        "persona-get": cmd_persona_get,
        # Phase 7: 个人风格 Agent
        "roles": cmd_roles,
        "role-get": cmd_role_get,
        "role-apply": cmd_role_apply,
        "role-create": cmd_role_create,
        "role-delete": cmd_role_delete,
        "role-from-media": cmd_role_from_media,
        # Phase 6: 统一自我
        "self": cmd_self,
        # V9.2: 文档精读
        "doc": cmd_doc,
        # V9.3: 人格分析
        "personality": cmd_personality,
        # v10.0: Spirit 器灵/管家
        "spirit": cmd_spirit,
        "daily-report": cmd_daily_report,
        "weekly-report": cmd_weekly_report,
        "health": cmd_health,
        "awareness": cmd_awareness,
        # v10.1: 联邦知识
        "federation": cmd_federation,
        # Level 6.0: Curiosity Engine
        "curiosity": cmd_curiosity_dispatch,
        # Level 6.0: Knowledge Validation
        "validate": cmd_validate,
        "validate-all": cmd_validate_all,
        # Batch remember
        "batch-remember": cmd_batch_remember,
        # echo / bookmark / bookmarks / milestones
        "echo": cmd_echo,
        "bookmark": cmd_bookmark,
        "bookmarks": cmd_bookmarks,
        "milestones": cmd_milestones,
        # v6.0 Phase 4: 分布式一致性同步
        "sync-peers": cmd_sync_peers,
        "sync-with": cmd_sync_with,
        "sync-all": cmd_sync_all,
        "sync-checkpoint": cmd_sync_checkpoint,
        "sync-stats": cmd_sync_stats,
        # Growth & Gamification
        "annual-report": cmd_annual_report,
        "achievements": cmd_achievements,
        "growth-feedback": cmd_growth_feedback,
        "share-card": cmd_share_card,
        # Unified API server
        "serve": lambda args: _cmd_serve(),
        # Interactive REPL
        "repl": lambda args: _cmd_repl(),
    }

    # 检测 model_server 状态（仅涉及模型的命令才检查）
    _MODEL_COMMANDS = {"remember", "recall", "context", "auto-context", "maintain", "distill", "sync"}
    if args.command in _MODEL_COMMANDS:
        _check_model_server()

    handler = handlers.get(args.command)
    if handler:
        try:
            handler(args)
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                print("❌ 系统繁忙：数据库正在被其他操作占用，请稍后重试")
            else:
                print(f"❌ 数据库错误：{e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
