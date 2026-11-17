#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inject_self_improve.py — 给一组技能批量注入通用自进化学习系统。

对未拥有的技能：复制 learner.py 到 scripts/、初始化 learned_patterns.json、
在 SKILL.md 末尾追加「自进化学习系统」章节。已拥有的技能自动跳过（幂等）。
"""
import os, sys, shutil

KIT = os.path.dirname(os.path.abspath(__file__))
LEARNER_SRC = os.path.join(KIT, "learner.py")
SECTION_SRC = os.path.join(KIT, "section.md")
SKILLS_BASE = os.path.expanduser("~/.workbuddy/skills")
PY = r"C:\Users\小江\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# 待注入技能（已具备自进化能力的 auto-publisher-self-learning / archive-smart-reader 不在其中）
TARGETS = [
    "resume-interview-coach", "ecommerce-ops-assistant", "personal-health-manager",
    "smart-travel-planner", "personal-finance-tracker", "legal-assistant-pro",
    "video-creator-assistant", "task-time-manager", "exam-study-assistant",
    "data-privacy-guardian",
    "cross-border-listing-optimizer", "faceless-video-automation",
    "content-matrix-factory", "digital-template-factory",
    "shop-savvy", "home-renovation-planner", "complaint-letter-pro",
    "kids-homework-helper",
]

def has_section(md_path):
    if not os.path.exists(md_path):
        return False
    txt = open(md_path, encoding="utf-8").read()
    return ("自进化学习系统" in txt) or ("learned_patterns" in txt)

def inject(skill):
    d = os.path.join(SKILLS_BASE, skill)
    if not os.path.isdir(d):
        return (skill, "MISSING")
    md = os.path.join(d, "SKILL.md")
    if not os.path.exists(md):
        return (skill, "NO_SKILL_MD")
    # 1) 已拥有 -> 跳过
    if has_section(md):
        return (skill, "SKIP_ALREADY_HAS")
    # 2) 复制 learner.py
    scripts = os.path.join(d, "scripts")
    os.makedirs(scripts, exist_ok=True)
    shutil.copyfile(LEARNER_SRC, os.path.join(scripts, "learner.py"))
    # 3) 初始化 learned_patterns.json
    import subprocess
    r = subprocess.run([PY, os.path.join(scripts, "learner.py"), "init", d],
                       capture_output=True, text=True)
    # 4) 追加章节
    section = open(SECTION_SRC, encoding="utf-8").read()
    with open(md, "a", encoding="utf-8") as f:
        f.write(section)
    return (skill, "OK")

def main():
    print(f"注入目标数: {len(TARGETS)}")
    for s in TARGETS:
        skill, status = inject(s)
        print(f"  {skill:32} -> {status}")

if __name__ == "__main__":
    main()
