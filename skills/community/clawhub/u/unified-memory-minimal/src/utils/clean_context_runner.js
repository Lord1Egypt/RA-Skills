/**
 * CleanContextRunner: executes LLM calls in a fully isolated context
 * using runEmbeddedPiAgent (same mechanism as the llm-task extension).
 *
 * Guarantees:
 * 1. Blank conversation history (temporary session file)
 * 2. Independent system prompt (only the task prompt)
 * 3. No tool calls (tools restricted to minimal read-only set to avoid empty tools[] rejection by some providers)
 * 4. No contamination from the main agent's context
 */

import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";

/**
 * Resolve a preferred temporary directory for memory-tdai operations.
 *
 * Previously imported from `openclaw/plugin-sdk` as `resolvePreferredOpenClawTmpDir`,
 * but that export was removed in openclaw 2026.2.23+. This local implementation
 * provides equivalent behavior:
 *   1. Try `/tmp/openclaw` (if writable)
 *   2. Fall back to `os.tmpdir()/openclaw-<uid>`
 * @returns {string}
 */
function resolveOpenClawTmpDir() {
  const POSIX_DIR = "/tmp/openclaw";
  try {
    if (fsSync.existsSync(POSIX_DIR)) {
      fsSync.accessSync(POSIX_DIR, fsSync.constants.W_OK | fsSync.constants.X_OK);
      return POSIX_DIR;
    }
    // Try to create it
    fsSync.mkdirSync(POSIX_DIR, { recursive: true, mode: 0o700 });
    return POSIX_DIR;
  } catch {
    // Fall back to os.tmpdir()
    const uid = typeof process.getuid === "function" ? process.getuid() : undefined;
    const suffix = uid === undefined ? "openclaw" : `openclaw-${uid}`;
    const fallback = path.join(os.tmpdir(), suffix);
    fsSync.mkdirSync(fallback, { recursive: true });
    return fallback;
  }
}

const TAG = "[memory-tdai] [runner]";

/**
 * @typedef {Object} RunnerLogger
 * @property {(message: string) => void} [debug]
 * @property {(message: string) => void} info
 * @property {(message: string) => void} warn
 * @property {(message: string) => void} error
 */

/**
 * Dynamic import type — runEmbeddedPiAgent is an internal API
 * @typedef {(params: Record<string, unknown>) => Promise<unknown>} RunEmbeddedPiAgentFn
 */

// ── Core import (mirrors voice-call/core-bridge.ts — dist/ only, no jiti) ──

/** @type {string | null} */
let _rootCache = null;

/**
 * @param {string} startDir
 * @param {string} name
 * @returns {string | null}
 */
function findPackageRoot(startDir, name) {
  let dir = startDir;
  for (;;) {
    const pkgPath = path.join(dir, "package.json");
    try {
      if (fsSync.existsSync(pkgPath)) {
        const raw = fsSync.readFileSync(pkgPath, "utf8");
        const pkg = JSON.parse(raw);
        if (pkg.name === name) return dir;
      }
    } catch { /* ignore */ }
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

/**
 * @returns {string}
 */
function resolveOpenClawRoot() {
  if (_rootCache) return _rootCache;
  const override = process.env.OPENCLAW_ROOT?.trim();
  if (override) { _rootCache = override; return override; }

  const candidates = new Set();
  if (process.argv[1]) candidates.add(path.dirname(process.argv[1]));
  candidates.add(process.cwd());
  try { candidates.add(path.dirname(fileURLToPath(import.meta.url))); } catch { /* ignore */ }

  for (const start of candidates) {
    const found = findPackageRoot(start, "openclaw");
    if (found) { _rootCache = found; return found; }
  }
  throw new Error("Unable to resolve OpenClaw root. Set OPENCLAW_ROOT or run `pnpm build`.");
}

/** @type {Promise<RunEmbeddedPiAgentFn> | null} */
let _loadPromise = null;

/**
 * @param {RunnerLogger} [logger]
 * @returns {Promise<RunEmbeddedPiAgentFn>}
 */
function loadRunEmbeddedPiAgent(logger) {
  if (_loadPromise) return _loadPromise;

  _loadPromise = (async () => {
    const t0 = Date.now();
    const distPath = path.join(resolveOpenClawRoot(), "dist", "extensionAPI.js");
    if (!fsSync.existsSync(distPath)) {
      throw new Error(`Missing core module at ${distPath}. Run \`pnpm build\` or install the official package.`);
    }
    const mod = await import(pathToFileURL(distPath).href);
    if (typeof mod.runEmbeddedPiAgent !== "function") {
      throw new Error("runEmbeddedPiAgent not exported from dist/extensionAPI.js");
    }
    logger?.info(`${TAG} loadRunEmbeddedPiAgent: dist/ import OK (${Date.now() - t0}ms)`);
    return mod.runEmbeddedPiAgent;
  })();

  _loadPromise.catch(() => { _loadPromise = null; });
  return _loadPromise;
}

/**
 * Pre-warm the embedded agent import. Call this during plugin init to avoid
 * the cold-start penalty on the first actual extraction run.
 * Returns immediately (fire-and-forget) — errors are swallowed.
 * @param {RunnerLogger} [logger]
 */
export function prewarmEmbeddedAgent(logger) {
  loadRunEmbeddedPiAgent(logger).catch((err) => {
    logger?.warn(`${TAG} prewarmEmbeddedAgent: failed (non-fatal): ${err instanceof Error ? err.message : String(err)}`);
  });
}

/**
 * @param {Array<{ text?: string; isError?: boolean }> | undefined} payloads
 * @returns {string}
 */
function collectText(payloads) {
  const texts = (payloads ?? [])
    .filter((p) => !p.isError && typeof p.text === "string")
    .map((p) => p.text ?? "");
  return texts.join("\n").trim();
}

// ── Model resolution utilities ──

/**
 * Parsed model reference: { provider, model }
 * @typedef {Object} ModelRef
 * @property {string} provider
 * @property {string} model
 */

/**
 * Parse a "provider/model" string into its components.
 * Returns undefined if the input is empty or doesn't contain a "/".
 *
 * Examples:
 *   "azure/gpt-5.2-chat"          → { provider: "azure", model: "gpt-5.2-chat" }
 *   "custom-host/org/model-v2"    → { provider: "custom-host", model: "org/model-v2" }
 *   ""                            → undefined
 *   "bare-model-name"             → undefined (no "/" — may be an alias)
 * @param {string | undefined} raw
 * @returns {ModelRef | undefined}
 */
export function parseModelRef(raw) {
  if (!raw) return undefined;
  const trimmed = raw.trim();
  if (!trimmed) return undefined;

  const slashIdx = trimmed.indexOf("/");
  if (slashIdx <= 0 || slashIdx === trimmed.length - 1) return undefined;

  return {
    provider: trimmed.slice(0, slashIdx),
    model: trimmed.slice(slashIdx + 1),
  };
}

/**
 * Resolve the user's default model from the main OpenClaw config.
 *
 * Resolution order:
 * 1. Read `agents.defaults.model` (string or { primary })
 * 2. If the value contains "/", parse directly
 * 3. If not (may be an alias), look up in `agents.defaults.models` alias table
 * 4. Return undefined if nothing resolves — let the core use its built-in default
 * @param {unknown} config
 * @returns {ModelRef | undefined}
 */
export function resolveModelFromMainConfig(config) {
  if (!config || typeof config !== "object") return undefined;

  const cfg = config;
  const agents = cfg.agents;
  if (!agents || typeof agents !== "object") return undefined;

  const defaults = agents.defaults;
  if (!defaults || typeof defaults !== "object") return undefined;

  // Step 1: extract raw model value (string | { primary?: string })
  const modelCfg = defaults.model;
  let raw;
  if (typeof modelCfg === "string") {
    raw = modelCfg.trim();
  } else if (modelCfg && typeof modelCfg === "object") {
    const primary = modelCfg.primary;
    raw = typeof primary === "string" ? primary.trim() : undefined;
  }
  if (!raw) return undefined;

  // Step 2: try direct "provider/model" parse
  const direct = parseModelRef(raw);
  if (direct) return direct;

  // Step 3: alias lookup — raw doesn't contain "/", check agents.defaults.models
  const models = defaults.models;
  if (!models || typeof models !== "object") return undefined;

  const rawLower = raw.toLowerCase();
  for (const [key, entry] of Object.entries(models)) {
    if (!entry || typeof entry !== "object") continue;
    const alias = entry.alias;
    if (typeof alias !== "string") continue;
    if (alias.trim().toLowerCase() !== rawLower) continue;

    // key is "provider/model" format
    const resolved = parseModelRef(key);
    if (resolved) return resolved;
  }

  return undefined;
}

/**
 * @typedef {Object} CleanContextRunnerOptions
 * @property {unknown} config - OpenClawConfig
 * @property {string} [provider]
 * @property {string} [model]
 * @property {string} [modelRef] - Convenience field: full "provider/model" string.
 *   Takes precedence over separate `provider`/`model` fields.
 * @property {boolean} [enableTools] - Allow the LLM to use tools. Default: false
 * @property {RunnerLogger} [logger]
 */

/**
 * Stable empty directory used as default workspaceDir so that:
 * 1. Bootstrap/skills scans find nothing → clean LLM context
 * 2. The path is constant → plugin cacheKey stays stable (no re-registration)
 * @type {string | undefined}
 */
let _cleanWorkspaceDir = undefined;

/**
 * @returns {Promise<string>}
 */
async function getCleanWorkspaceDir() {
  if (_cleanWorkspaceDir) return _cleanWorkspaceDir;
  const dir = path.join(resolveOpenClawTmpDir(), "memory-tdai-clean-workspace");
  await fs.mkdir(dir, { recursive: true });
  _cleanWorkspaceDir = dir;
  return dir;
}

export class CleanContextRunner {
  /** @type {CleanContextRunnerOptions} */
  options;
  /** @type {RunnerLogger | undefined} */
  logger;
  /** Resolved provider after modelRef / config fallback */
  resolvedProvider;
  /** Resolved model after modelRef / config fallback */
  resolvedModel;

  /**
   * @param {CleanContextRunnerOptions} options
   */
  constructor(options) {
    this.options = options;
    this.logger = options.logger;

    // Model resolution priority:
    // 1. modelRef ("provider/model" string)  — highest
    // 2. explicit provider + model fields
    // 3. main config agents.defaults.model   — automatic fallback
    // 4. undefined (let core use built-in default)
    const fromRef = parseModelRef(options.modelRef);
    if (fromRef) {
      this.resolvedProvider = fromRef.provider;
      this.resolvedModel = fromRef.model;
    } else if (options.provider || options.model) {
      this.resolvedProvider = options.provider;
      this.resolvedModel = options.model;
    } else {
      // No explicit model specified — fall back to main config
      const fromConfig = resolveModelFromMainConfig(options.config);
      if (fromConfig) {
        this.resolvedProvider = fromConfig.provider;
        this.resolvedModel = fromConfig.model;
        this.logger?.debug?.(
          `${TAG} Using model from main config: ${fromConfig.provider}/${fromConfig.model}`,
        );
      }
      // else: both undefined → core will use its built-in default (anthropic/claude-opus-4-6)
    }
  }

  /**
   * Run a prompt in a fully isolated clean context.
   * Returns the LLM's text output.
   *
   * When `workspaceDir` is provided it overrides the default `process.cwd()`,
   * letting the LLM's file-tool calls resolve paths relative to a custom root.
   * @param {Object} params
   * @param {string} params.prompt
   * @param {string} [params.systemPrompt] - Optional system prompt. When provided, `prompt` is used as the user message.
   * @param {string} params.taskId
   * @param {number} [params.timeoutMs]
   * @param {number} [params.maxTokens]
   * @param {string} [params.workspaceDir]
   * @returns {Promise<string>}
   */
  async run(params) {
    const runStartMs = Date.now();
    this.logger?.debug?.(`${TAG} run() start: taskId=${params.taskId}, timeout=${params.timeoutMs ?? 120_000}ms, tools=${this.options.enableTools ? "enabled" : "disabled"}, workspaceDir=${params.workspaceDir ?? "(default)"}`);

    const tmpDir = await fs.mkdtemp(
      path.join(resolveOpenClawTmpDir(), `memory-tdai-${params.taskId}-`),
    );
    const cleanWorkspace = params.workspaceDir ?? await getCleanWorkspaceDir();
    this.logger?.debug?.(`${TAG} run() tmpDir=${tmpDir}, cleanWorkspace=${cleanWorkspace}`);

    try {
      const sessionFile = path.join(tmpDir, "session.json");

      // Phase 1: Load runEmbeddedPiAgent (fast if dist/ exists or already cached)
      const importStartMs = Date.now();
      const runEmbeddedPiAgent = await loadRunEmbeddedPiAgent(this.logger);
      const importElapsedMs = Date.now() - importStartMs;
      this.logger?.debug?.(`${TAG} run() dynamic import phase: ${importElapsedMs}ms`);

      // Derive a config with plugins disabled to prevent loadOpenClawPlugins
      // from re-registering plugins when the workspaceDir differs from the
      // gateway's original workspace (cacheKey mismatch triggers full reload).
      //
      // Security: restrict available tools to the minimal set needed for
      // scene extraction (read/write/edit). This prevents the LLM from
      // accessing exec, sessions, browser, cron, or any other powerful tools.
      // File deletion is handled via "soft-delete" (write empty) + cleanup afterward.
      const cleanConfig = {
        ...this.options.config,
        plugins: {
          ...(this.options.config?.plugins ?? {}),
          enabled: false,
        },
        tools: {
          ...(this.options.config?.tools ?? {}),
          // When enableTools=false we still keep one lightweight read-only tool
          // so that the tools array sent to the API is non-empty.
          // Some providers (e.g. qwencode) reject tools:[] with minItems:1 validation.
          allow: this.options.enableTools ? ["read", "write", "edit"] : ["read"],
        },
      };

      // Build the effective prompt:
      // If systemPrompt is provided, pass it as a separate parameter to the agent
      // and use `prompt` as the user message. Fallback: prepend to prompt if the
      // embedded agent doesn't support systemPrompt natively.
      const effectivePrompt = params.systemPrompt
        ? `${params.systemPrompt}\n\n---\n\n${params.prompt}`
        : params.prompt;

      const ts = Date.now();
      const sessionId = `memory-${params.taskId}-session-${ts}`;
      const runId = `memory-${params.taskId}-run-${ts}`;
      this.logger?.debug?.(`${TAG} run() starting embedded agent: sessionId=${sessionId}, runId=${runId}, provider=${this.resolvedProvider ?? "(default)"}, model=${this.resolvedModel ?? "(default)"}`);

      // Phase 2: Embedded agent run (LLM call + tool calls)
      const agentStartMs = Date.now();
      const result = await runEmbeddedPiAgent({
        sessionId,
        sessionFile,
        workspaceDir: cleanWorkspace,
        config: cleanConfig,
        prompt: effectivePrompt,
        systemPrompt: params.systemPrompt,
        timeoutMs: params.timeoutMs ?? 120_000,
        runId,
        provider: this.resolvedProvider,
        model: this.resolvedModel,
        // Do NOT pass disableTools:true — that produces tools:[] which some
        // providers (qwencode) reject with "[] is too short - 'tools'".
        // Instead rely on cleanConfig.tools.allow to restrict the tool set
        // to a minimal read-only tool (when enableTools=false).
        disableTools: false,
        streamParams: {
          maxTokens: params.maxTokens,
        },
      });
      const agentElapsedMs = Date.now() - agentStartMs;
      this.logger?.debug?.(`${TAG} run() embedded agent completed: ${agentElapsedMs}ms`);

      // Phase 3: Collect output
      const text = collectText(result?.payloads);
      const totalMs = Date.now() - runStartMs;

      if (!text) {
        // Empty output is normal when the LLM decides there is nothing to
        // extract (e.g. trivial greetings).  Log a warning instead of
        // throwing so the caller can handle it gracefully.
        this.logger?.warn?.(`${TAG} run() empty output after ${totalMs}ms (import=${importElapsedMs}ms, agent=${agentElapsedMs}ms) — treating as empty result`);
        return "";
      }

      this.logger?.debug?.(`${TAG} run() completed: ${totalMs}ms total (import=${importElapsedMs}ms, agent=${agentElapsedMs}ms), output=${text.length} chars`);
      return text;
    } catch (err) {
      const totalMs = Date.now() - runStartMs;
      this.logger?.error(`${TAG} run() failed after ${totalMs}ms: ${err instanceof Error ? err.stack ?? err.message : String(err)}`);
      throw err;
    } finally {
      await fs.rm(tmpDir, { recursive: true, force: true }).catch(() => {});
    }
  }
}
