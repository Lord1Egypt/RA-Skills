import test from "node:test";
import assert from "node:assert/strict";

import { DEFAULT_RISK_POLICY, simulateTicket } from "../tde-lifecycle.mjs";

const candle = (t, o, h, l, c) => ({ t, o, h, l, c });
const limitLong = (overrides = {}) => ({
  id: "limit-long",
  direction: "LONG",
  entryType: "limit",
  entry: 100,
  sl: 98,
  target: 104,
  placedIndex: 0,
  ...overrides,
});
test("validated risk policy protects at half an R from the following candle", () => {
  assert.equal(DEFAULT_RISK_POLICY.moveStopToBreakevenAtR, 0.5);
  assert.equal(DEFAULT_RISK_POLICY.breakevenEffective, "next-candle");
});


test("an untouched limit remains pending at the data boundary", () => {
  const out = simulateTicket(limitLong(), [
    candle(0, 103, 104, 102, 103),
    candle(900, 102, 103, 101, 102),
  ]);
  assert.equal(out.outcome, "pending-at-data-end");
  assert.equal(out.filledAt, null);
});

test("a limit invalidated before touch is not resurfaced as pending", () => {
  const out = simulateTicket(limitLong(), [
    candle(0, 103, 104, 102, 103),
    candle(900, 99, 99.5, 97.5, 98),
  ]);
  assert.equal(out.outcome, "invalidated-before-fill");
  assert.equal(out.filledAt, null);
});

test("a latest-close market signal remains a current pending execution", () => {
  const out = simulateTicket(limitLong({
    id: "market-long",
    entryType: "market",
    entry: 101,
  }), [candle(0, 101, 102, 100, 101)]);
  assert.equal(out.outcome, "pending-at-data-end");
  assert.equal(out.entry, 101);
});

test("breakeven becomes effective on the candle after the trigger", () => {
  const out = simulateTicket(limitLong(), [
    candle(0, 103, 104, 102, 103),
    candle(900, 101, 101, 99.5, 100.5),
    candle(1800, 100.5, 102.2, 100.2, 102),
    candle(2700, 102, 102.1, 99.5, 100),
  ]);
  assert.equal(out.outcome, "breakeven");
  assert.equal(out.breakevenTriggeredAt, 900);
  assert.equal(out.breakevenEffectiveAt, 1800);
  assert.equal(out.rMultiple, 0);
});

test("same-candle stop and target remains explicitly ambiguous", () => {
  const out = simulateTicket(limitLong(), [
    candle(0, 103, 104, 102, 103),
    candle(900, 101, 104.5, 97.5, 101),
  ]);
  assert.equal(out.outcome, "ambiguous");
  assert.equal(out.rMultiple, null);
});
