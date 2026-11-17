const finite = (value) => typeof value === "number" && Number.isFinite(value);
const clean = (value) => Number(value.toFixed(12));

export function deriveStructuralStop({ direction, entry, anchors }) {
  if (!["LONG", "SHORT"].includes(direction))
    throw new Error("direction must be LONG or SHORT");
  if (!finite(entry)) throw new Error("entry must be finite");
  if (!Array.isArray(anchors) || anchors.length === 0)
    throw new Error("at least one structural anchor is required");

  for (const anchor of anchors) {
    if (!anchor || typeof anchor.type !== "string" || !anchor.type.trim() || !finite(anchor.price))
      throw new Error("each structural anchor requires a type and finite price");
    if (direction === "LONG" && anchor.price >= entry)
      throw new Error("LONG structural anchors must be below entry");
    if (direction === "SHORT" && anchor.price <= entry)
      throw new Error("SHORT structural anchors must be above entry");
  }

  const selected = anchors.reduce((best, anchor) => {
    if (!best) return anchor;
    if (direction === "LONG") return anchor.price < best.price ? anchor : best;
    return anchor.price > best.price ? anchor : best;
  }, null);
  const invalidationLevel = clean(selected.price);

  return {
    price: invalidationLevel,
    invalidationLevel,
    structuralAnchor: invalidationLevel,
    anchorType: selected.type,
    risk: clean(Math.abs(entry - invalidationLevel)),
  };
}

const FVG_MODELS = new Set([
  "fvg-mitigation",
  "premium-discount",
  "trend-continuation",
  "fvg-fourth-candle-confirmed",
  "in-gap-bounce",
]);
const SWEEP_MODELS = new Set([
  "mss-fvg",
  "ict-2022",
  "ote",
  "choch-continuation",
  "turtle-soup-confirmed",
]);
const CONTINUATION_MODELS = new Set(["momentum-bos", "volume-continuation"]);

const fvgBoundaryAnchor = (direction, zone) => {
  const boundary = direction === "LONG" ? zone?.lower : zone?.upper;
  if (!finite(boundary)) throw new Error("FVG stop requires its far invalidation boundary");
  return { type: "fvg-invalidation-boundary", price: boundary };
};


export function deriveModelStop({
  model,
  direction,
  entry,
  zone,
  orderBlock,
  event,
  sweep,
  opposingSwing,
}) {
  const anchors = [];
  if (FVG_MODELS.has(model)) {
    anchors.push(fvgBoundaryAnchor(direction, zone));
  } else if (model === "order-block") {
    const obPrice = direction === "LONG" ? orderBlock?.lower : orderBlock?.upper;
    if (!finite(obPrice))
      throw new Error("order-block stop requires the full order-block extreme");
    anchors.push({ type: "order-block-extreme", price: obPrice });
  } else if (SWEEP_MODELS.has(model)) {
    const sweepPrice = event?.sweepExtreme ?? sweep?.extreme;
    if (!finite(sweepPrice))
      throw new Error(`${model} stop requires its originating sweep`);
    anchors.push({ type: "originating-sweep", price: sweepPrice });
  } else if (CONTINUATION_MODELS.has(model)) {
    if (!finite(opposingSwing?.level))
      throw new Error(`${model} stop requires a confirmed opposing swing`);
    anchors.push({ type: "confirmed-opposing-swing", price: opposingSwing.level });
  } else {
    throw new Error(`unsupported model stop policy: ${model}`);
  }

  return deriveStructuralStop({ direction, entry, anchors });
}
