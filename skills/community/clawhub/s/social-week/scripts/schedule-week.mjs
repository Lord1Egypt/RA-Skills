#!/usr/bin/env node
// social-week: turn an APPROVED calendar file into PostWire bulk rows, check them (dry run), and schedule them only
// with --confirm. Zero dependencies, Node 18+.
//
//   POSTWIRE_API_KEY=… node scripts/schedule-week.mjs social-week/2026-10-12.json            check only (nothing is stored)
//   POSTWIRE_API_KEY=… node scripts/schedule-week.mjs social-week/2026-10-12.json --confirm  check, then schedule all or none
//   POSTWIRE_API_KEY=… node scripts/schedule-week.mjs social-week/2026-10-12.json --report   what worked (step 7)
//   options: --json (machine-readable output) · --brand <id> · POSTWIRE_BASE_URL (default https://postwire.io)
//
// Only posts whose "status" is "approved" are sent. A network that is not connected, X on the Free plan, or a media
// network without media is left out and listed; nothing is sent twice (PostWire refuses the same upload with 409).
// The key is read from the environment and never printed.
import fs from "node:fs";
import { pathToFileURL } from "node:url";

export const SOURCE = "mcp-skill-social-week"; // starts with "mcp": PostWire treats the calls as an AI agent's
export const LIMITS = { linkedin: 3000, x: 280, bluesky: 300, mastodon: 500, instagram: 2200, tiktok: 2200, youtube: 5000, facebook: 2000, telegram: 4000, discord: 2000 };
export const TITLE_LIMITS = { youtube: 100, tiktok: 150 };
export const NEEDS_MEDIA = { instagram: "a photo or a video", tiktok: "a video or photos", youtube: "a video" };
export const LINKEDIN_COMMENT_MAX = 1250;
export const X_THREAD_MAX = 25;

// X counts a link as 23 and an emoji as 2 (PostWire's dry run is the authority; this is the early warning).
const URL_RE = /https?:\/\/[^\s]+/g;
export function xLength(s) {
  const t = String(s ?? "").normalize("NFC").replace(URL_RE, "x".repeat(23));
  let n = 0;
  for (const ch of t) n += /\p{Extended_Pictographic}/u.test(ch) ? 2 : 1;
  return n;
}
export const lengthOf = (net, s) => (net === "x" ? xLength(s) : String(s ?? "").length);

const mediaOf = (d) => [...(d.media || []).map((u) => (typeof u === "string" ? u : u.url)), ...(d.video_url ? [`video:${d.video_url}`] : []), ...(d.photo_url ? [d.photo_url] : [])].filter(Boolean);

// calendar + what /api/me says -> { rows, skipped, problems, notes }. Pure: no network, no clock.
export function planRows(cal, me = null) {
  const rows = [], skipped = [], problems = [], notes = [];
  if (!cal || !Array.isArray(cal.posts)) return { rows, skipped, problems: [{ where: "file", message: "no posts[] in the calendar file" }], notes };
  if (!cal.timezone) problems.push({ where: "file", message: "timezone is missing (an IANA name such as America/Lima)" });
  const plan = me?.plan || null;
  const brand = cal.brand_id || null;
  const connected = me?.connections ? new Set(me.connections.filter((c) => !brand || c.brand_id === brand).map((c) => c.platform)) : null;
  for (const [i, p] of cal.posts.entries()) {
    const where = `${p.day || "post " + (i + 1)} ${p.date || ""} ${p.time || ""}`.trim();
    if (p.status !== "approved") { skipped.push({ where, network: "*", reason: `status is "${p.status || "missing"}", not "approved"` }); continue; }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(p.date || "") || !/^\d{1,2}:\d{2}$/.test(p.time || "")) { problems.push({ where, message: "date must be YYYY-MM-DD and time HH:MM" }); continue; }
    // One row per media set: networks that share the same photo or video go in one row (row-level media_urls, so a
    // single video reaches TikTok/YouTube/Reels as a video), text-only networks in another row at the same time.
    // PostWire's bulk parser treats per-network media lists as photo posts, which TikTok refuses for a video.
    const groups = new Map();
    const label = `social-week · ${p.day || p.date} · ${String(p.angle || "").trim()}`.slice(0, 120);
    for (const [net, d] of Object.entries(p.networks || {})) {
      if (!LIMITS[net]) { skipped.push({ where, network: net, reason: "PostWire does not post there" }); continue; }
      if (connected && !connected.has(net)) { skipped.push({ where, network: net, reason: "not connected (create_connect_link / POST /api/connect-link)" }); continue; }
      if (net === "x" && plan === "free") { skipped.push({ where, network: net, reason: "X is on the paid plans only" }); continue; }
      const media = mediaOf(d || {});
      if (NEEDS_MEDIA[net] && !media.length) { skipped.push({ where, network: net, reason: `needs ${NEEDS_MEDIA[net]}` }); continue; }
      const text = String(d.text ?? "");
      if (!text.trim() && !media.length) { problems.push({ where, network: net, message: "empty text" }); continue; }
      const n = lengthOf(net, text);
      if (n > LIMITS[net]) problems.push({ where, network: net, message: `${n} characters, ${net} takes ${LIMITS[net]}` });
      if (d.title && TITLE_LIMITS[net] && d.title.length > TITLE_LIMITS[net]) problems.push({ where, network: net, message: `title ${d.title.length} characters, ${net} takes ${TITLE_LIMITS[net]}` });
      const sig = media.join(" ");
      if (!groups.has(sig)) groups.set(sig, { date: `${p.date} ${p.time}`, networks: [], ...(sig ? { media_urls: sig } : {}), label });
      const row = groups.get(sig);
      row[`text_${net}`] = text;
      if (d.title) row[`title_${net}`] = d.title;
      if (net === "linkedin" && d.first_comment) {
        if (d.first_comment.length > LINKEDIN_COMMENT_MAX) problems.push({ where, network: net, message: `first comment ${d.first_comment.length} characters, LinkedIn takes ${LINKEDIN_COMMENT_MAX}` });
        row.first_comment = d.first_comment;
      }
      if (net === "x") {
        const thread = (d.thread || []).map(String);
        if (thread.length > X_THREAD_MAX) problems.push({ where, network: net, message: `thread has ${thread.length} posts after the first, X takes ${X_THREAD_MAX}` });
        for (const [k, t] of [...thread.entries()]) if (xLength(t) > 280) problems.push({ where, network: net, message: `thread post ${k + 2}: ${xLength(t)} characters, X takes 280` });
        if (d.reply && xLength(d.reply) > 280) problems.push({ where, network: net, message: `reply: ${xLength(d.reply)} characters, X takes 280` });
        if (thread.length) row.x_thread = thread.join("|||");
        if (d.reply) row.x_reply = String(d.reply);
      }
      if ((net === "tiktok" || net === "youtube") && d.privacy) {
        if (row.privacy && row.privacy !== d.privacy) problems.push({ where, network: net, message: "TikTok and YouTube with the same video need the same privacy: give one of them its own post" });
        row.privacy = d.privacy;
      }
      if (net === "tiktok" && !d.privacy) problems.push({ where, network: "tiktok", message: "TikTok needs the account owner's choice of privacy (public, friends or private)" });
      row.networks.push(net);
    }
    for (const row of groups.values()) rows.push({ ...row, networks: row.networks.join(", ") });
  }
  const L = me?.limits || {};
  const perPost = L.networks_per_post?.limit;
  if (perPost != null && rows.some((r) => r.networks.split(", ").length > perPost))
    notes.push(`This plan sends each post to ${perPost} networks: the first ${perPost} of each row go out, the others are written and held.`);
  const left = L.scheduled_queue?.left;
  if (left != null && rows.length > left)
    notes.push(`This plan keeps ${L.scheduled_queue.limit} scheduled posts waiting at a time (${left} free now): ${rows.length - left} of these ${rows.length} will be saved as held, not published, until the plan is upgraded.`);
  const maxRows = L.automation?.bulk_rows_per_upload;
  if (maxRows != null && maxRows > 0 && rows.length > maxRows) problems.push({ where: "upload", message: `${rows.length} rows, this plan takes ${maxRows} per upload` });
  const postsLeft = L.posts_this_month?.limit != null ? L.posts_this_month.limit - (L.posts_this_month.used || 0) : null;
  const count = rows.reduce((a, r) => a + r.networks.split(", ").length, 0);
  if (postsLeft != null && count > postsLeft) notes.push(`These rows are ${count} network posts and the plan has ${postsLeft} left this month.`);
  return { rows, skipped, problems, notes };
}

export async function api(base, key, method, path, body) {
  const res = await fetch(base.replace(/\/+$/, "") + path, {
    method,
    headers: { Authorization: `Bearer ${key}`, "X-PostWire-Source": SOURCE, ...(body ? { "Content-Type": "application/json" } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  let json = null;
  try { json = await res.json(); } catch { /* not JSON */ }
  return { status: res.status, json };
}

// Step 7 (the re-run): what the account's own numbers say, reduced to what next week's plan needs.
export function summarizeInsights(ins = {}) {
  const top = (ins.top || []).map((p) => ({ platform: p.platform, x_median: p.x_median, headline: p.headline || p.excerpt || "", n: p.n, url: p.post_url || null, id: p.id }));
  return { winners: top.filter((p) => p.x_median >= 2), under: top.filter((p) => p.x_median != null && p.x_median <= 0.5), measured: top.length,
    best_times: ins.best_times || null, headline_pattern: ins.headline_pattern || null, next: ins.next || [], patterns_locked: !!ins.locked };
}

// The whole run. Returns { ok, stage, ... }; never throws for an API answer.
export async function run({ file, cal, confirm = false, report = false, base = "https://postwire.io", key, brand = null } = {}) {
  if (!key) return { ok: false, stage: "key", message: "POSTWIRE_API_KEY is not set (create one in the dashboard, API & MCP)" };
  if (!/^https:\/\//.test(base) && !/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?/.test(base)) return { ok: false, stage: "base", message: "POSTWIRE_BASE_URL must be https" };
  cal ||= JSON.parse(fs.readFileSync(file, "utf8"));
  if (brand) cal.brand_id = brand;
  if (report) {
    const q = new URLSearchParams({ tz: cal.timezone || "UTC", ...(cal.brand_id ? { brand_id: cal.brand_id } : {}) });
    const ins = await api(base, key, "GET", `/api/insights?${q}`);
    if (ins.status !== 200) return { ok: false, stage: "report", status: ins.status, error: ins.json };
    return { ok: true, stage: "report", insights: summarizeInsights(ins.json) };
  }
  const me = await api(base, key, "GET", "/api/me");
  if (me.status !== 200) return { ok: false, stage: "account", status: me.status, error: me.json };
  const plan = planRows(cal, me.json);
  if (plan.problems.length || !plan.rows.length) return { ok: false, stage: "plan", ...plan, message: plan.rows.length ? "fix these first" : "nothing to schedule" };
  const body = { rows: plan.rows, timezone: cal.timezone, ...(cal.brand_id ? { brand_id: cal.brand_id } : {}) };
  const check = await api(base, key, "POST", "/api/bulk", { ...body, dry_run: true });
  if (check.status !== 200 || !check.json?.ok) return { ok: false, stage: "dry_run", status: check.status, result: check.json, ...plan };
  if (!confirm) return { ok: true, stage: "dry_run", result: check.json, ...plan, message: "Checked, nothing scheduled. Run again with --confirm after the user approved." };
  const done = await api(base, key, "POST", "/api/bulk", { ...body, dry_run: false });
  if (done.status === 409) return { ok: true, stage: "already", result: done.json, ...plan, message: "This week was already scheduled; nothing was sent twice." };
  if (done.status !== 200 || !done.json?.ok) return { ok: false, stage: "schedule", status: done.status, result: done.json, ...plan };
  const first = cal.posts.filter((p) => p.status === "approved").map((p) => p.date).sort()[0];
  const from = new Date(Date.parse(`${first}T00:00:00Z`) - 86400_000).toISOString();
  const to = new Date(Date.parse(`${first}T00:00:00Z`) + 9 * 86400_000).toISOString();
  const queue = await api(base, key, "GET", `/api/schedule?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`);
  const ids = new Set((done.json.rows || []).map((r) => r.schedule_id).filter(Boolean));
  const mine = (queue.json?.scheduled || []).filter((s) => ids.has(s.id) || /^social-week · /.test(s.label || ""));
  return { ok: true, stage: "scheduled", batch_id: done.json.batch_id, result: done.json, queue: mine, ...plan,
    undo: `DELETE ${base.replace(/\/+$/, "")}/api/bulk/${done.json.batch_id}`, dashboard: "https://postwire.io/dashboard.html (Queue)" };
}

function print(r) {
  const out = [];
  if (r.insights) {
    const i = r.insights;
    out.push(`  measured posts: ${i.measured}${i.patterns_locked ? " (patterns need a paid plan or more posts)" : ""}`);
    for (const p of i.winners) out.push(`  winner    ${p.platform} ${p.x_median}x its median (n=${p.n}): ${String(p.headline).slice(0, 80)}`);
    for (const p of i.under) out.push(`  under     ${p.platform} ${p.x_median}x its median (n=${p.n}): ${String(p.headline).slice(0, 80)}`);
    if (i.headline_pattern) out.push(`  pattern   ${typeof i.headline_pattern === "string" ? i.headline_pattern : i.headline_pattern.sentence || JSON.stringify(i.headline_pattern)}`);
    for (const n of i.next) out.push(`  next      ${typeof n === "string" ? n : n.text || n.sentence || JSON.stringify(n)}`);
  }
  for (const s of r.skipped || []) out.push(`  left out  ${s.where} ${s.network}: ${s.reason}`);
  for (const p of r.problems || []) out.push(`  PROBLEM   ${p.where}${p.network ? " " + p.network : ""}: ${p.message}`);
  for (const n of r.notes || []) out.push(`  note      ${n}`);
  for (const row of r.result?.rows || []) {
    const errs = (row.errors || []).map((e) => `${e.network ? e.network + ": " : ""}${e.message}`).join("; ");
    out.push(`  line ${row.line}  ${row.local || row.run_at || "?"} ${row.timezone || ""}  ${(row.networks || []).join(", ")}  ${row.ok ? "ok" : "ERROR " + errs}`
      + `${row.approval ? "  waits for approval" : ""}${row.held_for ? `  held (${row.held_for})` : ""}${row.x_credits ? `  ${row.x_credits} X credits` : ""}${row.status ? "  " + row.status : ""}`);
  }
  if (r.result?.message) out.push(`  ${r.result.message}`);
  for (const q of r.queue || []) out.push(`  queued    ${q.run_at}  ${(q.platforms || []).join(", ")}  ${q.status}  ${q.id}`);
  if (r.undo) out.push(`  undo the whole week: ${r.undo}`);
  if (r.dashboard) out.push(`  queue: ${r.dashboard}`);
  if (r.message) out.push(`  ${r.message}`);
  console.log(`${r.ok ? "OK" : "NOT DONE"} (${r.stage})\n${out.join("\n")}`);
}

if (import.meta.url === pathToFileURL(process.argv[1] || "").href) {
  const args = process.argv.slice(2);
  const file = args.find((a) => !a.startsWith("--") && args[args.indexOf(a) - 1] !== "--brand");
  if (!file) { console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).slice(0, 11).map((l) => l.slice(3)).join("\n")); process.exit(2); }
  const brand = args.includes("--brand") ? args[args.indexOf("--brand") + 1] : null;
  const r = await run({ file, confirm: args.includes("--confirm"), report: args.includes("--report"), base: process.env.POSTWIRE_BASE_URL || "https://postwire.io", key: process.env.POSTWIRE_API_KEY, brand });
  if (args.includes("--json")) console.log(JSON.stringify(r, null, 2)); else print(r);
  process.exitCode = r.ok ? 0 : 1; // not process.exit(): on Windows it can abort while fetch's sockets close
}
