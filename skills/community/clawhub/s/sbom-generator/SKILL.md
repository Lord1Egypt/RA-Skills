---
name: sbom-generator
description: Generate Software Bill of Materials (SBOM) in CycloneDX or SPDX format — inventory all dependencies, licenses, vulnerabilities, and supply chain metadata. Required for compliance (FDA, EU CRA, NIST) and security audits.
---

# SBOM Generator

Create a comprehensive Software Bill of Materials listing every dependency, its version, license, and known vulnerabilities. Supports CycloneDX and SPDX formats required by regulatory frameworks (FDA, EU Cyber Resilience Act, NIST SSDF).

Use when: "generate SBOM", "software bill of materials", "list all dependencies", "license audit", "supply chain inventory", "compliance report", "CycloneDX", "SPDX", or during security/compliance audits.

## Commands

### 1. `generate` — Generate Full SBOM

Scan the project and produce a complete dependency inventory.

#### Step 1: Detect Package Managers

```bash
echo "=== Package Manager Detection ==="

MANAGERS=""

# Node.js
[ -f "package-lock.json" ] && MANAGERS="$MANAGERS npm" && echo "✅ npm (package-lock.json)"
[ -f "yarn.lock" ] && MANAGERS="$MANAGERS yarn" && echo "✅ Yarn (yarn.lock)"
[ -f "pnpm-lock.yaml" ] && MANAGERS="$MANAGERS pnpm" && echo "✅ pnpm (pnpm-lock.yaml)"

# Python
[ -f "requirements.txt" ] && MANAGERS="$MANAGERS pip" && echo "✅ pip (requirements.txt)"
[ -f "Pipfile.lock" ] && MANAGERS="$MANAGERS pipenv" && echo "✅ Pipenv (Pipfile.lock)"
[ -f "poetry.lock" ] && MANAGERS="$MANAGERS poetry" && echo "✅ Poetry (poetry.lock)"
[ -f "pdm.lock" ] && MANAGERS="$MANAGERS pdm" && echo "✅ PDM (pdm.lock)"

# Go
[ -f "go.sum" ] && MANAGERS="$MANAGERS go" && echo "✅ Go (go.sum)"

# Rust
[ -f "Cargo.lock" ] && MANAGERS="$MANAGERS cargo" && echo "✅ Cargo (Cargo.lock)"

# Ruby
[ -f "Gemfile.lock" ] && MANAGERS="$MANAGERS bundler" && echo "✅ Bundler (Gemfile.lock)"

# PHP
[ -f "composer.lock" ] && MANAGERS="$MANAGERS composer" && echo "✅ Composer (composer.lock)"

# Java
[ -f "pom.xml" ] && MANAGERS="$MANAGERS maven" && echo "✅ Maven (pom.xml)"
[ -f "build.gradle" ] || [ -f "build.gradle.kts" ] && MANAGERS="$MANAGERS gradle" && echo "✅ Gradle"

# .NET
find . -name "*.csproj" -maxdepth 3 2>/dev/null | head -1 | grep -q . && MANAGERS="$MANAGERS nuget" && echo "✅ NuGet (.csproj)"

echo ""
echo "Package managers found: $(echo $MANAGERS | wc -w)"
```

#### Step 2: Extract Dependencies

```bash
echo ""
echo "=== Dependency Extraction ==="

# npm/Node.js
if [ -f "package-lock.json" ]; then
  echo "--- npm Dependencies ---"
  python3 -c "
import json
lock = json.load(open('package-lock.json'))
packages = lock.get('packages', {})
count = 0
for name, info in sorted(packages.items()):
    if not name or name == '': continue
    clean_name = name.replace('node_modules/', '')
    version = info.get('version', '?')
    license = info.get('license', 'UNKNOWN')
    resolved = info.get('resolved', '')
    dev = info.get('dev', False)
    print(f'{clean_name}|{version}|{license}|{\"dev\" if dev else \"prod\"}')
    count += 1
print(f'Total npm packages: {count}', file=__import__('sys').stderr)
" 2>/dev/null | head -50
fi

# Python
if [ -f "requirements.txt" ]; then
  echo "--- Python Dependencies ---"
  python3 -c "
import re
with open('requirements.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'): continue
        match = re.match(r'([a-zA-Z0-9_.-]+)\s*([=<>!~]+\s*\S+)?', line)
        if match:
            name = match.group(1)
            version = match.group(2) or 'any'
            print(f'{name}|{version.strip()}|UNKNOWN|prod')
" 2>/dev/null
fi

# Go
if [ -f "go.sum" ]; then
  echo "--- Go Dependencies ---"
  python3 -c "
import re
seen = set()
with open('go.sum') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            name = parts[0]
            version = parts[1].split('/')[0]
            key = f'{name}@{version}'
            if key not in seen:
                seen.add(key)
                print(f'{name}|{version}|UNKNOWN|prod')
" 2>/dev/null | head -50
fi

# Rust
if [ -f "Cargo.lock" ]; then
  echo "--- Rust Dependencies ---"
  python3 -c "
import re
with open('Cargo.lock') as f:
    content = f.read()
for match in re.finditer(r'name = \"([^\"]+)\"\nversion = \"([^\"]+)\"', content):
    print(f'{match.group(1)}|{match.group(2)}|UNKNOWN|prod')
" 2>/dev/null | head -50
fi
```

#### Step 3: License Detection

```bash
echo ""
echo "=== License Analysis ==="

# For npm: licenses are in package-lock.json and package.json
if [ -f "package-lock.json" ]; then
  python3 -c "
import json
from collections import Counter

lock = json.load(open('package-lock.json'))
licenses = Counter()
unknown = []

for name, info in lock.get('packages', {}).items():
    if not name: continue
    lic = info.get('license', 'UNKNOWN')
    if isinstance(lic, dict):
        lic = lic.get('type', 'UNKNOWN')
    licenses[lic] += 1
    if lic == 'UNKNOWN':
        unknown.append(name.replace('node_modules/', ''))

print('License Distribution:')
for lic, count in licenses.most_common():
    print(f'  {lic}: {count}')

if unknown:
    print(f'\nUnknown licenses ({len(unknown)}):')
    for pkg in unknown[:10]:
        print(f'  {pkg}')

# Flag copyleft licenses
copyleft = ['GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'LGPL-2.1', 'LGPL-3.0', 'MPL-2.0', 'EUPL-1.2', 'SSPL-1.0']
risky = {l: c for l, c in licenses.items() if any(l.startswith(cp) for cp in copyleft)}
if risky:
    print('\n⚠️  Copyleft licenses detected (may restrict distribution):')
    for lic, count in risky.items():
        print(f'  {lic}: {count}')
" 2>/dev/null
fi
```

#### Step 4: Vulnerability Check

```bash
echo ""
echo "=== Vulnerability Scan ==="

# npm audit
if [ -f "package-lock.json" ]; then
  npm audit --json 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    vulns = d.get('metadata', {}).get('vulnerabilities', {})
    total = sum(vulns.values())
    print(f'npm vulnerabilities: {total}')
    for severity in ['critical', 'high', 'moderate', 'low']:
        count = vulns.get(severity, 0)
        if count > 0:
            icon = '❌' if severity in ['critical', 'high'] else '⚠️'
            print(f'  {icon} {severity}: {count}')
    if total == 0:
        print('  ✅ No known vulnerabilities')
except:
    print('  Could not parse npm audit')
" 2>/dev/null
fi

# pip-audit
if [ -f "requirements.txt" ] && command -v pip-audit &>/dev/null; then
  pip-audit -r requirements.txt 2>/dev/null | head -20
fi

# Go vuln check
if [ -f "go.sum" ] && command -v govulncheck &>/dev/null; then
  govulncheck ./... 2>/dev/null | head -20
fi
```

### 2. `cyclonedx` — Generate CycloneDX SBOM

Output in CycloneDX 1.5 JSON format:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "serialNumber": "urn:uuid:<generated>",
  "version": 1,
  "metadata": {
    "timestamp": "<ISO 8601>",
    "tools": [{"name": "sbom-generator", "version": "1.0.0"}],
    "component": {
      "type": "application",
      "name": "<project name>",
      "version": "<project version>"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "<package>",
      "version": "<version>",
      "purl": "pkg:npm/<package>@<version>",
      "licenses": [{"license": {"id": "<SPDX ID>"}}],
      "scope": "required"
    }
  ]
}
```

### 3. `spdx` — Generate SPDX SBOM

Output in SPDX 2.3 JSON format.

### 4. `licenses` — License Compliance Report

Focus on license analysis only:
- Distribution by license type
- Copyleft detection (GPL, AGPL, SSPL)
- License compatibility matrix
- Unknown/missing licenses
- Recommendations for compliance

```markdown
## License Compliance Report

### Summary
- Total packages: 247
- Permissive (MIT, Apache-2.0, BSD): 231 (93.5%)
- Copyleft (GPL, LGPL, MPL): 8 (3.2%)
- Unknown: 8 (3.2%)

### Action Required
1. ❌ 3 packages under GPL-3.0 — may require source disclosure
2. ⚠️  8 packages with unknown licenses — verify manually
3. ✅ 231 packages are permissive — no restrictions
```

### 5. `diff` — SBOM Diff Between Versions

Compare two SBOMs to find what changed:

```
Added dependencies:
  + @tanstack/react-query 5.0.0 (MIT)
  + zod 3.22.0 (MIT)

Removed dependencies:
  - react-query 3.39.0 (MIT)
  - yup 1.2.0 (MIT)

Version changes:
  ~ react 18.2.0 → 18.3.0
  ~ typescript 5.2.0 → 5.3.0

License changes:
  ~ some-package: MIT → Apache-2.0
```

### 6. `policy` — Check Against License Policy

Define allowed/denied licenses in `.sbom-policy.json`:

```json
{
  "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD", "Unlicense", "CC0-1.0"],
  "denied": ["GPL-3.0", "AGPL-3.0", "SSPL-1.0"],
  "review_required": ["GPL-2.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "EUPL-1.2"],
  "allow_unknown": false
}
```

Exit codes:
- 0: All dependencies comply with policy
- 1: Denied license found
- 2: Unknown license and `allow_unknown` is false

## Output Formats

- **text** (default): Human-readable inventory
- **json**: CycloneDX 1.5 or SPDX 2.3 (specify with `--format cyclonedx` or `--format spdx`)
- **csv**: Spreadsheet-friendly `name,version,license,scope,purl`
- **markdown**: Report with tables for documentation

## Compliance Standards

This skill helps with:
- **EU Cyber Resilience Act (CRA)**: Requires SBOM for software products sold in EU
- **US Executive Order 14028**: Federal software procurement requires SBOM
- **FDA**: Medical device software must include SBOM
- **NIST SSDF**: Recommends SBOM generation as part of secure development
- **PCI DSS 4.0**: Software inventory requirements

## Notes

- Extracts from lock files for accurate, reproducible results (not manifest files)
- License detection uses SPDX identifiers when available
- Vulnerability scanning requires network access (npm audit, pip-audit, govulncheck)
- For private registries, ensure authentication is configured
- PURL (Package URL) format follows the PURL spec for universal package identification
- Run in CI to generate SBOM on every release (commit to artifacts or registry)
