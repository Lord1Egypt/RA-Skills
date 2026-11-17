#!/usr/bin/env python3
"""Install a local copy without overwriting an existing skill; prompt for setup."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="安装 xjev 并引导配置 Jev API key")
    parser.add_argument("--target",type=Path,help="完整安装目录；默认 ~/.agents/skills/xjev")
    parser.add_argument("--no-setup",action="store_true",help="仅显示配置命令，不打开本机配置页")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    requested = (args.target or Path.home()/".agents/skills/xjev").expanduser().absolute()
    if requested.is_symlink():
        print(json.dumps({"ok":False,"message":"安装目标是已有符号链接，未修改。"},ensure_ascii=False))
        return 2
    target = requested.resolve()
    if target != source:
        if target.exists():
            print(json.dumps({"ok":False,"message":"安装目录已存在，未覆盖；请使用现有目录或指定新目标。"},ensure_ascii=False))
            return 2
        if source in target.parents:
            print(json.dumps({"ok":False,"message":"安装目标不能位于源目录内。"},ensure_ascii=False))
            return 2
        shutil.copytree(source,target,ignore=shutil.ignore_patterns("__pycache__","*.pyc",".DS_Store"))
    command = [sys.executable,str(target/"scripts/xjev.py")]
    check = subprocess.run(command+["status"],capture_output=True,text=True)
    if check.returncode:
        print(check.stdout)
        return check.returncode
    result = json.loads(check.stdout)["result"]
    print(json.dumps({"ok":True,"installed":str(target),"configured":result["configured"],
        "message":"xjev 已安装。配置 Jev API key 后可在相关决策中自动选用；安装没有常驻后台进程。",
        "setup_command":command+["setup"]},ensure_ascii=False),flush=True)
    if not result["configured"] and not args.no_setup:
        return subprocess.call(command+["setup"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
