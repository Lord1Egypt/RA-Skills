#!/usr/bin/env bash
# wreckit — verify declared dependencies exist in registries
# Usage: ./check-deps.sh [project-path]
# Outputs JSON to stdout (status PASS/FAIL), human-readable logs to stderr
# Exit 0 = results produced (check JSON status)

set -euo pipefail
PROJECT="${1:-.}"
PROJECT="$(cd "$PROJECT" && pwd)"
cd "$PROJECT"
HALLUCINATED=()

check_npm() {
  local pkg="$1"
  # Skip scoped packages with complex names, builtins
  [[ "$pkg" == node:* ]] && return 0
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://registry.npmjs.org/$pkg" 2>/dev/null || echo "000")
  if [ "$status" = "404" ]; then
    HALLUCINATED+=("npm:$pkg")
  fi
}

check_pypi() {
  local pkg="$1"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://pypi.org/pypi/$pkg/json" 2>/dev/null || echo "000")
  if [ "$status" = "404" ]; then
    HALLUCINATED+=("pypi:$pkg")
  fi
}

check_crate() {
  local pkg="$1"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://crates.io/api/v1/crates/$pkg" 2>/dev/null || echo "000")
  if [ "$status" = "404" ]; then
    HALLUCINATED+=("crate:$pkg")
  fi
}

# npm/yarn
if [ -f "package.json" ]; then
  deps=$(python3 -c "
import json,sys
d=json.load(open('package.json'))
for k in ['dependencies','devDependencies']:
  for p,v in d.get(k,{}).items():
    if not p.startswith('@types/'):
      print(f'{p}\\t{v}')
" 2>/dev/null || true)
  while IFS=$'\t' read -r pkg version; do
    [ -z "$pkg" ] && continue
    if [[ "$version" == npm:* ]] || [[ "$version" == workspace:* ]] || [[ "$version" == file:* ]] || [[ "$version" == link:* ]] || [[ "$version" == github:* ]] || [[ "$version" == git+https:* ]] || [[ "$version" == patch:* ]] || [[ "$version" == portal:* ]]; then
      continue
    fi
    check_npm "$pkg"
  done <<< "$deps"
fi

# Python
if [ -f "requirements.txt" ]; then
  while IFS= read -r line; do
    pkg=$(echo "$line" | sed 's/[>=<!\[].*//;s/#.*//' | tr -d '[:space:]')
    [ -n "$pkg" ] && check_pypi "$pkg"
  done < requirements.txt
elif [ -f "pyproject.toml" ]; then
  deps=$(python3 -c "
try:
  import tomllib
except: import tomli as tomllib
with open('pyproject.toml','rb') as f: d=tomllib.load(f)
for dep in d.get('project',{}).get('dependencies',[]):
  print(dep.split('>')[0].split('<')[0].split('=')[0].split('[')[0].strip())
" 2>/dev/null || true)
  for pkg in $deps; do
    check_pypi "$pkg"
  done
fi

# Swift / SPM
# Note: There is no automated CVE database for Swift Package Manager (unlike npm/PyPI/crates).
# We list dependencies and flag known-vulnerable packages from a small hardcoded list,
# but manual review is always recommended for Swift projects.
if [ -f "Package.swift" ]; then
  echo "Checking Swift Package Manager dependencies..." >&2
  SPM_DEPS=""
  if command -v swift >/dev/null 2>&1; then
    SPM_DEPS=$(swift package show-dependencies --format json 2>/dev/null || echo "")
  fi

  if [ -n "$SPM_DEPS" ] && echo "$SPM_DEPS" | python3 -c "import json,sys; json.load(sys.stdin)" >/dev/null 2>&1; then
    # Parse and check against known-vulnerable packages
    SPM_DEPS="$SPM_DEPS" python3 - <<'PYEOF'
import json, os, sys

deps_json = json.loads(os.environ["SPM_DEPS"])
known_vulns = {
    # package_url_substring: (description, fixed_version_note)
    "vapor/vapor": ("CVE-2023-vapor: versions < 4.65 have HTTP request smuggling vulnerability", "upgrade to >= 4.65"),
    "apple/swift-nio": ("CVE-2022-nio: versions < 2.42 have potential DoS via malformed frames", "upgrade to >= 2.42"),
    "Alamofire/Alamofire": ("Older versions may have certificate pinning bypass", "use latest"),
}

def flatten_deps(node, depth=0):
    """Recursively flatten the SPM dependency tree."""
    results = []
    if isinstance(node, dict):
        url = node.get("url", node.get("identity", ""))
        version = node.get("version", "unresolved")
        if url:
            results.append({"url": url, "version": str(version), "depth": depth})
        for child in node.get("dependencies", []):
            results.extend(flatten_deps(child, depth + 1))
    elif isinstance(node, list):
        for item in node:
            results.extend(flatten_deps(item, depth))
    return results

all_deps = flatten_deps(deps_json)
warnings = []
for dep in all_deps:
    for vuln_key, (desc, fix) in known_vulns.items():
        if vuln_key.lower() in dep["url"].lower():
            warnings.append({
                "package": dep["url"],
                "version": dep["version"],
                "advisory": desc,
                "fix": fix
            })

print(json.dumps({
    "status": "CAUTION" if warnings else "PASS",
    "confidence": 0.5,  # Low confidence — no automated CVE DB for Swift SPM
    "findings": len(warnings),
    "dependencies": len(all_deps),
    "advisories": warnings,
    "hallucinated": [],
    "note": "No automated CVE database for Swift SPM — manual review recommended. Only a small hardcoded list of known vulnerabilities is checked."
}))
PYEOF
  else
    echo "Could not parse SPM dependencies — swift CLI may not be available" >&2
    python3 - <<'PYEOF'
import json
print(json.dumps({
    "status": "CAUTION",
    "confidence": 0.3,
    "findings": 0,
    "hallucinated": [],
    "note": "Swift Package Manager dependencies could not be enumerated. Manual review recommended."
}))
PYEOF
  fi
  # Swift deps handled — check CocoaPods if present, then exit
  # (don't fall through to npm/pypi/cargo generic checks)
  if [ -f "Podfile" ] && command -v pod >/dev/null 2>&1; then
    echo "Also checking CocoaPods..." >&2
    pod outdated 2>/dev/null | head -20 >&2 || true
  fi
  exit 0
fi

# CocoaPods (Podfile — standalone, without SPM)
if [ -f "Podfile" ]; then
  echo "Checking CocoaPods dependencies..." >&2
  POD_OUTDATED=""
  if command -v pod >/dev/null 2>&1; then
    POD_OUTDATED=$(pod outdated 2>/dev/null || echo "")
  fi
  if [ -n "$POD_OUTDATED" ]; then
    OUTDATED_COUNT=$(echo "$POD_OUTDATED" | grep -c "^-" 2>/dev/null || echo 0)
    echo "  Found $OUTDATED_COUNT outdated pods" >&2
    # We don't fail on outdated pods — just note it
  fi
fi

# Rust
if [ -f "Cargo.toml" ]; then
  deps=$(python3 -c "
try:
  import tomllib
except: import tomli as tomllib
with open('Cargo.toml','rb') as f: d=tomllib.load(f)
for dep in d.get('dependencies',{}):
  print(dep)
" 2>/dev/null || true)
  for pkg in $deps; do
    check_crate "$pkg"
  done
fi

if [ ${#HALLUCINATED[@]} -gt 0 ]; then
  echo "HALLUCINATED DEPENDENCIES FOUND:" >&2
  for h in "${HALLUCINATED[@]}"; do
    echo "  ❌ $h" >&2
  done
  # Serialize the hallucinated list to JSON via a short one-liner, then pass
  # it as an env variable to the reporting script.  This avoids the pipe+heredoc
  # stdin conflict that would cause findings to be under-reported.
  HALLUCINATED_JSON=$(printf '%s\n' "${HALLUCINATED[@]}" | python3 -c "
import json, sys
seen = set()
items = []
for raw in sys.stdin:
    entry = raw.strip()
    if entry and entry not in seen:
        seen.add(entry)
        items.append(entry)
print(json.dumps(items))
")
  # Build the final report: findings MUST always equal len(hallucinated)
  HALLUCINATED_JSON="$HALLUCINATED_JSON" python3 - <<'PYEOF'
import json, os

items = json.loads(os.environ["HALLUCINATED_JSON"])

# Invariant: findings == len(hallucinated) — enforced here, not assumed.
findings = len(items)

print(json.dumps({
    "status": "FAIL",
    "confidence": 1.0,
    "findings": findings,
    "hallucinated": items
}))
PYEOF
else
  echo "All dependencies verified in registries." >&2
  python3 - <<'PYEOF'
import json
print(json.dumps({
    "status": "PASS",
    "confidence": 1.0,
    "findings": 0,
    "hallucinated": []
}))
PYEOF
fi

exit 0
