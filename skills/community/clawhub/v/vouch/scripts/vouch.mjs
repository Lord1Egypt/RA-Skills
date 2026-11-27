#!/usr/bin/env node
// vouch.mjs: spend ledger, tolerance judge and report renderer for the Vouch skill.
// Dependency-free (Node 18+). It never talks to the network and never touches keys:
// Telegraph calls are made by the agent through the telegraph MCP server.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const LEDGER = process.env.VOUCH_LEDGER || path.join(os.homedir(), ".vouch", "ledger.json");
const DEFAULT_CLAIM_CAP = 0.05;
const DEFAULT_TASK_CAP = 0.25;
const VERDICTS = ["verified", "contradicted", "cannot_verify"];

function args(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1] !== undefined && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
      out[k] = v;
    } else out._.push(a);
  }
  return out;
}
const usd = (n) => "$" + (Math.round(n * 1e6) / 1e6).toFixed(2 + (Math.abs(n * 100 - Math.round(n * 100)) > 1e-9 ? 2 : 0));
const round6 = (n) => Math.round(n * 1e6) / 1e6;
function load() {
  try { return JSON.parse(fs.readFileSync(LEDGER, "utf8")); }
  catch { die("No ledger. Run: node vouch.mjs init [--task-cap 0.25] [--claim-cap 0.05]"); }
}
function save(l) {
  fs.mkdirSync(path.dirname(LEDGER), { recursive: true });
  fs.writeFileSync(LEDGER, JSON.stringify(l, null, 2));
}
function die(msg, code = 2) { console.error(msg); process.exit(code); }
const num = (v, name) => { const n = Number(v); if (!Number.isFinite(n) || n < 0) die(`--${name} must be a non-negative number`); return n; };
const spent = (l) => round6(l.entries.reduce((s, e) => s + e.cost_usd, 0));
const spentOn = (l, claim) => round6(l.entries.filter((e) => e.claim_id === claim).reduce((s, e) => s + e.cost_usd, 0));

const [cmd, ...rest] = process.argv.slice(2);
const a = args(rest);

if (cmd === "init") {
  const l = {
    task: a.task || "unnamed task",
    created: new Date().toISOString(),
    claim_cap_usd: a["claim-cap"] ? num(a["claim-cap"], "claim-cap") : DEFAULT_CLAIM_CAP,
    task_cap_usd: a["task-cap"] ? num(a["task-cap"], "task-cap") : DEFAULT_TASK_CAP,
    claims: {},
    entries: [],
  };
  save(l);
  console.log(`ledger ${LEDGER}: claim cap ${usd(l.claim_cap_usd)}, task cap ${usd(l.task_cap_usd)}`);

} else if (cmd === "claim") {
  // claim --id c1 --text "..." [--tolerance "..."]
  const l = load();
  if (!a.id || !a.text) die("usage: claim --id c1 --text \"...\" [--tolerance \"...\"]");
  l.claims[a.id] = { text: a.text, tolerance: a.tolerance || "exact", verdict: null };
  save(l);
  console.log(`claim ${a.id} registered`);

} else if (cmd === "check") {
  // check --claim c1 --est 0.01 : exit 0 = allowed, 3 = refused
  const l = load();
  const est = num(a.est ?? "0.01", "est");
  const claim = a.claim || "?";
  const onClaim = spentOn(l, claim), total = spent(l);
  const why = [];
  if (onClaim + est > l.claim_cap_usd + 1e-9) why.push(`claim cap ${usd(l.claim_cap_usd)} (already ${usd(onClaim)} on ${claim})`);
  if (total + est > l.task_cap_usd + 1e-9) why.push(`task cap ${usd(l.task_cap_usd)} (already ${usd(total)})`);
  if (why.length) { console.log(`REFUSED: would exceed ${why.join("; ")}`); process.exit(3); }
  console.log(`OK: ${usd(est)} fits; claim ${usd(onClaim)}/${usd(l.claim_cap_usd)}, task ${usd(total)}/${usd(l.task_cap_usd)}`);

} else if (cmd === "record") {
  // record --claim c1 --intent X --miner M --cost 0.01 --receipt 0x.. [--note ..]   (cost 0 for failed asks)
  const l = load();
  if (!a.claim) die("record needs --claim");
  l.entries.push({
    at: new Date().toISOString(), claim_id: a.claim, intent: a.intent || "", miner: a.miner || "",
    cost_usd: num(a.cost ?? "0", "cost"), receipt: a.receipt || "", note: a.note || "",
  });
  save(l);
  console.log(`recorded; running total ${usd(spent(l))} of ${usd(l.task_cap_usd)}`);

} else if (cmd === "verdict") {
  // verdict --claim c1 --verdict verified|contradicted|cannot_verify --observed "..." --why "..."
  const l = load();
  if (!l.claims[a.claim]) die(`unknown claim ${a.claim}; register it with: claim --id`);
  if (!VERDICTS.includes(a.verdict)) die(`--verdict must be one of ${VERDICTS.join(", ")}`);
  if (a.verdict !== "cannot_verify" && !l.entries.some((e) => e.claim_id === a.claim && e.receipt))
    die(`refused: ${a.verdict} needs at least one recorded Telegraph receipt for ${a.claim}. A claim with no answer is cannot_verify.`, 4);
  Object.assign(l.claims[a.claim], { verdict: a.verdict, observed: a.observed || "", why: a.why || "" });
  save(l);
  console.log(`${a.claim}: ${a.verdict}`);

} else if (cmd === "judge") {
  // judge --claimed 5 --observed 0.0449 --tol "abs:0.5" | "pct:5" | "exact"   (numbers or strings)
  const tol = a.tol || "exact";
  const c = a.claimed, o = a.observed;
  if (c === undefined || o === undefined) die("usage: judge --claimed X --observed Y [--tol exact|abs:N|pct:N|lt|gt|le|ge]");
  const cn = Number(c), on = Number(o);
  let ok;
  if (tol === "exact") ok = Number.isFinite(cn) && Number.isFinite(on) ? cn === on : String(c).trim().toLowerCase() === String(o).trim().toLowerCase();
  else if (!Number.isFinite(cn) || !Number.isFinite(on)) die("numeric tolerance needs numeric --claimed and --observed");
  else if (tol.startsWith("abs:")) ok = Math.abs(cn - on) <= Number(tol.slice(4));
  else if (tol.startsWith("pct:")) ok = Math.abs(cn - on) <= Math.abs(cn) * Number(tol.slice(4)) / 100;
  else if (tol === "lt") ok = on < cn; // claim "value is below C": observed must be < C
  else if (tol === "le") ok = on <= cn;
  else if (tol === "gt") ok = on > cn;
  else if (tol === "ge") ok = on >= cn;
  else die(`unknown --tol ${tol}`);
  console.log(ok ? "MATCH" : "MISMATCH");
  process.exit(ok ? 0 : 1);

} else if (cmd === "report") {
  const l = load();
  const lines = [`# Vouch report: ${l.task}`, ""];
  const counts = { verified: 0, contradicted: 0, cannot_verify: 0, pending: 0 };
  for (const [id, c] of Object.entries(l.claims)) {
    counts[c.verdict || "pending"]++;
    const es = l.entries.filter((e) => e.claim_id === id);
    lines.push(`## ${id}: ${(c.verdict || "NOT CHECKED").toUpperCase().replace("_", " ")}`);
    lines.push(`- Claim: ${c.text}`);
    if (c.observed) lines.push(`- Telegraph said: ${c.observed}`);
    if (c.why) lines.push(`- Why: ${c.why}`);
    lines.push(`- Spent: ${usd(es.reduce((s, e) => s + e.cost_usd, 0))} over ${es.length} ask(s)`);
    for (const e of es) lines.push(`  - ${e.intent || "-"} via ${e.miner || "-"}: ${usd(e.cost_usd)}${e.receipt ? `, receipt ${e.receipt}` : ", no receipt"}${e.note ? ` (${e.note})` : ""}`);
    lines.push("");
  }
  lines.push(`Totals: ${counts.verified} verified, ${counts.contradicted} contradicted, ${counts.cannot_verify} cannot verify, ${counts.pending} not checked.`);
  lines.push(`Spend: ${usd(spent(l))} of ${usd(l.task_cap_usd)} task cap (per-claim cap ${usd(l.claim_cap_usd)}).`);
  console.log(lines.join("\n"));

} else {
  die("vouch.mjs commands: init | claim | check | record | verdict | judge | report\nSee SKILL.md.", 1);
}
