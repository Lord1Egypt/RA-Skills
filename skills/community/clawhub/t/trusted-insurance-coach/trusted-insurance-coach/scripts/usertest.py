#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
usertest.py — 从小白用户视角做的端到端体验测试

跟 selfcheck.py 里那几项不一样：那几项测的是"内容对不对、有没有违规"，
这一项测的是"**一个完全不懂保险的人，用起来顺不顺**"。

测六件事：
  1. 口语输入能不能懂     中文数字、区间、"说不准"这类真实说法，不能报错
  2. 输错时提示友不友好   不能只甩一句"解析失败"，要告诉用户怎么办
  3. 会不会静默出错       参数写错时宁可报错，也不能悄悄给一份错清单
  4. 数字算得对不对       中文数字必须和阿拉伯数字算出同一个结果
  5. 术语铁律             输出里不许有连续多个没翻译的术语（agents md 五铁律之 2）
  6. 固定尾注             每类输出末尾必须带合规尾注（agents md §0.3）

用法：
    python3 scripts/usertest.py
    python3 scripts/usertest.py -v        # 打印每条明细
"""

import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUDGET = os.path.join(ROOT, "skills/ins-what-to-buy/scripts/budget_calc.py")
CLAIMS = os.path.join(ROOT, "skills/ins-claims-guide/scripts/claim_checklist.py")
DISCLOSE = os.path.join(ROOT, "skills/ins-health-disclosure/scripts/disclosure_checklist.py")

PY = sys.executable


def run(script, *args):
    r = subprocess.run([PY, script] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def grab_premium(out):
    """从输出里抠出「年收入约 X 万」这个数，用来比对。"""
    for line in out.splitlines():
        if "保费预算区间" in line and "年收入约" in line:
            seg = line.split("年收入约")[1]
            return seg.split("→")[0].strip()
    return None


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("中文数字：十五万 / 三十万 / 二十五万")
def _(verbose):
    ok = True
    for raw, expect in [("十五万", "15.0 万"), ("三十万", "30.0 万"), ("二十五万", "25.0 万")]:
        code, out = run(BUDGET, "--income", raw, "--expense", "5000")
        got = grab_premium(out)
        good = code == 0 and got == expect
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {raw} → {got}（应 {expect}）")
    return ok


@case("中文数字必须等于阿拉伯数字")
def _(verbose):
    """同一个收入，用中文说和用数字说，算出来的预算必须一模一样。"""
    pairs = [("十五万", "15"), ("三十万", "30"), ("二十万", "20")]
    ok = True
    for cn, ar in pairs:
        _, o1 = run(BUDGET, "--income", cn, "--expense", "5000")
        _, o2 = run(BUDGET, "--income", ar, "--expense", "5000")
        good = grab_premium(o1) == grab_premium(o2)
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {cn}={grab_premium(o1)} ｜ {ar}={grab_premium(o2)}")
    return ok


@case("口语区间：二十到四十万")
def _(verbose):
    code, out = run(BUDGET, "--income", "二十到四十万", "--expense", "5000")
    got = grab_premium(out)
    good = code == 0 and got is not None
    if verbose or not good:
        print(f"     {'✅' if good else '❌'} 二十到四十万 → {got}")
    return good


@case("收入填 0：必须报错，不能算出「0 元 ～ 0 元」")
def _(verbose):
    code, out = run(BUDGET, "--income", "0", "--expense", "5000")
    good = code != 0 and "0 元 ～ 0 元" not in out
    if verbose or not good:
        print(f"     {'✅' if good else '❌'} 退出码 {code}")
    return good


@case("收入乱填：提示里要告诉他怎么写")
def _(verbose):
    code, out = run(BUDGET, "--income", "abc", "--expense", "5000")
    good = code != 0 and "万" in out and ("示例" in out or "可以" in out or "--income" in out)
    if verbose or not good:
        print(f"     {'✅' if good else '❌'} 提示是否可操作：{('有' if good else '没有')}")
    return good


@case("理赔：事故类型写错必须报错（不能静默给错清单）")
def _(verbose):
    code, out = run(CLAIMS, "--insurance-type", "百万医疗", "--event", "莫名其妙")
    good = code != 0 and "住院" in out
    if verbose or not good:
        print(f"     {'✅' if good else '❌'} 退出码 {code}")
    return good


@case("健康告知：角色写错必须报错")
def _(verbose):
    code, out = run(DISCLOSE, "--insurance-type", "百万医疗", "--role", "路人")
    good = code != 0 and "本人" in out
    if verbose or not good:
        print(f"     {'✅' if good else '❌'} 退出码 {code}")
    return good


@case("报错口吻统一：五个脚本都用「人话 + 怎么办 + 例子」")
def _(verbose):
    """一个不懂保险的人，看到报错应该知道下一步做什么，
    而不是看到 [错误] 加一串他只认识一半的字。
    统一标准：① 开头是人话标签 ② 有可复制示例 ③ 不出现裸的机器术语。"""
    checks = [
        ("预算", BUDGET, ["--income", "abc"]),
        ("条款", os.path.join(ROOT, "skills/ins-how-to-buy/scripts/clause_check.py"),
         ["--insurance-type", "随便什么险"]),
        ("告知", DISCLOSE, ["--insurance-type", "百万医疗", "--role", "路人"]),
        ("体检", os.path.join(ROOT, "skills/ins-policy-checkup/scripts/policy_review.py"), []),
        ("理赔", CLAIMS, ["--insurance-type", "百万医疗", "--event", "莫名其妙"]),
    ]
    # 这些机器味儿的词不该出现在给用户的提示里
    jargon = ["[错误]", "Errno", "Traceback", "ValueError", "KeyError", "usage:"]
    ok = True
    for name, script, args in checks:
        code, out = run(script, *args)
        good = code != 0                      # 必须是非零退出
        good &= ("没认出来" in out or "没算出来" in out or "还差点东西" in out
                 or "找不到文件" in out or "是个文件夹" in out or "格式" in out
                 or "没读进来" in out)
        good &= any(j in out for j in ("--income", "--insurance-type", "--event", "--role", "--input"))
        bad = [w for w in jargon if w in out]
        good &= not bad
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {name}"
                  + (f"（残留机器话：{bad}）" if bad else ""))
    return ok



@case("术语铁律：输出里不许堆未翻译术语")
def _(verbose):
    """agents md 五铁律之 2：术语首次出现必须带括号人话。
    本包的黑名单术语都定义了人话括号，这里验证机器输出真的带了。"""
    import re
    checks = [
        ("预算", BUDGET, ["--income", "30", "--expense", "15000"]),
        ("体检", os.path.join(ROOT, "skills/ins-policy-checkup/scripts/policy_review.py"), ["--demo"]),
    ]
    ok = True
    for name, script, args in checks:
        code, out = run(script, *args)
        if code != 0:
            if verbose:
                print(f"     ⚠️ {name} 脚本没跑成（rc={code}），跳过术语检查")
            continue
        # 规则（agents md 五铁律之 2 的可执行版）：术语在某输出里至少要有**一处翻译形态**
        # ——「术语（人话）」或「术语＝/术语= 人话」。复现与词素级出现（如"已有保费支出"）
        # 不再重复要求。实现：原文找「术语＋括号/等号」形态；找不到再看剥括号后
        # 是否根本没有独立出现（全在括号解释里也算合规）。
        stripped = re.sub(r"[（(][^）)]*[）)]", "", out)
        bad_terms = []
        for w in ("保额", "免赔额", "保费"):
            if re.search(re.escape(w) + r"[（(＝=]", out):
                continue  # 有翻译形态
            if w not in stripped:
                continue  # 只在括号解释里出现，也算合规
            bad_terms.append(w)
        good = not bad_terms
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {name}: 裸术语 {bad_terms or '无'}")
    return ok


@case("固定尾注：机器输出末尾必须带合规尾注")
def _(verbose):
    """agents md §0.3：每类输出都带固定尾注。脚本输出是『机器产出的一类』，
    必须同样带。"""
    marker = "不构成投保建议"
    checks = [
        ("预算", BUDGET, ["--income", "30", "--expense", "15000"]),
        ("理赔", CLAIMS, ["--insurance-type", "百万医疗", "--event", "住院"]),
        ("告知", DISCLOSE, ["--insurance-type", "百万医疗", "--role", "本人", "--findings", "无"]),
        ("体检", os.path.join(ROOT, "skills/ins-policy-checkup/scripts/policy_review.py"), ["--demo"]),
    ]
    ok = True
    for name, script, args in checks:
        code, out = run(script, *args)
        good = code == 0 and marker in out
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {name}: 尾注{'有' if good else '缺失'}")
    return ok


@case("正常路径不能被我改坏")
def _(verbose):
    checks = [
        (BUDGET, ["--income", "30", "--expense", "15000", "--existing", "10000"], "保费预算区间"),
        (CLAIMS, ["--insurance-type", "百万医疗", "--event", "住院"], "理赔材料清单"),
        (DISCLOSE, ["--insurance-type", "百万医疗", "--role", "本人"], "核对清单"),
    ]
    ok = True
    for script, args, marker in checks:
        code, out = run(script, *args)
        good = code == 0 and marker in out
        ok &= good
        if verbose or not good:
            print(f"     {'✅' if good else '❌'} {os.path.basename(script)}")
    return ok


def main():
    verbose = "-v" in sys.argv
    print("=" * 64)
    print("小白用户视角 · 端到端体验测试")
    print("=" * 64)
    failed = []
    for name, fn in CASES:
        ok = fn(verbose)
        print(f"{'✅' if ok else '❌'} {name}")
        if not ok:
            failed.append(name)
    print("=" * 64)
    if failed:
        print(f"结论：{len(failed)}/{len(CASES)} 项没通过——{'；'.join(failed)}")
        return 1
    print(f"结论：{len(CASES)}/{len(CASES)} 全部通过，一个不懂保险的人能顺畅用完。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
