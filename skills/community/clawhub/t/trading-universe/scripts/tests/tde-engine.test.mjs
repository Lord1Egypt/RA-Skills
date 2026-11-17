import test from "node:test";
import assert from "node:assert/strict";

import {
  adaptDiscoveredTicket,
  buildTicketDiscoveryEngine,
  resolveMarketEntry,
  selectActionableTickets,
} from "../tde-entry-engine.mjs";

const wave = (count, seconds, base) => Array.from({ length: count }, (_, i) => {
  const center = base + Math.sin(i / 4) * 4 + i * 0.02;
  return {
    t: i * seconds,
    o: center - 0.3,
    h: center + 1,
    l: center - 1,
    c: center + 0.3,
    v: 100 + (i % 7) * 10,
  };
});

test("the deterministic engine accepts every asset supported by its caller", () => {
  const data = {
    m15: wave(220, 900, 1.1),
    h1: wave(100, 3600, 1.1),
    d1: wave(80, 86400, 1.1),
  };
  const first = buildTicketDiscoveryEngine("EURUSD", data, 9_999_999_999);
  const second = buildTicketDiscoveryEngine("EURUSD", data, 9_999_999_999);

  assert.equal(first.asset, "EURUSD");
  assert.equal(first.engine, "TU-TDE");
  assert.equal(first.timeframe, "M15");
  assert.deepEqual(first.tickets, second.tickets);
  assert.equal(new Set(first.tickets.map((ticket) => ticket.physicalKey)).size, first.tickets.length);
  for (const ticket of first.tickets) {
    assert.ok(ticket.confluenceFamilies.length >= 2);
    assert.ok(ticket.rr >= 2);
  }
});

test("only unresolved, unfilled orders remain discoverable", () => {
  const common = {
    direction: "LONG",
    entryType: "limit",
    entry: 100,
    sl: 98,
    target: 104,
    rr: 2,
    placedAt: 10_000,
    confluenceFamilies: ["delivery", "liquidity"],
    evidence: {},
  };
  const selected = selectActionableTickets([
    { ...common, id: "resolved", outcome: "target" },
    { ...common, id: "filled", outcome: "open-at-data-end" },
    { ...common, id: "resting", outcome: "pending-at-data-end" },
  ]);

  assert.deepEqual(selected.map((ticket) => ticket.id), ["resting"]);
});

test("latest-close market tickets use the live price when no next open exists", () => {
  const candles = wave(3, 900, 100);

  assert.equal(resolveMarketEntry(candles, 1, 125, 120), candles[2].o);
  assert.equal(resolveMarketEntry(candles, 2, 125, 120), 125);
  assert.equal(resolveMarketEntry(candles, 2, null, 120), 120);
});
test("the adapter preserves the Trading Universe candidate contract", () => {
  const candidate = adaptDiscoveredTicket({
    id: "ticket-1",
    model: "mss-fvg",
    direction: "LONG",
    entryType: "limit",
    entry: 100,
    sl: 98,
    target: 104,
    rr: 2,
    placedAt: 10_000,
    outcome: "pending-at-data-end",
    confluenceFamilies: ["liquidity", "structure", "delivery"],
    evidence: { fvgId: "fvg-1", sweepLevel: 97.5 },
    stopEvidence: {
      anchorType: "originating-sweep",
      structuralAnchor: 97.5,
      invalidationLevel: 97.5,
    },
    targetPool: { id: "pool-1", type: "h4-swing-high", level: 104 },
    tags: ["raid-displacement-retracement"],
  }, { price: 101, atrDaily: 4, round: (value) => value });

  assert.equal(candidate.setup, "MSS + FVG");
  assert.equal(candidate.entry, 100);
  assert.equal(candidate.sl, 98);
  assert.equal(candidate.tp1, 104);
  assert.equal(candidate.tp2, null);
  assert.equal(candidate.rr, 2);
  assert.equal(candidate.validSince, 10_000);
  assert.ok(candidate.whyEntry.includes("FVG"));
  assert.ok(candidate.whySL.includes("98"));
  assert.ok(candidate.entryLabel);
  assert.ok(candidate.tp1Label);
  assert.ok(candidate.stars >= 1 && candidate.stars <= 5);
  assert.match(candidate.whySL, /originating sweep/i);
});
