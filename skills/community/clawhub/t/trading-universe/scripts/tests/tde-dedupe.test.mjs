import test from "node:test";
import assert from "node:assert/strict";

import { dedupePhysicalTickets } from "../tde-entry-engine.mjs";

test("physical-order dedupe retains all independent qualification evidence", () => {
  const common = {
    direction: "LONG",
    entryType: "limit",
    placedIndex: 10,
    actualEntry: 100,
    entry: 100,
    sl: 98,
    target: 104,
    rr: 2,
  };
  const rows = dedupePhysicalTickets([
    { ...common, model: "fvg-mitigation", confluenceFamilies: ["delivery", "structure"], tags: ["any-touch"] },
    { ...common, model: "premium-discount", confluenceFamilies: ["delivery", "structure", "location"], tags: ["discount"] },
  ]);

  assert.equal(rows.length, 1);
  assert.deepEqual(rows[0].modelAliases, ["fvg-mitigation", "premium-discount"]);
  assert.deepEqual(new Set(rows[0].confluenceFamilies), new Set(["delivery", "structure", "location"]));
  assert.deepEqual(new Set(rows[0].tags), new Set(["any-touch", "discount"]));
});
