#!/usr/bin/env node
// video-repurpose-engine-lite — rank short-clip windows from a transcript.
"use strict";
const fs = require("node:fs");

const HOOK = /\?|!|never|always|biggest|mistake|secret|truth|actually|everyone|nobody|stop|don't|worst|best|insane|crazy|exactly|story|remember when/i;
const ts = (s) => {
  const m = s.match(/(?:(\d+):)?(\d{1,2}):(\d{1,2})[,.](\d{1,3})/);
  return m ? (+(m[1] || 0) * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000) : null;
};
const fmt = (t) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = (t % 60).toFixed(0).padStart(2, "0");
  return `${h ? h + ":" : ""}${String(m).padStart(2, "0")}:${s}`;
};

function parseCues(text) {
  // SRT/VTT: timestamp lines; fallback: [mm:ss] prefixed lines; last resort: sentence chunks
  const cues = [];
  const re = /(\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})[^\n]*\n([\s\S]*?)(?=\n\s*\n|\n\d+\s*\n|$)/g;
  let m;
  while ((m = re.exec(text))) cues.push({ start: ts(m[1]), end: ts(m[2]), text: m[3].replace(/<[^>]+>/g, "").trim() });
  if (cues.length) return cues;
  for (const line of text.split("\n")) {
    const lm = line.match(/^\s*\[?(\d{1,3}:\d{2}(?::\d{2})?)\]?\s*(.+)/);
    if (lm) {
      const p = lm[1].split(":").map(Number);
      const start = p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1];
      cues.push({ start, end: start + 5, text: lm[2].trim() });
    }
  }
  return cues;
}

function main() {
  const args = process.argv.slice(2);
  const file = args.find((a) => !a.startsWith("--"));
  if (!file) { console.error("usage: node pick.js <transcript.srt> [--clips N] [--min S] [--max S]"); process.exit(2); }
  const get = (k, d) => { const i = args.indexOf(k); return i !== -1 ? Number(args[i + 1]) : d; };
  const nClips = get("--clips", 5), minD = get("--min", 20), maxD = get("--max", 60);

  let text;
  try { text = fs.readFileSync(file, "utf8"); }
  catch (e) { console.error(e.message); process.exit(2); }
  const cues = parseCues(text);
  if (!cues.length) { console.error("no timestamped cues parsed"); process.exit(2); }

  const clips = [];
  for (let i = 0; i < cues.length; i++) {
    let seg = [], end = i;
    for (let j = i; j < cues.length && cues[j].end - cues[i].start <= maxD; j++) { seg.push(cues[j]); end = j; }
    const dur = cues[end].end - cues[i].start;
    if (dur < minD) continue;
    const body = seg.map((c) => c.text).join(" ");
    const hookHits = (body.match(HOOK) || []).length + (body.match(/\?|!/g) || []).length;
    const startsWithHook = HOOK.test(seg[0].text) ? 2 : 0;
    const score = hookHits + startsWithHook + Math.min(seg.length, 8) * 0.5;
    const reason = [
      hookHits && "hook language/questions",
      startsWithHook && "strong opening line",
      `~${Math.round(dur)}s self-contained`,
    ].filter(Boolean).join("; ");
    clips.push({ start: fmt(cues[i].start), end: fmt(cues[end].end), durationSec: Math.round(dur), score: +score.toFixed(1), reason, textPreview: body.slice(0, 140) });
  }
  clips.sort((a, b) => b.score - a.score);
  // drop heavily overlapping picks (same start within 15s)
  const picked = [];
  const sec = (s) => s.split(":").reduce((a, x) => a * 60 + +x, 0);
  for (const c of clips) {
    if (picked.some((p) => Math.abs(sec(p.start) - sec(c.start)) < 15)) continue;
    picked.push(c);
    if (picked.length >= nClips) break;
  }
  console.log(JSON.stringify({ file, cues: cues.length, clips: picked }, null, 2));
}
main();
