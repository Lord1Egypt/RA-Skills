import test from "node:test";
import assert from "node:assert/strict";

import { selectActionableTickets } from "../tde-entry-engine.mjs";

const pending = (id, timeframe, barsSincePlacement) => ({
  id,
  timeframe,
  barsSincePlacement,
  outcome: "pending-at-data-end",
  entry: 100,
  rr: 2,
  placedAt: 10_000,
  confluenceFamilies: ["delivery", "liquidity"],
});

test("pending discovery expires by observed market bars, not wall-clock weekends", () => {
  const selected = selectActionableTickets([
    pending("m15-live", "M15", 144),
    pending("m15-stale", "M15", 145),
    pending("h1-live", "H1", 36),
    pending("h1-stale", "H1", 37),
  ]);

  assert.deepEqual(new Set(selected.map((ticket) => ticket.id)), new Set(["m15-live", "h1-live"]));
});
