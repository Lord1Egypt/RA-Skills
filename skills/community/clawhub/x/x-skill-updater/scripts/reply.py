#!/usr/bin/env python3
"""
x-skill-updater reply.py — 解析用户对未知 skill 来源的回复，写入 skill-sources.json

用法：
  python3 reply.py "skill名 → clawhub"
  python3 reply.py "skill名 → custom"
  python3 reply.py "skill名 → skillhub"
  python3 reply.py "skill名 → custom:github:user/repo"
  python3 reply.py "skill1 → clawhub, skill2 → custom"

信息来源：全部来自本地文件（SKILL.md / _meta.json / pending-sources.json）
- 不访问网络
- clawhub 的 ownerId 直接从用户回复中推断（无需查 API）

流程：
  - 读取 pending-sources.json 获取 skill 的本地元数据线索
  - 解析用户回复的 "name → source" 格式
  - 写入 skill-sources.json（来源 / slug / ownerId / author 全部来自本地）
  - 写入后从 pending-sources.json 移除该 skill
"""
import sys, json, re
from pathlib import Path

SKILL_DIR    = Path(__file__).parent.parent
SOURCES_FILE = SKILL_DIR / "data" / "skill-sources.json"
PENDING_FILE = SKILL_DIR / "data" / "pending-sources.json"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return []


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def parse_reply(reply):
    """
    解析 "skill1 → clawhub, skill2 → custom" 格式
    返回 [(name, source, extra_note), ...]
    """
    results = []
    parts = re.split(r',\s*', reply)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r'^(.+?)\s*→\s*(.+)$', part)
        if not m:
            print(f"[跳过] 无法解析格式: {part}", file=sys.stderr)
            continue
        name = m.group(1).strip()
        rest = m.group(2).strip()

        source = "unknown"
        note   = ""
        if rest.startswith("github:"):
            source = "custom"
            note   = f"GitHub {rest}"
        elif rest in ("clawhub", "skillhub", "custom"):
            source = rest
        elif rest.startswith("github"):
            source = "custom"
            note   = "GitHub"
        else:
            source = "custom"
            note   = rest

        results.append((name, source, note))
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python3 reply.py \"skill名 → clawhub\"", file=sys.stderr)
        sys.exit(1)

    reply   = sys.argv[1]
    pending = load_json(PENDING_FILE)
    sources_raw = SOURCES_FILE.read_text() if SOURCES_FILE.exists() else "{}"
    sources = json.loads(sources_raw)

    pending_by_name = {e["name"]: e for e in pending}

    parsed  = parse_reply(reply)
    updated = []

    for name, source, note in parsed:
        entry = sources.get(name, {})
        slug  = entry.get("slug", name)

        entry["source"]     = source
        entry["check_mode"] = "manual" if source == "custom" else "auto"
        entry["slug"]       = slug
        if note:
            entry["note"] = note

        # ownerId 和 author：优先从 pending 记录补全（来自本地 _meta.json / SKILL.md）
        if name in pending_by_name:
            p = pending_by_name[name]
            # ownerId 来自 _meta.json
            if not entry.get("ownerId") and p.get("ownerId"):
                entry["ownerId"] = p["ownerId"]
            # skillmd_author 来自 SKILL.md（作为参考信息，不写入 skill-sources.json）
            skillmd_author = p.get("skillmd_author", "")
            if skillmd_author:
                entry["_local_author"] = skillmd_author

        sources[name] = entry
        updated.append(name)
        print(f"✅ 已写入 {name}: source={source}, ownerId={entry.get('ownerId', '?')}")

    save_json(SOURCES_FILE, sources)

    updated_names = {n for n, _, _ in parsed}
    remaining = [e for e in pending if e["name"] not in updated_names]
    save_json(PENDING_FILE, remaining)

    print(f"\n✅ 已更新 {len(updated)} 条: {', '.join(updated)}")
    if remaining:
        print(f"📋 还有 {len(remaining)} 个待确认: {[e['name'] for e in remaining]}")
    else:
        print(f"✅ pending 列表已清空")


if __name__ == "__main__":
    main()