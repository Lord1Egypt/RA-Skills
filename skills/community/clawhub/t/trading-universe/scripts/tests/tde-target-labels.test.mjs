import test from "node:test";
import assert from "node:assert/strict";

import { adaptDiscoveredTicket } from "../tde-entry-engine.mjs";

const base = {
  id: "ote|signal",
  model: "ote",
  entryType: "limit",
  entry: 100,
  sl: 98,
  target: 104,
  rr: 2,
  placedAt: 10_000,
  outcome: "pending-at-data-end",
  confluenceFamilies: ["liquidity", "structure", "location"],
  evidence: { creationLeg: [98, 102] },
  tags: [],
};

test("swing targets name their structural side without exposing an opaque ID", () => {
  const long = adaptDiscoveredTicket({
    ...base,
    direction: "LONG",
    targetPool: { id: "swing|high|opaque", kind: "external-swing", level: 104 },
  });
  const short = adaptDiscoveredTicket({
    ...base,
    direction: "SHORT",
    entry: 100,
    sl: 102,
    target: 96,
    targetPool: { id: "swing|low|opaque", kind: "internal-swing", level: 96 },
  });

  assert.equal(long.tp1Label, "external swing high");
  assert.equal(short.tp1Label, "internal swing low");
  assert.doesNotMatch(long.whyEntry + short.whyEntry, /opaque/);
});
