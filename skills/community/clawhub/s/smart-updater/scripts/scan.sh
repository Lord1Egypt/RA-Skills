#!/usr/bin/env bash
# scan.sh — 扫描可用更新
# 依赖：~/.openclaw/inventory.json（先运行 inventory.sh）
# 输出：~/.openclaw/scan-result.json
# 用法：bash scan.sh [--quiet]
set -u
export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

INVENTORY_FILE="${HOME}/.openclaw/inventory.json"
SCAN_FILE="${HOME}/.openclaw/scan-result.json"
QUIET=false

[[ "${1:-}" == "--quiet" ]] && QUIET=true

log() { $QUIET || echo "$*" >&2; }

if [ ! -f "$INVENTORY_FILE" ]; then
  echo "❌ inventory.json not found. Run inventory.sh first." >&2
  exit 1
fi

# Read inventory into temp file for python processing
SCAN_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 << 'PYEOF'
import json, subprocess, os, sys, time, re

inventory_file = os.path.expanduser("~/.openclaw/inventory.json")
scan_file = os.path.expanduser("~/.openclaw/scan-result.json")
quiet = "--quiet" in sys.argv

def log(msg):
    if not quiet:
        print(msg, file=sys.stderr)

def run(cmd, timeout=15):
    """Run a command and return stdout, or empty string on failure."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def semver_compare(current, latest):
    """Compare semver strings, return change type."""
    def parse(v):
        # Extract digits from version string
        parts = re.findall(r'\d+', v)
        return [int(x) for x in parts[:3]] if parts else [0, 0, 0]
    
    c = parse(current)
    l = parse(latest)
    
    if l <= c:
        return "none"
    if l[0] > c[0]:
        return "major"
    if l[1] > c[1]:
        return "minor"
    return "patch"

inv = json.load(open(inventory_file))
assets = inv["assets"]

updates = []
up_to_date = []
unreachable = []
skipped = []

for asset in assets:
    name = asset["name"]
    source = asset.get("source", "")
    asset_type = asset.get("type", "")
    
    # Skip types that can't be independently checked
    if asset_type == "builtin":
        skipped.append({"name": name, "reason": "version tied to core"})
        continue
    
    if source == "local":
        skipped.append({"name": name, "reason": "no update source registered"})
        continue
    
    # --- npm (core + extensions) ---
    if source == "npm":
        pkg = asset.get("npmPackage", name)
        log(f"🔍 Checking {name} (npm: {pkg})...")
        latest = run(f"npm view {pkg} version")
        time.sleep(0.2)  # rate limit
        
        if not latest:
            unreachable.append({"name": name, "source": source, "reason": "npm view failed"})
            continue
        
        current = asset.get("currentVersion", "0.0.0")
        # For core, strip commit hash: "2026.3.8 (3caab92)" -> "2026.3.8"
        current_clean = current.split(" ")[0] if " " in current else current
        
        change = semver_compare(current_clean, latest)
        if change == "none":
            up_to_date.append({"name": name, "version": current_clean})
            log(f"  ✅ {current_clean} = {latest}")
        else:
            changelog_url = f"https://www.npmjs.com/package/{pkg}?activeTab=changelog"
            if "openclaw" in pkg:
                changelog_url = "https://github.com/openclaw/openclaw/releases"
            updates.append({
                "name": name,
                "type": asset_type,
                "source": source,
                "current": current_clean,
                "latest": latest,
                "changeType": change,
                "changelogUrl": changelog_url,
                "npmPackage": pkg
            })
            log(f"  🆕 {current_clean} → {latest} ({change})")
    
    # --- clawhub ---
    elif source == "clawhub":
        # We batch-check clawhub below
        pass
    
    # --- github ---
    elif source == "github":
        repo_url = asset.get("repo", "")
        current_commit = asset.get("currentCommit", "")
        skill_dir = asset.get("installedAt", "")
        
        if not repo_url or not skill_dir:
            unreachable.append({"name": name, "source": source, "reason": "missing repo or path"})
            continue
        
        log(f"🔍 Checking {name} (git: {repo_url})...")
        remote_head = run(f"cd '{skill_dir}' && git ls-remote origin HEAD 2>/dev/null | head -1 | cut -f1")
        time.sleep(0.3)
        
        if not remote_head:
            unreachable.append({"name": name, "source": source, "reason": "git ls-remote failed"})
            continue
        
        if remote_head == current_commit:
            up_to_date.append({"name": name, "version": current_commit[:8]})
            log(f"  ✅ {current_commit[:8]} = latest")
        else:
            # Note: only ls-remote in scan phase, no git fetch (read-only scan)
            updates.append({
                "name": name,
                "type": "skill",
                "source": source,
                "current": current_commit[:8],
                "latest": remote_head[:8],
                "changeType": "unknown",
                "changelogUrl": repo_url.replace(".git", "") + "/commits"
            })
            log(f"  🆕 {current_commit[:8]} → {remote_head[:8]}")

# --- Check clawhub skills: SkillHub index first, clawhub inspect as fallback ---
log("🔍 Checking ClawHub skills (via SkillHub index + clawhub fallback)...")
clawhub_assets = [a for a in assets if a.get("source") == "clawhub"]

# Step 1: Try to fetch SkillHub index in one shot (fast, no rate limit)
SKILLHUB_INDEX_URL = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills.json"
skillhub_index = {}  # {slug: {version, changelog_url, ...}}
try:
    import urllib.request
    req = urllib.request.urlopen(SKILLHUB_INDEX_URL, timeout=5)
    sh_data = json.loads(req.read().decode())
    for skill in sh_data.get("skills", []):
        slug = skill.get("slug", "")
        if slug:
            skillhub_index[slug] = {
                "version": skill.get("version", ""),
                "name": skill.get("name", slug),
                "description": skill.get("description", ""),
            }
    log(f"  ✅ SkillHub index loaded: {len(skillhub_index)} skills")
except Exception as e:
    log(f"  ⚠️ SkillHub index unavailable ({e}), falling back to clawhub inspect for all")

for asset in clawhub_assets:
    aname = asset["name"]
    current_v = asset.get("currentVersion", "?")
    
    # Cross-check: also read version from local SKILL.md if available
    installed_at = asset.get("installedAt", "")
    if installed_at:
        local_skill_ver = run(f"grep '^version:' '{installed_at}/SKILL.md' 2>/dev/null | head -1 | sed 's/version:[[:space:]]*//'")
        if local_skill_ver and local_skill_ver != current_v:
            log(f"  ⚠️ Version mismatch: clawhub list says {current_v}, SKILL.md says {local_skill_ver} — using SKILL.md")
            current_v = local_skill_ver

    # Step 2: Check SkillHub index first (no rate limit, fast)
    remote_v = None
    changelog_lines = []
    changelog_url = f"https://clawhub.ai/search?q={aname}"

    if aname in skillhub_index:
        sh_entry = skillhub_index[aname]
        remote_v = sh_entry.get("version", "")
        log(f"🔍 {aname} (skillhub)...")
    
    # Step 3: Fall back to clawhub inspect if not in SkillHub
    if not remote_v:
        log(f"🔍 {aname} (clawhub inspect)...")
        inspect_output = run(f"clawhub inspect {aname} 2>/dev/null", timeout=15)
        time.sleep(0.3)  # rate limit
        
        if not inspect_output:
            unreachable.append({"name": aname, "source": "clawhub", "reason": "not in SkillHub + clawhub inspect failed"})
            log(f"  ⚠️ {aname} (unreachable)")
            continue
        
        for line in inspect_output.split("\n"):
            line = line.strip()
            if line.startswith("Latest:"):
                remote_v = line.split(":", 1)[1].strip()
                break
            if "latest=" in line:
                m = re.search(r'latest=(\S+)', line)
                if m:
                    remote_v = m.group(1)
    
    if not remote_v:
        unreachable.append({"name": aname, "source": "clawhub", "reason": "could not determine remote version"})
        log(f"  ⚠️ {aname} (no remote version found)")
        continue
    
    if current_v == remote_v:
        up_to_date.append({"name": aname, "version": current_v})
        log(f"  ✅ {aname}@{current_v}")
    else:
        change = semver_compare(current_v, remote_v)
        if change == "none":
            up_to_date.append({"name": aname, "version": current_v})
            log(f"  ✅ {aname}@{current_v}")
        else:
            # Fetch changelog: try SkillHub description first, then clawhub inspect --versions
            if not changelog_lines and aname in skillhub_index:
                desc = skillhub_index[aname].get("description", "")
                if desc:
                    changelog_lines = [f"{remote_v}: {desc[:120]}"]
            
            if not changelog_lines:
                versions_output = run(f"clawhub inspect {aname} --versions --limit 5 2>/dev/null", timeout=15)
                if versions_output:
                    for vline in versions_output.split("\n"):
                        vline = vline.strip()
                        vm = re.match(r'^(\d+\.\d+\.\d+)\s+\S+\s+(.*)', vline)
                        if vm:
                            changelog_lines.append(f"{vm.group(1)}: {vm.group(2)}")
            
            updates.append({
                "name": aname,
                "type": "skill",
                "source": "clawhub",
                "current": current_v,
                "latest": remote_v,
                "changeType": change,
                "changelog": changelog_lines[:5] if changelog_lines else [],
                "changelogUrl": changelog_url,
                "inSkillHub": aname in skillhub_index,
            })
            log(f"  🆕 {aname}: {current_v} → {remote_v} ({change})")

# --- Write result ---
result = {
    "version": 1,
    "scanTime": os.popen("date -u +'%Y-%m-%dT%H:%M:%SZ'").read().strip(),
    "summary": {
        "total": len(assets),
        "updatesAvailable": len(updates),
        "upToDate": len(up_to_date),
        "unreachable": len(unreachable),
        "skipped": len(skipped)
    },
    "updates": updates,
    "upToDate": up_to_date,
    "unreachable": unreachable,
    "skipped": skipped
}

with open(scan_file, "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

log(f"\n✅ Scan complete → {scan_file}")
log(f"   {len(updates)} updates | {len(up_to_date)} current | {len(unreachable)} unreachable | {len(skipped)} skipped")

PYEOF
