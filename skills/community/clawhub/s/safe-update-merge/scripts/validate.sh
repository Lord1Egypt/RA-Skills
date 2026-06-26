#!/usr/bin/env bash
# safe-merge-update: Post-merge validation
set -euo pipefail

REPO_DIR="${REPO_DIR:?REPO_DIR must be set to your OpenClaw repo path}"
MANIFEST="${MANIFEST:-$(dirname "$0")/../MERGE_MANIFEST.json}"
REPORT_DIR="/tmp/safe-merge"
REPORT="$REPORT_DIR/validation-report.json"
ERRORS=()
WARNINGS=()

mkdir -p "$REPORT_DIR"
cd "$REPO_DIR"

# Auto-detect package manager
if [[ -f "package-lock.json" ]]; then
  PKG="npm"
elif [[ -f "pnpm-lock.yaml" ]] && command -v pnpm &>/dev/null; then
  PKG="pnpm"
elif command -v npm &>/dev/null; then
  PKG="npm"
else
  echo "❌ No package manager found (npm or pnpm required)" >&2
  exit 1
fi

echo "=== Post-Merge Validation (using ${PKG}) ==="
echo ""

# ─── Check 1: install ───
echo ">>> Check 1: ${PKG} install (--ignore-scripts for safety)..."
INSTALL_OK=false
if [[ "$PKG" == "pnpm" ]]; then
  if pnpm install --frozen-lockfile --ignore-scripts 2>&1 | tail -5; then
    INSTALL_OK=true
  elif pnpm install --ignore-scripts 2>&1 | tail -5; then
    INSTALL_OK=true
    WARNINGS+=("pnpm lockfile was updated during install")
  fi
else
  if npm ci --ignore-scripts 2>&1 | tail -5; then
    INSTALL_OK=true
  elif npm install --ignore-scripts 2>&1 | tail -5; then
    INSTALL_OK=true
    WARNINGS+=("npm lockfile was updated during install")
  fi
fi
if $INSTALL_OK; then
  echo "✅ install succeeded"
else
  echo "❌ install failed"
  ERRORS+=("${PKG} install failed")
fi

# ─── Check 2: build ───
echo ""
echo ">>> Check 2: ${PKG} run build..."
if "$PKG" run build 2>&1 | tail -10; then
  echo "✅ Build succeeded"
else
  echo "❌ Build FAILED"
  ERRORS+=("${PKG} build failed — TypeScript compilation errors")
fi

# ─── Check 2b: TypeScript undefined-name check (catches zombie/shadow bugs) ───
# tsdown/rolldown does NOT type-check — a function can reference undefined symbols,
# compile cleanly, and crash at runtime. This step runs tsgo --noEmit and filters for
# TS2304 (Cannot find name) and TS2305 (no exported member) errors in src/secrets/
# and src/gateway/ — the areas most likely to regress during a secrets refactor.
echo ""
echo ">>> Check 2b: TypeScript undefined-name check (src/secrets/ + src/gateway/)..."
if command -v node_modules/.bin/tsgo &>/dev/null; then
  TS_ERRORS=$(node_modules/.bin/tsgo --noEmit 2>&1 \
    | grep -E "^(src/secrets/|src/gateway/)" \
    | grep -E "error TS(2304|2305|2306):" \
    || true)
  if [[ -z "$TS_ERRORS" ]]; then
    echo "✅ No undefined-name errors in src/secrets/ or src/gateway/"
  else
    echo "❌ TypeScript undefined-name errors found (these WILL crash at runtime):"
    echo "$TS_ERRORS"
    ERRORS+=("TypeScript undefined-name errors in critical paths — check for zombie functions shadowing imports")
  fi
else
  WARNINGS+=("tsgo not found — skipped undefined-name check (install @typescript/native-preview for this check)")
fi

# ─── Check 3: ui:build ───
echo ""
echo ">>> Check 3: ${PKG} run ui:build..."
if "$PKG" run ui:build 2>&1 | tail -5; then
  echo "✅ UI build succeeded"
else
  echo "❌ UI build FAILED"
  ERRORS+=("${PKG} ui:build failed")
fi

# ─── Check 4: Protected tabs in navigation.ts ───
echo ""
echo ">>> Check 4: Protected tabs in navigation.ts..."
NAV_FILE="ui/src/ui/navigation.ts"
REQUIRED_TABS=("jarvis" "mode" "usage" "memory" "agents" "sessions" "discord" "pipedream" "zapier")
for tab in "${REQUIRED_TABS[@]}"; do
  if grep -q "\"$tab\"" "$NAV_FILE" 2>/dev/null; then
    echo "  ✅ Tab '$tab' present"
  else
    echo "  ❌ Tab '$tab' MISSING"
    ERRORS+=("Tab '$tab' missing from navigation.ts")
  fi
done

# ─── Check 5: Protected files exist ───
echo ""
echo ">>> Check 5: Protected files from manifest..."
if [[ -f "$MANIFEST" ]]; then
  while IFS= read -r pf; do
    [[ -z "$pf" ]] && continue
    if [[ -f "$pf" ]]; then
      echo "  ✅ $pf"
    else
      echo "  ❌ MISSING: $pf"
      ERRORS+=("Protected file missing: $pf")
    fi
  done < <(python3 -c "
import json, sys
with open('$MANIFEST') as f:
    m = json.load(f)
for path in m.get('protectedFiles', {}):
    print(path)
" 2>/dev/null)
fi

# ─── Check 6: Custom new files still exist ───
echo ""
echo ">>> Check 6: Custom new files..."
NEW_FILES=(
  "ui/src/ui/views/jarvis-view.ts"
  "ui/src/ui/views/memory.ts"
  "ui/src/ui/views/mode.ts"
  "ui/src/ui/views/sessions-history-modal.ts"
  "ui/src/ui/plugins/registry.ts"
  "ui/src/ui/controllers/mode.ts"
)
for nf in "${NEW_FILES[@]}"; do
  if [[ -f "$nf" ]]; then
    echo "  ✅ $nf"
  else
    echo "  ❌ MISSING: $nf"
    ERRORS+=("Custom file deleted: $nf")
  fi
done

# ─── Check 7: Must-preserve patterns ───
echo ""
echo ">>> Check 7: Must-preserve patterns..."
declare -A CRITICAL_PATTERNS
CRITICAL_PATTERNS=(
  ["uiPluginRegistry"]="ui/src/ui/plugins/registry.ts"
  ["BackgroundJobToast"]="ui/src/ui/app-view-state.ts"
  ["backgroundJobToasts"]="ui/src/ui/app-view-state.ts"
  ["compactionStatus"]="ui/src/ui/app-view-state.ts"
  ["renderMemory"]="ui/src/ui/app-render.ts"
  ["renderMode"]="ui/src/ui/app-render.ts"
  ["jarvis-view"]="ui/src/ui/app-render.ts"
  ["loadModeStatus"]="ui/src/ui/app-settings.ts"
  ["loadArchivedSessions"]="ui/src/ui/app-settings.ts"
)
for pattern in "${!CRITICAL_PATTERNS[@]}"; do
  file="${CRITICAL_PATTERNS[$pattern]}"
  if grep -q "$pattern" "$file" 2>/dev/null; then
    echo "  ✅ '$pattern' in $file"
  else
    echo "  ❌ '$pattern' NOT FOUND in $file"
    ERRORS+=("Pattern '$pattern' missing from $file")
  fi
done

# ─── Check 8: Plugin registry export ───
echo ""
echo ">>> Check 8: Plugin registry export..."
if grep -q "export const uiPluginRegistry" "ui/src/ui/plugins/registry.ts" 2>/dev/null; then
  echo "  ✅ uiPluginRegistry exported"
else
  echo "  ❌ uiPluginRegistry export missing"
  ERRORS+=("uiPluginRegistry export missing from plugins/registry.ts")
fi

# ─── Check 9: Post-restart smoke test ───
# Only runs if the gateway was restarted as part of this merge (safe-merge-update.sh does this).
# Checks HTTP health endpoint + crash keywords in recent journal logs.
echo ""
echo ">>> Check 9: Post-restart smoke test (if gateway was restarted)..."
if [[ "${SKIP_SMOKE_TEST:-false}" != "true" ]] && [[ -f "scripts/smoke-test.sh" ]]; then
  if bash scripts/smoke-test.sh 2>&1; then
    echo "✅ Smoke test passed"
  else
    SMOKE_EXIT=$?
    if [[ $SMOKE_EXIT -eq 2 ]]; then
      WARNINGS+=("Smoke test: gateway up but crash keywords in logs — check journalctl -u openclaw-gateway")
    else
      ERRORS+=("Smoke test: gateway did not start cleanly after restart")
    fi
  fi
else
  echo "  (skipped — set SKIP_SMOKE_TEST=false and ensure scripts/smoke-test.sh exists to enable)"
fi

# ─── Summary ───
echo ""
echo "=== Validation Summary ==="
ERROR_COUNT=${#ERRORS[@]}
WARN_COUNT=${#WARNINGS[@]}

if [[ "$ERROR_COUNT" -eq 0 ]]; then
  echo "✅ ALL CHECKS PASSED ($WARN_COUNT warnings)"
  STATUS="pass"
else
  echo "❌ $ERROR_COUNT ERRORS, $WARN_COUNT WARNINGS"
  STATUS="fail"
  echo ""
  echo "Errors:"
  for e in "${ERRORS[@]}"; do
    echo "  ❌ $e"
  done
fi

if [[ "$WARN_COUNT" -gt 0 ]]; then
  echo ""
  echo "Warnings:"
  for w in "${WARNINGS[@]}"; do
    echo "  ⚠️  $w"
  done
fi

# ─── Write JSON report ───
python3 - <<PYEOF
import json
errors = ${ERRORS[@]+"$(printf '"%s",' "${ERRORS[@]}" | sed 's/,$//; s/,/","/g')"}
warnings = ${WARNINGS[@]+"$(printf '"%s",' "${WARNINGS[@]}" | sed 's/,$//; s/,/","/g')"}
report = {
    "status": "$STATUS",
    "errorCount": $ERROR_COUNT,
    "warningCount": $WARN_COUNT,
    "errors": [e for e in """${ERRORS[*]:-}""".split("\n") if e] if $ERROR_COUNT > 0 else [],
    "warnings": [w for w in """${WARNINGS[*]:-}""".split("\n") if w] if $WARN_COUNT > 0 else [],
}
with open("$REPORT", "w") as f:
    json.dump(report, f, indent=2)
print(f"Report written to $REPORT")
PYEOF

echo ""
echo "=== Validation Complete ==="
exit "$ERROR_COUNT"
