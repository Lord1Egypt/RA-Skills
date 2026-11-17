#!/usr/bin/env node
// Standalone: tokens and cost from OpenClaw session transcripts. No dependencies.
// Usage: node cost.mjs [--window <minutes>] [--json]
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const windowMin = Number(opt("--window") ?? 0);
const since = windowMin ? Date.now() - windowMin * 60_000 : 0;
const root = process.env.OPENCLAW_STATE_DIR?.trim() || path.join(os.homedir(), ".openclaw");
const num = (v) => (typeof v === "number" && Number.isFinite(v) ? v : 0);

function usageOf(line) {
  const msg = line?.message && typeof line.message === "object" ? line.message : line;
  const u = msg?.usage ?? line?.usage;
  const content = Array.isArray(msg?.content) ? msg.content : [];
  const toolCalls = content.filter((c) => c && (c.type === "toolCall" || c.type === "tool_use" || c.type === "tool_call")).length;
  const ts = typeof line?.ts === "number" ? line.ts : typeof line?.timestamp === "number" ? line.timestamp : typeof line?.timestamp === "string" ? Date.parse(line.timestamp) : undefined;
  if (!u || typeof u !== "object") return toolCalls ? { input: 0, output: 0, total: 0, cost: 0, ts, toolCalls } : undefined;
  const input = num(u.input ?? u.input_tokens ?? u.prompt_tokens);
  const output = num(u.output ?? u.output_tokens ?? u.completion_tokens);
  const total = num(u.totalTokens ?? u.total_tokens) || input + output + num(u.cacheRead) + num(u.cacheWrite);
  const c = u.cost;
  const cost = typeof c === "number" ? c : c && typeof c === "object" ? num(c.total) || num(c.input) + num(c.output) + num(c.cacheRead) + num(c.cacheWrite) : 0;
  return { input, output, total, cost, model: msg?.model, ts, toolCalls };
}

const sessions = [];
let agents = [];
try { agents = fs.readdirSync(path.join(root, "agents")); } catch {}
for (const a of agents) {
  const dir = path.join(root, "agents", a, "sessions");
  let files = [];
  try { files = fs.readdirSync(dir); } catch { continue; }
  for (const f of files) {
    if (!f.endsWith(".jsonl") || f.includes(".trajectory.")) continue;
    const s = { agent: a, session: f.replace(/\.jsonl$/, ""), tokens: 0, cost: 0, toolCalls: 0, messages: 0 };
    for (const raw of fs.readFileSync(path.join(dir, f), "utf8").split(/\r?\n/)) {
      if (!raw.trim()) continue;
      let line; try { line = JSON.parse(raw); } catch { continue; }
      const u = usageOf(line); if (!u) continue;
      if (u.ts && u.ts < since) continue;
      s.tokens += u.total; s.cost += u.cost; s.toolCalls += u.toolCalls; if (u.total > 0) s.messages++;
    }
    if (s.tokens || s.toolCalls) sessions.push(s);
  }
}
sessions.sort((a, b) => b.cost - a.cost || b.tokens - a.tokens);
const t = sessions.reduce((t, s) => ({ tokens: t.tokens + s.tokens, cost: t.cost + s.cost, toolCalls: t.toolCalls + s.toolCalls }), { tokens: 0, cost: 0, toolCalls: 0 });
if (args.includes("--json")) { console.log(JSON.stringify({ root, windowMin, totals: t, sessions }, null, 2)); process.exit(0); }
console.log(`${sessions.length} session(s)${windowMin ? " in the last " + windowMin + " min" : ""}: ${t.tokens.toLocaleString()} tokens, ${t.cost ? "$" + t.cost.toFixed(4) : "cost not reported"}, ${t.toolCalls} tool calls${t.toolCalls && t.cost ? " (~$" + (t.cost / t.toolCalls).toFixed(4) + " per tool call)" : ""}`);
for (const s of sessions.slice(0, 10)) console.log(`- ${s.agent}/${s.session.slice(0, 8)}  ${s.tokens.toLocaleString()} tok  ${s.cost ? "$" + s.cost.toFixed(4) : "-"}  ${s.toolCalls} tool calls`);
