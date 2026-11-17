import test from "node:test";
import assert from "node:assert/strict";
import { validateFundamentalBoard, validateReviewOutput, validateRevisedTicket } from "../reasoning-validation.mjs";

const grounding = { asset: "EURUSD", price: 1.1000, levels: { entry: 1.1010, sl: 1.0990, tp1: 1.1050, tp2: 1.1080 } };

test("accepts only evidence-traceable revised levels and recomputes RR", () => {
  const t = validateRevisedTicket({ direction: "LONG", entry: 1.1010, sl: 1.0990, tp1: 1.1050, tp2: 1.1080, rr: 99 }, grounding);
  assert.equal(t.rr, 2);
  assert.throws(() => validateRevisedTicket({ direction: "LONG", entry: 1.1011, sl: 1.0990, tp1: 1.1050, tp2: 1.1080 }, grounding), /not traceable/);
});

test("rejects invalid review verdicts and validates MODIFY", () => {
  assert.throws(() => validateReviewOutput({ verdict: "BUY" }, grounding, ["TAKE", "MODIFY"]));
  const out = validateReviewOutput({ verdict: "MODIFY", revisedTicket: { direction: "LONG", entry: 1.1010, sl: 1.0990, tp1: 1.1050, tp2: 1.1080 } }, grounding, ["TAKE", "MODIFY"]);
  assert.equal(out.validatedTicket.rr, 2);
});

test("fundamentals direction and conviction are recomputed from factors", () => {
  const items = validateFundamentalBoard({ items: [{ asset: "EURUSD", direction: "Bearish", score: 5,
    factors: ["+1 ECB hawkish", "+1 growth beat", "-1 USD strong"], reason: "mixed" }] }, ["EURUSD", "GBPUSD"]);
  assert.deepEqual(items[0], { asset: "EURUSD", net: 1, direction: "Bullish", score: 2, reason: "mixed",
    factors: ["+1 ECB hawkish", "+1 growth beat", "-1 USD strong"], flip: "" });
  assert.equal(items[1].direction, "Neutral");
  assert.match(items[1].reason, /insufficient/);
});
