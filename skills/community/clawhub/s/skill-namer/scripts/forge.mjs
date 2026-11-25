#!/usr/bin/env node
// Skill Namer: forge.mjs
// Generates blend candidates from lane words, or from the person's own words in any script.
// Node built-ins only. It applies letter, length, seam, script-mix, and near-known-name checks and nothing else:
// no availability, trademark, language, cultural, or accessibility check. Raw candidates for the cut list to sort.
//
// Usage:
//   node scripts/forge.mjs --lanes social,network --max 10 --count 25
//   node scripts/forge.mjs --words work,crew,pay,rail,mesh --seed 7
//   node scripts/forge.mjs --words trabajo,red,pago --script any
//   node scripts/forge.mjs --mutate workcrew --mine
//   node scripts/forge.mjs --lanes money,network --json
import { parseArgs } from "node:util";
import { randomInt } from "node:crypto";

let lib;
try {
  lib = await import("./lib.mjs");
} catch {
  console.log("scripts/lib.mjs is missing beside this file. Nothing was generated; blend by hand with the lanes in the workflow.");
  process.exit(1);
}
const { CONTROL_RE, HIDDEN_RE, fold, hadTurkishDot, revealHidden, joinersAllowed, scriptsOf, mixAllowed, mixReason, nearKnownName, wholeScriptLookalike, NOT_DETECTED } = lib;
const JOINERS_RE = new RegExp("[" + String.fromCodePoint(0x200C) + String.fromCodePoint(0x200D) + "]", "gu");

const LANES = {
  social: ["work", "gig", "ask", "crew", "guild", "team", "coop"],
  vitality: ["bloom", "pulse", "root", "flow", "kin", "weave", "garden"],
  coordination: ["handoff", "relay", "invite", "route", "queue", "sync", "link"],
  trust: ["claim", "record", "proof", "attest", "receipt", "verify"],
  money: ["pay", "tip", "fund", "split", "settle", "escrow"],
  network: ["mesh", "rail", "hub", "lane", "ring", "fabric", "bridge"],
};

const RINGS = [
  { rung: "1 suffix", words: ["mesh", "hub", "lane", "rail", "room"] },
  { rung: "2 group word", words: ["crew", "guild", "coop", "team", "kin"] },
  { rung: "3 work noun", words: ["gig", "work", "task", "job", "quest"] },
];

const USAGE = `forge.mjs: raw blend candidates from lane words. No availability, trademark, language, or cultural check.
  --lanes social,network     lanes to blend (social, vitality, coordination, trust, money, network)
  --words work,crew,rail     your own words instead of lanes, in your own language (two or more)
  --script latin | any       latin (default): a to z only, for slugs. any: letters of any script
  --max 10 --min 6           length window, counted in characters of the script
  --count 20                 how many to print (stopped candidates are not counted)
  --seed 7                   shuffle with this seed; without it a fresh seed is drawn and printed, so runs differ
  --mutate workcrew --mine   ladder rungs 1 to 4 for one candidate of your own; --mine affirms it is yours, not a brand's
                             (an honor flag: it records your word and protects nothing by itself; the small list and the cut list do)
  --json                     print one JSON object instead of text; agents should parse this, never the text
  --help                     this text
Exit code 0 means the run completed with at least one candidate; stopped candidates are reported in the output.
Exit code 2 means nothing could be produced (every candidate stopped, or none fit the window).`;

const wantsJson = process.argv.some((a) => a === "--json" || a.startsWith("--json="));
function fail(message, code = 1) {
  if (wantsJson) console.log(JSON.stringify({ script: "forge.mjs", error: message }, null, 2));
  else console.log(message);
  process.exit(code);
}

let values;
try {
  ({ values } = parseArgs({
    options: {
      lanes: { type: "string" },
      words: { type: "string" },
      script: { type: "string", default: "latin" },
      max: { type: "string", default: "10" },
      min: { type: "string", default: "6" },
      count: { type: "string", default: "20" },
      seed: { type: "string" },
      mutate: { type: "string" },
      mine: { type: "boolean", default: false },
      json: { type: "boolean", default: false },
      help: { type: "boolean", default: false },
    },
  }));
} catch (err) {
  fail(err.message + "\n" + USAGE);
}
if (values.help) {
  console.log(USAGE);
  process.exit(0);
}
if (!["latin", "any"].includes(values.script)) fail("--script takes latin or any.");
if (values.words !== undefined && values.lanes !== undefined) fail("Give --words or --lanes, not both; --words are your own words, --lanes are this file's English lists.");
if (values.words !== undefined && values.words.trim() === "") fail("--words is empty; give two or more words.");
const anyScript = values.script === "any";
function whole(name, raw, lo, hi) {
  const v = Number(raw);
  if (!Number.isInteger(v) || v < lo || v > hi) fail(`--${name} takes a whole number from ${lo} to ${hi}.`);
  return v;
}
const max = whole("max", values.max, 1, 64);
const min = whole("min", values.min, 1, 64);
const count = whole("count", values.count, 1, 500);
const seed = values.seed === undefined ? randomInt(0, 1000000000) : whole("seed", values.seed, 0, 1000000000);
const seedGiven = values.seed !== undefined;
if (min > max) fail("--min cannot be larger than --max.");
const segmenter = new Intl.Segmenter(undefined, { granularity: "grapheme" });
let stopped = 0;

// Length counts what a reader sees: one grapheme per letter, marks included.
function visibleLength(s) {
  let k = 0;
  for (const _ of segmenter.segment(s)) k += 1;
  return k;
}

// Letters plus combining marks, so Devanagari, Thai, Bengali, Tamil, and vocalized Arabic and Hebrew words can enter.
// A word starts with a letter; a mark on its own, or a leading mark, is not a word.
function lettersOnly(s) {
  const core = s.replace(JOINERS_RE, "");
  return anyScript ? /^\p{L}[\p{L}\p{M}]*$/u.test(core) : /^[a-z]+$/.test(core);
}

function isLatin(s) {
  return /^[a-z]+$/.test(s);
}

// Heuristic, Latin script only. Digraphs (sh, ch, th, ph, ck) count as one consonant; a run of three or more
// consonants across the seam with no liquid or nasal among them (r, l, m, n) reads badly. workmesh, workcrew, and
// meshwork pass.
function seamOk(a, b) {
  const seam = (a.slice(-2) + b.slice(0, 2)).replace(/sh|ch|th|ph|ck/g, "S");
  const runs = seam.match(/[^aeiouy]+/g) || [];
  return runs.every((run) => run.length < 3 || /[rlmn]/.test(run));
}

// Heuristic, Latin script only: mirrored-letter pairs at the seam are hard for some readers.
function mirrorOk(a, b) {
  const pair = a.slice(-1) + b.slice(0, 1);
  return !["bd", "db", "pq", "qp"].includes(pair);
}

// Returns a reason to stop the candidate, or null.
function stopReason(name) {
  if (HIDDEN_RE.test(name) && !joinersAllowed(name)) return "hidden character";
  const sc = scriptsOf(name);
  if (!mixAllowed(sc)) return `mixed scripts (${sc.join(" + ")}): ${mixReason(sc)}`;
  const near = nearKnownName(name);
  if (near) return `within one edit of, or built around, "${near}"`;
  return null;
}

function note(name) {
  const sc = scriptsOf(name);
  const parts = [];
  if (sc.length > 1) parts.push(`scripts: ${sc.join(" + ")}; a language that writes this way decides`);
  if (wholeScriptLookalike(name)) parts.push("every letter has a Latin lookalike; a person decides whether this is a real word or a lookalike");
  return parts.length ? ` [${parts.join("; ")}]` : "";
}

// With two or more lanes, a blend takes one word from each lane; within one lane the words share a job and the blend says it twice.
function blends(words) {
  const out = new Set();
  for (const a of words) {
    for (const b of words) {
      if (a === b) continue;
      if (laneOf.size && laneOf.get(a) && laneOf.get(a) === laneOf.get(b) && new Set(laneOf.values()).size >= 2) continue;
      const name = (a + b).normalize("NFC");
      if (!lettersOnly(name)) continue;
      const len = visibleLength(name);
      if (len < min || len > max) { setAside.length += 1; continue; }
      if (isLatin(a) && isLatin(b) && (!seamOk(a, b) || !mirrorOk(a, b))) { setAside.sound += 1; continue; }
      out.add(name);
    }
  }
  const list = [...out].sort((x, y) => visibleLength(x) - visibleLength(y) || x.localeCompare(y));
  return shuffle(list, seed);
}

// Small deterministic shuffle so a seed gives a different order from the shared default.
function shuffle(list, s) {
  let x = (s * 2654435761 + 1013904223) >>> 0;
  const next = () => { x ^= x << 13; x >>>= 0; x ^= x >>> 17; x ^= x << 5; x >>>= 0; return x / 4294967296; };
  const arr = [...list];
  for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(next() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]]; }
  return arr;
}

// Rungs 1 to 4 of the ladder (suffix, group word, work noun, plural). Rungs 5 and 6 (clarifier syllable, lengthen)
// need meaning, so they stay with the agent. The rings are English words, so a swap is offered only where the rest
// of the name is Latin letters, and each swap goes through the same seam and mirror heuristics as a fresh blend.
function mutate(name) {
  const out = new Map();
  const latin = isLatin(name);
  for (const { rung, words } of RINGS) {
    for (const w of words) {
      if (name.endsWith(w) && name.length > w.length) {
        const head = name.slice(0, -w.length);
        for (const alt of words) if (alt !== w && (!latin || (seamOk(head, alt) && mirrorOk(head, alt)))) out.set(head + alt, rung);
      }
      if (name.startsWith(w) && name.length > w.length) {
        const tail = name.slice(w.length);
        for (const alt of words) if (alt !== w && (!latin || (seamOk(alt, tail) && mirrorOk(alt, tail)))) out.set(alt + tail, rung);
      }
    }
  }
  if (latin) out.set(name + "s", "4 plural");
  return [...out.entries()].filter(([n]) => lettersOnly(n) && visibleLength(n) <= max + 2).sort();
}

// Blends outside the length window or failing the sound heuristics are not stops; they are counted and reported.
const setAside = { length: 0, sound: 0 };
const report = { script: "forge.mjs", performed: "letters only, length, a Latin-only seam and mirrored-letter heuristic, script mixing, a small list of well-known names; no availability, trademark, language, cultural, or accessibility check", seed, seed_given: seedGiven, candidates: [], stopped: [], notes: [], not_detected: NOT_DETECTED.replace(/\n\s*/g, " ") };

// Every candidate is checked for a stop reason, so stopped names are always reported; then up to limit are shown.
function collect(list, limit) {
  const kept = [];
  for (const item of list) {
    const [n, rung] = Array.isArray(item) ? item : [item, null];
    const why = stopReason(n);
    if (why) { stopped += 1; report.stopped.push({ name: revealHidden(n), reason: why }); continue; }
    kept.push([n, rung]);
  }
  const shown = limit === null ? kept : kept.slice(0, limit);
  for (const [n, rung] of shown) report.candidates.push({ name: n, rung: rung || undefined, note: note(n).replace(/^ \[|\]$/g, "") || undefined });
  return shown.length;
}

function finish(headline, code) {
  if (anyScript) report.notes.push("The seam and mirrored-letter heuristics apply to Latin letters only; the audience's own sound rules decide the rest.");
  report.notes.push(seedGiven ? `Order from --seed ${seed}.` : `Order from a fresh seed, ${seed}; pass --seed ${seed} to repeat it.`);
  report.notes.push("These are raw candidates for the cut list. Run the ladder only on your own candidates.");
  if (setAside.length || setAside.sound) {
    report.set_aside = { outside_length_window: setAside.length, seam_or_mirror_heuristic: setAside.sound };
    report.notes.push(`Set aside, not stopped: ${setAside.length} blend(s) outside the ${min} to ${max} window and ${setAside.sound} by the seam or mirrored-letter heuristic. Change --min, --max, or the words to see them.`);
  }
  if (values.json) {
    console.log(JSON.stringify(report, null, 2));
    process.exit(code);
  }
  console.log(headline);
  for (const c of report.candidates) console.log("  " + c.name + (c.rung ? `  (rung ${c.rung})` : "") + (c.note ? `  [${c.note}]` : ""));
  if (report.candidates.length === 0) console.log("  (none)");
  for (const s of report.stopped) console.log(`  (stopped: ${s.name}, ${s.reason})`);
  console.log("");
  console.log("No availability, trademark, language, cultural, or accessibility check was performed.");
  console.log("Applied here: letters only, length, a Latin-only seam and mirrored-letter heuristic, script mixing, and a small list of well-known names.");
  for (const l of report.notes) console.log(l);
  console.log(NOT_DETECTED);
  if (stopped) console.log(`${stopped} candidate(s) stopped and reported above.`);
  process.exit(code);
}

if (values.mutate !== undefined) {
  if (!values.mine) fail("--mutate needs --mine: an affirmation that the word is your own candidate, not a brand, project, or person's name. The ladder on someone else's name makes lookalikes.", 2);
  const name = fold(values.mutate);
  if (!name || CONTROL_RE.test(name) || !lettersOnly(name)) fail(anyScript ? "Mutate takes a single word of letters." : "Mutate takes a single lowercase, a-to-z word (add --script any for other scripts).");
  const why = stopReason(name);
  if (why) fail(`Stopped: ${revealHidden(name)}, ${why}. Nothing mutated.`, 2);
  report.mutated = name;
  report.affirmation = "Affirmed by the person as their own candidate (--mine). This records their word; it is not a check, and the ledger's harm line carries it.";
  const list = mutate(name);
  const shownMutations = collect(list, null);
  finish(`Mutations of ${name} (ladder rungs 1 suffix, 2 group word, 3 work noun, 4 plural; the rings are English words):\n${report.affirmation}`, shownMutations === 0 ? 2 : 0);
}

let words = [];
const laneOf = new Map();
if (values.words !== undefined) words = [...new Set(values.words.split(",").map((w) => fold(w.trim())).filter(Boolean))];
else {
  const lanes = (values.lanes || "social,network").split(",").map((l) => l.trim());
  for (const l of lanes) {
    if (!LANES[l]) fail(`Unknown lane: ${l}. Lanes: ${Object.keys(LANES).join(", ")}`);
    for (const w of LANES[l]) { words.push(w); if (!laneOf.has(w)) laneOf.set(w, l); }
  }
  words = [...new Set(words)];
}

if (words.length < 2) fail("Give at least two words; a blend needs two.");
if (values.words !== undefined && hadTurkishDot(values.words)) report.notes.push("Turkish letters were folded the Turkish way: a dotted capital I became i and, where ş, ğ, or ı are present, a plain capital I became dotless ı; no blend carries a combining dot that looks like the plain word.");
const control = words.filter((w) => CONTROL_RE.test(w));
if (control.length) fail(`Whitespace or control characters found in: ${control.map(revealHidden).join(", ")}. One word per entry, no spaces.`);
const hidden = words.filter((w) => HIDDEN_RE.test(w) && !joinersAllowed(w));
if (hidden.length) fail(`Hidden characters (zero-width, format, or direction marks) found in: ${hidden.map(revealHidden).join(", ")}. Remove them first.`);
const bad = words.filter((w) => !lettersOnly(w));
if (bad.length) fail(anyScript ? `Letters only: ${bad.join(", ")}` : `Letters only, a to z, lowercase: ${bad.join(", ")} (add --script any for other scripts)`);

const list = blends(words);
const shown = collect(list, count);
report.window = { min, max, count, script: values.script };
finish(`Candidates (up to ${count}, ${min} to ${max} characters, letters only${anyScript ? ", any script, marks included" : ""}):`, shown === 0 ? 2 : 0);
