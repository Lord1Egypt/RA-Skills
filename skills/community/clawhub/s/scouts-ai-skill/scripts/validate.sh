#!/usr/bin/env bash
# Minimal validation for the scouts-ai-search skill.
# Runs locally; no external network calls.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

# 1. SKILL.md frontmatter: regex sanity check (no PyYAML dependency).
python3 - "$root/SKILL.md" <<'PY'
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
text = path.read_text()
m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
if not m:
    print("SKILL.md: missing YAML frontmatter", file=sys.stderr)
    sys.exit(1)
fm = m.group(1)
required = ("name:", "description:", "version:")
for key in required:
    if not re.search(rf"(?m)^{re.escape(key)}\s+\S", fm):
        print(f"SKILL.md: missing frontmatter key: {key}", file=sys.stderr)
        sys.exit(1)
if "openclaw" not in fm:
    print("SKILL.md: missing openclaw runtime metadata", file=sys.stderr)
    sys.exit(1)
print("SKILL.md: frontmatter OK")
PY

# 2. Bash block sanity: every API call must use the full safe-call pattern.
python3 - "$root/SKILL.md" <<'PY'
import re, sys, pathlib
text = pathlib.Path(sys.argv[1]).read_text()
blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
required_patterns = {
    "mktemp temp dir":        r"\bmktemp\b",
    "mktemp -d":              r"\bmktemp\s+-d\b",
    "umask 077":              r"\bumask\s+077\b",
    "trap cleanup":           r"\btrap\b.*\brm\b",
    "curl -D headers":        r"\bcurl\b.*-D\b",
    "curl -w http_code":      r"-w\s+.*%\{http_code\}(?!\w)",
    "no fixed /tmp paths":    r"/tmp/[A-Za-z0-9_\-]+\.(txt|json|log|body)\b",
}
FLAGS = re.DOTALL
for i, b in enumerate(blocks, 1):
    if "scouts-ai.com/api/search" not in b:
        continue
    for label, pat in required_patterns.items():
        if label == "no fixed /tmp paths":
            if re.search(pat, b, FLAGS):
                print(f"SKILL.md bash block #{i}: uses fixed /tmp path; use $tmpdir/<name>", file=sys.stderr)
                sys.exit(1)
            continue
        if not re.search(pat, b, FLAGS):
            print(f"SKILL.md bash block #{i}: missing {label} (pattern: {pat})", file=sys.stderr)
            sys.exit(1)
print(f"SKILL.md: {len(blocks)} bash block(s) OK")
PY

# 3. License / README must be MIT-0 aligned and point to a real LICENSE file.
test -f "$root/LICENSE" || { echo "LICENSE missing"; exit 1; }
grep -qiE "MIT-?0|MIT No Attribution" "$root/LICENSE" || { echo "LICENSE must be MIT-0"; exit 1; }
grep -q "MIT-0" "$root/README.md" || { echo "README must declare MIT-0"; exit 1; }
echo "LICENSE/README: OK"

# 4. Smoke test the curl wrapper pattern offline.
bash "$root/scripts/smoke.sh"

echo "All checks passed."
