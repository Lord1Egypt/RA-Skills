#!/usr/bin/env python3
"""Check core integration files and print a health summary."""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
PROJECT = (
    ROOT.parents[1]
    if (ROOT.parents[1] / "书籍蒸馏").exists()
    else Path.home() / "Documents/Codex/2026-07-30/new-chat/资治通鉴蒸馏"
)

REQUIRED = [
    "SKILL.md",
    "test-prompts.json",
    "references/方法网络.md",
    "references/素材来源索引.md",
    "references/核心概念索引.md",
    "references/技能合并索引.md",
    "references/技能路由索引.md",
    "references/技能路由配置.md",
    "references/技能路由反馈日志.md",
    "references/技能异同表.md",
    "references/调用优化协议.md",
    "references/知识蒸馏日志.md",
    "references/自我学习日志.md",
    "references/学习循环协议.md",
    "references/对话与身份适配协议.md",
    "references/变化时空象数模块协议.md",
    "references/推演决策时机协议.md",
    "references/溯源标注协议.md",
    "references/高生产力服务协议.md",
    "references/高生产力协作分工协议.md",
    "references/高生产力场景模板.md",
    "references/能力转工作成果清单.md",
    "references/AI影视工具与提示词协议.md",
    "references/小说剧本融合创作协议.md",
    "references/高生产力输出自检清单.md",
    "references/高生产力反馈闭环协议.md",
    "references/事实与数据核验协议.md",
    "references/行业模板与评审标准库.md",
    "references/专业边界与复核清单.md",
    "scripts/verify_traceability.py",
    "scripts/check_distillation_quality.py",
    "scripts/review_learning_log.py",
    "scripts/build_traceability_panel.py",
    "scripts/generate_work_product.py",
    "scripts/build_handoff.py",
    "scripts/run_high_productivity_checks.py",
    "scripts/archive_work_product_feedback.py",
    "scripts/test_routing_coverage.py",
]

def main():
    ok = True
    for rel in REQUIRED:
        path = ROOT / rel
        exists = path.exists()
        ok = ok and exists
        print(f"{'OK' if exists else 'MISSING'} {rel}")

    prompts_path = ROOT / "test-prompts.json"
    if prompts_path.exists():
        data = json.loads(prompts_path.read_text(encoding="utf-8"))
        cases = data.get("test_cases", [])
        print(f"test_cases: {len(cases)}")
    else:
        ok = False

    routing_path = ROOT / "references" / "技能路由索引.md"
    if routing_path.exists():
        routing_text = routing_path.read_text(encoding="utf-8", errors="ignore")
        pack_paths = re.findall(r"技能包 `(书籍蒸馏/[^`]+)`", routing_text)
        source_paths = re.findall(r"原书 `((?:书籍蒸馏|其他书籍)/[^`]+)`", routing_text)
        missing = [
            path
            for path in pack_paths + source_paths
            if not (PROJECT / path).exists()
        ]
        print(f"routing_pack_links: {len(pack_paths)} source_links: {len(source_paths)} missing_links: {len(missing)}")
        for path in missing[:20]:
            print(f"MISSING_ROUTING_PATH {path}")
        ok = ok and not missing
    else:
        ok = False
        print("MISSING references/技能路由索引.md")

    main_skill_text = SKILL.read_text(encoding="utf-8", errors="ignore")
    main_routing = {
        (name, load)
        for name, load in re.findall(
            r"^\| \d+ \| ([^|]+?) \| (core|full) \|$",
            main_skill_text,
            re.MULTILINE,
        )
    }
    routing_clusters = []
    current_num = None
    current_name = None
    for line in routing_text.splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line.strip())
        if m:
            current_num = int(m.group(1))
            current_name = m.group(2).strip()
        elif line.startswith("- 加载深度：") and current_num is not None:
            load = line.split("：", 1)[1].strip()
            routing_clusters.append((current_name, load))
            current_num = None
    routing_set = set(routing_clusters)
    print(f"main_routing_rows: {len(main_routing)} routing_clusters: {len(routing_set)}")
    if main_routing != routing_set:
        ok = False
        print("ROUTING_TABLE_MISMATCH")
        missing = routing_set - main_routing
        extra = main_routing - routing_set
        for item in sorted(missing):
            print(f"MISSING_MAIN_ROUTING {item}")
        for item in sorted(extra):
            print(f"EXTRA_MAIN_ROUTING {item}")

    config_path = ROOT / "references" / "技能路由配置.md"
    if config_path.exists():
        config_text = config_path.read_text(encoding="utf-8", errors="ignore")
        config_sections = re.findall(r"^## \d+\. ", config_text, re.MULTILINE)
        missing_fields = []
        current = None
        has_trigger = False
        has_exclude = False
        for line in config_text.splitlines():
            m = re.match(r"^## (\d+)\. (.+)$", line.strip())
            if m:
                if current is not None and (not has_trigger or not has_exclude):
                    missing_fields.append(current)
                current = m.group(2).strip()
                has_trigger = False
                has_exclude = False
            elif current:
                if line.startswith("- trigger:"):
                    has_trigger = True
                elif line.startswith("- exclude:"):
                    has_exclude = True
        if current is not None and (not has_trigger or not has_exclude):
            missing_fields.append(current)
        print(f"routing_config_sections: {len(config_sections)} missing_fields: {len(missing_fields)}")
        if len(config_sections) != 28 or missing_fields:
            ok = False
            for item in missing_fields:
                print(f"MISSING_ROUTING_CONFIG_FIELD {item}")
    else:
        ok = False
        print("MISSING references/技能路由配置.md")

    routing_test = ROOT / "scripts" / "test_routing_coverage.py"
    if routing_test.exists():
        result = subprocess.run(
            [sys.executable, str(routing_test)],
            capture_output=True,
            text=True,
        )
        stdout = result.stdout.strip()
        if stdout:
            print(" | ".join(stdout.splitlines()[-2:]))
        if result.returncode != 0:
            ok = False
            print("ROUTING_ACCURACY_FAIL")
    else:
        ok = False
        print("MISSING scripts/test_routing_coverage.py")

    summary_path = PROJECT / "司马光综合思维-全量总结.md"
    list_path = PROJECT / "学习记录" / "已蒸馏书籍全清单-2026-08-14.md"
    if summary_path.exists() and list_path.exists():
        summary = summary_path.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"已并入 (\d+) 个蒸馏项目、(\d+) 个书籍/文本条目、(\d+) 个能力簇", summary)
        listed = sum(1 for line in list_path.read_text(encoding="utf-8", errors="ignore").splitlines() if re.match(r"^\d+\.", line.strip()))
        if match:
            projects, books, clusters = map(int, match.groups())
            state_ok = books == listed
            print(f"state: projects={projects}, books={books}, listed={listed}, clusters={clusters}")
            ok = ok and state_ok
            if not state_ok:
                print("STATE_MISMATCH books vs listed")
        else:
            ok = False
            print("STATE_MISMATCH summary pattern not found")

    print("INTEGRATION_OK" if ok else "INTEGRATION_INCOMPLETE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
