"""Novelty check: overlaps with the local skill library.

Library sources: ~/.openclaw/skills, ~/.openclaw/workspace/skills,
$OPENCLAW_SKILLS_DIR and the offline ClawHub cache ~/.openclaw/clawhub.
If no library is reachable the module warns ('no library') instead of
failing — that is a warning, not an error.
"""

import difflib
import os
import re
from pathlib import Path

TEMPLATE_DESC_RE = re.compile(
    r"^(описание|description|a skill that|todo|tbd|навык|skill)\b", re.I)
EXAMPLES_HEADING_RE = re.compile(
    r"(?m)^\s*#{1,4}\s*(Examples|Примеры|Usage|Использование)\b")
# Copy suffixes: vibo-memory-MASTER / vibo-memory-backup / my-skill-v2 /
# skill-vibo-memory-MASTER-20260813_211353 (dated copy) are copies of the
# SAME skill, not duplicates of someone else's.
COPY_SUFFIX_RE = re.compile(
    r"[-_.\s]?(?:master|backup|bak|copy|clone|old|new|test|tmp|orig|work|v\d+)(?:[-_][\d_]{6,16})?$",
    re.I)


def _norm_name(s):
    """Normalize a skill name for duplicate detection (strip copy suffixes)."""
    s = s.lower().strip()
    s = COPY_SUFFIX_RE.sub("", s)
    return s.strip("-_. ")


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


def _read_meta(md_path):
    """Minimal frontmatter reader: name/description/version (no deps)."""
    meta = {}
    try:
        text = Path(md_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return meta
    if not text.startswith("---"):
        return meta
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        line = lines[i]
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip("\"'")
    return meta


def _find_library():
    """Return a list of {folder, name, description, path} for library skills."""
    dirs = []
    env_dir = os.environ.get("OPENCLAW_SKILLS_DIR")
    if env_dir:
        dirs.append(Path(env_dir))
    home = Path.home()
    for rel in ("~/.openclaw/skills", "~/.openclaw/workspace/skills",
                "~/.openclaw/clawhub"):
        p = Path(rel).expanduser()
        if p != home and p.exists():
            dirs.append(p)
    entries = []
    seen = set()
    for base in dirs:
        if not base.is_dir():
            continue
        for md in sorted(base.rglob("SKILL.md")):
            folder = md.parent.name
            key = str(md)
            if key in seen:
                continue
            seen.add(key)
            meta = _read_meta(md)
            entries.append({
                "folder": folder,
                "name": str(meta.get("name") or folder),
                "description": str(meta.get("description") or ""),
                "path": str(md),
            })
    return entries


def _exclude_self(entries, skill_path):
    """Drop the skill under test itself from the library — otherwise a skill
    installed inside a library folder is reported as colliding with itself."""
    skip = Path(skill_path).resolve()
    return [e for e in entries if Path(e["path"]).resolve().parent != skip]


class NoveltyCheck:
    name = "novelty"
    title = {"ru": "Новизна", "en": "Novelty"}

    def run(self, ctx):
        t = ctx.t
        checks = []
        skill = Path(ctx.skill_path)
        md = skill / "SKILL.md"
        meta = _read_meta(md) if md.exists() else {}
        name = str(meta.get("name") or skill.name).lower()
        description = str(meta.get("description") or "")

        library = _find_library()
        if not library:
            checks.append(_check("library_reachable", "pass",
                                 t("check.library_reachable.none")))
            checks.append(_check("name_collision", "pass",
                                 t("check.name_collision.ok")))
            checks.append(_check("description_overlap", "pass",
                                 t("check.description_overlap.ok")))
            library = []
        else:
            library = _exclude_self(library, ctx.skill_path)
            lib_dirs = []
            env_dir = os.environ.get("OPENCLAW_SKILLS_DIR")
            if env_dir and Path(env_dir).is_dir():
                lib_dirs.append(env_dir)
            for rel in ("~/.openclaw/skills", "~/.openclaw/workspace/skills",
                        "~/.openclaw/clawhub"):
                p = Path(rel).expanduser()
                if p.is_dir():
                    lib_dirs.append(str(p))
            checks.append(_check("library_reachable", "pass",
                                 t("check.library_reachable.ok",
                                   dirs=", ".join(lib_dirs[:3]))))

            # 1. name collision (exact duplicate = fail; copy of SAME skill
            #    (e.g. -MASTER/-backup/-v2 or copy-suffixed folder) = warn)
            name_norm = _norm_name(name)
            same_name = [e for e in library
                         if e["name"].lower() == name
                         and not COPY_SUFFIX_RE.search(e["folder"])]
            same_norm = [e for e in library
                         if (e["name"].lower() != name
                             and _norm_name(e["name"]) == name_norm)
                         or (e["name"].lower() == name
                             and COPY_SUFFIX_RE.search(e["folder"]))]
            same_folder = [e for e in library
                           if e["folder"].lower() == skill.name.lower()]
            if same_name:
                checks.append(_check("name_collision", "fail",
                                     t("check.name_collision.fail",
                                       skills=", ".join(
                                           e["folder"] for e in same_name[:3]))))
            elif same_norm:
                checks.append(_check("name_collision", "warn",
                                     t("check.name_collision.warn",
                                       skills=", ".join(
                                           e["folder"] for e in same_norm[:3]))))
            elif same_folder:
                checks.append(_check("name_collision", "warn",
                                     t("check.name_collision.warn",
                                       skills=", ".join(
                                           e["folder"] for e in same_folder[:3]))))
            else:
                checks.append(_check("name_collision", "pass",
                                     t("check.name_collision.ok")))

            # 2. description overlap (max() must compare ratios only — equal
            #    ratios crash on dict comparison)
            if description.strip():
                best = max(
                    ((difflib.SequenceMatcher(
                        None, description.lower(), e["description"].lower()).ratio(), e)
                     for e in library if e["description"]),
                    default=(0.0, None),
                    key=lambda x: x[0])
                ratio, entry = best
                if entry and ratio >= 0.85:
                    checks.append(_check("description_overlap", "fail",
                                         t("check.description_overlap.fail",
                                           ratio=round(ratio, 2),
                                           skill=entry["folder"])))
                elif entry and ratio >= 0.6:
                    checks.append(_check("description_overlap", "warn",
                                         t("check.description_overlap.warn",
                                           ratio=round(ratio, 2),
                                           skill=entry["folder"])))
                else:
                    checks.append(_check("description_overlap", "pass",
                                         t("check.description_overlap.ok")))
            else:
                checks.append(_check("description_overlap", "warn",
                                     t("check.description_overlap.nodesc")))

        # 3. description not empty / not a template
        desc = description.strip()
        if len(desc) < 20 or TEMPLATE_DESC_RE.match(desc.lower()):
            checks.append(_check("description_not_empty", "fail",
                                 t("check.description_not_empty.fail")))
        else:
            checks.append(_check("description_not_empty", "pass",
                                 t("check.description_not_empty.ok", n=len(desc))))

        # 4. has examples
        md_text = md.read_text(encoding="utf-8", errors="replace") if md.exists() else ""
        if EXAMPLES_HEADING_RE.search(md_text) or "```" in md_text:
            checks.append(_check("has_examples", "pass",
                                 t("check.has_examples.ok")))
        else:
            checks.append(_check("has_examples", "warn",
                                 t("check.has_examples.warn")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        verdict = (t("check.novelty.duplicate")
                   if any(c["name"] in ("name_collision", "description_overlap")
                          and c["status"] == "fail" for c in checks)
                   else t("check.novelty.value"))
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        details += f" — {verdict}"
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}
