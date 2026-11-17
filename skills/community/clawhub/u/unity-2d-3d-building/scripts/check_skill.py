#!/usr/bin/env python3
"""Self-check for the unity-2d-3d-building skill pack.

One named rule per failure that has actually reached this package. Every rule answers with a named
boolean, because "ok": false tells nobody anything at 2am, while
{"failed": ["pinned_installs: docs/install.md has a floating version"]} does.

Stdlib only. No network. No subprocess. Reads the pack's own text and reports.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: hosts whose licence position this pack is allowed to state in the asset guide
KNOWN_ASSET_HOSTS = {
    "kenney.nl", "quaternius.com", "polyhaven.com", "api.polyhaven.com", "kaylousberg.itch.io",
    "poly.pizza", "sonniss.com", "freesound.org", "assetstore.unity.com", "mixamo.com",
    "opengameart.org", "github.com", "chatagent.ca", "deepseekoracle.github.io", "clawhub.ai",
}

#: hosts named as forbidden (redistributors of paid packs) - documented, never recommended
FORBIDDEN_HOSTS = {"unityassetpack.com", "unityassetcollection.com", "opengameasset.net"}

TEXT_SUFFIXES = (".md", ".json", ".py", ".txt")


def _files() -> list[Path]:
    return [p for p in sorted(ROOT.rglob("*")) if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _frontmatter(text: str) -> dict:
    """Frontmatter keys, with YAML folded blocks (`key: >`) joined into one value.

    A naive parser returns ">" for a description written as a folded block, which then fails the
    trigger rule on a file that is perfectly correct - the parser is the thing to fix, not the rule.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict = {}
    key: str | None = None
    for line in text[3:end].splitlines():
        if line.startswith((" ", "\t")):
            if key:
                out[key] = (out[key] + " " + line.strip()).strip()
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            key = k
            out[k] = "" if v in (">", "|", ">-", "|-") else v
        else:
            key = None
    return out


def rule_version_agrees() -> tuple[bool, str]:
    """SKILL.md frontmatter version must equal claw.json version."""
    skill = _frontmatter(_read(ROOT / "SKILL.md")).get("version", "")
    try:
        claw = json.loads(_read(ROOT / "claw.json")).get("version", "")
    except json.JSONDecodeError:
        return False, "claw.json is not valid JSON"
    if not skill or not claw:
        return False, f"missing version (SKILL.md={skill!r} claw.json={claw!r})"
    return (skill == claw), f"SKILL.md={skill} claw.json={claw}"


def rule_no_local_paths() -> tuple[bool, str]:
    """A drive letter or a user folder in shipped text is someone else's machine."""
    bad: list[str] = []
    # assembled from parts on purpose: a detector whose own source contains the shape it bans reports
    # itself, and the tempting "fix" is to exclude the file - which blinds the rule where it matters.
    drive = r"(?<![A-Za-z0-9])[A-Za-z]:" + re.escape(chr(92)) + "|(?<![A-Za-z0-9])[A-Za-z]:/"
    users = re.escape("/" + "Users" + "/") + "|" + re.escape("/" + "home" + "/") + "[a-z]"
    pat = re.compile(drive + "|" + users)
    for p in _files():
        for i, line in enumerate(_read(p).splitlines(), 1):
            if pat.search(line):
                bad.append(f"{p.relative_to(ROOT)}:{i}")
    return (not bad), ("; ".join(bad[:5]) if bad else "no absolute local paths")


def rule_pinned_installs() -> tuple[bool, str]:
    """Every clawhub install line pins both the CLI and the package version."""
    bad: list[str] = []
    floating = "@" + "latest"          # assembled: prose may name it, a command may not use it
    for p in _files():
        for i, line in enumerate(_read(p).splitlines(), 1):
            if "install" not in line and " npx " not in line:
                continue
            if floating in line:
                bad.append(f"{p.relative_to(ROOT)}:{i} floating version in an install command")
                continue
            m = re.search(r"npx\s+(?:--yes\s+)?clawhub(@[\w.\-]+)?\s+install\s+(\S+)", line)
            if m:
                pkg = m.group(2)
                if not m.group(1) or "@" not in pkg:
                    bad.append(f"{p.relative_to(ROOT)}:{i} unpinned install ({pkg})")
    return (not bad), ("; ".join(bad[:5]) if bad else "CLI and package both pinned")


def rule_references_present() -> tuple[bool, str]:
    """Every references/<file> named in SKILL.md exists in the pack."""
    text = _read(ROOT / "SKILL.md")
    missing = [ref for ref in sorted(set(re.findall(r"references/[A-Za-z0-9._\-]+\.md", text)))
               if not (ROOT / ref).is_file()]
    return (not missing), ("missing: " + ", ".join(missing) if missing else "all referenced files present")


def rule_techniques_log_intact() -> tuple[bool, str]:
    """The living log keeps both its sections, and says how to append."""
    text = _read(ROOT / "references/techniques.md")
    if not text:
        return False, "references/techniques.md is missing or empty"
    has_conf = "## Confirmed" in text
    has_rej = "## Rejected" in text
    if not (has_conf and has_rej):
        return False, f"Confirmed={has_conf} Rejected={has_rej}"
    return True, "Confirmed and Rejected sections both present"


def rule_asset_hosts_known() -> tuple[bool, str]:
    """Licence statements only about hosts this pack names, and the blacklist stays documented."""
    text = _read(ROOT / "references/assets-and-licences.md")
    if not text:
        return False, "references/assets-and-licences.md is missing"
    hosts = set(re.findall(r"https?://([A-Za-z0-9.\-]+)", text))
    unknown = sorted(h for h in hosts if h not in KNOWN_ASSET_HOSTS)
    if unknown:
        return False, "unlisted hosts: " + ", ".join(unknown[:5])
    missing_forbidden = sorted(h for h in FORBIDDEN_HOSTS if h not in text)
    if missing_forbidden:
        return False, "blacklist lost: " + ", ".join(missing_forbidden)
    return True, "all named hosts are known and the blacklist is intact"


def rule_no_html_comments() -> tuple[bool, str]:
    """A comment in shipped text reads to a scanner as hidden instructions."""
    marker = "<" + "!" + "--"          # assembled: the rule must not contain what it bans
    bad = [str(p.relative_to(ROOT)) for p in _files() if marker in _read(p)]
    return (not bad), ("; ".join(bad[:5]) if bad else "no HTML comments")


def rule_trigger_is_tight() -> tuple[bool, str]:
    """The description opens with a self-contained trigger."""
    desc = _frontmatter(_read(ROOT / "SKILL.md")).get("description", "")
    head = " ".join(desc.split())[:60]
    return head.lower().startswith("use when"), f"opens with: {head!r}"


def rule_manifest_declares_permissions() -> tuple[bool, str]:
    """The manifest states network, filesystem and publish posture."""
    try:
        claw = json.loads(_read(ROOT / "claw.json"))
    except json.JSONDecodeError:
        return False, "claw.json is not valid JSON"
    perms = claw.get("permissions") or {}
    need = ("network", "filesystem", "publish")
    missing = [k for k in need if k not in perms]
    if missing:
        return False, "missing: " + ", ".join(missing)
    if perms["filesystem"].get("shell") is not False or perms["filesystem"].get("subprocess") is not False:
        return False, "shell/subprocess must be declared false"
    return True, "network, filesystem and publish declared"


RULES = (
    ("version_agrees", rule_version_agrees),
    ("no_local_paths", rule_no_local_paths),
    ("pinned_installs", rule_pinned_installs),
    ("references_present", rule_references_present),
    ("techniques_log_intact", rule_techniques_log_intact),
    ("asset_hosts_known", rule_asset_hosts_known),
    ("no_html_comments", rule_no_html_comments),
    ("trigger_is_tight", rule_trigger_is_tight),
    ("manifest_declares_permissions", rule_manifest_declares_permissions),
)


def main() -> int:
    checks: dict[str, bool] = {}
    detail: dict[str, str] = {}
    failed: list[str] = []
    for name, fn in RULES:
        try:
            ok, why = fn()
        except Exception as exc:  # a rule that cannot run is a failure, never a pass
            ok, why = False, f"{type(exc).__name__}: {exc}"
        checks[name] = bool(ok)
        detail[name] = why
        if not ok:
            failed.append(f"audit {name}: {why}")
    report = {"ok": not failed, "checks": checks, "detail": detail, "failed": failed,
              "root": str(ROOT), "rules": len(RULES)}
    if "--json" in sys.argv:
        print(json.dumps(report, indent=1))
    else:
        print(f"unity-2d-3d-building self-check: {'PASS' if report['ok'] else 'FAIL'}"
              f" ({sum(checks.values())}/{len(RULES)} rules)")
        for name in checks:
            print(f"  {'ok  ' if checks[name] else 'FAIL'} {name}: {detail[name]}")
        for f in failed:
            print(f"  -> {f}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
