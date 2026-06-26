#!/usr/bin/env python3
"""
WeChat Mini Program console log reader.
Reads console output, error logs, network requests, etc. from DevTools.
"""

import subprocess
import json
import os
import re
import time
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    """Log level"""
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    ALL = "all"


@dataclass
class ConsoleLog:
    """Console log entry"""
    timestamp: str
    level: str
    message: str
    source: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConsoleReader:
    """
    Mini program console log reader.

    Features:
    - Read console logs (debug/info/warn/error)
    - Filter logs by level
    - Monitor errors and exceptions
    - Export log reports
    """

    def __init__(self, project_path: str, ws_endpoint: str = "ws://localhost:9420"):
        self.project_path = project_path
        self.ws_endpoint = ws_endpoint
        self.logs: List[ConsoleLog] = []
        self.error_handlers: List[Callable[[ConsoleLog], None]] = []

    def _get_log_file_path(self) -> Optional[str]:
        """
        Get the DevTools log file path (platform-aware).
        """
        import sys as _sys
        home = os.path.expanduser("~")

        if _sys.platform == "win32":
            log_dirs = [
                os.path.join(home, "AppData", "Local", "微信开发者工具", "User Data"),
                os.path.join(home, "AppData", "Local", "WeChat DevTools", "User Data"),
            ]
        else:
            log_dirs = [
                os.path.join(home, "Library/Application Support/微信开发者工具"),
                os.path.join(home, "Library/Application Support/wechatwebdevtools"),
            ]

        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                log_files = []
                for root, dirs, files in os.walk(log_dir):
                    for file in files:
                        if file.endswith(".log") or "console" in file.lower():
                            filepath = os.path.join(root, file)
                            log_files.append((filepath, os.path.getmtime(filepath)))

                if log_files:
                    log_files.sort(key=lambda x: x[1], reverse=True)
                    return log_files[0][0]

        return None

    def read_logs_from_script(self) -> List[ConsoleLog]:
        """
        Read console logs via automation script.

        Connects to DevTools using miniprogram-automator to fetch logs.
        """
        ws_endpoint = self.ws_endpoint
        script_content = f'''
const automator = require('miniprogram-automator');

async function getLogs() {{
    try {{
        const miniProgram = await automator.connect({{
            wsEndpoint: '{ws_endpoint}'
        }});

        const page = await miniProgram.currentPage();

        const logs = await miniProgram.evaluate(() => {{
            return {{
                page: getCurrentPages().map(p => p.route),
                systemInfo: wx.getSystemInfoSync()
            }};
        }});

        console.log('CONSOLE_LOGS_RESULT: ' + JSON.stringify({{
            success: true,
            data: logs
        }}));

        await miniProgram.disconnect();
    }} catch (error) {{
        console.log('CONSOLE_LOGS_RESULT: ' + JSON.stringify({{
            success: false,
            error: error.message
        }}));
        process.exit(1);
    }}
}}

getLogs();
'''
        script_path = os.path.join(tempfile.gettempdir(), f"console_reader_{int(time.time())}.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        try:
            result = subprocess.run(
                ["node", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse result
            output = result.stdout + result.stderr
            match = re.search(r'CONSOLE_LOGS_RESULT:\s*(\{.*?\})', output, re.DOTALL)

            if match:
                data = json.loads(match.group(1))
                if data.get("success"):
                    # Convert to ConsoleLog format
                    log = ConsoleLog(
                        timestamp=datetime.now().isoformat(),
                        level="info",
                        message=json.dumps(data.get("data", {}), ensure_ascii=False)
                    )
                    return [log]

        except Exception as e:
            return [ConsoleLog(
                timestamp=datetime.now().isoformat(),
                level="error",
                message=f"Failed to read logs: {str(e)}"
            )]
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)

        return []

    def parse_log_line(self, line: str) -> Optional[ConsoleLog]:
        """Parse a single log line."""
        # Common log formats:
        # [2024-01-15 10:30:45] [INFO] message
        # 2024-01-15T10:30:45.123Z [error] message at file.js:123

        patterns = [
            # Format: [timestamp] [level] message
            r'\[(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s*\[(\w+)\]\s*(.+)',
            # Format: timestamp [level] message
            r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s*\[(\w+)\]\s*(.+)',
            # Format: level: message
            r'(debug|info|warn|error):\s*(.+)',
        ]

        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    return ConsoleLog(
                        timestamp=groups[0] if ':' in groups[0] else datetime.now().isoformat(),
                        level=groups[1].lower(),
                        message=groups[2].strip()
                    )
                elif len(groups) == 2:
                    return ConsoleLog(
                        timestamp=datetime.now().isoformat(),
                        level=groups[0].lower(),
                        message=groups[1].strip()
                    )

        # Unable to parse format, treat as plain info
        return ConsoleLog(
            timestamp=datetime.now().isoformat(),
            level="info",
            message=line.strip()
        )

    def filter_logs(self, level: LogLevel = LogLevel.ALL, pattern: Optional[str] = None) -> List[ConsoleLog]:
        """
        Filter logs.

        Args:
            level: Log level
            pattern: Regex pattern

        Returns:
            Filtered list of logs
        """
        filtered = self.logs

        if level != LogLevel.ALL:
            filtered = [log for log in filtered if log.level.lower() == level.value]

        if pattern:
            regex = re.compile(pattern, re.IGNORECASE)
            filtered = [log for log in filtered if regex.search(log.message)]

        return filtered

    def get_errors(self) -> List[ConsoleLog]:
        """Get all error logs."""
        return self.filter_logs(LogLevel.ERROR)

    def get_warnings(self) -> List[ConsoleLog]:
        """Get all warning logs."""
        return self.filter_logs(LogLevel.WARN)

    def on_error(self, handler: Callable[[ConsoleLog], None]):
        """Register an error handler."""
        self.error_handlers.append(handler)

    def export_to_json(self, filepath: str, level: LogLevel = LogLevel.ALL):
        """Export logs to a JSON file."""
        logs = self.filter_logs(level)
        data = {
            "export_time": datetime.now().isoformat(),
            "project_path": self.project_path,
            "total_logs": len(logs),
            "logs": [log.to_dict() for log in logs]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_to_markdown(self, filepath: str, level: LogLevel = LogLevel.ALL):
        """Export logs to a Markdown file."""
        logs = self.filter_logs(level)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Mini Program Console Log Report\n\n")
            f.write(f"**Export Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Project Path**: {self.project_path}\n\n")
            f.write(f"**Total Logs**: {len(logs)}\n\n")

            # Statistics
            error_count = len([l for l in logs if l.level == "error"])
            warn_count = len([l for l in logs if l.level == "warn"])

            f.write("## Statistics\n\n")
            f.write(f"- Errors: {error_count}\n")
            f.write(f"- Warnings: {warn_count}\n")
            f.write(f"- Info: {len(logs) - error_count - warn_count}\n\n")

            f.write("## Detailed Logs\n\n")
            f.write("| Time | Level | Message |\n")
            f.write("|------|-------|--------|\n")

            for log in logs:
                # Escape Markdown table characters
                message = log.message.replace("|", "\\|").replace("\n", " ")
                f.write(f"| {log.timestamp} | {log.level.upper()} | {message} |\n")


class PerformanceMonitor:
    """Performance monitor - collect mini program performance data."""

    def __init__(self, project_path: str, ws_endpoint: str = "ws://localhost:9420"):
        self.project_path = project_path
        self.ws_endpoint = ws_endpoint
        self.metrics: List[Dict[str, Any]] = []

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect performance metrics via automation script."""
        ws_endpoint = self.ws_endpoint
        script_content = f'''
const automator = require('miniprogram-automator');

async function collectMetrics() {{
    try {{
        const miniProgram = await automator.connect({{
            wsEndpoint: '{ws_endpoint}'
        }});

        const systemInfo = await miniProgram.evaluate(() => {{
            return wx.getSystemInfoSync();
        }});

        const performance = await miniProgram.evaluate(() => {{
            if (typeof wx.getPerformance === 'function') {{
                return wx.getPerformance();
            }}
            return null;
        }});

        console.log('PERFORMANCE_RESULT: ' + JSON.stringify({{
            success: true,
            data: {{
                systemInfo: systemInfo,
                performance: performance
            }}
        }}));

        await miniProgram.disconnect();
    }} catch (error) {{
        console.log('PERFORMANCE_RESULT: ' + JSON.stringify({{
            success: false,
            error: error.message
        }}));
        process.exit(1);
    }}
}}

collectMetrics();
'''
        script_path = os.path.join(tempfile.gettempdir(), f"perf_monitor_{int(time.time())}.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        try:
            result = subprocess.run(
                ["node", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout + result.stderr
            match = re.search(r'PERFORMANCE_RESULT:\s*(\{.*?\})', output, re.DOTALL)

            if match:
                data = json.loads(match.group(1))
                if data.get("success"):
                    self.metrics.append({
                        "timestamp": datetime.now().isoformat(),
                        "data": data.get("data", {})
                    })
                    return data.get("data", {})

        except Exception as e:
            return {"error": str(e)}
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)

        return {}

    def export_report(self, filepath: str):
        """Export performance report."""
        report = {
            "export_time": datetime.now().isoformat(),
            "project_path": self.project_path,
            "metrics_count": len(self.metrics),
            "metrics": self.metrics
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Mini program console log reader")
    parser.add_argument("--project", "-p", required=True, help="Mini program project path")
    parser.add_argument("--action", "-a", choices=["read", "errors", "export"], default="read")
    parser.add_argument("--level", choices=["debug", "info", "warn", "error", "all"], default="all")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")

    args = parser.parse_args()

    reader = ConsoleReader(args.project)

    if args.action == "read":
        logs = reader.read_logs_from_script()
        reader.logs = logs
        filtered = reader.filter_logs(LogLevel(args.level))

        for log in filtered:
            print(f"[{log.level.upper()}] {log.timestamp}: {log.message}")

    elif args.action == "errors":
        logs = reader.read_logs_from_script()
        reader.logs = logs
        errors = reader.get_errors()

        print(f"Found {len(errors)} error(s):")
        for error in errors:
            print(f"[{error.timestamp}] {error.message}")

    elif args.action == "export":
        logs = reader.read_logs_from_script()
        reader.logs = logs

        output_path = args.output or f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"

        if args.format == "json":
            reader.export_to_json(output_path, LogLevel(args.level))
        else:
            reader.export_to_markdown(output_path, LogLevel(args.level))

        print(f"Logs exported to: {output_path}")


if __name__ == "__main__":
    main()
