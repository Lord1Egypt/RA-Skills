#!/usr/bin/env node
// workled skill installer/uninstaller for all supported clients.
// Usage client targets: run `node skill-install.mjs --help`.

import { spawnSync } from "child_process";
import { homedir } from "os";
import { dirname, join, resolve, sep } from "path";
import { fileURLToPath, pathToFileURL } from "url";
import {
  copyFileSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  rmdirSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "fs";
import {
  WRITE_ERROR_REASONS,
  checkWriteAccess,
  stripJsonc,
  hermesHome,
  sleep,
  dshHome,
  traeCnHooksHome,
  createSkillJunctions,
} from "./utils.js";
import { CLIENTS, CLIENT_TARGETS, detectClient, resolveMergedUrl, resolveMcpType } from "./index.js";

const scriptDir = dirname(fileURLToPath(import.meta.url));

// Build every path with forward slashes so commands, emitted hooks/MCP configs,
// status output, and uninstall messages read identically on Windows and POSIX.
// Node's fs and dirname accept forward slashes on Windows, so using `joinP`
// for every path is safe and makes ALL paths cross-platform consistent.
const joinP = (...a) => String(join(...a)).split(/[\\/]+/).join("/");

function resolveCorePath() {
  const globalIndex = joinP(homedir(), ".agents", "skills", "workled", "index.js");
  const chosen = existsSync(globalIndex) ? globalIndex : joinP(scriptDir, "index.js");
  // Normalize to forward slashes so the emitted hook/MCP command bytes are
  // identical on Windows and POSIX. Backslashes would otherwise (a) mangle the
  // path under Hermes' shlex.split on Windows and (b) change the command text
  // vs. the forward-slash form already in the shell-hook allowlist, silently
  // invalidating every byte-exact approval. `sep` handles win32 vs posix.
  return chosen.split(sep).join("/");
}
const corePath = resolveCorePath();

// Entry point a GENERATED artifact (client plugin file / hook command) must
// import: the self-contained copy installSkill() writes into that client's own
// skills dir — never the source checkout.
//
// Why: installSkill copies the whole tree next to the client precisely so an
// installed plugin does not depend on the checkout surviving. Emitting
// corePath there silently re-introduced that dependency, so deleting or moving
// the checkout broke every plugin and hook even though a working copy sat in
// the client's own skills dir. Each client references its own copy, which the
// same install run (re)writes, so the two can never drift.
//
// Falls back to corePath only when no copy is on disk yet: an installer running
// from inside the installed copy (installSkill is then a no-op), or a client
// without a skillPath. Passing null keeps the old corePath behaviour.
function entryPathFor(client) {
  const dir = client ? CLIENT_TARGETS[client]?.skillPath?.() : null;
  if (dir) {
    const p = joinP(dir, "index.js");
    if (existsSync(p)) return p;
  }
  return corePath;
}
// SKILL_VERSION: single-sourced from SKILL.md frontmatter (the `version` field),
// with a fallback so a missing or corrupt frontmatter never crashes the installer.
// (_meta.json was deprecated and removed; the version now lives only in SKILL.md.)
let SKILL_VERSION = "";
try {
  const skillMd = readFileSync(joinP(scriptDir, "SKILL.md"), "utf8");
  const m = skillMd.match(/^version:\s*"?(.*?)"?\s*$/m);
  if (m) SKILL_VERSION = m[1];
} catch {
  // fallback to default
}
const h = homedir();

// ---- safe path removal ----------------------------------------------------
// WorkBuddy's managed Node intercepts fs delete calls through a "safe-delete"
// shim. Two behaviours are known:
//   1. It may MOVE the target into the Recycle Bin and then THROW, even though
//      the path is already gone (a no-op that would otherwise abort the caller).
//   2. For a "bulk"/recursive delete past a per-turn threshold it REFUSES and
//      THROWS, leaving the target STILL PRESENT ("SAFE_DELETE_BULK_*").
// removePath tolerates both: it only treats removal as failed when the path is
// still present after every escape hatch has been tried. A single recursive
// rm covers behaviour 1 and the normal case; when that is refused (behaviour
// 2) we fall back to removeTreeRobust, which deletes entries ONE AT A TIME so
// no individual call trips the bulk-confirm refusal.
function removePath(p, opts = {}) {
  if (!existsSync(p)) return; // already gone — nothing to do

  // Escape hatch 1: a single recursive rm. Succeeds on a normal environment;
  // on behaviour 1 the shim moves the path to the bin and throws (path gone);
  // only behaviour 2 (bulk refusal) leaves the target present.
  try {
    rmSync(p, { recursive: true, force: true, ...opts });
    if (!existsSync(p)) return; // shim moved it to the bin — gone
  } catch {
    if (!existsSync(p)) return; // shim threw but target is gone — treat as success
    // still present: fall through to the manual walk
  }

  // Escape hatch 2: the bulk-refusal path. Walk the tree and delete entries
  // individually — non-recursive deletes are not subject to the bulk-confirm
  // refusal, so this removes the directory even when a single recursive rm was
  // denied.
  try {
    removeTreeRobust(p);
  } catch {
    // fall through to the final existence check
  }
  if (!existsSync(p)) return;

  // Last resort: one more recursive rm in case the walk got partway.
  try { rmSync(p, { recursive: true, force: true, ...opts }); } catch {}
  if (existsSync(p)) {
    throw new Error(`Failed to remove ${p} (safe-delete shim refused and manual removal was blocked)`);
  }
}

// Remove a skill install path that may be a link/junction rather than a real
// directory. A link MUST be removed with a NON-recursive call: removePath's
// behaviour-2 fallback (removeTreeRobust) walks the tree with readdirSync and
// unlinks entries one by one — through a junction that deletes the files of the
// LINK TARGET, i.e. the user's source checkout. rmdirSync on a junction removes
// only the reparse point (verified: target tree untouched). Anything that is
// not a link falls through to the normal recursive removal.
function removeSkillEntry(p) {
  try {
    if (lstatSync(p).isSymbolicLink()) {
      rmdirSync(p);
      return;
    }
  } catch {
    // lstat threw (already gone, or not inspectable) — fall through to removePath
  }
  removePath(p);
}

// Recursive per-entry removal. Each file is unlinked individually and each
// directory is emptied bottom-up, so no single call is a "bulk" delete. Every
// operation is wrapped and verified by an existence check, because the shim may
// move a target to the Recycle Bin and throw (target gone) or refuse (target
// still present) — either way we only escalate when the target truly remains.
function removeTreeRobust(p) {
  let st;
  try { st = statSync(p); } catch { return; } // already gone or inaccessible
  if (st.isDirectory()) {
    let entries = [];
    try { entries = readdirSync(p); } catch { entries = []; }
    for (const entry of entries) {
      removeTreeRobust(joinP(p, entry));
    }
    // Directory should be empty now — remove it bottom-up.
    try { rmdirSync(p, { recursive: false }); } catch {}
  } else {
    try { unlinkSync(p); } catch {}
  }
  // Final attempt for this entry if it is somehow still present.
  if (existsSync(p)) {
    try { rmSync(p, { recursive: true, force: true }); } catch {}
  }
}

// Best-effort cleanup of an empty parent directory (P3). Shared plugin /
// extension dirs that still hold other files are left untouched because
// rmdirSync fails on a non-empty directory (and any throw here is swallowed).
function removeEmptyParent(dir) {
  try {
    rmdirSync(dir, { recursive: false });
  } catch {
    // not empty, missing, or rejected by the safe-delete shim — leave it.
  }
}

// ---- JSON / JSONC merge helpers ---------------------------------------------

function readJsonOrEmpty(file) {
  if (!existsSync(file)) return null;
  try {
    return JSON.parse(stripJsonc(readFileSync(file, "utf8")));
  } catch {
    return null;
  }
}

// Write a JSON config object. mkdir -p the parent first. The single write
// helper for every JSON config this tool manages. No `.bak` is created: the
// writes are idempotent (re-install overwrites the same entries), so backups
// would be pure extra filesystem churn that only prompts cleanup later.
function writeConfig(file, obj) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

// ---- JSON/JSONC text editors (comment-preserving) ---------------------------
// install/uninstall edit config files with byte-level surgery instead of
// JSON.stringify round-trips, so user comments, key order, and formatting
// survive untouched. The workled entry is always a flat object, which makes
// locating it inside the server map a single flat-object regex.

// Return true when <text> parses as JSON (JSONC comments/trailing commas OK).
export function isValidJsonc(text) {
  try {
    JSON.parse(stripJsonc(text));
    return true;
  } catch {
    return false;
  }
}

// Walk raw text (string literals and // and /* */ comments skipped) and return
// the span of a top-level key's object value: { start, end } are the opening
// `{` and its matching `}`. Only the first match of `"<key>"` at brace depth 1
// (directly inside the root object) is considered. Returns null when the key
// or an object value is absent.
//
// A leading UTF-8 BOM is skipped internally so brace-depth counting lines up
// with the actual root `{`, but returned indices are ALWAYS relative to the
// ORIGINAL caller-supplied text (fixes #5: without this BOM compensation every
// returned span would be off by one, and the caller would slice into the
// middle of keys, corrupting the file and falling back to JSON.stringify —
// losing all user comments/formatting).
function findTopLevelObjectValueSpan(text, key) {
  let bom = 0;
  if (text.charCodeAt(0) === 0xfeff) bom = 1;
  const body = bom ? text.slice(1) : text;
  const needle = `"${key}"`;
  const n = body.length;
  let inStr = false;
  let i = 0;
  let depth = 0;
  let valueStart = -1;

  while (i < n) {
    const c = body[i];
    if (inStr) {
      if (c === "\\") i += 2;
      else {
        if (c === '"') inStr = false;
        i++;
      }
      continue;
    }
    if (c === '"') {
      const start = i;
      i++;
      while (i < n) {
        if (body[i] === "\\") i += 2;
        else if (body[i] === '"') {
          i++;
          break;
        } else i++;
      }
      if (depth === 1 && body.slice(start, i) === needle) {
        let j = i;
        while (j < n && /\s/.test(body[j])) j++;
        if (body[j] === ":") {
          j++;
          while (j < n && /\s/.test(body[j])) j++;
          if (body[j] === "{") {
            valueStart = j;
            break;
          }
        }
      }
      continue;
    }
    if (c === "/" && body[i + 1] === "/") {
      while (i < n && body[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && body[i + 1] === "*") {
      i += 2;
      while (i < n && !(body[i] === "*" && body[i + 1] === "/")) i++;
      i += 2;
      continue;
    }
    if (c === "{" || c === "[") depth++;
    else if (c === "}" || c === "]") depth--;
    i++;
  }
  if (valueStart < 0) return null;

  // Match braces from valueStart to find the matching closing brace.
  inStr = false;
  let d = 0;
  let j = valueStart;
  while (j < n) {
    const c = body[j];
    if (inStr) {
      if (c === "\\") j += 2;
      else {
        if (c === '"') inStr = false;
        j++;
      }
      continue;
    }
    if (c === '"') {
      inStr = true;
      j++;
      continue;
    }
    if (c === "/" && body[j + 1] === "/") {
      while (j < n && body[j] !== "\n") j++;
      continue;
    }
    if (c === "/" && body[j + 1] === "*") {
      j += 2;
      while (j < n && !(body[j] === "*" && body[j + 1] === "/")) j++;
      j += 2;
      continue;
    }
    if (c === "{") d++;
    else if (c === "}") {
      d--;
      if (d === 0) return { start: valueStart + bom, end: j + bom };
    }
    j++;
  }
  return null;
}

// Index of the root object's closing `}` (string/comment safe), or -1 when the
// document is not an object literal. A leading BOM is skipped internally but
// returned indices are still relative to the original caller-supplied text so
// callers slice the original bytes correctly (sibling fix of #5).
function findRootObjectEnd(text) {
  let bom = 0;
  if (text.charCodeAt(0) === 0xfeff) bom = 1;
  const body = bom ? text.slice(1) : text;
  let inStr = false;
  let depth = 0;
  for (let i = 0; i < body.length; i++) {
    const c = body[i];
    if (inStr) {
      if (c === "\\") i++;
      else if (c === '"') inStr = false;
      continue;
    }
    if (c === '"') {
      inStr = true;
      continue;
    }
    if (c === "/" && body[i + 1] === "/") {
      while (i < body.length && body[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && body[i + 1] === "*") {
      i += 2;
      while (i < body.length && !(body[i] === "*" && body[i + 1] === "/")) i++;
      continue;
    }
    if (c === "{") depth++;
    else if (c === "}") {
      depth--;
      if (depth === 0) return i + bom;
    }
  }
  return -1;
}

// Locate the span { start, end } of the NAMED OBJECT entry inside a parent
// object-value span. The parent span covers `{ ... }` of the containing map
// (e.g. the value of `"mcp": { ... }`). Walks through the map text with full
// brace-balancing and string/comment awareness so a nested object value
// (e.g. `"workled": { "effects": { "thinking": {...} } }`) does NOT cut the
// match short at an inner `}`. Used by upsertJsoncEntry / removeJsoncEntry
// to replace the regex `[^{}]*` that choked on nested values (fixes #4/#10).
// Returns null when the named entry is absent.
//
// NOTE: the caller passes text.slice(span.start, span.end) which INCLUDES the
// outer opening `{` at index 0 and the closing `}` at the last index. After
// we consume the outer `{` depth becomes 1, and keys written inside the map
// are encountered at depth == 1 (not 0).
//
// Exported for unit tests (fixes #9 — nesting, inline comments, and strings
// containing `{}` must not cut the span short).
export function findNamedObjectSpanInMap(mapText, name) {
  const needle = `"${name}"`;
  const n = mapText.length;
  let inStr = false;
  let i = 0;
  // Depth starts at 0 and increments once when we see the outer `{` of the
  // enclosing map. Top-level keys of the map (e.g. "workled", "my-other-mcp")
  // therefore live at depth == 1; any nested objects push depth to >= 2.
  let depth = 0;

  while (i < n) {
    const c = mapText[i];
    if (inStr) {
      if (c === "\\") i += 2;
      else {
        if (c === '"') inStr = false;
        i++;
      }
      continue;
    }
    if (c === '"') {
      const start = i;
      i++;
      while (i < n) {
        if (mapText[i] === "\\") i += 2;
        else if (mapText[i] === '"') { i++; break; }
        else i++;
      }
      // Keys at depth 1 inside the slice = top-level keys of the containing
      // map (after consuming the outer `{`). This is where we match needle.
      if (depth === 1 && mapText.slice(start, i) === needle) {
        let j = i;
        while (j < n && /\s/.test(mapText[j])) j++;
        if (mapText[j] === ":") {
          j++;
          while (j < n && /\s/.test(mapText[j])) j++;
          if (mapText[j] === "{") {
            // Brace-balance to find the matching `}`. Nesting depth here is
            // local to the needle's value object so we start a fresh counter.
            const objStart = j;
            let d = 0;
            let k = j;
            while (k < n) {
              const cc = mapText[k];
              if (inStr) {
                if (cc === "\\") k += 2;
                else { if (cc === '"') inStr = false; k++; }
                continue;
              }
              if (cc === '"') { inStr = true; k++; continue; }
              if (cc === "/" && mapText[k + 1] === "/") { while (k < n && mapText[k] !== "\n") k++; continue; }
              if (cc === "/" && mapText[k + 1] === "*") { k += 2; while (k < n && !(mapText[k] === "*" && mapText[k + 1] === "/")) k++; k += 2; continue; }
              if (cc === "{") d++;
              else if (cc === "}") { d--; if (d === 0) return { start: objStart, end: k }; }
              k++;
            }
          }
        }
      }
      continue;
    }
    if (c === "/" && mapText[i + 1] === "/") { while (i < n && mapText[i] !== "\n") i++; continue; }
    if (c === "/" && mapText[i + 1] === "*") { i += 2; while (i < n && !(mapText[i] === "*" && mapText[i + 1] === "/")) i++; i += 2; continue; }
    if (c === "{" || c === "[") depth++;
    else if (c === "}" || c === "]") depth--;
    i++;
  }
  return null;
}

// Whitespace prefix of the line containing <index>.
function lineIndentAt(text, index) {
  let lineStart = index;
  while (lineStart > 0 && text[lineStart - 1] !== "\n") lineStart--;
  const m = text.slice(lineStart, index).match(/^[\t ]*/);
  return m ? m[0] : "";
}

// Format a server entry as a multi-line JSON object block.
// <keyIndent> is the indentation that the `"serverName": {` line itself
// should sit at (i.e. the indent of a sibling key inside the containing
// map); child fields sit one level deeper, consistently using 2 spaces.
function jsoncEntryBlock(serverName, entry, keyIndent) {
  const fieldIndent = keyIndent + "  ";
  const keys = Object.keys(entry);
  const lines = [`${keyIndent}${JSON.stringify(serverName)}: {`];
  keys.forEach((k, idx) => {
    const comma = idx < keys.length - 1 ? "," : "";
    lines.push(`${fieldIndent}${JSON.stringify(k)}: ${JSON.stringify(entry[k])}${comma}`);
  });
  lines.push(`${keyIndent}}`);
  return lines.join("\n");
}

// First non-whitespace, non-comment character at/after <from>.
function nextSignificant(text, from) {
  let i = from;
  const n = text.length;
  while (i < n) {
    const c = text[i];
    if (/\s/.test(c)) {
      i++;
      continue;
    }
    if (c === "/" && text[i + 1] === "/") {
      while (i < n && text[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && text[i + 1] === "*") {
      i += 2;
      while (i < n && !(text[i] === "*" && text[i + 1] === "/")) i++;
      i += 2;
      continue;
    }
    return { index: i, char: c };
  }
  return { index: n, char: "" };
}

// First non-whitespace, non-comment character strictly before <from>.
function prevSignificant(text, from) {
  let i = from - 1;
  while (i >= 0) {
    const c = text[i];
    if (/\s/.test(c)) {
      i--;
      continue;
    }
    if (c === "/" && text[i - 1] === "/") {
      const lineStart = text.lastIndexOf("\n", i - 1) + 1;
      i = lineStart - 1;
      continue;
    }
    if (c === "/" && text[i - 1] === "*") {
      const open = text.lastIndexOf("/*", i - 2);
      i = open >= 0 ? open - 1 : i - 2;
      continue;
    }
    return { index: i, char: c };
  }
  return { index: -1, char: "" };
}

// Find the character index of the OPENING QUOTE of a QUOTED KEY ("...") that
// sits immediately before `valObjStart` (the `{` of an object value).
// Specifically: when we see the `{` of e.g. `"workled": { ... }`, this helper
// walks backwards, properly honoring escape sequences, to land on the FIRST
// character of the `"workled"` key (the opening double quote) and NOT on the
// closing double quote (fixes the remove/upsert surgery where only half the
// key string was being deleted). Then, to make sure we haven't walked into a
// string value instead of a key, we verify that the token before this quoted
// string is NOT a colon (a key sits after nothing / `{` / `,` or whitespace,
// never after `:`).
//
// Exported for unit tests (fixes #10 — cross-line `"key":\n  { ... }` layouts
// and string values containing escaped quotes/colons must not return the
// wrong starting index, otherwise the key string is only half-deleted).
export function findKeyLineStartForValue(text, valObjStart) {
  let i = valObjStart;
  while (i > 0) {
    const c = text[i];
    if (c === '"') {
      // Candidate closing quote. Walk backwards (honoring \ escapes) to the
      // matching opening quote of this string.
      let j = i - 1;
      while (j >= 0) {
        if (text[j] === "\\") {
          // skip the escaped character (or just the backslash at the start)
          j -= 2;
          continue;
        }
        if (text[j] === '"') {
          // FOUND the opening quote at index `j`.
          // Verify this is a KEY (not a VALUE): the non-whitespace character
          // BEFORE position j must NOT be `:` (it's typically `{` or `,`).
          let k = j - 1;
          while (k >= 0 && /\s/.test(text[k])) k--;
          if (k >= 0 && text[k] === ":") {
            // It's a value string. Keep the outer backwards-scan going from
            // BEFORE this value string.
            i = k - 1;
          } else {
            // Opening quote of a map key. This is what we want.
            return j;
          }
          break;
        }
        j--;
      }
      if (j < 0) { i--; continue; }
      continue;
    }
    i--;
  }
  return -1;
}

// Insert or replace the <serverName> entry under a top-level <key> map in raw
// JSONC text, preserving every unrelated byte. Returns the edited text, or null
// when surgery is not possible (caller falls back to a JSON.stringify rewrite).
export function upsertJsoncEntry(text, key, serverName, entry) {
  const span = findTopLevelObjectValueSpan(text, key);
  if (!span) {
    // No top-level <key> yet: append it inside the root object.
    const rootEnd = findRootObjectEnd(text);
    if (rootEnd < 0) return null;
    // The closing brace's own indent is the ROOT object's indent, so the new
    // key and its members sit one level deeper. Using it as the key indent
    // (the previous behaviour) emitted the key flush at column 0.
    const rootIndent = lineIndentAt(text, rootEnd);
    const keyIndent = rootIndent + "  ";
    const block = `${JSON.stringify(key)}: {\n${jsoncEntryBlock(serverName, entry, keyIndent + "  ")}\n${keyIndent}}`;
    // Trim the whitespace the root's last member was followed by, so the comma
    // we add lands at the end of that member's line instead of on a line of its
    // own. A root object that held nothing but whitespace collapses to "{".
    const before = text.slice(0, rootEnd).replace(/[ \t\r\n]+$/, "") || "{";
    const after = text.slice(rootEnd);
    const prev = prevSignificant(before, before.length);
    const sep = prev.char === "{" ? "\n" + keyIndent : ",\n" + keyIndent;
    return before + sep + block + "\n" + rootIndent + after;
  }
  const mapSlice = text.slice(span.start, span.end);
  // Use the brace-balancing scanner (not the naive `[^{}]*` regex) so a
  // nested value inside the entry (e.g. `"effects": {...}` inside workled)
  // doesn't truncate the match (fixes #4/#10 — without this we'd overwrite
  // only up to the first inner `}` leaving the rest of the object and a
  // stray `}` that corrupts the file).
  const found = findNamedObjectSpanInMap(mapSlice, serverName);
  if (found) {
    // Existing entry: replace the FULL `"serverName": { ... }` span.
    // jsoncEntryBlock emits the key together with the value block, so the
    // replacement range must cover the entire key:value (not just the value
    // object). Indentation is inherited from the original key line so
    // `"workled":\n  { ... }` layouts remain consistent after re-insertion.
    //
    // findKeyLineStartForValue returns the index of the opening quote of the
    // key (i.e. the position right AFTER the line's leading whitespace).
    // text.slice(0, keyIdx) therefore ends with those leading spaces. Back
    // off the slice by the key-line indent length so the slice ends at the
    // line start (just past the preceding '\n'); jsoncEntryBlock will then
    // re-emit the full key line including its own keyIndent. Without this
    // offset, the prefix indent and the indent emitted inside
    // jsoncEntryBlock add up, producing key lines with 2x indent and field
    // lines with 1x indent (an asymmetric drift that doubles on every
    // reinstall).
    const objAbsoluteStart = span.start + found.start; // index of `{`
    const objAbsoluteEnd   = span.start + found.end;   // index of matching `}`
    const keyIdx = findKeyLineStartForValue(text, objAbsoluteStart);
    const keyIndent = lineIndentAt(text, keyIdx >= 0 ? keyIdx : objAbsoluteStart);
    const replaceFrom = keyIdx >= 0 ? Math.max(0, keyIdx - keyIndent.length) : objAbsoluteStart;
    const replaceTo   = objAbsoluteEnd + 1; // include closing `}`
    return text.slice(0, replaceFrom) + jsoncEntryBlock(serverName, entry, keyIndent) + text.slice(replaceTo);
  }
  // Insert at the end of the map (just before its closing brace).
  const keyIndent = lineIndentAt(text, span.start);
  const inner = text.slice(span.start + 1, span.end).replace(/\s+$/, "");
  const lastSig = prevSignificant(inner, inner.length);
  let sep;
  if (stripJsonc(inner).trim() === "") sep = ""; // empty (or comment-only) map
  else if (lastSig.char === ",") sep = "\n"; // JSONC trailing comma already present
  else sep = ",";
  return (
    text.slice(0, span.start + 1) +
    inner +
    sep +
    "\n" +
    jsoncEntryBlock(serverName, entry, keyIndent + "  ") +
    "\n" +
    keyIndent +
    text.slice(span.end)
  );
}

// Remove the <serverName> entry from a top-level <key> map in raw JSONC text,
// fixing surrounding commas. Returns the edited text, or null when the entry or
// the map is absent. Uses findNamedObjectSpanInMap so entries with nested
// object values (e.g. workled.effects = {...}) are correctly removed end-to-end
// instead of being truncated at the first inner `}` (fixes #4/#10).
export function removeJsoncEntry(text, key, serverName) {
  const span = findTopLevelObjectValueSpan(text, key);
  if (!span) return null;
  const mapSlice = text.slice(span.start, span.end);
  const found = findNamedObjectSpanInMap(mapSlice, serverName);
  if (!found) return null;
  // Compute the KEY start + value end, so comma cleanup covers the full
  // `"key": { ... }` range not just the value part.
  const objAbsoluteStart = span.start + found.start;
  const objAbsoluteEnd   = span.start + found.end;
  const keyIdx = findKeyLineStartForValue(text, objAbsoluteStart);
  // If we can't find the key line, still attempt cleanup starting at the
  // value's `{` — it'll leave `"workled": ` dangling but that's obvious and
  // the isValidJsonc guard will refuse the edit (fallback to full rewrite).
  const removeFrom = keyIdx >= 0 ? keyIdx : objAbsoluteStart;
  const removeTo   = objAbsoluteEnd + 1; // include the closing `}`

  const after = nextSignificant(text, removeTo);
  // A removal must be whitespace-neutral: an earlier version dropped the entry
  // and its comma but left the line break it sat on, stranding one blank line
  // per install/uninstall cycle (measured: 5 blank lines in opencode.json after
  // 5 cycles). Exactly one source of indentation is kept per branch below —
  // consuming both, or neither, doubles or loses the indent.
  const prefix = text.slice(0, removeFrom);
  if (after.char === ",") {
    // Not the last member: drop the entry, the comma that followed it, and the
    // next member's line break + indent. The prefix still carries the removed
    // member's own indent, so the layout under the map is unchanged.
    const tail = text.slice(after.index + 1);
    const m = tail.match(/^\r?\n[ \t]*/);
    return prefix + tail.slice(m ? m[0].length : 0);
  }
  const prev = prevSignificant(text, removeFrom);
  if (prev.char === ",") {
    // Last member: also drop the comma that preceded it.
    return text.slice(0, prev.index) + text.slice(removeTo);
  }
  // Only member: the prefix's trailing indent belonged to the removed line, so
  // it goes with it and the map's closing brace keeps its own indent. The map
  // stays on one line when it was written that way.
  const tail = text.slice(removeTo);
  const m = tail.match(/^\r?\n/);
  return prefix.replace(/[ \t]+$/, "") + tail.slice(m ? m[0].length : 0);
}

// ---- hook command construction (hermes) -------------------------------

function hookCommand(eventName, client = null) {
  // Cross-platform: invoke `node` from PATH as a bare command name so the line
  // parses under any shell (bash for Claude Code/workbuddy, PowerShell for
  // trae-cn). Quote the entry path only when it contains spaces — otherwise
  // leave it bare. Note for hermes/YAML: JSON.stringify escapes the quotes
  // correctly for the YAML scalar, and keeping the path bare (no manual
  // wrapping) avoids the window path/backslash corruption documented below.
  // `client` selects that client's installed copy (see entryPathFor).
  const entry = entryPathFor(client);
  const core = /\s/.test(entry) ? `"${entry}"` : entry;
  const base = `node ${core} hook`;
  return eventName ? `${base} --event ${eventName}` : base;
}

// ---- MCP workled server cleanup (uninstall) ---------------------------------

// YAML top-level keys that may hold an MCP server map. hermes versioned its
// config key over time, so each candidate is probed in order (the first block
// that exists wins). Only used for YAML configs; JSON configs use the client's mcpKey.
const MCP_KEY_CANDIDATES = ["mcp_servers", "mcpServers", "mcp-servers", "servers"];

// Remove the `workled` server from a YAML MCP block in <file>. Candidates are
// probed via splitTopLevelBlock(); the first one present is edited in place.
// Server keys are detected by the block's indentation, so only the `workled`
// server (and its indented body) is dropped; every other server is preserved
// verbatim. If the whole block becomes empty the top-level section is dropped,
// and if the file ends up empty it is deleted. Returns a message or null when
// nothing was removed.
function removeMcpServerYaml(file, keyCandidates) {
  if (!existsSync(file)) return null;
  let content = readFileSync(file, "utf8");
  for (const key of keyCandidates) {
    const split = splitTopLevelBlock(content, key);
    if (!split) continue;
    const lines = content.split("\n");
    const blockLines = lines.slice(split.start, split.end);
    // Detect the indent used for server keys inside this block (e.g. 2
    // spaces, 4 spaces). Server keys live at the deepest level under the
    // top-level block, so we look for any indented block-start mapping.
    // Uses isBlockStartKey so inline values (`url: "...":` even with a
    // colon in the URL string), anchors (`&ref`), aliases (`*ref`), and
    // flow syntax (`{...}` / `[...]`) are not mistaken for a new block key.
    let serverIndent = null;
    for (const line of blockLines) {
      if (!isBlockStartKey(line)) continue;
      const m = line.match(/^(\s+)/);
      if (m) {
        serverIndent = m[1];
        break;
      }
    }
    if (!serverIndent) continue; // no servers defined
    // Walk the block, drop ONLY the workled server (and its indented body),
    // preserve every other server verbatim.
    const out = [];
    let skipping = false;
    const curIndentLen = serverIndent.length;
    for (const line of blockLines) {
      const blockStarter = isBlockStartKey(line);
      const indentMatch = line.match(/^(\s+)/);
      const lineIndentLen = indentMatch ? indentMatch[1].length : 0;
      if (blockStarter && lineIndentLen === curIndentLen) {
        const nameMatch = line.match(/^\s*([A-Za-z_][A-Za-z0-9_.\-:]*):/);
        const name = nameMatch ? nameMatch[1] : null;
        if (name === "workled") {
          skipping = true;
          continue;
        } else {
          skipping = false;
          out.push(line);
          continue;
        }
      }
      // Indented continuation: skip if we're inside the workled block.
      if (skipping && /^\s+\S/.test(line)) continue;
      out.push(line);
    }
    const before = lines.slice(0, split.start);
    const after = lines.slice(split.end);
    const mcpBlock = out.join("\n").replace(/\n{3,}/g, "\n\n").trimEnd();
    // If the MCP block becomes empty, drop the whole top-level section.
    if (mcpBlock === "" || mcpBlock === `${key}:`) {
      const merged = [...before, ...after].join("\n").replace(/\n{3,}/g, "\n\n").trimEnd();
      content = merged ? merged + "\n" : "";
      if (content.trim() === "") {
        removePath(file);
        removeEmptyParent(dirname(file));
        return `Removed empty hermes config.yaml -> ${file}`;
      }
      writeFileSync(file, content, "utf8");
      return `Removed empty ${key} block`;
    }
    content = [...before, `${key}:`, mcpBlock.replace(new RegExp(`^${key}:\\s*\\n`), ""), ...after]
      .join("\n")
      .replace(/\n{3,}/g, "\n\n");
    writeFileSync(file, content, "utf8");
    return `Removed workled from ${key}`;
  }
  return null;
}

// Remove the `workled` MCP server entry from one client's MCP config.
// JSON sources: drop obj[key].workled, then the key itself when
// empty; the config is rewritten in place via writeConfig (no backup file is
// created). YAML sources (hermes) go through removeMcpServerYaml(), which
// probes the historical MCP key candidates.
// Returns null when nothing was touched.
function removeMcpServer(client) {
  const t = CLIENT_TARGETS[client];
  if (!t?.mcpPath) return null;
  const file = t.mcpPath();
  const key = t.mcpKey;
  const format = t.mcpFormat;
  if (format === "yaml") {
    const candidates = [key, ...MCP_KEY_CANDIDATES.filter((k) => k !== key)];
    return removeMcpServerYaml(file, candidates);
  }
  // Nested-container client (openclaw): remove workled from the nested map via
  // a clean object round-trip, then prune any emptied container segments.
  if (t.mcpNestedPath) {
    return removeMcpServerNested(client, t);
  }
  if (!existsSync(file)) return null;
  const raw = readFileSync(file, "utf8");
  if (!isValidJsonc(raw)) return null;
  let edited = removeJsoncEntry(raw, key, "workled");
  if (edited == null) return null; // no workled entry here
  // Drop the map too when uninstall emptied it (replaces the old `delete obj[key]`).
  const dropped = removeJsoncKey(edited, key);
  if (dropped != null) edited = dropped;
  // Safety net: if surgery produced an unparseable file, leave it untouched.
  if (!isValidJsonc(edited)) return null;
  writeFileSync(file, edited, "utf8");
  // If the file is now effectively empty `{}`, delete it entirely.
  // This prevents file litter and blank-line accumulation on re-install.
  if (existsSync(file)) {
    const finalRaw = readFileSync(file, "utf8");
    if (stripJsonc(finalRaw).replace(/\s/g, "") === "{}") {
      removePath(file);
      removeEmptyParent(dirname(file));
      return `Removed workled from ${key} -> ${file} (deleted empty config)`;
    }
  }
  return `Removed workled from ${key} -> ${file}`;
}

// Remove the `workled` server from a nested-container client (openclaw) and
// prune empty container segments (e.g. mcp.servers, then mcp) so uninstall
// leaves no `{}` shells behind. Object round-trip on clean JSON. Returns null
// when no workled entry existed.
function removeMcpServerNested(client, t) {
  const file = t.mcpPath();
  if (!existsSync(file)) return null;
  let obj;
  try {
    obj = JSON.parse(stripJsonc(readFileSync(file, "utf8")));
  } catch {
    return null;
  }
  if (!obj || typeof obj !== "object") return null;
  // Walk to the server map; any missing segment means no workled entry.
  let map = obj;
  for (const seg of t.mcpNestedPath) {
    if (!map[seg] || typeof map[seg] !== "object") return null;
    map = map[seg];
  }
  if (!map.workled) return null;
  delete map.workled;
  // Prune emptied container segments bottom-up: once a level's map is empty,
  // drop that key from its parent and move up. Stop at the first level that
  // still holds entries — nothing above it can have been emptied by us.
  const segs = [...t.mcpNestedPath];
  for (let i = segs.length - 1; i >= 0; i--) {
    let holder = obj; // object that directly owns segs[i]
    for (let k = 0; k < i; k++) holder = holder[segs[k]];
    const child = holder[segs[i]];
    if (child && typeof child === "object" && Object.keys(child).length === 0) {
      delete holder[segs[i]];
    } else {
      break;
    }
  }
  writeConfig(file, obj);
  return `Removed workled from ${t.mcpNestedPath.join(".")} -> ${file}`;
}

// Remove a top-level <key> entry (the whole `"key": {...}`) from raw JSONC
// text, fixing the surrounding comma. Returns the edited text, or null when the
// key is absent. Only used to drop an emptied map left behind by uninstall.
export function removeJsoncKey(text, key) {
  const span = findTopLevelObjectValueSpan(text, key);
  if (!span) return null;
  const inner = text.slice(span.start + 1, span.end);
  if (stripJsonc(inner).trim() !== "") return null; // refuse to drop a populated map
  const needle = `"${key}"`;
  const keyAt = text.lastIndexOf(needle, span.start - 1);
  if (keyAt < 0) return null;
  const sep = text.slice(keyAt + needle.length, span.start);
  if (!/^\s*:\s*$/.test(sep)) return null;

  const after = nextSignificant(text, span.end + 1);
  let start = keyAt;
  let end = span.end + 1;
  if (after.char === ",") {
    end = after.index + 1;
  } else {
    const before = prevSignificant(text, keyAt);
    if (before.char === ",") start = before.index;
  }
  return text.slice(0, start) + text.slice(end);
}

// Remove the `workled` MCP server entry from every config source of one client.
// Returns the list of removal messages produced by
// unregisterWorkledMcp(client) via removeMcpServer() (null results filtered
// out); an empty array means no `workled` MCP server entry was found to remove.
function unregisterWorkledMcp(client) {
  const t = CLIENT_TARGETS[client];
  if (!t?.mcpPath) return [];
  const msg = removeMcpServer(client);
  return msg ? [msg] : [];
}

// Resolve the workled MCP server URL, in priority order:
//   1. WORKLED_MCP_URL        (explicit configuration wins)
//   2. placeholder            (http://<device-name>.local:18791/mcp, user must replace)
// There is intentionally no Bluetooth scan and no hard-coded specific host
// (e.g. HomeAnt-2831.local): the user supplies the real device name either via
// WORKLED_MCP_URL or by replacing the placeholder before connecting.
async function resolveWorkledMcpUrl() {
  if (process.env.WORKLED_MCP_URL) return process.env.WORKLED_MCP_URL;
  // No explicit URL: emit a placeholder the user must replace with their real
  // workled device name before connecting.
  return "http://<device-name>.local:18791/mcp";
}

// ---- WorkBuddy user-level hooks (settings.json) ----------------------------
// WorkBuddy loads hooks from ~/.workbuddy/settings.json (a Claude Code-compatible
// `hooks` field), NOT from the skill directory. These fire automatically on each
// lifecycle event — independent of agent discipline — so the workled LED tracks
// state reliably across new sessions without re-reminding the agent.
export function workledHookCommand(eventName, client, url) {
  // Cross-platform hook command. We intentionally invoke `node` from PATH (a
  // bare command name with no spaces) rather than the absolute process.execPath
  // ("C:\Program Files\nodejs\node.exe" on Windows). This single form parses
  // equally under a POSIX shell (Claude Code / workbuddy run hooks via bash)
  // and Windows PowerShell (trae-cn): a spaced "quoted path first" token is a
  // parse error in PowerShell (needs the `&` call operator) yet the same string
  // would run `&` as a background operator in bash — so absolute-node forms
  // can never satisfy both. Only the entry path is quoted, and only when it has
  // spaces, so the command stays valid on every shell. The path is this
  // client's own installed copy (entryPathFor), not the source checkout.
  const entry = entryPathFor(client);
  const core = /\s/.test(entry) ? `"${entry}"` : entry;
  let cmd = `node ${core} hook --event ${eventName} --client ${client}`;
  // The hook discovers the MCP URL at runtime from its own configuration
  // (mcp.json / WORKLED_MCP_URL), so no --url is inlined here. This keeps the
  // command stable across installs and avoids any shell/sandbox mangling of the
  // URL argument. The `url` parameter is accepted for call compatibility but is
  // intentionally unused by the generated command.
  return cmd;
}

// Each lifecycle event the workled hook should fire on. `matcher` (only for
// PreToolUse/PostToolUse/Notification) restricts the hook so it does NOT run on
// every tool call — a bare PreToolUse hook would spawn a ~3.6s process per
// Bash/Read/Write and stall the agent.
//
// AskUserQuestion timing (WorkBuddy/CodeBuddy, verified in index.js): the host
// fires PreToolUse AND PostToolUse for AskUserQuestion at the correct moments
// — the earlier "only-on-answer" behavior no longer reproduces. So the
// PreToolUse matcher below lights "waiting" as the question is shown and the
// PostToolUse matcher returns the LED to "thinking" once the user answers; no
// agent-side set_agent_state call is required for a plain question.
// Notification is the render-time signal for approval dialogs:
// permission_prompt fires when a tool approval dialog is SHOWN -> waiting;
// idle_prompt fires after ~60s of session idle -> idle (fallback if Stop did
// not fire).
const WORKLED_HOOK_SPECS = [
  { event: "UserPromptSubmit", matcher: null },
  { event: "Stop", matcher: null },
  { event: "Notification", matcher: "permission_prompt" },
  { event: "Notification", matcher: "idle_prompt" },
  // PreToolUse maps to "tool" (HOOK_MAP): restricted to AskUserQuestion it
  // lights "waiting" as the question is rendered, without spawning a process
  // on every other tool call.
  { event: "PreToolUse", matcher: "AskUserQuestion" },
  // PostToolUse maps to "thinking" (HOOK_MAP) so answering an AskUserQuestion
  // returns the LED to the working state; it fires when the user answers.
  { event: "PostToolUse", matcher: "AskUserQuestion" },
];

// Generic, disk-backed hook installer shared by the hook-driven clients
// (workbuddy: ~/.workbuddy/settings.json, trae-cn: <home>/.trae-cn/hooks.json).
// The client marker drives both the generated `--client` command and group
// matching via the shared merge core, so no path/client is hard-coded here.
function installWorkledHooks(hooksFile, { client, version, url }) {
  const parsed = readJsonOrEmpty(hooksFile);
  // Never overwrite a config that exists but cannot be parsed: the user's
  // other hooks/settings would be lost. Warn and bail out instead.
  if (parsed === null && existsSync(hooksFile)) {
    console.warn(`SKIPPED writing hooks: ${hooksFile} is unreadable, not modified`);
    return `SKIPPED workled hooks -> ${hooksFile} (unreadable, not modified)`;
  }
  const merged = mergeClientHooks(parsed || {}, {
    client,
    commandForEvent: (ev) => workledHookCommand(ev, client, url),
    version,
  });
  writeConfig(hooksFile, merged);
  return `Installed workled hooks -> ${hooksFile}`;
}

// Generic uninstaller that mirrors installWorkledHooks. `allowDeleteFile` lets
// a dedicated hooks file (trae-cn) holding nothing but the schema `version` be
// deleted entirely so uninstall leaves nothing behind; it is false for a
// settings file (workbuddy) that may carry unrelated user settings.
function uninstallWorkledHooks(hooksFile, { client, allowDeleteFile }) {
  const cfg = readJsonOrEmpty(hooksFile);
  if (!cfg || !cfg.hooks) return `No workled hooks at ${hooksFile}`;
  const { config: stripped, changed } = stripClientHooks(cfg, client);
  if (!changed) return `No workled hooks at ${hooksFile}`;
  if (stripped.hooks && Object.keys(stripped.hooks).length === 0) delete stripped.hooks;
  if (allowDeleteFile && Object.keys(stripped).filter((k) => k !== "version").length === 0) {
    if (existsSync(hooksFile)) removePath(hooksFile);
    removeEmptyParent(dirname(hooksFile));
    return `Removed workled hooks -> ${hooksFile} (deleted empty config)`;
  }
  writeConfig(hooksFile, stripped);
  return `Removed workled hooks -> ${hooksFile}`;
}

// Group the workled hook specs by event, preserving spec order within each
// event. Grouping BEFORE filtering keeps multiple matchers under one event
// (e.g. the two Notification specs) from dropping each other.
function groupWorkledSpecs() {
  const byEvent = new Map();
  for (const spec of WORKLED_HOOK_SPECS) {
    if (!byEvent.has(spec.event)) byEvent.set(spec.event, []);
    byEvent.get(spec.event).push(spec);
  }
  return byEvent;
}

// Pure: detect a hook group that belongs to workled for a specific client,
// matched safely on the client-scoped command (e.g. `--client trae-cn` or
// `--client workbuddy`). This single predicate is shared by every client.
function isClientWorkledGroup(group, client) {
  const marker = `--client ${client}`;
  return (
    group &&
    Array.isArray(group.hooks) &&
    group.hooks.some(
      (hk) =>
        hk &&
        typeof hk.command === "string" &&
        hk.command.includes("workled") &&
        hk.command.includes(marker)
    )
  );
}

// Pure (testable without touching disk): return a NEW hooks config with the
// workled hook groups for `client` upserted. Any prior workled group for the
// same client/event is replaced first, unrelated hooks are preserved. A schema
// `version` is only injected when provided (trae-cn uses 1; workbuddy does not).
export function mergeClientHooks(cfg, { client, commandForEvent, version }) {
  const out = { ...(cfg || {}) };
  if (typeof version === "number" && typeof out.version !== "number") out.version = version;
  if (!out.hooks || typeof out.hooks !== "object") out.hooks = {};
  for (const [ev, specs] of groupWorkledSpecs()) {
    if (!Array.isArray(out.hooks[ev])) out.hooks[ev] = [];
    out.hooks[ev] = out.hooks[ev].filter((group) => !isClientWorkledGroup(group, client));
    for (const spec of specs) {
      const group = {
        hooks: [
          {
            type: "command",
            command: commandForEvent(ev),
            // Host-side watchdog cap, in seconds. It governs exactly one event:
            // Stop, which declares no `async` so the host waits for the process
            // to exit (that is what keeps it alive across the turn-end worker
            // recycle — a detached child is inside the same job object and dies
            // with it). The other four events declare `{async:true,
            // asyncTimeout:12000}` and are released ~250ms in, so this cap only
            // covers the pre-declaration stretch for them.
            // Budget for the sync path: node startup + one .local mDNS resolve +
            // one stateless POST, typically 1.2-1.5s, with a measured 5050ms
            // spike on a slow resolve. 10s covers the spike without letting a
            // genuinely wedged device stall the turn.
            timeout: 10,
          },
        ],
      };
      if (spec.matcher) group.matcher = spec.matcher;
      out.hooks[ev].push(group);
    }
  }
  return out;
}

// Pure: return a NEW hooks config with only the workled hook groups for
// `client` removed, plus a `changed` flag. Unrelated hooks are preserved.
export function stripClientHooks(cfg, client) {
  const out = { ...(cfg || {}) };
  if (!out.hooks || typeof out.hooks !== "object") return { config: out, changed: false };
  const hooks = {};
  let changed = false;
  for (const ev of Object.keys(out.hooks)) {
    if (!Array.isArray(out.hooks[ev])) {
      hooks[ev] = out.hooks[ev];
      continue;
    }
    const kept = out.hooks[ev].filter((group) => !isClientWorkledGroup(group, client));
    if (kept.length !== out.hooks[ev].length) changed = true;
    if (kept.length) hooks[ev] = kept;
  }
  out.hooks = hooks;
  return { config: out, changed };
}

// --- Per-client install/uninstall (hook-driven clients) ---------------------
// These aggregate every file/setting a single client needs, so the client
// dispatch in install()/uninstall() reads as a plain per-client switch. The
// generic installWorkledHooks/uninstallWorkledHooks below are the shared
// implementation; only the target file, client marker and version differ.

// WorkBuddy: MCP server + lifecycle hooks, both written automatically.
async function installWorkbuddy(mcpEntry) {
  const lines = [];
  lines.push(...(await registerWorkledMcp("workbuddy", mcpEntry)));
  lines.push(installWorkledHooks(joinP(h, ".workbuddy", "settings.json"), { client: "workbuddy", url: mcpEntry && mcpEntry.url }));
  return lines;
}

async function uninstallWorkbuddy() {
  const lines = [];
  lines.push(...unregisterWorkledMcp("workbuddy"));
  lines.push(uninstallWorkledHooks(joinP(h, ".workbuddy", "settings.json"), { client: "workbuddy" }));
  return lines;
}

// trae-cn (VSCode fork) reads a GLOBAL MCP config at <user-data>/User/mcp.json
// (the VSCode convention it inherits) for servers shared by every workspace, so
// the workled MCP server is written there directly. Its lifecycle hooks go to
// <home>/.trae-cn/hooks.json using the Claude Code-style schema (version 1 +
// hooks.<Event>[]). Both are therefore wired automatically on install.
function installTraeCn(mcpEntry) {
  return [
    ...registerWorkledMcp("trae-cn", mcpEntry),
    installWorkledHooks(joinP(traeCnHooksHome(), "hooks.json"), { client: "trae-cn", version: 1, url: mcpEntry && mcpEntry.url }),
  ];
}

function uninstallTraeCn() {
  return [
    ...unregisterWorkledMcp("trae-cn"),
    uninstallWorkledHooks(joinP(traeCnHooksHome(), "hooks.json"), { client: "trae-cn", allowDeleteFile: true }),
  ];
}

// Inverse of removeMcpServer: write the `workled` server entry into one
// client's MCP config (JSON or YAML). For JSON, an existing `type` is
// preserved and a fresh entry is written with the client's default `type`
// (see CLIENT_TARGETS.mcpType), so clients that require an explicit transport
// declaration (opencode/kilo/workbuddy use "remote") never get a bare
// `{ url, enabled }` entry that the client would ignore.
function addMcpServer(client, entry) {
  const t = CLIENT_TARGETS[client];
  if (!t?.mcpPath) return null;
  const file = t.mcpPath();
  const key = t.mcpKey;
  const format = t.mcpFormat;
  const defaultType = t.mcpType;
  if (format === "yaml") {
    // Pass `t` through: addMcpServerYaml reads t.mcpTimeoutSeconds /
    // t.mcpConnectTimeoutSeconds to emit hermes' `timeout` / `connect_timeout`.
    // Omitting it silently produced a workled entry with no timeout fields.
    return addMcpServerYaml(file, key, "workled", entry, t);
  }
  // Nested-container client (e.g. openclaw: server map lives at mcp.servers and
  // a remote server declares `transport` rather than `type`). Such files are
  // clean JSON, so a plain object round-trip is safe and far simpler than the
  // top-level JSONC surgery used below.
  if (t.mcpNestedPath) {
    return addMcpServerNested(client, t, entry);
  }
  // A corrupt existing config must never be flattened to {} and written back,
  // or the user's other servers would be lost. Skip the source with a warning
  // instead; a missing file still falls through to creating a fresh entry.
  const raw = existsSync(file) ? readFileSync(file, "utf8") : null;
  if (raw != null && !isValidJsonc(raw)) {
    return `SKIPPED workled -> ${key} (${file}): config file unreadable, not modified`;
  }
  const obj = raw == null ? {} : JSON.parse(stripJsonc(raw));
  const map =
    obj[key] && typeof obj[key] === "object"
      ? obj[key]
      : (obj[key] = {});
  const existing = map.workled && typeof map.workled === "object" ? map.workled : {};
  // Never downgrade a working URL to the <device-name> placeholder: if the new
  // entry carries the placeholder but an existing real URL is present, keep the
  // real one. This guards `install` runs where WORKLED_MCP_URL / Bluetooth are
  // unavailable (placeholder path) yet a valid config already exists.
  const url = resolveMergedUrl(existing.url, entry.url);
  const desired = { url, enabled: entry.enabled !== false };
  // Per-client request timeout on the server entry: opencode/kilo take a
  // `timeout` (ms); trae-cn reads HTTP headers set by its client. workbuddy
  // intentionally declares none: its client clamps config timeouts to a 60s
  // floor, so the field would be a no-op.
  if (t.mcpTimeoutMs) desired.timeout = t.mcpTimeoutMs;
  if (t.mcpHeaderTimeoutMs) {
    desired.headers = {
      ...(existing.headers || {}),
      START_MCP_TIMEOUT_MS: String(t.mcpHeaderTimeoutMs),
      RUN_MCP_TIMEOUT_MS: String(t.mcpHeaderTimeoutMs),
    };
  }
  // Existing type wins; otherwise fall back to the client's default so fresh
  // installs carry the transport declaration their client requires.
  const type = resolveMcpType(existing.type, defaultType);
  if (type) desired.type = type;

  if (raw == null) {
    // No file yet: create a minimal one with just the workled server.
    map.workled = desired;
    writeConfig(file, { [key]: map });
    return `Registered workled -> ${key} (${file})`;
  }

  // No-op fast path: the entry already matches. Do not rewrite the file — this
  // keeps user comments and formatting untouched across repeated installs.
  const same =
    existing.url === desired.url &&
    (existing.enabled === undefined ? true : existing.enabled) === desired.enabled &&
    (existing.type || null) === (desired.type || null) &&
    (existing.timeout ?? null) === (desired.timeout ?? null) &&
    (existing.headers?.START_MCP_TIMEOUT_MS ?? null) === (desired.headers?.START_MCP_TIMEOUT_MS ?? null);
  if (same) {
    return `Registered workled -> ${key} (${file}) (unchanged)`;
  }

  // Preferred path: byte-level surgery that preserves user comments, key
  // order, and formatting. Falls back to a full JSON.stringify rewrite only if
  // the layout defeats the editor (the file was already validated as parseable,
  // so the rewrite loses nothing but comments/formatting).
  const edited = upsertJsoncEntry(raw, key, "workled", desired);
  if (edited != null && isValidJsonc(edited)) {
    writeFileSync(file, edited, "utf8");
    return `Registered workled -> ${key} (${file})`;
  }
  map.workled = desired;
  writeConfig(file, obj);
  return `Registered workled -> ${key} (${file})`;
}

// Write/update the `workled` server inside a client whose server map lives at
// a nested path (CLIENT_TARGETS.mcpNestedPath), e.g. openclaw -> mcp.servers.
// A remote server there uses `transport` (default streamable-http), not `type`.
// The container file is clean JSON, so we round-trip the whole object.
function addMcpServerNested(client, t, entry) {
  const file = t.mcpPath();
  const label = t.mcpNestedPath.join(".");
  let obj = {};
  if (existsSync(file)) {
    try {
      obj = JSON.parse(stripJsonc(readFileSync(file, "utf8")));
    } catch {
      return `SKIPPED workled -> ${label} (${file}): config file unreadable, not modified`;
    }
    if (!obj || typeof obj !== "object") obj = {};
  }
  // Walk down / create the container path; the last segment is the server map.
  let map = obj;
  for (const seg of t.mcpNestedPath) {
    if (!map[seg] || typeof map[seg] !== "object") map[seg] = {};
    map = map[seg];
  }
  const existing = map.workled && typeof map.workled === "object" ? map.workled : {};
  const url = resolveMergedUrl(existing.url, entry.url);
  const transport = t.mcpTransport || "streamable-http";
  const desired = {
    // Start from the existing entry so any field the user added by hand
    // (headers, auth, ...) survives a re-install; building the object from
    // scratch used to drop everything outside url/enabled/transport.
    ...existing,
    url,
    enabled: entry.enabled !== false,
    transport: existing.transport || transport,
  };
  if (t.mcpRequestTimeoutMs) {
    desired.requestTimeoutMs = t.mcpRequestTimeoutMs;
  }
  const same =
    existing.url === desired.url &&
    (existing.enabled === undefined ? true : existing.enabled) === desired.enabled &&
    (existing.transport || null) === desired.transport &&
    (existing.requestTimeoutMs || null) === (desired.requestTimeoutMs || null);
  if (same) {
    return `Registered workled -> ${label}.workled (${file}) (unchanged)`;
  }
  map.workled = desired;
  writeConfig(file, obj);
  return `Registered workled -> ${label}.workled (${file})`;
}

// Add (or replace) a `workled` server under a YAML top-level MCP block
// (`mcp_servers:` or an aliased key). Preserves every other server and the
// block's indentation.
function addMcpServerYaml(file, key, serverName, entry, t) {
  if (!existsSync(file)) return null;
  let content = readFileSync(file, "utf8");
  const split = splitTopLevelBlock(content, key);
  const serverLines = [
    `  ${serverName}:`,
    `    url: ${JSON.stringify(entry.url)}`,
    `    enabled: true`,
  ];
  // hermes: tool-call and connect/tool-list trends are separate seconds fields.
  if (t?.mcpTimeoutSeconds) serverLines.push(`    timeout: ${t.mcpTimeoutSeconds}`);
  if (t?.mcpConnectTimeoutSeconds) serverLines.push(`    connect_timeout: ${t.mcpConnectTimeoutSeconds}`);
  if (!split) {
    const trimmed = content.trimEnd();
    content = (trimmed ? trimmed + "\n" : "") + `${key}:\n` + serverLines.join("\n") + "\n";
    writeFileSync(file, content, "utf8");
    return `Registered workled -> ${key} (${file})`;
  }
  const lines = content.split("\n");
  const blockLines = lines.slice(split.start, split.end);
  let sIndent = "  ";
  for (const l of blockLines) {
    if (!isBlockStartKey(l)) continue;
    const m = l.match(/^(\s+)/);
    if (m) {
      sIndent = m[1];
      break;
    }
  }
  const out = [];
  let skipping = false;
  const targetIndentLen = sIndent.length;
  for (const l of blockLines) {
    const blockStarter = isBlockStartKey(l);
    const indentMatch = l.match(/^(\s+)/);
    const lineIndentLen = indentMatch ? indentMatch[1].length : 0;
    if (blockStarter && lineIndentLen === targetIndentLen) {
      const nameMatch = l.match(/^\s*([A-Za-z_][A-Za-z0-9_.\-:]*):/);
      const name = nameMatch ? nameMatch[1] : null;
      if (name === serverName) {
        skipping = true;
        continue;
      }
      skipping = false;
      out.push(l);
      continue;
    }
    if (skipping && /^\s+\S/.test(l)) continue;
    out.push(l);
  }
  out.push(`${sIndent}${serverName}:`);
  out.push(`${sIndent}  url: ${JSON.stringify(entry.url)}`);
  out.push(`${sIndent}  enabled: true`);
  if (t?.mcpTimeoutSeconds) out.push(`${sIndent}  timeout: ${t.mcpTimeoutSeconds}`);
  if (t?.mcpConnectTimeoutSeconds) out.push(`${sIndent}  connect_timeout: ${t.mcpConnectTimeoutSeconds}`);
  const before = lines.slice(0, split.start);
  const after = lines.slice(split.end);
  content = [...before, ...out, ...after].join("\n").replace(/\n{3,}/g, "\n\n");
  writeFileSync(file, content, "utf8");
  return `Registered workled -> ${key} (${file})`;
}

// Register the workled MCP server for one client across its config
// sources (deduped by path). Mirrors unregisterWorkledMcp so install and
// uninstall stay symmetric and every client's logic is identical.
function registerWorkledMcp(client, entry) {
  const t = CLIENT_TARGETS[client];
  if (!t?.mcpPath) return [];
  const msg = addMcpServer(client, entry);
  return msg ? [msg] : [];
}

// ---- per-client install/uninstall -------------------------------------------
// openclaw: the Gateway loads standalone plugin files listed in
// ~/.openclaw/openclaw.json `plugins.load.paths`. Each plugin needs a sibling
// `openclaw.plugin.json` manifest (id + configSchema, validated cold), and the
// entry must be enabled under `plugins.entries.<id>` with conversation-hook
// access granted for the agent_end hook.
const OPENCLAW_PLUGIN_MANIFEST = {
  id: "workled",
  name: "workled",
  description:
    "Maps OpenClaw agent lifecycle events (thinking/idle/waiting/error) to the workled MCP set_agent_state tool driving the LED strip.",
  version: SKILL_VERSION,
  activation: { onStartup: true, onCapabilities: ["hook"] },
  configSchema: { type: "object", additionalProperties: false, properties: {} },
};

function openclawConfigPath() {
  return joinP(h, ".openclaw", "openclaw.json");
}

function openclawPluginDir() {
  return joinP(h, ".openclaw", "plugins");
}

// Parse openclaw.json text. Exported for unit tests.
//   object -> the config
//   null   -> present, but not a parseable config object
// openclaw itself reads this file with JSON5, so user comments and trailing
// commas are legal; JSONC stripping covers the comment/trailing-comma subset
// and anything beyond it must be reported, never coerced to an empty object.
// Arrays and scalars count as "not a config": the caller merges `plugins` into
// the result and writes it back, which an array would silently drop.
export function parseOpenclawConfigText(text) {
  try {
    const parsed = JSON.parse(stripJsonc(text));
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

// Load ~/.openclaw/openclaw.json. Tri-state on purpose:
//   {}     -> file absent (a fresh config is safe to create)
//   object -> parsed config
//   null   -> file exists but is unparseable
// `null` must never be treated as "no workled entries": both install and
// uninstall write the object back WHOLE, so an empty fallback would replace the
// user's entire config (agents/models/... measured 346 lines on this machine)
// with a stub. Callers refuse to write instead - see skippedOpenclawConfig().
function readOpenclawConfig() {
  const p = openclawConfigPath();
  if (!existsSync(p)) return {};
  return parseOpenclawConfigText(readFileSync(p, "utf8"));
}

// The single "refused to touch it" message for openclaw.json, so install and
// uninstall report the same reason (mirrors addMcpServerNested's wording).
function skippedOpenclawConfig(file = openclawConfigPath()) {
  return `SKIPPED workled -> openclaw.json (${file}): config file unreadable, not modified`;
}

// openclaw install, manifest + config portion only. The entry file is written
// by the shared plugin-file path (see the generic loop in main()), which calls
// this after writing ~/.openclaw/plugins/workled/index.js. Path is single-
// sourced from CLIENT_TARGETS.openclaw.pluginPath().
async function installOpenclawManifest() {
  const dest = CLIENT_TARGETS.openclaw.pluginPath();
  const destDir = dirname(dest);

  // Read the config BEFORE writing anything. An unparseable file must be left
  // untouched (see readOpenclawConfig); bailing here also avoids leaving a
  // manifest for a plugin the config never references.
  const cfg = readOpenclawConfig();
  if (cfg === null) return skippedOpenclawConfig();

  // The entry file is already written by the caller; ensure the dir exists for
  // the manifest (idempotent on re-run).
  mkdirSync(destDir, { recursive: true });

  // Write plugin manifest (lives in the same plugin dir as the entry file)
  writeFileSync(
    joinP(destDir, "openclaw.plugin.json"),
    JSON.stringify(OPENCLAW_PLUGIN_MANIFEST, null, 2) + "\n",
    "utf8"
  );
  const entryPath = dest.replace(/\\/g, "/");
  const plugins = (cfg.plugins && typeof cfg.plugins === "object" ? cfg.plugins : {});
  const load = (plugins.load && typeof plugins.load === "object" ? plugins.load : {});
  const paths = Array.isArray(load.paths) ? load.paths : [];
  if (!paths.includes(entryPath)) paths.push(entryPath);
  plugins.load = { ...load, paths };
  const entries = (plugins.entries && typeof plugins.entries === "object" ? plugins.entries : {});
  entries.workled = {
    ...(entries.workled && typeof entries.workled === "object" ? entries.workled : {}),
    enabled: true,
    hooks: { allowConversationAccess: true },
  };
  plugins.entries = entries;
  cfg.plugins = plugins;
  // cfg already carries every existing section from readOpenclawConfig(), so
  // write it whole — a merge round-trip would re-read the file and risk mixing
  // two snapshots while the Gateway watcher is reloading.
  writeConfig(openclawConfigPath(), cfg);

  // Wait for Gateway to finish reloading and verify the config persisted.
  // Gateway's file watcher triggers a restart when plugins.load changes.
  // On Windows, filesystem commits can be asynchronous, so the Gateway may
  // read a stale/incomplete file and roll back to .bak. We poll until the
  // config stabilises or we give up.
  const configPath = openclawConfigPath();
  let verified = false;
  for (let i = 0; i < 6; i++) {
    await sleep(1000);
    // `?? {}` only covers a file that turned unreadable mid-verify: it simply
    // counts as "not verified yet" and the !verified branch below handles it.
    const check = readOpenclawConfig() ?? {};
    const pathsOk = Array.isArray(check.plugins?.load?.paths) &&
      check.plugins.load.paths.some(p => String(p).includes("workled"));
    const entryOk = !!(check.plugins?.entries?.workled?.enabled);
    const dirOk = existsSync(dest);
    if (pathsOk && entryOk && dirOk) {
      verified = true;
      break;
    }
  }

  if (!verified) {
    // Config didn't stabilise — write it one more time directly (no merge)
    // to bypass any rollback edge-case with empty existing plugins.
    const cfg2 = readOpenclawConfig();
    if (cfg2 === null) return skippedOpenclawConfig(configPath);
    cfg2.plugins = { ...cfg.plugins };
    writeConfig(configPath, cfg2);
    // Verify again
    await sleep(2000);
    const final = readOpenclawConfig() ?? {};
    if (!final.plugins?.entries?.workled) {
      return `Installed openclaw manifest -> ${destDir}\n⚠ Config update may have been rolled back by Gateway restart. Run the install again or restart the Gateway manually.`;
    }
  }

  return `Installed openclaw manifest + config -> ${destDir}\nRegistered in openclaw.json plugins.load.paths and plugins.entries.workled (restart the Gateway to load)`;
}

// Strip every workled entry from an openclaw config object, returning the
// cleaned copy, whether anything changed, and the messages describing it.
// Shared by uninstallOpenclaw's main cleanup and its rollback recovery path.
function stripWorkledFromOpenclawConfig(cfg) {
  const out = { cfg: { ...cfg }, changed: false, messages: [] };
  if (out.cfg && out.cfg.plugins) {
    const plugins = out.cfg.plugins;
    if (plugins.load && Array.isArray(plugins.load.paths)) {
      const filtered = plugins.load.paths.filter((p) => !String(p).includes("workled"));
      if (filtered.length !== plugins.load.paths.length) {
        plugins.load.paths = filtered;
        if (filtered.length === 0) delete plugins.load;
        out.changed = true;
        out.messages.push(`Unregistered workled from openclaw.json plugins.load.paths`);
      }
    }
    if (plugins.entries && plugins.entries.workled) {
      delete plugins.entries.workled;
      if (Object.keys(plugins.entries).length === 0) delete plugins.entries;
      out.changed = true;
      out.messages.push(`Unregistered workled from openclaw.json plugins.entries`);
    }
    if (plugins.load && Object.keys(plugins.load).length === 0) delete plugins.load;
    if (plugins.entries && Object.keys(plugins.entries).length === 0) delete plugins.entries;
    if (Object.keys(plugins).length === 0) delete out.cfg.plugins;
  }
  return out;
}

async function uninstallOpenclaw() {
  const configPath = openclawConfigPath();
  // Refuse up front when the config cannot be parsed. The plugin dir and its
  // config entry are removed as a pair, and writing a stripped fallback object
  // would replace the user's whole config with a stub (see readOpenclawConfig).
  const current = readOpenclawConfig();
  if (current === null) return skippedOpenclawConfig(configPath);

  const destDir = joinP(openclawPluginDir(), "workled");
  let msg = "";
  if (existsSync(destDir)) {
    removePath(destDir, { recursive: true });
    removeEmptyParent(dirname(destDir));
    msg += `Removed openclaw plugin dir -> ${destDir}\n`;
  } else {
    msg += `No openclaw workled plugin dir at ${destDir}\n`;
  }

  // Always read the current config and remove workled entries, then write.
  // We must write unconditionally because the Gateway file watcher may have
  // already rolled back the config to .bak between our read and any write.
  let cleaned = stripWorkledFromOpenclawConfig(current);

  // Write the cleaned config via the shared helper (no merge round-trip, so
  // stale workled entries from a concurrently-modified file cannot resurface).
  writeConfig(configPath, cleaned.cfg);
  if (cleaned.changed) {
    msg += cleaned.messages.join("\n") + "\n";
    msg += `Updated openclaw.json -> ${configPath}\n`;
  }

  // Wait for Gateway to finish reloading, then verify the config is clean.
  // If Gateway rolled back (e.g. because it read an intermediate state),
  // rewrite the clean config one more time.
  for (let i = 0; i < 8; i++) {
    await sleep(1000);
    const check = readOpenclawConfig() ?? {};
    const hasWorkled = check.plugins?.load?.paths?.some(p => String(p).includes("workled"))
      || check.plugins?.entries?.workled;
    if (!hasWorkled) return msg.trimEnd() || `No openclaw workled plugin installed`;
  }

  // Gateway didn't stabilise — force-write clean config one final time. Skip the
  // write (but keep the report) if the file became unparseable in the meantime.
  const again = readOpenclawConfig();
  if (again !== null) {
    cleaned = stripWorkledFromOpenclawConfig(again);
    writeConfig(configPath, cleaned.cfg);
    msg += `Force-cleaned openclaw.json (Gateway rollback recovery)\n`;
  }
  return msg.trimEnd();
}

// ---- entry file generation ---------------------------------------------------

function fileUrl(p) {
  return pathToFileURL(p).href;
}

// Generated entry files share a fixed "do not edit" header and a trailing
// newline; each adapter only supplies its own import/export body lines.
const ENTRY_HEADER = "// Generated by workled install.mjs. Do not edit.";
function entryFile(lines) {
  return [ENTRY_HEADER, ...lines, ""].join("\n");
}

// Every generator takes the client name and imports that client's own
// installed copy (entryPathFor), so a generated plugin keeps working after the
// source checkout is moved or deleted.
//
// opencode: the plugins dir auto-loads EVERY exported function as a plugin, so
// the installed file exposes a single plugin function that adapts the entry's
// register() into opencode's factory shape.
// Dest (CLIENT_TARGETS.opencode.pluginPath()): ~/.config/opencode/plugins/workled.js
function opencodeEntryFile(client) {
  return entryFile([
    `import { opencodeEntry as core } from "${fileUrl(entryPathFor(client))}";`,
    `export const workled = async (ctx) => await core.register(ctx);`,
  ]);
}

// openclaw: Gateway loads via plugins.load.paths; wraps the entry with the SDK.
// Dest (CLIENT_TARGETS.openclaw.pluginPath()): ~/.openclaw/plugins/workled/index.js
function openclawEntryFile(client) {
  return entryFile([
    `import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";`,
    `import { openclawEntry } from "${fileUrl(entryPathFor(client))}";`,
    `export default definePluginEntry(openclawEntry);`,
  ]);
}

// pi: extensions take the default export as (pi: ExtensionAPI) => void.
// Dest (CLIENT_TARGETS.pi.pluginPath()): ~/.pi/agent/extensions/workled/index.ts
function piEntryFile(client) {
  return entryFile([
    `import { piEntry } from "${fileUrl(entryPathFor(client))}";`,
    `export default (pi) => piEntry.register(pi);`,
  ]);
}

// kilo (Anomaly) is an opencode fork: Event/Hooks types are identical to
// opencode, so it reuses opencodeEntry. The installed file is a module
// descriptor (default export { id, server }) in the single `plugin/` dir.
// Dest (CLIENT_TARGETS.kilo.pluginPath()): ~/.config/kilo/plugin/workled.js
function kiloEntryFile(client) {
  return entryFile([
    `import { opencodeEntry as core } from "${fileUrl(entryPathFor(client))}";`,
    `export default {`,
    `  id: "workled",`,
    `  server: async (ctx) => await core.register(ctx),`,
    `};`,
  ]);
}

// Entry-file generators for the plugin-file clients (opencode / kilo / pi /
// openclaw). Target paths and labels live in CLIENT_TARGETS (index.js); this
// table only adds what cannot be data — the generated entry content — so
// client paths are maintained in exactly one place. Keys must be a subset of
// CLIENTS. openclaw additionally needs a plugin manifest + openclaw.json
// registration, which is owned by installOpenclawManifest() (the entry file
// itself is written by the same generic loop as the other plugin clients).
const PLUGIN_CLIENTS = {
  opencode: opencodeEntryFile,
  kilo: kiloEntryFile,
  pi: piEntryFile,
  openclaw: openclawEntryFile,
};

// hermes: shell hooks are declared in <hermes-home>/config.yaml under a
// top-level `hooks:` block; each event maps to an array of { command,
// timeout? }. The config is YAML, so these helpers do a minimal top-level
// block edit that preserves any other top-level keys (model, terminal, ...)
// untouched. hermes home resolution mirrors hermes_constants.get_hermes_home:
//   $HERMES_HOME env var wins; otherwise Windows uses %LOCALAPPDATA%\hermes,
//   everything else uses ~/.hermes. Implemented once in utils.js.

export function hermesHookEvents() {
  return [
    "pre_llm_call",
    "post_llm_call",
    "pre_tool_call",
    "post_tool_call",
    "pre_approval_request",
    "post_approval_response",
    "on_session_start",
    "on_session_end",
    "subagent_start",
    "subagent_stop",
  ];
}

function hermesCommandYaml(ev, client = null) {
  // JSON.stringify produces valid YAML double-quoted scalar (backslashes/escaping).
  return JSON.stringify(hookCommand(ev, client));
}

// True when <line> is a YAML document boundary:
//   `---`  document start / explicit directives end
//   `...`  document end
// Anchors/comments/flow markers are not boundaries. Used to avoid straddling
// multi-doc YAML files (fixes #9 — previously a workled block in doc #1
// could be detected as spanning all the way down through subsequent docs).
function isYamlDocBoundary(line) {
  return /^---\s*(#.*)?$|^\.\.\.\s*(#.*)?$/.test(line.trim());
}
// True when a line that starts an indented mapping key (e.g. "  workled:") is
// actually a BLOCK start — i.e. the value lives on subsequent indented lines,
// NOT inline after the colon. The following inline forms must NOT be treated
// as block starts (fixes #9):
//   - anchors / aliases:   `  workled: &common` / `  workled: *ref`
//   - flow maps / lists:   `  workled: { a: 1 }` / `  workled: [1, 2]`
//   - plain scalars:       `  url: "http://..."` / `  enabled: true`
// Without this check, `url: "http://..."` lines whose quoted value contains
// a trailing `:` would falsely be detected as nested keys, collapsing the
// server body and leaving stale fields behind.
function isBlockStartKey(line) {
  const m = line.match(/^(\s*)([A-Za-z_][A-Za-z0-9_.\-:]*):(.*)$/);
  if (!m) return false;
  const rest = m[3].trim();
  // Drop a trailing YAML comment from the "rest" portion before checking.
  const stripped = rest.replace(/\s+#.*$/, "");
  if (stripped === "") return true; // key: EOL or key: # comment only
  // Inline value is present → NOT a block start. Any anchor/alias/flow
  // opener / plain scalar counts as inline.
  if (/^[&*?!>|%@`]/.test(stripped)) return false;
  if (/^[\[{"']/.test(stripped)) return false; // flow scalar
  if (/^\d/.test(stripped)) return false;      // number / timestamp
  return false; // any other non-empty tail (e.g. `enabled: true`) is inline
}
// Same as isBlockStartKey but for UNINDENTED top-level keys. Accepts a
// candidate key name so we also match `key: # end-of-line comment` as a
// valid block start. Used by splitTopLevelBlock to anchor the search.
function isTopLevelKeyStart(line, key) {
  const re = new RegExp(`^${key}:(.*)$`);
  const m = line.match(re);
  if (!m) return false;
  if (/^\s/.test(line)) return false; // top-level means line starts with the key
  const rest = m[1].trim().replace(/\s+#.*$/, "");
  if (rest === "") return true;
  // A value exists on the same line: not a block start.
  return false;
}

// Split a YAML document into a leading top-level block for a given key and the
// remainder, so the caller can replace just that key.
//
// YAML feature coverage (fixes #9):
//   * Multi-doc (`---` / `...` boundaries): block end detection stops at the
//     next top-level key OR next document boundary, whichever comes first.
//   * Anchors/aliases: `key: &anchor` at top level is not mistaken for a
//     block body; `*ref` values don't look like indented keys.
//   * Flow syntax (inline maps `{...}` and lists `[...]`): inline values are
//     not treated as nested keys, so values like `url: "http://x:y"` don't
//     confuse the indent-based server-key detector.
//
// Exported for unit tests so the three new YAML parsing invariants of #9 are
// independently assertable (no need to hit the filesystem install helpers).
export function splitTopLevelBlock(yamlText, key) {
  const lines = yamlText.split("\n");
  // If the file contains multiple documents, only search the FIRST one for
  // our key. Config.yaml is overwhelmingly a single-doc file, but when a
  // hand-edited file uses `---` we should not span docs.
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (isYamlDocBoundary(l) && start !== -1) {
      // Encountered a doc boundary AFTER locating our key — block ends here.
      return { start, end: i };
    }
    if (isTopLevelKeyStart(l, key)) {
      start = i;
      break;
    }
  }
  if (start === -1) return null;
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    const l = lines[i];
    // Next non-empty, non-indented line = next top-level key = block ends.
    if (l.trim() !== "" && !/^\s/.test(l)) {
      end = i;
      break;
    }
    // Explicit YAML doc boundary also ends the block (and the doc).
    if (isYamlDocBoundary(l)) {
      end = i;
      break;
    }
  }
  return { start, end };
}

// Detect the indentation of event keys inside an existing `hooks:` block, so we
// reuse whatever indent the user's config uses instead of assuming 2 spaces.
// Falls back to 2 spaces (the canonical default) when no indented key is found.
// Uses isBlockStartKey so inline scalars / anchors / flow syntax are not
// mistaken for block event keys (fixes #9).
function detectEventIndent(blockLines) {
  for (const line of blockLines) {
    if (!isBlockStartKey(line)) continue;
    const m = line.match(/^(\s+)/);
    if (m && m[1].length >= 1 && m[1].length <= 6) return m[1];
  }
  return "  ";
}

// Exported for unit tests (fixes #9). Purely rewrites the hermes hooks block;
// does not touch the filesystem (the filesystem helpers call into this).
// `client` selects the entry point the emitted commands reference (defaults to
// the installer's own copy, which is what the unit tests exercise).
export function installHermesHooks(yamlText, client = null) {
  const events = hermesHookEvents();
  const split = splitTopLevelBlock(yamlText, "hooks");
  if (!split) {
    // No hooks block yet: append one with our workled events.
    const block = [
      "hooks:",
      ...events.map((ev) => [
        `  ${ev}:`,
        `    - command: ${hermesCommandYaml(ev, client)}`,
      ]).flat(),
    ].join("\n");
    const trimmed = yamlText.trimEnd();
    return (trimmed ? trimmed + "\n" : "") + block + "\n";
  }
  // A hooks block exists: rebuild it, preserving every non-workled hook entry
  // and only replacing the workled entries for our events. Indentation is read
  // from the existing block (any consistent indent works), so a user config
  // using 4-space or tab indentation is not corrupted.
  const lines = yamlText.split("\n");
  const blockLines = lines.slice(split.start, split.end);
  const indent = detectEventIndent(blockLines);
  const out = [];
  let currentEvent = null;
  const ensured = new Set();
  for (const line of blockLines) {
    const isBlock = isBlockStartKey(line);
    const evIndentMatch = line.match(/^(\s+)/);
    if (isBlock && evIndentMatch && evIndentMatch[1].length > 0) {
      // Any indented map key under `hooks:` is an event key. Keep its own
      // indentation; entries are derived one level deeper than that key.
      const nameMatch = line.match(/^\s*([A-Za-z_][A-Za-z0-9_.\-:]*):/);
      if (!nameMatch) { out.push(line); continue; }
      currentEvent = nameMatch[1];
      out.push(line);
      if (events.includes(currentEvent) && !ensured.has(currentEvent)) {
        ensured.add(currentEvent);
        out.push(`${evIndentMatch[1]}  - command: ${hermesCommandYaml(currentEvent, client)}`);
      }
      continue;
    }
    // Regular line inside the block: drop stale workled entries of OUR events
    // (regardless of their indent), preserve everything else verbatim.
    const isWorkledEntry =
      currentEvent && events.includes(currentEvent) && /^\s*-\s+command:.*workled/.test(line);
    if (isWorkledEntry) {
      continue;
    }
    // Drop orphan continuation lines left behind by previous broken installs
    // (e.g. " hook --event" that no longer has a parent - command: line).
    // Only lines that carry the workled "hook --event" fragment qualify, so a
    // user's own continuation lines (e.g. a hook's "timeout:") are preserved.
    const isOrphan = /^\s+\S+/.test(line) && !line.includes("command:") && line.includes("hook --event");
    if (isOrphan) continue;
    out.push(line);
  }
  // Ensure every workled event exists with exactly our command.
  for (const ev of events) {
    if (ensured.has(ev)) continue;
    out.push(`${indent}${ev}:`);
    out.push(`${indent}  - command: ${hermesCommandYaml(ev, client)}`);
  }
  const before = lines.slice(0, split.start);
  const after = lines.slice(split.end);
  return [...before, ...out, ...after].join("\n");
}

// Exported for unit tests (fixes #9). Purely rewrites the hermes hooks block;
// does not touch the filesystem (the filesystem helpers call into this).
export function uninstallHermesHooks(yamlText) {
  const events = hermesHookEvents();
  const split = splitTopLevelBlock(yamlText, "hooks");
  if (!split) return yamlText;
  const lines = yamlText.split("\n");
  const blockLines = lines.slice(split.start, split.end);
  const indent = detectEventIndent(blockLines);
  // Group the block into (eventKey | null for a prelude, entries[]). Top-level
  // lines (the `hooks:` key itself) and blank lines are skipped.
  const groups = [];
  let cur = null;
  let prelude = null;
  for (const line of blockLines) {
    if (line.trim() === "") continue;
    if (!/^\s/.test(line)) continue;
    const evIndentMatch = line.match(/^(\s+)/);
    if (isBlockStartKey(line) && evIndentMatch) {
      const nameMatch = line.match(/^\s*([A-Za-z_][A-Za-z0-9_.\-:]*):/);
      if (nameMatch) {
        cur = { key: nameMatch[1], indent: evIndentMatch[1], entries: [] };
        groups.push(cur);
        continue;
      }
    }
    if (cur) {
      cur.entries.push(line);
    } else {
      // Indented line before any event group (odd but harmless): keep it so
      // nothing is silently dropped.
      if (!prelude) {
        prelude = [];
        groups.push({ key: null, indent: "", entries: prelude });
      }
      prelude.push(line);
    }
  }
  // Drop only our workled entries; keep everything else (indent-preserving).
  // A workled event group keeps its remaining entries, so the user's own hooks
  // on the same event survive an uninstall.
  const keptGroups = groups
    .map((g) => {
      const workledEvt = events.includes(g.key);
      const kept = workledEvt
        ? g.entries.filter((l) => !/^\s*-\s+command:.*workled/.test(l))
        : g.entries;
      return { key: g.key, indent: g.indent, entries: kept };
    })
    .filter((g) => g.entries.length > 0);
  // If nothing remains under hooks, drop the whole block.
  if (keptGroups.length === 0) {
    const before = lines.slice(0, split.start);
    const after = lines.slice(split.end);
    return [...before, ...after].join("\n").replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";
  }
  const rebuilt = [
    "hooks:",
    ...keptGroups.flatMap((g) =>
      g.key === null ? g.entries : [`${g.indent}${g.key}:`, ...g.entries]
    ),
  ];
  const before = lines.slice(0, split.start);
  const after = lines.slice(split.end);
  return [...before, ...rebuilt, ...after].join("\n").replace(/\n{3,}/g, "\n\n");
}

// ---- hermes hook allowlist (per-hook consent, v0.1.25) -----------------------
//
// Hermes gates every shell hook on a byte-exact (event, command) consent for
// non-interactive runs (gateway/cron/CI). The coarse escape hatch is
// `hooks_auto_accept: true` in config.yaml — but that disables the consent
// mechanism for EVERY hook on the machine, which a security review (2026-09-07)
// rightly flagged as out of scope for an LED skill. The fine-grained mechanism
// is the per-user allowlist <hermes-home>/shell-hooks-allowlist.json:
//   { "approvals": [ { "event", "command", "approved_at", ... } ] }
// Runtime matching (agent/shell_hooks.py::_is_allowlisted) compares only the
// (event, command) pair byte-exactly; the other fields are metadata. So workled
// registers exactly its own hook commands there and never touches
// hooks_auto_accept — the host's consent posture stays intact.

function hermesAllowlistPath() {
  return joinP(hermesHome(), "shell-hooks-allowlist.json");
}

// Every command this installer has ever written into the hermes allowlist has
// the shape `node <...>/workled/index.js hook --event <event>`. The entry path
// changes over time (source checkout before entryPathFor, the client's own
// installed copy after it), so revoking by exact string match leaves every
// earlier approval behind — 10 stale rows survived uninstall that way, still
// pointing at the checkout. Recognise our own rows structurally instead.
// The match is deliberately narrow: the command must invoke an index.js inside
// a `workled` directory, through `hook`, with an `--event` argument. Nothing a
// user hand-writes for another tool looks like that.
const WORKLED_HOOK_COMMAND_RE =
  /^\s*node\s+(?:"([^"]+)"|(\S+))\s+hook\s+--event\s+(\w+)(?:\s+--client\s+[\w-]+)?\s*$/;

function isWorkledAllowlistEntry(entry) {
  if (!entry || typeof entry.command !== "string") return false;
  const m = entry.command.match(WORKLED_HOOK_COMMAND_RE);
  if (!m) return false;
  const entryPath = (m[1] ?? m[2]).replace(/\\/g, "/");
  return /(^|\/)workled\/index\.js$/i.test(entryPath);
}

// Pure JSON edit, exported for unit tests. Adds one approval per event using
// the same command string the config.yaml hook rows carry (hookCommand(ev) is
// the single source; hermesCommandYaml merely JSON-quotes it, and YAML parsing
// yields the identical scalar). Idempotent: existing (event, command) pairs are
// kept untouched, as are all non-workled approvals. script_mtime_at_approval is
// intentionally omitted — hermes only uses it for `hooks doctor` drift hints.
export function approveHermesAllowlist(jsonText, events, client = null) {
  let data;
  try {
    data = JSON.parse(jsonText);
  } catch {
    data = {};
  }
  if (!data || typeof data !== "object" || Array.isArray(data)) data = {};
  if (!Array.isArray(data.approvals)) data.approvals = [];
  const current = new Set(events.map((ev) => hookCommand(ev, client)));
  // Migrate: drop our own rows left over from an earlier entry path before
  // adding the current ones, so a re-install after the path changed replaces
  // the approvals instead of stacking a second set beside the stale rows.
  const before = data.approvals.length;
  data.approvals = data.approvals.filter(
    (e) => !(isWorkledAllowlistEntry(e) && !current.has(e.command))
  );
  const pruned = before - data.approvals.length;
  const approvedAt = new Date().toISOString();
  let added = 0;
  for (const ev of events) {
    const command = hookCommand(ev, client);
    const exists = data.approvals.some(
      (e) => e && e.event === ev && e.command === command
    );
    if (exists) continue;
    data.approvals.push({ event: ev, command, approved_at: approvedAt });
    added++;
  }
  return { text: JSON.stringify(data, null, 2) + "\n", added, pruned };
}

// Pure JSON edit, exported for unit tests. Drops workled's own approvals —
// both the current commands and any row from a previous entry path (see
// isWorkledAllowlistEntry); every other entry survives. Returns the new text
// plus how many entries were removed so the caller can decide whether to
// persist (and whether the file is now empty enough to delete).
export function revokeHermesAllowlist(jsonText, events, client = null) {
  let data;
  try {
    data = JSON.parse(jsonText);
  } catch {
    return { text: jsonText, removed: 0 };
  }
  const commands = new Set(events.map((ev) => hookCommand(ev, client)));
  const before = Array.isArray(data?.approvals) ? data.approvals.length : 0;
  const kept = (data.approvals || []).filter(
    (e) => !(e && (commands.has(e.command) || isWorkledAllowlistEntry(e)))
  );
  if (kept.length === before) return { text: jsonText, removed: 0 };
  data.approvals = kept;
  return { text: JSON.stringify(data, null, 2) + "\n", removed: before - kept.length };
}

// File-level wrapper for install: persist the approvals, reporting only what
// changed. Never writes when there is nothing to add (preserves file mtime and
// any concurrent edits hermes may have made).
function applyHermesAllowlist(client = null) {
  const p = hermesAllowlistPath();
  const current = existsSync(p) ? readFileSync(p, "utf8") : "";
  const { text, added, pruned } = approveHermesAllowlist(current, hermesHookEvents(), client);
  // `pruned` alone still needs a write: migrating stale rows to the current
  // entry path adds nothing when the current rows are already there.
  if (added > 0 || pruned > 0) {
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, text, "utf8");
  }
  return { path: p, added, pruned };
}

// File-level wrapper for uninstall: remove workled's approvals. When nothing
// of ours remains the file is left as-is; when it becomes empty because of our
// removal we delete it so an uninstall leaves zero residue.
function stripHermesAllowlist(client = null) {
  const p = hermesAllowlistPath();
  if (!existsSync(p)) return { path: p, removed: 0 };
  const { text, removed } = revokeHermesAllowlist(readFileSync(p, "utf8"), hermesHookEvents(), client);
  if (removed > 0) {
    let remaining = 0;
    try {
      remaining = (JSON.parse(text).approvals || []).length;
    } catch {
      remaining = 1; // unparsable after our edit: keep the file, be safe
    }
    if (remaining === 0) {
      unlinkSync(p);
    } else {
      writeFileSync(p, text, "utf8");
    }
  }
  return { path: p, removed };
}

function installHermes(client = null) {
  const cfg = joinP(hermesHome(), "config.yaml");
  mkdirSync(dirname(cfg), { recursive: true });
  const existing = existsSync(cfg) ? readFileSync(cfg, "utf8") : "";
  const withHooks = installHermesHooks(existing, client);
  writeFileSync(cfg, withHooks, "utf8");
  const allow = applyHermesAllowlist(client);
  return (
    `Installed hermes shell hooks -> ${cfg}\n` +
    `Allowlisted ${allow.added} workled hook command(s) -> ${allow.path}` +
    // A re-install after the entry path changed replaces stale approvals rather
    // than adding a second set; surface that so "Allowlisted 0" never looks
    // like a no-op when the file was in fact rewritten.
    (allow.pruned > 0 ? ` (replaced ${allow.pruned} entr(y/ies) from an earlier path)` : "")
  );
}

function uninstallHermes(client = null) {
  const cfg = joinP(hermesHome(), "config.yaml");
  const allow = stripHermesAllowlist(client);
  if (!existsSync(cfg)) {
    return allow.removed > 0
      ? `No hermes config at ${cfg}; revoked ${allow.removed} allowlist entr(y/ies) -> ${allow.path}`
      : `No hermes config at ${cfg}`;
  }
  const content = readFileSync(cfg, "utf8");
  // Remove workled hooks from the hooks block; every other top-level key
  // (user hooks, MCP servers, model/terminal settings, ...) is preserved.
  // The workled MCP server entry is removed separately by
  // unregisterWorkledMcp("hermes") via removeMcpServerYaml().
  let cleaned = uninstallHermesHooks(content);
  if (cleaned === content) {
    return allow.removed > 0
      ? `No hermes workled hooks at ${cfg}; revoked ${allow.removed} allowlist entr(y/ies) -> ${allow.path}`
      : `No hermes workled hooks at ${cfg}`;
  }
  if (cleaned.trim() === "") {
    removePath(cfg);
    removeEmptyParent(dirname(cfg));
    return `Removed empty hermes config.yaml -> ${cfg}`;
  }
  writeFileSync(cfg, cleaned, "utf8");
  return `Removed hermes shell hooks -> ${cfg}`;
}

// ---- Skill directory management ----------------------------------------------
// Copy the entire workled skill directory to each client's skills/workled
// directory so status reports the skill field correctly. Re-install overwrites;
// uninstall removes only the workled directory (leaf directories with other
// files are left untouched).

// Install the skill by copying the whole tree into the client's skills/workled
// directory — no junction, no symlink.
//
// Why a copy rather than a link: the skill ships as a self-contained tree, so
// an installed copy must not depend on a source checkout still being there. A
// junction into the checkout breaks as soon as the skill is installed from a
// release artifact (there is no checkout to point at), and it also exposes the
// whole repo — including .git — to the client. Re-run install after editing the
// source; that is the price of a self-contained install. (The earlier link
// install avoided that re-install, but only ever worked on a dev machine.)
//
// Replacing an existing entry is deliberate: an install from before this change
// is a legacy junction, and it has to go before the copy can be written there.
// It is our own skill directory either way, and removeSkillEntry guarantees a
// link is never walked through.
function installSkill(client) {
  const t = CLIENT_TARGETS[client];
  if (!t?.skillPath) return null;
  const destDir = t.skillPath();
  if (!destDir) return null;
  // Resolve the true source directory so an installer invoked through a legacy
  // linked install still copies from the real tree rather than from the link.
  const srcDir = realpathSync(scriptDir);
  if (!existsSync(srcDir)) return null;

  // Never copy the skill onto itself. When the installer is itself run from an
  // installed copy, scriptDir IS this client's skill directory: removing the
  // destination first would delete the very tree we are about to read from, and
  // the copy would end up empty. It is already installed there — nothing to do.
  if (resolve(srcDir).toLowerCase() === resolve(destDir).toLowerCase()) return null;

  // lstat (not existsSync) so a dangling link still counts as present and gets
  // replaced rather than making the copy trip over it.
  let destPresent = true;
  try {
    lstatSync(destDir);
  } catch {
    destPresent = false;
  }
  if (destPresent) removeSkillEntry(destDir);

  mkdirSync(dirname(destDir), { recursive: true });
  cpDir(srcDir, destDir);

  // A copy that landed somewhere wrong would still report success, which
  // leaves a dangling entry point: the user then runs `node <dest>/index.js`
  // against a file that is not reachable. Verify the one file every entry
  // point needs before claiming the copy worked.
  if (!existsSync(joinP(destDir, "index.js"))) {
    throw new Error(`skill copy produced no index.js at ${joinP(destDir, "index.js")}`);
  }
  return `Copied skill directory -> ${destDir}`;
}

function uninstallSkill(client) {
  const t = CLIENT_TARGETS[client];
  if (!t?.skillPath) return null;
  const destDir = t.skillPath();
  if (!destDir) return null;
  if (!existsSync(destDir)) return null;
  // removeSkillEntry, not removePath: with junction installs the entry is a
  // link, and a recursive removal fallback must never walk into the source.
  removeSkillEntry(destDir);
  removeEmptyParent(dirname(destDir));
  return `Removed skill directory -> ${destDir}`;
}

// Create a junction for workled if installed under a @namespace subdirectory.
// Only targets @namespace/workled/SKILL.md (confirmed workled skill).
// Create the canonical `skills/workled` link for a scoped `@namespace/workled`
// install. Logic lives in utils.js (shared with `status` so we don't import
// back from here into index.js). See createSkillJunctions in utils.js.

// Remove workled junction AND real directory from the skills directory.
function removeSkillJunctions(skillsDir) {
  if (!existsSync(skillsDir)) return [];
  const msgs = [];
  const workledDir = joinP(skillsDir, "workled");
  if (!existsSync(workledDir)) return msgs;
  try {
    // removeSkillEntry: this entry may be a junction, which must be unlinked
    // rather than recursed into (see that helper).
    removeSkillEntry(workledDir);
    msgs.push(`Removed workled skill directory ${workledDir}`);
  } catch {
    // removal failed, skip silently
  }
  return msgs;
}

// ---- dsh (DeepSeek Harness) --------------------------------------------------
// dsh architecture: everything is a Cordis plugin — there is no zero-plugin
// pure-config path. We ship a first-class `workled-dsh-plugin` (sibling
// directory `./dsh-plugin/`) that:
//   1. ctx.on() SEVEN native Cordis events (bridge-source-validated):
//        agent/session-start, agent/pre-step, tools/pre-execute,
//        tools/post-execute, agent/turn-stopping, subagent/start,
//        subagent/end
//   2. drives the workled LED BY DIRECT HTTP to the workled MCP endpoint
//      (tools/call set_agent_state JSON-RPC POST), no shell hop, no hook CLI.

// Write the real device url into the copied bundle patch.yml in place (plan B:
// no separate cordis.patch.yml override layer — the bundle carries the real
// config). When WORKLED_MCP_URL is unset the bundle's placeholder url is kept.
function patchBundleUrl(patchYmlPath, url) {
  if (!existsSync(patchYmlPath)) return;
  let text = readFileSync(patchYmlPath, "utf8");
  const out = text.replace(/url:\s*'[^']*'/, `url: '${url}'`);
  if (out !== text) writeFileSync(patchYmlPath, out, "utf8");
}

// Split a YAML top-level array (rows starting with `- ` at column 0) into
// items, preserving any prelude lines (comments) before the first item. Used to
// surgically remove stale workled rows from cordis.patch.yml on re-install /
// uninstall without touching the user's other rows.
function splitYamlTopItems(text) {
  const lines = text.split("\n");
  const items = [];
  let cur = null;
  const prelude = [];
  for (const line of lines) {
    if (/^-\s/.test(line)) {
      if (cur) items.push(cur);
      cur = [line];
    } else if (cur) {
      cur.push(line);
    } else if (line.trim() !== "") {
      prelude.push(line);
    }
  }
  if (cur) items.push(cur);
  items.prelude = prelude;
  return items;
}

// Recursively copy the dsh-plugin tree. Node 18+ supports fs.cp; we use a
// small manual cpDir so the installer doesn't need fs.promises or flag checks.
function cpDir(src, dest) {
  mkdirSync(dest, { recursive: true });
  for (const entry of readdirSync(src, { withFileTypes: true })) {
    // Skip .git and .dsh-local directories to avoid permission issues and infinite recursion
    if (entry.name === ".git" || entry.name === ".dsh-local") continue;
    const s = joinP(src, entry.name);
    const d = joinP(dest, entry.name);
    if (entry.isDirectory()) cpDir(s, d);
    else copyFileSync(s, d);
  }
}

// ============================================================
// dsh: blocked-path report + permission request (probe lives in utils.js)
// ============================================================

// dsh installs to the L1 standard paths only — no workspace-local fallback and
// no env-only mode. When dsh's agent runs this installer it does so under a
// WRITE_RESTRICTED token (dsh-sandbox-windows-acl / CreateRestrictedToken) that
// only allows writes inside the workspace, so ~/.dsh is genuinely unwritable
// even though the user owns it. A blocked path is therefore reported and the
// installer re-runs itself elevated (UAC / sudo) so the user can grant access
// explicitly — never silent, never degraded.

// Loud, explicit failure notice. Never silent, never degraded.
function reportWriteFailure(check, paths) {
  const reason = WRITE_ERROR_REASONS[check.code] || `write failed (${check.code})`;
  const block = [
    "",
    "✖ workled: the dsh standard paths are not writable — install aborted.",
    "",
    `  Blocked path : ${check.path}`,
    `  Reason       : ${reason}`,
    `  dsh home     : ${dshHome()}`,
    "",
    "  workled must be able to write:",
    ...paths.map((p) => `    - ${p}`),
    "",
  ];
  console.error(block.join("\n"));
}

// Re-run this installer with elevated privileges so the user sees a real OS
// permission prompt (Windows UAC / POSIX sudo) instead of a silent degrade.
// The elevated process runs with a full (admin) token, escaping dsh's
// restricted-token sandbox. Returns true when the elevated run exited 0.
function runElevated() {
  const self = fileURLToPath(import.meta.url);
  const args = [self, ...process.argv.slice(2)];
  // WORKLED_ELEVATED marks the child so a second failure cannot loop forever.
  const childEnv = { ...process.env, WORKLED_ELEVATED: "1" };

  if (process.platform === "win32") {
    const psQuote = (s) => "'" + String(s).replace(/'/g, "''") + "'";
    const argList = args.map(psQuote).join(",");
    // ASCII only: `powershell.exe -Command` decodes its argument with the
    // console code page, so non-ASCII characters would be mangled.
    const cmd =
      `try { ` +
      `$p = Start-Process -FilePath ${psQuote(process.execPath)} ` +
      `-ArgumentList @(${argList}) -WorkingDirectory ${psQuote(process.cwd())} ` +
      `-Verb RunAs -Wait -PassThru -ErrorAction Stop; ` +
      `if ($null -eq $p) { exit 1 }; ` +
      `exit $p.ExitCode ` +
      `} catch { ` +
      `Write-Output "workled: elevation not granted - $($_.Exception.Message)"; ` +
      `exit 1 }`;
    const r = spawnSync("powershell.exe", ["-NoProfile", "-Command", cmd], {
      stdio: "inherit",
      env: childEnv,
    });
    if (r.error) {
      console.error(`workled: could not raise the permission prompt: ${r.error.message}`);
      return false;
    }
    return r.status === 0;
  }

  const r = spawnSync("sudo", [process.execPath, ...args], { stdio: "inherit", env: childEnv });
  if (r.error) {
    console.error(
      `workled: could not re-run through sudo (${r.error.message}).\n` +
        `  Re-run manually with enough privileges:\n` +
        `    sudo ${[process.execPath, ...args].map((a) => JSON.stringify(a)).join(" ")}`
    );
    return false;
  }
  return r.status === 0;
}

function installDsh(mcpEntry, customHome = null) {
  const home = customHome || dshHome();
  // Use the caller-resolved url: main() runs device discovery once and hands the
  // same entry to every client. Reading the env alone here (the old behaviour)
  // meant dsh was the only client that never saw discovery and always fell back
  // to the <device-name> placeholder, silently installing a broken endpoint.
  const url =
    mcpEntry?.url || process.env.WORKLED_MCP_URL || "http://<device-name>.local:18791/mcp";
  mkdirSync(home, { recursive: true });
  // A) Install as a proper dsh bundle under the web profile's node_modules.
  const srcPlugin = joinP(scriptDir, "dsh-plugin");
  const dstPlugin = joinP(home, "profiles", "web", "node_modules", "workled");
  cpDir(srcPlugin, dstPlugin);
  // A2) Write the real device url into the copied bundle patch.yml in place.
  patchBundleUrl(joinP(dstPlugin, "patch.yml"), url);
  // B) Register the bundle in the web profile's package.json.
  const profileDir = joinP(home, "profiles", "web");
  mkdirSync(profileDir, { recursive: true });
  const pkgFile = joinP(profileDir, "package.json");
  const pkg = readJsonOrEmpty(pkgFile) || {};
  if (!pkg.dsh) pkg.dsh = {};
  if (!pkg.dsh.profile) pkg.dsh.profile = {};
  if (!Array.isArray(pkg.dsh.profile.bundles)) pkg.dsh.profile.bundles = [];
  if (!pkg.dsh.profile.bundles.includes("workled")) {
    pkg.dsh.profile.bundles.push("workled");
  }
  writeConfig(pkgFile, pkg);
  return `Installed dsh bundle -> ${dstPlugin}`;
}

function uninstallDsh() {
  const home = dshHome();
  const removed = [];
  // A) Remove bundle from the web profile's node_modules.
  const bundleDir = joinP(home, "profiles", "web", "node_modules", "workled");
  if (existsSync(bundleDir)) {
    removePath(bundleDir);
    removed.push(`Removed dsh bundle dir ${bundleDir}`);
    removeEmptyParent(dirname(bundleDir));
  }
  // Backward compat: also remove old vendored plugin tree if present.
  const pluginDir = joinP(home, "plugins", "workled");
  if (existsSync(pluginDir)) {
    removePath(pluginDir);
    removed.push(`Removed old dsh plugin dir ${pluginDir}`);
    removeEmptyParent(dirname(pluginDir));
  }
  // B) Unregister bundle from the web profile's package.json.
  const pkgFile = joinP(home, "profiles", "web", "package.json");
  if (existsSync(pkgFile)) {
    const pkg = readJsonOrEmpty(pkgFile);
    if (pkg && Array.isArray(pkg.dsh?.profile?.bundles)) {
      pkg.dsh.profile.bundles = pkg.dsh.profile.bundles.filter((b) => b !== "workled");
      if (pkg.dsh.profile.bundles.length === 0) delete pkg.dsh.profile.bundles;
      if (Object.keys(pkg.dsh.profile || {}).length === 0) delete pkg.dsh.profile;
      if (Object.keys(pkg.dsh || {}).length === 0) delete pkg.dsh;
      writeConfig(pkgFile, pkg);
      removed.push(`Removed workled from ${pkgFile}`);
    }
  }
  // C) Backward compat: strip any legacy workled rows a pre-"plan B" install
  // left in the `web` profile cordis.patch.yml (the override layer no longer
  // exists — the bundle carries the real url in its own patch.yml now).
  const patchFile = joinP(home, "profiles", "web", "cordis.patch.yml");
  if (existsSync(patchFile)) {
    const items = splitYamlTopItems(readFileSync(patchFile, "utf8"));
    const kept = items.filter((it) => !it.some((l) => l.includes("workled")));
    const rows = (items.prelude || []).filter((l) => l.trim() !== "[]").concat(kept);
    const written = rows.flat().join("\n").replace(/\n{3,}/g, "\n\n").trimEnd();
    const body = kept.length > 0 ? written : (written ? written + "\n" : "") + "[]";
    writeFileSync(patchFile, body + "\n", "utf8");
    removed.push(`Removed workled plugin from ${patchFile}`);
  }
  return removed.length > 0 ? removed.join("\n") : `No workled install at ${home}`;
}

// ---- CLI ----------------------------------------------------------------------

function printHelp() {
  console.log(`workled skill installer

Usage:
  node skill-install.mjs install|uninstall [--client <name>]

Options:
  --client <name>   Target client. Omitted = auto-detect. Pass it explicitly
                    when several clients are installed (e.g. "install workled
                    in kilocode" → --client kilocode).

Clients:
  ${CLIENTS.join(", ")}
`);
}

// ============================================================
// Post-install self-check
// ============================================================

// Run the status diagnostic for the clients this run touched and print a short
// human-readable summary, so a finished install answers "did the wiring land?"
// (MCP entry + skill dir + plugin/hooks + device reach) without a manual
// `node index.js status`.
//
// Best-effort by design: a slow, blocked or failing diagnostic must never
// change the install's exit code. Every failure path ends in a one-line note.
async function runPostInstallStatus(client, corePath) {
  // Long enough for the Bluetooth + URL probes (which retry) but short enough
  // that a hung child never stalls the install. Overridable for slow networks.
  const timeoutMs = Number(process.env.WORKLED_STATUS_TIMEOUT_MS) || 10000;
  // `--client` keeps the scan to this client, so unrelated configs never add
  // probe time or noise.
  const args = [corePath, "status", "--client", client];

  let stdout = "";
  let stderr = "";
  let timedOut = false;

  try {
    const { spawn } = await import("child_process");
    // process.execPath (not a bare "node"): the check then works even when the
    // user's PATH has no Node entry (e.g. an IDE-managed runtime).
    const proc = spawn(process.execPath, args, {
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });
    proc.stdout.on("data", (c) => { stdout += c; });
    proc.stderr.on("data", (c) => { stderr += c; });
    const timer = setTimeout(() => {
      timedOut = true;
      proc.kill();
    }, timeoutMs);
    await new Promise((done) => {
      proc.on("close", done);
      proc.on("error", done);
    });
    clearTimeout(timer);
  } catch (err) {
    console.log(`   (status diagnostic could not start: ${err && err.message})`);
    return;
  }

  if (timedOut) {
    console.log(
      `   (status diagnostic timed out after ${timeoutMs}ms - re-run \`node index.js status --client ${client}\`)`
    );
    return;
  }

  let status;
  try {
    status = JSON.parse(stdout);
  } catch {
    // No parseable report: surface the child's own progress log rather than
    // failing silently — that is the only clue left about what went wrong.
    const tail = stderr.trim().split(/\r?\n/).slice(-3).join("\n     ");
    console.log(
      "   (status diagnostic returned no report)" + (tail ? `\n     ${tail}` : "")
    );
    return;
  }

  // clients[] holds installable clients only — the WORKLED_MCP_URL override is
  // reported as a top-level field plus a hint sentence, never as an entry, so
  // this is a plain per-client match.
  const entries = (status.clients || []).filter((e) => e.client.startsWith(client));

  console.log("");
  console.log("Status check:");
  if (entries.length === 0) {
    console.log(`   no workled server reported for: ${client}`);
  } else {
    // Aligned columns so the three install surfaces read at a glance.
    // "-" = not applicable for this client (it has no such artifact).
    const head = ["client", "mcp", "skill", "plugin", "reachable"];
    const rows = entries.map((e) => [
      e.client,
      e.mcpConfig ? "yes" : "no",
      e.skill ? "yes" : "-",
      e.plugin ? "yes" : "-",
      e.mcpUrlReachable ? "yes" : "no",
    ]);
    const width = head.map((c, i) =>
      Math.max(c.length, ...rows.map((r) => String(r[i]).length))
    );
    const line = (r) =>
      "   " + r.map((v, i) => String(v).padEnd(width[i])).join("  ");
    console.log(line(head));
    for (const r of rows) console.log(line(r));
  }
  if (status.hint) console.log(`   ${status.hint}`);
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    printHelp();
    return;
  }

  const action = args[0]; // install | uninstall
  if (action !== "install" && action !== "uninstall") {
    printHelp();
    process.exit(1);
  }

  // Target client resolution. An explicit `--client <name>` always wins.
  // Omitted --client triggers auto-detection: layer 1 reads process-injected
  // env vars that are NOT present in the OS persistent env (system-level
  // leftovers like a registry HERMES_HOME are ignored, so they never cause a
  // false hermes match), layer 2 looks for a unique client whose MCP config
  // already mentions workled, layer 3 looks for a unique signature dir. If
  // ambiguous or no signal, we require an explicit --client.
  const clientIdx = args.indexOf("--client");
  let clientArg = clientIdx >= 0 ? args[clientIdx + 1] : null;
  if (clientArg && !CLIENTS.includes(clientArg)) {
    console.error(`Unknown client: ${clientArg}\nSupported clients: ${CLIENTS.join(", ")}`);
    process.exit(1);
  }
  if (!clientArg) {
    const detected = detectClient();
    if (!detected) {
      console.error(
        `Could not auto-detect the client environment.\n` +
        `Please specify the target client explicitly:\n\n` +
        `  node skill-install.mjs ${action} --client <name>\n\n` +
        `Supported clients:\n` +
        `  ${CLIENTS.join(", ")}\n\n` +
        `Detection checks performed:\n` +
        `  • Process environment variables (DSH_HOME, OPENCODE_HOME, etc.)\n` +
        `  • Existing workled MCP configuration (unique entry only)\n` +
        `  • Client signature directories (unique only)\n\n` +
        `Tip: Run this command from within your agent's terminal/session ` +
        `so its environment variables are available for detection.`
      );
      process.exit(1);
    }
    clientArg = detected;
    console.error(`[workled] auto-detected client: ${clientArg}`);
  }
  const targets = [clientArg];

  // Resolve the MCP URL once (discovers the real workled device name when
  // possible) so every client's install registers the same, correct endpoint.
  let mcpEntry = null;
  if (action === "install") {
    const url = await resolveWorkledMcpUrl();
    if (url.includes("<device-name>")) {
      console.warn(
        "Warning: no WORKLED_MCP_URL set. A placeholder URL " +
          "(http://<device-name>.local:18791/mcp) will be " +
          "written into configs that have no existing workled entry (e.g. after an " +
          "earlier uninstall) — existing real URLs are kept. Replace <device-name> with " +
          "your real workled device name (e.g. HomeAnt-XXXX), or re-run install with " +
          "WORKLED_MCP_URL set, before connecting."
      );
    }
    mcpEntry = { url, enabled: true };
  }

  const failedClients = [];
  for (const c of targets) {
    const isInstall = action === "install";
    const lines = [];
    try {
    switch (c) {
      case "opencode":
      case "kilo":
      case "pi":
      case "openclaw": {
        const t = CLIENT_TARGETS[c]; // { label, pluginPath } — plugin-file client
        const dest = t.pluginPath();
        const destDir = dirname(dest);
        if (isInstall) {
          // Install the self-contained copy FIRST: the generated entry file
          // imports that copy (entryPathFor), so it must exist before the file
          // referencing it is written.
          const skillMsg = installSkill(c);
          if (skillMsg) lines.push(skillMsg);
          mkdirSync(destDir, { recursive: true });
          writeFileSync(dest, PLUGIN_CLIENTS[c](c), "utf8");
          lines.push(`Installed ${c} ${t.label} -> ${dest}`);
          // openclaw additionally writes the plugin manifest + openclaw.json
          // registration; its entry file is generated by the same shared path.
          if (c === "openclaw") {
            lines.push(await installOpenclawManifest());
          }
          lines.push(...(await registerWorkledMcp(c, mcpEntry)));
          // Create junction for @namespace/workled if present
          const junctionMsgs = createSkillJunctions(dirname(t.skillPath()));
          lines.push(...junctionMsgs);
        } else {
          if (existsSync(dest)) {
            removePath(dest);
            removeEmptyParent(destDir);
            lines.push(`Removed ${c} ${t.label} -> ${dest}`);
          } else {
            lines.push(`No ${c} ${t.label} at ${dest}`);
          }
          // openclaw: drop the manifest + openclaw.json registration (the whole
          // plugin dir, including the entry, is removed by uninstallOpenclaw).
          if (c === "openclaw") {
            lines.push(await uninstallOpenclaw());
          }
          lines.push(...unregisterWorkledMcp(c));
          // Remove SKILL.md from client's skills directory
          const skillMsg = uninstallSkill(c);
          if (skillMsg) lines.push(skillMsg);
          // Remove workled junction and real directory
          const junctionMsgs = removeSkillJunctions(dirname(t.skillPath()));
          lines.push(...junctionMsgs);
        }
        break;
      }
      case "hermes": {
        const hh = hermesHome();
        if (isInstall) {
          // Copy first: installHermes() emits hook commands that reference this
          // client's own installed copy (entryPathFor), and the allowlist must
          // record the very same command string the config carries.
          const skillMsg = installSkill("hermes");
          if (skillMsg) lines.push(skillMsg);
          lines.push(installHermes("hermes"));
          lines.push(...(await registerWorkledMcp("hermes", mcpEntry)));
          const hermesT = CLIENT_TARGETS.hermes;
          if (hermesT?.skillPath) {
            const junctionMsgs = createSkillJunctions(dirname(hermesT.skillPath()));
            lines.push(...junctionMsgs);
          }
        } else {
          // Mirror image: revoke the allowlist / hooks BEFORE deleting the
          // copy, because the revoke predicate is byte-exact against the
          // command that copy produces.
          lines.push(uninstallHermes("hermes"));
          lines.push(...unregisterWorkledMcp("hermes"));
          const skillMsg = uninstallSkill("hermes");
          if (skillMsg) lines.push(skillMsg);
          const hermesT = CLIENT_TARGETS.hermes;
          if (hermesT?.skillPath) {
            const junctionMsgs = removeSkillJunctions(dirname(hermesT.skillPath()));
            lines.push(...junctionMsgs);
          }
        }
        break;
      }
      case "dsh": {
        if (isInstall) {
          // L1 only: probe the standard dsh paths before touching anything.
          const t = CLIENT_TARGETS.dsh;
          const standardPaths = [t.mcpPath?.(), t.pluginPath?.(), t.skillPath?.()].filter(Boolean);
          const check = checkWriteAccess(standardPaths);
          if (!check.ok) {
            reportWriteFailure(check, standardPaths);
            // WORKLED_ELEVATED: set on the child, so a blocked elevated run
            // reports instead of prompting again. WORKLED_NO_ELEVATE: opt out
            // for CI / non-interactive runs.
            const canElevate =
              process.env.WORKLED_ELEVATED !== "1" && process.env.WORKLED_NO_ELEVATE !== "1";
            if (canElevate) {
              console.error(
                "  Requesting permission: re-running the installer with elevated privileges."
              );
              console.error(
                "  Approve the OS permission prompt to continue; declining aborts the install.\n"
              );
              if (runElevated()) {
                // Do not trust the elevated run's exit code on its own: a UAC
                // prompt that is blocked, auto-denied or silently dismissed can
                // still surface as 0 while nothing was written (observed: a
                // non-existent DSH_HOME reported "installed" and exited 0).
                // Re-probe the same paths and only claim success when they are
                // genuinely writable now.
                const after = checkWriteAccess(standardPaths);
                if (!after.ok) {
                  throw new Error(
                    `dsh standard path still not writable after the elevated run: ${after.path} (${after.code})`
                  );
                }
                lines.push("dsh: installed by the elevated run above.");
                break;
              }
            }
            throw new Error(`dsh standard path not writable: ${check.path} (${check.code})`);
          }
          lines.push(installDsh(mcpEntry));
          const skillMsg = installSkill("dsh");
          if (skillMsg) lines.push(skillMsg);
          const dshT = CLIENT_TARGETS.dsh;
          if (dshT?.skillPath) {
            const junctionMsgs = createSkillJunctions(dirname(dshT.skillPath()));
            lines.push(...junctionMsgs);
          }
        } else {
          lines.push(uninstallDsh());
          const skillMsg = uninstallSkill("dsh");
          if (skillMsg) lines.push(skillMsg);
          const dshT = CLIENT_TARGETS.dsh;
          if (dshT?.skillPath) {
            const junctionMsgs = removeSkillJunctions(dirname(dshT.skillPath()));
            lines.push(...junctionMsgs);
          }
        }
        break;
      }
      case "workbuddy": {
        // WorkBuddy is a pure-MCP client whose state protocol is enforced by
        // user-level lifecycle hooks (settings.json) rather than by agent
        // discipline; install wires MCP + hooks, uninstall removes both.
        if (isInstall) {
          // Copy first: the hook commands written below reference it.
          const skillMsg = installSkill("workbuddy");
          if (skillMsg) lines.push(skillMsg);
          lines.push(...(await installWorkbuddy(mcpEntry)));
          const wbT = CLIENT_TARGETS.workbuddy;
          if (wbT?.skillPath) {
            const junctionMsgs = createSkillJunctions(dirname(wbT.skillPath()));
            lines.push(...junctionMsgs);
          }
        } else {
          lines.push(...(await uninstallWorkbuddy()));
          const skillMsg = uninstallSkill("workbuddy");
          if (skillMsg) lines.push(skillMsg);
          const wbT = CLIENT_TARGETS.workbuddy;
          if (wbT?.skillPath) {
            const junctionMsgs = removeSkillJunctions(dirname(wbT.skillPath()));
            lines.push(...junctionMsgs);
          }
        }
        break;
      }
      case "trae-cn": {
        // trae-cn (VSCode fork) reads a GLOBAL MCP config at
        // <user-data>/User/mcp.json (shared by every workspace) plus lifecycle
        // hooks at <home>/.trae-cn/hooks.json — both are wired automatically.
        // MCP is picked up after a reload; if the URL is the <device-name>
        // placeholder the user must still replace it in Settings → MCP, and the
        // Hooks config needs manual enabling in Settings > Hooks to fire.
        if (isInstall) {
          // Copy first: the hook commands written by installTraeCn() reference
          // this client's own installed copy.
          const skillMsg = installSkill("trae-cn");
          if (skillMsg) lines.push(skillMsg);
          lines.push(...installTraeCn(mcpEntry));
          const traeT = CLIENT_TARGETS["trae-cn"];
          if (traeT?.skillPath) {
            const junctionMsgs = createSkillJunctions(dirname(traeT.skillPath()));
            lines.push(...junctionMsgs);
          }
          // The placeholder reminder is conditional: when a real URL was
          // resolved (WORKLED_MCP_URL, or an existing entry kept in place)
          // there is no `<device-name>` left to replace, and telling the user
          // to go look for one is noise.
          const traePlaceholder = String(mcpEntry?.url || "").includes("<device-name>");
          lines.push(
            "trae-cn: MCP written to <user-data>/User/mcp.json (reload to pick it up)." +
              (traePlaceholder
                ? " Replace <device-name> in Settings → MCP with your real device name."
                : "") +
              " Enable the workled hooks in Settings → Hooks for agent-state tracking."
          );
        } else {
          lines.push(...uninstallTraeCn());
          const skillMsg = uninstallSkill("trae-cn");
          if (skillMsg) lines.push(skillMsg);
          const traeT = CLIENT_TARGETS["trae-cn"];
          if (traeT?.skillPath) {
            const junctionMsgs = removeSkillJunctions(dirname(traeT.skillPath()));
            lines.push(...junctionMsgs);
          }
          lines.push(
            "trae-cn: workled MCP entry and hooks removed; the server you added via Settings → MCP (if any) stays as you configured it."
          );
        }
        break;
      }
      default:
        console.error(`Unknown client: ${c}`);
        process.exit(1);
    }
    console.log(lines.join("\n") + "\n");
    } catch (err) {
      // One client failed (e.g. the safe-delete shim refused a bulk delete this
      // turn). Do NOT abort the batch — report and continue so every other
      // client is still (un)installed.
      console.error(`⚠ Failed to ${action} client "${c}": ${err && err.message}`);
      failedClients.push(c);
    }
  }

  // If any client could not be (un)installed this run (typically because the
  // safe-delete shim blocked a bulk delete under a busy turn), surface a
  // summary and a non-zero exit so the caller knows to retry those clients in a
  // fresh turn — without having skipped the ones that succeeded.
  if (failedClients.length) {
    console.error(
      `\n⚠ ${failedClients.length} client(s) failed to ${action}: ${failedClients.join(", ")}.\n` +
      `  Re-run \`node skill-install.mjs ${action} --client ${failedClients.join(", ")}\` in a fresh turn to finish.`
    );
    process.exitCode = 1;
  }

  // No `.bak` files are created (writes are idempotent), so there is nothing
  // to clean up here. Historical `.bak` files left by older versions are
  // deliberately left untouched — the tool never deletes user-visible
  // backup files.

  // Self-check: report the state of every client this run touched. Runs for
  // install only (uninstall has nothing left to verify) and never affects the
  // exit code — see runPostInstallStatus.
  //
  // The old version skipped this whenever DSH_HOME was set, on the theory that
  // it indicated a sandbox. It does not: DSH_HOME is a user-settable variable
  // with no bearing on whether the check can run, and the real dsh sandbox
  // (a WRITE_RESTRICTED token) typically leaves it unset — so the guard
  // skipped the check exactly when it was most useful. The timeout below is
  // what actually protects against a hung probe.
  if (action === "install") {
    await runPostInstallStatus(targets[0], corePath);
    // Spell out the entry point: `corePath` resolves to the user-level copy
    // when there is one and to this script's own directory otherwise, so the
    // runnable `index.js` is not always where the install output points.
    console.log(
      `\nFull report: node "${corePath}" status --client ${targets[0]}`
    );
  } else {
    // Uninstall deletes the per-client skill copy, so the path the user may
    // have been running `index.js` from is gone by now. Point at the stable
    // user-level entry instead — otherwise `status` dies with "Cannot find
    // module" before workled even loads.
    console.log(
      `\nVerify: node "${corePath}" status --client ${targets[0]}`
    );
  }
}

// Run only when invoked directly (not when imported by the test suite, which
// needs the exported JSONC editor helpers without triggering an install).
const isMain =
  (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) ||
  (process.argv[1] && resolve(process.argv[1]).split(/[\\/]/).at(-1) === fileURLToPath(import.meta.url).split(/[\\/]/).at(-1));
if (isMain) {
  main().catch((err) => {
    console.error(`install.mjs error: ${err && err.stack}`);
    process.exit(1);
  });
}
