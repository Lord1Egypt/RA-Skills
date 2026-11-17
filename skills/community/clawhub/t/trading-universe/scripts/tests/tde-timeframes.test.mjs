import test from "node:test";
import assert from "node:assert/strict";

import { buildTicketDiscoveryEngine } from "../tde-entry-engine.mjs";

const wave = (count, seconds, base) => Array.from({ length: count }, (_, i) => {
  const center = base + Math.sin(i / 4) * 40 + i * 0.2;
  return {
    t: i * seconds,
    o: center - 3,
    h: center + 10,
    l: center - 10,
    c: center + 3,
    v: 100 + (i % 7) * 10,
  };
});

test("H1 discovery uses H1 as primary without inventing an M15 bias", () => {
  const out = buildTicketDiscoveryEngine("NAS100", {
    m15: wave(220, 900, 20_000),
    h1: wave(220, 3600, 20_000),
    d1: wave(80, 86_400, 20_000),
  }, 9_999_999_999, { timeframe: "H1" });

  assert.equal(out.asset, "NAS100");
  assert.equal(out.timeframe, "H1");
  assert.equal(out.primarySeconds, 3600);
  assert.ok(out.tickets.every((ticket) => ticket.timeframe === "H1"));
  assert.ok(out.tickets.every((ticket) => ticket.m15Bias == null));
});

test("unsupported primary timeframes fail closed", () => {
  assert.throws(() => buildTicketDiscoveryEngine("EURUSD", {
    m15: [], h1: [], d1: [],
  }, 9_999_999_999, { timeframe: "M5" }), /timeframe must be M15 or H1/);
});
