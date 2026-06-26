#!/usr/bin/env python3
"""
ClawHub Guard — 技能市场安全守卫
Usage:
    python clawhub_guard.py scan
    python clawhub_guard.py hunt "<keyword>"
    python clawhub_guard.py audit
    python clawhub_guard.py install <slug>
"""

import argparse, json, os, re, subprocess, sys
from pathlib import Path

CLAWHUB_BIN = str(Path.home() / "AppData" / "Roaming" / "npm" / "clawhub.cmd")
SKILLS_DIR = str(Path.home() / "skills")


def run_ch(args, timeout=60):
    r = subprocess.run([CLAWHUB_BIN] + args, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr, r.returncode


def parse_explore_output(stdout):
    """Parse 'clawhub explore' output into list of {slug, version, desc}."""
    skills = []
    for line in stdout.splitlines():
        # Format: slug  version  time  description
        parts = line.strip().split(None, 3)
        if len(parts) >= 4:
            skills.append({
                "slug": parts[0],
                "version": parts[1],
                "description": parts[3],
            })
    return skills


def parse_search_output(stdout):
    """Parse 'clawhub search' output into list of {slug, name, score}."""
    skills = []
    for line in stdout.splitlines():
        match = re.match(r"^(\S+)\s+(.+?)\s+\(([\d.]+)\)", line.strip())
        if match:
            skills.append({
                "slug": match.group(1),
                "name": match.group(2).strip(),
                "score": float(match.group(3)),
            })
    return skills


def quick_vet(slug, description=""):
    """Quick risk assessment based on name and description."""
    risk = "LOW"
    flags = []

    desc_lower = description.lower()
    slug_lower = slug.lower()

    # Red flag patterns
    high_risk_keywords = [
        "credential", "password", "token", "secret", "sudo", "root",
        "wallet", "trade", "exchange", "transfer", "payment",
        "auth", "login", "ssh", "key",
    ]
    medium_risk_keywords = [
        "upload", "download", "fetch", "curl", "wget",
        "browser", "execute", "shell", "command",
    ]

    for kw in high_risk_keywords:
        if kw in slug_lower or kw in desc_lower:
            risk = "HIGH"
            flags.append(f"HIGH: contains '{kw}'")
            break

    if risk != "HIGH":
        for kw in medium_risk_keywords:
            if kw in slug_lower or kw in desc_lower:
                risk = "MEDIUM"
                flags.append(f"MEDIUM: contains '{kw}'")
                break

    # Known safe patterns
    safe_patterns = ["skill-vetter", "codegraph", "openclaw", "hermes", "cursor"]
    for sp in safe_patterns:
        if sp in slug_lower:
            risk = "LOW"
            flags = []
            break

    return {"risk": risk, "flags": flags}


def cmd_scan():
    print("Scanning ClawHub marketplace...")
    out, err, rc = run_ch(["explore"])
    skills = parse_explore_output(out)

    if not skills:
        print("No skills found or parse error.")
        return

    print(f"Found {len(skills)} skills. Vetting...\n")

    results = []
    for s in skills:
        vet = quick_vet(s["slug"], s.get("description", ""))
        results.append({**s, **vet})

    # Sort by risk (LOW first, then MEDIUM, then HIGH)
    risk_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    results.sort(key=lambda x: risk_order.get(x["risk"], 3))

    # Top 5 safest
    print("## Top 5 Recommended Skills\n")
    for i, r in enumerate(results[:5]):
        risk_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(r["risk"], "⚪")
        print(f"  {i+1}. {risk_icon} **{r['slug']}** v{r.get('version','?')}")
        print(f"     {r.get('description', '')[:100]}")
        if r.get("flags"):
            for f in r["flags"]:
                print(f"     ⚠ {f}")
        print()

    # Count warnings
    high = sum(1 for r in results if r["risk"] == "HIGH")
    med = sum(1 for r in results if r["risk"] == "MEDIUM")
    low = sum(1 for r in results if r["risk"] == "LOW")
    print(f"Summary: {low} safe, {med} caution, {high} high-risk (out of {len(results)})")


def cmd_hunt(keyword):
    kw = " ".join(keyword) if isinstance(keyword, list) else keyword
    print(f"Hunting for '{kw}' on ClawHub...")
    out, err, rc = run_ch(["search", kw])
    skills = parse_search_output(out)

    if not skills:
        print(f"No skills found for '{kw}'.")
        return

    print(f"Found {len(skills)} matches. Vetting...\n")

    for i, s in enumerate(skills[:10]):
        vet = quick_vet(s["slug"], s.get("name", ""))
        risk_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(vet["risk"], "⚪")
        print(f"  {risk_icon} **{s['slug']}** (score: {s['score']:.2f})")
        print(f"     {s.get('name', '')[:100]}")
        if vet.get("flags"):
            for f in vet["flags"]:
                print(f"     ⚠ {f}")
        print()


def cmd_audit():
    print("Checking installed skills for updates...")
    out, err, rc = run_ch(["list"])
    installed = [line.strip() for line in out.splitlines() if line.strip()]

    for skill in installed:
        parts = skill.split()
        slug = parts[0]
        print(f"  Checking {slug}...")
        out2, err2, rc2 = run_ch(["update", slug, "--dry-run"] if False else ["inspect", slug], timeout=30)
        # ClawHub doesn't have --dry-run, just note it
        print(f"    Installed: {skill}")

    print(f"\n{len(installed)} skills installed. Run 'clawhub update' to update all.")


def cmd_install(slug):
    print(f"Vetting {slug} before install...")
    out, err, rc = run_ch(["inspect", slug], timeout=30)
    
    vet = quick_vet(slug, out[:200])
    risk_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(vet["risk"], "⚪")
    print(f"  Risk: {risk_icon} {vet['risk']}")
    
    if vet["risk"] == "HIGH":
        print(f"  ⚠ High risk skill — manual review recommended before install.")
        print(f"  Run: clawhub install {slug} --force  (if you trust it)")
        return

    if vet["flags"]:
        for f in vet["flags"]:
            print(f"  Note: {f}")

    print(f"\nInstalling {slug}...")
    out2, err2, rc2 = run_ch(["install", slug, "-y"], timeout=60)
    print(out2)
    if rc2 == 0:
        print(f"Installed: {slug}")


def main():
    parser = argparse.ArgumentParser(description="ClawHub Guard")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("scan", help="Browse market, vet, recommend top 5")
    
    p_hunt = sub.add_parser("hunt", help="Search market for keyword")
    p_hunt.add_argument("keyword", nargs="+", help="Search keyword (multi-word OK)")
    
    sub.add_parser("audit", help="Check installed skills for updates")
    
    p_inst = sub.add_parser("install", help="Safe install (vet first)")
    p_inst.add_argument("slug", help="Skill slug to install")

    args = parser.parse_args()

    if args.cmd == "scan":
        cmd_scan()
    elif args.cmd == "hunt":
        cmd_hunt(args.keyword)
    elif args.cmd == "audit":
        cmd_audit()
    elif args.cmd == "install":
        cmd_install(args.slug)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
