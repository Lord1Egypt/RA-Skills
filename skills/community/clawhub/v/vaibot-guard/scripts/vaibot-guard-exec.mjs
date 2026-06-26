#!/usr/bin/env node
/**
 * vaibot-guard-exec (MVP)
 *
 * Execution wrapper that:
 * - requires a run plan
 * - asks vaibot-guard-service for a decision
 * - logs locally (service logs the decision; wrapper logs execution outcome)
 * - executes only on allow
 */

import { spawn } from "node:child_process";
import http from "node:http";
import { randomUUID, createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const GUARD_HOST = process.env.VAIBOT_GUARD_HOST || "127.0.0.1";
const GUARD_PORT = Number(process.env.VAIBOT_GUARD_PORT || 39111);

const WORKSPACE = process.env.VAIBOT_WORKSPACE || process.cwd();
const LOG_DIR = process.env.VAIBOT_GUARD_LOG_DIR || path.join(WORKSPACE, ".vaibot-guard");
fs.mkdirSync(LOG_DIR, { recursive: true });

function sha256(s) {
  return createHash("sha256").update(s).digest("hex");
}

function nowIso() {
  return new Date().toISOString();
}

function appendLocalEvent(sessionId, event) {
  const logPath = path.join(LOG_DIR, `${sessionId}.exec.jsonl`);
  const prevHashPath = path.join(LOG_DIR, `${sessionId}.exec.prevhash`);
  const prevHash = fs.existsSync(prevHashPath) ? fs.readFileSync(prevHashPath, "utf8").trim() : "";
  const fullEvent = { ...event, prevHash };
  const line = JSON.stringify(fullEvent);
  const h = sha256(line);
  fs.appendFileSync(logPath, line + "\n");
  fs.writeFileSync(prevHashPath, h + "\n");
  return { hash: h, prevHash };
}

function requestDecision(payload) {
  const body = JSON.stringify(payload);
  const options = {
    hostname: GUARD_HOST,
    port: GUARD_PORT,
    path: "/v1/decide/exec",
    method: "POST",
    headers: {
      "content-type": "application/json; charset=utf-8",
      "content-length": Buffer.byteLength(body),
    },
    timeout: 5000,
  };

  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data || "{}"));
        } catch {
          reject(new Error(`invalid JSON from guard: ${data.slice(0, 200)}`));
        }
      });
    });
    req.on("timeout", () => req.destroy(new Error("guard request timeout")));
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// Run plan is required. Provide either:
// - env VAIBOT_RUN_PLAN (JSON)
// - argv[2] as JSON
const runPlanJson = process.env.VAIBOT_RUN_PLAN || process.argv[2];
if (!runPlanJson) {
  console.error("DENY: missing run plan (set VAIBOT_RUN_PLAN or pass as first arg)");
  process.exit(40);
}

let runPlan;
try {
  runPlan = JSON.parse(runPlanJson);
} catch {
  console.error("DENY: run plan is not valid JSON");
  process.exit(41);
}

const cmd = process.argv[3];
const args = process.argv.slice(4);
if (!cmd) {
  console.error("DENY: missing command");
  process.exit(42);
}

const sessionId = process.env.OPENCLAW_SESSION_KEY || process.env.OPENCLAW_SESSION || "unknown-session";
const execId = `exec_${randomUUID()}`;

const decisionResp = await requestDecision({
  sessionId,
  cmd,
  args,
  runPlan,
});

if (!decisionResp?.ok) {
  console.error(`DENY: guard error: ${decisionResp?.error || "unknown"}`);
  process.exit(50);
}

const decision = decisionResp.decision;
appendLocalEvent(sessionId, {
  ts: nowIso(),
  execId,
  kind: "exec.request",
  cmd,
  args,
  decision,
  guardAudit: decisionResp.audit,
});

if (decision.decision !== "allow") {
  console.error(`DENY: ${decision.decision.toUpperCase()}: ${decision.reason}`);
  if (decision.decision === "approve") {
    console.error(`approvalId: ${decision.approvalId}`);
  }
  process.exit(45);
}

// Containment (MVP): force cwd to workspace.
const child = spawn(cmd, args, { cwd: WORKSPACE, stdio: "inherit", env: process.env });
child.on("exit", (code, signal) => {
  appendLocalEvent(sessionId, {
    ts: nowIso(),
    execId,
    kind: "exec.result",
    code: code ?? null,
    signal: signal ?? null,
  });
  process.exit(code ?? 1);
});
