import test from "node:test";
import assert from "node:assert/strict";

import { setupId, validateTicket } from "../trade-lifecycle.mjs";

const ticket = (tp1) => ({ direction: "LONG", entry: 100, sl: 99, tp1, tp2: null });

test("fresh ledger entries use the TU-TDE quality threshold", () => {
  assert.equal(validateTicket(ticket(101.9)).ok, false);
  assert.equal(validateTicket(ticket(102)).ok, true);
});

test("all TU-TDE model labels receive stable setup identifiers", () => {
  const labels = [
    "FVG mitigation",
    "Premium/discount reversal",
    "Trend continuation",
    "Order block",
    "MSS + FVG",
    "ICT 2022 model",
    "OTE retracement",
    "CHOCH continuation",
    "Confirmed Turtle Soup",
    "Momentum BOS",
    "Relative-volume continuation",
    "Fourth-candle FVG confirmation",
    "In-gap bounce",
  ];
  for (const label of labels) assert.notEqual(setupId(label), "unknown", label);
});
