#!/usr/bin/env node
// Portable dispatch for libraries already named by the public skill index.
// It does not rank sellers, sign, pay, or treat a catalog flag as authority.
import { spawn, spawnSync } from "node:child_process";
import { createHash, randomBytes, randomUUID } from "node:crypto";
import {
  createOutputBudget,
  observationIdentity,
  requestIdentity,
  selectSuccessfulObservation,
} from "./delivery-contracts/contracts.mjs";
import {
  appendFileSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PINS_PATH = join(SKILL_ROOT, "references/pins.json");
const REQUEST_SCHEMA = "neomorphic.received-useful-work.request.v1";
const EVENT_SCHEMA = "neomorphic.received-useful-work.event.v1";
const EXECUTION_MODE = "contract_replay";
const CALLER_MODE = "caller";
const RECORDER = "received-useful-work.dispatch";
const ISO_TIME = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/;
const FORBIDDEN_KEY = /grant|token|wallet|authorization|signature|secret|password|credential|preimage|cookie|claimurl|email/i;
const MAINTAINED_SOURCES = new Set(["moltjobs", "x402stats", "smithery_mcp"]);
const NEXT_ACTION = {
  now: "Supply now as an ISO-8601 UTC timestamp. The wall clock and the replay dates are not used.",
  task: "Supply task as one pinned task id. The label selects a library and is not authority or a paid task.",
  expectedOutput: "Supply expectedOutput as one expected output of that task.",
  inputs: "Supply inputs as an object.",
  "inputs.request": "Supply inputs.request as the caller composition document. examples/admissible.json is not loaded.",
  "inputs.request.evidence": "Supply inputs.request.evidence.feed or inputs.request.evidence.routeLockRequest. A route label without that evidence is not used.",
  "inputs.request.now": "Supply inputs.request.now as the composition clock. A fixture date is not written in.",
  "inputs.store": "Supply inputs.store as the caller-owned composition directory before compare.",
  "inputs.network": "Supply inputs.network. The replay networks are not used.",
  "inputs.body": "Supply inputs.body as a file path, or inputs.source as supported, not both and not neither.",
  "inputs.source": "Supply inputs.source only as supported, together with observedAt, expiresAt, and now. An unsupplied live clock is not used.",
  "inputs.observedAt": "Supply inputs.observedAt for the source observation.",
  "inputs.expiresAt": "Supply inputs.expiresAt after now. A replay expiry is not used.",
  "inputs.owner": "Supply inputs.owner. An owner is not invented.",
  "inputs.observation": "Supply inputs.observation as the caller projection file. The bundled projection is not loaded.",
  "inputs.intervalMs": "Supply inputs.intervalMs as an integer from 0 through 7 days.",
  "inputs.maxRuns": "Supply inputs.maxRuns as an integer from 1 through 100.",
  "inputs.maxUseful": "Supply inputs.maxUseful as an integer from 1 through 20.",
  "inputs.explicitOptIn": "Supply inputs.explicitOptIn true. Opt-in is not assumed.",
  "inputs.receiverKind": "Supply inputs.receiverKind local-vm or inputs.receivers as a receiver file.",
  "inputs.continuationHome": "Supply inputs.continuationHome as a caller-owned directory. An empty example home is not created, and the grant is not accepted in this request.",
  "inputs.budget": "Supply inputs.budget as the caller budget file. The walletless fixture budget is not loaded.",
  "inputs.subject": "Supply inputs.subject as a file path, or inputs.subjectArchive true for the pinned public archive. A missing path is not replaced.",
  "inputs.contributorId": "Supply inputs.contributorId matching ^[a-z0-9_]{1,64}$.",
};

export function loadPins() {
  return JSON.parse(readFileSync(PINS_PATH, "utf8"));
}

function nodeBin() {
  if (process.env.NEOMORPHIC_NODE && existsSync(process.env.NEOMORPHIC_NODE)) return process.env.NEOMORPHIC_NODE;
  return process.execPath;
}

export const PUBLIC_GET_HEADERS = Object.freeze({
  accept: "*/*",
  "user-agent": "received-useful-work/0.1.1",
});

export const NPM_REGISTRY = "https://registry.npmjs.org";

// Child processes do not inherit the caller home, npm token, proxy, or shell.
// Their home and temp directory are created under the caller work directory.
export function childEnvironment(cwd) {
  if (typeof cwd !== "string" || cwd.length === 0 || cwd.includes("\0")) {
    throw Object.assign(new Error("output_scope_required"), { code: "output_scope_required" });
  }
  const home = join(cwd, ".received-child-home");
  const tmp = join(home, "tmp");
  mkdirSync(tmp, { recursive: true, mode: 0o700 });
  const npmrc = join(home, "npmrc");
  if (!existsSync(npmrc)) writeFileSync(npmrc, "fund=false\naudit=false\nupdate-notifier=false\n", { mode: 0o600 });
  const node = nodeBin();
  return {
    PATH: `${dirname(node)}:/usr/bin:/bin`,
    HOME: home,
    LANG: "C",
    LC_ALL: "C",
    TMPDIR: tmp,
    NEOMORPHIC_NODE: node,
    npm_config_fund: "false",
    npm_config_audit: "false",
    npm_config_update_notifier: "false",
    npm_config_userconfig: npmrc,
    npm_config_registry: NPM_REGISTRY,
  };
}

export function reviewPublicGet(urlString) {
  let url;
  try { url = new URL(urlString); }
  catch { throw Object.assign(new Error("blocked_origin"), { code: "blocked_origin" }); }
  if (url.username || url.password || url.hash) {
    throw Object.assign(new Error("credential_url"), { code: "credential_url" });
  }
  const loopback = url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "localhost");
  const retained = url.protocol === "https:"
    && url.hostname === "agents.samedaydesk.com"
    && url.pathname.startsWith("/.well-known/useful-result-reuse/");
  if (!loopback && !retained) throw Object.assign(new Error("blocked_origin"), { code: "blocked_origin" });
  return { href: url.href, method: "GET", headers: { ...PUBLIC_GET_HEADERS }, body: null };
}

function publicCopy(value, depth = 0) {
  if (depth > 6 || value == null) return value ?? null;
  if (typeof value === "number" || typeof value === "boolean") return value;
  if (typeof value === "string") {
    if (/[0-9a-f]{64}/i.test(value)) return value.replace(/[0-9a-f]{64}/gi, "[redacted]");
    if (value.length > 400) return `${value.slice(0, 160)}…`;
    return value;
  }
  if (Array.isArray(value)) return value.slice(0, 16).map((item) => publicCopy(item, depth + 1));
  if (typeof value === "object") {
    const out = {};
    for (const [key, child] of Object.entries(value)) {
      if (FORBIDDEN_KEY.test(key)) continue;
      if ((key === "requestIdentity" || key === "observationIdentity") && typeof child === "string" && /^[0-9a-f]{64}$/.test(child)) {
        out[key] = child;
        continue;
      }
      out[key] = publicCopy(child, depth + 1);
    }
    return out;
  }
  return null;
}

function sha256File(file) {
  const hash = createHash("sha256");
  const data = readFileSync(file);
  hash.update(data);
  return { hex: hash.digest("hex"), bytes: data.length };
}

function functionById(pins, id) {
  return pins.functions.find((item) => item.id === id) || null;
}

export function budgetOf(request) {
  const budget = request?.budget && typeof request.budget === "object" ? request.budget : {};
  const timeoutMs = Number(budget.timeoutMs ?? 8000);
  const bodyBytes = Number(budget.bodyBytes ?? 65536);
  const outputBytes = Number(budget.outputBytes ?? 200_000);
  return {
    maxUsd: budget.maxUsd ?? null,
    pay: budget.pay === true,
    timeoutMs: Number.isInteger(timeoutMs) && timeoutMs >= 1000 ? timeoutMs : 8000,
    bodyBytes: Number.isInteger(bodyBytes) ? Math.min(Math.max(bodyBytes, 1), 65536) : 65536,
    outputBytes: Number.isInteger(outputBytes) && outputBytes >= 1024 ? Math.min(outputBytes, 200_000) : 200_000,
    ceilingIsNotSpend: budget.ceilingIsNotSpend !== false,
  };
}

function clockOf(request) {
  const now = request?.now || new Date().toISOString();
  const parsed = Date.parse(now);
  return Number.isFinite(parsed) ? new Date(parsed).toISOString() : new Date().toISOString();
}

export function isIso(value) {
  return typeof value === "string" && ISO_TIME.test(value) && Number.isFinite(Date.parse(value));
}

export function executionModeOf(request) {
  if (!request || typeof request !== "object" || Array.isArray(request)) return EXECUTION_MODE;
  const mode = request.executionMode;
  if (mode == null || mode === EXECUTION_MODE) return EXECUTION_MODE;
  if (mode === CALLER_MODE) return CALLER_MODE;
  return "invalid";
}

export function nodeSatisfies(actual, required) {
  const left = String(actual || "").split(".").map((part) => Number(part));
  const right = String(required || "").split(".").map((part) => Number(part));
  if (left.length < 3 || right.length < 3) return false;
  if (left.some((part) => !Number.isInteger(part)) || right.some((part) => !Number.isInteger(part))) return false;
  for (let index = 0; index < 3; index += 1) {
    if (left[index] > right[index]) return true;
    if (left[index] < right[index]) return false;
  }
  return true;
}

function chargeCaptured(outputBudget, stdout, stderr) {
  if (!outputBudget) return null;
  try {
    outputBudget.charge(String(stdout || ""));
    outputBudget.charge(String(stderr || ""));
    return null;
  } catch (error) {
    if (error?.code === "output_budget") return "output_budget";
    throw error;
  }
}

function resolvedNodeVersion(deadline, outputBudget) {
  const bin = nodeBin();
  if (bin === process.execPath) return process.versions.node;
  const remaining = remainingMs(deadline);
  if (remaining <= 0) return null;
  const ran = spawnSync(bin, ["-p", "process.versions.node"], {
    encoding: "utf8",
    timeout: Math.min(5000, remaining),
    env: { PATH: `${dirname(bin)}:/usr/bin:/bin`, LANG: "C", LC_ALL: "C" },
  });
  const budgetHit = chargeCaptured(outputBudget, ran.stdout, ran.stderr);
  if (remainingMs(deadline) <= 0) return null;
  if (budgetHit) return "output_budget";
  return ran.status === 0 ? String(ran.stdout || "").trim() : null;
}

function runtimeBlock(fn, deadline, outputBudget) {
  if (!fn?.node) return null;
  const actual = resolvedNodeVersion(deadline, outputBudget);
  if (remainingMs(deadline) <= 0) {
    return { code: 124, elapsedMs: 0, failure: "deadline", usefulRefusal: false,
      publicResult: { reason: "deadline", nextAction: "Runtime validation exhausted the caller\'s whole-operation deadline." } };
  }
  if (actual === "output_budget") {
    return {
      code: 1, elapsedMs: 0, failure: "output_budget", usefulRefusal: false,
      publicResult: { reason: "output_budget", nextAction: "The operation output budget was exhausted. Later owned children were not started." },
    };
  }
  if (nodeSatisfies(actual, fn.node)) return null;
  return {
    code: 2,
    elapsedMs: 0,
    failure: "node_runtime",
    usefulRefusal: false,
    publicResult: {
      reason: "node_runtime",
      required: fn.node,
      actual,
      nextAction: `Use Node >= ${fn.node} via NEOMORPHIC_NODE or the invoking process. This command does not search a home directory or reinstall Node.`,
    },
  };
}

function regularFile(file) {
  try {
    const info = lstatSync(file);
    return info.isFile() && !info.isSymbolicLink();
  } catch {
    return false;
  }
}

function directoryOf(file) {
  try {
    const info = lstatSync(file);
    return info.isDirectory() && !info.isSymbolicLink();
  } catch {
    return false;
  }
}

function nextActionFor(missing, fnId) {
  return missing.map((key) => {
    if (key === "inputs.source" && fnId === "maintained-observation") {
      return "Supply inputs.source as moltjobs, x402stats, or smithery_mcp. A new source is not enrolled.";
    }
    if (key === "inputs.home") return "Supply inputs.home as an existing caller-owned directory, or omit it.";
    return NEXT_ACTION[key] || `Supply ${key} and rerun with executionMode caller. A bundled example is not loaded.`;
  }).join(" ");
}

function missingInput(base, fn, missing) {
  return {
    ...base,
    ok: true,
    exit: 0,
    decision: "useful_refusal",
    reason: "missing_input",
    selected: fn ? viewOf(fn) : null,
    run: false,
    useful: true,
    coverage: "known",
    missing,
    nextAction: nextActionFor(missing, fn?.id || null),
  };
}

export function callerGaps(request, fn) {
  const missing = [];
  const inputs = request.inputs || {};
  const now = request.now;
  if (!isIso(now)) missing.push("now");
  if (fn.id === "no-spend-composition") {
    const doc = inputs.request;
    const requestOk = doc && typeof doc === "object" && !Array.isArray(doc) && typeof doc.task?.id === "string" && doc.task.id.length > 0;
    if (!requestOk) missing.push("inputs.request");
    else {
      const evidence = doc.evidence;
      const hasEvidence = evidence && typeof evidence === "object" && (evidence.feed || evidence.routeLockRequest);
      if (!hasEvidence) missing.push("inputs.request.evidence");
      if (!isIso(doc.now)) missing.push("inputs.request.now");
    }
    if (inputs.store != null || inputs.compare === true) {
      if (typeof inputs.store !== "string" || !directoryOf(resolve(inputs.store))) missing.push("inputs.store");
    }
  }
  if (fn.id === "compatibility-query") {
    if (typeof inputs.network !== "string" || inputs.network.length < 1) missing.push("inputs.network");
    if (!isIso(inputs.observedAt)) missing.push("inputs.observedAt");
    if (!isIso(inputs.expiresAt)) missing.push("inputs.expiresAt");
    const hasBody = typeof inputs.body === "string" && inputs.body.length > 0;
    const hasSource = inputs.source != null;
    if (hasBody && hasSource) missing.push("inputs.body");
    else if (!hasBody && !hasSource) missing.push("inputs.body");
    else if (hasSource && inputs.source !== "supported") missing.push("inputs.source");
    else if (hasBody && !regularFile(resolve(inputs.body))) missing.push("inputs.body");
  }
  if (fn.id === "maintained-observation") {
    if (typeof inputs.owner !== "string" || !/^[A-Za-z0-9][A-Za-z0-9 ._-]{0,80}$/.test(inputs.owner)) missing.push("inputs.owner");
    if (typeof inputs.source !== "string" || !MAINTAINED_SOURCES.has(inputs.source)) missing.push("inputs.source");
    if (inputs.control !== "cancel") {
      if (typeof inputs.observation !== "string" || !regularFile(resolve(inputs.observation))) missing.push("inputs.observation");
    }
    if (!isIso(inputs.expiresAt) || (isIso(now) && Date.parse(inputs.expiresAt) <= Date.parse(now))) missing.push("inputs.expiresAt");
    const week = 7 * 24 * 60 * 60 * 1000;
    if (!Number.isInteger(inputs.intervalMs) || inputs.intervalMs < 0 || inputs.intervalMs > week) missing.push("inputs.intervalMs");
    if (!Number.isInteger(inputs.maxRuns) || inputs.maxRuns < 1 || inputs.maxRuns > 100) missing.push("inputs.maxRuns");
    if (!Number.isInteger(inputs.maxUseful) || inputs.maxUseful < 1 || inputs.maxUseful > 20) missing.push("inputs.maxUseful");
    if (inputs.explicitOptIn !== true) missing.push("inputs.explicitOptIn");
    const receiversOk = typeof inputs.receivers === "string" && regularFile(resolve(inputs.receivers));
    if (inputs.receiverKind !== "local-vm" && !receiversOk) missing.push("inputs.receiverKind");
    if (inputs.home != null && (typeof inputs.home !== "string" || !directoryOf(resolve(inputs.home)))) missing.push("inputs.home");
  }
  if (fn.id === "grantless-retained-read") {
    if (typeof inputs.continuationHome !== "string" || !directoryOf(resolve(inputs.continuationHome))) missing.push("inputs.continuationHome");
  }
  if (fn.id === "walletless-trial") {
    if (typeof inputs.contributorId !== "string" || !/^[a-z0-9_]{1,64}$/.test(inputs.contributorId)) missing.push("inputs.contributorId");
    if (typeof inputs.budget !== "string" || !regularFile(resolve(inputs.budget))) missing.push("inputs.budget");
    if (typeof inputs.subject === "string") {
      if (!regularFile(resolve(inputs.subject))) missing.push("inputs.subject");
    } else if (inputs.subjectArchive !== true) missing.push("inputs.subject");
  }
  return missing;
}

function scrubCaptured(value) {
  return String(value || "").replace(/[0-9a-f]{64}/gi, "[redacted]").slice(0, 180);
}

function selectFunction(pins, request) {
  const byOutput = pins.functions.filter((item) => item.expectedOutputs.includes(request.expectedOutput));
  const knownTasks = new Set(pins.functions.flatMap((item) => item.taskIds));
  if (byOutput.length === 1) {
    const fn = byOutput[0];
    if (knownTasks.has(request.task) && !fn.taskIds.includes(request.task)) return null;
    return fn;
  }
  if (byOutput.length > 1) return byOutput.find((item) => item.taskIds.includes(request.task)) || null;
  return null;
}

function authorityRefusal(fn, request, now) {
  const authority = request.authority;
  if (!authority || authority.reuse !== true) return null;
  if (authority.owner && authority.owner !== fn.owner) return "wrong_owner";
  if (authority.input && authority.input !== fn.id) return "wrong_input";
  if (authority.version && authority.version !== fn.version) return "wrong_version";
  if (!authority.expiresAt) return "expiry_required";
  if (!isIso(now)) return null;
  if (Date.parse(authority.expiresAt) <= Date.parse(now)) return "expired";
  return "catalog_flag_is_not_authority";
}

function viewOf(fn) {
  return {
    id: fn.id,
    class: fn.class,
    hostedApi: false,
    subscription: false,
    spendingPermission: false,
    publicationStatus: fn.publicationStatus,
    hostedAcquisitionVerified: fn.hostedAcquisitionVerified === true,
    providerEnrollment: fn.providerEnrollment || "not_required",
    version: fn.version,
    owner: fn.owner,
    archive: fn.archive,
    sha256: fn.sha256,
    bytes: fn.bytes,
    machineEntry: fn.machineEntry,
    providerRoute: fn.providerRoute,
    consumer: fn.consumer,
    node: fn.node || null,
    taskIds: fn.taskIds || [],
    expectedOutputs: fn.expectedOutputs || [],
    taskDescription: fn.taskDescription || null,
    usages: fn.usages || [],
    entryCommands: fn.entryCommands || null,
    installedCommand: "scripts/dispatch.mjs",
    nativeProviderRoute: "/.well-known/skills/received-useful-work/SKILL.md",
    dependencies: (fn.dependencies || []).map((item) => ({
      id: item.id,
      role: item.role,
      archive: item.archive,
      sha256: item.sha256,
      bytes: item.bytes,
      required: item.required === true,
      note: item.note || null,
    })),
    authority: fn.server?.authority || "none",
    paymentAuthority: "none",
    claimAuthority: "none",
  };
}

export function qualifyRequest(request, pins = loadPins(), now = undefined) {
  const mode = executionModeOf(request);
  const resolvedNow = mode === CALLER_MODE
    ? (isIso(request?.now) ? request.now : null)
    : (now ?? clockOf(request));
  const base = {
    schema: "neomorphic.received-useful-work.qualification.v1",
    executionMode: mode === "invalid" ? (request?.executionMode ?? null) : mode,
    installedCommand: pins.installedCommand,
    nativeProviderRoute: pins.nativeProviderRoute,
    paymentAuthority: "none",
    claimAuthority: "none",
    paymentPermitted: false,
    catalogMutation: false,
    acceptedDerivativeReceived: false,
    customerExecution: "unknown",
    now: resolvedNow,
  };
  if (!request || typeof request !== "object" || Array.isArray(request)) {
    return { ...base, ok: false, exit: 2, decision: "usage", reason: "request_object" };
  }
  if (request.schema && request.schema !== REQUEST_SCHEMA) {
    return { ...base, ok: false, exit: 2, decision: "usage", reason: "request_schema" };
  }
  if (mode === "invalid") {
    return { ...base, ok: false, exit: 2, decision: "usage", reason: "execution_mode" };
  }
  const basis = request.basis || request.reason;
  if (basis === "missing_standard_402" || basis === "declaration") {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "useful_refusal",
      reason: "no_paid_need",
      selected: null,
      useful: true,
      coverage: "known",
      explanation: "A missing standard402 field or a declaration alone does not create a paid need.",
    };
  }
  if (request.expectedOutput === "accepted-derivative") {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "useful_refusal",
      reason: "accepted_derivative_not_received",
      selected: null,
      useful: true,
      coverage: "known",
      explanation: "Source-accepted contribution QA is not Root acceptance. This dispatch does not claim the scaffold has passed receiving.",
    };
  }
  const inputsOk = request.inputs && typeof request.inputs === "object" && !Array.isArray(request.inputs);
  if (typeof request.task !== "string" || typeof request.expectedOutput !== "string" || !inputsOk) {
    if (mode === CALLER_MODE) {
      const missing = [];
      if (!isIso(request.now)) missing.push("now");
      if (typeof request.task !== "string") missing.push("task");
      if (typeof request.expectedOutput !== "string") missing.push("expectedOutput");
      if (!inputsOk) missing.push("inputs");
      return missingInput(base, null, missing);
    }
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "coverage_unknown",
      reason: "incomplete_request",
      selected: null,
      useful: true,
      coverage: "unknown",
    };
  }
  const fn = selectFunction(pins, request);
  if (!fn) {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "no_fit",
      reason: "no_supported_function",
      selected: null,
      useful: true,
      coverage: "known",
    };
  }
  const refused = authorityRefusal(fn, request, resolvedNow);
  if (refused) {
    return {
      ...base,
      ok: false,
      exit: 3,
      decision: "useful_refusal",
      reason: refused,
      selected: null,
      useful: true,
      coverage: "known",
      reusedAuthority: false,
      explanation: "Old authority is not reused. Current authority is the supported server or a caller-held grant, not a catalog flag.",
    };
  }
  const budget = budgetOf(request);
  if (budget.pay === true || request.inputs.purchase === true) {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "useful_refusal",
      reason: "qualification_is_not_spending_permission",
      selected: viewOf(fn),
      run: false,
      useful: true,
      coverage: "known",
      budget,
      explanation: "The hosted library can be used without paying. This match does not authorize a purchase.",
    };
  }
  if (fn.id === "maintained-observation" && request.inputs.subscription === true) {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "useful_refusal",
      reason: "runner_is_not_a_subscription",
      selected: viewOf(fn),
      run: false,
      useful: true,
      coverage: "known",
      explanation: "The maintained runner is a free one-shot observation. It is not a subscription.",
    };
  }
  if (fn.id === "walletless-trial" && (request.inputs.wallet === true || request.inputs.walletRequired === true)) {
    return {
      ...base,
      ok: true,
      exit: 0,
      decision: "useful_refusal",
      reason: "wallet_is_not_required",
      selected: viewOf(fn),
      run: false,
      useful: true,
      coverage: "known",
    };
  }
  if (mode === CALLER_MODE) {
    const missing = callerGaps(request, fn);
    if (missing.length) return missingInput(base, fn, missing);
  }
  return {
    ...base,
    ok: true,
    exit: 0,
    decision: "match",
    reason: "supported_function",
    selected: viewOf(fn),
    run: true,
    useful: null,
    coverage: fn.hostedAcquisitionVerified === false ? "partial" : "known",
    budget,
    libraryNotHostedApi: true,
    freeRunnerNotSubscription: fn.class === "free_runner",
    providerEnrollment: fn.providerEnrollment || "not_required",
  };
}

function verifyArchive(publicRoot, spec) {
  const file = join(publicRoot, spec.archive.replace(/^\//, ""));
  if (!existsSync(file)) {
    const error = new Error(`missing archive ${spec.archive}`);
    error.code = "missing_archive";
    throw error;
  }
  const hashed = sha256File(file);
  if (hashed.hex !== spec.sha256 || hashed.bytes !== spec.bytes) {
    const error = new Error(`archive pin mismatch ${spec.archive}`);
    error.code = "tampered_archive";
    throw error;
  }
  return file;
}

function verifyMachineEntry(publicRoot, fn) {
  if (!fn.machineEntry) return null;
  const file = join(publicRoot, fn.machineEntry.replace(/^\//, ""));
  if (!existsSync(file)) return null;
  const entry = JSON.parse(readFileSync(file, "utf8"));
  if (entry.sha256 && entry.sha256 !== fn.sha256) {
    const error = new Error(`machine entry hash disagrees with pin ${fn.id}`);
    error.code = "entry_pin_mismatch";
    throw error;
  }
  if (entry.paymentAuthority && entry.paymentAuthority !== "none") {
    const error = new Error("machine entry claimed payment authority");
    error.code = "payment_authority";
    throw error;
  }
  return {
    path: fn.machineEntry,
    publicationStatus: entry.publicationStatus || fn.publicationStatus,
    hostedAcquisitionVerified: entry.hostedAcquisitionVerified === true,
    execute: entry.execute === true,
    commands: entry.commands || entry.defaultCommands || null,
  };
}

export function discoverDocument(pins = loadPins(), publicRoot = null) {
  const checked = [];
  if (publicRoot) {
    for (const fn of pins.functions) {
      const archive = verifyArchive(publicRoot, fn);
      const entry = verifyMachineEntry(publicRoot, fn);
      checked.push({ id: fn.id, archive, machineEntry: entry });
    }
  }
  return {
    schema: "neomorphic.received-useful-work.discovery.v1",
    executionMode: EXECUTION_MODE,
    callerMode: pins.callerMode || null,
    installedCommand: pins.installedCommand,
    nativeProviderRoute: pins.nativeProviderRoute,
    index: pins.index,
    paymentAuthority: "none",
    claimAuthority: "none",
    catalogMutation: false,
    acceptedDerivativeReceived: false,
    customerExecution: "unknown",
    exportResult: "export-result --log events.jsonl --task TASK --useful yes|no --note TEXT",
    exportOutput: "export-output --log events.jsonl --request REQUEST [--attempt ATTEMPT]",
    functions: pins.functions.map((fn) => {
      const found = checked.find((item) => item.id === fn.id);
      return viewOf({ ...fn, entryCommands: found?.machineEntry?.commands || null });
    }),
    checked,
  };
}

function appendEvent(log, event) {
  if (!log) return;
  mkdirSync(dirname(log), { recursive: true });
  const line = {
    schema: EVENT_SCHEMA,
    executionMode: EXECUTION_MODE,
    at: new Date().toISOString(),
    customerExecution: "unknown",
    independentCustomerUse: false,
    ownerQa: false,
    downloadCountedAsUse: false,
    forumReadCountedAsUse: false,
    paymentPermitted: false,
    claimAuthority: "none",
    inferred: false,
    ...publicCopy(event),
  };
  appendFileSync(log, `${JSON.stringify(line)}\n`);
}

function killOwned(child) {
  if (!child?.pid) return "no_pid";
  try {
    if (process.platform === "win32") child.kill("SIGKILL");
    else process.kill(-child.pid, "SIGKILL");
    return "killed";
  } catch (error) {
    if (error.code === "ESRCH") return "gone";
    try { child.kill("SIGKILL"); } catch { /* already gone */ }
    return "cleanup_failed";
  }
}

function sharedBudget(value) {
  if (value && typeof value.charge === "function" && typeof value.snapshot === "function") return value;
  const limit = Number.isInteger(value) && value >= 0 ? value : 200_000;
  return createOutputBudget(limit);
}

function spawnCaptured(command, args, { cwd, deadline, outputBudget, outputBytes }) {
  const started = Date.now();
  const budget = sharedBudget(outputBudget || outputBytes);
  const remaining = Math.max(0, deadline - started);
  if (budget.snapshot().exhausted) {
    return Promise.resolve({
      code: 1,
      signal: null,
      timedOut: false,
      failure: "output_budget",
      elapsedMs: 0,
      stdout: "",
      stderr: "",
      pid: null,
      cleanup: "not_started",
    });
  }
  if (remaining <= 0) {
    return Promise.resolve({
      code: 124,
      signal: null,
      timedOut: true,
      failure: "deadline",
      elapsedMs: 0,
      stdout: "",
      stderr: "",
      pid: null,
      cleanup: "not_started",
    });
  }
  return new Promise((resolvePromise) => {
    let child;
    try {
      child = spawn(command, args, {
        cwd,
        env: childEnvironment(cwd),
        detached: process.platform !== "win32",
        stdio: ["ignore", "pipe", "pipe"],
      });
    } catch (error) {
      resolvePromise({
        code: 1,
        signal: null,
        timedOut: false,
        failure: "spawn_failed",
        elapsedMs: Date.now() - started,
        stdout: "",
        stderr: String(error?.message || "spawn_failed").slice(0, 180),
        pid: null,
        cleanup: "not_started",
      });
      return;
    }
    let stdout = "";
    let stderr = "";
    let failure = null;
    let settled = false;
    const finish = (code, signal) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      const cleanup = killOwned(child);
      let exit = code;
      if (failure === "deadline") exit = 124;
      else if (failure === "output_budget" || failure === "spawn_failed") exit = 1;
      else if (exit == null) exit = 1;
      resolvePromise({
        code: exit,
        signal: signal || null,
        timedOut: failure === "deadline",
        failure,
        elapsedMs: Date.now() - started,
        stdout,
        stderr,
        pid: child.pid || null,
        cleanup,
      });
    };
    const timer = setTimeout(() => {
      failure ||= "deadline";
      killOwned(child);
    }, remaining);
    const capture = (which, chunk) => {
      if (failure) return;
      try {
        budget.charge(chunk);
      } catch (error) {
        if (error?.code === "output_budget") {
          failure = "output_budget";
          killOwned(child);
          return;
        }
        failure = "output_budget";
        killOwned(child);
        return;
      }
      if (which === "stdout") stdout += chunk;
      else stderr += chunk;
    };
    child.stdout.on("data", (chunk) => capture("stdout", chunk));
    child.stderr.on("data", (chunk) => capture("stderr", chunk));
    child.on("error", (error) => { failure ||= error.code || "spawn_failed"; });
    child.on("close", (code, signal) => finish(code, signal));
  });
}

function parseJson(text) {
  const trimmed = String(text || "").trim();
  if (!trimmed) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    const start = trimmed.indexOf("{");
    const end = trimmed.lastIndexOf("}");
    if (start >= 0 && end > start) {
      try {
        return JSON.parse(trimmed.slice(start, end + 1));
      } catch {
        return null;
      }
    }
    return null;
  }
}

function stepBody(ran) {
  const fromOut = parseJson(ran.stdout);
  if (fromOut && typeof fromOut === "object") return { body: fromOut, parseFailed: false, missing: false };
  const fromErr = parseJson(ran.stderr);
  if (fromErr && typeof fromErr === "object") return { body: fromErr, parseFailed: false, missing: false };
  const text = `${ran.stdout || ""}${ran.stderr || ""}`.trim();
  if (!text) return { body: null, parseFailed: false, missing: true };
  return { body: null, parseFailed: true, missing: false };
}

export function classifyStep(ran, contract) {
  if (ran.failure === "deadline" || ran.timedOut) return { matched: false, kind: null, failure: "deadline" };
  if (ran.failure === "output_budget") return { matched: false, kind: null, failure: "output_budget" };
  if (ran.failure === "spawn_failed") return { matched: false, kind: null, failure: "spawn_failed" };
  if (ran.signal || ran.code == null) return { matched: false, kind: null, failure: "signal" };
  const parsed = stepBody(ran);
  if (contract.requiresBody !== false && parsed.parseFailed) return { matched: false, kind: null, failure: "parse_failure" };
  if (contract.requiresBody !== false && parsed.missing) return { matched: false, kind: null, failure: "missing_output" };
  const step = { ...ran, body: parsed.body };
  if (contract.success && contract.success(step)) return { matched: true, kind: "success", failure: null };
  if (contract.usefulRefusal && contract.usefulRefusal(step)) return { matched: true, kind: "useful_refusal", failure: null };
  return { matched: false, kind: null, failure: "contract_mismatch" };
}

export function classifyExchange(read) {
  if (read?.failure === "deadline" || read?.code === "timeout") return { matched: false, kind: null, failure: "deadline" };
  if (read?.code === "body_budget") return { matched: false, kind: null, failure: "output_budget" };
  if (read?.code === "blocked_origin" || read?.code === "credential_url") {
    return { matched: false, kind: null, failure: read.code };
  }
  if (read?.status === 401 && read?.code === "grant_required") return { matched: true, kind: "useful_refusal", failure: null };
  if (read?.status == null) return { matched: false, kind: null, failure: "missing_output" };
  return { matched: false, kind: null, failure: "contract_mismatch" };
}

function remainingMs(deadline) {
  return Math.max(0, deadline - Date.now());
}

async function runBound(args, ctx, contract, cwd) {
  const ran = await spawnCaptured(nodeBin(), args, {
    cwd: cwd || ctx.acquired.packageDir,
    deadline: ctx.deadline,
    outputBudget: ctx.budget.outputBudget,
  });
  const parsed = stepBody(ran);
  const judged = classifyStep(ran, contract);
  return { ...ran, body: parsed.body, judged };
}

function failedStep(step, elapsedMs, publicResult = null, later = null) {
  const code = step.judged.failure === "deadline" ? 124
    : step.judged.failure === "output_budget" ? 1
      : (Number.isInteger(step.code) && step.code > 0 ? step.code : 1);
  return {
    code,
    failure: step.judged.failure,
    elapsedMs,
    capturedPrefix: scrubCaptured(`${step.stdout || ""}${step.stderr || ""}`),
    publicResult,
    later,
    usefulRefusal: false,
  };
}

async function boundedGet(urlString, { deadline, bodyBytes }) {
  const started = Date.now();
  const timeoutMs = Math.max(0, deadline - started);
  if (timeoutMs <= 0) {
    return { ok: false, status: null, code: "timeout", failure: "deadline", bytes: 0, elapsedMs: 0, error: null };
  }
  let plan;
  try { plan = reviewPublicGet(urlString); }
  catch (error) {
    return { ok: false, status: null, code: error.code || "blocked_origin", bytes: 0, elapsedMs: 0, error: null };
  }
  const signal = AbortSignal.timeout(timeoutMs);
  let response;
  try {
    response = await fetch(plan.href, { method: plan.method, headers: plan.headers, redirect: "manual", signal });
  } catch (error) {
    const timedOut = error?.name === "TimeoutError" || error?.name === "AbortError";
    return {
      ok: false,
      status: null,
      code: timedOut ? "timeout" : "unavailable",
      bytes: 0,
      elapsedMs: Date.now() - started,
      error: null,
    };
  }
  if (response.status >= 300 && response.status < 400) {
    await response.body?.cancel?.();
    return { ok: false, status: response.status, code: "redirect_rejected", bytes: 0, elapsedMs: Date.now() - started, error: null };
  }
  const reader = response.body?.getReader?.();
  let received = 0;
  const chunks = [];
  if (reader) {
    while (received <= bodyBytes) {
      if (Date.now() >= deadline) {
        await reader.cancel();
        return { ok: false, status: response.status, code: "timeout", failure: "deadline", bytes: received, elapsedMs: Date.now() - started, error: null };
      }
      const step = await reader.read();
      if (step.done) break;
      received += step.value.byteLength;
      if (received > bodyBytes) {
        await reader.cancel();
        return { ok: false, status: response.status, code: "body_budget", bytes: received, elapsedMs: Date.now() - started, error: null };
      }
      chunks.push(step.value);
    }
  }
  const text = Buffer.concat(chunks.map((chunk) => Buffer.from(chunk))).toString("utf8");
  let error = null;
  try {
    const body = JSON.parse(text);
    if (typeof body.error === "string") error = body.error.slice(0, 80);
  } catch {
    error = null;
  }
  return {
    ok: response.status === 200,
    status: response.status,
    code: response.status === 401 ? "grant_required" : (error || `http_${response.status}`),
    bytes: received,
    elapsedMs: Date.now() - started,
    error,
  };
}

function extractArchive(archiveFile, dest, deadline, outputBudget) {
  mkdirSync(dest, { recursive: true });
  return spawnCaptured("tar", ["-xzf", archiveFile, "-C", dest], { cwd: dest, deadline, outputBudget });
}

function packageDir(dest, fn) {
  if (fn.layout === "flat") return dest;
  return join(dest, fn.extractTop);
}

function throwStep(extracted) {
  if (extracted.failure === "deadline") {
    const error = new Error("deadline");
    error.code = "deadline";
    throw error;
  }
  if (extracted.failure === "output_budget") {
    const error = new Error("output_budget");
    error.code = "output_budget";
    throw error;
  }
  if (extracted.code !== 0) {
    const error = new Error(extracted.stderr.slice(0, 200) || "extract failed");
    error.code = "extract_failed";
    throw error;
  }
}

async function acquireOne(publicRoot, spec, dest, deadline, outputBudget) {
  const archiveFile = verifyArchive(publicRoot, spec);
  if (spec.layout === "unextracted") return { archiveFile, dir: null };
  const extracted = await extractArchive(archiveFile, dest, deadline, outputBudget);
  throwStep(extracted);
  return { archiveFile, dir: spec.layout === "flat" ? dest : join(dest, spec.extractTop) };
}

export async function acquireFunction(publicRoot, fn, dest, log, task, deadline, outputBudget, mode = EXECUTION_MODE) {
  const started = Date.now();
  verifyMachineEntry(publicRoot, fn);
  const budget = sharedBudget(outputBudget);
  const main = await acquireOne(publicRoot, fn, join(dest, "package"), deadline, budget);
  const dependencies = [];
  for (const dep of fn.dependencies || []) {
    if (dep.required !== true) continue;
    const got = await acquireOne(publicRoot, dep, join(dest, "deps", dep.id), deadline, budget);
    dependencies.push({ id: dep.id, role: dep.role, dir: got.dir, archiveFile: got.archiveFile });
  }
  appendEvent(log, {
    kind: "acquisition",
    executionMode: mode,
    task,
    functionId: fn.id,
    sourceClass: fn.class,
    consent: "public_bytes",
    elapsedMs: Date.now() - started,
    coverage: fn.hostedAcquisitionVerified === true ? "known" : "partial",
    join: { task, outcomeId: null, requestIdentity: null, contract: fn.contract || null },
  });
  return { packageDir: main.dir, archiveFile: main.archiveFile, dependencies };
}

function allowListed(body, keys) {
  if (!body || typeof body !== "object") return null;
  const out = {};
  for (const key of keys) {
    if (body[key] !== undefined) out[key] = publicCopy(body[key]);
  }
  return out;
}

async function runWalletless(ctx) {
  const started = Date.now();
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const crt = ctx.acquired.dependencies.find((item) => item.id === "contributor-reuse-trial");
  const subject = verifyArchive(ctx.publicRoot, ctx.fn.dependencies.find((item) => item.id === "capability-preflight"));
  const budget = join(ctx.acquired.packageDir, "experiments/funded-task-consumer-100257/fixtures/budget-walletless.json");
  const out = join(ctx.work, "trial-out");
  mkdirSync(out, { recursive: true });
  const contributor = String(ctx.request.inputs?.contributorId || "");
  if (!/^[a-z0-9_]{1,64}$/.test(contributor)) {
    return failedStep({ code: 2, stdout: "", stderr: "", judged: { failure: "contract_mismatch" } }, 0, { reason: "contributor_id" });
  }
  const ran = await runBound([
    bin, "run",
    "--crt-client", crt.dir,
    "--now", ctx.now,
    "--budget", budget,
    "--subject", subject,
    "--contributor-id", contributor,
    "--claim-key", `sha256:${randomBytes(32).toString("hex")}`,
    "--submit-key", `sha256:${randomBytes(32).toString("hex")}`,
    "--outcome", "useful_negative",
    "--timeout-ms", String(remainingMs(ctx.deadline)),
    "--out", out,
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.ok === true && step.body?.transmitted === false && step.body?.outcome === "useful_negative",
  });
  const publicResult = allowListed(ran.body, ["ok", "decision", "reason", "prepare", "transmitted", "outcome", "code"]);
  if (!ran.judged.matched) return failedStep(ran, Date.now() - started, publicResult);
  return { code: 0, elapsedMs: Date.now() - started, publicResult, usefulRefusal: false, failure: null };
}

async function runRetained(ctx) {
  const started = Date.now();
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const origin = ctx.fn.server.origin;
  const discovered = await runBound([
    bin, "discover", "--origin", origin, "--timeout-ms", String(remainingMs(ctx.deadline)),
  ], ctx, {
    success: (step) => step.code === 0
      && step.body?.schema === "samedaydesk.useful-result-reuse.current.v1"
      && step.body?.paymentPermitted === false
      && step.body?.executed === false,
  });
  const discovery = allowListed(discovered.body, [
    "schema", "paymentPermitted", "executed", "hostedReuseVerified",
    "customerRetentionHostedVerified", "compatibilityCount", "recognizedRevenueAtomic",
  ]);
  if (!discovered.judged.matched) return failedStep(discovered, Date.now() - started, { discovery });
  const read = await boundedGet(new URL(ctx.fn.server.readPath, origin).href, {
    deadline: ctx.deadline,
    bodyBytes: ctx.budget.bodyBytes,
  });
  const grant = classifyExchange(read);
  const grantless = { status: read.status, code: read.code, bytes: read.bytes, elapsedMs: read.elapsedMs };
  if (!grant.matched) {
    return failedStep(
      { code: read.code === "timeout" ? 124 : 1, stdout: "", stderr: "", judged: grant },
      Date.now() - started,
      { discovery, grantless },
    );
  }
  const home = join(ctx.work, "empty-home");
  mkdirSync(home, { recursive: true });
  const missing = await runBound([
    bin, "read", "--home", home, "--timeout-ms", String(remainingMs(ctx.deadline)),
  ], ctx, {
    usefulRefusal: (step) => step.code === 2 && step.body?.code === "missing_continuation",
  });
  const missingContinuation = allowListed(missing.body, ["code", "error"]) || { exit: missing.code };
  if (!missing.judged.matched) {
    return failedStep(missing, Date.now() - started, { discovery, grantless, missingContinuation });
  }
  const seeded = join(ctx.acquired.packageDir, "experiments/customer-retained-operations-100256/fixtures/seeded-forged-retention.json");
  const forged = await runBound([bin, "reject-seeded", "--file", seeded], ctx, {
    success: (step) => step.code === 0 && step.body?.refused === true,
  });
  const publicResult = {
    discovery,
    grantless,
    missingContinuation,
    seededRefused: forged.body?.refused === true,
    authority: "server",
  };
  if (!forged.judged.matched) return failedStep(forged, Date.now() - started, publicResult);
  return {
    code: 0,
    elapsedMs: Date.now() - started,
    publicResult,
    usefulRefusal: true,
    failure: null,
  };
}

async function runComposition(ctx) {
  const started = Date.now();
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const request = join(ctx.acquired.packageDir, "examples/admissible.json");
  const self = await runBound([bin, "self-check"], ctx, {
    success: (step) => step.code === 0 && step.body?.ok === true && step.body?.paymentSent === false && step.body?.targetAdvertisedInUpstreamInputSchema === false,
  });
  const selfCheck = allowListed(self.body, ["ok", "paymentAuthority", "paymentSent", "targetAdvertisedInUpstreamInputSchema"]);
  if (!self.judged.matched) return failedStep(self, Date.now() - started, { selfCheck });
  const decided = await runBound([bin, "decide", "--request", request], ctx, {
    success: (step) => step.code === 0 && step.body?.decision === "admissible" && step.body?.paymentSent === false && step.body?.spendAuthorized === false && step.body?.savingsObserved === false,
  });
  const decision = allowListed(decided.body, ["decision", "reason", "paymentSent", "paymentAuthority", "spendAuthorized", "savingsObserved", "cashDelta", "tokenDelta"]);
  const publicResult = {
    selfCheck,
    decision,
    optionalFeatures: { buyerMandate: "unresolved", ownerQa: false, standard402: "not_a_paid_need" },
  };
  if (!decided.judged.matched) return failedStep(decided, Date.now() - started, publicResult);
  const store = join(ctx.work, "store");
  mkdirSync(store, { recursive: true });
  const retained = await runBound([bin, "retain", "--request", request, "--store", store], ctx, {
    success: (step) => step.code === 0 && step.body?.decision === "admissible" && step.body?.paymentSent === false,
  });
  if (!retained.judged.matched) return failedStep(retained, Date.now() - started, publicResult);
  const changed = JSON.parse(readFileSync(request, "utf8"));
  changed.task = { id: "sha256-later", statement: "sha256 hash of a different string" };
  const changedPath = join(ctx.work, "changed-task.json");
  writeFileSync(changedPath, JSON.stringify(changed));
  const later = await runBound([bin, "compare", "--request", changedPath, "--store", store], ctx, {
    usefulRefusal: (step) => step.code === 2 && step.body?.decision === "refused" && step.body?.reason === "inherited_authority" && step.body?.paymentSent === false && step.body?.spendAuthorized === false,
  });
  const laterResult = {
    code: later.code,
    elapsedMs: later.elapsedMs,
    publicResult: allowListed(later.body, ["decision", "reason", "paymentSent", "paymentAuthority", "spendAuthorized"]),
  };
  if (!later.judged.matched) return failedStep(later, Date.now() - started, publicResult, laterResult);
  return {
    code: 0,
    elapsedMs: Date.now() - started,
    later: laterResult,
    publicResult,
    usefulRefusal: true,
    failure: null,
  };
}

async function runMaintained(ctx) {
  const started = Date.now();
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const task = ctx.request.task;
  const home = join(ctx.work, "home");
  const sink = join(ctx.work, "sink");
  mkdirSync(home, { recursive: true });
  mkdirSync(sink, { recursive: true });
  const receivers = join(ctx.work, "receivers.json");
  writeFileSync(receivers, `${JSON.stringify({ "local-vm": { kind: "local-http", baseUrl: "http://127.0.0.1:9" } })}\n`);
  const file = join(ctx.acquired.packageDir, "experiments/maintained-operations-100184/examples/comparable-x402.json");
  const pick = (ran) => allowListed(ran.body, ["disposition", "code", "enrollment", "applied", "paymentExecuted", "paymentAuthority", "subscriptionOffered"]);
  const opt = await runBound([
    bin, "opt-in", "--explicit", "yes",
    "--home", home, "--task", task, "--source", "x402stats",
    "--owner", "ordinary-agent", "--sink-dir", sink, "--receivers", receivers,
    "--interval-ms", "0", "--max-runs", "6", "--max-useful", "2",
    "--expires-at", "2026-10-08T00:00:00.000Z", "--now", "2026-10-01T12:00:00.000Z",
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.enrollment === "created" && step.body?.paymentExecuted === false && step.body?.code == null,
  });
  if (!opt.judged.matched) return failedStep(opt, Date.now() - started, { optIn: pick(opt) });
  const baseline = await runBound([
    bin, "run", "--home", home, "--task", task, "--file", file, "--now", "2026-10-01T12:00:00.000Z",
  ], ctx, { success: (step) => step.code === 0 && step.body?.disposition === "baseline" });
  const partial = { baseline: pick(baseline) };
  if (!baseline.judged.matched) return failedStep(baseline, Date.now() - started, partial);
  const comparable = JSON.parse(readFileSync(file, "utf8"));
  const slot = comparable.projection.sources.find((entry) => entry.sourceId === "x402stats");
  // A changed observation, not a seller ranking and not a payment.
  const sellers = slot.metrics.find((metric) => metric.key === "sellers_30d");
  sellers.value = Number(sellers.value) + 1;
  const changedPath = join(ctx.work, "changed-sellers.json");
  writeFileSync(changedPath, `${JSON.stringify(comparable)}\n`);
  const changed = await runBound([
    bin, "run", "--home", home, "--task", task, "--file", changedPath, "--now", "2026-10-01T14:00:00.000Z",
  ], ctx, { success: (step) => step.code === 0 && step.body?.disposition === "changed" });
  partial.changed = pick(changed);
  if (!changed.judged.matched) return failedStep(changed, Date.now() - started, partial);
  const unchanged = await runBound([
    bin, "run", "--home", home, "--task", task, "--file", changedPath, "--now", "2026-10-01T15:00:00.000Z",
  ], ctx, { success: (step) => step.code === 0 && step.body?.disposition === "unchanged" });
  partial.unchanged = pick(unchanged);
  if (!unchanged.judged.matched) return failedStep(unchanged, Date.now() - started, partial);
  const cancelled = await runBound([
    bin, "cancel", "--home", home, "--task", task, "--now", "2026-10-01T15:10:00.000Z",
  ], ctx, {
    // An applied cancel spreads extra.applied and exits 0. Exit 3 is an unapplied admission, not this command.
    success: (step) => step.code === 0 && step.body?.disposition === "cancelled" && step.body?.applied === true && step.body?.paymentExecuted === false,
  });
  partial.cancel = pick(cancelled);
  if (!cancelled.judged.matched) return failedStep(cancelled, Date.now() - started, partial);
  const wrong = await runBound([
    bin, "opt-in", "--explicit", "yes",
    "--home", home, "--task", task, "--source", "x402stats",
    "--owner", "other-agent", "--sink-dir", sink, "--receivers", receivers,
    "--interval-ms", "0", "--max-runs", "4", "--max-useful", "2",
    "--expires-at", "2026-10-08T00:00:00.000Z", "--now", "2026-10-01T15:20:00.000Z",
  ], ctx, { usefulRefusal: (step) => step.code === 2 && step.body?.code === "enrollment_conflict" });
  partial.wrongOwner = pick(wrong);
  partial.contract = ctx.fn.contract;
  partial.providerEnrollment = "conditional";
  if (!wrong.judged.matched) return failedStep(wrong, Date.now() - started, partial);
  return { code: 0, elapsedMs: Date.now() - started, publicResult: partial, usefulRefusal: true, failure: null };
}

async function runCompatibility(ctx) {
  const started = Date.now();
  const root = ctx.acquired.packageDir;
  const installed = await spawnCaptured("npm", ["ci", "--ignore-scripts", "--no-audit", "--no-fund"], {
    cwd: root,
    deadline: ctx.deadline,
    outputBudget: ctx.budget.outputBudget,
  });
  const setup = classifyStep(installed, {
    requiresBody: false,
    success: (step) => step.code === 0 && !step.failure,
  });
  if (!setup.matched) {
    return failedStep(
      { ...installed, judged: setup },
      Date.now() - started,
      { reason: "install_failed", exit: installed.code, failure: setup.failure },
    );
  }
  const bin = join(root, ctx.fn.consumer);
  const observed = "2026-10-01T16:11:10.000Z";
  const expires = "2026-10-01T16:16:10.000Z";
  const currentNow = "2026-10-01T16:12:00.000Z";
  const keys = ["outcome", "decision", "reason", "live", "evidenceClass", "paymentAuthorized", "savingsClaim", "task", "reusedDecision"];
  const fixture = await runBound([
    bin, "decide",
    "--body", "fixtures/supported-derived.json",
    "--observed-at", observed,
    "--expires-at", expires,
    "--now", currentNow,
    "--network", "algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe",
    "--evidence-out", "evidence-fixture",
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.outcome === "incompatible" && step.body?.decision === "mismatch" && step.body?.reason === "normalizer_and_lookup_disagree" && step.body?.live === false && step.body?.paymentAuthorized === false,
  }, root);
  const publicResult = {
    fixture: allowListed(fixture.body, keys),
    hostedAcquisitionVerified: false,
    publicationStatus: "candidate",
  };
  if (!fixture.judged.matched) return failedStep(fixture, Date.now() - started, publicResult);
  const laterTask = await runBound([
    bin, "later",
    "--evidence", "evidence-fixture",
    "--envelope", "evidence-fixture/envelope.json",
    "--now", currentNow,
    "--network", "algorand:SGO1GKSzyE7IEPItTxCByw9x8FmnrCDe",
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.task === "client-registration-bind" && step.body?.reusedDecision === false && step.body?.paymentAuthorized === false,
  }, root);
  publicResult.laterTask = allowListed(laterTask.body, keys);
  if (!laterTask.judged.matched) return failedStep(laterTask, Date.now() - started, publicResult);
  const decide = await runBound([
    bin, "decide",
    "--body", "fixtures/supported-derived.json",
    "--observed-at", observed,
    "--expires-at", expires,
    "--now", currentNow,
    "--network", "eip155:8453",
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.outcome === "known" && step.body?.decision === "exact_listed" && step.body?.live === false && step.body?.paymentAuthorized === false,
  }, root);
  publicResult.current = allowListed(decide.body, keys);
  if (!decide.judged.matched) return failedStep(decide, Date.now() - started, publicResult);
  const stale = await runBound([
    bin, "decide",
    "--body", "fixtures/supported-derived.json",
    "--observed-at", observed,
    "--expires-at", expires,
    "--now", "2026-10-01T18:00:00.000Z",
    "--network", "eip155:8453",
  ], ctx, {
    usefulRefusal: (step) => step.code === 0 && step.body?.outcome === "stale" && step.body?.reason === "source_not_current" && step.body?.paymentAuthorized === false,
  }, root);
  publicResult.stale = allowListed(stale.body, keys);
  const later = { code: stale.code, elapsedMs: stale.elapsedMs, publicResult: publicResult.stale };
  if (!stale.judged.matched) return failedStep(stale, Date.now() - started, publicResult, later);
  const seeded = await runBound([bin, "decide", "--import", "seeded-refuse"], ctx, {
    requiresBody: false,
    usefulRefusal: (step) => step.code === 2 && /unknown flag --import/.test(`${step.stderr || ""}${step.stdout || ""}`),
  }, root);
  publicResult.seededImport = { code: seeded.code, refused: seeded.judged.kind === "useful_refusal" };
  if (!seeded.judged.matched) return failedStep(seeded, Date.now() - started, publicResult, later);
  return {
    code: 0,
    elapsedMs: Date.now() - started,
    later,
    publicResult,
    usefulRefusal: true,
    failure: null,
  };
}

function finishCaller(started, ran, publicResult, later = null) {
  if (ran.judged?.kind === "useful_refusal") {
    return { code: 0, elapsedMs: Date.now() - started, publicResult, later, usefulRefusal: true, failure: null };
  }
  if (!ran.judged?.matched) return failedStep(ran, Date.now() - started, publicResult, later);
  return { code: 0, elapsedMs: Date.now() - started, publicResult, later, usefulRefusal: false, failure: null };
}

async function runWalletlessCaller(ctx) {
  const started = Date.now();
  const blocked = runtimeBlock(ctx.fn, ctx.deadline, ctx.budget.outputBudget);
  if (blocked) return blocked;
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const crt = ctx.acquired.dependencies.find((item) => item.id === "contributor-reuse-trial");
  const trial = join(crt.dir, "bin/trial.mjs");
  const inputs = ctx.request.inputs;
  const subject = typeof inputs.subject === "string"
    ? resolve(inputs.subject)
    : verifyArchive(ctx.publicRoot, ctx.fn.dependencies.find((item) => item.id === "capability-preflight"));
  const budget = resolve(inputs.budget);
  const measure = join(ctx.work, "caller-measure");
  mkdirSync(measure, { recursive: true });
  const evaluated = await runBound([
    trial, "evaluate", "--subject", subject, "--out", measure,
  ], ctx, {
    success: (step) => step.code === 0 && typeof step.body?.negative === "string",
  }, crt.dir);
  if (!evaluated.judged.matched) return failedStep(evaluated, Date.now() - started, { reason: "evaluation_failed" });
  let measurement = null;
  try {
    measurement = JSON.parse(readFileSync(join(measure, "measurement.json"), "utf8"));
  } catch {
    return failedStep({ code: 1, stdout: "", stderr: "", judged: { failure: "missing_output" } }, Date.now() - started, { reason: "missing_output" });
  }
  const failures = measurement?.negative?.failures;
  const concrete = Array.isArray(failures) && failures.some((item) => typeof item === "string" && item.length > 0);
  let outcome = null;
  if (evaluated.body.negative === "integrated_partial" && concrete) outcome = "useful_negative";
  else if (evaluated.body.releaseAcceptance === true && evaluated.body.negative !== "integrated_partial") outcome = "useful_positive";
  if (!outcome) {
    return {
      code: 0,
      elapsedMs: Date.now() - started,
      publicResult: {
        reason: "outcome_not_measured",
        negative: evaluated.body.negative,
        releaseAcceptance: evaluated.body.releaseAcceptance === true,
        nextAction: "The trial measurement did not record a concrete negative failure or release acceptance. A request outcome string is not used.",
      },
      usefulRefusal: true,
      failure: null,
    };
  }
  const out = join(ctx.work, "trial-out");
  mkdirSync(out, { recursive: true });
  const ran = await runBound([
    bin, "run",
    "--crt-client", crt.dir,
    "--now", ctx.now,
    "--budget", budget,
    "--subject", subject,
    "--contributor-id", inputs.contributorId,
    "--claim-key", `sha256:${randomBytes(32).toString("hex")}`,
    "--submit-key", `sha256:${randomBytes(32).toString("hex")}`,
    "--outcome", outcome,
    // Frozen trial discover refuses a timeout above 8000. The caller deadline still bounds the child.
    "--timeout-ms", String(Math.min(8000, Math.max(50, remainingMs(ctx.deadline)))),
    "--out", out,
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.ok === true && step.body?.transmitted === false && step.body?.outcome === outcome,
    usefulRefusal: (step) => step.code === 3 && step.body?.decision === "decline" && Boolean(step.body?.reason) && step.body?.prepare === false,
  });
  const publicResult = {
    ...(allowListed(ran.body, ["ok", "decision", "reason", "prepare", "transmitted", "outcome", "code"]) || {}),
    measuredOutcome: outcome,
    requestedOutcomeIgnored: inputs.outcome != null,
  };
  return finishCaller(started, ran, publicResult);
}

async function runRetainedCaller(ctx) {
  const started = Date.now();
  const blocked = runtimeBlock(ctx.fn, ctx.deadline, ctx.budget.outputBudget);
  if (blocked) return blocked;
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const home = resolve(ctx.request.inputs.continuationHome);
  const timeout = Math.min(20000, Math.max(1000, remainingMs(ctx.deadline)));
  const ran = await runBound([
    bin, "read", "--home", home, "--now", ctx.now, "--timeout-ms", String(timeout),
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.disposition === "useful_read" && step.body?.usefulEvent === true && step.body?.paymentPermitted === false,
    usefulRefusal: (step) => step.code === 2 && step.body?.code === "missing_continuation",
  });
  const publicResult = allowListed(ran.body, ["disposition", "code", "paymentPermitted", "usefulEvent", "paidJob", "nextAction", "operationId"]);
  return finishCaller(started, ran, publicResult);
}

async function runCompositionCaller(ctx) {
  const started = Date.now();
  const blocked = runtimeBlock(ctx.fn, ctx.deadline, ctx.budget.outputBudget);
  if (blocked) return blocked;
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const inputs = ctx.request.inputs;
  const taskId = inputs.request.task.id;
  const self = await runBound([bin, "self-check"], ctx, {
    success: (step) => step.code === 0 && step.body?.ok === true && step.body?.paymentSent === false && step.body?.targetAdvertisedInUpstreamInputSchema === false,
  });
  const selfCheck = allowListed(self.body, ["ok", "paymentAuthority", "paymentSent", "targetAdvertisedInUpstreamInputSchema"]);
  if (!self.judged.matched) return failedStep(self, Date.now() - started, { selfCheck });
  const requestPath = join(ctx.work, "caller-request.json");
  writeFileSync(requestPath, JSON.stringify(inputs.request));
  const keys = ["decision", "reason", "paymentSent", "paymentAuthority", "spendAuthorized", "savingsObserved", "task"];
  if (inputs.compare === true) {
    const compared = await runBound([
      bin, "compare", "--request", requestPath, "--store", resolve(inputs.store),
    ], ctx, {
      usefulRefusal: (step) => step.code === 2 && step.body?.decision === "refused" && step.body?.reason === "inherited_authority" && step.body?.paymentSent === false && step.body?.spendAuthorized === false,
    });
    const publicResult = {
      selfCheck,
      decision: allowListed(compared.body, keys),
      taskId,
    };
    return finishCaller(started, compared, publicResult);
  }
  const decided = await runBound([bin, "decide", "--request", requestPath], ctx, {
    success: (step) => step.code === 0 && step.body?.decision === "admissible" && step.body?.paymentSent === false && step.body?.spendAuthorized === false && step.body?.task?.id === taskId,
  });
  const publicResult = {
    selfCheck,
    decision: allowListed(decided.body, keys),
    taskId,
  };
  if (!decided.judged.matched) return failedStep(decided, Date.now() - started, publicResult);
  if (typeof inputs.store === "string") {
    const retained = await runBound([
      bin, "retain", "--request", requestPath, "--store", resolve(inputs.store),
    ], ctx, {
      success: (step) => step.code === 0 && step.body?.decision === "admissible" && step.body?.paymentSent === false && step.body?.task?.id === taskId,
    });
    publicResult.retained = allowListed(retained.body, ["decision", "reason", "paymentSent"]);
    if (!retained.judged.matched) return failedStep(retained, Date.now() - started, publicResult);
  }
  return { code: 0, elapsedMs: Date.now() - started, publicResult, usefulRefusal: false, failure: null };
}

async function runMaintainedCaller(ctx) {
  const started = Date.now();
  const blocked = runtimeBlock(ctx.fn, ctx.deadline, ctx.budget.outputBudget);
  if (blocked) return blocked;
  const bin = join(ctx.acquired.packageDir, ctx.fn.consumer);
  const inputs = ctx.request.inputs;
  const task = ctx.request.task;
  const home = typeof inputs.home === "string" ? resolve(inputs.home) : join(ctx.work, "home");
  if (typeof inputs.home !== "string") mkdirSync(home, { recursive: true });
  const sink = typeof inputs.home === "string" ? join(home, "sink") : join(ctx.work, "sink");
  mkdirSync(sink, { recursive: true });
  let receivers;
  if (inputs.receiverKind === "local-vm") {
    receivers = join(ctx.work, "receivers.json");
    writeFileSync(receivers, `${JSON.stringify({ "local-vm": { kind: "local-http", baseUrl: "http://127.0.0.1:9" } })}\n`);
  } else receivers = resolve(inputs.receivers);
  const pick = (ran) => allowListed(ran.body, ["disposition", "code", "enrollment", "applied", "paymentExecuted", "paymentAuthority", "subscriptionOffered"]);
  if (inputs.control === "cancel") {
    const cancelled = await runBound([
      bin, "cancel", "--home", home, "--task", task, "--now", ctx.now,
    ], ctx, {
      success: (step) => step.code === 0 && step.body?.disposition === "cancelled" && step.body?.applied === true && step.body?.paymentExecuted === false,
    });
    return finishCaller(started, cancelled, { cancel: pick(cancelled), contract: ctx.fn.contract, providerEnrollment: "conditional" });
  }
  const opt = await runBound([
    bin, "opt-in", "--explicit", "yes",
    "--home", home, "--task", task, "--source", inputs.source,
    "--owner", inputs.owner, "--sink-dir", sink, "--receivers", receivers,
    "--interval-ms", String(inputs.intervalMs),
    "--max-runs", String(inputs.maxRuns),
    "--max-useful", String(inputs.maxUseful),
    "--expires-at", inputs.expiresAt, "--now", ctx.now,
  ], ctx, {
    success: (step) => step.code === 0 && (step.body?.enrollment === "created" || step.body?.enrollment === "existing") && step.body?.paymentExecuted === false && step.body?.code == null,
    usefulRefusal: (step) => step.code === 2 && step.body?.code === "enrollment_conflict",
  });
  const partial = { optIn: pick(opt), contract: ctx.fn.contract, providerEnrollment: "conditional" };
  if (opt.judged.kind === "useful_refusal") return finishCaller(started, opt, partial);
  if (!opt.judged.matched) return failedStep(opt, Date.now() - started, partial);
  const ran = await runBound([
    bin, "run", "--home", home, "--task", task, "--file", resolve(inputs.observation), "--now", ctx.now,
  ], ctx, {
    success: (step) => step.code === 0 && ["baseline", "unchanged", "changed"].includes(step.body?.disposition) && step.body?.paymentExecuted === false,
  });
  partial.run = pick(ran);
  return finishCaller(started, ran, partial);
}

async function runCompatibilityCaller(ctx) {
  const started = Date.now();
  const blocked = runtimeBlock(ctx.fn, ctx.deadline, ctx.budget.outputBudget);
  if (blocked) return blocked;
  const root = ctx.acquired.packageDir;
  if (!existsSync(join(root, "node_modules"))) {
    const installed = await spawnCaptured("npm", ["ci", "--ignore-scripts", "--no-audit", "--no-fund"], {
      cwd: root,
      deadline: ctx.deadline,
      outputBudget: ctx.budget.outputBudget,
    });
    const setup = classifyStep(installed, { requiresBody: false, success: (step) => step.code === 0 && !step.failure });
    if (!setup.matched) {
      return failedStep({ ...installed, judged: setup }, Date.now() - started, { reason: "install_failed", exit: installed.code, failure: setup.failure });
    }
  }
  const bin = join(root, ctx.fn.consumer);
  const inputs = ctx.request.inputs;
  const body = inputs.source === "supported" ? "fixtures/supported-derived.json" : resolve(inputs.body);
  const evidence = join(ctx.work, "caller-evidence");
  const keys = ["outcome", "decision", "reason", "live", "evidenceClass", "paymentAuthorized", "savingsClaim", "task", "reusedDecision"];
  const decided = await runBound([
    bin, "decide",
    "--body", body,
    "--observed-at", inputs.observedAt,
    "--expires-at", inputs.expiresAt,
    "--now", ctx.now,
    "--network", inputs.network,
    "--evidence-out", evidence,
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.paymentAuthorized === false && step.body?.outcome && step.body.outcome !== "stale",
    usefulRefusal: (step) => step.code === 0 && step.body?.outcome === "stale" && step.body?.reason === "source_not_current" && step.body?.paymentAuthorized === false,
  }, root);
  const publicResult = {
    current: allowListed(decided.body, keys),
    hostedAcquisitionVerified: false,
    publicationStatus: ctx.fn.publicationStatus || "candidate",
  };
  if (decided.judged.kind === "useful_refusal") return finishCaller(started, decided, publicResult);
  if (!decided.judged.matched) return failedStep(decided, Date.now() - started, publicResult);
  if (typeof inputs.laterTask !== "string" || inputs.laterTask.length < 1) {
    return { code: 0, elapsedMs: Date.now() - started, publicResult, usefulRefusal: false, failure: null };
  }
  const laterRan = await runBound([
    bin, "later",
    "--task", inputs.laterTask,
    "--evidence", evidence,
    "--envelope", join(evidence, "envelope.json"),
    "--now", ctx.now,
    "--network", inputs.network,
  ], ctx, {
    success: (step) => step.code === 0 && step.body?.task === inputs.laterTask && step.body?.reusedDecision === false && step.body?.paymentAuthorized === false,
  }, root);
  publicResult.laterTask = allowListed(laterRan.body, keys);
  const later = { code: laterRan.code, elapsedMs: laterRan.elapsedMs, publicResult: publicResult.laterTask };
  if (!laterRan.judged.matched) return failedStep(laterRan, Date.now() - started, publicResult, later);
  return { code: 0, elapsedMs: Date.now() - started, later, publicResult, usefulRefusal: false, failure: null };
}

const RUNNERS = {
  "walletless-trial": runWalletless,
  "grantless-retained-read": runRetained,
  "no-spend-composition": runComposition,
  "maintained-observation": runMaintained,
  "compatibility-query": runCompatibility,
};

const CALLER_RUNNERS = {
  "walletless-trial": runWalletlessCaller,
  "grantless-retained-read": runRetainedCaller,
  "no-spend-composition": runCompositionCaller,
  "maintained-observation": runMaintainedCaller,
  "compatibility-query": runCompatibilityCaller,
};

function failureResult(qualified, error) {
  const deadline = error.code === "deadline";
  return {
    qualified,
    executed: false,
    exit: deadline ? 124 : 1,
    failure: error.code,
    observed: { failure: error.code },
    customerExecution: "unknown",
  };
}

export async function runRequest({ request, publicRoot, work, log }) {
  const pins = loadPins();
  const mode = executionModeOf(request);
  const now = mode === CALLER_MODE ? (isIso(request?.now) ? request.now : null) : clockOf(request);
  const qualified = qualifyRequest(request, pins, now);
  const budget = budgetOf(request);
  const deadline = Date.now() + budget.timeoutMs;
  const record = (event) => appendEvent(log, { ...event, executionMode: qualified.executionMode || EXECUTION_MODE });
  record({
    kind: "source_discovery",
    task: request?.task || null,
    functionId: qualified.selected?.id || null,
    sourceClass: qualified.selected?.class || "unknown",
    consent: "public_bytes",
    qualification: qualified.decision,
    decision: qualified.decision,
    reason: qualified.reason,
    expectedOutput: request?.expectedOutput || null,
    execution: null,
    coverage: qualified.coverage || "unknown",
    join: { task: request?.task || null, outcomeId: null, requestIdentity: null },
  });
  if (!qualified.run) return { qualified, executed: false, nextAction: qualified.nextAction || null };
  const fn = functionById(pins, qualified.selected.id);
  const outputBudget = createOutputBudget(budget.outputBytes);
  budget.outputBudget = outputBudget;
  let identity;
  try {
    identity = requestIdentity(deliveryRequestOf(request, fn, qualified.executionMode || EXECUTION_MODE));
  } catch (error) {
    return {
      qualified, executed: false, exit: 2, failure: error.code || "request_missing",
      nextAction: error.message || "The exact request could not be canonicalized.",
      customerExecution: "unknown",
    };
  }
  const attemptId = randomUUID();
  record({
    kind: "execution_attempt",
    recorder: RECORDER,
    supplied: false,
    attemptId,
    requestIdentity: identity,
    task: request.task,
    functionId: fn.id,
    sourceClass: fn.class,
    consent: "public_bytes",
    qualification: qualified.decision,
    expectedOutput: request.expectedOutput,
    execution: null,
    coverage: qualified.coverage,
    join: { task: request.task, outcomeId: null, requestIdentity: identity, contract: fn.contract || null },
  });
  const recordObservation = (ran) => {
    const outcome = ran.usefulRefusal === true ? "refused" : (ran.code === 0 && !ran.failure ? "success" : "failed");
    const draft = {
      kind: "observed_output",
      recorder: RECORDER,
      supplied: false,
      attemptId,
      requestIdentity: identity,
      outcome,
      task: request.task,
      functionId: fn.id,
      sourceClass: fn.class,
      consent: "public_bytes",
      elapsedMs: ran.elapsedMs,
      exit: ran.code ?? null,
      useful: null,
      qualification: qualified.decision,
      expectedOutput: request.expectedOutput,
      execution: { exit: ran.code, executionSucceeded: ran.code === 0 && !ran.failure, failure: ran.failure || null },
      executionSucceeded: ran.code === 0 && !ran.failure,
      failure: ran.failure ?? null,
      coverage: qualified.coverage,
      observed: ran.publicResult ?? null,
      result: ran.publicResult ?? null,
      join: { task: request.task, outcomeId: null, requestIdentity: identity, contract: fn.contract || null },
    };
    // Identity is over the same public copy appendEvent stores. A second copy at
    // the same depth is stable, so export recomputes the stored observation.
    const copied = publicCopy(draft);
    const observationId = observationIdentity({
      requestIdentity: identity,
      attemptId,
      outcome,
      exit: copied.exit ?? null,
      failure: copied.failure ?? null,
      result: copied.result ?? null,
    });
    record({ ...draft, observationIdentity: observationId });
  };
  if (qualified.executionMode === CALLER_MODE) {
    const blocked = runtimeBlock(fn, deadline, outputBudget);
    if (blocked) {
      recordObservation({ code: blocked.code, failure: blocked.failure, publicResult: blocked.publicResult, elapsedMs: blocked.elapsedMs, usefulRefusal: false });
      return {
        qualified,
        executed: false,
        exit: blocked.code,
        failure: blocked.failure,
        observed: blocked.publicResult,
        customerExecution: "unknown",
      };
    }
  }
  let acquired;
  try {
    acquired = await acquireFunction(publicRoot, fn, join(work, "acquire"), log, request.task, deadline, outputBudget, qualified.executionMode || EXECUTION_MODE);
  } catch (error) {
    if (error.code === "deadline" || error.code === "output_budget") {
      recordObservation({ code: error.code === "deadline" ? 124 : 1, failure: error.code, publicResult: { failure: error.code }, elapsedMs: 0, usefulRefusal: false });
      return failureResult(qualified, error);
    }
    throw error;
  }
  const started = Date.now();
  const runners = qualified.executionMode === CALLER_MODE ? CALLER_RUNNERS : RUNNERS;
  const ran = await runners[fn.id]({
    fn,
    request,
    publicRoot,
    work,
    acquired,
    now,
    budget,
    deadline,
  });
  const executionSucceeded = ran.code === 0 && !ran.failure;
  recordObservation(ran);
  const refusalObserved = executionSucceeded && ran.usefulRefusal === true;
  if (refusalObserved) {
    record({
      kind: "useful_refusal",
      task: request.task,
      functionId: fn.id,
      sourceClass: fn.server ? "server_record" : fn.class,
      consent: "public_bytes",
      elapsedMs: ran.elapsedMs,
      useful: null,
      qualification: qualified.decision,
      expectedOutput: request.expectedOutput,
      execution: { exit: ran.code, executionSucceeded: true, failure: null },
      coverage: qualified.coverage,
      observed: ran.publicResult?.grantless || ran.publicResult?.stale || ran.publicResult?.wrongOwner || ran.later?.publicResult || ran.publicResult,
      reusedAuthority: false,
      join: { task: request.task, outcomeId: null, requestIdentity: null },
    });
  }
  if (ran.later) {
    record({
      kind: "later_continuation",
      task: request.task,
      functionId: fn.id,
      sourceClass: fn.class,
      consent: "public_bytes",
      elapsedMs: ran.later.elapsedMs,
      exit: ran.later.code,
      qualification: qualified.decision,
      expectedOutput: request.expectedOutput,
      execution: { exit: ran.later.code, executionSucceeded: !ran.failure, failure: ran.failure || null },
      observed: ran.later.publicResult,
      reusedAuthority: false,
      join: { task: request.task, outcomeId: null, requestIdentity: null },
    });
  }
  return {
    qualified,
    executed: true,
    elapsedMs: Date.now() - started,
    exit: ran.code,
    failure: ran.failure || null,
    capturedPrefix: ran.capturedPrefix ? scrubCaptured(ran.capturedPrefix) : null,
    observed: ran.publicResult,
    later: ran.later?.publicResult || null,
    customerExecution: "unknown",
    exportResult: "caller-controlled explicit result export; static host did not observe customer execution",
  };
}

function parseArgs(argv) {
  if (argv.includes("--pay") || argv.includes("--settle") || argv.includes("--sign")) {
    return { error: "refusing --pay" };
  }
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      out._.push(token);
      continue;
    }
    const key = token.slice(2);
    const value = argv[i + 1];
    if (value == null || value.startsWith("--")) out[key] = true;
    else {
      out[key] = value;
      i += 1;
    }
  }
  return out;
}

function emit(document, exit) {
  process.stdout.write(`${JSON.stringify(document, null, 2)}\n`);
  process.exitCode = exit;
}

export function executionOutcome(result) {
  const qualification = result.qualified;
  if (result.failure) {
    const exit = Number.isInteger(result.exit) && result.exit > 0 ? result.exit : 1;
    return { exit, ok: false };
  }
  const exit = qualification.exit !== 0 ? qualification.exit
    : !result.executed ? 0
    : Number.isInteger(result.exit) && result.exit >= 0 ? result.exit : 1;
  const usefulRefusal = !result.executed && exit === 3 && qualification.decision === "useful_refusal";
  return { exit, ok: qualification.ok === true && (exit === 0 || usefulRefusal) };
}

function deliveryRequestOf(request, fn, mode) {
  const inputs = request?.inputs && typeof request.inputs === "object" && !Array.isArray(request.inputs) ? request.inputs : {};
  return {
    taskId: String(request.task),
    operation: "run",
    functionId: fn.id,
    version: String(fn.version),
    callerInputs: inputs,
    expectedOutput: request.expectedOutput,
    context: {
      source: inputs.source ?? null,
      now: request.now ?? null,
      authority: request.authority ?? null,
    },
    contract: {
      id: fn.contract ?? null,
      output: request.expectedOutput,
    },
    executionMode: mode,
  };
}

function exportFailure(reason, exit, nextAction) {
  return {
    ok: false,
    reason,
    exit,
    nextAction,
    useful: null,
    settlement: null,
    laterUse: null,
    independentExecution: false,
    provenance: "log_schema_not_external_witness",
  };
}

function exportExecuted(log, flags) {
  if (typeof flags.request !== "string") {
    return exportFailure(
      "legacy_task_export",
      2,
      "Pass --request with the exact admitted request. A task id is not an observation selector. If several successes match, also pass --attempt.",
    );
  }
  if (typeof log !== "string" || !existsSync(log) || !existsSync(flags.request)) {
    return exportFailure("missing_output", 2, "The log and the exact request file must both exist.");
  }
  let request;
  try {
    request = JSON.parse(readFileSync(flags.request, "utf8"));
  } catch {
    return exportFailure("request_missing", 2, "The request file is not JSON.");
  }
  const loaded = applyMode(request, flags);
  if (loaded.error) return exportFailure(loaded.error, 2, "The export mode must match the admitted request.");
  request = loaded.request;
  if (typeof flags.task === "string" && flags.task !== request.task) {
    return exportFailure("request_mismatch", 2, "The --task value does not match the exact request. Pass the request that was admitted.");
  }
  const pins = loadPins();
  const qualified = qualifyRequest(request, pins);
  if (!qualified.run || !qualified.selected?.id) {
    return exportFailure(qualified.reason || "not_qualified", qualified.exit || 2, qualified.nextAction || "The request is not an admitted run.");
  }
  const fn = functionById(pins, qualified.selected.id);
  let identity;
  try {
    identity = requestIdentity(deliveryRequestOf(request, fn, qualified.executionMode || EXECUTION_MODE));
  } catch (error) {
    return exportFailure(error.code || "request_missing", 2, error.message);
  }
  const rows = [];
  for (const line of readFileSync(log, "utf8").split("\n")) {
    if (!line) continue;
    try { rows.push(JSON.parse(line)); } catch { /* torn or foreign line is not a record */ }
  }
  const observations = rows.filter((row) => row && row.kind === "observed_output" && (row.requestIdentity === identity || row.task === request.task));
  const attempts = new Set(rows.filter((row) => row && row.kind === "execution_attempt" && row.recorder === RECORDER && row.supplied !== true && row.requestIdentity === identity).map((row) => row.attemptId));
  const sameRequest = observations.filter((row) => row.requestIdentity === identity);
  const trusted = sameRequest.filter((row) => row.supplied !== true && row.recorder === RECORDER && attempts.has(row.attemptId));
  if (!trusted.length) {
    if (observations.some((row) => !row.requestIdentity)) {
      return exportFailure("legacy_observation_migration", 2, "This log has task-only observations. Re-run the exact request so the recorder writes attempt and outcome rows. Prior observations are not invented.");
    }
    if (sameRequest.length) {
      return exportFailure("supplied_log", 2, "A lone or caller-supplied observation is not execution evidence. Export only a log this dispatcher recorded for the exact request.");
    }
    return exportFailure("missing_evidence", 2, "No recorded observation matches this exact request.");
  }
  let selected;
  try {
    selected = selectSuccessfulObservation(trusted, deliveryRequestOf(request, fn, qualified.executionMode || EXECUTION_MODE), {
      attemptId: typeof flags.attempt === "string" ? flags.attempt : undefined,
    });
  } catch (error) {
    return exportFailure(error.code || "observation_missing", 2, error.message || "The recorded observation is not a complete outcome.");
  }
  if (!selected.ok) {
    const next = selected.code === "ambiguous_evidence"
      ? "Several successes match this request. Pass --attempt with the attempt id to export one."
      : selected.code === "execution_not_successful"
        ? "The recorded attempt did not succeed. A caller executionSucceeded flag is not promoted."
        : "No successful observation matches this exact request and attempt.";
    return exportFailure(selected.code, 2, next);
  }
  appendEvent(log, {
    kind: "executed_output",
    executionMode: qualified.executionMode || EXECUTION_MODE,
    recorder: RECORDER,
    supplied: false,
    task: request.task,
    functionId: fn.id,
    sourceClass: "executed_output",
    consent: "public_bytes",
    useful: null,
    settlement: null,
    laterUse: null,
    customerExecution: "unknown",
    inferred: false,
    independentExecution: false,
    provenance: "log_schema_not_external_witness",
    attemptId: selected.attemptId,
    requestIdentity: selected.requestIdentity,
    observationIdentity: selected.observationIdentity,
    observed: selected.result,
    join: { task: request.task, outcomeId: null, requestIdentity: selected.requestIdentity },
  });
  return {
    ok: true,
    kind: "executed_output",
    useful: null,
    settlement: null,
    laterUse: null,
    inferred: false,
    independentExecution: false,
    provenance: "log_schema_not_external_witness",
    attemptId: selected.attemptId,
    requestIdentity: selected.requestIdentity,
    observationIdentity: selected.observationIdentity,
    exit: 0,
  };
}

function applyMode(request, flags) {
  if (flags.mode == null) return { request };
  if (request && request.executionMode && request.executionMode !== flags.mode) return { error: "mode_conflict" };
  return { request: { ...(request || {}), executionMode: flags.mode } };
}

async function main(argv) {
  const flags = parseArgs(argv);
  if (flags.error) {
    emit({ ok: false, reason: flags.error, paymentPermitted: false }, 2);
    return;
  }
  if (flags.mode != null && flags.mode !== CALLER_MODE && flags.mode !== EXECUTION_MODE) {
    emit({ ok: false, reason: "execution_mode", paymentPermitted: false }, 2);
    return;
  }
  const command = flags._[0] || "discover";
  const log = flags.log || null;
  try {
    if (command === "discover") {
      const document = discoverDocument(loadPins(), flags["public-root"] || null);
      if (log) {
        appendEvent(log, {
          kind: "source_discovery",
          task: null,
          functionId: null,
          sourceClass: "public_index",
          consent: "public_bytes",
          coverage: "known",
          functions: document.functions.map((item) => item.id),
        });
      }
      emit({ ok: true, ...document }, 0);
      return;
    }
    if (command === "qualify") {
      const loaded = applyMode(JSON.parse(readFileSync(flags.request, "utf8")), flags);
      if (loaded.error) {
        emit({ ok: false, reason: loaded.error, paymentPermitted: false }, 2);
        return;
      }
      const qualified = qualifyRequest(loaded.request);
      emit(qualified, qualified.exit);
      return;
    }
    if (command === "export-result") {
      appendEvent(log, {
        kind: "caller_export",
        executionMode: "caller_asserted",
        task: flags.task || null,
        functionId: null,
        sourceClass: "caller_export",
        consent: "caller_export",
        customerExecution: "caller_asserted",
        useful: flags.useful === "yes",
        note: typeof flags.note === "string" ? flags.note.slice(0, 180) : null,
        inferred: false,
        join: { task: flags.task || null, outcomeId: null, requestIdentity: null },
      });
      emit({ ok: true, kind: "caller_export", customerExecution: "caller_asserted", inferred: false }, 0);
      return;
    }
    if (command === "export-output") {
      const exported = exportExecuted(log, flags);
      emit({ ...exported, customerExecution: "unknown", paymentPermitted: false }, exported.exit);
      return;
    }
    if (command === "run") {
      const loaded = applyMode(JSON.parse(readFileSync(flags.request, "utf8")), flags);
      if (loaded.error) {
        emit({ ok: false, reason: loaded.error, paymentPermitted: false }, 2);
        return;
      }
      const result = await runRequest({
        request: loaded.request,
        publicRoot: flags["public-root"],
        work: flags.work,
        log,
      });
      const outcome = executionOutcome(result);
      emit({
        ok: outcome.ok,
        executionMode: result.qualified?.executionMode || EXECUTION_MODE,
        qualified: result.qualified,
        executed: result.executed,
        executionExit: result.exit ?? null,
        failure: result.failure || null,
        capturedPrefix: result.capturedPrefix ? scrubCaptured(result.capturedPrefix) : null,
        elapsedMs: result.elapsedMs ?? null,
        observed: result.observed ?? null,
        later: result.later ?? null,
        nextAction: result.nextAction || result.qualified?.nextAction || null,
        customerExecution: "unknown",
        paymentPermitted: false,
      }, outcome.exit);
      return;
    }
    emit({ ok: false, reason: "usage" }, 2);
  } catch (error) {
    const code = error.code || "failed";
    const exit = code === "tampered_archive" || code === "entry_pin_mismatch" ? 2 : 1;
    emit({ ok: false, reason: code, message: String(error.message || "").slice(0, 180), paymentPermitted: false }, exit);
  }
}

const invoked = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) await main(process.argv.slice(2));
