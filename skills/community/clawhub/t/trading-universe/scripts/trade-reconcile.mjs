#!/usr/bin/env node
// Reconcile tracked tickets from Yahoo candles without TradingView drawings.
// Default is dry-run. Pass --apply to atomically update the ledger after making
// a timestamped backup. Dashboard mode calls the same lifecycle functions.
import { copyFile, readFile, rename, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { ACTIVE_STATUSES, TRADE_SCHEMA_VERSION, fetchLifecycleCandles, migrateTradeDocument, performanceStats, reconcileTrade } from "./trade-lifecycle.mjs";
import { normalizeAsset } from "./symbols.mjs";

const DATA_DIR = process.env.TRADE_DATA_DIR || join(homedir(), ".trading-universe");
const FILE = process.env.TRADES_FILE || join(DATA_DIR, "live-trades.json");
const apply = process.argv.includes("--apply");
const raw = JSON.parse(await readFile(FILE, "utf8"));
const migrated = migrateTradeDocument(raw).document;
const active = migrated.trades.filter((t) => ACTIVE_STATUSES.has(t.status));
const byAsset = new Map();
for (const t of active) {
  const asset = normalizeAsset(t.asset), start = new Date(t.orderPlacedAt || t.activatedAt).getTime();
  if (!Number.isFinite(start)) continue;
  const old = byAsset.get(asset); if (!old || start < old) byAsset.set(asset, start);
}
const feeds = new Map(), errors = [];
await Promise.all([...byAsset].map(async ([asset, start]) => {
  try { feeds.set(asset, await fetchLifecycleCandles(asset, start)); }
  catch (e) { errors.push({ asset, error: e.message }); }
}));

const changes = [];
for (const t of active) {
  const f = feeds.get(normalizeAsset(t.asset)); if (!f) continue;
  const before = { status: t.status, outcome: t.outcome, filledAt: t.filledAt, tp1HitAt: t.tp1HitAt, mfeR: t.mfeR, maeR: t.maeR };
  const start = new Date(t.orderPlacedAt || t.activatedAt).getTime();
  const rows = f.candles.filter((c) => c.t >= start); rows.interval = f.interval;
  const result = reconcileTrade(t, rows);
  if (result.changed) changes.push({ id: t.id, asset: t.asset, before, after: {
    status: t.status, outcome: t.outcome, filledAt: t.filledAt, tp1HitAt: t.tp1HitAt, eventClosedAt: t.eventClosedAt, mfeR: t.mfeR, maeR: t.maeR,
  }, interval: f.interval });
}

if (apply && (changes.length || raw.schemaVersion !== TRADE_SCHEMA_VERSION)) {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  await copyFile(FILE, `${FILE}.pre-v2-${stamp}.bak`);
  const tmp = `${FILE}.tmp`;
  await writeFile(tmp, JSON.stringify({ schemaVersion: TRADE_SCHEMA_VERSION, updatedAt: new Date().toISOString(), trades: migrated.trades }, null, 2));
  await rename(tmp, FILE);
}

console.log(JSON.stringify({ mode: apply ? "applied" : "dry-run", file: FILE, activeChecked: active.length, changes, errors,
  performance: performanceStats(migrated.trades) }, null, 2));
