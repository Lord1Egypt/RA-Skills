#!/usr/bin/env bash
set -euo pipefail

root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [[ $# -gt 1 ]]; then
  printf 'usage: %s [package-root]\n' "$0" >&2
  exit 2
fi
if [[ $# -eq 1 ]]; then
  root="$(CDPATH= cd -- "$1" && pwd)"
fi

fail() { printf 'validation failed: %s\n' "$1" >&2; exit 1; }
require_file() { [[ -f "$root/$1" ]] || fail "missing $1"; }

command -v rg >/dev/null 2>&1 || fail 'rg is required for security scans'

for file in SKILL.md README.md LICENSE PROVENANCE.md VERSION SECURITY.md RELEASE.md; do
  require_file "$file"
done

# The public skill has a deliberately small, stable top-level layout.
while IFS= read -r -d '' path; do
  rel="${path#"$root/"}"
  case "$rel" in
    SKILL.md|README.md|LICENSE|PROVENANCE.md|VERSION|SECURITY.md|RELEASE.md|package.json|package-lock.json|requirements*.txt|pyproject.toml|Cargo.toml|Cargo.lock|go.mod|go.sum|scripts/*|tests/*|.github/workflows/*|tests/fixtures/*)
      ;;
    *) fail "unexpected package path: $rel" ;;
  esac
done < <(find "$root" -type f -not -path '*/.git/*' -print0)

# Frontmatter is intentionally exact: three required fields, no credentials or executable directives.
frontmatter="$(mktemp)"
trap 'rm -f "$frontmatter"' EXIT
awk 'NR == 1 && $0 == "---" { open=1; next }
     open && NR <= 8 { print; if ($0 == "---") { ended=1; exit } }
     END { if (!open || !ended) exit 1 }' "$root/SKILL.md" >"$frontmatter" || fail 'SKILL.md frontmatter delimiters'
grep -Fx 'name: replynodes' "$frontmatter" >/dev/null || fail 'SKILL.md name'
grep -Fx 'description: Approval-first social media publishing with the ReplyNodes scheduler for cross-posting and auto-posting in OpenClaw, using browser OAuth for LinkedIn and X/Twitter.' "$frontmatter" >/dev/null || fail 'SKILL.md description'
grep -Fx 'homepage: https://replynodes.com/openclaw' "$frontmatter" >/dev/null || fail 'SKILL.md homepage'
[[ "$(grep -c '^---$' "$frontmatter")" -eq 1 ]] || fail 'SKILL.md frontmatter shape'
[[ "$(head -n 1 "$root/SKILL.md")" == '---' ]] || fail 'SKILL.md frontmatter start'

# Scan tracked package text for common credential forms. The scanner itself is excluded so its
# detection expressions cannot self-match. Test fixtures are excluded only when validating the
# package root; validating an individual fixture directly still scans all of its contents.
fixture_glob=()
if [[ -d "$root/tests/fixtures" ]]; then
  fixture_glob=(--glob '!**/tests/fixtures/**')
fi
if rg -n -I --hidden --glob '!scripts/validate-package.sh' --glob '!.git/**' "${fixture_glob[@]}" \
  '(AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|Bearer[[:space:]]+[A-Za-z0-9._-]{24,}|(api[_-]?key|client[_-]?secret|access[_-]?token|session[_-]?token)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9._-]{16,})' "$root" >/dev/null; then
  fail 'credential-like value found'
fi

# Executable code must remain human-readable and reviewable. Shell scripts are the only
# executable source currently permitted; minified/obfuscated executable source is rejected.
while IFS= read -r -d '' path; do
  rel="${path#"$root/"}"
  case "$rel" in
    scripts/*.sh|tests/*.sh) ;;
    *) fail "unexpected executable file: $rel" ;;
  esac
done < <(find "$root" -type f -perm /111 -not -path '*/.git/*' -print0)
if rg -n -I --hidden --glob '!.git/**' --glob '!scripts/validate-package.sh' "${fixture_glob[@]}" \
  '(^|[[:space:]])(eval|exec)[[:space:]]|base64[[:space:]]+(-d|--decode)|[A-Fa-f0-9]{80,}' "$root" >/dev/null; then
  fail 'obfuscated or encoded executable content found'
fi
while IFS= read -r -d '' path; do
  awk 'length($0) > 500 { exit 1 }' "$path" || fail "minified line in ${path#"$root/"}"
done < <(find "$root" -type f \( -name '*.js' -o -name '*.ts' -o -name '*.mjs' -o -name '*.cjs' -o -name '*.py' \) -print0)

# Shell safety policy: data is passed as arguments/stdin, never evaluated or interpolated into a command.
shell_unsafe='(^|[;&|])[[:space:]]*(eval|bash[[:space:]]+-c|sh[[:space:]]+-c|xargs[[:space:]]+(-I[^ ]+[[:space:]]+)?(sh|bash))|curl[^\n]*[$][A-Za-z_{]|wget[^\n]*[$][A-Za-z_{]'
if rg -n -I --glob '*.sh' --glob '!scripts/validate-package.sh' "${fixture_glob[@]}" "$shell_unsafe" "$root" >/dev/null; then
  fail 'unsafe shell interpolation or command execution pattern found'
fi

# Dependencies are not needed today. If a manifest is added, it must have a lockfile where
# applicable, exact versions, and a deterministic high-severity audit.
if [[ -f "$root/package.json" ]]; then
  require_file package-lock.json
  command -v node >/dev/null || fail 'node is required when package.json exists'
  node - "$root/package.json" <<'NODE' || fail 'package dependency is not exactly pinned'
const fs = require('fs');
const packageJson = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const sections = ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies'];
const exact = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/;
for (const section of sections) {
  for (const [name, version] of Object.entries(packageJson[section] || {})) {
    if (typeof version !== 'string' || !exact.test(version)) {
      console.error(`${section}.${name} must use an exact numeric version`);
      process.exit(1);
    }
  }
}
NODE
  command -v npm >/dev/null || fail 'npm is required when package.json exists'
  npm audit --package-lock-only --audit-level=high --ignore-scripts --prefix "$root" >/dev/null
fi

for manifest in "$root"/requirements*.txt; do
  [[ -f "$manifest" ]] || continue
  while IFS= read -r dependency || [[ -n "$dependency" ]]; do
    dependency="${dependency%%#*}"
    [[ -z "${dependency//[[:space:]]/}" || "$dependency" == -* ]] && continue
    [[ "$dependency" =~ ^[A-Za-z0-9_.-]+(\[[A-Za-z0-9_,.-]+\])?==[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]] ||
      fail "dependency is not exactly pinned: ${manifest#"$root/"}"
  done < "$manifest"
done

for manifest in "$root/pyproject.toml" "$root/Cargo.toml" "$root/go.mod"; do
  [[ -f "$manifest" ]] || continue
  floating_version="([\"'](latest|\*|\^|~|>=|<=|>|<)|[=:][[:space:]]*[\"']?(latest|\*|\^|~|>=|<=|>|<))"
  if rg -n -I "$floating_version" "$manifest" >/dev/null; then
    fail "dependency range or floating version found: ${manifest#"$root/"}"
  fi
done

grep -Eiq 'untrusted|structured (JSON|data)|never.*instructions' "$root/SKILL.md" || fail 'untrusted source-data boundary not documented'
grep -Eiq 'MIT License' "$root/LICENSE" || fail 'license missing'
grep -Eiq 'source|provenance|issue #149' "$root/PROVENANCE.md" || fail 'provenance missing'

version="$(tr -d '[:space:]' <"$root/VERSION")"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail 'VERSION is not SemVer'
grep -F "@v$version" "$root/README.md" >/dev/null || fail 'README install tag does not match VERSION'
grep -F "v$version" "$root/RELEASE.md" >/dev/null || fail 'release metadata does not mention VERSION'

echo "ReplyNodes skill package validation passed (version $version)"
