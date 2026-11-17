import test from "node:test";
import assert from "node:assert/strict";

import {
  buildRegistry,
  detectFvgs,
  detectMssEvents,
  detectMultiScaleSwings,
  qualifyFvgSizes,
} from "../tde-registry.mjs";

const candle = (t, o, h, l, c, v = 0) => ({ t, o, h, l, c, v });

test("FVG geometry, any-touch activation, and inversion lifecycle remain deterministic", () => {
  const candles = [
    candle(0, 100, 101, 99, 100.2), candle(900, 100.5, 104.2, 100.4, 104),
    candle(1800, 103, 105, 102, 104), candle(2700, 104, 105, 103, 104),
    candle(3600, 103, 104, 101.4, 102), candle(4500, 102, 102.5, 100.5, 100.8),
    candle(5400, 100.8, 101.5, 100, 100.7),
  ];
  const bull = detectFvgs(candles).find((zone) => zone.createdAt === 1800 && zone.direction === "bullish");
  assert.ok(bull);
  assert.equal(bull.lower, 101);
  assert.equal(bull.upper, 102);

  const registry = buildRegistry("EURUSD", candles, [], [], 999_999);
  const tracked = registry.zones.find((zone) => zone.id === bull.id);
  assert.equal(tracked.lifecycle.firstTouchCandleNumber, 5);
  assert.equal(tracked.lifecycle.ceReachedAt, 3600);
  assert.equal(tracked.lifecycle.closedThroughAt, 4500);
  assert.equal(tracked.lifecycle.inversionConfirmedAt, 5400);
  assert.equal(tracked.entryActivation.activated, true);
  assert.equal(tracked.entryActivation.ceRequired, false);
});

test("FVG adjacency scales with the selected primary timeframe", () => {
  const hourly = [
    candle(0, 1, 2, 0, 1),
    candle(3600, 2, 5, 2, 5),
    candle(7200, 5, 6, 5, 6),
  ];
  assert.equal(detectFvgs(hourly).length, 0);
  assert.equal(detectFvgs(hourly, 7200).length, 1);

  const broken = [candle(0, 1, 2, 0, 1), candle(900, 2, 4, 2, 4), candle(5000, 5, 6, 5, 6)];
  assert.equal(detectFvgs(broken).length, 0);
});

test("FVG size qualification uses only the causal prior baseline", () => {
  const zones = Array.from({ length: 20 }, (_, i) => ({ id: `base-${i}`, size: 10 }));
  zones.push({ id: "valid", size: 6 });
  zones.push({ id: "invalid", size: 5.8 });
  zones.push({ id: "large", size: 20 });
  zones.push({ id: "after-large", size: 10 });
  qualifyFvgSizes(zones);

  assert.equal(zones[20].sizeQualification.status, "valid-size");
  assert.equal(zones[21].sizeQualification.status, "invalid-size");
  assert.equal(zones[23].sizeQualification.priorBaselineSamples,
    zones[22].sizeQualification.priorBaselineSamples + 1);
});

test("multi-scale swings and MSS lifecycle retain their causal timing", () => {
  const candles = [
    candle(0, 100, 102, 99, 101), candle(900, 101, 103, 100, 102),
    candle(1800, 102, 110, 101, 105), candle(2700, 105, 106, 98, 100),
    candle(3600, 100, 107, 100, 104), candle(4500, 104, 108, 101, 106),
    candle(5400, 106, 111, 104, 106), candle(6300, 108, 109, 96, 97),
    candle(7200, 97, 99, 94, 95), candle(8100, 95, 113, 94, 112),
  ];
  const swingHigh = detectMultiScaleSwings(candles).highs.find((swing) => swing.index === 2);
  assert.equal(swingHigh.strength, 5);
  const bearish = detectMssEvents(candles).find((event) => event.direction === "bearish");
  assert.ok(bearish);
  assert.equal(bearish.liquiditySweptAt, 5400);
  assert.equal(bearish.at, 6300);
  assert.equal(bearish.lifecycle.status, "failed-creation-leg");
  assert.equal(bearish.barsSweepToMss, 1);
  assert.equal(bearish.lifecycle.barsMssToFirstClose, 1);
});
