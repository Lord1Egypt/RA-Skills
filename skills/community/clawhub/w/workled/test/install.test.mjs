// Unit tests for the JSONC comment-preserving editors (skill-install.mjs) and
// the stripJsonc trailing-comma handling (utils.js).
// Run: node --test test/install.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { stripJsonc } from "../utils.js";
import {
  isValidJsonc,
  upsertJsoncEntry,
  removeJsoncEntry,
  removeJsoncKey,
  findKeyLineStartForValue,
  findNamedObjectSpanInMap,
  splitTopLevelBlock,
  installHermesHooks,
  uninstallHermesHooks,
  approveHermesAllowlist,
  revokeHermesAllowlist,
  hermesHookEvents,
  parseOpenclawConfigText,
} from "../skill-install.mjs";

const ENTRY = { url: "http://HomeAnt-A919.local:18791/mcp", enabled: true, type: "remote" };

test("stripJsonc drops comments and trailing commas without touching strings", () => {
  const src = `{
    "a": 1, // line comment
    "b": "x, }", /* block */
    "c": [1, 2,],
  }`;
  assert.deepEqual(JSON.parse(stripJsonc(src)), { a: 1, b: "x, }", c: [1, 2] });
});

test("stripJsonc leaves a lone trailing comma string value intact", () => {
  assert.deepEqual(JSON.parse(stripJsonc('{ "s": ",}" }')), { s: ",}" });
});

test("isValidJsonc accepts comments and trailing commas, rejects broken JSON", () => {
  assert.equal(isValidJsonc('{\n  "a": 1, // trailing\n  "b": [1, 2,],\n}'), true);
  assert.equal(isValidJsonc('{ "a": , }'), false);
});

const COMMENTED = `{
  // user comment that must survive
  "auth": true,
  "mcp": {
    "other": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"] }
  }
}
`;

test("upsertJsoncEntry inserts into an existing map and preserves comments", () => {
  const out = upsertJsoncEntry(COMMENTED, "mcp", "workled", ENTRY);
  assert.ok(out, "expected an edited document");
  assert.ok(out.includes("// user comment that must survive"), "comment preserved");
  assert.ok(out.includes('"other"'), "unrelated server preserved");
  assert.ok(out.includes('"workled"'));
  assert.ok(out.includes('"type": "remote"'));
  const parsed = JSON.parse(stripJsonc(out));
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(parsed.auth, true);
  assert.equal(isValidJsonc(out), true);
});

test("upsertJsoncEntry replaces an existing workled entry in place", () => {
  const withWorkled = `{
  "mcp": {
    "workled": {
      "url": "http://old.local:18791/mcp",
      "enabled": true
    }
  }
}
`;
  const out = upsertJsoncEntry(withWorkled, "mcp", "workled", ENTRY);
  const parsed = JSON.parse(stripJsonc(out));
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(parsed.mcp.workled.url, ENTRY.url);
});

// Regression test for #key-indent-drift — when workled already exists and we
// re-upsert, the previous implementation accumulated 2 spaces per replace on
// the key line while fields only used keyIndent + "  ", causing a visible
// `    "workled"` → `        "workled"` drift after each reinstall and JSON
// files doubling in nested-indent on every cycle. The repair moves the
// replace-from slice past the leading whitespace of the key line so
// jsoncEntryBlock can re-emit a uniform indent.
test("upsertJsoncEntry existing-replace keeps key-line indent stable across N cycles", () => {
  const start = `{
  "mcp": {
    "requestTimeoutMs": 1500,
    "workled": {
      "url": "http://old.local/mcp",
      "enabled": true
    }
  }
}
`;
  let out = start;
  for (let i = 0; i < 4; i++) {
    out = upsertJsoncEntry(out, "mcp", "workled", ENTRY);
  }
  // Key line: 4 spaces (the indent of fields inside mcp)
  assert.match(out, /\n {4}"workled":/);
  // Field line: 6 spaces (one level deeper)
  assert.match(out, /\n {6}"url":/);
  // The drift regression would produce `\n {8}"workled"` — assert it's not there
  assert.doesNotMatch(out, /\n {8}"workled":/);
  assert.equal(isValidJsonc(out), true);
  assert.equal(JSON.parse(stripJsonc(out)).mcp.workled.url, ENTRY.url);
});

test("upsertJsoncEntry appends a new top-level key when absent", () => {
  const bare = '{ "note": "x" }\n';
  const out = upsertJsoncEntry(bare, "mcp", "workled", ENTRY);
  const parsed = JSON.parse(stripJsonc(out));
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(parsed.note, "x");
  assert.equal(isValidJsonc(out), true);
});

test("upsertJsoncEntry inserts into an empty map without a leading comma", () => {
  const emptyMap = '{\n  "mcp": {}\n}\n';
  const out = upsertJsoncEntry(emptyMap, "mcp", "workled", ENTRY);
  assert.ok(out);
  const parsed = JSON.parse(stripJsonc(out));
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(isValidJsonc(out), true);
});

test("upsertJsoncEntry inserts into a comment-only map", () => {
  const commentOnly = '{\n  "mcp": {\n    // placeholder for future servers\n  }\n}\n';
  const out = upsertJsoncEntry(commentOnly, "mcp", "workled", ENTRY);
  assert.ok(out);
  assert.ok(out.includes("// placeholder for future servers"), "comment preserved");
  const parsed = JSON.parse(stripJsonc(out));
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(isValidJsonc(out), true);
});

test("removeJsoncEntry deletes workled in the middle of a map and fixes commas", () => {
  const middle = `{
  "mcp": {
    "a": 1,
    "workled": { "url": "u", "enabled": true },
    "b": 2
  }
}
`;
  const out = removeJsoncEntry(middle, "mcp", "workled");
  const parsed = JSON.parse(stripJsonc(out));
  assert.equal(parsed.mcp.workled, undefined);
  assert.equal(parsed.mcp.a, 1);
  assert.equal(parsed.mcp.b, 2);
  assert.equal(isValidJsonc(out), true);
});

test("removeJsoncEntry leaves the map when workled is the last member", () => {
  const last = `{
  "mcp": {
    "a": 1,
    "workled": { "url": "u", "enabled": true }
  }
}
`;
  const out = removeJsoncEntry(last, "mcp", "workled");
  const parsed = JSON.parse(stripJsonc(out));
  assert.equal(parsed.mcp.workled, undefined);
  assert.equal(parsed.mcp.a, 1);
  assert.deepEqual(Object.keys(parsed.mcp), ["a"]);
  assert.equal(isValidJsonc(out), true);
});

test("removeJsoncEntry returns null when workled is not present", () => {
  const noWorkled = '{\n  "mcp": { "a": 1 }\n}\n';
  assert.equal(removeJsoncEntry(noWorkled, "mcp", "workled"), null);
});

test("round-trip preserves comments across insert then remove", () => {
  const inserted = upsertJsoncEntry(COMMENTED, "mcp", "workled", ENTRY);
  const removed = removeJsoncEntry(inserted, "mcp", "workled");
  assert.ok(removed);
  assert.ok(removed.includes("// user comment that must survive"));
  const parsed = JSON.parse(stripJsonc(removed));
  assert.equal(parsed.mcp.workled, undefined);
  assert.equal(parsed.mcp.other.command, "npx");
});

test("removeJsoncKey drops an emptied map (last member) with its comma", () => {
  const only = `{
  "auth": true,
  "mcp": {
    "workled": { "url": "u", "enabled": true }
  }
}
`;
  const withoutEntry = removeJsoncEntry(only, "mcp", "workled");
  assert.ok(withoutEntry);
  const out = removeJsoncKey(withoutEntry, "mcp");
  assert.ok(out, "emptied map should be removed");
  assert.equal(out.includes('"mcp"'), false);
  const parsed = JSON.parse(stripJsonc(out));
  assert.equal(parsed.mcp, undefined);
  assert.equal(parsed.auth, true);
  assert.equal(isValidJsonc(out), true);
});

test("removeJsoncKey refuses to drop a populated map", () => {
  const populated = '{\n  "mcp": { "a": 1 }\n}\n';
  assert.equal(removeJsoncKey(populated, "mcp"), null);
});

// --- #5 UTF-8 BOM coverage ----------------------------------------------------
//
// A BOM on the leading byte used to shift every slice index by +1 in
// findTopLevelObjectValueSpan, causing the editor to drop out of surgery mode
// and fall back to a JSON.stringify rewrite (which wipes user comments).
// Lock in the corrected behaviour: both upsert and remove must succeed on a
// BOM-prefixed document, the BOM itself must be preserved in the output, and
// the edited text must remain valid JSONC + parse to the right value.
test("upsertJsoncEntry edits a BOM-prefixed document and keeps the BOM", () => {
  const withBom = "\ufeff" + COMMENTED;
  const out = upsertJsoncEntry(withBom, "mcp", "workled", ENTRY);
  assert.ok(out, "expected edited document, not null");
  assert.equal(out.charCodeAt(0), 0xfeff, "BOM byte must be preserved");
  assert.ok(out.includes("// user comment that must survive"), "comment preserved");
  const parsed = JSON.parse(stripJsonc(out.slice(1))); // strip BOM for JSON.parse
  assert.deepEqual(parsed.mcp.workled, ENTRY);
  assert.equal(isValidJsonc(out.slice(1)), true);
});

test("removeJsoncEntry edits a BOM-prefixed document and keeps the BOM", () => {
  const withWorkled = "\ufeff{\n  \"mcp\": {\n    \"workled\": { \"url\": \"u\" },\n    \"a\": 1\n  }\n}\n";
  const out = removeJsoncEntry(withWorkled, "mcp", "workled");
  assert.ok(out);
  assert.equal(out.charCodeAt(0), 0xfeff);
  assert.equal(out.includes("workled"), false);
  const parsed = JSON.parse(stripJsonc(out.slice(1)));
  assert.equal(parsed.mcp.workled, undefined);
  assert.equal(parsed.mcp.a, 1);
  assert.equal(isValidJsonc(out.slice(1)), true);
});

// --- #10 cross-line key layouts + key start index ----------------------------
//
// The user can write `"workled":\n  { ... }` with the `{` on a separate line.
// `findKeyLineStartForValue` must walk back from the `{` and return the
// OPENING quote of the key string, not the closing quote — otherwise remove
// surgery leaves half the key behind and the JSON becomes invalid.
test("findKeyLineStartForValue returns opening quote on key+value cross-line layout", () => {
  const text = `{
  "mcp": {
    "workled":
      { "url": "u", "enabled": true }
  }
}`;
  const braceIdx = text.indexOf("{ \"url\"");
  assert.ok(braceIdx > 0);
  const start = findKeyLineStartForValue(text, braceIdx);
  assert.ok(start > 0, `expected opening-quote index, got ${start}`);
  // From the opening-quote index, consume one JSON string and assert it is
  // EXACTLY `"workled"` — if we land on the CLOSING quote instead, we'll only
  // see `"`, which is what the previous buggy implementation produced.
  const rest = text.slice(start);
  const m = rest.match(/^"[^"\\]*(?:\\.[^"\\]*)*"/s);
  assert.ok(m, `expected a full quoted JSON string at start=${start}, saw ${JSON.stringify(rest.slice(0, 20))}`);
  assert.equal(m[0], '"workled"', "the consumed key string must be exactly \"workled\"");
});

test("findKeyLineStartForValue skips values containing escaped quotes/colons", () => {
  // This document has `"value"` (a VALUE string) between the key and the
  // object `{`. If findKeyLineStartForValue honours the colon-prefix check
  // and escape-handling correctly, it returns the `"ke\"y"` opening quote.
  const text = `{
  "weird": { "before": true },
  "ke\\"y": "a:\\"b,c:{[}]d",
  "workled": { "url": "u" }
}`;
  const brace = text.indexOf('{ "url"');
  const start = findKeyLineStartForValue(text, brace);
  assert.ok(start > 0);
  const rest = text.slice(start);
  const m = rest.match(/^"[^"\\]*(?:\\.[^"\\]*)*"/s);
  assert.equal(m && m[0], '"workled"', "must not walk into the preceding value string");
});

test("removeJsoncEntry fully removes a key whose value `{` sits on the next line", () => {
  const crossLine = `{
  "mcp": {
    "a": 1,
    "workled":
      { "url": "u", "enabled": true },
    "b": 2
  }
}
`;
  const out = removeJsoncEntry(crossLine, "mcp", "workled");
  assert.ok(out);
  // After remove, a partial key residue like `"kled"` must NOT appear.
  assert.equal(/workled|kled|workl/.test(out), false, "no partial key residue in:\n" + out);
  const parsed = JSON.parse(stripJsonc(out));
  assert.equal(parsed.mcp.workled, undefined);
  assert.equal(parsed.mcp.a, 1);
  assert.equal(parsed.mcp.b, 2);
  assert.equal(isValidJsonc(out), true);
});

// --- #9 findNamedObjectSpanInMap – nested object / comment / string braces ---
test("findNamedObjectSpanInMap spans through nested objects, comments, and string braces", () => {
  const map = `{
  "other": { "x": 1 },
  "workled": {
    "url": "http://x:1/mcp",
    // a "{" inside a comment is ignored
    "nested": { "a": { "b": "}" }, // trailing brace in a string: "}}}"
      "arr": [1, { "c": 2 }]
    },
    "enabled": true
  },
  "after": true
}`;
  const span = findNamedObjectSpanInMap(map, "workled");
  assert.ok(span, "expected to find workled span");
  const body = map.slice(span.start, span.end + 1);
  // Must start at the `{` immediately after `"workled":` and stop at the
  // matching closing `}` that closes workled's own object.
  assert.ok(body.startsWith("{"));
  assert.ok(body.endsWith("}"));
  const parsed = JSON.parse(stripJsonc(body));
  assert.equal(parsed.url, "http://x:1/mcp");
  assert.equal(parsed.enabled, true);
  assert.equal(parsed.nested.a.b, "}");
  assert.equal(parsed.nested.arr[1].c, 2);
});

// --- #9 splitTopLevelBlock — YAML ---/ flow { } / anchor/alias --------------
test("splitTopLevelBlock stops at a --- document boundary", () => {
  const multiDoc = `# header
hooks:
  tool:before:
    - command: something

---
# Second document — hooks: must not be pulled into the first block
hooks:
  tool:before:
    - command: other
`;
  const s = splitTopLevelBlock(multiDoc, "hooks");
  assert.ok(s);
  const chunk = multiDoc.split("\n").slice(s.start, s.end).join("\n");
  assert.ok(chunk.includes("something"), "first-doc content captured");
  assert.equal(chunk.includes("other"), false, "second doc must not be captured");
});

test("splitTopLevelBlock sees hooks written in flow syntax {...} as non-block", () => {
  const flow = `# A hooks key that is a single inline flow-map => no indented block.
model: "gpt"
hooks: { tool:before: [{ command: "echo hi" }] }
something: else
`;
  // `isBlockStartKey` requires "name:" followed by nothing / a comment (no
  // inline value), so a flow `{ ... }` on the same line should NOT produce
  // a block match → split returns null and installHermesHooks will append
  // a brand-new block-style `hooks:` after.
  const s = splitTopLevelBlock(flow, "hooks");
  assert.equal(s, null, "flow-syntax hooks should not be treated as a block");

  const installed = installHermesHooks(flow);
  assert.ok(installed.includes("\nhooks:"));
  assert.ok(installed.includes("workled"));
  // The original flow-style line should still be there; we do not try to
  // mutate a flow map (we can't do byte-level surgery on inline JSON-in-YAML).
  assert.ok(installed.includes('hooks: { tool:before:'), "original flow line untouched");
});

test("uninstallHermesHooks preserves anchors/aliases and unrelated hooks", () => {
  const yaml = `# hermes-native hook + workled hook, yaml alias
defaults: &defaults
  timeout: 5000
hooks:
  pre_tool_call:
    - <<: *defaults
      name: user-own-hook
      command: echo hello
    - command: npx -y @modelcontextprotocol/workled hook --event pre_tool_call
  post_llm_call:
    - command: npx -y @modelcontextprotocol/workled hook --event post_llm_call
    - command: ls
`;
  const cleaned = uninstallHermesHooks(yaml);
  // The <<:*defaults alias and the user's own `echo hello` and `ls` entries
  // must remain after workled hooks are stripped.
  assert.ok(cleaned.includes("<<: *defaults"), "yaml alias preserved");
  assert.ok(cleaned.includes("echo hello"), "user hook kept");
  assert.ok(cleaned.includes("command: ls"), "user post_llm_call hook kept");
  assert.equal(/hook --event/.test(cleaned), false, "workled hooks removed");
  // Event keys themselves must still be present because they still carry user
  // content (pre_tool_call has echo hello, post_llm_call has ls).
  assert.ok(cleaned.includes("pre_tool_call:"));
  assert.ok(cleaned.includes("post_llm_call:"));
});

// --- hermes per-hook allowlist (v0.1.25) + post_tool_call coverage -------

test("installHermesHooks now includes post_tool_call alongside pre_tool_call", () => {
  const out = installHermesHooks("");
  assert.ok(out.includes("post_tool_call:"), "post_tool_call event registered");
  assert.ok(out.includes("pre_tool_call:"), "pre_tool_call event registered");
  // Every installed event must carry a workled hook --event command.
  assert.ok(out.includes("hook --event post_tool_call"));
});

const EVENTS_COUNT = hermesHookEvents().length;

test("approveHermesAllowlist adds one entry per event on an empty skeleton", () => {
  const { text, added } = approveHermesAllowlist("", hermesHookEvents());
  assert.equal(added, EVENTS_COUNT, "one entry per hermes event");
  const data = JSON.parse(text);
  assert.equal(data.approvals.length, EVENTS_COUNT);
  for (const e of data.approvals) {
    assert.ok(e.event && typeof e.command === "string", "entry shape");
    assert.ok(e.command.includes(`hook --event ${e.event}`), "command matches event");
    assert.ok(e.approved_at, "approved_at recorded");
  }
});

test("approveHermesAllowlist is idempotent and preserves foreign approvals", () => {
  const foreign = { event: "pre_tool_call", command: "user-own-tool --run" };
  const first = approveHermesAllowlist(
    JSON.stringify({ approvals: [foreign] }),
    hermesHookEvents()
  );
  assert.equal(first.added, EVENTS_COUNT);
  const second = approveHermesAllowlist(first.text, hermesHookEvents());
  assert.equal(second.added, 0, "no duplicates on re-approval");
  const data = JSON.parse(second.text);
  assert.equal(data.approvals.length, EVENTS_COUNT + 1, "foreign entry kept");
  assert.deepEqual(
    data.approvals.find((e) => e.command === foreign.command),
    foreign,
    "foreign entry untouched"
  );
});

test("approveHermesAllowlist tolerates corrupt or non-object JSON", () => {
  for (const bad of ["not json", "[1, 2]", '"str"']) {
    const { text, added } = approveHermesAllowlist(bad, hermesHookEvents());
    assert.equal(added, EVENTS_COUNT, `recovers from ${bad.slice(0, 8)}`);
    assert.ok(JSON.parse(text).approvals.length === EVENTS_COUNT);
  }
});

test("revokeHermesAllowlist removes only workled's own entries", () => {
  const foreign = { event: "on_session_start", command: "user-own-tool --run" };
  const approved = approveHermesAllowlist(
    JSON.stringify({ approvals: [foreign] }),
    hermesHookEvents()
  );
  const { text, removed } = revokeHermesAllowlist(approved.text, hermesHookEvents());
  assert.equal(removed, EVENTS_COUNT, "all workled entries removed");
  const data = JSON.parse(text);
  assert.deepEqual(data.approvals, [foreign], "foreign approval survives");
});

test("revokeHermesAllowlist roundtrips to zero and is a no-op on empty", () => {
  const approved = approveHermesAllowlist("", hermesHookEvents());
  const empty = revokeHermesAllowlist(approved.text, hermesHookEvents());
  assert.equal(JSON.parse(empty.text).approvals.length, 0);
  const again = revokeHermesAllowlist(empty.text, hermesHookEvents());
  assert.equal(again.removed, 0, "nothing to remove");
  assert.equal(again.text, empty.text, "text untouched");
});

test("revokeHermesAllowlist tolerates corrupt JSON without writing", () => {
  const { text, removed } = revokeHermesAllowlist("not json", hermesHookEvents());
  assert.equal(removed, 0);
  assert.equal(text, "not json", "input returned unchanged");
});

// --- hermes allowlist residue -------------------------------------------------
//
// Regression: the generated commands used to point at the source checkout and
// later at each client's own installed copy. Revoking matched the CURRENT
// command strings byte-exactly, so after that path change an uninstall removed
// nothing and all 10 approvals survived, still invoking the checkout. Our own
// rows are recognised structurally now — and only ours: the shape is narrow
// enough that no other tool's hook can be mistaken for one.

const STALE_ENTRY = "C:/repo/.agents/skills/workled/index.js";

test("revokeHermesAllowlist drops approvals from an earlier entry path", () => {
  const stale = hermesHookEvents().map((ev) => ({
    event: ev,
    command: `node ${STALE_ENTRY} hook --event ${ev}`,
    approved_at: "2026-09-16T05:01:17.747Z",
  }));
  const foreign = { event: "pre_tool_call", command: "user-own-tool --run" };
  const { text, removed } = revokeHermesAllowlist(
    JSON.stringify({ approvals: [...stale, foreign] }),
    hermesHookEvents()
  );
  assert.equal(removed, EVENTS_COUNT, "every stale row is workled's own");
  assert.deepEqual(JSON.parse(text).approvals, [foreign], "foreign row survives");
});

test("revokeHermesAllowlist keeps lookalike commands that are not ours", () => {
  const lookalikes = [
    { event: "pre_tool_call", command: "node /opt/other/index.js hook --event pre_tool_call" },
    { event: "pre_tool_call", command: `node ${STALE_ENTRY} --status` },
    { event: "pre_tool_call", command: "npx workled hook --event pre_tool_call" },
    { event: "pre_tool_call", command: `node ${STALE_ENTRY} hook` },
  ];
  const { text, removed } = revokeHermesAllowlist(
    JSON.stringify({ approvals: lookalikes }),
    hermesHookEvents()
  );
  assert.equal(removed, 0, "only real workled hook rows may be dropped");
  assert.deepEqual(JSON.parse(text).approvals, lookalikes);
});

test("approveHermesAllowlist migrates stale rows instead of stacking a second set", () => {
  const stale = hermesHookEvents().map((ev) => ({
    event: ev,
    command: `node ${STALE_ENTRY} hook --event ${ev}`,
    approved_at: "2026-09-16T05:01:17.747Z",
  }));
  const { text, added, pruned } = approveHermesAllowlist(
    JSON.stringify({ approvals: stale }),
    hermesHookEvents()
  );
  assert.equal(pruned, EVENTS_COUNT, "stale rows reported for the caller to persist");
  assert.equal(added, EVENTS_COUNT, "current rows written");
  assert.equal(
    JSON.parse(text).approvals.length,
    EVENTS_COUNT,
    "one row per event, not two per event"
  );
});

// --- install/uninstall JSON layout -------------------------------------------
//
// Regression: appending a top-level key to a config that had none emitted the
// comma on a line of its own and put the key flush at column 0, and every
// install/uninstall cycle stranded one more blank line (observed: 5 blank lines
// in opencode.json after 5 cycles). Both are layout-only bugs, so the file has
// to stay byte-identical to what the user wrote once a cycle completes.

test("upsertJsoncEntry appends a top-level key on its own line with correct indent", () => {
  const bare = '{\n  "$schema": "https://opencode.ai/config.json"\n}\n';
  const out = upsertJsoncEntry(bare, "mcp", "workled", ENTRY);
  // The comma belongs at the end of the previous member, and the new key sits
  // one level inside the root object.
  assert.match(out, /\n {2}"mcp": \{\n {4}"workled": \{/);
  assert.doesNotMatch(out, /^\s*,\s*$/m, "no comma-only line");
  assert.doesNotMatch(out, /\n[ \t]*\n/, "no blank line introduced");
  assert.equal(isValidJsonc(out), true);
  assert.deepEqual(JSON.parse(stripJsonc(out)).mcp.workled, ENTRY);
});

test("upsertJsoncEntry appends into an empty root object as a formatted block", () => {
  const out = upsertJsoncEntry("{}", "mcp", "workled", ENTRY);
  assert.equal(out, `{\n  "mcp": {\n    "workled": {\n      "url": "http://HomeAnt-A919.local:18791/mcp",\n      "enabled": true,\n      "type": "remote"\n    }\n  }\n}`);
  assert.equal(JSON.parse(stripJsonc(out)).mcp.workled.url, ENTRY.url);
});

test("removeJsoncEntry reclaims the removed member's line", () => {
  const middle = `{
  "mcp": {
    "workled": { "url": "u", "enabled": true },
    "b": 2
  }
}
`;
  const out = removeJsoncEntry(middle, "mcp", "workled");
  assert.equal(out, `{
  "mcp": {
    "b": 2
  }
}
`);
});

test("a full install/uninstall cycle is whitespace-neutral", () => {
  const seed = '{\n  "$schema": "https://opencode.ai/config.json"\n}\n';
  let text = seed;
  for (let i = 0; i < 5; i++) {
    text = upsertJsoncEntry(text, "mcp", "workled", ENTRY);
    const removed = removeJsoncEntry(text, "mcp", "workled");
    assert.ok(removed, `cycle ${i}: entry removed`);
    text = removeJsoncKey(removed, "mcp") ?? removed;
  }
  assert.equal(text, seed, "5 cycles must return the file to its original bytes");
});

test("a cycle seeded from a populated map is whitespace-neutral too", () => {
  const seed = `{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "other": { "type": "local", "command": ["echo"] }
  }
}
`;
  let text = seed;
  for (let i = 0; i < 3; i++) {
    text = upsertJsoncEntry(text, "mcp", "workled", ENTRY);
    const removed = removeJsoncEntry(text, "mcp", "workled");
    text = removeJsoncKey(removed, "mcp") ?? removed;
  }
  assert.equal(text, seed);
});

// A file that already carries blank lines stranded by an older version must be
// cleaned up rather than preserved: the append path trims the whitespace the
// root's last member was followed by, so the very next install normalises it.
test("a cycle repairs a file carrying stranded blank lines", () => {
  const seed = '{\n  "$schema": "https://opencode.ai/config.json"\n}\n';
  const stranded = '{\n  "$schema": "https://opencode.ai/config.json"\n' + "\n".repeat(9) + "}\n";
  assert.notEqual(stranded, seed);
  let text = upsertJsoncEntry(stranded, "mcp", "workled", ENTRY);
  assert.doesNotMatch(text, /\n[ \t]*\n/, "install collapses the stranded lines");
  const removed = removeJsoncEntry(text, "mcp", "workled");
  text = removeJsoncKey(removed, "mcp") ?? removed;
  assert.equal(text, seed, "and the cycle lands back on the original bytes");
});

// --- generated entry points ---------------------------------------------------
//
// Regression: generated plugins/hooks imported the SOURCE CHECKOUT, so moving or
// deleting the repo broke every client even though installSkill had written a
// working copy into that client's own skills dir. The command/config pair must
// reference that copy — and for hermes the allowlist has to record the exact
// same byte string, or hermes' byte-exact consent check never matches.

test("hook commands reference the client's own installed copy", () => {
  const tmp = mkdtempSync(join(tmpdir(), "workled-entry-"));
  const prev = process.env.HERMES_HOME;
  const posix = (p) => p.replace(/\\/g, "/");
  try {
    process.env.HERMES_HOME = tmp;
    const copyDir = join(tmp, "skills", "workled");
    mkdirSync(copyDir, { recursive: true });
    writeFileSync(join(copyDir, "index.js"), "", "utf8");
    const expected = `${posix(copyDir)}/index.js`;

    const yaml = installHermesHooks("", "hermes");
    const cmds = yaml.split("\n").filter((l) => l.includes("- command:"));
    assert.equal(cmds.length, hermesHookEvents().length);
    for (const line of cmds) {
      assert.ok(line.includes(expected), `command must use the installed copy: ${line}`);
    }

    const { text } = approveHermesAllowlist("", hermesHookEvents(), "hermes");
    const approvals = JSON.parse(text).approvals;
    assert.equal(approvals.length, hermesHookEvents().length);
    for (const a of approvals) {
      assert.ok(a.command.includes(expected), `allowlist must record the same command: ${a.command}`);
    }
  } finally {
    if (prev === undefined) delete process.env.HERMES_HOME;
    else process.env.HERMES_HOME = prev;
    rmSync(tmp, { recursive: true, force: true });
  }
});

test("hook commands fall back to the installer's own copy when no copy is on disk", () => {
  const tmp = mkdtempSync(join(tmpdir(), "workled-entry-"));
  const prev = process.env.HERMES_HOME;
  try {
    process.env.HERMES_HOME = tmp; // exists, but holds no skills/workled copy
    const yaml = installHermesHooks("", "hermes");
    for (const line of yaml.split("\n").filter((l) => l.includes("- command:"))) {
      assert.ok(line.includes("/index.js hook --event"), `unexpected command: ${line}`);
      assert.ok(!line.includes(tmp.replace(/\\/g, "/")), "no copy -> must not point into the empty home");
    }
  } finally {
    if (prev === undefined) delete process.env.HERMES_HOME;
    else process.env.HERMES_HOME = prev;
    rmSync(tmp, { recursive: true, force: true });
  }
});

// openclaw reads openclaw.json with JSON5, so comments and trailing commas are
// legal user content. install/uninstall rewrite that file WHOLE, so a parse
// failure must report "unparseable" (null) rather than degrade to {} — the {}
// fallback replaced the user's entire config with a workled stub.
test("parseOpenclawConfigText accepts comments and trailing commas", () => {
  const text = `{
  // hand-written note
  "agents": { "defaults": { "workspace": "C:\\\\ws" } },
  "plugins": { "load": { "paths": [] }, },
}`;
  const cfg = parseOpenclawConfigText(text);
  assert.ok(cfg, "expected an object");
  assert.equal(cfg.agents.defaults.workspace, "C:\\ws");
  assert.deepEqual(cfg.plugins.load.paths, []);
});

test("parseOpenclawConfigText returns null for content it cannot parse", () => {
  // Must NOT be {} — every caller treats {} as "safe to write".
  assert.equal(parseOpenclawConfigText("{ \"a\": , }"), null);
  assert.equal(parseOpenclawConfigText(""), null);
  assert.equal(parseOpenclawConfigText("null"), null);
  assert.equal(parseOpenclawConfigText('"just a string"'), null);
  assert.equal(parseOpenclawConfigText("[1, 2]"), null);
});

test("parseOpenclawConfigText still returns an object for an empty config", () => {
  assert.deepEqual(parseOpenclawConfigText("{}"), {});
  assert.deepEqual(parseOpenclawConfigText("{}\n"), {});
});
