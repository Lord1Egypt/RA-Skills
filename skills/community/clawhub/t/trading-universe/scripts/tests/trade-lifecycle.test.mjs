import test from "node:test";
import assert from "node:assert/strict";
import { migrateTradeDocument, reconcileTrade, snapshotTicket, validateTicket } from "../trade-lifecycle.mjs";
import { symbolForAsset } from "../symbols.mjs";
import { filterForwardDraws, findFvgs, findOrderBlocks } from "../zone-lifecycle.mjs";

const base = (overrides = {}) => ({
  id: "t1", asset: "EURUSD", direction: "LONG", entryType: "limit",
  entry: 100, sl: 90, tp1: 120, tp2: 140, r1: 2, r2: 4,
  status: "pending", orderPlacedAt: "2026-07-10T00:00:00Z", events: [],
  ...overrides,
});
const bar = (min, o, h, l, c) => ({ t: Date.parse("2026-07-10T00:00:00Z") + min * 60000, o, h, l, c });

test("validates ordering and RR", () => {
  assert.equal(validateTicket(base()).ok, true);
  assert.equal(validateTicket(base({ sl: 105 })).ok, false);
  assert.equal(validateTicket(base({ tp1: 110 })).ok, false);
  assert.equal(validateTicket(base({ tp1: 110 }), { skipRR: true }).ok, true);
});

test("migrates an old limit plan conservatively to pending", () => {
  const { document, changed } = migrateTradeDocument({ trades: [{ ...base(), status: "open", activatedAt: "2026-07-10T00:00:00Z", events: undefined }] });
  assert.equal(changed, true);
  assert.equal(document.schemaVersion, 2);
  assert.equal(document.trades[0].status, "pending");
  assert.equal(document.trades[0].setupId, "unknown");
  assert.equal(document.trades[0].originalTicket.entry, 100);
  assert.equal(document.trades[0].originalTicket.source, "migration-current-state");
});

test("keeps the activation ticket immutable across manual level changes", () => {
  const t = base({ activatedAt: "2026-07-10T00:00:00Z", setup: "Sweep reversal" });
  t.originalTicket = snapshotTicket(t);
  t.entry = 101; t.sl = 91; t.tp1 = 111; t.rr = 1;
  assert.equal(t.originalTicket.entry, 100);
  assert.equal(t.originalTicket.sl, 90);
  assert.equal(t.originalTicket.tp1, 120);
  assert.equal(t.originalTicket.source, "activation");
});

test("keeps an untouched limit pending", () => {
  const t = base();
  reconcileTrade(t, [bar(1, 110, 115, 105, 111)]);
  assert.equal(t.status, "pending");
  assert.equal(t.filledAt, undefined);
});

test("replays fill, TP1, then breakeven", () => {
  const t = base();
  const r = reconcileTrade(t, [bar(1, 105, 108, 99, 102), bar(2, 102, 121, 101, 119), bar(3, 119, 120, 99, 101)]);
  assert.equal(r.changed, true);
  assert.equal(t.status, "closed");
  assert.equal(t.outcome, "tp1be");
  assert.equal(t.rMultiple, 1);
  assert.ok(t.filledAt && t.tp1HitAt && t.eventClosedAt);
});

test("replays full runner to TP2", () => {
  const t = base();
  reconcileTrade(t, [bar(1, 105, 108, 99, 102), bar(2, 102, 121, 101, 119), bar(3, 119, 141, 118, 139)]);
  assert.equal(t.outcome, "tp2");
  assert.equal(t.rMultiple, 3);
});

test("replays stop loss", () => {
  const t = base();
  reconcileTrade(t, [bar(1, 105, 106, 99, 100), bar(2, 100, 101, 89, 91)]);
  assert.equal(t.outcome, "sl");
  assert.equal(t.rMultiple, -1);
});

test("does not guess a same-bar stop/target conflict", () => {
  const t = base({ priceAtActivation: 100 });
  const rows = [bar(1, 100, 121, 89, 105)]; rows.interval = "1m";
  reconcileTrade(t, rows);
  assert.equal(t.status, "ambiguous");
});

test("forming candle updates FVG lifecycle", () => {
  const closed = [bar(0, 95, 100, 94, 99), bar(1, 100, 111, 99, 110), bar(2, 112, 115, 110, 114)];
  const raw = [...closed, bar(3, 114, 114, 104, 106)];
  const out = findFvgs(closed, raw, 20, 114, 1, 86400, String);
  assert.equal(out.bullish.length, 0, "forming candle touched beyond CE, so zone is no longer a resting-limit anchor");
});

test("order block tracks partial touch without calling it fresh", () => {
  const closed = [bar(0, 100, 105, 95, 96), bar(1, 96, 112, 96, 111), bar(2, 112, 115, 110, 114)];
  const raw = [...closed, bar(3, 114, 114, 103, 110)];
  const out = findOrderBlocks(closed, raw, 20, 112, 1, 86400, String);
  assert.equal(out.bullish.length, 1);
  assert.equal(out.bullish[0].zoneState, "partial");
  assert.ok(out.bullish[0].fillPct > 0);
});

test("liquidity draw never falls back to visited or too-close pools", () => {
  const visited = { label: "visited", dist: 20, touched: true };
  const near = { label: "near", dist: 2, touched: false };
  const forward = { label: "forward", dist: 30, touched: false };
  assert.deepEqual(filterForwardDraws([visited, near], 100), []);
  assert.deepEqual(filterForwardDraws([visited, near, forward], 100), [forward]);
});

test("generic supported crosses resolve dynamically", () => {
  assert.equal(symbolForAsset("NZDCAD"), "NZDCAD=X");
  assert.equal(symbolForAsset("GBPNZD"), "GBPNZD=X");
  assert.equal(symbolForAsset("XAUUSD"), "GC=F");
});
