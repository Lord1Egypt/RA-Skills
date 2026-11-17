import { pipSize } from "./symbols.mjs";
import { validateTicket } from "./trade-lifecycle.mjs";

function collectNumbers(value, out = []) {
  if (typeof value === "number" && Number.isFinite(value)) out.push(value);
  else if (Array.isArray(value)) for (const x of value) collectNumbers(x, out);
  else if (value && typeof value === "object") for (const x of Object.values(value)) collectNumbers(x, out);
  return out;
}

export function validateRevisedTicket(ticket, grounding) {
  if (!ticket || typeof ticket !== "object") throw new Error("revised ticket missing");
  const t = { direction: String(ticket.direction || "").toUpperCase(), entry: Number(ticket.entry), sl: Number(ticket.sl),
    tp1: Number(ticket.tp1), tp2: ticket.tp2 == null ? null : Number(ticket.tp2) };
  const shape = validateTicket(t, { skipRR: true });
  if (!shape.ok) throw new Error("revised ticket invalid: " + shape.errors.join("; "));
  const evidence = collectNumbers(grounding);
  const tol = pipSize(grounding.asset) * 0.51;
  for (const key of ["entry", "sl", "tp1", "tp2"]) {
    if (t[key] == null) continue;
    if (!evidence.some((n) => Math.abs(n - t[key]) <= tol)) throw new Error(`revised ${key} ${t[key]} is not traceable to supplied evidence`);
  }
  const quality = validateTicket(t);
  if (!quality.ok) throw new Error("revised ticket invalid: " + quality.errors.join("; "));
  const risk = Math.abs(t.entry - t.sl);
  t.rr = Number(((t.direction === "LONG" ? t.tp1 - t.entry : t.entry - t.tp1) / risk).toFixed(2));
  return t;
}

export function validateReviewOutput(out, grounding, allowed) {
  if (!out || !allowed.includes(out.verdict)) throw new Error("review returned an invalid verdict");
  if (["MODIFY", "REPLACE"].includes(out.verdict)) {
    const field = out.verdict === "REPLACE" ? (out.advisorTicket || out.recommendedTicket || out.revisedTicket)
      : (out.recommendedTicket || out.revisedTicket);
    out.validatedTicket = validateRevisedTicket(field, grounding);
  } else out.validatedTicket = null;
  return out;
}

function factorNet(factors) {
  let net = 0;
  for (const f of factors || []) {
    const m = String(f).trim().match(/^([+-]?1|0)\b/);
    if (m) net += Number(m[1]);
  }
  return net;
}
const scoreFromNet = (net) => Math.abs(net) >= 4 ? 5 : Math.abs(net) === 3 ? 4 : Math.abs(net) === 2 ? 3 : Math.abs(net) === 1 ? 2 : 1;

export function validateFundamentalBoard(out, assets) {
  const byAsset = new Map((Array.isArray(out?.items) ? out.items : []).map((x) => [String(x?.asset || "").toUpperCase(), x]));
  return assets.map((asset) => {
    const x = byAsset.get(asset);
    if (!x) return { asset, direction: "Neutral", score: 1, net: 0, reason: "insufficient fresh evidence", factors: [], flip: "" };
    const factors = (Array.isArray(x.factors) ? x.factors : []).map((f) => String(f).slice(0, 200)).slice(0, 8);
    const net = factorNet(factors);
    return {
      asset, net, direction: net > 0 ? "Bullish" : net < 0 ? "Bearish" : "Neutral", score: scoreFromNet(net),
      reason: String(x.reason || "").slice(0, 300), factors, flip: String(x.flip || "").slice(0, 200),
    };
  });
}
