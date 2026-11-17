#!/usr/bin/env python3
"""Audit current skill index coverage without modifying routing files."""

import datetime
import re
from pathlib import Path

import project_paths

ROOT = Path(__file__).resolve().parents[1]
PROJECT = project_paths.find_project_dir() or ROOT
INDEX = ROOT / "references" / "技能合并索引.md"
SKILL = ROOT / "SKILL.md"
DISTILL = PROJECT / "书籍蒸馏"
LEGACY = PROJECT / "其他书籍"
OUT = (PROJECT / "学习记录" / "技能索引审计.md") if PROJECT != ROOT else (ROOT / "handoff" / "技能索引审计.md")


def norm(text):
    text = re.sub(r"[《》]", "", text.strip())
    text = re.sub(r"[（(].*?[)）]", "", text)
    text = re.split("技能包", text)[0]
    return re.sub(r"[\s:：\-_—/\\,，、;；.。]+", "", text).lower()


def extract_clusters(text):
    clusters = []
    current = None
    for line in text.splitlines():
        m = re.match(r"^##\s+(\d+)\.\s*(.+)$", line.strip())
        if m:
            if current:
                clusters.append(current)
            current = {
                "num": int(m.group(1)),
                "name": m.group(2).strip(),
                "members": [],
                "text": "",
            }
            continue
        if current is not None:
            current["text"] += line + "\n"
            mm = re.match(r"^\s*[-*]\s*(?:成员|成员补充)\s*[:：]\s*(.*)$", line.strip())
            if mm:
                for part in re.split(r"[,，、;；]", mm.group(1)):
                    part = re.sub(r"\[[^\]]*\]|`[^`]*`|\*\*[^*]*\*\*", "", part).strip()
                    if part:
                        current["members"].append(part)
    if current is not None:
        clusters.append(current)
    return clusters


def list_skill_packs(root, require_skills=True):
    packs = []
    for path in sorted(root.rglob("SKILL.md")):
        if require_skills and "/skills/" not in str(path):
            continue
        rel = path.relative_to(PROJECT)
        title = ""
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines()[:20]:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        packs.append(
            {
                "path": rel,
                "title": title,
                "key": norm(title) or norm(path.parent.name),
                "root": root.name,
            }
        )
    return packs


def cluster_aliases(cluster):
    aliases = {norm(cluster["name"])}
    aliases.update(norm(member) for member in cluster["members"])
    return {alias for alias in aliases if alias}


def matches(key, aliases):
    key = norm(key)
    if not key:
        return False
    for alias in aliases:
        if alias and (alias in key or key in alias):
            return True
    return False


def main():
    index_text = INDEX.read_text(encoding="utf-8")
    skill_text = SKILL.read_text(encoding="utf-8")
    clusters = extract_clusters(index_text)
    packs = list_skill_packs(DISTILL)
    legacy = list_skill_packs(LEGACY, require_skills=False)

    matched = {}
    unmatched = []
    for pack in packs:
        found = False
        for cluster in clusters:
            if matches(pack["key"], cluster_aliases(cluster)):
                matched.setdefault(cluster["name"], []).append(pack)
                found = True
                break
        if not found:
            unmatched.append(pack)

    direct_links = len(set(re.findall(r"书籍蒸馏/[^` )]+SKILL\.md", skill_text)))
    index_links = len(set(re.findall(r"书籍蒸馏/[^` )]+SKILL\.md", index_text)))

    lines = [
        f"# 技能索引审计（{datetime.date.today().isoformat()}）",
        "",
        "## 统计",
        "",
        f"- 能力簇：{len(clusters)}",
        f"- 书籍蒸馏技能包：{len(packs)}",
        f"- 历史对照技能包（其他书籍）：{len(legacy)}",
        f"- 已归入簇的技能包：{len(packs) - len(unmatched)}",
        f"- 未归入簇的技能包：{len(unmatched)}",
        f"- 主 SKILL 直接技能包路径：{direct_links}",
        f"- 技能合并索引直接技能包路径：{index_links}",
        "",
        "## 各簇技能包覆盖",
        "",
        "| 簇 | 匹配技能包数 |",
        "| --- | --- |",
    ]
    for cluster in clusters:
        lines.append(f"| {cluster['name']} | {len(matched.get(cluster['name'], []))} |")

    lines += ["", "## 未归入簇的技能包", ""]
    if unmatched:
        for pack in unmatched:
            lines.append(f"- {pack['title'] or pack['path']}：`{pack['path']}`")
    else:
        lines.append("- 无")

    lines += ["", "## 说明", ""]
    lines.append(
        "- 本审计只检查现有索引与技能包的对应关系，不修改主 SKILL、技能合并索引或技能包。"
    )
    lines.append("- 未归入簇不代表技能缺失，可能因为索引成员名与技能包标题未统一，需要进一步核对。")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"clusters={len(clusters)} packs={len(packs)} matched={len(packs) - len(unmatched)} unmatched={len(unmatched)}")
    print(f"main_skill_direct_links={direct_links} index_direct_links={index_links}")
    print(f"report={OUT}")


if __name__ == "__main__":
    main()
