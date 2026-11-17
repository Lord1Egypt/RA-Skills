#!/usr/bin/env python3
"""Generate a routing index from existing clusters and skill packages."""

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import project_paths
from audit_skill_index import (
    DISTILL,
    INDEX,
    LEGACY,
    OUT,
    PROJECT,
    ROOT,
    SKILL,
    cluster_aliases,
    extract_clusters,
    list_skill_packs,
    matches,
    norm,
)

ROUTING = ROOT / "references" / "技能路由索引.md"
ROUTING_CONFIG = ROOT / "references" / "技能路由配置.md"

CORE_CLUSTERS = {
    "识人观察簇",
    "谎言与可信度簇",
    "认知与决策簇",
    "战略与竞争簇",
    "系统与规模簇",
    "治理与历史簇",
    "心性修养簇",
    "管理与人本簇",
    "社会与群体簇",
    "情感与关系簇",
    "表达与论证簇",
    "对话沟通簇",
    "投资与市场簇",
    "法律与权益执行簇",
    "高生产力与叙事创作簇",
}

MANUAL_ROUTES = {
    "书籍蒸馏/中国法律基础蒸馏/skills/劳动法与劳动争议/SKILL.md": ["法律与权益执行簇"],
    "书籍蒸馏/就业利息和货币通论蒸馏/skills/就业利息和货币通论/SKILL.md": ["系统与规模簇"],
    "书籍蒸馏/疯传与传染蒸馏/skills/疯传与传染/SKILL.md": ["社会与群体簇"],
}

SOURCE_MAP = {
    "书籍蒸馏/早期基础理论蒸馏/skills/挺经/SKILL.md": "书籍蒸馏/曾国藩蒸馏/books/tingjing/input/挺经-原典-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/冰鉴/SKILL.md": "书籍蒸馏/曾国藩蒸馏/books/bingjian/input/冰鉴-原典-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/孙子兵法/SKILL.md": "书籍蒸馏/曾国藩蒸馏/books/sunzi/input/孙子兵法-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/道德经/SKILL.md": "书籍蒸馏/诸子四书蒸馏/books/daodejing/input/道德经-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/易经/SKILL.md": "书籍蒸馏/诸子四书蒸馏/books/yijing/input/易经-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/庄子/SKILL.md": "书籍蒸馏/诸子四书蒸馏/books/zhuangzi/input/庄子-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/鬼谷子/SKILL.md": "书籍蒸馏/诸子四书蒸馏/books/guiguzi/input/鬼谷子-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/思考好与坏/SKILL.md": "其他书籍/心理学三书/思考好与坏/input/思考好与坏-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/思考快与慢/SKILL.md": "其他书籍/心理学三书/思考快与慢/input/思考快与慢-clean.txt",
    "书籍蒸馏/早期基础理论蒸馏/skills/乌合之众/SKILL.md": "其他书籍/心理学三书/乌合之众/input/乌合之众-clean.txt",
}

SOURCES = []


def load_routing_config():
    config = {}
    current = None
    for line in ROUTING_CONFIG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line.strip())
        if m:
            current = m.group(2).strip()
            config[current] = {"trigger": "", "exclude": ""}
        elif current:
            if line.startswith("- trigger:"):
                config[current]["trigger"] = line.split(":", 1)[1].strip()
            elif line.startswith("- exclude:"):
                config[current]["exclude"] = line.split(":", 1)[1].strip()
    return config


def section_lines(path, pattern):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for line in text.splitlines():
        if re.match(pattern, line.strip()):
            lines.append(re.sub(r"^[-*#]+\s*", "", line.strip()))
    return lines


def pack_skills(path):
    headings = section_lines(path, r"^##\s+\d+\.\s*")
    return "；".join(headings[:8]) or "见技能包正文"


def source_score(name, key):
    name_key = norm(name)
    if not key or not name_key:
        return 0
    if name_key in key or key in name_key:
        return 1.0
    return SequenceMatcher(None, name_key, key).ratio()


def find_source(path, key):
    mapped = SOURCE_MAP.get(str(path.relative_to(PROJECT)))
    if mapped:
        return mapped
    project_root = path.parents[2]
    root_prefix = str(project_root.relative_to(PROJECT))
    parent_prefix = (
        str(project_root.parent.relative_to(PROJECT))
        if project_root.parent != PROJECT
        else ""
    )
    candidates = []
    for name, rel in SOURCES:
        score = max(
            source_score(name, key),
            source_score(name, norm(path.parent.name)),
        )
        if rel.startswith(root_prefix):
            score += 0.4
        elif parent_prefix and rel.startswith(parent_prefix):
            score += 0.15
        candidates.append((score, name, rel))
    if not candidates:
        return ""
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][2]


def cluster_meta(cluster):
    meta = {"trigger": "", "exclude": "", "core": ""}
    for line in cluster["text"].splitlines():
        stripped = line.strip()
        if stripped.startswith("- 核心判断尺"):
            meta["core"] = stripped.split("：", 1)[-1].strip()
        elif stripped.startswith("- 边界"):
            meta["exclude"] = stripped.split("：", 1)[-1].strip()
        elif stripped.startswith("- 触发"):
            meta["trigger"] = stripped.split("：", 1)[-1].strip()
    routing_config = load_routing_config()
    if cluster["name"] in routing_config:
        meta["trigger"] = routing_config[cluster["name"]]["trigger"] or meta["trigger"]
        meta["exclude"] = routing_config[cluster["name"]]["exclude"] or meta["exclude"]
    if not meta["trigger"]:
        members = "、".join(cluster["members"][:12])
        meta["trigger"] = f"{cluster['name']}相关场景；成员：{members}"
    return meta


def package_protocols() -> list[str]:
    """包内 references/*.md —— 不依赖外部项目就能用的协议清单。"""
    refs = ROOT / "references"
    return sorted(p.stem for p in refs.glob("*.md") if p.is_file())


def main():
    if PROJECT == ROOT:
        # 没解析到外部项目根：索引/技能包都不存在，不能凭空生成。
        print(project_paths.project_dir_help(), file=sys.stderr)
        print("已跳过路由索引重建；包内 SKILL.md 与 references/ 不受影响。", file=sys.stderr)
        return 2
    clusters = extract_clusters(INDEX.read_text(encoding="utf-8"))
    packs = list_skill_packs(DISTILL)
    for candidate in sorted(DISTILL.rglob("*")):
        if candidate.suffix not in {".txt", ".md"}:
            continue
        if "skills" in candidate.parts or "SKILL" in candidate.name:
            continue
        SOURCES.append((candidate.name, str(candidate.relative_to(PROJECT))))
    for candidate in sorted(LEGACY.rglob("*")):
        if candidate.suffix not in {".txt", ".md"}:
            continue
        if "skills" in candidate.parts or "SKILL" in candidate.name:
            continue
        SOURCES.append((candidate.name, str(candidate.relative_to(PROJECT))))
    skill_text = SKILL.read_text(encoding="utf-8")

    matched = {}
    unmatched = []
    main_links = len(set(re.findall(r"书籍蒸馏/[^` )]+SKILL\.md", skill_text)))
    for pack in packs:
        matched_clusters = []
        for cluster in clusters:
            if matches(pack["key"], cluster_aliases(cluster)):
                matched_clusters.append(cluster["name"])
        matched_clusters += MANUAL_ROUTES.get(str(pack["path"]), [])
        matched_clusters = list(dict.fromkeys(matched_clusters))
        if not matched_clusters:
            unmatched.append(pack)
        else:
            for name in matched_clusters:
                matched.setdefault(name, []).append(pack)

    lines = [
        "# 司马光综合思维 · 技能路由索引（自动生成）",
        "",
        "> 本文件由 `scripts/build_skill_index.py` 自动生成，不手工编辑。",
        "> 源数据：`references/技能合并索引.md`、`references/技能路由配置.md`；技能包：`书籍蒸馏/*/skills/*/SKILL.md`；原书：各项目 `input/`。",
        "",
        "## 先说清楚：这是本地扩展索引，技能包独立可用",
        "",
        "下面 28 个簇指向的 `书籍蒸馏/.../skills/.../SKILL.md` 是**作者本地项目里的蒸馏产物**，",
        "不随技能包发布。缺它们时本技能照样能用——判断尺、协议、模板、脚本全在包内 `references/`：",
        "",
        f"包内协议 {len(package_protocols())} 份：" + "、".join(f"`{name}`" for name in package_protocols()),
        "",
        "用法差别只有一条：",
        "",
        "- 有外部项目（设置了 `SIMAGUANG_PROJECT_DIR`）：按簇路由到具体书籍技能包，能引用原书出处。",
        "- 没有外部项目：按 `SKILL.md` 的「协议索引」直接加载包内协议，出处标注写「未接入书籍技能包」。",
        "",
        "本文件是给「有项目的人」看的加速索引，不是技能包的依赖清单。",
        "",
        "## 统计",
        "",
        f"- 能力簇：{len(clusters)}",
        f"- 技能包：{len(packs)}",
        f"- 已路由：{len(packs) - len(unmatched)}",
        f"- 待路由：{len(unmatched)}",
        f"- 主 SKILL 直接技能包路径：{main_links}",
        "",
        "## 使用方式",
        "",
        "1. 先判断问题属于哪个能力簇。",
        "2. 打开对应簇，选择匹配的技能包。",
        "3. 按需读取技能包 `SKILL.md`。",
        "4. 需要验证出处时，打开该技能包对应的原书路径。",
        "",
        "## 反馈记录",
        "",
        "- 暂无；路由失败或用户纠正后追加到 `references/技能路由反馈日志.md`，复盘后更新 `references/技能路由配置.md`。",
        "",
    ]

    for cluster in clusters:
        meta = cluster_meta(cluster)
        load = "core" if cluster["name"] in CORE_CLUSTERS else "full"
        lines += [
            f"## {cluster['num']}. {cluster['name']}",
            "",
            f"- 触发场景：{meta['trigger']}",
            f"- 排除场景：{meta['exclude'] or '待人工补充'}",
            f"- 核心判断尺：{meta['core'] or '见成员技能包'}",
            f"- 优先级：high",
            f"- 加载深度：{load}",
            "- 技能包：",
        ]
        cluster_packs = matched.get(cluster["name"], [])
        if not cluster_packs:
            lines.append("  - 暂无自动匹配；待路由确认。")
        for pack in cluster_packs:
            source = find_source(PROJECT / pack["path"], pack["key"])
            source_text = f"原书 `{source}`" if source else "原书待补"
            lines.append(
                f"  - {pack['title'] or pack['path'].name}：核心 `{pack_skills(PROJECT / pack['path'])}`；技能包 `{pack['path']}`；{source_text}"
            )
        lines.append("")

    lines += ["## 待路由", ""]
    if unmatched:
        for pack in unmatched:
            lines.append(f"- {pack['title'] or pack['path']}：`{pack['path']}`")
    else:
        lines.append("- 无")
    lines.append("")

    ROUTING.write_text("\n".join(lines), encoding="utf-8")
    print(f"routing={ROUTING}")
    print(f"clusters={len(clusters)} routed={len(packs) - len(unmatched)} pending={len(unmatched)}")


if __name__ == "__main__":
    main()
