#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

function stop(message, code = 2) {
  process.stderr.write(JSON.stringify({ ok: false, error: message }) + "\n");
  process.exit(code);
}

function parse(values) {
  const out = { _: [] };
  for (let i = 0; i < values.length; i += 1) {
    const value = values[i];
    if (!value.startsWith("--")) out._.push(value);
    else {
      const key = value.slice(2);
      const next = values[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        out[key] = next;
        i += 1;
      } else out[key] = true;
    }
  }
  return out;
}

function need(args, key) {
  const value = args[key];
  if (value === undefined || value === true || String(value).trim() === "") stop("Missing --" + key);
  return String(value);
}

function root() {
  return path.resolve(process.env.OPENCLAW_UPGRADE_HOME || path.join(os.homedir(), ".openclaw", "upgrade-runs"));
}

function ensure(dir) {
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
}

function put(file, value) {
  ensure(path.dirname(file));
  const temp = file + ".tmp-" + process.pid + "-" + crypto.randomBytes(3).toString("hex");
  fs.writeFileSync(temp, JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  fs.renameSync(temp, file);
}

function get(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function event(dir, action, status) {
  fs.appendFileSync(path.join(dir, "events.jsonl"), JSON.stringify({
    at: new Date().toISOString(), action, status
  }) + "\n", { mode: 0o600 });
}

function exactVersion(value) {
  if (!/^\d{4}\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(value)) stop("Use an exact version");
  return value;
}

function snapshot(args) {
  const cliPath = path.resolve(need(args, "cli-path"));
  if (!path.isAbsolute(cliPath) || !fs.existsSync(cliPath)) stop("CLI path must exist");
  const cliVersion = exactVersion(need(args, "cli-version"));
  const allowed = new Set(["tag", "no-restart", "yes", "json", "dry-run"]);
  const capabilities = [...new Set(need(args, "capabilities").split(",").map((v) => v.trim()).filter(Boolean))].sort();
  if (!capabilities.length || capabilities.some((v) => !allowed.has(v))) stop("Unknown capability");
  return { cliPath: fs.realpathSync(cliPath), cliVersion, capabilities };
}

function hash(value) {
  return crypto.createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

function newId() {
  return new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z") +
    "-" + crypto.randomBytes(3).toString("hex");
}

function runDir(id) {
  if (!/^[A-Za-z0-9._:+-]+$/.test(id || "")) stop("Invalid run id");
  return path.join(root(), id);
}

function load(id) {
  const dir = runDir(id);
  const file = path.join(dir, "manifest.json");
  if (!fs.existsSync(file)) stop("Unknown run");
  return { dir, file, data: get(file) };
}

function save(ctx) {
  ctx.data.updatedAt = new Date().toISOString();
  put(ctx.file, ctx.data);
}

function acquire(id) {
  const dir = path.join(root(), "active.lock");
  try {
    fs.mkdirSync(dir, { mode: 0o700 });
    put(path.join(dir, "owner.json"), { runId: id, createdAt: new Date().toISOString() });
  } catch {
    stop("Another upgrade transaction owns active.lock");
  }
}

function release(id) {
  const dir = path.join(root(), "active.lock");
  try {
    const owner = get(path.join(dir, "owner.json"));
    if (owner.runId !== id) return;
    fs.unlinkSync(path.join(dir, "owner.json"));
    fs.rmdirSync(dir);
  } catch {}
}

function plan(args) {
  const target = exactVersion(need(args, "target"));
  const baseline = snapshot(args);
  const id = newId();
  const dir = runDir(id);
  ensure(dir);
  const data = {
    schemaVersion: 3,
    runId: id,
    status: "PLAN_READY",
    target,
    baseline,
    fingerprint: hash(baseline),
    attempts: {
      coreUpdate: 0,
      service: { install: 0, restart: 0, forceInstall: 0, bootout: 0 }
    },
    reentryRefusals: 0,
    serviceReentryRefusals: 0,
    classifications: [],
    observations: [],
    gates: { cli: null, gateway: null, rpc: null, config: null, channels: null, stable: null },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  put(path.join(dir, "manifest.json"), data);
  fs.writeFileSync(path.join(dir, "events.jsonl"), "", { mode: 0o600 });
  event(dir, "plan", data.status);
  process.stdout.write(JSON.stringify({ ok: true, runId: id, status: data.status, target, baseline }, null, 2) + "\n");
}

function status(args) {
  const ctx = load(need(args, "run"));
  process.stdout.write(JSON.stringify({ ok: true, ...ctx.data }, null, 2) + "\n");
}

function begin(args) {
  const id = need(args, "run");
  if (need(args, "confirm") !== id) stop("Confirmation must match run id");
  const ctx = load(id);
  if (ctx.data.attempts.coreUpdate >= 1) {
    ctx.data.reentryRefusals = (ctx.data.reentryRefusals || 0) + 1;
    ctx.data.lastRefusal = "UPDATE_REENTRY_DETECTED";
    save(ctx);
    event(ctx.dir, "begin_refused", ctx.data.status);
    stop("Core update already began");
  }
  if (ctx.data.status !== "PLAN_READY") stop("Run is not ready");
  const current = snapshot(args);
  if (hash(current) !== ctx.data.fingerprint) {
    ctx.data.status = "PLAN_STALE";
    save(ctx);
    event(ctx.dir, "fingerprint_refused", ctx.data.status);
    stop("Verified snapshot changed");
  }
  const required = ["json", "no-restart", "tag", "yes"];
  if (required.some((value) => !current.capabilities.includes(value))) {
    ctx.data.status = "COMMAND_CAPABILITY_UNSUPPORTED";
    save(ctx);
    event(ctx.dir, "capability_refused", ctx.data.status);
    stop("Required capability is absent");
  }
  acquire(id);
  ctx.data.attempts.coreUpdate = 1;
  ctx.data.status = "CORE_UPDATE_RUNNING";
  save(ctx);
  event(ctx.dir, "core_armed", ctx.data.status);
  const command = [current.cliPath, "update", "--tag", ctx.data.target, "--no-restart", "--yes", "--json"];
  process.stdout.write(JSON.stringify({ ok: true, runId: id, status: ctx.data.status, command }, null, 2) + "\n");
}

function record(args) {
  const id = need(args, "run");
  const ctx = load(id);
  if (ctx.data.status !== "CORE_UPDATE_RUNNING") stop("Run is not awaiting a core result");
  const observed = exactVersion(need(args, "observed-version"));
  const exit = Number(need(args, "exit-code"));
  ctx.data.coreResult = { exit, observed };
  ctx.data.status = observed === ctx.data.target
    ? (exit === 0 ? "CORE_APPLIED" : "CORE_APPLIED_WITH_POST_FAILURE")
    : "CORE_UPDATE_FAILED";
  save(ctx);
  event(ctx.dir, "core_recorded", ctx.data.status);
  release(id);
  process.stdout.write(JSON.stringify({ ok: true, runId: id, status: ctx.data.status }, null, 2) + "\n");
}


const classificationKinds = new Set([
  "UPDATE_COMPETITION", "CORE_UPDATE_FAILED", "CORE_APPLIED_WITH_POST_FAILURE",
  "MIGRATION_NOTICE", "MIGRATION_LOCKED", "MIGRATION_BLOCKED",
  "DUPLICATE_SOURCE_RECOVERABLE", "SERVICE_DEFINITION_DRIFT",
  "GATEWAY_EXTERNAL_SIGTERM", "READINESS_FAILED", "STABILITY_FAILED",
  "MANUAL_INTERVENTION_REQUIRED"
]);

function classify(args) {
  const ctx = load(need(args, "run"));
  const kind = need(args, "kind");
  if (!classificationKinds.has(kind)) stop("Unknown classification");
  const evidence = need(args, "evidence");
  if (evidence.length > 240) stop("Evidence reference is too long");
  ctx.data.classifications.push({ at: new Date().toISOString(), kind, evidence });
  if (kind !== "MIGRATION_NOTICE" && ctx.data.status !== "COMPLETE") {
    ctx.data.frozenFrom = ctx.data.status;
    ctx.data.status = "FAILURE_FROZEN";
  }
  save(ctx);
  event(ctx.dir, "classify_" + kind.toLowerCase(), ctx.data.status);
  process.stdout.write(JSON.stringify({ ok: true, runId: ctx.data.runId, status: ctx.data.status, kind }, null, 2) + "\n");
}

function resume(args) {
  const ctx = load(need(args, "run"));
  const decisions = {
    PLAN_READY: "VERIFY_BACKUP_AND_CONFIRM",
    CORE_UPDATE_RUNNING: "RECORD_EXISTING_CORE_RESULT",
    CORE_APPLIED: "RECONCILE_SERVICE_OR_OBSERVE",
    SERVICE_ACTION_RUNNING: "RECORD_EXISTING_SERVICE_RESULT",
    SERVICE_RECONCILED: "COLLECT_STABILITY_OBSERVATIONS",
    COMPLETE: "NO_ACTION"
  };
  const nextAction = decisions[ctx.data.status] || "STOP_WITH_EVIDENCE";
  process.stdout.write(JSON.stringify({
    ok: true, runId: ctx.data.runId, status: ctx.data.status,
    nextAction, mutationAllowed: false
  }, null, 2) + "\n");
}

const serviceActions = new Set(["install", "restart", "force-install", "bootout"]);

function beginService(args) {
  const id = need(args, "run");
  if (need(args, "confirm") !== id) stop("Confirmation must match run id");
  const ctx = load(id);
  const action = need(args, "action");
  if (!serviceActions.has(action)) stop("Unknown service action");
  const total = Object.values(ctx.data.attempts.service).reduce((sum, value) => sum + value, 0);
  if (total >= 1) {
    ctx.data.serviceReentryRefusals = (ctx.data.serviceReentryRefusals || 0) + 1;
    ctx.data.lastRefusal = "SERVICE_ACTION_REENTRY_DETECTED";
    save(ctx);
    event(ctx.dir, "service_begin_refused", ctx.data.status);
    stop("Service action already began");
  }
  if (ctx.data.status !== "CORE_APPLIED") stop("Core is not ready for service reconciliation");
  ctx.data.attempts.service[action] = 1;
  ctx.data.serviceAction = { action, result: null, armedAt: new Date().toISOString() };
  ctx.data.status = "SERVICE_ACTION_RUNNING";
  save(ctx);
  event(ctx.dir, "service_armed_" + action, ctx.data.status);
  process.stdout.write(JSON.stringify({
    ok: true, runId: id, status: ctx.data.status, authorizedAction: action
  }, null, 2) + "\n");
}

function recordService(args) {
  const ctx = load(need(args, "run"));
  if (ctx.data.status !== "SERVICE_ACTION_RUNNING") stop("Run is not awaiting a service result");
  const result = need(args, "result");
  if (!["pass", "fail"].includes(result)) stop("--result must be pass or fail");
  ctx.data.serviceAction.result = result;
  ctx.data.serviceAction.recordedAt = new Date().toISOString();
  ctx.data.status = result === "pass" ? "SERVICE_RECONCILED" : "FAILURE_FROZEN";
  if (result === "fail") ctx.data.classifications.push({
    at: new Date().toISOString(),
    kind: "MANUAL_INTERVENTION_REQUIRED",
    evidence: "service-action-failed"
  });
  save(ctx);
  event(ctx.dir, "service_recorded", ctx.data.status);
  process.stdout.write(JSON.stringify({ ok: true, runId: ctx.data.runId, status: ctx.data.status }, null, 2) + "\n");
}

function verdict(args, key) {
  const value = need(args, key);
  if (!["pass", "fail"].includes(value)) stop("--" + key + " must be pass or fail");
  return value === "pass";
}

function flag(args, key) {
  const value = need(args, key);
  if (!["yes", "no"].includes(value)) stop("--" + key + " must be yes or no");
  return value === "yes";
}

function observe(args) {
  const ctx = load(need(args, "run"));
  if (!["CORE_APPLIED", "SERVICE_RECONCILED"].includes(ctx.data.status)) stop("Run is not ready for stability observations");
  const at = new Date(need(args, "at"));
  const gatewayPid = Number(need(args, "gateway-pid"));
  const binaryInode = Number(need(args, "binary-inode"));
  const sourceUpdateCount = Number(need(args, "source-update-count"));
  if (!Number.isFinite(at.getTime())) stop("Invalid observation timestamp");
  if (![gatewayPid, binaryInode, sourceUpdateCount].every(Number.isInteger) ||
      gatewayPid <= 0 || binaryInode < 0 || sourceUpdateCount < 0) stop("Invalid numeric observation field");
  ctx.data.observations.push({
    at: at.toISOString(),
    gatewayPid,
    binaryPath: path.resolve(need(args, "binary-path")),
    binaryInode,
    service: verdict(args, "service"),
    port: verdict(args, "port"),
    rpc: verdict(args, "rpc"),
    app: verdict(args, "app"),
    channels: verdict(args, "channels"),
    fatal: flag(args, "fatal"),
    sigterm: flag(args, "sigterm"),
    sourceUpdateCount
  });
  ctx.data.observations.sort((a, b) => Date.parse(a.at) - Date.parse(b.at));
  if (ctx.data.observations.length > 20) ctx.data.observations = ctx.data.observations.slice(-20);
  save(ctx);
  event(ctx.dir, "observe", ctx.data.status);
  process.stdout.write(JSON.stringify({ ok: true, runId: ctx.data.runId, observationCount: ctx.data.observations.length }, null, 2) + "\n");
}

function stability(data) {
  const samples = data.observations || [];
  if (samples.length < 3) return { pass: false, reason: "need-at-least-three-samples" };
  const first = samples[0];
  const last = samples[samples.length - 1];
  const spanSeconds = (Date.parse(last.at) - Date.parse(first.at)) / 1000;
  if (spanSeconds < 120) return { pass: false, reason: "window-shorter-than-120-seconds", spanSeconds };
  const identity = samples.every((sample) =>
    sample.gatewayPid === first.gatewayPid &&
    sample.binaryPath === first.binaryPath &&
    sample.binaryInode === first.binaryInode
  );
  const readiness = samples.every((sample) =>
    sample.service && sample.port && sample.rpc && sample.app && sample.channels
  );
  const clean = samples.every((sample) => !sample.fatal && !sample.sigterm);
  const noUpdateDelta = last.sourceUpdateCount === first.sourceUpdateCount;
  const pass = identity && readiness && clean && noUpdateDelta;
  return {
    pass, reason: pass ? "stable" : "sample-invariant-failed",
    spanSeconds, sampleCount: samples.length, identity, readiness, clean, noUpdateDelta
  };
}

function finish(args) {
  const id = need(args, "run");
  const ctx = load(id);
  const names = ["cli", "gateway", "rpc", "config", "channels"];
  for (const name of names) ctx.data.gates[name] = verdict(args, name);
  const stable = stability(ctx.data);
  ctx.data.gates.stable = stable.pass;
  ctx.data.stability = stable;
  const passed = names.every((name) => ctx.data.gates[name] === true) && stable.pass;
  if (passed && ["CORE_APPLIED", "SERVICE_RECONCILED"].includes(ctx.data.status)) {
    ctx.data.status = "COMPLETE";
    ctx.data.result = "success";
  } else {
    ctx.data.status = "STOPPED_WITH_EVIDENCE";
    ctx.data.result = "not_complete";
  }
  save(ctx);
  event(ctx.dir, "finish", ctx.data.status);
  process.stdout.write(JSON.stringify({
    ok: passed, runId: id, status: ctx.data.status,
    gates: ctx.data.gates, stability: stable
  }, null, 2) + "\n");
  if (!passed) process.exitCode = 3;
}

const args = parse(process.argv.slice(2));
ensure(root());
if (args._[0] === "plan") plan(args);
else if (args._[0] === "status") status(args);
else if (args._[0] === "begin-core") begin(args);
else if (args._[0] === "record-core") record(args);
else if (args._[0] === "classify") classify(args);
else if (args._[0] === "resume") resume(args);
else if (args._[0] === "begin-service") beginService(args);
else if (args._[0] === "record-service") recordService(args);
else if (args._[0] === "observe") observe(args);
else if (args._[0] === "finish") finish(args);
else stop("Use plan, status, begin-core, record-core, classify, resume, begin-service, record-service, observe, or finish");
