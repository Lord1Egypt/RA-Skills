import test from "node:test";
import assert from "node:assert/strict";

import {
  scoreTicketQuality,
  selectActionableTickets,
} from "../tde-entry-engine.mjs";

const pending = (id, overrides = {}) => ({
  id,
  model: "mss-fvg",
  direction: "LONG",
  timeframe: "M15",
  entryType: "limit",
  entry: 100,
  sl: 98,
  target: 104,
  rr: 2,
  placedAt: 10_000,
  barsSincePlacement: 1,
  outcome: "pending-at-data-end",
  confluenceFamilies: ["liquidity", "structure"],
  evidence: {},
  tags: [],
  ...overrides,
});

const structurallyComplete = (id = "strong", overrides = {}) => pending(id, {
  evidence: {
    sweepLevel: 97.5,
    mssAt: 9_000,
    fvgId: "fvg-1",
    displacement: { valid: true },
    htfAligned: ["h1", "h4"],
    location: "discount",
    selectedLiquidityTarget: { id: "pool-1" },
  },
  targetPool: { kind: "htf-liquidity", type: "h4-swing-high", level: 104 },
  stopEvidence: { anchorType: "originating-sweep", structuralAnchor: 97.5, invalidationLevel: 97.5 },
  killzone: "new-york-am",
  rangeLocation: "discount",
  tags: ["fresh", "raid-displacement-retracement"],
  ...overrides,
});

test("complete structural sequence outranks a larger raw confluence list", () => {
  const strong = scoreTicketQuality(structurallyComplete());
  const shallow = scoreTicketQuality(pending("shallow", {
    confluenceFamilies: ["a", "b", "c", "d", "e", "f"],
    rr: 5,
  }));

  assert.ok(strong.score > shallow.score);
  assert.equal(Object.hasOwn(strong.components, "confluenceCount"), false);
  assert.equal(Object.hasOwn(strong.components, "rr"), false);
});

test("model aliases cannot inflate ticket quality", () => {
  const base = structurallyComplete();
  const withoutAliases = scoreTicketQuality(base);
  const withAliases = scoreTicketQuality({
    ...base,
    modelAliases: ["mss-fvg", "ict-2022", "ote", "premium-discount"],
  });

  assert.deepEqual(withAliases, withoutAliases);
});

test("actionable tickets rank by structural quality before recency or RR", () => {
  const selected = selectActionableTickets([
    pending("recent-shallow", { placedAt: 20_000, rr: 6 }),
    structurallyComplete("older-strong", { placedAt: 10_000, rr: 2 }),
  ]);

  assert.deepEqual(selected.map((ticket) => ticket.id), ["older-strong", "recent-shallow"]);
});

test("equal-quality actionable tickets keep deterministic tie breakers", () => {
  const selected = selectActionableTickets([
    pending("far", { placedAt: 10_000, entry: 110 }),
    pending("near", { placedAt: 10_000, entry: 101 }),
    pending("newest", { placedAt: 20_000, entry: 115 }),
  ], { price: 100 });

  assert.deepEqual(selected.map((ticket) => ticket.id), ["newest", "near", "far"]);
});
