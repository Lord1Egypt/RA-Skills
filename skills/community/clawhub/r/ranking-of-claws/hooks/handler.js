const { createHash } = require("crypto");
const { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } = require("fs");
const { hostname } = require("os");
const { join } = require("path");
const https = require("https");

const API_URL = "https://rankingofclaws.angelstreet.io/api/report";
const HOME = process.env.HOME || "";
const LOG_FILE = join(HOME, ".openclaw", "ranking-hook.log");
const CONFIG_FILE = join(HOME, ".openclaw", "workspace", "skills", "ranking-of-claws", "config.json");
const STATE_FILE = join(HOME, ".openclaw", "ranking-hook-state.json");
const AGENTS_DIR = join(HOME, ".openclaw", "agents");
const REPORT_INTERVAL_MS = 10 * 60 * 1000;
const SCAN_INTERVAL_MS = 60 * 1000;
const JSONL_SCAN_WINDOW_MS = 24 * 60 * 60 * 1000;

let intervalStarted = false;
let lastReportTime = 0;

const modelDeltas = new Map();
let lastSeenByFile = new Map();

function log(message) {
  try {
    appendFileSync(LOG_FILE, `[${new Date().toISOString()}] ${message}\n`);
  } catch (_) {}
}

function getGatewayId() {
  const raw = `${hostname()}-${HOME}-openclaw`;
  return createHash("sha256").update(raw).digest("hex").slice(0, 16);
}

function safeNumber(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

function ensureDir(path) {
  try {
    mkdirSync(path, { recursive: true });
  } catch (_) {}
}

function loadConfig() {
  try {
    if (!existsSync(CONFIG_FILE)) return null;
    const parsed = JSON.parse(readFileSync(CONFIG_FILE, "utf8"));
    if (!parsed || !parsed.agent_name) return null;
    return {
      agent_name: String(parsed.agent_name).trim(),
      country: parsed.country ? String(parsed.country).toUpperCase() : "XX",
      gateway_id: parsed.gateway_id || getGatewayId(),
      registered_at: parsed.registered_at || new Date().toISOString(),
    };
  } catch (_) {
    return null;
  }
}

function registerFallback() {
  const config = {
    agent_name: hostname() || "anonymous",
    country: "XX",
    gateway_id: getGatewayId(),
    registered_at: new Date().toISOString(),
  };
  try {
    ensureDir(join(HOME, ".openclaw", "workspace", "skills", "ranking-of-claws"));
    writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), "utf8");
    log(`Created fallback config at ${CONFIG_FILE}`);
  } catch (err) {
    log(`Failed creating fallback config: ${err && err.message ? err.message : err}`);
  }
  return config;
}

function listAgentIds() {
  if (!existsSync(AGENTS_DIR)) return [];
  try {
    return readdirSync(AGENTS_DIR).filter((entry) => {
      try {
        return statSync(join(AGENTS_DIR, entry)).isDirectory();
      } catch (_) {
        return false;
      }
    });
  } catch (_) {
    return [];
  }
}

function getRecentJsonlFiles() {
  const files = [];
  const cutoff = Date.now() - JSONL_SCAN_WINDOW_MS;
  for (const agentId of listAgentIds()) {
    const sessionsDir = join(AGENTS_DIR, agentId, "sessions");
    if (!existsSync(sessionsDir)) continue;
    let entries = [];
    try {
      entries = readdirSync(sessionsDir);
    } catch (_) {
      continue;
    }
    for (const entry of entries) {
      if (!entry.endsWith(".jsonl")) continue;
      const filePath = join(sessionsDir, entry);
      try {
        if (statSync(filePath).mtimeMs >= cutoff) files.push(filePath);
      } catch (_) {}
    }
  }
  return files;
}

function parseUsage(usage) {
  if (!usage || typeof usage !== "object") return null;
  const input = safeNumber(
    usage.input !== undefined ? usage.input : usage.inputTokens !== undefined ? usage.inputTokens : usage.promptTokens
  );
  const output = safeNumber(
    usage.output !== undefined ? usage.output : usage.outputTokens !== undefined ? usage.outputTokens : usage.completionTokens
  );
  let total = safeNumber(
    usage.totalTokens !== undefined ? usage.totalTokens : usage.total !== undefined ? usage.total : usage.tokens
  );
  if (total <= 0 && (input > 0 || output > 0)) total = input + output;

  let cost = 0;
  if (usage.cost && typeof usage.cost === "object") {
    cost = safeNumber(usage.cost.total);
  } else {
    cost = safeNumber(usage.cost);
  }

  if (total <= 0 && input <= 0 && output <= 0 && cost <= 0) return null;
  return { total, input, output, cost };
}

function extractMessageRecord(obj) {
  if (!obj || typeof obj !== "object") return null;
  if (obj.type === "message" && obj.message) return obj.message;
  if (obj.message) return obj.message;
  if (obj.data && obj.data.message) return obj.data.message;
  if (obj.event && obj.event.message) return obj.event.message;
  return null;
}

function normalizeModel(message) {
  if (!message || typeof message !== "object") return "unknown";
  return (
    message.model ||
    message.modelId ||
    (message.metadata && message.metadata.model) ||
    (message.usage && message.usage.model) ||
    "unknown"
  );
}

function scanJsonlByModel(filePath) {
  const byModel = {};
  try {
    const raw = readFileSync(filePath, "utf8");
    const lines = raw.split("\n");
    for (const line of lines) {
      if (!line.trim()) continue;
      let obj;
      try {
        obj = JSON.parse(line);
      } catch (_) {
        continue;
      }

      const message = extractMessageRecord(obj);
      if (!message || message.role !== "assistant") continue;
      const usage = parseUsage(message.usage);
      if (!usage) continue;
      const model = String(normalizeModel(message));

      if (!byModel[model]) byModel[model] = { tokens: 0, input: 0, output: 0, cost: 0 };
      byModel[model].tokens += usage.total;
      byModel[model].input += usage.input;
      byModel[model].output += usage.output;
      byModel[model].cost += usage.cost;
    }
  } catch (err) {
    log(`Failed scanning ${filePath}: ${err && err.message ? err.message : err}`);
  }
  return byModel;
}

function saveState() {
  try {
    const files = {};
    for (const [key, value] of lastSeenByFile.entries()) files[key] = value;
    writeFileSync(STATE_FILE, JSON.stringify({ version: 4, files }, null, 2), "utf8");
  } catch (err) {
    log(`Failed saving state: ${err && err.message ? err.message : err}`);
  }
}

function loadState() {
  try {
    if (!existsSync(STATE_FILE)) return;
    const parsed = JSON.parse(readFileSync(STATE_FILE, "utf8"));
    if (!parsed || !parsed.files || typeof parsed.files !== "object") return;
    for (const [filePath, state] of Object.entries(parsed.files)) {
      if (!state || typeof state !== "object") continue;
      lastSeenByFile.set(filePath, {
        mtime: safeNumber(state.mtime),
        models: state.models && typeof state.models === "object" ? state.models : {},
      });
    }
    log(`Loaded state (${lastSeenByFile.size} files)`);
  } catch (err) {
    log(`Failed loading state: ${err && err.message ? err.message : err}`);
  }
}

function addDelta(model, delta) {
  const existing = modelDeltas.get(model) || { tokens: 0, input: 0, output: 0, cost: 0 };
  existing.tokens += Math.max(0, safeNumber(delta.tokens));
  existing.input += Math.max(0, safeNumber(delta.input));
  existing.output += Math.max(0, safeNumber(delta.output));
  existing.cost += Math.max(0, safeNumber(delta.cost));
  modelDeltas.set(model, existing);
}

function accumulateDeltas() {
  const files = getRecentJsonlFiles();
  for (const filePath of files) {
    let mtime = 0;
    try {
      mtime = statSync(filePath).mtimeMs;
    } catch (_) {
      continue;
    }

    const previous = lastSeenByFile.get(filePath);
    if (previous && previous.mtime >= mtime) continue;

    const currentByModel = scanJsonlByModel(filePath);
    if (!previous) {
      lastSeenByFile.set(filePath, { mtime, models: currentByModel });
      continue;
    }

    for (const [model, totals] of Object.entries(currentByModel)) {
      const prev = (previous.models && previous.models[model]) || { tokens: 0, input: 0, output: 0, cost: 0 };
      addDelta(model, {
        tokens: safeNumber(totals.tokens) - safeNumber(prev.tokens),
        input: safeNumber(totals.input) - safeNumber(prev.input),
        output: safeNumber(totals.output) - safeNumber(prev.output),
        cost: safeNumber(totals.cost) - safeNumber(prev.cost),
      });
    }

    lastSeenByFile.set(filePath, { mtime, models: currentByModel });
  }

  saveState();
}

function hasPendingDeltas() {
  for (const delta of modelDeltas.values()) {
    if (delta.tokens > 0 || delta.input > 0 || delta.output > 0 || delta.cost > 0) return true;
  }
  return false;
}

function postReport(body) {
  return new Promise((resolve) => {
    const payload = JSON.stringify(body);
    const url = new URL(API_URL);
    const request = https.request(
      {
        hostname: url.hostname,
        path: url.pathname,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(payload),
        },
        timeout: 10000,
      },
      (response) => {
        const status = response.statusCode || 0;
        response.resume();
        log(`Report model=${body.model} status=${status} tokens=${body.tokens_delta}`);
        resolve(status >= 200 && status < 300);
      }
    );
    request.on("error", (err) => {
      log(`Report failed model=${body.model}: ${err && err.message ? err.message : err}`);
      resolve(false);
    });
    request.write(payload);
    request.end();
  });
}

async function report(config) {
  if (!hasPendingDeltas()) return;
  for (const [model, delta] of modelDeltas.entries()) {
    if (delta.tokens <= 0 && delta.input <= 0 && delta.output <= 0 && delta.cost <= 0) continue;
    const ok = await postReport({
      gateway_id: config.gateway_id,
      agent_name: config.agent_name,
      country: config.country || "XX",
      tokens_delta: delta.tokens > 0 ? delta.tokens : delta.input + delta.output,
      tokens_in_delta: delta.input,
      tokens_out_delta: delta.output,
      cost_delta: delta.cost,
      model,
    });
    if (!ok) continue;
  }

  modelDeltas.clear();
  lastReportTime = Date.now();
}

function startPeriodicReporting(config) {
  if (intervalStarted) return;
  intervalStarted = true;

  loadState();
  for (const filePath of getRecentJsonlFiles()) {
    if (lastSeenByFile.has(filePath)) continue;
    const models = scanJsonlByModel(filePath);
    let mtime = 0;
    try {
      mtime = statSync(filePath).mtimeMs;
    } catch (_) {}
    lastSeenByFile.set(filePath, { mtime, models });
  }
  saveState();
  log(`Baseline loaded (${lastSeenByFile.size} files)`);

  setInterval(async () => {
    try {
      accumulateDeltas();
      if (hasPendingDeltas() && Date.now() - lastReportTime >= REPORT_INTERVAL_MS) {
        await report(config);
      }
    } catch (err) {
      log(`Tick failed: ${err && err.message ? err.message : err}`);
    }
  }, SCAN_INTERVAL_MS);
}

module.exports = async function handler(event) {
  log(`Event: type=${event && event.type} action=${event && event.action}`);

  const config = loadConfig() || registerFallback();

  if (event && event.type === "gateway" && event.action === "startup") {
    startPeriodicReporting(config);
    return;
  }

  if (event && event.type === "command" && ["new", "reset", "compact"].includes(event.action)) {
    accumulateDeltas();
    if (hasPendingDeltas()) await report(config);
  }
};
