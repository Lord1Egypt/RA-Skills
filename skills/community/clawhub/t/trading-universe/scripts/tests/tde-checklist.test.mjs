import test from "node:test";
import assert from "node:assert/strict";

import { buildEntryChecklist } from "../tde-entry-engine.mjs";

const baseTicket = {
  model: "fvg-mitigation",
  direction: "LONG",
  htf: { h1: "bullish", h4: "range", daily: "unknown" },
  evidence: { zoneId: "fvg-1", bounds: [99.5, 100] },
  targetPool: { id: "buy-side-1", level: 104, kind: "external-swing" },
  stopEvidence: {
    anchorType: "fvg-invalidation-boundary",
    structuralAnchor: 99.5,
    invalidationLevel: 99.5,
  },
};

test("entry checklist requires HTF alignment, mapped POI, objective, and protected level", () => {
  const checklist = buildEntryChecklist(baseTicket);

  assert.equal(checklist.passed, true);
  assert.equal(checklist.items.htfTrendAlignment.passed, true);
  assert.deepEqual(checklist.items.htfTrendAlignment.alignedTimeframes, ["h1"]);
  assert.equal(checklist.items.pointsOfInterest.passed, true);
  assert.equal(checklist.items.liquidityObjective.level, 104);
  assert.equal(checklist.items.protectedLevel.level, 99.5);
  assert.equal(checklist.items.protectedLevel.type, "fvg-invalidation-boundary");
  assert.equal(checklist.items.oteConfluence.applicable, false);
  assert.equal(checklist.items.oteConfluence.passed, null);
});

test("OTE requires a valid OTE band overlap and mapped entry confluence", () => {
  const missingOverlap = buildEntryChecklist({ ...baseTicket, model: "ote" });
  assert.equal(missingOverlap.items.oteConfluence.applicable, true);
  assert.equal(missingOverlap.items.oteConfluence.passed, false);
  assert.equal(missingOverlap.passed, false);

  const qualified = buildEntryChecklist({
    ...baseTicket,
    model: "ote",
    evidence: {
      creationLeg: [98, 104],
      retracementPct: 0.705,
      oteBand: [99.26, 100.28],
      overlap: [99.5, 100],
      overlapFeatureType: "order-block",
      overlapFeatureId: "ob-1",
    },
  });
  assert.equal(qualified.items.oteConfluence.passed, true);
  assert.equal(qualified.passed, true);
});

test("checklist fails closed when HTF, objective, POI, or invalidation evidence is missing", () => {
  assert.equal(buildEntryChecklist({ ...baseTicket, htf: { h1: "bearish" } }).passed, false);
  assert.equal(buildEntryChecklist({ ...baseTicket, evidence: {} }).passed, false);
  assert.equal(buildEntryChecklist({ ...baseTicket, targetPool: null }).passed, false);
  assert.equal(buildEntryChecklist({ ...baseTicket, stopEvidence: null }).passed, false);
});

test("a confirmed primary structure direction can qualify a transparently counter-HTF setup", () => {
  const checklist = buildEntryChecklist({
    ...baseTicket,
    htf: { h1: "bearish", h4: "range", daily: "unknown" },
    primaryBias: "bullish",
  });

  assert.equal(checklist.items.htfTrendAlignment.passed, false);
  assert.equal(checklist.items.htfTrendAlignment.accepted, true);
  assert.equal(checklist.items.htfTrendAlignment.acceptanceBasis, "primary-structure");
  assert.equal(checklist.passed, true);
});
