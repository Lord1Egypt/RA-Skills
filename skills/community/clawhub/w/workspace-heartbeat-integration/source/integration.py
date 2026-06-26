#!/usr/bin/env python3
"""
Workspace Heartbeat Integration
Synchronizes workspace heartbeat tracking with self-improving system.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Workspace paths
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
HEARTBEAT_STATE = MEMORY_DIR / "heartbeat-state.json"
TASK_BOARD = WORKSPACE / "TASK_BOARD.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"


class HeartbeatIntegration:
    def __init__(self, config_path: Optional[Path] = None):
        self.workspace = WORKSPACE
        self.memory_dir = MEMORY_DIR
        self.state_file = HEARTBEAT_STATE
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[Path]) -> Dict:
        default_config = {
            "auto_sync": True,
            "log_retention_days": 30,
            "memory_update_threshold": 3,
            "excluded_dirs": [".git", "node_modules", "__pycache__", ".venv"],
        }
        if config_path and config_path.exists():
            try:
                with open(config_path) as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: failed to load config: {e}")
        return default_config

    def load_state(self) -> Dict:
        if not self.state_file.exists():
            return {"lastChecks": {}, "notes": ""}
        with open(self.state_file) as f:
            return json.load(f)

    def save_state(self, state: Dict) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def get_today_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def get_today_log_path(self) -> Path:
        return self.memory_dir / self.get_today_date()

    def ensure_today_log(self) -> Path:
        log_path = self.get_today_log_path()
        if not log_path.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(f"# {log_path.name} 学习日志\n\n## 🕐 时间线\n\n**凌晨 (4:00-6:00)**\n- 00:00 心跳检查，开始新一天\n\n")
        return log_path

    def append_work_log(self, category: str, description: str, details: Optional[str] = None) -> Path:
        """Append a work log entry to today's memory file."""
        log_path = self.ensure_today_log()
        timestamp = datetime.now().strftime("%H:%M")
        category_icons = {
            "learning": "📚",
            "development": "🏗️",
            "testing": "🧪",
            "debugging": "🔧",
            "documentation": "📝",
            "release": "🚀",
            "research": "🔍",
            "optimization": "⚡",
            "meeting": "🤝",
            "other": "💡"
        }
        icon = category_icons.get(category.lower(), "•")

        entry = f"- {timestamp} {category.title()}: {description}\n"
        if details:
            entry += f"  Details: {details}\n"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

        print(f"✅ Logged work: {description}")
        return log_path

    def sync(self, dry_run: bool = False) -> Dict:
        """Perform full synchronization of heartbeat state."""
        print("🔄 Starting heartbeat sync...")

        state = self.load_state()
        now = int(datetime.now().timestamp())

        # Update last sync timestamp
        state.setdefault("lastSync", now)

        # Check which intervals need updating based on last check times
        intervals = {
            "hourly": 3600,
            "twoHourly": 7200,
            "fourHourly": 14400,
            "daily": 86400
        }

        for key, interval in intervals.items():
            last_check = state.get("lastChecks", {}).get(key, 0)
            if now - last_check >= interval:
                print(f"  • {key} check due")
                state.setdefault("lastChecks", {})[key] = now

        # Scan today's log and generate summary
        today = self.get_today_date()
        log_path = self.memory_dir / today
        if log_path.exists():
            entry_count = sum(1 for _ in open(log_path, encoding="utf-8") if "- " in _)
            state.setdefault("todayStats", {})[today] = {
                "entries": entry_count,
                "lastUpdated": now
            }
            print(f"  • Today's log: {entry_count} entries")

        # If dry_run, don't save
        if not dry_run:
            self.save_state(state)
            print(f"✅ Sync completed at {datetime.fromtimestamp(now).strftime('%H:%M:%S')}")
        else:
            print("ℹ️ Dry run mode, state not saved")

        return state

    def generate_report(self, output_format: str = "text") -> str:
        """Generate a comprehensive heartbeat report."""
        state = self.load_state()
        today = self.get_today_date()
        log_path = self.memory_dir / today

        report_lines = [
            "📊 Heartbeat Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Last Checks",
        ]

        for check, ts in state.get("lastChecks", {}).items():
            dt = datetime.fromtimestamp(ts).strftime("%H:%M:%S") if ts else "Never"
            report_lines.append(f"- {check}: {dt}")

        report_lines.append("")
        report_lines.append("## Today's Work Summary")

        if log_path.exists():
            with open(log_path, encoding="utf-8") as f:
                content = f.read()
                # Extract actual work entries (skip header)
                lines = [l for l in content.splitlines() if l.strip().startswith("- ")]
                report_lines.extend(lines[:20])  # Limit to 20 entries
                if len(lines) > 20:
                    report_lines.append(f"... and {len(lines)-20} more entries")
        else:
            report_lines.append("No log entries for today yet.")

        # Task board summary
        if TASK_BOARD.exists():
            report_lines.append("")
            report_lines.append("## Pending High-Priority Tasks")
            with open(TASK_BOARD) as f:
                content = f.read()
                # Simple parsing: look for "🚧 开发中" section
                if "🚧 开发中" in content:
                    report_lines.append("(See TASK_BOARD.md for full list)")

        report = "\n".join(report_lines)

        if output_format == "json":
            import json
            report = json.dumps({
                "generated": datetime.now().isoformat(),
                "lastChecks": state.get("lastChecks", {}),
                "todayLog": str(log_path) if log_path.exists() else None,
                "summary": report
            }, indent=2, ensure_ascii=False)

        return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Workspace Heartbeat Integration")
    parser.add_argument("--sync", action="store_true", help="Sync heartbeat state")
    parser.add_argument("--log", metavar="CATEGORY:DESCRIPTION", help="Log work session (format: 'category:description')")
    parser.add_argument("--report", action="store_true", help="Generate heartbeat report")
    parser.add_argument("--format", choices=["text", "markdown", "json"], default="text", help="Report format")
    parser.add_argument("--dry-run", action="store_true", help="Do not save changes")
    args = parser.parse_args()

    integration = HeartbeatIntegration()

    if args.log:
        try:
            category, description = args.log.split(":", 1)
            integration.append_work_log(category.strip(), description.strip())
        except ValueError:
            print("Error: --log requires format 'category:description'")
            sys.exit(1)

    if args.sync:
        integration.sync(dry_run=args.dry_run)

    if args.report:
        report = integration.generate_report(output_format=args.format)
        print(report)

    # If no arguments, show help
    if not any([args.sync, args.log, args.report]):
        parser.print_help()


if __name__ == "__main__":
    main()