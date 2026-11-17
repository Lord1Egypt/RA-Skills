// workled-dsh-plugin — native Cordis plugin for DeepSeek Harness (dsh).
//
// Listens to the dsh native Cordis events (verified against agent-loop and
// tools packages in the harness source) and drives the workled status LED
// by issuing MCP tools/call HTTP requests directly to the workled device.
//
// Dispatch types (verified against dsh source):
//   agent/session-start  -> concurrent (emitAgentEvent) — fire & forget
//   agent/pre-step       -> WATERFALL (dispatch.waterfall) — MUST call next()
//   tools/pre-execute    -> WATERFALL (ctx.waterfall) — MUST call next()
//   tools/post-execute   -> WATERFALL (ctx.waterfall) — MUST call next()
//   agent/turn-stopping  -> serial (dispatch.serial) — fire & forget
//   agent/error          -> concurrent (dispatch.emit) — fire & forget
//   subagent/start       -> concurrent (dispatch("emit")) — fire & forget
//   subagent/end         -> concurrent (dispatch("emit")) — fire & forget
//
// Event mapping:
//   agent/session-start  -> thinking   (session opened)
//   agent/pre-step       -> thinking   (every step, including user submit)
//   tools/pre-execute    -> waiting iff tool name contains ask/question/...
//                        -> thinking otherwise
//   tools/post-execute   -> thinking
//   agent/turn-stopping  -> idle       (waiting on next user message)
//   agent/error          -> error      (fatal agent error, e.g. PI_AI_ERROR)
//   subagent/start       -> thinking
//   subagent/end         -> thinking

const WORKLED_STATE_RE = /^(thinking|idle|waiting|error)$/;

const INPUT_TOOL_KEYWORDS = [
  'question', 'confirm', 'ask', 'choose', 'select',
  'prompt', 'input', 'approval',
];

function isInputTool(name) {
  if (!name) return false;
  const n = String(name).toLowerCase();
  return INPUT_TOOL_KEYWORDS.some((k) => n.includes(k));
}

export function apply(ctx, config = {}) {
  ctx.provide('workled');
  const enabled = config.enabled !== false;
  const baseUrl = process.env.WORKLED_MCP_URL || config.url || null;
  const timeout = Number(config.timeout) || 1500;

  if (!enabled) return;
  if (!baseUrl) {
    ctx.logger?.warn?.('[workled] WORKLED_MCP_URL or config.url not set — skipping plugin mount');
    return;
  }

  let lastState = null;

  // Best-effort fire-and-forget HTTP client. workled MCP endpoint accepts
  // JSON-RPC 2.0 over POST /mcp with body:
  //   { jsonrpc: "2.0", id: N, method: "tools/call",
  //     params: { name: "set_agent_state", arguments: { state_name: S } } }
  async function setState(state) {
    if (!WORKLED_STATE_RE.test(state)) return;
    lastState = state;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    try {
      const body = JSON.stringify({
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/call',
        params: {
          name: 'set_agent_state',
          arguments: { state_name: state },
        },
      });
      await fetch(baseUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
        signal: controller.signal,
      }).catch(() => {});
    } catch {
      /* workled unreachable — intentionally swallowed */
    } finally {
      clearTimeout(timer);
    }
  }

  // Fire setState without awaiting — Cordis event listeners must not block
  // the agent loop. A plugin-global microtask queue keeps ordering roughly
  // FIFO without introducing head-of-line blocking.
  let tail = Promise.resolve();
  function fire(state) {
    tail = tail.then(() => setState(state), () => setState(state));
  }

  // ── Non-waterfall events — fire and forget ──
  ctx.on('agent/session-start', () => fire('thinking'));
  ctx.on('agent/turn-stopping', () => fire('idle'));
  ctx.on('agent/error', () => fire('error'));
  ctx.on('subagent/start', () => fire('thinking'));
  ctx.on('subagent/end', () => fire('thinking'));

  // ── Waterfall events — MUST call next() and return its result ──
  // Without next(), the waterfall chain breaks and the agent loop gets
  // undefined instead of { kind: "enter" }, causing:
  //   Cannot read properties of undefined (reading 'kind')
  ctx.on('agent/pre-step', (_payload, next) => {
    fire('thinking');
    return next();
  });

  ctx.on('tools/pre-execute', (exec, next) => {
    const name = exec?.tool?.name || exec?.name || '';
    fire(isInputTool(name) ? 'waiting' : 'thinking');
    return next();
  });

  ctx.on('tools/post-execute', (_exec, _result, next) => {
    fire('thinking');
    return next();
  });

  // Expose a read-only service for other dsh plugins that want to
  // inspect or drive the LED without going through the MCP endpoint.
  ctx.workled = {
    get lastState() { return lastState; },
    fire,
    config: Object.freeze({ ...config, url: baseUrl }),
  };
}

export default apply;