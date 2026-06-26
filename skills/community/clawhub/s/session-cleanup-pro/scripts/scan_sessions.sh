#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-scan}"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
AGENT_ID="${OPENCLAW_AGENT_ID:-main}"
SESSIONS_DIR="$STATE_DIR/agents/$AGENT_ID/sessions"
SESSIONS_JSON="$SESSIONS_DIR/sessions.json"
NOW_MS=$(node -e 'console.log(Date.now())')
PROTECT_MS=$((72*60*60*1000))

if [[ ! -f "$SESSIONS_JSON" ]]; then
  echo "ERROR: sessions.json not found: $SESSIONS_JSON" >&2
  exit 1
fi

node - "$SESSIONS_JSON" "$SESSIONS_DIR" "$NOW_MS" "$PROTECT_MS" "$MODE" <<'NODE'
const fs = require('fs');
const path = require('path');
const [sessionsJsonPath, sessionsDir, nowMsRaw, protectMsRaw, mode] = process.argv.slice(2);
const nowMs = Number(nowMsRaw);
const protectMs = Number(protectMsRaw);
const sessions = JSON.parse(fs.readFileSync(sessionsJsonPath, 'utf8'));

const registeredFiles = new Set();
const registeredRows = [];
for (const [key, meta] of Object.entries(sessions)) {
  const sf = meta?.sessionFile ? path.basename(meta.sessionFile) : null;
  if (sf) registeredFiles.add(sf);
  const updatedAt = Number(meta?.updatedAt || 0);
  const ageMs = updatedAt ? nowMs - updatedAt : Number.MAX_SAFE_INTEGER;
  const isProtected = key === 'agent:main:main' || ageMs < protectMs;
  registeredRows.push({
    key,
    sessionFile: sf,
    updatedAt,
    ageHours: updatedAt ? Math.round(ageMs / 36e5) : null,
    isProtected,
  });
}

const diskFiles = fs.readdirSync(sessionsDir)
  .filter((f) => f.endsWith('.jsonl'))
  .sort();

const orphans = diskFiles.filter((f) => !registeredFiles.has(f));

const stale = registeredRows
  .filter((r) => !r.isProtected)
  .sort((a, b) => (b.ageHours || 0) - (a.ageHours || 0));

const orphanSizeBytes = orphans.reduce((sum, f) => {
  const st = fs.statSync(path.join(sessionsDir, f));
  return sum + st.size;
}, 0);

const summary = {
  mode,
  sessionsDir,
  sessionsJsonPath,
  protectHours: 72,
  totals: {
    registered: registeredRows.length,
    onDiskJsonl: diskFiles.length,
    orphanCount: orphans.length,
    staleCount: stale.length,
    reclaimBytesOrphans: orphanSizeBytes,
  },
  orphanFiles: orphans,
  staleSessions: stale.map((r) => ({
    key: r.key,
    sessionFile: r.sessionFile,
    updatedAt: r.updatedAt,
    ageHours: r.ageHours,
  })),
  protectedSessions: registeredRows.filter((r) => r.isProtected).map((r) => ({
    key: r.key,
    sessionFile: r.sessionFile,
    updatedAt: r.updatedAt,
    ageHours: r.ageHours,
  })),
};

console.log(JSON.stringify(summary, null, 2));
NODE