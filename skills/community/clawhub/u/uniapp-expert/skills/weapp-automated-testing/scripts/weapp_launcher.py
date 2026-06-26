#!/usr/bin/env python3
"""
WeChat Mini Program DevTools launcher.
Provides functionality to launch, close, and connect to DevTools.
"""

import subprocess
import os
import time
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Platform-specific default CLI path
if sys.platform == "win32":
    DEFAULT_CLI_PATH = r"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat"
else:
    DEFAULT_CLI_PATH = "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"

class WeappLauncher:
    """WeChat Mini Program DevTools launcher."""

    def __init__(self, cli_path: str = DEFAULT_CLI_PATH):
        self.cli_path = cli_path
        self._validate_cli()

    def _validate_cli(self):
        """Validate that the CLI tool exists."""
        if not os.path.exists(self.cli_path):
            raise FileNotFoundError(
                f"WeChat DevTools CLI not found: {self.cli_path}\n"
                "Make sure WeChat DevTools is installed, or specify the cli path manually."
            )

    def _run_command(self, args: list, timeout: int = 30) -> Dict[str, Any]:
        """Run a CLI command."""
        cmd = [self.cli_path] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timeout",
                "stdout": "",
                "stderr": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": ""
            }

    def open_project(self, project_path: str, auto_preview: bool = False) -> Dict[str, Any]:
        """
        Open a mini program project.

        Args:
            project_path: Mini program project root directory path
            auto_preview: Whether to automatically open preview

        Returns:
            Command execution result
        """
        if not os.path.exists(project_path):
            return {
                "success": False,
                "error": f"Project path does not exist: {project_path}"
            }

        args = ["-o", project_path]
        if auto_preview:
            args.append("--preview")

        return self._run_command(args)

    def close_project(self, project_path: str) -> Dict[str, Any]:
        """
        Close a mini program project.

        Args:
            project_path: Mini program project root directory path

        Returns:
            Command execution result
        """
        args = ["-c", project_path]
        return self._run_command(args)

    def quit_wechatdevtools(self) -> Dict[str, Any]:
        """Quit WeChat DevTools."""
        return self._run_command(["-q"])

    def auto_test(self, project_path: str, port: int = 9420) -> Dict[str, Any]:
        """
        Open automation test port.

        Args:
            project_path: Mini program project path
            port: Automation test WebSocket port

        Returns:
            Execution result
        """
        args = [
            "auto",
            "--project", project_path,
            "--auto-port", str(port)
        ]
        return self._run_command(args, timeout=120)

    def is_running(self) -> bool:
        """Check if WeChat DevTools is running."""
        if sys.platform == "win32":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq wechatdevtools.exe"],
                capture_output=True, text=True
            )
            return "wechatdevtools.exe" in result.stdout.lower()
        else:
            result = subprocess.run(
                ["pgrep", "-f", "wechatwebdevtools"],
                capture_output=True
            )
            return result.returncode == 0


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="WeChat Mini Program DevTools launcher")
    parser.add_argument("--cli-path", default=DEFAULT_CLI_PATH, help="CLI tool path")
    parser.add_argument("--project", "-p", required=True, help="Mini program project path")
    parser.add_argument("--action", "-a", choices=["open", "close", "quit", "test"], default="open")
    parser.add_argument("--auto-preview", action="store_true", help="Automatically open preview")
    parser.add_argument("--test-script", help="Automation test script path")

    args = parser.parse_args()

    launcher = WeappLauncher(args.cli_path)

    if args.action == "open":
        result = launcher.open_project(args.project, args.auto_preview)
    elif args.action == "close":
        result = launcher.close_project(args.project)
    elif args.action == "quit":
        result = launcher.quit_wechatdevtools()
    elif args.action == "test":
        result = launcher.auto_test(args.project, 9420)
    else:
        print(f"Unknown action: {args.action}")
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
