const DEFAULTS = {
  maxFrameBytes: 256 * 1024,
  rateWindowMs: 10_000,
  maxMessagesPerWindow: 120,
  maxBytesPerWindow: 1024 * 1024,
  maxBrowserSocketsPerThread: 8,
  idleTtlMs: 30 * 60 * 1000,
  maxMalformedFrames: 3,
  maxPendingBytes: 1024 * 1024,
};

export const CODEX_WS_CLOSE_CODES = Object.freeze({
  oversizedFrame: 4400,
  rateLimited: 4401,
  tooManySockets: 4402,
  idleTimeout: 4403,
  malformedFrames: 4404,
  operatorDisabled: 4405,
  pendingBytes: 4406,
});

function positiveInt(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ""), 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function parseAgentSet(value) {
  if (!value) return new Set();
  return new Set(
    String(value)
      .split(",")
      .map((part) => part.trim())
      .filter(Boolean),
  );
}

export function createCodexWsAbuseLimitConfig(env = process.env) {
  return {
    maxFrameBytes: positiveInt(env.LDM_CODEX_WS_MAX_FRAME_BYTES, DEFAULTS.maxFrameBytes),
    rateWindowMs: positiveInt(env.LDM_CODEX_WS_RATE_WINDOW_MS, DEFAULTS.rateWindowMs),
    maxMessagesPerWindow: positiveInt(env.LDM_CODEX_WS_MAX_MESSAGES_PER_WINDOW, DEFAULTS.maxMessagesPerWindow),
    maxBytesPerWindow: positiveInt(env.LDM_CODEX_WS_MAX_BYTES_PER_WINDOW, DEFAULTS.maxBytesPerWindow),
    maxBrowserSocketsPerThread: positiveInt(
      env.LDM_CODEX_WS_MAX_BROWSER_SOCKETS_PER_THREAD,
      DEFAULTS.maxBrowserSocketsPerThread,
    ),
    idleTtlMs: positiveInt(env.LDM_CODEX_WS_IDLE_TTL_MS, DEFAULTS.idleTtlMs),
    maxMalformedFrames: positiveInt(env.LDM_CODEX_WS_MAX_MALFORMED_FRAMES, DEFAULTS.maxMalformedFrames),
    maxPendingBytes: positiveInt(env.LDM_CODEX_WS_MAX_PENDING_BYTES, DEFAULTS.maxPendingBytes),
    killSwitchAll: env.LDM_CODEX_WS_KILL_SWITCH_ALL === "1",
    killSwitchAgents: parseAgentSet(env.LDM_CODEX_WS_KILL_SWITCH_AGENTS),
  };
}

export function isCodexWsAgentDisabled(config, agentId) {
  return !!(
    config?.killSwitchAll
    || (typeof agentId === "string" && config?.killSwitchAgents?.has(agentId))
  );
}

function rejected(code, reason) {
  return { ok: false, code, reason };
}

export function createCodexWsConnectionGuard({ config, agentId, now = Date.now }) {
  let windowStartMs = now();
  let messagesInWindow = 0;
  let bytesInWindow = 0;
  let malformedFrames = 0;
  let lastActivityMs = windowStartMs;

  function resetWindow(nowMs) {
    windowStartMs = nowMs;
    messagesInWindow = 0;
    bytesInWindow = 0;
  }

  return {
    observeFrame(byteLength, nowMs = now()) {
      if (isCodexWsAgentDisabled(config, agentId)) {
        return rejected(CODEX_WS_CLOSE_CODES.operatorDisabled, "operator disabled");
      }
      if (byteLength > config.maxFrameBytes) {
        return rejected(CODEX_WS_CLOSE_CODES.oversizedFrame, "frame too large");
      }
      if (nowMs - windowStartMs > config.rateWindowMs) {
        resetWindow(nowMs);
      }
      messagesInWindow += 1;
      bytesInWindow += byteLength;
      lastActivityMs = nowMs;
      if (messagesInWindow > config.maxMessagesPerWindow) {
        return rejected(CODEX_WS_CLOSE_CODES.rateLimited, "message rate limit");
      }
      if (bytesInWindow > config.maxBytesPerWindow) {
        return rejected(CODEX_WS_CLOSE_CODES.rateLimited, "byte rate limit");
      }
      return { ok: true };
    },
    observeMalformed(nowMs = now()) {
      lastActivityMs = nowMs;
      malformedFrames += 1;
      if (malformedFrames > config.maxMalformedFrames) {
        return rejected(CODEX_WS_CLOSE_CODES.malformedFrames, "malformed frame limit");
      }
      return { ok: true };
    },
    observePendingBytes(bufferedAmount) {
      if (bufferedAmount > config.maxPendingBytes) {
        return rejected(CODEX_WS_CLOSE_CODES.pendingBytes, "pending byte limit");
      }
      return { ok: true };
    },
    observeIdle(nowMs = now()) {
      if (nowMs - lastActivityMs > config.idleTtlMs) {
        return rejected(CODEX_WS_CLOSE_CODES.idleTimeout, "idle timeout");
      }
      return { ok: true };
    },
  };
}

export function codexWsFrameByteLength(data) {
  if (typeof data === "string") return Buffer.byteLength(data);
  if (Buffer.isBuffer(data)) return data.length;
  if (data instanceof ArrayBuffer) return data.byteLength;
  if (ArrayBuffer.isView(data)) return data.byteLength;
  return Buffer.byteLength(String(data ?? ""));
}

export function formatCodexWsLimitLog({ agentId, threadId, connectionId, reason }) {
  return (
    "codex-relay: websocket limit"
    + " reason=" + String(reason || "unknown").slice(0, 64)
    + " agent=" + String(agentId || "<none>").slice(0, 96)
    + " thread=" + String(threadId || "<none>").slice(0, 96)
    + " conn=" + String(connectionId || "<none>").slice(0, 64)
  );
}
