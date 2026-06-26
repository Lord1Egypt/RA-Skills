#!/usr/bin/env node
/**
 * vaibot-guard-service (MVP)
 *
 * Local policy decision service for tool execution.
 *
 * Endpoints:
 * - GET  /health
 * - POST /v1/decide/exec
 * - POST /v1/finalize
 */

import http from "node:http";
import https from "node:https";
import { createHash, randomUUID } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const PORT = Number(process.env.VAIBOT_GUARD_PORT || 39111);
const HOST = process.env.VAIBOT_GUARD_HOST || "127.0.0.1";

const VAIBOT_LOG_RETENTION_DAYS = Math.max(1, Number(process.env.VAIBOT_LOG_RETENTION_DAYS || 14));

const WORKSPACE = process.env.VAIBOT_WORKSPACE || process.cwd();
const WORKSPACE_REAL = (() => {
  try { return fs.realpathSync(WORKSPACE); } catch { return path.resolve(WORKSPACE); }
})();
const LOG_DIR = process.env.VAIBOT_GUARD_LOG_DIR || path.join(WORKSPACE, ".vaibot-guard");
fs.mkdirSync(LOG_DIR, { recursive: true });

const SKILL_DIR = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const VAIBOT_POLICY_PATH = process.env.VAIBOT_POLICY_PATH || path.join(SKILL_DIR, "references", "policy.default.json");

function loadPolicy() {
  try {
    const raw = fs.readFileSync(VAIBOT_POLICY_PATH, "utf8");
    const j = JSON.parse(raw);
    // minimal sanity
    const denyTokens = Array.isArray(j.denyTokens) ? j.denyTokens.map(String) : [];
    const approveTokens = Array.isArray(j.approveTokens) ? j.approveTokens.map(String) : [];
    const allowlistedDomains = Array.isArray(j.allowlistedDomains) ? j.allowlistedDomains.map(String) : [];
    const denyPaths = Array.isArray(j.denyPaths) ? j.denyPaths.map(String) : [];
    const redactPatterns = Array.isArray(j.redactPatterns) ? j.redactPatterns.map(String) : [];
    const redactEnvKeyPatterns = Array.isArray(j.redactEnvKeyPatterns) ? j.redactEnvKeyPatterns.map(String) : [];
    const fileMutationOutsideWorkspaceAction = (j.fileMutationOutsideWorkspaceAction === "approve" ? "approve" : "deny");
    const fileMutationDeniedPathAction = (j.fileMutationDeniedPathAction === "approve" ? "approve" : "deny");
    return { version: String(j.version || ""), denyTokens, approveTokens, allowlistedDomains, denyPaths, redactPatterns, redactEnvKeyPatterns, fileMutationOutsideWorkspaceAction, fileMutationDeniedPathAction };
  } catch (e) {
    // fail closed if policy cannot be loaded
    console.error(`[vaibot-guard] failed to load policy from ${VAIBOT_POLICY_PATH}: ${e?.message || e}`);
    return null;
  }
}

const POLICY = loadPolicy();
if (!POLICY) process.exit(2);

const DENY_TOKENS = POLICY.denyTokens;
const APPROVE_TOKENS = POLICY.approveTokens;
const ALLOWLISTED_DOMAINS = POLICY.allowlistedDomains;
const DENY_PATHS = POLICY.denyPaths;
const FILE_MUTATION_OUTSIDE_WORKSPACE_ACTION = POLICY.fileMutationOutsideWorkspaceAction || "deny";
const FILE_MUTATION_DENIED_PATH_ACTION = POLICY.fileMutationDeniedPathAction || "deny";

const VAIBOT_API_URL = process.env.VAIBOT_API_URL || ""; // e.g. https://www.vaibot.io/api
const VAIBOT_API_KEY = process.env.VAIBOT_API_KEY || ""; // bearer token
const VAIBOT_PROVE_MODEL = process.env.VAIBOT_PROVE_MODEL || "vaibot-guard"; // /api/prove requires model

// Persist run context so finalize receipts can include intent+decision+result even across service restarts.
// Stored under VAIBOT_GUARD_LOG_DIR as: runctx/<runId>.json
const RUNCTX_DIR = path.join(LOG_DIR, "runctx");
fs.mkdirSync(RUNCTX_DIR, { recursive: true });

// Persist approvals so humans can approve/deny actions out-of-band (chat commands).
// Stored under VAIBOT_GUARD_LOG_DIR as: approvals/<approvalId>.json
const APPROVAL_DIR = path.join(LOG_DIR, "approvals");
fs.mkdirSync(APPROVAL_DIR, { recursive: true });

const VAIBOT_APPROVAL_TTL_MS = Math.max(30_000, Number(process.env.VAIBOT_APPROVAL_TTL_MS || 5 * 60_000));

function approvalPath(approvalId) {
  return path.join(APPROVAL_DIR, `${approvalId}.json`);
}

function writeApproval(rec) {
  const p = approvalPath(rec.approvalId);
  const tmp = p + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(rec, null, 2));
  fs.renameSync(tmp, p);
}

function readApproval(approvalId) {
  try {
    const raw = fs.readFileSync(approvalPath(approvalId), "utf8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function listApprovals({ status, sessionId } = {}) {
  const out = [];
  for (const ent of fs.readdirSync(APPROVAL_DIR, { withFileTypes: true })) {
    if (!ent.isFile() || !ent.name.endsWith(".json")) continue;
    const approvalId = ent.name.slice(0, -5);
    const rec = readApproval(approvalId);
    if (!rec) continue;

    // expire pending approvals
    if (rec.status === "pending" && rec.expiresAt && Date.now() > Date.parse(rec.expiresAt)) {
      rec.status = "expired";
      writeApproval(rec);
    }

    if (status && rec.status !== status) continue;
    if (sessionId && rec.sessionId !== sessionId) continue;
    out.push(rec);
  }
  // newest first
  out.sort((a, b) => Date.parse(b.createdAt || 0) - Date.parse(a.createdAt || 0));
  return out;
}

function createApproval({ sessionId, kind, reason, request, approvalId: approvalIdIn }) {
  const approvalId = String(approvalIdIn || `appr_${randomUUID()}`);
  const createdAt = nowIso();
  const expiresAt = new Date(Date.now() + VAIBOT_APPROVAL_TTL_MS).toISOString();

  const rec = {
    schema: "vaibot-guard/approval@0.1",
    approvalId,
    sessionId,
    kind,
    reason,
    status: "pending",
    createdAt,
    expiresAt,
    request,
    usedAt: null,
    resolvedAt: null,
  };

  writeApproval(rec);
  return rec;
}

function resolveApproval({ approvalId, action }) {
  const rec = readApproval(approvalId);
  if (!rec) return { ok: false, error: "Approval not found" };

  // expire pending approvals
  if (rec.status === "pending" && rec.expiresAt && Date.now() > Date.parse(rec.expiresAt)) {
    rec.status = "expired";
    writeApproval(rec);
  }

  if (rec.status !== "pending") {
    return { ok: false, error: `Cannot resolve approval in status '${rec.status}'` };
  }

  if (action === "approve") rec.status = "approved";
  else if (action === "deny") rec.status = "denied";
  else return { ok: false, error: "Invalid action" };

  rec.resolvedAt = nowIso();
  writeApproval(rec);

  return { ok: true, approvalId: rec.approvalId, status: rec.status, expiresAt: rec.expiresAt, reason: rec.reason, request: rec.request };
}

function markApprovalUsed({ approvalId }) {
  const rec = readApproval(approvalId);
  if (!rec) return;
  rec.status = "used";
  rec.usedAt = nowIso();
  writeApproval(rec);
}

function runCtxPath(runId) {
  return path.join(RUNCTX_DIR, `${runId}.json`);
}

function writeRunContext(runId, ctx) {
  const p = runCtxPath(runId);
  const tmp = p + ".tmp";
  fs.writeFileSync(tmp, stableStringify(ctx) + "\n");
  fs.renameSync(tmp, p);
}

function readRunContext(runId) {
  const p = runCtxPath(runId);
  if (!fs.existsSync(p)) return null;
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return null;
  }
}

function deleteRunContext(runId) {
  const p = runCtxPath(runId);
  try { fs.rmSync(p); } catch {}
}

// Local service auth (recommended): when set, require bearer token for all mutating endpoints.
const VAIBOT_GUARD_TOKEN = process.env.VAIBOT_GUARD_TOKEN || "";

// Prove modes:
// - off: never call /prove
// - best-effort: call /prove but do not block on failure
// - required: if prove fails (or config missing) for high-risk actions, deny (fail-closed)
const VAIBOT_PROVE_MODE = (process.env.VAIBOT_PROVE_MODE || "best-effort").toLowerCase();

function sha256(s) {
  return createHash("sha256").update(s).digest("hex");
}

// Reserved for future improvements (e.g., migrating checkpoint hashing to SHA3-512).
// For now, keep checkpoint hashing consistent with the Merkle/event hashing (sha256).
const VAIBOT_CHECKPOINT_HASH_ALG = (process.env.VAIBOT_CHECKPOINT_HASH_ALG || "").toLowerCase();
function hashCheckpoint(data) {
  // Intentionally ignore VAIBOT_CHECKPOINT_HASH_ALG for now (future migration knob).
  return sha256(data);
}

// Deterministic JSON serialization (stable key order) for hashing.
function stableStringify(value) {
  if (value === null || value === undefined) return JSON.stringify(value);
  if (typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map((v) => stableStringify(v)).join(",") + "]";
  const keys = Object.keys(value).sort();
  return "{" + keys.map((k) => JSON.stringify(k) + ":" + stableStringify(value[k])).join(",") + "}";
}

function nowIso() {
  return new Date().toISOString();
}

function json(res, statusCode, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(statusCode, {
    "content-type": "application/json; charset=utf-8",
    "content-length": Buffer.byteLength(body),
  });
  res.end(body);
}

function getBearer(req) {
  const h = req.headers["authorization"] || req.headers["Authorization"];
  if (!h) return "";
  const s = Array.isArray(h) ? h[0] : String(h);
  const m = s.match(/^Bearer\s+(.+)$/i);
  return m ? m[1].trim() : "";
}

function requireAuth(req, res) {
  if (!VAIBOT_GUARD_TOKEN) return true; // auth disabled
  const bearer = getBearer(req);
  const alt = req.headers["x-vaibot-guard-token"];
  const token = bearer || (Array.isArray(alt) ? alt[0] : (alt ? String(alt) : ""));
  if (token !== VAIBOT_GUARD_TOKEN) {
    json(res, 401, { ok: false, error: "Unauthorized" });
    return false;
  }
  return true;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
      if (data.length > 1024 * 1024) {
        reject(new Error("body too large"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

// ---- Policy (loaded at startup; restart service to apply policy changes)

function matchToken(tokens, joined) {
  return tokens.find((t) => new RegExp(`\\b${t}\\b`, "i").test(joined));
}

// (policy helpers moved below: isDomainAllowlisted / isDeniedPath)

function validateIntent(intent) {
  if (!intent || typeof intent !== "object") return "Missing intent";
  // Minimal fields per SKILL.md schema (relaxed: allow extra fields)
  const required = ["tool", "action", "command", "cwd"];
  for (const k of required) {
    if (!(k in intent)) return `intent missing field: ${k}`;
  }
  return null;
}

function normalizeCwdForIntent(intentCwd) {
  const cwd = typeof intentCwd === "string" && intentCwd.length ? intentCwd : WORKSPACE_REAL;
  try { return fs.realpathSync(cwd); } catch { return path.resolve(cwd); }
}

function resolveIntentPath(p, intentCwd) {
  const cwdReal = normalizeCwdForIntent(intentCwd);
  const raw = String(p);
  const abs = path.isAbsolute(raw) ? path.resolve(raw) : path.resolve(cwdReal, raw);

  // If target exists, realpath it (symlinks resolved).
  try {
    const full = fs.realpathSync(abs);
    return { abs, full, exists: true };
  } catch {
    // If it doesn't exist, resolve the nearest existing parent directory.
    const parent = path.dirname(abs);
    try {
      const parentReal = fs.realpathSync(parent);
      const full = path.join(parentReal, path.basename(abs));
      return { abs, full, exists: false };
    } catch {
      // Can't resolve parent => treat as outside.
      return { abs, full: abs, exists: false, unresolved: true };
    }
  }
}

function isInsideWorkspace(resolvedFullPath) {
  const rel = path.relative(WORKSPACE_REAL, resolvedFullPath);
  return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
}

function expandTilde(p) {
  const s = String(p || "");
  if (!s.startsWith("~/")) return s;
  const home = process.env.HOME || "";
  return home ? path.join(home, s.slice(2)) : s;
}

function isDeniedPath(p) {
  const s0 = expandTilde(p);
  if (!s0) return false;
  const s = path.resolve(s0);
  return DENY_PATHS.some((dp0) => {
    const dp = path.resolve(expandTilde(dp0));
    return s === dp || s.startsWith(dp + path.sep);
  });
}

function isDomainAllowlisted(dest) {
  // Tight allowlist semantics:
  // - If allowlist is empty: allow all (legacy behavior).
  // - Exact host match is allowed.
  // - Subdomains are ONLY allowed when the allowlist entry is explicitly wildcarded as "*.example.com".
  if (ALLOWLISTED_DOMAINS.length === 0) return true;
  try {
    const u = new URL(dest);
    const host = u.hostname.toLowerCase();
    return ALLOWLISTED_DOMAINS.some((entry0) => {
      const entry = String(entry0 || "").trim().toLowerCase();
      if (!entry) return false;

      if (entry.startsWith("*.")) {
        const base = entry.slice(2);
        if (!base) return false;
        // Allow both the base domain and any subdomain.
        return host === base || host.endsWith("." + base);
      }

      // Exact only.
      return host === entry;
    });
  } catch {
    return false;
  }
}

function classifyRisk({ intent, cmd, args }) {
  // Risk classes are MVP: low | high
  // High risk when:
  // - explicit network destinations present
  // - any file write/delete is requested (especially outside workspace)
  // - command includes known network egress tokens
  // - env_keys includes suspicious keys (basic heuristic)

  const joined = [cmd, ...(args || [])].join(" ");

  // Network destinations
  const dests = intent?.network?.destinations;
  if (Array.isArray(dests) && dests.length > 0) {
    const anyNotAllowlisted = dests.some((d) => !isDomainAllowlisted(String(d)));
    return anyNotAllowlisted
      ? { risk: "high", reason: "network destinations not allowlisted" }
      : { risk: "high", reason: "network destinations present (allowlisted)" };
  }

  // File mutations
  const writes = intent?.files?.write;
  const dels = intent?.files?.delete;
  const mut = ([]).concat(Array.isArray(writes) ? writes : [], Array.isArray(dels) ? dels : []);
  if (mut.length > 0) {
    for (const p of mut) {
      const r = resolveIntentPath(p, intent.cwd);
      if (isDeniedPath(r.abs) || isDeniedPath(r.full)) return { risk: "high", reason: "file mutation in denied path" };
      if (r.unresolved || !isInsideWorkspace(r.full)) return { risk: "high", reason: "file mutation outside workspace" };
    }
    return { risk: "high", reason: "file mutation requested" };
  }

  // Egress primitives in command
  if (matchToken(["curl", "wget"], joined)) return { risk: "high", reason: "network egress primitive" };

  // Secret-adjacent env access (very light heuristic)
  const envKeys = intent?.env_keys;
  if (Array.isArray(envKeys) && envKeys.some((k) => /key|token|secret|pass/i.test(String(k)))) {
    return { risk: "high", reason: "secret-like env_keys requested" };
  }

  return { risk: "low", reason: "no high-risk signals" };
}

function decideExec({ sessionId, cmd, args, intent }) {
  const err = validateIntent(intent);
  if (err) return { decision: "deny", reason: err };

  const joined = [cmd, ...(args || [])].join(" ");

  // ---- File mutation posture (fail-closed)
  // If intent indicates filesystem mutation outside the workspace boundary or in a denied path,
  // deny outright. This prevents symlink/path traversal confusion from being treated as "just high risk".
  const writes = intent?.files?.write;
  const dels = intent?.files?.delete;
  const mut = ([]).concat(Array.isArray(writes) ? writes : [], Array.isArray(dels) ? dels : []);
  if (mut.length > 0) {
    for (const p of mut) {
      const r = resolveIntentPath(p, intent.cwd);
      if (isDeniedPath(r.abs) || isDeniedPath(r.full)) {
        if (FILE_MUTATION_DENIED_PATH_ACTION === "approve") {
          return { decision: "approve", reason: "File mutation touches denied path", approvalId: `appr_${randomUUID()}` };
        }
        return { decision: "deny", reason: "File mutation touches denied path" };
      }
      if (r.unresolved || !isInsideWorkspace(r.full)) {
        if (FILE_MUTATION_OUTSIDE_WORKSPACE_ACTION === "approve") {
          return { decision: "approve", reason: "File mutation outside workspace", approvalId: `appr_${randomUUID()}` };
        }
        return { decision: "deny", reason: "File mutation outside workspace" };
      }
    }
  }

  // ---- Token posture
  const deny = matchToken(DENY_TOKENS, joined);
  if (deny) return { decision: "deny", reason: `Denied token: ${deny}` };

  // ---- Network posture
  // If destinations present and not allowlisted, require approval.
  const dests = intent?.network?.destinations;
  if (Array.isArray(dests) && dests.length > 0) {
    const anyNotAllowlisted = dests.some((d) => !isDomainAllowlisted(String(d)));
    if (anyNotAllowlisted) {
      return { decision: "approve", reason: "Network destination not allowlisted", approvalId: `appr_${randomUUID()}` };
    }
  }

  const approve = matchToken(APPROVE_TOKENS, joined);
  if (approve) {
    return {
      decision: "approve",
      reason: `Approval required for token: ${approve}`,
      approvalId: `appr_${randomUUID()}`,
    };
  }

  return { decision: "allow", reason: "Allowed by baseline policy" };
}

// ---------------------------------------------------------------------------
// Tool (generic) decisions — used by the Gateway bridge plugin.
// ---------------------------------------------------------------------------

function extractPathsFromToolParams(params) {
  // Heuristic: common path keys used by OpenClaw tools.
  const keys = [
    "path",
    "file_path",
    "filePath",
    "oldPath",
    "newPath",
    "directory",
    "cwd",
    "outPath",
    "jsonlPath",
  ];

  const out = [];
  if (!params || typeof params !== "object") return out;

  for (const k of keys) {
    const v = params[k];
    if (typeof v === "string" && v.trim()) out.push(v);
    if (Array.isArray(v)) {
      for (const item of v) if (typeof item === "string" && item.trim()) out.push(item);
    }
  }

  return out;
}

function extractUrlFromToolParams(params) {
  if (!params || typeof params !== "object") return "";
  const v = params.url || params.targetUrl || params.target_url;
  return typeof v === "string" ? v : "";
}

function classifyToolRisk({ toolName, params, workspaceDir }) {
  // MVP risk classes: low | high
  // This is intentionally conservative: we mark outbound/network/mutation as high.

  const tn = String(toolName || "").toLowerCase();
  const url = extractUrlFromToolParams(params);

  // Network tools
  if (url && /^(https?:)?\/\//i.test(url)) {
    const allowlisted = isDomainAllowlisted(url);
    return allowlisted
      ? { risk: "high", reason: "network destination present (allowlisted)" }
      : { risk: "high", reason: "network destination not allowlisted" };
  }
  if (tn.includes("web_fetch") || tn.includes("browser") || tn.includes("fetch")) {
    return { risk: "high", reason: "network/browsing tool" };
  }

  // Explicit outbound messaging
  if (tn.startsWith("message") || tn.includes("message")) {
    return { risk: "high", reason: "outbound messaging tool" };
  }

  // Shell / remote execution
  if (tn === "exec" || tn.includes("exec") || tn.includes("run")) {
    return { risk: "high", reason: "execution tool" };
  }

  // File mutations (heuristic by tool name)
  if (/(^|\b)(write|edit|patch|apply|delete|rm|mkdir|upload)(\b|$)/i.test(tn)) {
    return { risk: "high", reason: "file mutation tool" };
  }

  // Reads are usually low risk, but reading denied paths is sensitive.
  if (tn === "read" || tn.includes("read")) {
    const paths = extractPathsFromToolParams(params);
    const anyDenied = paths.some((p) => isDeniedPath(p));
    if (anyDenied) return { risk: "high", reason: "read touches denied path" };
    return { risk: "low", reason: "read-only tool" };
  }

  return { risk: "low", reason: "default low risk" };
}

function decideTool({ sessionId, toolName, params, workspaceDir }) {
  const tn = String(toolName || "");
  const joined = tn + " " + (() => {
    try {
      return JSON.stringify(params || {});
    } catch {
      return "{unserializable:true}";
    }
  })();

  // Token posture (applies across all tools)
  const deny = matchToken(DENY_TOKENS, joined);
  if (deny) return { decision: "deny", reason: `Denied token: ${deny}` };

  const approve = matchToken(APPROVE_TOKENS, joined);
  if (approve) return { decision: "approve", reason: `Approval required for token: ${approve}`, approvalId: `appr_${randomUUID()}` };

  // Tool-specific posture
  const lower = tn.toLowerCase();

  // Outbound messaging: default approval gate.
  if (lower.startsWith("message") || lower.includes("message")) {
    return { decision: "approve", reason: "Outbound messaging requires approval", approvalId: `appr_${randomUUID()}` };
  }

  // Network/browsing: allow allowlisted destinations, otherwise require approval.
  const url = extractUrlFromToolParams(params);
  if (url) {
    if (!isDomainAllowlisted(url)) {
      return { decision: "approve", reason: "Network destination not allowlisted", approvalId: `appr_${randomUUID()}` };
    }
    return { decision: "allow", reason: "Allowlisted network destination" };
  }

  // File mutation: deny/approve based on workspace boundary + denied paths.
  if (/(^|\b)(write|edit|delete|upload)(\b|$)/i.test(lower)) {
    const paths = extractPathsFromToolParams(params);
    for (const p of paths) {
      const r = resolveIntentPath(p, workspaceDir);
      if (isDeniedPath(r.abs) || isDeniedPath(r.full)) {
        if (FILE_MUTATION_DENIED_PATH_ACTION === "approve") {
          return { decision: "approve", reason: "File mutation touches denied path", approvalId: `appr_${randomUUID()}` };
        }
        return { decision: "deny", reason: "File mutation touches denied path" };
      }
      if (r.unresolved || !isInsideWorkspace(r.full)) {
        if (FILE_MUTATION_OUTSIDE_WORKSPACE_ACTION === "approve") {
          return { decision: "approve", reason: "File mutation outside workspace", approvalId: `appr_${randomUUID()}` };
        }
        return { decision: "deny", reason: "File mutation outside workspace" };
      }
    }
  }

  // Reads: allow by default, but reading denied paths requires approval.
  if (lower === "read" || lower.includes("read")) {
    const paths = extractPathsFromToolParams(params);
    const anyDenied = paths.some((p) => isDeniedPath(p));
    if (anyDenied) return { decision: "approve", reason: "Read touches denied path", approvalId: `appr_${randomUUID()}` };
    return { decision: "allow", reason: "Allowed read" };
  }

  // Default allow (keeps UX smooth). High-risk tools should be handled by the cases above.
  return { decision: "allow", reason: "Allowed by baseline tool policy" };
}

function postVaibotProve({ receipt, idempotencyKey }) {
  if (VAIBOT_PROVE_MODE === "off") return Promise.resolve(null);
  if (!VAIBOT_API_URL || !VAIBOT_API_KEY) return Promise.resolve(null);

  const url = new URL(VAIBOT_API_URL.replace(/\/$/, "") + "/prove");
  const body = JSON.stringify({
    content: JSON.stringify({ ...receipt, intent: redactIntent(receipt.intent) }),
    contentType: "application/json",
    encoding: "utf-8",
    model: VAIBOT_PROVE_MODEL,
    metadata: {
      schema: receipt.schema,
      kind: receipt.kind,
      runId: receipt.runId,
      sessionId: receipt.sessionId,
    },
    idempotencyKey,
  });

  const options = {
    method: "POST",
    hostname: url.hostname,
    port: url.port || 443,
    path: url.pathname,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "content-length": Buffer.byteLength(body),
      "authorization": `Bearer ${VAIBOT_API_KEY}`,
    },
    timeout: 8000,
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try {
          const parsed = JSON.parse(data || "{}");
          if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) return resolve(parsed);
          reject(new Error(`vaibot /prove failed (${res.statusCode}): ${data.slice(0, 200)}`));
        } catch (e) {
          reject(new Error(`vaibot /prove invalid JSON: ${data.slice(0, 200)}`));
        }
      });
    });
    req.on("timeout", () => req.destroy(new Error("vaibot /prove timeout")));
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

/**
 * postGovernanceReceipt — Post a canonical governance receipt to VAIBot API v2.
 * Called best-effort on every finalize (tool or exec).
 * VAIBOT_API_URL format: https://www.vaibot.io/api  → appends /v2/receipts
 */
function postGovernanceReceipt({ runId, sessionId, intent, decision, risk, result, policyVersion }) {
  if (!VAIBOT_API_URL || !VAIBOT_API_KEY) return Promise.resolve(null);

  const toolName = String(intent?.toolName || intent?.tool || intent?.cmd?.split(" ")[0] || "unknown");
  const command = String(intent?.cmd || intent?.command || toolName).slice(0, 500);
  const cwd = String(intent?.workspaceDir || intent?.cwd || "/");

  const guardDecision = String(decision?.decision || "deny");
  // Map guard decision names to governance receipt decision names
  const mappedDecision = guardDecision === "approve" ? "approval_required" : guardDecision;

  const riskRaw = String(risk?.risk || "low");
  const riskLevel = ["low", "medium", "high", "critical"].includes(riskRaw) ? riskRaw : "low";

  const approvalStatus = guardDecision === "approve" ? "pending" : "not_required";

  let outcome = "blocked";
  if (guardDecision === "allow") {
    outcome = (result?.ok === false || result?.code !== 0) ? "blocked" : "allowed";
  } else if (guardDecision === "approve") {
    outcome = "blocked_until_approved";
  } else {
    outcome = "blocked";
  }

  const agentId = String(sessionId || "unknown-session");
  const actionVerb = mappedDecision === "deny" ? "blocked from executing" :
    mappedDecision === "approval_required" ? "paused pending approval for" :
    "executed";

  const receiptPayload = {
    run_id: runId,
    idempotency_key: `${runId}:finalize`,
    agent: { id: agentId, name: agentId },
    action: {
      tool: toolName,
      summary: `Agent ${actionVerb}: ${command.slice(0, 100)}`,
      command,
      cwd,
    },
    policy: {
      risk_level: riskLevel,
      decision: mappedDecision,
      reason: String(decision?.reason || risk?.reason || "Policy decision"),
    },
    approval: { status: approvalStatus },
    result: {
      outcome,
      summary: String(decision?.reason || outcome),
    },
  };

  // VAIBOT_API_URL is e.g. https://www.vaibot.io/api — strip trailing /api and append /api/v2/receipts
  const baseUrl = VAIBOT_API_URL.replace(/\/api\/?$/, "");
  const targetUrl = new URL(baseUrl + "/api/v2/receipts");
  const body = JSON.stringify(receiptPayload);

  const options = {
    method: "POST",
    hostname: targetUrl.hostname,
    port: targetUrl.port || (targetUrl.protocol === "https:" ? 443 : 80),
    path: targetUrl.pathname,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "content-length": Buffer.byteLength(body),
      "authorization": `Bearer ${VAIBOT_API_KEY}`,
    },
    timeout: 8000,
  };

  const transport = targetUrl.protocol === "https:" ? https : http;

  return new Promise((resolve) => {
    const req = transport.request(options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => {
        try { resolve(JSON.parse(data || "{}")); }
        catch { resolve({ ok: false, raw: data.slice(0, 200) }); }
      });
    });
    req.on("timeout", () => { req.destroy(); resolve({ ok: false, error: "timeout" }); });
    req.on("error", (e) => resolve({ ok: false, error: e?.message }));
    req.write(body);
    req.end();
  });
}

const MERKLE_CHECKPOINT_EVERY = Math.max(1, Number(process.env.VAIBOT_MERKLE_CHECKPOINT_EVERY || 50));
const MERKLE_CHECKPOINT_EVERY_MS = Math.max(10_000, Number(process.env.VAIBOT_MERKLE_CHECKPOINT_EVERY_MS || 10 * 60 * 1000));

// Track which sessions have produced events so periodic checkpointing can run.
const SEEN_SESSIONS = new Set();

function leafHash(eventHash) {
  return sha256("leaf:" + eventHash);
}

function parentHash(left, right) {
  return sha256("node:" + left + ":" + right);
}

function loadMerkleState(sessionId) {
  const p = path.join(LOG_DIR, `${sessionId}.merkle.json`);
  if (!fs.existsSync(p)) {
    return {
      count: 0,
      frontier: [],
      lastCheckpointSeq: 0,
      lastCheckpointHash: "",
      lastCheckpointAtMs: 0,
      lastCheckpointEventCount: 0,
      lastAnchoredSeq: 0,
    };
  }
  try {
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    return {
      count: Number(j.count || 0),
      frontier: Array.isArray(j.frontier) ? j.frontier.map((v) => (v === null ? null : String(v))) : [],
      lastCheckpointSeq: Number(j.lastCheckpointSeq || 0),
      lastCheckpointHash: String(j.lastCheckpointHash || ""),
      lastCheckpointAtMs: Number(j.lastCheckpointAtMs || 0),
      lastCheckpointEventCount: Number(j.lastCheckpointEventCount || 0),
      lastAnchoredSeq: Number(j.lastAnchoredSeq || 0),
    };
  } catch {
    return {
      count: 0,
      frontier: [],
      lastCheckpointSeq: 0,
      lastCheckpointHash: "",
      lastCheckpointAtMs: 0,
      lastCheckpointEventCount: 0,
      lastAnchoredSeq: 0,
    };
  }
}

function saveMerkleState(sessionId, st) {
  const p = path.join(LOG_DIR, `${sessionId}.merkle.json`);
  fs.writeFileSync(p, JSON.stringify(st, null, 2) + "\n");
}

function computeRoot(frontier) {
  // Fold highest->lowest to produce a single root.
  let acc = null;
  for (let level = frontier.length - 1; level >= 0; level--) {
    const h = frontier[level];
    if (!h) continue;
    acc = acc ? parentHash(h, acc) : h;
  }
  return acc || sha256("empty");
}

function appendLeaf(sessionId, leaf) {
  const p = path.join(LOG_DIR, `${sessionId}.leaves.jsonl`);
  fs.appendFileSync(p, stableStringify({ leaf }) + "\n");
}

function merkleAppend(sessionId, eventHash) {
  const st = loadMerkleState(sessionId);
  const leaf = leafHash(eventHash);
  appendLeaf(sessionId, leaf);

  let node = leaf;
  let level = 0;
  while (true) {
    if (!st.frontier[level]) {
      st.frontier[level] = node;
      break;
    }
    node = parentHash(st.frontier[level], node);
    st.frontier[level] = null;
    level++;
  }
  st.count += 1;
  // Trim trailing nulls
  while (st.frontier.length && st.frontier[st.frontier.length - 1] === null) {
    st.frontier.pop();
  }
  saveMerkleState(sessionId, st);
  return { count: st.count, root: computeRoot(st.frontier) };
}

function loadCheckpoints(sessionId) {
  const cpPath = path.join(LOG_DIR, `${sessionId}.checkpoints.jsonl`);
  if (!fs.existsSync(cpPath)) return [];
  return fs.readFileSync(cpPath, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
}

function loadLeaves(sessionId, count) {
  const p = path.join(LOG_DIR, `${sessionId}.leaves.jsonl`);
  if (!fs.existsSync(p)) return [];
  const lines = fs.readFileSync(p, "utf8").split("\n").filter(Boolean);
  const sliced = typeof count === "number" ? lines.slice(0, count) : lines;
  return sliced.map((l) => JSON.parse(l).leaf);
}

function nextLevel(nodes) {
  const out = [];
  for (let i = 0; i < nodes.length; i += 2) {
    const left = nodes[i];
    const right = nodes[i + 1] || nodes[i]; // duplicate last if odd
    out.push(parentHash(left, right));
  }
  return out;
}

function buildInclusionProof(leaves, index) {
  if (index < 0 || index >= leaves.length) throw new Error("index out of range");
  let idx = index;
  let level = leaves.slice();
  const siblings = [];

  while (level.length > 1) {
    const isRight = idx % 2 === 1;
    const sibIdx = isRight ? idx - 1 : idx + 1;
    const sib = level[sibIdx] ?? level[idx];
    siblings.push(sib);
    idx = Math.floor(idx / 2);
    level = nextLevel(level);
  }

  return { leaf: leaves[index], siblings, root: level[0] };
}

async function tryFlushCheckpoints(sessionId) {
  if (VAIBOT_PROVE_MODE === "off") return;
  const proveConfigured = !!(VAIBOT_API_URL && VAIBOT_API_KEY);
  if (!proveConfigured) {
    if (VAIBOT_PROVE_MODE === "required") {
      throw new Error("VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured");
    }
    return;
  }

  const st = loadMerkleState(sessionId);
  const cps = loadCheckpoints(sessionId);
  for (const cp of cps) {
    if (cp.seq <= st.lastAnchoredSeq) continue;

    const receipt = {
      schema: "vaibot-guard/checkpoint@0.1",
      kind: "merkle.checkpoint",
      ts: cp.ts,
      sessionId,
      seq: cp.seq,
      count: cp.count,
      root: cp.root,
      range: cp.range,
      prevCheckpointHash: cp.prevCheckpointHash,
    };

    // Prove checkpoint root (idempotent)
    await postVaibotProve({ receipt, idempotencyKey: `${sessionId}:checkpoint:${cp.seq}` });

    st.lastAnchoredSeq = cp.seq;
    saveMerkleState(sessionId, st);
  }
}

function appendCheckpoint(sessionId, checkpoint) {
  const p = path.join(LOG_DIR, `${sessionId}.checkpoints.jsonl`);
  fs.appendFileSync(p, stableStringify(checkpoint) + "\n");
}

function createCheckpointIfNeeded(sessionId, reason) {
  const st = loadMerkleState(sessionId);
  if (st.count <= st.lastCheckpointEventCount) return null;

  const root = computeRoot(st.frontier);
  const seq = st.lastCheckpointSeq + 1;
  const checkpoint = {
    schema: "vaibot-guard/checkpoint@0.1",
    ts: nowIso(),
    sessionId,
    seq,
    count: st.count,
    root,
    range: { uptoEventCount: st.count },
    reason,
    prevCheckpointHash: st.lastCheckpointHash || "",
    policyVersion: POLICY.version,
    guardVersion: "0.1",
    hashAlg: "sha256",
    merkle: {
      leaf: "sha256(\"leaf:\"+eventHash)",
      node: "sha256(\"node:\"+left+\":\"+right)",
    },
  };

  // domain-separated checkpoint hash (exclude existing hash field in the digest)
  const { hash: _ignore, ...cpNoHash } = checkpoint;
  checkpoint.hash = hashCheckpoint("checkpoint:" + stableStringify(cpNoHash));

  appendCheckpoint(sessionId, checkpoint);

  st.lastCheckpointSeq = seq;
  st.lastCheckpointHash = checkpoint.hash;
  st.lastCheckpointAtMs = Date.now();
  st.lastCheckpointEventCount = st.count;
  saveMerkleState(sessionId, st);

  return checkpoint;
}

function redactString(s) {
  let out = String(s);
  for (const pat of POLICY.redactPatterns) {
    try {
      out = out.replace(new RegExp(pat, "g"), "[REDACTED]");
    } catch {
      // ignore bad patterns
    }
  }
  return out;
}

function redactIntent(intent) {
  if (!intent || typeof intent !== "object") return intent;
  const clone = JSON.parse(JSON.stringify(intent));

  // Redact env_keys if they look secret-like
  if (Array.isArray(clone.env_keys)) {
    clone.env_keys = clone.env_keys.map((k) => {
      const ks = String(k);
      const shouldRedact = POLICY.redactEnvKeyPatterns.some((p) => {
        try { return new RegExp(p).test(ks); } catch { return false; }
      });
      return shouldRedact ? "[REDACTED_ENV_KEY]" : ks;
    });
  }

  // Redact command/args strings by pattern
  if (typeof clone.command === "string") clone.command = redactString(clone.command);
  if (Array.isArray(clone.args)) clone.args = clone.args.map((a) => redactString(a));

  // Redact network destinations (URLs can carry tokens)
  if (clone.network && Array.isArray(clone.network.destinations)) {
    clone.network.destinations = clone.network.destinations.map((d) => redactString(d));
  }

  return clone;
}

function appendAudit(event) {
  const sessionId = event.sessionId || "unknown-session";
  const logPath = path.join(LOG_DIR, `${sessionId}.jsonl`);
  const prevHashPath = path.join(LOG_DIR, `${sessionId}.prevhash`);
  const prevHash = fs.existsSync(prevHashPath) ? fs.readFileSync(prevHashPath, "utf8").trim() : "";

  // Redact sensitive strings before persistence/proving.
  const safeEvent = { ...event };
  if (safeEvent.intent) safeEvent.intent = redactIntent(safeEvent.intent);
  const fullEvent = { ...safeEvent, prevHash };
  const line = stableStringify(fullEvent);
  const h = sha256(line);

  fs.appendFileSync(logPath, line + "\n");
  fs.writeFileSync(prevHashPath, h + "\n");

  SEEN_SESSIONS.add(sessionId);

  // Merkle accumulator update + periodic checkpoints
  const merkle = merkleAppend(sessionId, h);

  // Checkpointing: whichever comes first (count delta or time interval)
  try {
    const st = loadMerkleState(sessionId);
    const delta = st.count - (st.lastCheckpointEventCount || 0);
    const dueByCount = delta >= MERKLE_CHECKPOINT_EVERY;
    const dueByTime = !st.lastCheckpointAtMs || (Date.now() - st.lastCheckpointAtMs) >= MERKLE_CHECKPOINT_EVERY_MS;

    if (dueByCount) {
      createCheckpointIfNeeded(sessionId, "count");
      tryFlushCheckpoints(sessionId).catch(() => {});
    } else if (dueByTime && st.count > (st.lastCheckpointEventCount || 0)) {
      // Only checkpoint by time if new events arrived
      createCheckpointIfNeeded(sessionId, "time");
      tryFlushCheckpoints(sessionId).catch(() => {});
    }
  } catch {
    // ignore checkpoint scheduling errors
  }

  return { hash: h, prevHash, merkle };
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === "GET" && req.url === "/health") {
      return json(res, 200, { ok: true, service: "vaibot-guard", ts: nowIso() });
    }

    // policy hot-reload disabled (restart service to apply policy changes)

    if (req.method === "POST" && req.url === "/api/proof") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "unknown-session");
      const index = Number(input.index);
      const checkpointSeq = Number(input.checkpointSeq);
      if (!Number.isFinite(index) || index < 0) return json(res, 400, { ok: false, error: "Missing/invalid index" });
      if (!Number.isFinite(checkpointSeq) || checkpointSeq < 1) return json(res, 400, { ok: false, error: "Missing/invalid checkpointSeq" });

      const cps = loadCheckpoints(sessionId);
      const cp = cps.find((c) => c.seq === checkpointSeq);
      if (!cp) return json(res, 404, { ok: false, error: "Checkpoint not found" });

      const leaves = loadLeaves(sessionId, cp.count);
      const proof = buildInclusionProof(leaves, index);

      // Sanity: computed root should match checkpoint root
      const rootMatches = proof.root === cp.root;

      return json(res, 200, {
        ok: true,
        sessionId,
        index,
        count: cp.count,
        leaf: proof.leaf,
        siblings: proof.siblings,
        root: proof.root,
        rootMatches,
        checkpoint: { seq: cp.seq, root: cp.root, count: cp.count },
      });
    }

    if (req.method === "POST" && req.url === "/v1/flush") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }
      const sessionId = String(input.sessionId || "unknown-session");
      try {
        await tryFlushCheckpoints(sessionId);
        const st = loadMerkleState(sessionId);
        return json(res, 200, { ok: true, sessionId, lastAnchoredSeq: st.lastAnchoredSeq, lastCheckpointSeq: st.lastCheckpointSeq });
      } catch (e) {
        return json(res, 500, { ok: false, error: e?.message || String(e) });
      }
    }

    // ---------------------------------------------------------------------
    // Approvals (chat-command UX)
    // ---------------------------------------------------------------------

    if (req.method === "POST" && req.url === "/v1/approvals/list") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "");
      const approvals = listApprovals({ status: "pending", sessionId: sessionId || undefined }).map((a) => ({
        approvalId: a.approvalId,
        status: a.status,
        createdAt: a.createdAt,
        expiresAt: a.expiresAt,
        reason: a.reason,
        kind: a.kind,
        request: a.request,
      }));

      return json(res, 200, { ok: true, approvals });
    }

    if (req.method === "POST" && req.url === "/v1/approvals/resolve") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const approvalId = String(input.approvalId || "");
      const action = String(input.action || "");
      if (!approvalId) return json(res, 400, { ok: false, error: "Missing approvalId" });
      if (action !== "approve" && action !== "deny") return json(res, 400, { ok: false, error: "Invalid action" });

      const out = resolveApproval({ approvalId, action });
      if (!out.ok) return json(res, 400, out);
      return json(res, 200, out);
    }

    if (req.method === "POST" && req.url === "/v1/decide/exec") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "unknown-session");
      const cmd = String(input.cmd || "");
      const args = Array.isArray(input.args) ? input.args.map(String) : [];
      const intent = input.intent;

      if (!cmd) return json(res, 400, { ok: false, error: "Missing cmd" });

      const risk = classifyRisk({ intent, cmd, args });
      const decision = decideExec({ sessionId, cmd, args, intent });
      const runId = `run_${randomUUID()}`;

      const eventId = randomUUID();
      const audit = appendAudit({
        ts: nowIso(),
        eventId,
        kind: "exec.precheck",
        sessionId,
        runId,
        cmd,
        args,
        risk,
        decision,
        intent,
      });

      // Prove the *precheck receipt* (best-effort unless VAIBOT_PROVE_MODE=required).
      let prove = null;
      let proveError = null;
      try {
        const receipt = {
          schema: "vaibot-guard/receipt@0.1",
          kind: "exec",
          ts: nowIso(),
          runId,
          sessionId,
          policyVersion: POLICY.version,
          risk,
          intent,
          decision,
          result: null,
          audit,
        };
        prove = await postVaibotProve({ receipt, idempotencyKey: runId + ":precheck" });
      } catch (e) {
        proveError = e?.message || String(e);
        prove = { ok: false, error: proveError };
      }

      // Fail-closed: if required mode is enabled, deny execution if we cannot prove the precheck receipt.
      if (VAIBOT_PROVE_MODE === "required") {
        if (!VAIBOT_API_URL || !VAIBOT_API_KEY) {
          return json(res, 200, {
            ok: true,
            runId,
            risk,
            decision: { decision: "deny", reason: "VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured" },
            audit,
            prove,
          });
        }
        if (proveError || (prove && prove.ok === false)) {
          return json(res, 200, {
            ok: true,
            runId,
            risk,
            decision: { decision: "deny", reason: `VAIBOT_PROVE_MODE=required but /api/prove failed: ${proveError || prove?.error || "unknown"}` },
            audit,
            prove,
          });
        }
      }

      // Store context for finalize (persisted).
      writeRunContext(runId, { sessionId, risk, intent, decision, precheckAudit: audit, ts: nowIso(), policyVersion: POLICY.version });

      return json(res, 200, { ok: true, runId, risk, decision, audit, prove });
    }

    if (req.method === "POST" && req.url === "/v1/decide/tool") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "unknown-session");
      const toolName = String(input.toolName || "");
      const params = input.params && typeof input.params === "object" ? input.params : {};
      const workspaceDir = String(input.workspaceDir || input.cwd || "");

      if (!toolName) return json(res, 400, { ok: false, error: "Missing toolName" });

      const risk = classifyToolRisk({ toolName, params, workspaceDir });

      const paramsHash = `sha256:${sha256(stableStringify({ toolName, params }))}`;
      const approvalId = String(input?.approval?.approvalId || "");

      let decision;

      // Approval redemption path: if caller presents an approvalId, verify it matches this exact request.
      if (approvalId) {
        const appr = readApproval(approvalId);
        if (!appr) {
          decision = { decision: "deny", reason: "Approval not found" };
        } else if (appr.kind !== "tool") {
          decision = { decision: "deny", reason: "Approval kind mismatch" };
        } else if (appr.status !== "approved") {
          decision = { decision: "deny", reason: `Approval not approved (status=${appr.status})` };
        } else if (appr.expiresAt && Date.now() > Date.parse(appr.expiresAt)) {
          decision = { decision: "deny", reason: "Approval expired" };
        } else if (appr.request?.paramsHash && appr.request.paramsHash !== paramsHash) {
          decision = { decision: "deny", reason: "Approval scope mismatch" };
        } else {
          decision = { decision: "allow", reason: "Approved by user", approvalId };
          markApprovalUsed({ approvalId });
        }
      } else {
        decision = decideTool({ sessionId, toolName, params, workspaceDir });

        // If policy requires approval, mint an approval record for chat-command resolution.
        if (decision && decision.decision === "approve") {
          const existingId = decision.approvalId;
          const already = existingId ? readApproval(existingId) : null;
          const appr = already
            ? already
            : createApproval({
                sessionId,
                kind: "tool",
                approvalId: existingId,
                reason: decision.reason || "Approval required",
                request: {
                  toolName,
                  paramsHash,
                  paramsPreview: redactIntent(params),
                },
              });

          decision.approvalId = appr.approvalId;
          decision.expiresAt = appr.expiresAt;
          decision.scope = { paramsHash };
        }
      }

      const runId = `run_${randomUUID()}`;

      const eventId = randomUUID();
      const audit = appendAudit({
        ts: nowIso(),
        eventId,
        kind: "tool.precheck",
        sessionId,
        runId,
        toolName,
        params: redactIntent(params),
        risk,
        decision,
      });

      // Prove the *precheck receipt* (best-effort unless VAIBOT_PROVE_MODE=required).
      let prove = null;
      let proveError = null;
      try {
        const receipt = {
          schema: "vaibot-guard/receipt@0.1",
          kind: "tool",
          ts: nowIso(),
          runId,
          sessionId,
          policyVersion: POLICY.version,
          risk,
          intent: { toolName, params: redactIntent(params), workspaceDir },
          decision,
          result: null,
          audit,
        };
        prove = await postVaibotProve({ receipt, idempotencyKey: runId + ":precheck" });
      } catch (e) {
        proveError = e?.message || String(e);
        prove = { ok: false, error: proveError };
      }

      if (VAIBOT_PROVE_MODE === "required") {
        if (!VAIBOT_API_URL || !VAIBOT_API_KEY) {
          return json(res, 200, {
            ok: true,
            runId,
            risk,
            decision: { decision: "deny", reason: "VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured" },
            audit,
            prove,
          });
        }
        if (proveError || (prove && prove.ok === false)) {
          return json(res, 200, {
            ok: true,
            runId,
            risk,
            decision: { decision: "deny", reason: `VAIBOT_PROVE_MODE=required but /api/prove failed: ${proveError || prove?.error || "unknown"}` },
            audit,
            prove,
          });
        }
      }

      writeRunContext(runId, {
        sessionId,
        risk,
        intent: { toolName, params: redactIntent(params), workspaceDir },
        decision,
        precheckAudit: audit,
        ts: nowIso(),
        policyVersion: POLICY.version,
      });

      return json(res, 200, { ok: true, runId, risk, decision, audit, prove });
    }

    if (req.method === "POST" && req.url === "/v1/finalize/tool") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "unknown-session");
      const runId = String(input.runId || "");
      const result = input.result;

      if (!runId) return json(res, 400, { ok: false, error: "Missing runId" });

      const ctx1 = readRunContext(runId);
      const effectiveSessionId = String(ctx1?.sessionId || sessionId || "unknown-session");

      const eventId = randomUUID();
      const audit = appendAudit({
        ts: nowIso(),
        eventId,
        kind: "tool.finalize",
        sessionId: effectiveSessionId,
        runId,
        result: redactIntent(result),
      });

      let prove = null;
      let proveError = null;
      try {
        const ctx = readRunContext(runId);
        const receipt = {
          schema: "vaibot-guard/receipt@0.1",
          kind: "tool",
          ts: nowIso(),
          runId,
          sessionId: effectiveSessionId,
          policyVersion: POLICY.version,
          risk: ctx?.risk ?? null,
          intent: ctx?.intent ?? null,
          decision: ctx?.decision ?? null,
          result: redactIntent(result),
          audit,
          precheckAudit: ctx?.precheckAudit ?? null,
        };
        prove = await postVaibotProve({ receipt, idempotencyKey: runId + ":finalize" });
      } catch (e) {
        proveError = e?.message || String(e);
        prove = { ok: false, error: proveError };
      }

      if (VAIBOT_PROVE_MODE === "required") {
        if (!VAIBOT_API_URL || !VAIBOT_API_KEY) {
          return json(res, 500, { ok: false, error: "VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured", audit, prove });
        }
        if (proveError || (prove && prove.ok === false)) {
          return json(res, 500, { ok: false, error: `VAIBOT_PROVE_MODE=required but /api/prove finalize failed: ${proveError || prove?.error || "unknown"}`, audit, prove });
        }
      }

      // Best-effort: post governance receipt to VAIBot API v2 (does not block response)
      postGovernanceReceipt({
        runId,
        sessionId: effectiveSessionId,
        intent: ctx1?.intent,
        decision: ctx1?.decision,
        risk: ctx1?.risk,
        result,
        policyVersion: ctx1?.policyVersion,
      }).catch((e) => console.error(`[vaibot-guard] governance receipt post failed (tool): ${e?.message || e}`));

      deleteRunContext(runId);

      return json(res, 200, { ok: true, audit, prove });
    }

    if (req.method === "POST" && req.url === "/v1/finalize") {
      if (!requireAuth(req, res)) return;
      const raw = await readBody(req);
      let input;
      try {
        input = JSON.parse(raw || "{}");
      } catch {
        return json(res, 400, { ok: false, error: "Invalid JSON" });
      }

      const sessionId = String(input.sessionId || "unknown-session");
      const runId = String(input.runId || "");
      const result = input.result;

      // If caller didn't send sessionId, try to infer from run context.
      if ((sessionId === "unknown-session" || !sessionId) && runId) {
        const ctx0 = readRunContext(runId);
        if (ctx0?.sessionId) {
          // eslint-disable-next-line no-param-reassign
          input.sessionId = ctx0.sessionId;
        }
      }

      if (!runId) return json(res, 400, { ok: false, error: "Missing runId" });

      const ctx1 = readRunContext(runId);
      const effectiveSessionId = String(ctx1?.sessionId || sessionId || "unknown-session");

      const eventId = randomUUID();
      const audit = appendAudit({
        ts: nowIso(),
        eventId,
        kind: "exec.finalize",
        sessionId: effectiveSessionId,
        runId,
        result,
      });

      let prove = null;
      let proveError = null;
      try {
        const ctx = readRunContext(runId);
        const receipt = {
          schema: "vaibot-guard/receipt@0.1",
          kind: "exec",
          ts: nowIso(),
          runId,
          sessionId,
          policyVersion: POLICY.version,
          risk: ctx?.risk ?? null,
          intent: ctx?.intent ?? null,
          decision: ctx?.decision ?? null,
          result,
          audit,
          precheckAudit: ctx?.precheckAudit ?? null,
        };
        prove = await postVaibotProve({ receipt, idempotencyKey: runId + ":finalize" });
      } catch (e) {
        proveError = e?.message || String(e);
        prove = { ok: false, error: proveError };
      }

      if (VAIBOT_PROVE_MODE === "required") {
        if (!VAIBOT_API_URL || !VAIBOT_API_KEY) {
          return json(res, 500, { ok: false, error: "VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured", audit, prove });
        }
        if (proveError || (prove && prove.ok === false)) {
          return json(res, 500, { ok: false, error: `VAIBOT_PROVE_MODE=required but /api/prove finalize failed: ${proveError || prove?.error || "unknown"}`, audit, prove });
        }
      }

      // Best-effort: post governance receipt to VAIBot API v2 (does not block response)
      postGovernanceReceipt({
        runId,
        sessionId: effectiveSessionId,
        intent: ctx1?.intent,
        decision: ctx1?.decision,
        risk: ctx1?.risk,
        result,
        policyVersion: ctx1?.policyVersion,
      }).catch((e) => console.error(`[vaibot-guard] governance receipt post failed (exec): ${e?.message || e}`));

      // Best-effort cleanup of run context.
      deleteRunContext(runId);

      return json(res, 200, { ok: true, audit, prove });
    }

    json(res, 404, { ok: false, error: "Not found" });
  } catch (err) {
    json(res, 500, { ok: false, error: err?.message || String(err) });
  }
});

if (VAIBOT_PROVE_MODE === "required" && (!VAIBOT_API_URL || !VAIBOT_API_KEY)) {
  // eslint-disable-next-line no-console
  console.error("[vaibot-guard] refusing to start: VAIBOT_PROVE_MODE=required but VAIBOT_API_URL/VAIBOT_API_KEY not configured");
  process.exit(2);
}

server.on("error", (err) => {
  if (err && err.code === "EADDRINUSE") {
    // eslint-disable-next-line no-console
    console.error(`[vaibot-guard] failed to bind http://${HOST}:${PORT} (EADDRINUSE). Another process is using this port.`);
    // eslint-disable-next-line no-console
    console.error(`[vaibot-guard] Fix: stop the other process, or set VAIBOT_GUARD_PORT to a free port (e.g. VAIBOT_GUARD_PORT=39112).`);
    process.exit(1);
  }
  // eslint-disable-next-line no-console
  console.error(`[vaibot-guard] server error: ${err?.message || err}`);
  process.exit(1);
});

server.listen(PORT, HOST, () => {
  // eslint-disable-next-line no-console
  console.log(`[vaibot-guard] listening on http://${HOST}:${PORT}`);
});

// Time-based checkpointing (every 10 minutes by default): create a checkpoint if any new events
// have arrived since the last checkpoint and time has elapsed.
setInterval(() => {
  for (const sessionId of SEEN_SESSIONS) {
    try {
      const st = loadMerkleState(sessionId);
      const hasNew = st.count > (st.lastCheckpointEventCount || 0);
      if (!hasNew) continue;

      const dueByTime = !st.lastCheckpointAtMs || (Date.now() - st.lastCheckpointAtMs) >= MERKLE_CHECKPOINT_EVERY_MS;
      if (dueByTime) {
        createCheckpointIfNeeded(sessionId, "time");
        tryFlushCheckpoints(sessionId).catch(() => {});
      }
    } catch {
      // ignore periodic errors
    }
  }
}, Math.min(60_000, MERKLE_CHECKPOINT_EVERY_MS));

function cleanupOldLogs() {
  const cutoffMs = Date.now() - VAIBOT_LOG_RETENTION_DAYS * 24 * 60 * 60 * 1000;
  let removed = 0;

  function sweepDir(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const name = ent.name;
      const p = path.join(dir, name);

      if (ent.isDirectory()) {
        // only recurse into known subdirs we manage
        if (name === "runctx") sweepDir(p);
        continue;
      }
      if (!ent.isFile()) continue;

      // only touch our own files
      if (!name.endsWith(".jsonl") && !name.endsWith(".json") && !name.endsWith(".prevhash")) continue;

      const st = fs.statSync(p);
      if (st.mtimeMs < cutoffMs) {
        fs.rmSync(p);
        removed++;
      }
    }
  }

  try {
    sweepDir(LOG_DIR);
  } catch {
    // ignore cleanup errors
  }

  if (removed > 0) {
    // eslint-disable-next-line no-console
    console.log(`[vaibot-guard] log cleanup: removed ${removed} file(s) older than ${VAIBOT_LOG_RETENTION_DAYS}d`);
  }
}

// Run cleanup hourly (cheap) and at startup.
cleanupOldLogs();
setInterval(cleanupOldLogs, 60 * 60 * 1000);
