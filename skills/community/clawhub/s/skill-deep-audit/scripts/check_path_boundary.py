#!/usr/bin/env python3
"""D3-E5 (1) checker: does a Path(__file__) .parent chain escape the skill root?

The criterion is the ENDPOINT, not the hop count:
  - Endpoint inside the audited skill root (root itself included) -> not judged
    (2 hops from a shallow script and 3 from a nested one are equivalent)
  - Endpoint outside the skill                                    -> ERR
    (breaks whenever the skill is relocated, renamed, or run from a temp copy)

Usage:
    python3 check_path_boundary.py <skill-path> [--json]
Exit codes: 0 = no ERR; 1 = ERR found; 2 = usage / bad path
"""
import json
import re
import sys
from pathlib import Path

CHAIN = re.compile(
    r"Path\(\s*__file__\s*\)((?:\s*\.\s*(?:resolve|absolute)\(\)|\s*\.\s*parent)+)"
)
# Literal directory segments appended to the chain: / "other-skill" / "scripts"
TAIL_SEG = re.compile(r"""\s*/\s*(?:f?["']([^"'/]+)["'])""")
# Variable bindings: BASE = Path(__file__)...  /  OTHER = BASE.parent.parent
ASSIGN = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(.+?)\s*(?:#.*)?$")
VAR_CHAIN = re.compile(r"^([A-Za-z_]\w*)((?:\s*\.\s*parent)+)")
SKIP_DIRS = {"__pycache__", "node_modules", ".git", ".venv", "venv"}
EXTS = {".py"}


def find_skill_root(start: Path, fallback: Path) -> Path:
    """Walk up to the directory containing SKILL.md; fall back to the audited dir."""
    for d in [start, *start.parents]:
        if (d / "SKILL.md").exists():
            return d
    return fallback


def chain_endpoint(file_path: Path, n_parent: int) -> Path:
    """.parent#1 is the file's own directory, so the endpoint is that directory
    walked up (n-1) more times."""
    end = file_path.parent
    for _ in range(max(0, n_parent - 1)):
        end = end.parent
    return end


def scan(skill_path: Path):
    """Scan every .py under the skill; return findings whose endpoint escapes."""
    skill_path = skill_path.resolve()
    findings = []
    for f in sorted(skill_path.rglob("*")):
        if f.suffix not in EXTS or not f.is_file():
            continue
        if SKIP_DIRS & set(f.parts):
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError as e:
            print(f"WARN: could not read, skipping: {f} - {e}", file=sys.stderr)
            continue
        root = find_skill_root(f.parent, skill_path)
        # variable name -> resolved absolute path, used to reconstruct
        # chains that were split across multiple lines
        bound: dict[str, Path] = {}
        for lineno, line in enumerate(lines, 1):
            if line.lstrip().startswith("#"):
                continue  # comment lines are exempt (matches the rule)

            # -- handle "VAR = <known var>.parent..." (cross-line chains) --
            am = ASSIGN.match(line)
            if am and not CHAIN.search(line):
                vm = VAR_CHAIN.match(am.group(2))
                if vm is None and am.group(1) in bound:
                    # Rebound to something unrelated to __file__ -> drop the
                    # stale binding, else later lines compute endpoints from a
                    # path that is no longer current (wrong endpoint / verdict).
                    del bound[am.group(1)]
                if vm and vm.group(1) in bound:
                    end = bound[vm.group(1)]
                    for _ in range(vm.group(2).count(".parent")):
                        end = end.parent
                    for seg in TAIL_SEG.finditer(am.group(2)[vm.end():]):
                        end = end / seg.group(1)
                    bound[am.group(1)] = end
                    if not (end == root or root in end.parents):
                        findings.append({
                            "file": str(f.relative_to(skill_path)),
                            "line": lineno,
                            "parents": f"{vm.group(2).count('.parent')} (via {vm.group(1)})",
                            "endpoint": str(end),
                            "skill_root": str(root),
                            "code": line.strip()[:120],
                        })

            for m in CHAIN.finditer(line):
                n = m.group(1).count(".parent")
                if n < 2:
                    continue  # single hop = own directory, always safe
                end = chain_endpoint(f.resolve(), n)
                # Literal tail segments must be counted too, otherwise a form
                # like `...parent.parent / "other-skill"` (step up to the skills
                # root, then across into a sibling) is missed: the chain endpoint
                # looks safe while the full path is already outside.
                for seg in TAIL_SEG.finditer(line[m.end():]):
                    end = end / seg.group(1)
                end = Path(*[p for p in end.parts])  # normalise
                if am and am.group(1):
                    bound[am.group(1)] = end  # record binding for later lines
                inside = end == root or root in end.parents
                if inside:
                    continue
                findings.append(
                    {
                        "file": str(f.relative_to(skill_path)),
                        "line": lineno,
                        "parents": n,
                        "endpoint": str(end),
                        "skill_root": str(root),
                        "code": line.strip()[:120],
                    }
                )
    return findings


def main() -> int:
    """CLI entry point: parse args, scan, print results. Returns 0/1/2."""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    target = Path(args[0]).expanduser()
    if not target.is_dir():
        print(f"ERROR: not a directory: {target}", file=sys.stderr)
        return 2

    findings = scan(target)
    if as_json:
        print(json.dumps({"err_count": len(findings), "findings": findings},
                         ensure_ascii=False, indent=2))
    elif not findings:
        print("OK  D3-E5 (1): no parent-chain derivation escapes the skill boundary")
    else:
        print(f"ERR D3-E5 (1): {len(findings)} parent chain(s) escape the skill boundary\n")
        for x in findings:
            print(f"  {x['file']}:{x['line']}  ({x['parents']} hops -> escapes)")
            print(f"    {x['code']}")
            print(f"    endpoint: {x['endpoint']}")
            print(f"    boundary: {x['skill_root']}\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
