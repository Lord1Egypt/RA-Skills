// Unit tests for the workled plugin's pure helpers.
// Run: node --test test/
import test from "node:test";
import assert from "node:assert/strict";
import {
  getInputTools,
  isInputTool,
  resolveMergedUrl,
  resolveMcpType,
  traeCnReminderText,
  shouldDedupState,
  drainFlushPromisesForState,
  CLIENTS,
  CLIENT_TARGETS,
} from "../index.js";
import { mergeClientHooks, stripClientHooks, workledHookCommand } from "../skill-install.mjs";

const PLACEHOLDER = "http://<device-name>.local:18791/mcp";
const REAL = "http://HomeAnt-A919.local:18791/mcp";

test("getInputTools covers common interactive-tool naming patterns", () => {
  // Coverage for AskUserQuestion / AskUserConfirm / choose_option /
  // select_choice / prompt_input / permission_approval and friends.
  assert.deepEqual(getInputTools(), [
    "question", "confirm", "ask", "choose", "select", "prompt", "input", "approval", "questionnaire",
  ]);
});

test("isInputTool matches by substring, case-insensitive", () => {
  assert.equal(isInputTool("AskUserQuestion"), true);
  assert.equal(isInputTool("question"), true);
  assert.equal(isInputTool("ask_question"), true);
  assert.equal(isInputTool("ASKQUESTION"), true);
  assert.equal(isInputTool("get_brightness"), false);
  assert.equal(isInputTool(""), false);
  assert.equal(isInputTool(null), false);
  assert.equal(isInputTool(undefined), false);
  assert.equal(isInputTool(123), false);
});

test("resolveMergedUrl never downgrades a real URL to the placeholder", () => {
  // Existing real URL + incoming placeholder -> keep the real URL.
  assert.equal(resolveMergedUrl(REAL, PLACEHOLDER), REAL);
  // Existing real URL + incoming real URL -> use the incoming one.
  const newer = "http://HomeAnt-B999.local:18791/mcp";
  assert.equal(resolveMergedUrl(REAL, newer), newer);
  // No existing URL + incoming placeholder -> placeholder (first install).
  assert.equal(resolveMergedUrl(undefined, PLACEHOLDER), PLACEHOLDER);
  // Existing placeholder + incoming placeholder -> placeholder.
  assert.equal(resolveMergedUrl(PLACEHOLDER, PLACEHOLDER), PLACEHOLDER);
  // No existing URL + incoming real URL -> real.
  assert.equal(resolveMergedUrl(undefined, REAL), REAL);
});

test("resolveMcpType writes the source default for a fresh entry", () => {
  // No existing type -> source default applies (opencode/kilo/workbuddy).
  assert.equal(resolveMcpType(undefined, "remote"), "remote");
  // Existing type wins over the source default.
  assert.equal(resolveMcpType("http", "remote"), "http");
  assert.equal(resolveMcpType("", "remote"), "remote");
  // No existing type and no default -> null (field omitted entirely).
  assert.equal(resolveMcpType(undefined, undefined), null);
  assert.equal(resolveMcpType(null, ""), null);
});

test("traeCnReminderText fires for a --client trae-cn / unfiltered scan", () => {
  // Explicit trae-cn filter -> reminder present.
  const note = traeCnReminderText({ clientPrefix: "trae-cn" });
  assert.equal(typeof note, "string");
  assert.ok(note.includes("Settings → Hooks"));
  assert.ok(note.includes("device-name"));
  // Unfiltered scan (no clientPrefix) treats trae-cn as in scope too.
  assert.ok(traeCnReminderText({}).includes("Settings"));
});

test("traeCnReminderText fires when a trae-cn entry is in the scan results", () => {
  const note = traeCnReminderText({
    clientPrefix: "trae-cn",
    clients: [{ client: "trae-cn", reachable: true }],
  });
  assert.ok(note.includes("Settings → Hooks"));
});

test("traeCnReminderText stays quiet for non-trae-cn-only scans", () => {
  // A non-trae-cn --client filter (and no trae-cn entry) gets no reminder.
  assert.equal(traeCnReminderText({ clientPrefix: "opencode" }), "");
  assert.equal(
    traeCnReminderText({ clientPrefix: "opencode", clients: [{ client: "env" }] }),
    ""
  );
});

test("traeCnReminderText matches trae-cn worktrees by prefix", () => {
  assert.ok(traeCnReminderText({ clientPrefix: "trae-cn" }).includes("Settings"));
});

test("CLIENT_TARGETS covers every client (with default fallback)", () => {
  for (const c of CLIENTS) {
    assert.ok(
      CLIENT_TARGETS[c] !== undefined || CLIENT_TARGETS.default !== undefined,
      `client "${c}" must have a CLIENT_TARGETS entry or a default fallback`
    );
  }
});

// --- #7 shouldDedupState — 200 ms short-window dedup -------------------------
//
// The behaviour we need to lock in: a repeat state is ONLY suppressed if ALL
// of (a) state matches lastSentState, (b) queue is empty (pendingState
// null-ish), (c) last delivery was <200 ms ago. Any other condition lets the
// new state through so the device can reset its animation (the original #7
// bug suppressed ALL same-state transitions, forever).
test("shouldDedupState suppresses a same-state repeat within the 200ms window", () => {
  assert.equal(
    shouldDedupState("thinking", {
      lastSentState: "thinking",
      lastSentStateAtMs: 0,
      nowMs: 199,
      pendingState: null,
    }),
    true
  );
});

test("shouldDedupState lets the same state through AFTER the 200ms window", () => {
  assert.equal(
    shouldDedupState("thinking", {
      lastSentState: "thinking",
      lastSentStateAtMs: 0,
      nowMs: 201, // past 200 ms boundary
      pendingState: null,
    }),
    false,
    "same state must propagate so animation resets on the next turn"
  );
});

test("shouldDedupState lets a different state through even at 0ms delta", () => {
  assert.equal(
    shouldDedupState("idle", {
      lastSentState: "thinking",
      lastSentStateAtMs: 0,
      nowMs: 10,
      pendingState: null,
    }),
    false
  );
});

test("shouldDedupState never dedups while another state is still queued", () => {
  assert.equal(
    shouldDedupState("thinking", {
      lastSentState: "thinking",
      lastSentStateAtMs: 0,
      nowMs: 10,
      pendingState: "waiting", // something still queued → no dedup
    }),
    false,
    "dedup is off while a state is pending; we only collapse fully idle replays"
  );
});

// --- #6 drainFlushPromisesForState – per-state settle ------------------------
//
// Before the #6 fix, a single completed state would settle EVERY queued flush
// regardless of which state each caller was waiting on. Tests below assert
// that (a) entries tagged with a specific state only settle on that exact
// state, (b) state=null "drain" entries settle on EITHER a specific state
// pass OR the special drain state=null pass, and (c) calls with a mismatched
// state leave other entries untouched so they can settle later.
test("drainFlushPromisesForState only settles entries tagged with the matching state", () => {
  const settled = new Map();
  const makeEntry = (name, state) => ({
    state,
    resolve: (r) => settled.set(name, r),
    reject: () => assert.fail(`${name} should not be rejected`),
  });
  const list = [
    makeEntry("idleWaiter", "idle"),
    makeEntry("thinkingWaiter", "thinking"),
  ];

  const nSettled = drainFlushPromisesForState(list, "idle", { state: "idle", sent: true });
  assert.equal(nSettled, 1, "only one waiter should settle on 'idle'");
  assert.equal(list.length, 1, "the thinking waiter must remain queued");
  assert.equal(list[0].state, "thinking");
  assert.ok(settled.has("idleWaiter"));
  assert.equal(settled.get("idleWaiter").state, "idle");

  // Now deliver "thinking": the remaining waiter should settle.
  const nSettled2 = drainFlushPromisesForState(list, "thinking", { state: "thinking", sent: true });
  assert.equal(nSettled2, 1);
  assert.equal(list.length, 0);
  assert.ok(settled.has("thinkingWaiter"));
});

test("drainFlushPromisesForState settles a state=null (drain) waiter on any state + null pass", () => {
  const settled = new Map();
  const makeEntry = (name, state) => ({
    state,
    resolve: (r) => settled.set(name, r),
    reject: () => assert.fail(`${name} should not be rejected`),
  });
  const list = [makeEntry("drainWaiter", null)];

  // A specific state pass also resolves the drain waiter.
  drainFlushPromisesForState(list, "idle", { state: "idle", sent: true });
  assert.equal(list.length, 0);
  assert.ok(settled.has("drainWaiter"));
  assert.equal(settled.get("drainWaiter").state, "idle");

  // A pure queue-drain pass (state=null) also works.
  const list2 = [makeEntry("drainWaiter2", null)];
  drainFlushPromisesForState(list2, null, { state: null, sent: true });
  assert.equal(list2.length, 0);
  assert.ok(settled.has("drainWaiter2"));
});

// --- Client-parameterised hook core (trae-cn) ------------------------------
//
// trae-cn's global Hooks live in <home>/.trae-cn/hooks.json using the Claude
// Code-style schema (version 1 + hooks.<Event>[]). The generic mergeClientHooks
// drives trae-cn exactly as installTraeCn() does; stripClientHooks removes
// only the trae-cn-scoped workled groups. Both are pure and disk-free.

// Every event in WORKLED_HOOK_SPECS should be present after a fresh merge.
const SPEC_EVENTS = ["UserPromptSubmit", "Stop", "Notification", "PreToolUse", "PostToolUse"];
const cmdFor = (e) => `node workled hook --event ${e} --client trae-cn`;
const mergeTraeCn = (cfg) => mergeClientHooks(cfg, { client: "trae-cn", commandForEvent: cmdFor, version: 1 });
const stripTraeCn = (cfg) => stripClientHooks(cfg, "trae-cn");

test("workledHookCommand is shell-portable (no absolute node, no `&`)", () => {
  // One command string must parse under both bash (workbuddy/Claude Code) and
  // PowerShell (trae-cn). A spaced "quoted absolute path" first token would be
  // a parse error in PowerShell (needs `&`) while `&` is a background operator
  // in bash — so we must start with a bare `node`, never the absolute binary.
  const cmd = workledHookCommand("Notification", "trae-cn");
  assert.ok(cmd.startsWith("node "), `hook command must start with bare node, got: ${cmd}`);
  assert.ok(!cmd.includes("Program Files"), "must not embed the spaced absolute node path");
  assert.ok(!cmd.includes("& "), "must not use the PowerShell-only `&` call operator");
  assert.ok(cmd.includes("--event Notification"));
  assert.ok(cmd.includes("--client trae-cn"));
});

test("workledHookCommand never inlines the MCP URL (config discovery at runtime)", () => {
  // The hook discovers the device URL from its own configuration (mcp.json /
  // WORKLED_MCP_URL) at runtime, so --url must never be baked into the command.
  // Keeping the command URL-free also avoids any shell/sandbox mangling of a
  // raw or base64-encoded URL argument.
  const real = "http://HomeAnt-2831.local:18791/mcp";
  assert.ok(!workledHookCommand("Stop", "trae-cn", real).includes("--url"), "real URL must not be inlined");
  assert.ok(!workledHookCommand("Stop", "trae-cn", real).includes("b64:"), "no base64 encoding");
  assert.ok(!workledHookCommand("Stop", "trae-cn", "http://<device-name>.local:18791/mcp").includes("--url"), "placeholder must not be inlined");
  assert.ok(!workledHookCommand("Stop", "trae-cn").includes("--url"), "bare command stays bare");
});

test("mergeClientHooks('trae-cn') builds a valid bare hooks config from nothing", () => {
  const merged = mergeTraeCn(undefined);
  assert.equal(merged.version, 1);
  assert.ok(merged.hooks, "hooks map required");
  for (const ev of SPEC_EVENTS) {
    assert.ok(Array.isArray(merged.hooks[ev]), `event ${ev} must be an array`);
    assert.ok(merged.hooks[ev].length >= 1, `event ${ev} must have at least one group`);
  }
  // Notification carries two matchers (permission_prompt + idle_prompt); every
  // group must route through the trae-cn client command.
  for (const ev of SPEC_EVENTS) {
    for (const group of merged.hooks[ev]) {
      assert.ok(group.hooks[0].type === "command");
      assert.ok(group.hooks[0].command.includes("--client trae-cn"));
      assert.equal(typeof group.hooks[0].timeout, "number");
    }
  }
});

test("mergeClientHooks('trae-cn') preserves unrelated hooks and version", () => {
  const base = {
    version: 3,
    hooks: {
      Stop: [{ hooks: [{ type: "command", command: "echo user-hook", timeout: 5 }] }],
    },
  };
  const merged = mergeTraeCn(base);
  assert.equal(merged.version, 3, "existing version kept");
  assert.deepEqual(merged.hooks.Stop[0], base.hooks.Stop[0], "unrelated Stop group preserved");
  // The workled group is appended after the unrelated one.
  assert.ok(merged.hooks.Stop.some((g) => g.hooks[0].command.includes("--client trae-cn")));
});

test("mergeClientHooks('trae-cn') is idempotent: re-merging replaces, not duplicates", () => {
  const once = mergeTraeCn(undefined);
  const twice = mergeTraeCn(once);
  for (const ev of SPEC_EVENTS) {
    assert.equal(twice.hooks[ev].length, once.hooks[ev].length, `${ev} must not grow`);
    // Every workled group is traced to our command; no double writes.
    assert.equal(
      twice.hooks[ev].filter((g) => g.hooks[0].command.includes("--client trae-cn")).length,
      once.hooks[ev].filter((g) => g.hooks[0].command.includes("--client trae-cn")).length
    );
  }
});

test("mergeClientHooks('trae-cn') embeds matchers for the Notification events", () => {
  const merged = mergeTraeCn(undefined);
  const matchers = merged.hooks.Notification.map((g) => g.matcher);
  assert.ok(matchers.includes("permission_prompt"));
  assert.ok(matchers.includes("idle_prompt"));
  // PreToolUse is restricted to AskUserQuestion so a question lights "waiting"
  // automatically without spawning a process on every other tool call.
  const pre = merged.hooks.PreToolUse.map((g) => g.matcher);
  assert.ok(pre.includes("AskUserQuestion"));
  // PostToolUse is restricted to AskUserQuestion so the hook does not spawn a
  // process on every tool call.
  const post = merged.hooks.PostToolUse.map((g) => g.matcher);
  assert.ok(post.includes("AskUserQuestion"));
});

test("stripClientHooks('trae-cn') removes all trae-cn workled groups and reports changed", () => {
  const merged = mergeTraeCn(undefined);
  const { config, changed } = stripTraeCn(merged);
  assert.equal(changed, true);
  for (const ev of SPEC_EVENTS) {
    assert.ok(!config.hooks[ev], `${ev} fully stripped`);
  }
  // The pure helper empties the hooks map; deleting the now-empty `hooks` key
  // is left to the caller (uninstallTraeCn), so it stays an empty object.
  assert.deepEqual(config.hooks, {});
});

test("stripClientHooks('trae-cn') is a no-op when there are no trae-cn workled groups", () => {
  const cfg = { version: 1, hooks: { Stop: [{ hooks: [{ type: "command", command: "echo x" }] }] } };
  const { config, changed } = stripTraeCn(cfg);
  assert.equal(changed, false);
  assert.deepEqual(config, cfg);
});

test("stripClientHooks('trae-cn') keeps unrelated hooks while dropping only trae-cn groups", () => {
  const cfg = {
    version: 1,
    hooks: {
      Stop: [
        { hooks: [{ type: "command", command: "echo keep-me" }] },
        { hooks: [{ type: "command", command: cmdFor("Stop") }] },
      ],
      UserPromptSubmit: [{ hooks: [{ type: "command", command: cmdFor("UserPromptSubmit") }] }],
    },
  };
  const { config, changed } = stripTraeCn(cfg);
  assert.equal(changed, true);
  assert.deepEqual(config.hooks.Stop, [{ hooks: [{ type: "command", command: "echo keep-me" }] }]);
  assert.ok(!config.hooks.UserPromptSubmit, "UserPromptSubmit fully stripped");
});

// The shared client-parameterised core (mergeClientHooks / stripClientHooks)
// backs BOTH workbuddy and trae-cn, differing only in the `client` marker. These
// tests lock in that behaviour: isolation between clients, no version leakage
// for workbuddy, and a clean round-trip.
const wbCmdFor = (e) => `node workled hook --event ${e} --client workbuddy`;

test("mergeClientHooks('workbuddy') builds hooks without injecting a schema version", () => {
  const merged = mergeClientHooks({ note: "keep" }, { client: "workbuddy", commandForEvent: wbCmdFor });
  assert.equal(merged.note, "keep", "unrelated settings preserved");
  assert.deepEqual(merged.version, undefined, "version not injected for workbuddy");
  assert.ok(merged.hooks.UserPromptSubmit[0].hooks[0].command.includes("--client workbuddy"));
});

test("stripClientHooks is client-isolated: one client's strip leaves the other intact", () => {
  // Build a config carrying both a workbuddy and a trae-cn workled group.
  const wb = mergeClientHooks({}, { client: "workbuddy", commandForEvent: wbCmdFor });
  const both = mergeClientHooks(wb, { client: "trae-cn", commandForEvent: cmdFor, version: 1 });

  // Strip only workbuddy -> trae-cn groups survive.
  const noWb = stripClientHooks(both, "workbuddy");
  assert.equal(noWb.changed, true);
  assert.ok(noWb.config.hooks.UserPromptSubmit.length, "trae-cn groups kept");
  assert.ok(
    noWb.config.hooks.UserPromptSubmit.every((g) => g.hooks[0].command.includes("--client trae-cn")),
    "only trae-cn groups remain"
  );
  assert.ok(!noWb.config.hooks.UserPromptSubmit.some((g) => g.hooks[0].command.includes("--client workbuddy")));

  // Strip only trae-cn -> workbuddy groups survive.
  const noTrae = stripClientHooks(both, "trae-cn");
  assert.equal(noTrae.changed, true);
  assert.ok(noTrae.config.hooks.UserPromptSubmit.length, "workbuddy groups kept");
  assert.ok(
    noTrae.config.hooks.UserPromptSubmit.every((g) => g.hooks[0].command.includes("--client workbuddy")),
    "only workbuddy groups remain"
  );
});

test("mergeClientHooks('workbuddy') is idempotent and round-trips clean", () => {
  const once = mergeClientHooks({}, { client: "workbuddy", commandForEvent: wbCmdFor });
  const twice = mergeClientHooks(once, { client: "workbuddy", commandForEvent: wbCmdFor });
  assert.equal(twice.hooks.Notification.length, once.hooks.Notification.length);
  const { config, changed } = stripClientHooks(twice, "workbuddy");
  assert.equal(changed, true);
  assert.deepEqual(config.hooks, {});
  assert.deepEqual(config.version, undefined);
});
