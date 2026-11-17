#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字 skill 客户端（skill_api.py）
================================================
统一封装服务端三个接口，避免手写 HTTP：

    python3 skill_api.py register --zhanghao 你的账号 --mima 你的密码
    python3 skill_api.py quota
    python3 skill_api.py report --birth "1991-09-21 14:45" --place 北屯 --country 中国 --gender 男 --save ./reports

账号默认存 ~/.xix-bazi/account.json，注册/登录成功后自动写入；
后续命令不传 --zhanghao/--mima 时自动读取。
"""
import argparse
import gzip
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = os.environ.get("BAZI_API", "https://api.xinjianxue.com/api/xinjianxue/skill")
ACCOUNT_PATH = Path.home() / ".xix-bazi" / "account.json"


def _post(path, payload, timeout=240):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"success": False, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"success": False, "error": f"网络错误: {e}"}


def load_account():
    try:
        return json.loads(ACCOUNT_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_account(zhanghao, mima):
    ACCOUNT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ACCOUNT_PATH.write_text(json.dumps({"zhanghao": zhanghao, "mima": mima},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(ACCOUNT_PATH, 0o600)
    except OSError:
        pass


def creds(args):
    acc = load_account()
    return (getattr(args, "zhanghao", None) or acc.get("zhanghao"),
            getattr(args, "mima", None) or acc.get("mima"))


def cmd_register(args):
    r = _post("/register", {"zhanghao": args.zhanghao, "mima": args.mima})
    if r.get("success"):
        save_account(args.zhanghao, args.mima)
        print(f"注册成功：{args.zhanghao}，当前可用次数 {r.get('cishu', 0)} 次")
        print(f"账号已保存在：{ACCOUNT_PATH}")
    else:
        print("注册失败：", r.get("error"))
    return 0 if r.get("success") else 1


def cmd_quota(args):
    z, m = creds(args)
    if not z or not m:
        print("本地没有账号，请先注册：python3 skill_api.py register --zhanghao X --mima Y")
        return 1
    r = _post("/quota", {"zhanghao": z, "mima": m})
    if r.get("success"):
        print(f"账号 {r.get('zhanghao')} 可用次数：{r.get('cishu')}")
        return 0
    print("查询失败：", r.get("error"))
    return 1


def cmd_report(args):
    z, m = creds(args)
    if not z or not m:
        print("本地没有账号，请先注册")
        return 1
    payload = {"zhanghao": z, "mima": m, "birth": args.birth,
               "place": args.place, "gender": args.gender}
    if args.country:
        payload["country"] = args.country
    r = _post("/report", payload)
    if not r.get("success"):
        print("生成失败：", r.get("error"))
        return 1

    print(f"资产名：{r.get('asset')}")
    print(f"下载链接：{r.get('url')}")
    print(f"命中缓存：{'是' if r.get('hit') else '否'}  剩余次数：{r.get('cishu')}")

    if args.save:
        outdir = Path(args.save).expanduser()
        outdir.mkdir(parents=True, exist_ok=True)
        dst = outdir / (r["asset"] + ".json")
        # urllib 默认不声明 Accept-Encoding，服务端回明文
        req = urllib.request.Request(r["url"])
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
        dst.write_bytes(data)
        print(f"报告已保存：{dst.resolve()}")
        print(f"文件大小：{len(data) / 1048576:.2f} MB")
    return 0


def main():
    ap = argparse.ArgumentParser(description="八字 skill 客户端")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("register")
    p.add_argument("--zhanghao", required=True)
    p.add_argument("--mima", required=True)
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("quota")
    p.add_argument("--zhanghao")
    p.add_argument("--mima")
    p.set_defaults(func=cmd_quota)

    p = sub.add_parser("report")
    p.add_argument("--birth", required=True, help="YYYY-MM-DD HH:MM")
    p.add_argument("--place", required=True, help="出生地，至少精确到市")
    p.add_argument("--country", help="国家，用于区分重名地点")
    p.add_argument("--gender", required=True, choices=["男", "女"])
    p.add_argument("--save", help="报告保存目录")
    p.add_argument("--zhanghao")
    p.add_argument("--mima")
    p.set_defaults(func=cmd_report)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
