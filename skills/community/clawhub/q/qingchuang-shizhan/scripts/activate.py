#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
activate.py —— yihaiyoudao 技能包·首次激活

用法：
  python scripts/activate.py           # 首次运行：自动生成安装编号并显示登记指引；再次运行：显示编号与状态
  python scripts/activate.py --check   # 只显示状态，不重复生成

机制：
  买家下载技能包后，第一次加载进 AI 工具时必须先运行本脚本。
  脚本在本机自动生成唯一安装编号（YHYD-日期-随机码），并保存到
  ~/.yihaiyoudao/activate.json。买家把编号发给作者骇老师登记，
  作者确认后即完成授权（见作者侧 fangdaomai 技能 --register）。

  编号只在本机生成与保存，不上传、不外发。
"""
import json
import os
import sys
import time
import uuid
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA_DIR = os.path.join(os.path.expanduser("~"), ".yihaiyoudao")
DATA_FILE = os.path.join(DATA_DIR, "activate.json")
AUTHOR_NOTE = "作者骇老师 · GitHub: https://github.com/lichengyu1207 · 体验群/私信发编号登记"


def gen_no():
    return "YHYD-" + time.strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6].upper()


def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def first_run():
    no = gen_no()
    data = {
        "install_no": no,
        "created": str(date.today()),
        "status": "未登记",
        "authorized": False,
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("首次激活：已自动生成你的专属安装编号")
    print("")
    print("你的安装编号：" + no)
    print("")
    print("下一步（必须）：把这个编号发给作者登记")
    print("  " + AUTHOR_NOTE)
    print("")
    print("作者登记后会回你授权确认。未登记前只提供基础说明，登记后完整使用。")
    print("")
    print("编号只保存在本机（~/.yihaiyoudao/activate.json），不会自动上传。")


def show(check_only=False):
    data = load()
    if not data:
        if check_only:
            print("未激活：请先运行 python scripts/activate.py 生成安装编号。")
        else:
            first_run()
        return
    print("你的安装编号：" + data.get("install_no", ""))
    print("状态：" + data.get("status", "未登记"))
    if data.get("authorized"):
        print("已授权登记，可完整使用本技能。")
    else:
        print("未登记：请把编号发给作者登记。" + AUTHOR_NOTE)


def main():
    args = sys.argv[1:]
    if "--check" in args:
        show(check_only=True)
    elif not load():
        first_run()
    else:
        show()


if __name__ == "__main__":
    main()
