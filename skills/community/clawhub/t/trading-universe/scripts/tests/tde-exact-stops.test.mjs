import test from "node:test";
import assert from "node:assert/strict";

import { deriveModelStop, deriveStructuralStop } from "../tde-risk.mjs";

test("structural stop equals the selected invalidation level and exposes no ATR policy", () => {
  const out = deriveStructuralStop({
    direction: "LONG",
    entry: 100,
    anchors: [
      { type: "fvg-invalidation-boundary", price: 99.4 },
      { type: "originating-sweep", price: 98.8 },
    ],
  });

  assert.deepEqual(out, {
    price: 98.8,
    invalidationLevel: 98.8,
    structuralAnchor: 98.8,
    anchorType: "originating-sweep",
    risk: 1.2,
  });
  assert.equal("riskAtr" in out, false);
  assert.equal("floorApplied" in out, false);
  assert.equal("buffer" in out, false);
});

test("limit FVG entries invalidate at the far gap boundary", () => {
  const out = deriveModelStop({
    model: "fvg-mitigation",
    direction: "LONG",
    entry: 101,
    candles: [
      { l: 98.4, h: 100.5 },
      { l: 99.1, h: 102.2 },
      { l: 100.8, h: 103.1 },
    ],
    zone: { createdIndex: 2, lower: 100.5, upper: 100.8 },
  });

  assert.equal(out.anchorType, "fvg-invalidation-boundary");
  assert.equal(out.price, 100.5);
});

test("market FVG entries invalidate at the traded zone's far boundary", () => {
  const out = deriveModelStop({
    model: "fvg-fourth-candle-confirmed",
    direction: "LONG",
    entry: 101,
    candles: [
      { l: 98.4, h: 100.5 },
      { l: 99.1, h: 102.2 },
      { l: 100.8, h: 103.1 },
    ],
    zone: { createdIndex: 2, lower: 100.5, upper: 100.8 },
  });

  assert.equal(out.anchorType, "fvg-invalidation-boundary");
  assert.equal(out.price, 100.5);
});

test("order-block, sweep, and continuation entries use their exact invalidation", () => {
  assert.equal(deriveModelStop({
    model: "order-block",
    direction: "LONG",
    entry: 101,
    orderBlock: { lower: 99, upper: 102 },
  }).price, 99);

  assert.equal(deriveModelStop({
    model: "ote",
    direction: "SHORT",
    entry: 100,
    event: { sweepExtreme: 101.3 },
  }).price, 101.3);

  assert.equal(deriveModelStop({
    model: "momentum-bos",
    direction: "LONG",
    entry: 100,
    opposingSwing: { level: 98.7 },
  }).price, 98.7);
});

test("invalid structural inputs fail closed", () => {
  assert.throws(() => deriveStructuralStop({
    direction: "LONG",
    entry: 100,
    anchors: [],
  }), /anchor/i);
  assert.throws(() => deriveStructuralStop({
    direction: "SIDEWAYS",
    entry: 100,
    anchors: [{ type: "swing", price: 99 }],
  }), /direction/i);
  assert.throws(() => deriveStructuralStop({
    direction: "LONG",
    entry: 100,
    anchors: [{ type: "wrong-side", price: 101 }],
  }), /below entry/i);
});
