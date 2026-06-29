#!/usr/bin/env python3
"""
x-skill-updater check.py — 检查所有 skill 更新
用法: python3 check.py

逻辑：
  1. 扫描 OPENCLAW_HOME/skills/，读取每个 skill 的 _meta.json + SKILL.md
  2. 按来源分发检查：
     - skillhub → COS bucket index（比对 version + publishedAt + 校验 ownerId）
     - clawhub  → clawhub.ai API（比对 version + publishedAt + 校验 ownerId + 校验 slug/homepage/metadata）
     - custom   → 跳过
  3. 生成检查报告发给用户，由用户决定是否更新

本地文件字段（全部纳入核对）：

_meta.json（skillhub + clawhub 共有）：
  ownerId, slug, version, publishedAt

SKILL.md — skillhub 来源特征：
  author, version（与 _meta.json 互为备份）

SKILL.md — clawhub 来源特征：
  slug（目录名以外的有效 slug）
  homepage（包含 clawic.com）
  metadata.clawdbot（clawhub 专属安装配置）

版本优先级：_meta.json.version > SKILL.md.version
"""
import subprocess, sys, json, re, urllib.request
from pathlib import Path
from datetime import datetime

# ============ 配置 ============
SKILLHUB_COS = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills.json"
CLAWHUB_API  = "https://clawhub.ai/api/skill?slug="

# 相对于本脚本所在位置定位 OpenClaw 根目录
# 脚本在：.../x-skill-updater/scripts/check.py
# 向上两级得到 x-skill-updater/，再向上一级得到 skills/ 的父目录 = OpenClaw 根目录
SKILL_DIR     = Path(__file__).parent.parent
OPENCLAW_HOME = SKILL_DIR.parent.parent

SOURCES_FILE = SKILL_DIR / "data" / "skill-sources.json"
PENDING_FILE = SKILL_DIR / "data" / "pending-sources.json"
REPORT_PATH  = SKILL_DIR / "data" / "last-report.md"

# ============ 工具函数 ============

def fetch_json(url, timeout=15):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            data = json.loads(r.read())
            return data if isinstance(data, (dict, list)) else None
    except Exception as e:
        print(f"[警告] 获取 {url} 失败: {e}", file=sys.stderr)
        return None


def semver_cmp(v1, v2):
    def parse(s):
        return [int(x) for x in re.sub(r'[^0-9.].*', '', str(s)).split('.') if x]
    a, b = parse(v1), parse(v2)
    return (a > b) - (a < b)


def ts_to_date(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d")
    except Exception:
        return ""


def read_frontmatter(text):
    """
    解析 SKILL.md YAML frontmatter，返回键值对字典。
    兼容有无 --- 包裹两种格式。
    """
    lines = text.split("\n")
    fm = {}
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            in_fm = not in_fm
            continue
        if not in_fm:
            break
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"')
    return fm


# ============ 第1步：扫描已安装 skill ============

def get_local_skills():
    """
    扫描 OPENCLAW_HOME/skills/，读取：
      _meta.json：ownerId, slug, version, publishedAt
      SKILL.md：author, version, slug, homepage, metadata
    """
    result = {}
    # 扫描所有 skills 目录：
    #   1. ~/.openclaw/skills/（全局共享）
    #   2. ~/.openclaw/workspace-*/skills/（各 workspace 私有）
    skills_dirs = [OPENCLAW_HOME / "skills"]
    for wp in OPENCLAW_HOME.glob("workspace-*"):
        wp_skills = wp / "skills"
        if wp_skills.exists():
            skills_dirs.append(wp_skills)

    for skills_dir in skills_dirs:
        if not p.is_dir() or p.name.startswith((".", "{")):
            continue

        skill_name = p.name

        # ── _meta.json ───────────────────────────────────────
        owner_id = ""
        meta_slug = ""
        meta_ver  = ""
        meta_pub  = ""

        meta_path = p / "_meta.json"
        if meta_path.exists():
            try:
                m = json.loads(meta_path.read_text())
                owner_id = m.get("ownerId", "")
                meta_slug = m.get("slug", "")
                meta_ver  = m.get("version", "")
                meta_pub  = str(m.get("publishedAt", ""))
            except Exception:
                pass

        # ── SKILL.md frontmatter ─────────────────────────────
        skillmd_path = p / "SKILL.md"
        fm = {}
        skillmd_text = ""
        if skillmd_path.exists():
            try:
                skillmd_text = skillmd_path.read_text()
                fm = read_frontmatter(skillmd_text)
            except Exception:
                pass

        skillmd_ver     = fm.get("version", "")
        skillmd_author  = fm.get("author", "")
        skillmd_slug    = fm.get("slug", "")
        skillmd_homepage = fm.get("homepage", "")
        skillmd_metadata = fm.get("metadata", "")

        # 版本：_meta.json 优先，SKILL.md 作备用
        final_ver = meta_ver or skillmd_ver

        result[skill_name] = {
            "path":              str(p),
            "version":           final_ver,
            "ownerId":           owner_id,
            "slug":              meta_slug or skillmd_slug or skill_name,
            "publishedAt":       meta_pub,
            # SKILL.md 字段
            "skillmd_version":   skillmd_ver,
            "skillmd_author":    skillmd_author,
            "skillmd_slug":      skillmd_slug,
            "skillmd_homepage":  skillmd_homepage,
            "skillmd_metadata":  skillmd_metadata,
        }

    return result


def load_sources():
    if SOURCES_FILE.exists():
        try:
            return json.loads(SOURCES_FILE.read_text())
        except Exception:
            pass
    return {}


def save_pending(entries):
    PENDING_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))
    print(f"[提示] 新 skill 已写入待确认列表: {PENDING_FILE}", file=sys.stderr)


# ============ 第2步：查询 remote 数据 ============

_cos_index = None

def get_skillhub_index():
    global _cos_index
    if _cos_index is not None:
        return _cos_index
    data = fetch_json(SKILLHUB_COS)
    if not data:
        _cos_index = {}
        return _cos_index
    result = {}
    for s in data.get("skills", []):
        slug = s.get("slug", "")
        if not re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9_]*$', slug):
            continue
        result[slug] = s
    _cos_index = result
    return result


def query_clawhub(slug):
    """
    查询 clawhub.ai API，返回：
      version, author (=owner.handle),
      publishedAt (=latestVersion.createdAt，毫秒时间戳),
      slug, homepage, metadata
    """
    data = fetch_json(CLAWHUB_API + slug)
    if not data:
        return None
    lv    = data.get("latestVersion", {})
    owner = data.get("owner", {})
    skill = data.get("skill", {})
    return {
        "version":     lv.get("version", ""),
        "author":      owner.get("handle", ""),
        "publishedAt": str(lv.get("createdAt", "")),
        "slug":        skill.get("slug", ""),
        "homepage":    f"https://clawhub.ai/skills/{slug}",
        "metadata":    data.get("metadata", {}).get("clawdbot", {}),
    }


# ============ 第3步：核对并比较版本 ============

def check_skill(name, local, sources):
    """
    单 skill 检查，返回 (badge, label, detail)
    核对项（全部来自本地文件）：
      _meta.json: ownerId, slug, version, publishedAt
      SKILL.md:   author, version, slug, homepage, metadata
    """
    local_ver     = local["version"]
    local_oid     = local["ownerId"]
    local_slug    = local["slug"]
    local_pub     = local["publishedAt"]

    # SKILL.md 字段（clawhub 来源特征）
    skillmd_slug     = local.get("skillmd_slug", "")
    skillmd_homepage = local.get("skillmd_homepage", "")
    skillmd_metadata = local.get("skillmd_metadata", "")
    skillmd_author   = local.get("skillmd_author", "")

    entry     = sources.get(name, {})
    source    = entry.get("source", "unknown")
    entry_oid = entry.get("ownerId", "")
    note      = entry.get("note", "")

    # slug 决策链：entry.slug > _meta.json.slug > SKILL.md.slug > name
    def resolve_slug():
        if entry.get("slug"):
            return entry["slug"], f"entry slug={entry['slug']}"
        if local_slug and local_slug != name:
            return local_slug, f"_meta.json slug={local_slug}"
        if skillmd_slug and skillmd_slug != name:
            return skillmd_slug, f"SKILL.md slug={skillmd_slug}"
        return name, f"目录名={name}"

    # ── custom ────────────────────────────────────────────────
    if source == "custom":
        return ("manual", "🔧", f"来源 custom（{note}），本地 {local_ver or '无版本记录'}")

    # ── 未知来源 ──────────────────────────────────────────────
    if source not in ("skillhub", "clawhub"):
        return ("unknown", "❓", f"来源未知（{source}），本地 {local_ver}，请补充 skill-sources.json")

    check_slug, slug_src = resolve_slug()

    # ── skillhub ─────────────────────────────────────────────
    if source == "skillhub":
        index = get_skillhub_index()
        if check_slug not in index:
            return ("unknown", "❓",
                    f"skillhub 来源但 COS index 中无此 slug（{check_slug}），本地 {local_ver}，请检查 slug")

        remote      = index[check_slug]
        remote_ver  = remote.get("version", "")
        remote_pub  = str(remote.get("publishedAt", ""))

        if not remote_ver and not local_ver:
            return ("unknown", "⚠️", f"本地/SKILL.md version=({local_ver})，COS version=({remote_ver})，版本信息不完整）")

        # 版本核对
        cmp = semver_cmp(local_ver, remote_ver) if (local_ver and remote_ver) else 0

        # publishedAt 核对（发布源头时间戳）
        pub_note = ""
        if local_pub and remote_pub:
            if local_pub < remote_pub:
                pub_note = f" [⚠️ COS 发布时间更晚：本地 {ts_to_date(local_pub)} < COS {ts_to_date(remote_pub)}]"
            elif local_pub > remote_pub:
                pub_note = f" [⚠️ 本地发布时间晚于 COS：本地 {ts_to_date(local_pub)} > COS {ts_to_date(remote_pub)}]"

        # 作者特征
        author_note = ""
        if skillmd_author:
            author_note = f"，作者={skillmd_author}"

        if cmp == 0 and not pub_note:
            return ("uptodate", "✅",
                    f"{local_ver}（skillhub: {remote_ver}）{slug_src}{author_note}")
        elif cmp > 0:
            return ("custom_higher", "🟡",
                    f"本地 {local_ver} > skillhub {remote_ver}（定制版，不降级 ✓）{slug_src}{pub_note}{author_note}")
        elif cmp < 0:
            return ("update_available", "🆕",
                    f"🆕 {local_ver} → {remote_ver}（skillhub）{slug_src}{pub_note}{author_note}")
        else:
            return ("unknown", "⚠️",
                    f"本地 {local_ver}，COS {remote_ver}（版本信息不完整）{slug_src}")

    # ── clawhub ──────────────────────────────────────────────
    remote = query_clawhub(check_slug)
    if not remote or not remote.get("version"):
        return ("unknown", "❓",
                f"clawhub 来源但 API 无数据（{slug_src}），本地 {local_ver}")

    remote_ver  = remote["version"]
    remote_auth = remote["author"]
    remote_pub  = remote["publishedAt"]
    remote_date = ts_to_date(remote_pub)
    remote_slug = remote.get("slug", "")

    # ownerId 决策链：entry.ownerId > _meta.json.ownerId
    ownerId_to_check = entry_oid or local_oid

    # ── ownerId 校验 ──────────────────────────────────────
    author_warn = ""
    if ownerId_to_check and remote_auth and ownerId_to_check != remote_auth:
        author_warn = f" [⚠️ ownerId 不一致：本地 {ownerId_to_check} ≠ remote {remote_auth}]"

    # ── SKILL.md 特征校验 ─────────────────────────────────
    clawhub_warns = []

    # homepage 校验
    if skillmd_homepage and "clawic.com" in skillmd_homepage:
        if check_slug and check_slug not in skillmd_homepage:
            clawhub_warns.append(f"SKILL.md homepage 与 slug 不匹配（{skillmd_homepage}）")

    # metadata.clawdbot 存在 = 强烈支持 clawhub 来源
    clawhub_marker = "metadata.clawdbot" if skillmd_metadata else ""

    clawhub_note = ""
    if clawhub_warns:
        clawhub_note = " " + " | ".join(clawhub_warns)
    if clawhub_marker:
        clawhub_note += f" [{clawhub_marker} ✓]"

    # ── publishedAt 核对 ──────────────────────────────────
    pub_note = ""
    if local_pub and remote_pub:
        if local_pub < remote_pub:
            pub_note = f" [⚠️ API 发布时间更晚：本地 {ts_to_date(local_pub)} < remote {remote_date}]"
        elif local_pub > remote_pub:
            pub_note = f" [⚠️ 本地发布时间晚于 remote：本地 {ts_to_date(local_pub)} > remote {remote_date}]"

    extra = f"，发布于 {remote_date}" if remote_date else ""

    if not remote_ver or not local_ver:
        detail = (f"本地 {local_ver}，clawhub {remote_ver}（版本信息不完整）"
                  f"{author_warn}{pub_note}{extra}{slug_src}{clawhub_note}")
        return ("unknown", "⚠️", detail)

    cmp = semver_cmp(local_ver, remote_ver)

    if cmp == 0 and not pub_note and not author_warn:
        return ("uptodate", "✅",
                f"{local_ver}（clawhub: {remote_ver}）{slug_src}{author_warn}{extra}{clawhub_note}")
    elif cmp > 0:
        return ("custom_higher", "🟡",
                f"本地 {local_ver} > clawhub {remote_ver}（定制版，不降级 ✓）{slug_src}{author_warn}{pub_note}{extra}{clawhub_note}")
    elif cmp < 0:
        changelog = ""
        if remote.get("changelog"):
            changelog = f"\n  📝 更新说明：{remote['changelog'][:80]}..."
        return ("update_available", "🆕",
                f"🆕 {local_ver} → {remote_ver}（clawhub）{slug_src}{author_warn}{pub_note}{extra}{changelog}{clawhub_note}")
    else:
        return ("unknown", "⚠️",
                f"本地 {local_ver}，clawhub {remote_ver}{author_warn}{pub_note}{extra}{slug_src}{clawhub_note}")


# ============ 第4步：生成报告 ============

def collect_hints(name, info):
    """
    收集未知 skill 的线索，全部来自本地文件。
    """
    path = Path(info.get("path", str(OPENCLAW_HOME / "skills" / name)))
    hints = {
        "name":              name,
        "version":           info.get("version", ""),
        "ownerId":           info.get("ownerId", ""),
        "slug":              info.get("slug", ""),
        "publishedAt":       info.get("publishedAt", ""),
        "publishedAt_date":  ts_to_date(info.get("publishedAt", "")),
        "skillmd_version":   info.get("skillmd_version", ""),
        "skillmd_author":    info.get("skillmd_author", ""),
        "skillmd_slug":      info.get("skillmd_slug", ""),
        "skillmd_homepage":  info.get("skillmd_homepage", ""),
        "skillmd_metadata":  info.get("skillmd_metadata", ""),
        "dir_structure":     [],
    }

    try:
        hints["dir_structure"] = [p.name for p in path.iterdir()
                                  if p.is_dir() and not p.name.startswith(".")]
    except Exception:
        pass

    return hints


def main():
    sources = load_sources()
    local  = get_local_skills()
    index  = get_skillhub_index()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# 🔧 Skill 检查 — {now}\n"]
    lines.append("> 规则：不降级 ✓ | 全量字段核对（_meta.json + SKILL.md）| custom → 手动\n")

    updates = []; latest = []; manuals = []; warns = []; unknowns = []
    pending_entries = []

    for name, info in sorted(local.items()):
        badge, label, detail = check_skill(name, info, sources)
        lines.append(f"- {name} {badge}: {detail}")

        if badge == "🆕":
            m = re.search(r"([0-9][0-9.]*) → ([0-9][0-9.]*)", detail)
            updates.append((name,
                            m.group(1) if m else info["version"],
                            m.group(2) if m else "?"))
        elif badge in ("✅", "🟡"):
            latest.append((name, info["version"]))
        elif badge == "🔧":
            manuals.append((name, detail))
        elif badge == "⚠️":
            warns.append((name, detail))
        elif badge == "❓":
            hints = collect_hints(name, info)
            unknowns.append((name, detail, hints))
            pending_entries.append(hints)

    lines.append("\n---\n\n## 📋 摘要\n")

    if updates:
        lines.append(f"🆕 **{len(updates)} 个可升级**：\n")
        for s, lv, nv in updates:
            lines.append(f"  - **{s}**: `{lv}` → `{nv}`\n")
        lines.append("\n回复「更新」征得同意后执行升级。\n")
    else:
        lines.append("✅ 所有 skill 均已最新或为定制版，无需升级。\n")

    if latest:
        lines.append(f"\n✅ **{len(latest)} 个已是最新或定制版**：\n")
        for s, v in latest:
            lines.append(f"  - **{s}**: `{v}`\n")

    if manuals:
        lines.append(f"\n🔧 **{len(manuals)} 个手动检查**（custom 来源）：\n")
        for s, d in manuals:
            lines.append(f"  - **{s}**: {d}\n")

    if warns:
        lines.append(f"\n⚠️ **{len(warns)} 个需关注**：\n")
        for s, d in warns:
            lines.append(f"  - **{s}**: {d}\n")

    if unknowns:
        lines.append(f"\n❓ **{len(unknowns)} 个来源不明**（请回复来源）：\n")
        for s, d, hints in unknowns:
            lines.append(f"\n### `{s}`\n")
            if hints["ownerId"]:
                lines.append(f"- _meta.json ownerId: `{hints['ownerId']}`\n")
            if hints["slug"]:
                lines.append(f"- _meta.json slug: `{hints['slug']}`\n")
            if hints["version"]:
                lines.append(f"- _meta.json version: `{hints['version']}`\n")
            if hints["publishedAt_date"]:
                lines.append(f"- _meta.json publishedAt: `{hints['publishedAt_date']}`\n")
            if hints["skillmd_author"]:
                lines.append(f"- SKILL.md author: `{hints['skillmd_author']}`\n")
            if hints["skillmd_slug"]:
                lines.append(f"- SKILL.md slug: `{hints['skillmd_slug']}`\n")
            if hints["skillmd_homepage"]:
                lines.append(f"- SKILL.md homepage: `{hints['skillmd_homepage']}`\n")
            if hints["skillmd_metadata"]:
                lines.append(f"- SKILL.md metadata: `{hints['skillmd_metadata']}`\n")
            if hints["dir_structure"]:
                lines.append(f"- 目录结构: {', '.join(hints['dir_structure'])}\n")
            lines.append(f"> 回复格式：`{s} → clawhub` / `{s} → custom` / `{s} → skillhub`\n")

    report = "".join(lines)
    REPORT_PATH.write_text(report)
    print(report)

    if pending_entries:
        save_pending(pending_entries)

    print(f"\n报告已存档: {REPORT_PATH}", file=sys.stderr)
    sys.exit(1 if updates else 0)


if __name__ == "__main__":
    main()
