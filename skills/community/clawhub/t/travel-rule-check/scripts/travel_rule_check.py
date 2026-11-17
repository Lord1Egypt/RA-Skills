#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""travel-rule-check — 链上资产旅行规则(VASP)校验纵深工具（零依赖）。
校验转账是否含收发方KYC(姓名+账号/地址+地理)，超阈(1000USD等值)强制。
理论真源：LGD 凡自治之物三律（SynomosAI）。"""
import argparse, json, sys
NAME = "travel-rule-check"
THRESHOLD = 1000
def check(tx):
    amt = float(tx.get("amount", 0) or 0)
    o = tx.get("originator") or {}
    b = tx.get("beneficiary") or {}
    need = amt >= THRESHOLD
    missing = []
    for role, party in (("发起方", o), ("受益方", b)):
        name = party.get("name")
        acct = party.get("account") or party.get("address")
        geo = party.get("geo")
        if not name: missing.append(role + "缺姓名")
        if not acct: missing.append(role + "缺账号/地址")
        if need and not geo: missing.append(role + "缺地理信息(超阈)")
    return {"amount": amt, "need_kyc": need, "missing": missing, "compliant": len(missing) == 0}
def main():
    ap = argparse.ArgumentParser(description=NAME + " · 旅行规则校验")
    ap.add_argument("--tx", help="转账 JSON: {originator:{name,account,geo}, beneficiary:{...}, amount}")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.tx: print("用法: --tx <JSON>", file=sys.stderr); sys.exit(2)
    try: tx = json.loads(a.tx)
    except Exception as e: print("tx JSON 解析失败: " + str(e), file=sys.stderr); sys.exit(2)
    r = check(tx)
    if a.json: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 旅行规则校验 ===")
        print("  缺失: " + (",".join(r["missing"]) or "无"))
        print("  结论: " + ("合规 ✅" if r["compliant"] else "违规 ⛔"))
    sys.exit(0 if r["compliant"] else 1)
if __name__ == "__main__":
    main()
