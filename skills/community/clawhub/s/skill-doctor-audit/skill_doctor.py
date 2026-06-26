#!/usr/bin/env python3
"""
skill_doctor.py - Audit your installed OpenClaw skills.

Zero external dependencies (uses PyYAML if present, falls back to a built-in
parser otherwise). Scans a directory of installed skills and reports:

  * conflicts  - skills whose triggers overlap (the agent may fire the wrong one)
  * stale      - skills behind their latest ClawHub version (best effort)
  * security   - inline red flags in SKILL.md / scripts (exfiltration, RCE, secrets)
  * which      - given a prompt, rank which skill is most likely to fire

Usage:
  python skill_doctor.py audit [--skills-dir DIR] [--json]
  python skill_doctor.py conflicts [--skills-dir DIR] [--threshold 0.30]
  python skill_doctor.py security [--skills-dir DIR] [--json]
  python skill_doctor.py stale [--skills-dir DIR]
  python skill_doctor.py which "the prompt to test" [--skills-dir DIR]

If --skills-dir is omitted, common OpenClaw locations are auto-detected.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Skill discovery
# --------------------------------------------------------------------------- #

CANDIDATE_DIRS = [
    os.environ.get("OPENCLAW_SKILLS_DIR", ""),
    "~/.openclaw/skills",
    "~/.openclaw/extensions",
    "/data/.openclaw/skills",
    "/data/.openclaw/extensions",
    "/usr/local/lib/node_modules/openclaw/extensions",
    "~/.claude/skills",
]


def find_skills_dir(explicit: str | None) -> Path | None:
    """Pick the first directory that actually contains skills."""
    candidates = [explicit] if explicit else CANDIDATE_DIRS
    for raw in candidates:
        if not raw:
            continue
        p = Path(os.path.expanduser(raw))
        if p.is_dir() and any(_iter_skill_dirs(p)):
            return p
    return None


def _iter_skill_dirs(root: Path):
    """Yield immediate child dirs that look like a skill (have a SKILL.md)."""
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            yield child


# --------------------------------------------------------------------------- #
# Frontmatter parsing (PyYAML if available, otherwise a tolerant fallback)
# --------------------------------------------------------------------------- #

def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    raw = m.group(1)
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return _mini_yaml(raw)


def _mini_yaml(raw: str) -> dict:
    """Parse just the top-level scalar keys we care about (name/version/description).

    Handles single-line scalars, quoted strings, and >- / |- block scalars.
    Good enough for skill frontmatter; not a general YAML engine.
    """
    out: dict = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block, i = [], i + 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                block.append(lines[i].strip())
                i += 1
            out[key] = " ".join(b for b in block if b)
            continue
        if val:
            out[key] = val.strip("\"'")
        i += 1
    return out


# --------------------------------------------------------------------------- #
# Skill model + trigger extraction
# --------------------------------------------------------------------------- #

STOPWORDS = set(
    """a an the and or of to for in on with use used using when this that these those
    your you their it its as at by from into about over via if then else not no any all
    can could should would may might will shall do does done is are be been being have has
    had also more most some such per etc eg ie also key triggers trigger covers user users
    skill skills claude openclaw clawdbot agent request requests asks want wants need needs
    help also like e.g i.e
    what who whom whose when where why how which whether
    i we us our ours my mine me you yours he she his her hers they them theirs
    get got make made just out up off down each other others new specific various""".split()
)

QUOTE_RE = re.compile(r"['\"]([^'\"]{2,60}?)['\"]")
WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9\-]{2,}")


class Skill:
    def __init__(self, path: Path):
        self.path = path
        self.dir_name = path.name
        fm = parse_frontmatter(path / "SKILL.md")
        self.name = str(fm.get("name") or path.name)
        self.version = str(fm.get("version")) if fm.get("version") is not None else ""
        self.description = str(fm.get("description") or "")
        self.quoted = self._quoted_triggers()
        self.keywords = self._keywords()

    def _quoted_triggers(self) -> set[str]:
        out: set[str] = set()
        for q in QUOTE_RE.findall(self.description):
            t = q.strip().lower().rstrip(",.;:!?")
            if not t:
                continue
            # A single quoted function word ('what', 'who', 'or') is not a real
            # trigger - only keep distinctive single words or multi-word phrases.
            if " " not in t and (len(t) < 4 or t in STOPWORDS):
                continue
            out.add(t)
        return out

    def _keywords(self) -> set[str]:
        words = {w.lower() for w in WORD_RE.findall(self.description)}
        words |= {w for q in self.quoted for w in WORD_RE.findall(q.lower())}
        return {w for w in words if w not in STOPWORDS and len(w) > 2}


def load_skills(skills_dir: Path) -> list[Skill]:
    return [Skill(d) for d in _iter_skill_dirs(skills_dir)]


# --------------------------------------------------------------------------- #
# Conflict detection
# --------------------------------------------------------------------------- #

def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_conflicts(skills: list[Skill], threshold: float = 0.20) -> list[dict]:
    conflicts = []
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            s1, s2 = skills[i], skills[j]
            shared_quotes = s1.quoted & s2.quoted
            kw_overlap = _jaccard(s1.keywords, s2.keywords)
            # Conflict = an identical explicit trigger phrase, OR high keyword overlap.
            if shared_quotes or kw_overlap >= threshold:
                conflicts.append(
                    {
                        "skill_a": s1.name,
                        "skill_b": s2.name,
                        "keyword_overlap": round(kw_overlap, 2),
                        "shared_triggers": sorted(shared_quotes),
                        "shared_keywords": sorted((s1.keywords & s2.keywords))[:12],
                    }
                )
    conflicts.sort(key=lambda c: (len(c["shared_triggers"]), c["keyword_overlap"]), reverse=True)
    return conflicts


# --------------------------------------------------------------------------- #
# "Which skill fires?" scoring
# --------------------------------------------------------------------------- #

def which_skill(skills: list[Skill], prompt: str) -> list[dict]:
    p_words = {w.lower() for w in WORD_RE.findall(prompt)} - STOPWORDS
    p_lower = prompt.lower()
    scored = []
    for s in skills:
        # explicit quoted phrase appearing in the prompt is a very strong signal
        phrase_hits = [q for q in s.quoted if q and q in p_lower]
        kw_hits = p_words & s.keywords
        score = 3 * len(phrase_hits) + len(kw_hits)
        if score:
            scored.append(
                {
                    "skill": s.name,
                    "score": score,
                    "matched_phrases": phrase_hits[:5],
                    "matched_keywords": sorted(kw_hits)[:8],
                }
            )
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


# --------------------------------------------------------------------------- #
# Security red-flag scan
# --------------------------------------------------------------------------- #

# (pattern, severity, human explanation)
SECURITY_RULES = [
    (re.compile(r"curl\s+[^|\n]*\|\s*(?:sudo\s+)?(?:bash|sh|zsh)\b"), "high",
     "Pipes a downloaded script straight into a shell (remote code execution)."),
    (re.compile(r"wget\s+[^|\n]*\|\s*(?:sudo\s+)?(?:bash|sh)\b"), "high",
     "Pipes a downloaded script straight into a shell (remote code execution)."),
    (re.compile(r"base64\s+(?:-d|--decode|-D)\b.*\|\s*(?:bash|sh)"), "high",
     "Decodes base64 and executes it - classic obfuscated payload."),
    (re.compile(r"\beval\s*\(\s*(?:requests|urllib|fetch|http)", re.I), "high",
     "Evaluates content fetched from the network."),
    (re.compile(r"(?:id_rsa|\.ssh/|\.aws/credentials|\.npmrc|\.netrc)"), "high",
     "References private credential files (possible exfiltration)."),
    (re.compile(r"\b(?:ghp_|gho_|github_pat_|sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|xoxb-)"), "high",
     "Looks like a hard-coded secret / API token committed in the skill."),
    (re.compile(r"requests\.(?:post|put)\([^)]*os\.environ", re.I), "high",
     "Sends environment variables to a remote server (credential exfiltration)."),
    (re.compile(r"\brm\s+-rf\s+(?:/|~|\$HOME)\b"), "high",
     "Destructive recursive delete of a top-level path."),
    (re.compile(r"subprocess\.[A-Za-z_]+\([^)]*shell\s*=\s*True", re.I), "medium",
     "Runs a shell with shell=True - injection risk if input is untrusted."),
    (re.compile(r"\bchmod\s+777\b"), "medium",
     "Sets world-writable permissions."),
    (re.compile(r"\beval\s*\(|\bexec\s*\(", re.I), "medium",
     "Uses eval()/exec() - review what is being executed."),
    (re.compile(r"(?:nc|ncat|netcat)\s+-[a-z]*e\b"), "high",
     "Netcat reverse-shell pattern."),
    (re.compile(r"os\.environ\b.*(?:print|json\.dump|write)", re.I), "low",
     "Dumps environment variables - check the destination."),
]

SCAN_SUFFIXES = {".md", ".py", ".sh", ".bash", ".js", ".ts", ".rb", ".pl"}


def scan_security(skill: Skill) -> list[dict]:
    findings = []
    for f in sorted(skill.path.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if "node_modules" in f.parts or f.name.startswith("."):
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for n, line in enumerate(lines, 1):
            if len(line) > 1000:
                line = line[:1000]
            for pat, sev, why in SECURITY_RULES:
                if pat.search(line):
                    findings.append(
                        {
                            "severity": sev,
                            "file": str(f.relative_to(skill.path)),
                            "line": n,
                            "why": why,
                            "snippet": line.strip()[:140],
                        }
                    )
    sev_rank = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda x: sev_rank.get(x["severity"], 9))
    return findings


# --------------------------------------------------------------------------- #
# Stale-version check (best effort, uses the clawhub CLI if installed)
# --------------------------------------------------------------------------- #

def _semver_tuple(v: str):
    nums = re.findall(r"\d+", v or "")
    return tuple(int(n) for n in nums[:3]) + (0,) * (3 - len(nums[:3])) if nums else None


def check_stale(skills: list[Skill]) -> list[dict]:
    has_clawhub = shutil.which("clawhub") is not None
    out = []
    for s in skills:
        entry = {"skill": s.name, "installed": s.version or "(none)", "latest": None, "status": ""}
        if not s.version:
            entry["status"] = "missing-version"
            out.append(entry)
            continue
        latest = _clawhub_latest(s.name) if has_clawhub else None
        entry["latest"] = latest
        if latest:
            it, lt = _semver_tuple(s.version), _semver_tuple(latest)
            if it and lt:
                entry["status"] = "behind" if it < lt else "current"
        else:
            entry["status"] = "unknown" if has_clawhub else "no-clawhub-cli"
        out.append(entry)
    return out


def _clawhub_latest(name: str) -> str | None:
    for args in (["clawhub", "info", name, "--json"], ["clawhub", "search", name, "--json"]):
        try:
            r = subprocess.run(args, capture_output=True, text=True, timeout=20)
            if r.returncode != 0 or not r.stdout.strip():
                continue
            data = json.loads(r.stdout)
            if isinstance(data, dict):
                return data.get("version") or data.get("latest")
            if isinstance(data, list) and data:
                return data[0].get("version") or data[0].get("latest")
        except Exception:
            continue
    return None


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def render_audit_md(skills_dir: Path, skills: list[Skill]) -> str:
    conflicts = find_conflicts(skills)
    stale = check_stale(skills)
    sec = {s.name: scan_security(s) for s in skills}
    high = sum(1 for s in sec.values() for f in s if f["severity"] == "high")
    med = sum(1 for s in sec.values() for f in s if f["severity"] == "medium")
    behind = [e for e in stale if e["status"] == "behind"]
    nover = [e for e in stale if e["status"] == "missing-version"]

    L = []
    L.append("# Skill Doctor report")
    L.append(f"_Scanned {len(skills)} skills in `{skills_dir}`_\n")
    L.append("## Summary")
    L.append(f"- Conflicting trigger pairs: **{len(conflicts)}**")
    L.append(f"- Security flags: **{high} high**, {med} medium")
    L.append(f"- Out-of-date: **{len(behind)}** behind latest, {len(nover)} missing a version\n")

    L.append("## Trigger conflicts")
    if not conflicts:
        L.append("_No overlapping triggers found - your skills fire cleanly._\n")
    else:
        L.append("_These skills compete for the same prompts; the agent may fire the wrong one._\n")
        for c in conflicts:
            tag = "shared trigger" if c["shared_triggers"] else f"{int(c['keyword_overlap']*100)}% keyword overlap"
            L.append(f"- **{c['skill_a']}** vs **{c['skill_b']}** ({tag})")
            if c["shared_triggers"]:
                L.append(f"  - identical triggers: {', '.join(repr(t) for t in c['shared_triggers'])}")
            elif c["shared_keywords"]:
                L.append(f"  - shared keywords: {', '.join(c['shared_keywords'])}")
        L.append("")

    L.append("## Security flags")
    if high + med == 0:
        L.append("_No high or medium red flags detected._\n")
    else:
        for name, findings in sec.items():
            flagged = [f for f in findings if f["severity"] in ("high", "medium")]
            if not flagged:
                continue
            L.append(f"### {name}")
            for f in flagged:
                L.append(f"- [{f['severity'].upper()}] `{f['file']}:{f['line']}` - {f['why']}")
                L.append(f"  - `{f['snippet']}`")
            L.append("")

    L.append("## Versions")
    if behind:
        for e in behind:
            L.append(f"- **{e['skill']}**: installed {e['installed']} -> latest {e['latest']}")
    if nover:
        L.append(f"- Missing a version field: {', '.join(e['skill'] for e in nover)}")
    if not behind and not nover:
        L.append("_All skills carry a version and none are known to be behind._")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _resolve(args) -> tuple[Path, list[Skill]]:
    d = find_skills_dir(getattr(args, "skills_dir", None))
    if not d:
        print(
            "Skill Doctor could not find an installed-skills directory.\n"
            "Pass one explicitly: --skills-dir /path/to/skills\n"
            "Auto-detect looked at: "
            + ", ".join(p for p in CANDIDATE_DIRS if p),
            file=sys.stderr,
        )
        sys.exit(2)
    skills = load_skills(d)
    if not skills:
        print(f"No skills (folders with SKILL.md) found in {d}", file=sys.stderr)
        sys.exit(2)
    return d, skills


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit installed OpenClaw skills.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_dir(p):
        p.add_argument("--skills-dir", help="Directory of installed skills (auto-detected if omitted).")

    pa = sub.add_parser("audit", help="Full health report (conflicts + security + versions).")
    add_dir(pa)
    pa.add_argument("--json", action="store_true")

    pc = sub.add_parser("conflicts", help="Show overlapping triggers.")
    add_dir(pc)
    pc.add_argument("--threshold", type=float, default=0.20)
    pc.add_argument("--json", action="store_true")

    ps = sub.add_parser("security", help="Inline security red-flag scan.")
    add_dir(ps)
    ps.add_argument("--json", action="store_true")

    pv = sub.add_parser("stale", help="Compare installed vs latest ClawHub versions.")
    add_dir(pv)
    pv.add_argument("--json", action="store_true")

    pw = sub.add_parser("which", help="Rank which skill would fire for a prompt.")
    pw.add_argument("prompt", help="The user prompt to test.")
    add_dir(pw)
    pw.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)
    skills_dir, skills = _resolve(args)

    if args.cmd == "audit":
        if args.json:
            payload = {
                "skills_dir": str(skills_dir),
                "skills": [{"name": s.name, "version": s.version} for s in skills],
                "conflicts": find_conflicts(skills),
                "stale": check_stale(skills),
                "security": {s.name: scan_security(s) for s in skills},
            }
            print(json.dumps(payload, indent=2))
        else:
            print(render_audit_md(skills_dir, skills))

    elif args.cmd == "conflicts":
        res = find_conflicts(skills, args.threshold)
        print(json.dumps(res, indent=2) if args.json else _fmt_conflicts(res))

    elif args.cmd == "security":
        res = {s.name: scan_security(s) for s in skills}
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            any_hit = False
            for name, findings in res.items():
                if findings:
                    any_hit = True
                    print(f"\n{name}:")
                    for f in findings:
                        print(f"  [{f['severity'].upper()}] {f['file']}:{f['line']} - {f['why']}")
            if not any_hit:
                print("No red flags found.")

    elif args.cmd == "stale":
        res = check_stale(skills)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            for e in res:
                print(f"{e['skill']}: installed {e['installed']} | latest {e['latest']} | {e['status']}")

    elif args.cmd == "which":
        res = which_skill(skills, args.prompt)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(_fmt_which(args.prompt, res))


def _fmt_conflicts(res) -> str:
    if not res:
        return "No overlapping triggers found."
    out = []
    for c in res:
        tag = "shared trigger" if c["shared_triggers"] else f"{int(c['keyword_overlap']*100)}% overlap"
        out.append(f"{c['skill_a']} <-> {c['skill_b']} ({tag})")
        if c["shared_triggers"]:
            out.append("   triggers: " + ", ".join(c["shared_triggers"]))
    return "\n".join(out)


def _fmt_which(prompt, res) -> str:
    if not res:
        return f'No skill clearly matches: "{prompt}"\n(The agent would handle this with base tools.)'
    out = [f'Prompt: "{prompt}"', "Most likely to fire:"]
    top = res[0]
    out.append(f"  -> {top['skill']} (score {top['score']})")
    if len(res) > 1 and res[1]["score"] >= top["score"] * 0.7:
        out.append("  WARNING: ambiguous - a close runner-up could fire instead:")
    for r in res[1:4]:
        out.append(f"     {r['skill']} (score {r['score']})")
    if top["matched_phrases"]:
        out.append("  matched triggers: " + ", ".join(top["matched_phrases"]))
    elif top["matched_keywords"]:
        out.append("  matched keywords: " + ", ".join(top["matched_keywords"]))
    return "\n".join(out)


if __name__ == "__main__":
    main()
