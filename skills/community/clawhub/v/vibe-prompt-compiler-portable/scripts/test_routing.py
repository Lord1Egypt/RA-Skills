#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "compile_prompt.py"

CASES = [
    ("帮我做一个活动报名后台 MVP", "new-project"),
    ("Build an admin dashboard MVP", "new-project"),
    ("修复登录接口 500", "bugfix"),
    ("Refactor the profile settings module", "refactor"),
    ("设计一个活动报名页面", "page-ui"),
    ("给用户管理加 CRUD", "crud-feature"),
    ("实现一个提交报名的 API 接口", "api-backend"),
    ("我们有一套 React + FastAPI + SQLite 的测试系统，想支持两个产品，数据完全隔离但功能一致，怎么设计架构？", "architecture-review"),
    ("把我们的系统和企业微信审批打通，审批通过后自动回写状态", "integration"),
    ("做一个自动化流程，定时扫描目录里的文件，解析后入库，失败就提醒我", "automation-workflow"),
    ("给知识库问答加一个自动总结和推荐下一步操作的功能", "ai-feature"),
    ("帮我把这个 React + FastAPI 项目部署到 Windows 机器上，最好后面也方便迁移", "deployment"),
]


def classify(request: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--request", request, "--output", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)["task_type"]


def main():
    failed = 0
    for request, expected in CASES:
        task_type = classify(request)
        ok = task_type == expected
        print(f"{'OK' if ok else 'FAIL'} | expected={expected} got={task_type} | {request}")
        if not ok:
            failed += 1
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
