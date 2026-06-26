#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-win-edge}"
CDP_URL="${2:-}"

if [[ -z "$CDP_URL" ]]; then
  if command -v openclaw >/dev/null 2>&1; then
    CDP_URL=$(openclaw browser --browser-profile "$PROFILE" status 2>/dev/null | awk -F': ' '/cdpUrl:/ {print $2; exit}' || true)
  fi
fi

if [[ -z "$CDP_URL" ]]; then
  WIN_IP=$(ip route 2>/dev/null | awk '/default/ {print $3; exit}')
  CDP_URL="http://${WIN_IP}:9223"
fi

TMP_JSON=$(mktemp)
trap 'rm -f "$TMP_JSON"' EXIT

if ! curl -sS --max-time 8 "$CDP_URL/json/list" > "$TMP_JSON"; then
  echo "VERDICT: STOP"
  echo "Reason: CDP endpoint is not reachable: $CDP_URL"
  exit 2
fi

node - <<'NODE' "$TMP_JSON" "$CDP_URL"
const fs = require('fs');
const targets = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const cdpUrl = process.argv[3];
const byType = {};
const byDomain = {};
let recaptcha = 0;
for (const t of targets) {
  byType[t.type] = (byType[t.type] || 0) + 1;
  const url = t.url || '';
  if (url.includes('google.com/recaptcha')) recaptcha++;
  let domain = '(blank/invalid)';
  try { if (url) domain = new URL(url).hostname || domain; } catch {}
  byDomain[domain] ||= { total: 0, page: 0, iframe: 0, worker: 0 };
  byDomain[domain].total++;
  byDomain[domain][t.type] = (byDomain[domain][t.type] || 0) + 1;
}
const pages = byType.page || 0;
const iframes = byType.iframe || 0;
const workers = byType.worker || 0;
const total = targets.length;
let verdict = 'OK';
const reasons = [];
if (total > 30) { verdict = 'STOP'; reasons.push(`CDP targets ${total} > 30`); }
if (pages > 10) { verdict = verdict === 'STOP' ? verdict : 'CAUTION'; reasons.push(`page targets ${pages} > 10`); }
if ((iframes + workers) > Math.max(6, pages * 2)) { verdict = 'STOP'; reasons.push(`iframe/worker targets ${iframes + workers} are high vs pages ${pages}`); }
if (recaptcha > 0) { verdict = 'STOP'; reasons.push(`reCAPTCHA targets detected: ${recaptcha}`); }
console.log(`CDP: ${cdpUrl}`);
console.log(`VERDICT: ${verdict}`);
console.log(`Targets: total=${total} pages=${pages} iframes=${iframes} workers=${workers} recaptcha=${recaptcha}`);
if (reasons.length) console.log(`Reasons: ${reasons.join('; ')}`);
console.log('Domains:');
for (const [domain, v] of Object.entries(byDomain).sort((a,b)=>b[1].total-a[1].total)) {
  console.log(`- ${domain}: total=${v.total} page=${v.page||0} iframe=${v.iframe||0} worker=${v.worker||0}`);
}
console.log('Pages:');
for (const t of targets.filter(t=>t.type==='page')) {
  console.log(`- ${(t.title || '(untitled)').replace(/\s+/g,' ').slice(0,80)} — ${t.url}`);
}
NODE

if command -v free >/dev/null 2>&1; then
  echo "Linux memory:"
  free -h | sed -n '1,3p'
fi

PS='/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
if [[ -x "$PS" ]]; then
  PS1=$(mktemp --suffix=.ps1)
  cat > "$PS1" <<'PS'
$p = Get-Process msedge -ErrorAction SilentlyContinue
if (-not $p) { 'Edge memory: NO_EDGE'; exit }
$sum = ($p | Measure-Object WorkingSet64 -Sum).Sum
$priv = ($p | Measure-Object PrivateMemorySize64 -Sum).Sum
[pscustomobject]@{
  EdgeProcesses = $p.Count
  EdgeWorkingSetMB = [math]::Round($sum / 1MB, 1)
  EdgePrivateMB = [math]::Round($priv / 1MB, 1)
} | ConvertTo-Json -Compress
PS
  WIN_PS1=$(wslpath -w "$PS1")
  "$PS" -NoProfile -ExecutionPolicy Bypass -File "$WIN_PS1" 2>/dev/null | sed 's/\r$//' || true
  rm -f "$PS1"
fi
