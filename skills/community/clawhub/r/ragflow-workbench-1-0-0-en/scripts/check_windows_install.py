#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import urllib.error
import urllib.request
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="检查 Windows 上 RAGFlow 基础运行状态。")
    parser.add_argument(
        "--api-url",
        default="http://127.0.0.1:9380",
        help="RAGFlow API 地址，默认 http://127.0.0.1:9380",
    )
    parser.add_argument(
        "--web-url",
        default="http://127.0.0.1:9222",
        help="RAGFlow Web UI 地址，默认 http://127.0.0.1:9222",
    )
    parser.add_argument(
        "--container-name",
        default="docker-ragflow-cpu-1",
        help="RAGFlow 容器名，默认 docker-ragflow-cpu-1",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出 JSON")
    return parser.parse_args()


def run_command(cmd: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as exc:
        return False, str(exc)
    output = (result.stdout or "").strip() or (result.stderr or "").strip()
    return result.returncode == 0, output


def check_http(url: str) -> tuple[bool, str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return False, str(getattr(exc, "reason", exc))


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    docker_ok, docker_version = run_command(["docker", "--version"])
    ps_ok, ps_output = run_command(["docker", "ps", "--filter", f"name={args.container_name}"])
    api_ok, api_status = check_http(args.api_url)
    web_ok, web_status = check_http(args.web_url)

    container_running = ps_ok and args.container_name in ps_output
    all_passed = docker_ok and container_running and api_ok and web_ok

    return {
        "all_passed": all_passed,
        "checks": {
            "docker_cli": {"ok": docker_ok, "detail": docker_version},
            "container_running": {"ok": container_running, "detail": ps_output},
            "api_reachable": {"ok": api_ok, "detail": f"{args.api_url} -> {api_status}"},
            "web_reachable": {"ok": web_ok, "detail": f"{args.web_url} -> {web_status}"},
        },
        "suggestion": (
            "继续执行 bootstrap_admin.py"
            if all_passed
            else "请先修复未通过项，再继续初始化管理员和 API Key。"
        ),
    }


def print_text(report: dict[str, Any]) -> None:
    status = "通过" if report["all_passed"] else "未通过"
    print(f"安装检查结果: {status}")
    print("")
    for name, item in report["checks"].items():
        mark = "OK" if item["ok"] else "FAIL"
        print(f"[{mark}] {name}: {item['detail']}")
    print("")
    print(f"建议: {report['suggestion']}")


def main() -> int:
    args = parse_args()
    report = build_report(args)
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
