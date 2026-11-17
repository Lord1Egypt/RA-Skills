import argparse, json, sys

REQUIRED = ["代币总量", "分配方案", "锁仓", "团队", "风险提示"]
PROMISE = ["保证收益", "稳赚", "保本", "翻倍", "无风险"]

def main():
    ap = argparse.ArgumentParser(description="token-disclosure-check · 代币信息披露完备性检查（零依赖）")
    ap.add_argument("--text", required=True, help="白皮书/披露文案全文或要点")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = a.text
    missing = [k for k in REQUIRED if k not in t]
    promised = [k for k in PROMISE if k in t]
    problems = []
    if missing:
        problems.append("缺少必备披露要素：" + "、".join(missing))
    if promised:
        problems.append("含收益承诺类表述（" + "、".join(promised) + "）——披露不得作收益保证")
    if a.json:
        print(json.dumps({"pass": not problems, "required": REQUIRED, "missing": missing,
                          "promise_hits": promised, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        print("必备要素核查：")
        for k in REQUIRED:
            print(("  [x] " if k in t else "  [ ] ") + k)
        print("  判定：" + ("PASS 披露完备且无收益承诺" if not problems else "FAIL"))
        for p in problems:
            print("    - " + p)
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
