import test from "node:test";
import assert from "node:assert/strict";

import { adaptDiscoveredTicket } from "../tde-entry-engine.mjs";

test("normal candidates expose concise chart evidence, not the internal evidence graph", () => {
  const candidate = adaptDiscoveredTicket({
    id: "order-block|internal-source",
    model: "order-block",
    direction: "LONG",
    entryType: "limit",
    entry: 100,
    sl: 98,
    target: 104,
    rr: 2,
    placedAt: 10_000,
    outcome: "pending-at-data-end",
    confluenceFamilies: ["delivery", "structure", "location", "liquidity"],
    evidence: {
      ob: { id: "ob|opaque|334", lower: 99.5, upper: 100.5 },
      liquidityPathSnapshot: { destinationCandidates: [{ poolId: "opaque-pool" }] },
    },
    targetPool: { id: "h4-swing-low|opaque", type: "h4-swing-low", level: 104 },
    tags: [],
  }, { price: 101, atrDaily: 4, round: (value) => value });

  assert.equal("evidence" in candidate, false);
  assert.equal(candidate.tp1Label, "H4 swing low");
  assert.doesNotMatch(candidate.whyEntry, /opaque|internal-source/);
  assert.match(candidate.whyEntry, /99\.5-100\.5/);
});
