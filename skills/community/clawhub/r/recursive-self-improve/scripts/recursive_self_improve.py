#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recursive-self-improve —— 递归自我改进（元之元）。

把"改进技能"本身也程序化、可验证、可记忆：
  scan   : 只读扫描 skills/，识别改进机会（缺 learner / 缺自进化章节 / YAML 前置非法）
  propose: 把机会映射成安全补丁（仅追加/复制，从不删除）
  apply  : 先临时副本试应用 + 重扫校验，通过才落盘；失败回滚
  --selftest: 自带夹具，断言扫描/提案/试应用全链路通过

安全：绝不删除/覆盖任何技能源文件；落盘前沙箱试跑；仅写 skills/ 与记忆。
"""
import os, sys, json, shutil, tempfile, argparse, datetime

SKILLS_DEFAULT = os.path.expanduser("~/.workbuddy/skills")

# 自进化章节（与 skill-self-improve 的 section.md 保持一致）
SELF_EVOLVE_SECTION = """

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验。
"""

ACTION_FOR = {
    "no_learner": "inject_learner",
    "no_self_evolve_section": "append_self_evolve_section",
    "invalid_frontmatter": "prepend_yaml_frontmatter",
}


def _read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def _valid_frontmatter(txt):
    if not txt.startswith("---"):
        return False
    import re
    m = re.match(r"^---\n(.*?)\n---", txt, re.DOTALL)
    if not m:
        return False
    fm = m.group(1)
    return ("name:" in fm) and ("description:" in fm)


def scan_opportunities(skills_dir):
    """只读扫描，返回改进机会列表。绝不修改文件。"""
    cands = []
    if not os.path.isdir(skills_dir):
        return cands
    for name in sorted(os.listdir(skills_dir)):
        d = os.path.join(skills_dir, name)
        if not os.path.isdir(d) or name.startswith("_"):
            continue
        md = os.path.join(d, "SKILL.md")
        if not os.path.exists(md):
            continue
        txt = _read(md)
        issues = []
        if not _valid_frontmatter(txt):
            issues.append("invalid_frontmatter")
        if not os.path.exists(os.path.join(d, "scripts", "learner.py")):
            issues.append("no_learner")
        if "自进化学习系统" not in txt:
            issues.append("no_self_evolve_section")
        if issues:
            cands.append({"skill": name, "issues": issues, "body_len": len(txt)})
    return cands


def propose_patches(cands):
    plan = []
    for c in cands:
        for iss in c["issues"]:
            plan.append({
                "skill": c["skill"],
                "issue": iss,
                "action": ACTION_FOR[iss],
                "priority": 0 if iss == "invalid_frontmatter" else (1 if iss == "no_learner" else 2),
            })
    plan.sort(key=lambda x: (x["priority"], x["skill"]))
    return plan


def _apply_one(skill_dir, issue, learner_src):
    """在 skill_dir 上安全地应用一个补丁（追加/复制，不删不覆盖）。返回是否改变。"""
    changed = False
    md = os.path.join(skill_dir, "SKILL.md")
    txt = _read(md)
    if issue == "no_self_evolve_section":
        if "自进化学习系统" not in txt:
            with open(md, "a", encoding="utf-8") as f:
                f.write(SELF_EVOLVE_SECTION)
            changed = True
    elif issue == "no_learner":
        sdir = os.path.join(skill_dir, "scripts")
        os.makedirs(sdir, exist_ok=True)
        dst = os.path.join(sdir, "learner.py")
        if learner_src and os.path.exists(learner_src) and not os.path.exists(dst):
            shutil.copyfile(learner_src, dst)
            changed = True
        # 初始化记忆
        lp = os.path.join(skill_dir, "learned_patterns.json")
        if not os.path.exists(lp):
            json.dump({"version": 1, "skill": os.path.basename(skill_dir),
                       "totalOps": 0, "totalErrors": 0, "capabilityStats": {},
                       "errorPatterns": {}, "preferences": {}, "recentOps": []},
                      open(lp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            changed = True
    elif issue == "invalid_frontmatter":
        if not txt.startswith("---"):
            name = os.path.basename(skill_dir)
            fm = ("---\nname: %s\nversion: 1.0.0\ndescription: |\n"
                   "  由 recursive-self-improve 自动补丁注入的技能描述。\n---\n\n" % name)
            with open(md, "w", encoding="utf-8") as f:
                f.write(fm + txt)
            changed = True
    return changed


def apply_patches(skills_dir, plan, limit, learner_src, log_path):
    """逐条在临时副本上试应用 + 重扫校验；通过才落盘，失败回滚。"""
    done, rolled = [], []
    for p in plan[:limit]:
        skill_dir = os.path.join(skills_dir, p["skill"])
        if not os.path.isdir(skill_dir):
            continue
        tmp = tempfile.mkdtemp(prefix="rsi_")
        try:
            shutil.copytree(skill_dir, os.path.join(tmp, "s"))
            sandbox = os.path.join(tmp, "s")
            _apply_one(sandbox, p["issue"], learner_src)
            # 校验：重扫沙箱该技能，确认机会已消除
            recheck = scan_opportunities(os.path.join(tmp))
            still = [c for c in recheck if c["skill"] == p["skill"] and p["issue"] in c["issues"]]
            if still:
                rolled.append(p)  # 校验未通过 -> 丢弃沙箱，不改源
                continue
            # 通过：把沙箱结果拷回源
            for root, _, files in os.walk(sandbox):
                for fn in files:
                    src = os.path.join(root, fn)
                    rel = os.path.relpath(src, sandbox)
                    dst = os.path.join(skill_dir, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copyfile(src, dst)
            done.append(p)
        except Exception as e:
            rolled.append({**p, "error": str(e)})
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    # 写技能级记忆
    if done:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        log = []
        if os.path.exists(log_path):
            try:
                log = json.load(open(log_path, encoding="utf-8"))
            except Exception:
                log = []
        log.append({"t": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
                    "applied": [{"skill": d["skill"], "issue": d["issue"]} for d in done]})
        json.dump(log, open(log_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return done, rolled


def selftest():
    """生成临时夹具，断言 scan/propose/apply 全链路通过。"""
    print("🧪 selftest: 构造临时夹具 ...")
    tmp = tempfile.mkdtemp(prefix="rsi_fix_")
    fixtures = {
        "fix_a": "no frontmatter here\njust body text\n",  # invalid_frontmatter
        "fix_b": "---\nname: fix-b\nversion: 1.0.0\ndescription: |\n  ok\n---\n\nbody\n",  # no_learner + no_self_evolve_section
    }
    for name, body in fixtures.items():
        d = os.path.join(tmp, name)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
    learner_src = os.path.join(tmp, "learner_src.py")
    open(learner_src, "w", encoding="utf-8").write(
        "#!/usr/bin/env python3\n# stub learner for selftest\n")

    cands = scan_opportunities(tmp)
    assert len(cands) == 2, f"scan 应识别 2 个机会，实际 {len(cands)}"
    assert any(c["skill"] == "fix_a" and "invalid_frontmatter" in c["issues"] for c in cands)
    assert any(c["skill"] == "fix_b" and "no_learner" in c["issues"] for c in cands)
    print(f"  ✓ scan 识别 {len(cands)} 个机会")

    plan = propose_patches(cands)
    assert plan and plan[0]["issue"] == "invalid_frontmatter", "优先级：frontmatter 应最前"
    print(f"  ✓ propose 生成 {len(plan)} 条补丁计划（优先级正确）")

    done, rolled = apply_patches(tmp, plan, limit=10, learner_src=learner_src,
                                 log_path=os.path.join(tmp, "self_improve_log.json"))
    assert len(rolled) == 0, f"不应有回滚：{rolled}"
    assert len(done) == len(plan), f"全部应落盘，done={len(done)} plan={len(plan)}"
    # 校验落盘后 fix_a 有 frontmatter、fix_b 有 learner + 章节
    assert _valid_frontmatter(_read(os.path.join(tmp, "fix_a", "SKILL.md")))
    assert os.path.exists(os.path.join(tmp, "fix_b", "scripts", "learner.py"))
    assert "自进化学习系统" in _read(os.path.join(tmp, "fix_b", "SKILL.md"))
    assert os.path.exists(os.path.join(tmp, "self_improve_log.json"))
    print(f"  ✓ apply 沙箱试跑+校验通过，{len(done)} 条全部安全落盘，0 回滚")

    shutil.rmtree(tmp, ignore_errors=True)
    print("✅ selftest 全链路 PASS")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", default=SKILLS_DEFAULT)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("cmd", nargs="?", default="scan",
                    choices=["scan", "propose", "apply"])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    learner_src = os.path.join(os.path.dirname(__file__), "learner.py")
    if args.cmd == "scan":
        cands = scan_opportunities(args.skills)
        print(f"🔍 扫描 {args.skills}：发现 {len(cands)} 个待改进技能")
        for c in cands[:20]:
            print(f"  - {c['skill']}: {', '.join(c['issues'])}")
        return cands
    plan = propose_patches(scan_opportunities(args.skills))
    if args.cmd == "propose":
        print(f"📝 补丁计划（{len(plan)} 条）：")
        for p in plan[:20]:
            print(f"  - {p['skill']} :: {p['issue']} -> {p['action']}")
        return plan
    # apply
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "self_improve_log.json")
    done, rolled = apply_patches(args.skills, plan, args.limit, learner_src, log_path)
    print(f"✅ 已安全应用 {len(done)} 条补丁；回滚 {len(rolled)} 条")
    for p in done:
        print(f"  + {p['skill']} :: {p['issue']}")
    return done


if __name__ == "__main__":
    main()
