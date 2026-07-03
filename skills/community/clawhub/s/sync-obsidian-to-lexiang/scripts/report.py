"""
report.py - 同步报告生成器

每次同步完成后生成 Markdown 格式的报告文件，便于人工审计核对。
存储位置: {vault}/.obsidian/plugins/sync-obsidian-to-lexiang/reports/
命名规则: sync_report_YYYYMMDD_HHMMSS.md
自动保留最近 10 份报告，清理更早的。
"""

import glob
import os
from datetime import datetime, timezone
from typing import List, Optional

from manifest import get_plugin_dir, ensure_plugin_dir

REPORTS_DIR = "reports"
MAX_REPORTS = 10


def get_reports_dir(vault_path: str) -> str:
    """获取报告目录路径"""
    return os.path.join(get_plugin_dir(vault_path), REPORTS_DIR)


def ensure_reports_dir(vault_path: str) -> str:
    """确保报告目录存在"""
    reports_dir = get_reports_dir(vault_path)
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def generate_report_filename() -> str:
    """生成报告文件名"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"sync_report_{ts}.md"


def cleanup_old_reports(vault_path: str, keep: int = MAX_REPORTS) -> List[str]:
    """清理旧报告，保留最近 keep 份"""
    reports_dir = get_reports_dir(vault_path)
    if not os.path.isdir(reports_dir):
        return []

    pattern = os.path.join(reports_dir, "sync_report_*.md")
    files = sorted(glob.glob(pattern))

    removed = []
    if len(files) > keep:
        to_remove = files[: len(files) - keep]
        for f in to_remove:
            os.remove(f)
            removed.append(f)
    return removed


class SyncReport:
    """同步报告构建器"""

    def __init__(
        self,
        mode: str,
        vault_path: str,
        target_space_id: str,
        target_folder_id: str = "",
        conflict_strategy: str = "",
        dry_run: bool = False,
    ):
        self.mode = mode
        self.vault_path = vault_path
        self.target_space_id = target_space_id
        self.target_folder_id = target_folder_id
        self.conflict_strategy = conflict_strategy
        self.dry_run = dry_run
        self.start_time = datetime.now(timezone.utc).astimezone()
        self.end_time: Optional[datetime] = None

        # 操作记录
        self.actions: List[dict] = []
        # 错误回调：record_action 记录 error 时触发 on_error(rel_path, detail)
        self.on_error = None
        # 统计
        self.stats = {
            "folders_created": 0,
            "pages_created": 0,
            "pages_updated": 0,
            "files_created": 0,
            "pages_skipped_no_change": 0,
            "pages_skipped_conflict": 0,
            "attachments_uploaded": 0,
            "errors": 0,
            "source_deleted_ignored": 0,
        }

    def record_action(
        self,
        action: str,
        rel_path: str,
        status: str = "success",
        entry_id: str = "",
        detail: str = "",
    ):
        """记录一条操作"""
        record = {
            "action": action,
            "rel_path": rel_path,
            "status": status,
            "entry_id": entry_id,
            "detail": detail,
            "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        }
        self.actions.append(record)

        # 更新统计
        if status == "error":
            self.stats["errors"] += 1
            if self.on_error:
                try:
                    self.on_error(rel_path, detail)
                except Exception:
                    pass
        elif status == "skipped_no_change":
            self.stats["pages_skipped_no_change"] += 1
        elif status == "skipped_conflict":
            self.stats["pages_skipped_conflict"] += 1
        elif status == "success":
            if action == "create_folder":
                self.stats["folders_created"] += 1
            elif action == "create_page":
                self.stats["pages_created"] += 1
            elif action == "update_page":
                self.stats["pages_updated"] += 1
            elif action == "create_file":
                self.stats["files_created"] += 1
            elif action == "upload_attachment":
                self.stats["attachments_uploaded"] += 1

    def set_source_deleted_ignored(self, count: int):
        """设置源端删除忽略数"""
        self.stats["source_deleted_ignored"] = count

    def finish(self):
        """标记同步完成"""
        self.end_time = datetime.now(timezone.utc).astimezone()

    def to_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        self.finish()

        duration = ""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            secs = int(delta.total_seconds())
            if secs >= 60:
                duration = f"{secs // 60}m {secs % 60}s"
            else:
                duration = f"{secs}s"

        mode_label = "全量同步" if self.mode == "full" else "增量同步"
        dry_label = " (预览模式，未实际执行)" if self.dry_run else ""

        lines = []
        lines.append(f"# 同步报告 - {mode_label}{dry_label}")
        lines.append("")
        lines.append("## 基本信息")
        lines.append("")
        lines.append(f"| 项目 | 值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 同步模式 | {mode_label}{dry_label} |")
        lines.append(f"| 开始时间 | {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} |")
        if self.end_time:
            lines.append(f"| 结束时间 | {self.end_time.strftime('%Y-%m-%d %H:%M:%S')} |")
        if duration:
            lines.append(f"| 耗时 | {duration} |")
        lines.append(f"| Vault 路径 | `{self.vault_path}` |")
        lines.append(f"| 目标知识库 | `{self.target_space_id}` |")
        if self.target_folder_id:
            lines.append(f"| 目标目录 | `{self.target_folder_id}` |")
        if self.conflict_strategy:
            strategy_label = "乐享优先" if self.conflict_strategy == "lexiang_wins" else "源端优先"
            lines.append(f"| 冲突策略 | {strategy_label} (`{self.conflict_strategy}`) |")
        lines.append("")

        # 统计摘要
        lines.append("## 统计摘要")
        lines.append("")
        s = self.stats
        total_processed = (
            s["folders_created"]
            + s["pages_created"]
            + s["pages_updated"]
            + s.get("files_created", 0)
            + s["attachments_uploaded"]
        )
        total_skipped = s["pages_skipped_no_change"] + s["pages_skipped_conflict"]

        lines.append(f"| 指标 | 数量 |")
        lines.append(f"|------|------|")
        if s["folders_created"]:
            lines.append(f"| 创建目录 | {s['folders_created']} |")
        if s["pages_created"]:
            lines.append(f"| 创建文档 | {s['pages_created']} |")
        if s["pages_updated"]:
            lines.append(f"| 更新文档 | {s['pages_updated']} |")
        if s.get("files_created", 0):
            lines.append(f"| 上传文件 | {s['files_created']} |")
        if s["attachments_uploaded"]:
            lines.append(f"| 上传附件 | {s['attachments_uploaded']} |")
        if s["pages_skipped_no_change"]:
            lines.append(f"| 跳过（无变化） | {s['pages_skipped_no_change']} |")
        if s["pages_skipped_conflict"]:
            lines.append(f"| 跳过（乐享有更新） | {s['pages_skipped_conflict']} |")
        if s["source_deleted_ignored"]:
            lines.append(f"| 忽略（源端已删除） | {s['source_deleted_ignored']} |")
        if s["errors"]:
            lines.append(f"| **错误** | **{s['errors']}** |")
        lines.append(f"| **合计处理** | **{total_processed}** |")
        if total_skipped:
            lines.append(f"| 合计跳过 | {total_skipped} |")
        lines.append("")

        # 错误列表（如果有）
        error_actions = [a for a in self.actions if a["status"] == "error"]
        if error_actions:
            lines.append("## 错误记录")
            lines.append("")
            lines.append("| # | 操作 | 路径 | 错误信息 |")
            lines.append("|---|------|------|----------|")
            for i, a in enumerate(error_actions, 1):
                lines.append(f"| {i} | {a['action']} | `{a['rel_path']}` | {a['detail']} |")
            lines.append("")

        # 操作明细
        if self.actions:
            lines.append("## 操作明细")
            lines.append("")
            lines.append("| # | 操作 | 路径 | 状态 | entry_id | 备注 |")
            lines.append("|---|------|------|------|----------|------|")

            status_icons = {
                "success": "✅",
                "error": "❌",
                "skipped_no_change": "⏭️",
                "skipped_conflict": "⚠️",
            }

            for i, a in enumerate(self.actions, 1):
                icon = status_icons.get(a["status"], "")
                action_label = {
                    "create_folder": "创建目录",
                    "create_page": "创建文档",
                    "update_page": "更新文档",
                    "create_file": "上传文件",
                    "upload_attachment": "上传附件",
                }.get(a["action"], a["action"])
                eid = a["entry_id"][:8] + "..." if len(a["entry_id"]) > 8 else a["entry_id"]
                detail = a["detail"][:50] if a["detail"] else ""
                lines.append(
                    f"| {i} | {action_label} | `{a['rel_path']}` | {icon} | {eid} | {detail} |"
                )
            lines.append("")

        # 跳过的文件（简要列出，不重复出现在操作明细中）
        skipped_actions = [
            a
            for a in self.actions
            if a["status"] in ("skipped_no_change", "skipped_conflict")
        ]
        if skipped_actions and len(skipped_actions) > 10:
            # 如果跳过的太多，在明细中已列出，这里不再单独列
            pass

        lines.append("---")
        lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

        return "\n".join(lines)

    def save(self, vault_path: str) -> str:
        """保存报告到文件，返回文件路径"""
        reports_dir = ensure_reports_dir(vault_path)
        filename = generate_report_filename()
        report_path = os.path.join(reports_dir, filename)

        content = self.to_markdown()
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 清理旧报告
        cleanup_old_reports(vault_path)

        return report_path
