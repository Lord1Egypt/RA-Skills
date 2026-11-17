#!/usr/bin/env python3
"""通过腾讯云「自动化助手」（TAT）在服务器上以 root 身份执行 shell 命令，并等待输出结果。
不需要 SSH 密钥，也不需要本机有 ssh 和 base64 工具，Windows 上同样可用。纯标准库。

用法：
    python run_on_server.py --instance lhins-xxx "uname -a; df -h /"
    python run_on_server.py --instance lhins-xxx --file deploy.sh       # 执行本地脚本文件的内容
    python run_on_server.py --instance lhins-xxx --user ubuntu "whoami"
    可选：--region ap-hongkong（默认取 profile 配置）  --timeout 600  --profile agent-ops

输出一行 JSON：{"ok", "status", "exit_code", "output"}；output 最多保留 24KB（TAT 自身的上限）。
长时间任务（比如装依赖）把 --timeout 调大；TAT 单次最长 86400 秒。
"""
import argparse
import base64
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcapi  # noqa: E402


def run(instance, command, region=None, profile=tcapi.DEFAULT_PROFILE, timeout=300, user="root"):
    content = base64.b64encode(command.encode("utf-8")).decode()
    params = {"Content": content, "InstanceIds": [instance], "CommandType": "SHELL",
              "Timeout": timeout, "Username": user}
    inv = tcapi.call("tat", "RunCommand", params, region=region, profile=profile)["InvocationId"]
    deadline = time.time() + timeout + 30
    while time.time() < deadline:
        time.sleep(3)
        r = tcapi.call("tat", "DescribeInvocationTasks",
                       {"Filters": [{"Name": "invocation-id", "Values": [inv]}], "HideOutput": False},
                       region=region, profile=profile)
        tasks = r.get("InvocationTaskSet") or []
        if not tasks:
            continue
        t = tasks[0]
        if t["TaskStatus"] in ("PENDING", "DELIVERING", "RUNNING"):
            continue
        res = t.get("TaskResult") or {}
        out = base64.b64decode(res.get("Output") or "").decode("utf-8", "replace")
        return {"ok": t["TaskStatus"] == "SUCCESS", "status": t["TaskStatus"],
                "exit_code": res.get("ExitCode"), "output": out}
    return {"ok": False, "status": "LOCAL_TIMEOUT", "exit_code": None, "output": ""}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True)
    ap.add_argument("--region")
    ap.add_argument("--profile", default=tcapi.DEFAULT_PROFILE)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--user", default="root")
    ap.add_argument("--file")
    ap.add_argument("command", nargs="?")
    a = ap.parse_args()
    cmd = Path(a.file).read_text(encoding="utf-8") if a.file else a.command
    if not cmd:
        ap.error("需要命令或 --file")
    try:
        r = run(a.instance, cmd, a.region, a.profile, a.timeout, a.user)
    except tcapi.TcError as e:
        r = {"ok": False, **tcapi.error_report(e, "RunCommand")}
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
