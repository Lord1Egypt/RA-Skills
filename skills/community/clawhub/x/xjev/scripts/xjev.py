#!/usr/bin/env python3
"""xjev command-line interface. Secrets never accepted as command arguments."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys

from common import MAX_BYTES, Store, XjevError, dump, no_key_in, parse, probe, require, status
import decisions


def load_input(path):
    if path == "-":
        raw = sys.stdin.buffer.read(MAX_BYTES+1)
    else:
        with Path(path).open("rb") as f:
            raw = f.read(MAX_BYTES+1)
    require(len(raw) <= MAX_BYTES,"输入文件过大。")
    data = parse(raw)
    no_key_in(data)
    return data


def parser():
    p = argparse.ArgumentParser(description="xjev — Jev 决策与有范围的反馈学习")
    sub = p.add_subparsers(dest="command",required=True)
    s=sub.add_parser("status"); s.add_argument("--check",action="store_true")
    s=sub.add_parser("setup"); s.add_argument("--no-browser",action="store_true"); s.add_argument("--timeout",type=int,default=600)
    s=sub.add_parser("decide"); s.add_argument("--input",required=True); s.add_argument("--parent")
    s=sub.add_parser("show"); s.add_argument("id"); s.add_argument("--raw",action="store_true")
    s=sub.add_parser("feedback"); s.add_argument("id"); s.add_argument("--input",required=True)
    s=sub.add_parser("policies"); s.add_argument("--scope",required=True); s.add_argument("--all",action="store_true")
    s=sub.add_parser("policy-new"); s.add_argument("--input",required=True)
    s=sub.add_parser("policy-revoke"); s.add_argument("id")
    s=sub.add_parser("policy-trial"); s.add_argument("id"); s.add_argument("--input",required=True)
    s=sub.add_parser("policy-adopt"); s.add_argument("id"); s.add_argument("--trial",required=True)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    store = None
    try:
        if args.command == "status":
            result = status()
            if args.check:
                result["probe"] = probe()
        elif args.command == "setup":
            from onboarding import setup_server
            require(1 <= args.timeout <= 3600,"timeout 需要 1–3600 秒。")
            return setup_server(args.timeout,not args.no_browser)
        else:
            store = Store()
            if args.command == "decide":
                result = decisions.evaluate(store,load_input(args.input),args.parent)
            elif args.command == "show":
                record = store.get(args.id,"decision")
                result = record if args.raw else decisions.receipt(record)
            elif args.command == "feedback":
                result = decisions.feedback(store,args.id,load_input(args.input))
            elif args.command == "policies":
                result = store.all("policy",args.scope) if args.all else decisions.active_policies(store,args.scope)
            elif args.command == "policy-new":
                result = decisions.policy_new(store,load_input(args.input))
            elif args.command == "policy-revoke":
                result = decisions.revoke(store,args.id)
            elif args.command == "policy-trial":
                result = decisions.trial(store,args.id,load_input(args.input))
            else:
                result = decisions.adopt(store,args.id,args.trial)
        print(dump({"ok":True,"result":result}))
        return 0
    except XjevError as e:
        print(dump({"ok":False,"error":{"code":e.code,"message":e.message}}))
        return 2
    except (OSError,ValueError,TypeError,KeyError,sqlite3.Error):
        # Do not echo user input, response bodies, file contents or credentials.
        print(dump({"ok":False,"error":{"code":"local_error","message":"本机输入或存储操作失败；请检查文件格式与目录权限。"}}))
        return 2
    finally:
        if store:
            store.close()


if __name__ == "__main__":
    sys.exit(main())
