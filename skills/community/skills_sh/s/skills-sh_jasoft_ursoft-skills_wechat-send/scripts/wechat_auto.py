#!/usr/bin/env python3
"""Automate WeChat messaging on macOS."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Optional, Sequence


def format_cmd(cmd: Sequence[object]) -> str:
    return " ".join(str(part) for part in cmd)


def run_process(
    cmd: Sequence[object], timeout: int = 30
) -> subprocess.CompletedProcess[str]:
    cmd_parts = [str(part) for part in cmd]
    try:
        return subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Command timed out: {format_cmd(cmd_parts)}") from exc


def run(cmd: Sequence[object], timeout: int = 30) -> str:
    result = run_process(cmd, timeout=timeout)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(
            f"Command failed ({result.returncode}): {format_cmd(cmd)}"
            + (f"\n{stderr}" if stderr else "")
        )
    return result.stdout.strip()


def which(name: str) -> Optional[str]:
    return shutil.which(name)


def osascript(script: str, args: Optional[list[str]] = None) -> str:
    cmd: list[object] = ["osascript", "-e", script]
    if args:
        cmd.extend(args)
    return run(cmd)


def activate_wechat() -> None:
    script = """
tell application "WeChat" to activate
tell application "System Events"
    tell process "WeChat"
        set frontmost to true
    end tell
end tell
"""
    osascript(script)


def type_text_via_clipboard(text: str) -> None:
    result = subprocess.run(
        ["pbcopy"],
        input=text,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(
            "Failed to copy text to clipboard" + (f": {stderr}" if stderr else "")
        )

    script = """
tell application "System Events"
    keystroke "v" using command down
end tell
"""
    osascript(script)
    time.sleep(0.2)


def press_return() -> None:
    script = """
tell application "System Events"
    keystroke return
end tell
"""
    osascript(script)


class WeChatAuto:
    def __init__(self, debug: bool = False, delay: float = 0.5):
        self.debug = debug
        self.delay = delay

    def log(self, msg: str) -> None:
        if self.debug:
            print(f"[DEBUG] {msg}", file=sys.stderr)

    def wait_for_wechat(self, timeout: int = 10) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            try:
                script = """
tell application "System Events"
    return (name of first application process whose frontmost is true)
end tell
"""
                result = osascript(script)
                if "WeChat" in result:
                    return True
            except RuntimeError:
                pass
            time.sleep(0.5)
        return False

    def ensure_wechat_frontmost(self) -> None:
        activate_wechat()
        time.sleep(max(self.delay, 0.5))
        if not self.wait_for_wechat():
            raise RuntimeError("WeChat window did not become active")

    def ensure_wechat_running(self) -> None:
        result = run_process(["pgrep", "-x", "WeChat"])
        if result.returncode != 0:
            print("WeChat is not running, attempting to launch...")
            launch = run_process(["open", "-a", "WeChat"], timeout=15)
            if launch.returncode != 0:
                stderr = launch.stderr.strip()
                raise RuntimeError(
                    "Failed to launch WeChat" + (f": {stderr}" if stderr else "")
                )
            time.sleep(3.0)
        else:
            self.log("WeChat is already running")

        self.ensure_wechat_frontmost()

    def search_contact(self, contact_name: str) -> bool:
        self.log(f"Searching for contact: {contact_name}")

        script = """
tell application "System Events"
    keystroke "2" using command down
    keystroke "f" using command down
end tell
"""
        osascript(script)
        time.sleep(self.delay)

        clear_script = """
tell application "System Events"
    keystroke "a" using command down
    keystroke (ASCII character 8)
end tell
"""
        osascript(clear_script)
        time.sleep(0.3)

        type_text_via_clipboard(contact_name)
        time.sleep(1.0)
        press_return()
        time.sleep(self.delay)
        return True

    def send_message(self, contact_name: str, message: str) -> bool:
        self.log(f"Sending to {contact_name}: {message[:50]}")
        self.ensure_wechat_running()

        if not self.search_contact(contact_name):
            raise RuntimeError(f"Could not find contact: {contact_name}")

        self.ensure_wechat_frontmost()
        time.sleep(self.delay)

        type_text_via_clipboard(message)
        time.sleep(0.5)
        press_return()
        time.sleep(0.5)

        self.log("Message sent")
        return True


@dataclass
class DoctorCheck:
    name: str
    ok: bool
    detail: str
    required: bool = True


def command_check(name: str) -> DoctorCheck:
    path = which(name)
    if path:
        return DoctorCheck(name, True, path)
    return DoctorCheck(name, False, f"Missing command: {name}")


def wechat_app_check() -> DoctorCheck:
    result = run_process(["open", "-Ra", "WeChat"], timeout=15)
    if result.returncode == 0:
        return DoctorCheck("WeChat.app", True, "WeChat is available")
    stderr = result.stderr.strip() or result.stdout.strip() or "WeChat not found"
    return DoctorCheck("WeChat.app", False, stderr)


def collect_doctor_checks() -> list[DoctorCheck]:
    return [
        command_check("python3"),
        command_check("osascript"),
        command_check("pbcopy"),
        command_check("pbpaste"),
        command_check("open"),
        command_check("pgrep"),
        wechat_app_check(),
    ]


def print_doctor_report(checks: Sequence[DoctorCheck]) -> None:
    for check in checks:
        status = "OK" if check.ok else "ERR"
        print(f"[{status}] {check.name}: {check.detail}")


def run_doctor() -> int:
    checks = collect_doctor_checks()
    print_doctor_report(checks)
    failures = [check.name for check in checks if check.required and not check.ok]
    if failures:
        print(
            "Error: doctor found missing or invalid dependencies: "
            + ", ".join(failures),
            file=sys.stderr,
        )
        return 1
    print("doctor ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automate WeChat messaging on macOS")
    sub = parser.add_subparsers(dest="action", required=True)

    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--debug", action="store_true", help="Enable debug output")

    send = sub.add_parser("send", parents=[shared], help="Send a message")
    send.add_argument("contact", help="Contact name to search for")
    send.add_argument("message", help="Message text to send")
    send.add_argument(
        "--delay", type=float, default=0.5, help="Delay between actions (seconds)"
    )

    sub.add_parser("doctor", parents=[shared], help="Check required environment")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.action == "doctor":
            return run_doctor()

        wc = WeChatAuto(debug=args.debug, delay=args.delay)
        wc.send_message(args.contact, args.message)
        print(f"Message sent to {args.contact}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
