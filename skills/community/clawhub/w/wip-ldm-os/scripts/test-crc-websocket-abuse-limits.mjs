import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import {
  CODEX_WS_CLOSE_CODES,
  codexWsFrameByteLength,
  createCodexWsAbuseLimitConfig,
  createCodexWsConnectionGuard,
  formatCodexWsLimitLog,
  isCodexWsAgentDisabled,
} from "../src/hosted-mcp/codex-relay-ws-abuse-limits.mjs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");
const deploy = readFileSync("src/hosted-mcp/deploy.sh", "utf8");

function assertContains(source, needle, label) {
  if (!source.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertBefore(source, first, second, label) {
  const firstIndex = source.indexOf(first);
  const secondIndex = firstIndex === -1 ? -1 : source.indexOf(second, firstIndex + first.length);
  if (firstIndex === -1 || secondIndex === -1 || firstIndex >= secondIndex) {
    throw new Error(`${label} expected "${first}" before "${second}"`);
  }
}

const config = createCodexWsAbuseLimitConfig({
  LDM_CODEX_WS_MAX_FRAME_BYTES: "10",
  LDM_CODEX_WS_RATE_WINDOW_MS: "100",
  LDM_CODEX_WS_MAX_MESSAGES_PER_WINDOW: "2",
  LDM_CODEX_WS_MAX_BYTES_PER_WINDOW: "15",
  LDM_CODEX_WS_MAX_BROWSER_SOCKETS_PER_THREAD: "3",
  LDM_CODEX_WS_IDLE_TTL_MS: "50",
  LDM_CODEX_WS_MAX_MALFORMED_FRAMES: "1",
  LDM_CODEX_WS_MAX_PENDING_BYTES: "20",
  LDM_CODEX_WS_KILL_SWITCH_AGENTS: "acct:blocked, acct:other",
});

assert.equal(config.maxFrameBytes, 10);
assert.equal(config.maxBrowserSocketsPerThread, 3);
assert.equal(isCodexWsAgentDisabled(config, "acct:blocked"), true);
assert.equal(isCodexWsAgentDisabled(config, "acct:allowed"), false);

let nowMs = 1_000;
const guard = createCodexWsConnectionGuard({
  config,
  agentId: "acct:allowed",
  now: () => nowMs,
});

assert.equal(guard.observeFrame(11).code, CODEX_WS_CLOSE_CODES.oversizedFrame);
assert.equal(guard.observeFrame(5).ok, true);
assert.equal(guard.observeFrame(5).ok, true);
assert.equal(guard.observeFrame(5).reason, "message rate limit");

nowMs += 101;
const byteGuard = createCodexWsConnectionGuard({ config, agentId: "acct:allowed", now: () => nowMs });
assert.equal(byteGuard.observeFrame(8).ok, true);
assert.equal(byteGuard.observeFrame(8).reason, "byte rate limit");

const malformedGuard = createCodexWsConnectionGuard({ config, agentId: "acct:allowed", now: () => nowMs });
assert.equal(malformedGuard.observeMalformed().ok, true);
assert.equal(malformedGuard.observeMalformed().code, CODEX_WS_CLOSE_CODES.malformedFrames);

const pendingGuard = createCodexWsConnectionGuard({ config, agentId: "acct:allowed", now: () => nowMs });
assert.equal(pendingGuard.observePendingBytes(21).code, CODEX_WS_CLOSE_CODES.pendingBytes);

const idleGuard = createCodexWsConnectionGuard({ config, agentId: "acct:allowed", now: () => nowMs });
assert.equal(idleGuard.observeFrame(1).ok, true);
assert.equal(idleGuard.observeIdle(nowMs + 51).code, CODEX_WS_CLOSE_CODES.idleTimeout);

const killedGuard = createCodexWsConnectionGuard({ config, agentId: "acct:blocked", now: () => nowMs });
assert.equal(killedGuard.observeFrame(1).code, CODEX_WS_CLOSE_CODES.operatorDisabled);
assert.equal(codexWsFrameByteLength(Buffer.from("hello")), 5);
assert.match(
  formatCodexWsLimitLog({
    agentId: "acct:blocked",
    threadId: "thread-a",
    connectionId: "conn-a",
    reason: "message rate limit",
  }),
  /reason=message rate limit agent=acct:blocked thread=thread-a conn=conn-a/,
);

assertContains(server, "import {", "server imports abuse module");
assertContains(server, "createCodexWsAbuseLimitConfig", "server configures websocket limits");
assertContains(server, "isCodexWsAgentDisabled(CODEX_WS_ABUSE_LIMITS, identity.agentId)", "server checks operator kill switch");
assertContains(server, "openBrowserSockets >= CODEX_WS_ABUSE_LIMITS.maxBrowserSocketsPerThread", "server limits browser sockets per thread");
assertContains(server, "createCodexWsConnectionGuard({", "server creates per-socket guard");
assertContains(server, "guard.observeFrame(codexWsFrameByteLength(data))", "server observes browser frame size and rate");
assertContains(server, "guard.observeMalformed()", "server observes malformed browser frames");
assertContains(server, "guard.observePendingBytes(daemonWs.bufferedAmount || 0)", "server observes pending daemon bytes");
assertContains(server, "guard.observeIdle()", "server observes idle connections");
assertContains(server, "closeCodexWsForLimit(ws, guardContext, decision)", "server closes idle sockets by limit");
assertContains(server, "closeCodexWsForLimit(ws, guardContext, frameDecision)", "server closes frame abuse");
assertContains(server, "closeCodexWsForLimit(ws, guardContext, malformedDecision)", "server closes malformed abuse");
assertContains(server, "closeCodexWsForLimit(ws, guardContext, pendingDecision)", "server closes pending byte abuse");
assertContains(server, "codex-relay-ws-abuse-limits.mjs", "deploy inventory includes abuse module");
assertContains(deploy, "add_file \"codex-relay-ws-abuse-limits.mjs\"", "deploy copies abuse module");

assertBefore(
  server,
  "openBrowserSockets >= CODEX_WS_ABUSE_LIMITS.maxBrowserSocketsPerThread",
  "codexRelayWss.handleUpgrade(req, socket, head, (ws) => {",
  "socket cap should run before websocket upgrade is accepted",
);
assertBefore(
  server,
  "const frameDecision = guard.observeFrame(codexWsFrameByteLength(data));",
  "let text = data.toString();",
  "frame limit should run before parsing or forwarding browser data",
);
assertBefore(
  server,
  "if (!envelope || typeof envelope !== \"object\" || Array.isArray(envelope)) {",
  "const daemonWs = codexDaemons.get(identity.agentId);",
  "malformed browser frames should not be forwarded",
);
assertBefore(
  server,
  "const pendingDecision = guard.observePendingBytes(daemonWs.bufferedAmount || 0);",
  "daemonWs.send(text);",
  "pending byte check should run before forwarding to daemon",
);

console.log("crc websocket abuse limit checks passed");
