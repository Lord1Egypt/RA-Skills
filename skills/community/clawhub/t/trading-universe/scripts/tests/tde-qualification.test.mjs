import test from "node:test";
import assert from "node:assert/strict";

import {
  isZoneOpenAt,
  isMeaningfulLiquidityRaid,
  isModelEnabledForTimeframe,
  qualifiesMomentumContinuation,
  qualifiesMssDisplacement,
  selectOteOverlap,
} from "../tde-entry-engine.mjs";

const strongMss = (overrides = {}) => ({
  direction: "bullish",
  index: 10,
  barsSweepToMss: 2,
  sweepExtreme: 90,
  mssExtreme: 110,
  candleExpansion: { directional: true, bodyRangePct: 65, bodyMultiple: 1.4 },
  ...overrides,
});

test("MSS qualification requires directional displacement and prompt structure shift", () => {
  assert.equal(qualifiesMssDisplacement(strongMss()), true);
  assert.equal(qualifiesMssDisplacement(strongMss({
    candleExpansion: { directional: true, bodyRangePct: 30, bodyMultiple: 1.4 },
  })), false);
  assert.equal(qualifiesMssDisplacement(strongMss({
    candleExpansion: { directional: true, bodyRangePct: 65, bodyMultiple: 0.5 },
  })), false);
  assert.equal(qualifiesMssDisplacement(strongMss({ barsSweepToMss: 5 })), false);
});

test("OTE entry is the midpoint of overlap with a valid same-leg FVG", () => {
  const out = selectOteOverlap(strongMss(), [{
    id: "fvg-valid",
    direction: "bullish",
    createdIndex: 11,
    lower: 95,
    upper: 96,
    sizeQualification: { status: "valid-size" },
  }], []);

  assert.ok(out);
  assert.equal(out.featureType, "fvg");
  assert.deepEqual(out.oteBand, [94.2, 97.6]);
  assert.deepEqual(out.overlap, [95, 96]);
  assert.equal(out.entry, 95.5);
  assert.equal(out.retracementPct, 0.725);
});

test("OTE prefers an overlapping causal order block over a generic FVG", () => {
  const event = strongMss();
  const out = selectOteOverlap(event, [{
    id: "fvg-valid",
    direction: "bullish",
    createdIndex: 11,
    lower: 95,
    upper: 96,
    sizeQualification: { status: "valid-size" },
  }], [{
    id: "ob-valid",
    direction: "bullish",
    createdIndex: 11,
    lower: 94.5,
    upper: 95.5,
  }]);

  assert.ok(out);
  assert.equal(out.featureType, "order-block");
  assert.equal(out.featureId, "ob-valid");
  assert.equal(out.entry, 95);
});

test("OTE fails closed without valid same-leg feature overlap", () => {
  assert.equal(selectOteOverlap(strongMss(), [{
    id: "wrong-direction",
    direction: "bearish",
    createdIndex: 11,
    lower: 95,
    upper: 96,
    sizeQualification: { status: "valid-size" },
  }, {
    id: "invalid-size",
    direction: "bullish",
    createdIndex: 11,
    lower: 95,
    upper: 96,
    sizeQualification: { status: "invalid-size" },
  }], []), null);
});

test("FVG must still be open on the signal candle", () => {
  assert.equal(isZoneOpenAt({ lifecycle: { closedThroughIndex: null } }, 12), true);
  assert.equal(isZoneOpenAt({ lifecycle: { closedThroughIndex: 13 } }, 12), true);
  assert.equal(isZoneOpenAt({ lifecycle: { closedThroughIndex: 12 } }, 12), false);
  assert.equal(isZoneOpenAt({ lifecycle: { closedThroughIndex: 11 } }, 12), false);
});

test("momentum continuation requires both HTF alignment and displacement", () => {
  assert.equal(qualifiesMomentumContinuation({
    htfAligned: true,
    displacement: { valid: true },
  }), true);
  assert.equal(qualifiesMomentumContinuation({
    htfAligned: true,
    displacement: { valid: false },
  }), false);
  assert.equal(qualifiesMomentumContinuation({
    htfAligned: false,
    displacement: { valid: true },
  }), false);
});

test("Turtle Soup only treats equal or external liquidity as a meaningful raid", () => {
  assert.equal(isMeaningfulLiquidityRaid({ poolKind: "equal-highs" }), true);
  assert.equal(isMeaningfulLiquidityRaid({ poolKind: "equal-lows" }), true);
  assert.equal(isMeaningfulLiquidityRaid({ poolKind: "external-swing" }), true);
  assert.equal(isMeaningfulLiquidityRaid({ poolKind: "internal-swing" }), false);
});

test("model eligibility is fail-closed by timeframe and retained evidence", () => {
  assert.equal(isModelEnabledForTimeframe("fvg-mitigation", "M15"), true);
  assert.equal(isModelEnabledForTimeframe("order-block", "H1"), true);
  assert.equal(isModelEnabledForTimeframe("ote", "M15"), true);
  assert.equal(isModelEnabledForTimeframe("ote", "H1"), false);
  assert.equal(isModelEnabledForTimeframe("momentum-bos", "M15"), false);
  assert.equal(isModelEnabledForTimeframe("volume-continuation", "M15"), false);
  assert.equal(isModelEnabledForTimeframe("choch-continuation", "M15"), false);
  assert.equal(isModelEnabledForTimeframe("unknown-model", "M15"), false);
});
