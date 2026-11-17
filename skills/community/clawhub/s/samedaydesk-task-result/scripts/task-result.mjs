#!/usr/bin/env node
// Acquire the pinned samedaydesk-caller-result 0.1.1 archive and run its
// existing retain, recovery, and optional feedback contracts on caller-owned files.
import { createHash } from "node:crypto";
import { constants } from "node:fs";
import { closeSync, mkdirSync, openSync, readFileSync, writeSync } from "node:fs";
import { mkdir, open, readFile, realpath, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { gunzipSync } from "node:zlib";

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MAX_INPUT_BYTES = 2 * 1024 * 1024;
const MAX_CHILD_OUTPUT = 1024 * 1024;
const FETCH_TIMEOUT_MS = 15_000;
const NPM_TIMEOUT_MS = 120_000;
const KNOWN_FLAGS = new Set([
  "work", "public-root", "install", "result", "out", "caller", "action", "operation",
  "checkpoint", "grant", "channel", "endpoint", "disposition", "reason", "resource",
  "header-file", "purchase", "send", "pay", "settle", "sign", "wallet",
]);
const AUTHORITY_CODES = new Set([
  "endpoint_rejected", "operation_binding_rejected", "payment_binding_rejected", "operation_too_large",
  "raw_sdk_client_required", "checkpoint_rejected", "checkpoint_file_rejected", "checkpoint_result_integrity",
  "checkpoint_too_large", "checkpoint_binding_changed", "current_grant_required",
]);

export const PIN = JSON.parse(readFileSync(path.join(SKILL_ROOT, "references", "caller-pin.json"), "utf8"));

export function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function code(name) {
  const error = new Error(name);
  error.code = name;
  return error;
}

function baseResult(extra = {}) {
  return { usefulness: "unknown", paymentCreated: false, ...extra };
}

export function parseArgs(argv) {
  const [command, ...rest] = argv;
  const flags = {};
  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (!item.startsWith("--")) throw code("flag_rejected");
    const key = item.slice(2);
    if (!KNOWN_FLAGS.has(key)) throw code("flag_rejected");
    if (["pay", "settle", "sign", "wallet"].includes(key)) {
      flags[key] = true;
      continue;
    }
    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) throw code("flag_rejected");
    flags[key] = value;
    index += 1;
  }
  return { command, flags };
}

function finish(status, payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
  process.exit(status);
}

export function allowedPublicRoot(value) {
  if (value === undefined) {
    return { origin: PIN.origin, receiving: "hosted_descriptor", hostedAcceptance: false };
  }
  let url;
  try { url = new URL(value); } catch { throw code("public_root_rejected"); }
  const loopback = url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "[::1]");
  if (!loopback || !url.port || url.username || url.password || url.pathname !== "/" || url.search || url.hash) {
    throw code("public_root_rejected");
  }
  return { origin: url.origin, receiving: "local_receiving", hostedAcceptance: false };
}

function pinnedRequest(origin, pathname) {
  const url = new URL(pathname, origin);
  if (url.origin !== origin || url.pathname !== pathname || url.search || url.hash || url.username) {
    throw code("cross_origin_refused");
  }
  return url;
}

async function getExact(url, maxBytes) {
  const response = await fetch(url, {
    method: "GET",
    redirect: "manual",
    headers: { accept: "*/*", "accept-encoding": "identity" },
    signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
  });
  if (response.status >= 300 && response.status < 400) {
    await response.body?.cancel();
    throw code("redirect_refused");
  }
  if (response.status !== 200) {
    await response.body?.cancel();
    throw code("fetch_failed");
  }
  const reader = response.body?.getReader();
  if (!reader) throw code("fetch_failed");
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const next = await reader.read();
      if (next.done) break;
      total += next.value.byteLength;
      if (total > maxBytes) {
        await reader.cancel();
        throw code("body_too_large");
      }
      chunks.push(Buffer.from(next.value));
    }
  } catch (error) {
    if (error?.code === "body_too_large") throw error;
    throw code("fetch_failed");
  }
  return Buffer.concat(chunks);
}

function parseJson(bytes) {
  try { return JSON.parse(bytes.toString("utf8")); } catch { return null; }
}

function classifyDescriptor(bytes) {
  const parsed = parseJson(bytes);
  const canonicalArchive = `${PIN.origin}${PIN.files.archive.path}`;
  if (parsed && typeof parsed.archive === "string" && parsed.archive !== canonicalArchive) {
    let archiveOrigin = "";
    try { archiveOrigin = new URL(parsed.archive).origin; } catch { archiveOrigin = "unparseable"; }
    if (archiveOrigin !== PIN.origin) throw code("cross_origin_refused");
  }
  if (parsed && (parsed.version === PIN.rejectedArchive.version || parsed.sha256 === PIN.rejectedArchive.sha256
    || parsed.name !== PIN.package || parsed.version !== PIN.version)) {
    throw code("source_disagreement");
  }
  if (bytes.length !== PIN.files.descriptor.bytes || sha256(bytes) !== PIN.files.descriptor.sha256) {
    throw code("tampered_descriptor");
  }
  if (!parsed || parsed.npmPublished !== false || parsed.bytes !== PIN.files.archive.bytes
    || parsed.sha256 !== PIN.files.archive.sha256 || parsed.archive !== canonicalArchive) {
    throw code("source_disagreement");
  }
  return parsed;
}

function classifyProvenance(bytes) {
  const parsed = parseJson(bytes);
  if (parsed && (parsed.version === PIN.rejectedArchive.version || parsed.package !== PIN.package || parsed.version !== PIN.version)) {
    throw code("source_disagreement");
  }
  if (bytes.length !== PIN.files.provenance.bytes || sha256(bytes) !== PIN.files.provenance.sha256) {
    throw code("tampered_provenance");
  }
}

function classifyNamed(bytes, spec, label) {
  if (bytes.length !== spec.bytes || sha256(bytes) !== spec.sha256) throw code(`tampered_${label}`);
}

function classifyArchive(bytes) {
  if (sha256(bytes) === PIN.rejectedArchive.sha256 || bytes.length === PIN.rejectedArchive.bytes && sha256(bytes) === PIN.rejectedArchive.sha256) {
    throw code("source_disagreement");
  }
  if (bytes.length < PIN.files.archive.bytes) {
    if (sha256(bytes) === PIN.rejectedArchive.sha256) throw code("source_disagreement");
    throw code("truncated_archive");
  }
  if (bytes.length !== PIN.files.archive.bytes || sha256(bytes) !== PIN.files.archive.sha256) throw code("tampered_archive");
}

function readOctal(buffer, start, length) {
  const raw = buffer.subarray(start, start + length);
  const zero = raw.indexOf(0);
  const text = (zero === -1 ? raw : raw.subarray(0, zero)).toString("utf8").trim();
  if (!/^[0-7]+$/.test(text)) throw code("tampered_archive");
  return Number.parseInt(text, 8);
}

function cString(buffer) {
  const zero = buffer.indexOf(0);
  return (zero === -1 ? buffer : buffer.subarray(0, zero)).toString("utf8");
}

function headerChecksum(header) {
  let sum = 0;
  for (let index = 0; index < 512; index += 1) sum += index >= 148 && index < 156 ? 32 : header[index];
  return sum;
}

function safeMember(name) {
  if (!name || name.startsWith("/") || name.includes("\\") || name.includes("\0")) throw code("traversal_refused");
  const parts = name.split("/");
  if (parts.some((part) => part === "" || part === "." || part === "..")) throw code("traversal_refused");
  return name;
}

export function extractPinnedArchive(archive, destination, members = PIN.members) {
  let raw;
  try {
    raw = gunzipSync(archive, { maxOutputLength: PIN.files.archive.uncompressedBytes });
  } catch {
    throw code("tampered_archive");
  }
  const expected = new Map(members.map((member) => [member.path, member]));
  const seen = new Set();
  let offset = 0;
  while (offset + 512 <= raw.length) {
    const header = raw.subarray(offset, offset + 512);
    offset += 512;
    if (header.every((byte) => byte === 0)) {
      if (!raw.subarray(offset).every((byte) => byte === 0)) throw code("tampered_archive");
      break;
    }
    if (headerChecksum(header) !== readOctal(header, 148, 8)) throw code("tampered_archive");
    const magic = header.subarray(257, 263);
    const gnu = header.subarray(257, 265).equals(Buffer.from("ustar  \0"));
    if (!magic.equals(Buffer.from("ustar\0")) && !gnu) throw code("tampered_archive");
    const typeflag = header[156];
    if (typeflag !== 48) throw code(typeflag === 50 || typeflag === 49 ? "link_refused" : "traversal_refused");
    if (cString(header.subarray(157, 257)) || cString(header.subarray(345, 500))) throw code("traversal_refused");
    const name = safeMember(cString(header.subarray(0, 100)));
    const size = readOctal(header, 124, 12);
    const mode = readOctal(header, 100, 8);
    if (mode !== 0o644) throw code("tampered_archive");
    const dataStart = offset;
    const dataEnd = offset + size;
    const blocks = Math.ceil(size / 512) * 512;
    offset += blocks;
    if (dataEnd > raw.length) throw code("truncated_archive");
    const spec = expected.get(name);
    const body = raw.subarray(dataStart, dataEnd);
    if (!spec || seen.has(name) || body.length !== spec.bytes || sha256(body) !== spec.sha256) throw code("tampered_archive");
    seen.add(name);
    const target = path.resolve(destination, name);
    const root = path.resolve(destination);
    if (target !== root && !target.startsWith(`${root}${path.sep}`)) throw code("traversal_refused");
    yieldMember(target, body);
  }
  if (seen.size !== expected.size || raw.length !== PIN.files.archive.uncompressedBytes) throw code("tampered_archive");
}

function yieldMember(target, body) {
  const handle = openSyncExclusive(target);
  try {
    handle.writeFileSync(body);
  } finally {
    handle.close();
  }
}

function openSyncExclusive(target) {
  mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });
  const fd = openSync(target, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o644);
  return {
    writeFileSync(body) { writeSync(fd, body); },
    close() { closeSync(fd); },
  };
}

export async function verifyCallerTree(caller) {
  let root;
  try {
    root = await realpath(caller);
  } catch (error) {
    if (error?.code === "ENOENT") throw code("missing_input");
    throw error;
  }
  for (const member of PIN.members) {
    const target = path.resolve(root, member.path);
    if (target !== root && !target.startsWith(`${root}${path.sep}`)) throw code("traversal_refused");
    let fd;
    try {
      fd = await open(target, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
    } catch (error) {
      if (error?.code === "ENOENT" || error?.code === "ENOTDIR") throw code("tampered_source");
      throw error;
    }
    try {
      const info = await fd.stat();
      if (!info.isFile() || info.size !== member.bytes) throw code("tampered_source");
      const body = await fd.readFile();
      if (sha256(body) !== member.sha256) throw code("tampered_source");
    } finally {
      await fd.close();
    }
  }
  const manifest = JSON.parse(await readFile(path.join(root, "package.json"), "utf8"));
  if (manifest.name !== PIN.package || manifest.version !== PIN.version || manifest.private !== true
    || manifest.dependencies?.["@modelcontextprotocol/sdk"] !== PIN.dependencies["@modelcontextprotocol/sdk"]
    || manifest.dependencies?.["@x402/mcp"] !== PIN.dependencies["@x402/mcp"]) {
    throw code("source_disagreement");
  }
  return root;
}

async function readCapped(file) {
  let fd;
  try {
    fd = await open(file, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  } catch (error) {
    if (error?.code === "ENOENT") throw code("missing_input");
    if (error?.code === "ELOOP") throw code("tampered_source");
    throw error;
  }
  try {
    const info = await fd.stat();
    if (!info.isFile() || info.size > MAX_INPUT_BYTES) throw code("input_rejected");
    return await fd.readFile();
  } finally {
    await fd.close();
  }
}

async function readCallerJson(file) {
  const bytes = await readCapped(file);
  try { return JSON.parse(bytes.toString("utf8")); }
  catch { throw code("input_rejected"); }
}

async function writeExclusive(file, body) {
  await mkdir(path.dirname(file), { recursive: true, mode: 0o700 });
  const fd = await open(file, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o644);
  try { await fd.writeFile(body); } finally { await fd.close(); }
}

function runBounded(command, args, options) {
  return new Promise((resolve) => {
    const child = spawn(command, args, { cwd: options.cwd, env: options.env, shell: false, stdio: ["ignore", "pipe", "pipe"] });
    let settled = false;
    const done = (result) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve(result);
    };
    const stop = (reason) => {
      child.kill("SIGKILL");
      done({ code: 2, reason });
    };
    const timer = setTimeout(() => stop("child_timeout"), options.timeoutMs);
    let used = 0;
    const count = (chunk) => {
      used += chunk.length;
      if (used > MAX_CHILD_OUTPUT) stop("child_output_bound");
    };
    child.stdout.on("data", count);
    child.stderr.on("data", count);
    child.on("error", () => done({ code: 2, reason: "child_spawn_failed" }));
    child.on("close", (status) => done({ code: status ?? 2, reason: null }));
  });
}

async function acquire(flags) {
  if (!flags.work) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Pass --work DIR for a new directory. This command does not extract a bundled example." }) };
  }
  const root = allowedPublicRoot(flags["public-root"]);
  const work = path.resolve(flags.work);
  try {
    await mkdir(work, { recursive: false, mode: 0o700 });
  } catch (error) {
    if (error?.code === "EEXIST") throw code("overwrite_refused");
    throw error;
  }
  const created = work;
  try {
    const real = await realpath(work);
    if (real !== work) throw code("traversal_refused");
    const downloads = {};
    const descriptorBytes = await getExact(pinnedRequest(root.origin, PIN.files.descriptor.path), PIN.files.descriptor.bytes + 1);
    const descriptor = classifyDescriptor(descriptorBytes);
    downloads.descriptor = descriptorBytes;
    for (const key of ["provenance", "license", "sourceNotice", "archive"]) {
      const spec = PIN.files[key];
      const cap = key === "archive" ? Math.max(spec.bytes, PIN.rejectedArchive.bytes) + 1 : spec.bytes + 1;
      downloads[key] = await getExact(pinnedRequest(root.origin, spec.path), cap);
    }
    classifyProvenance(downloads.provenance);
    classifyNamed(downloads.license, PIN.files.license, "license");
    classifyNamed(downloads.sourceNotice, PIN.files.sourceNotice, "source_notice");
    classifyArchive(downloads.archive);
    const received = path.join(real, "received");
    await mkdir(received, { mode: 0o700 });
    await writeExclusive(path.join(received, "descriptor.json"), downloads.descriptor);
    await writeExclusive(path.join(received, "provenance.json"), downloads.provenance);
    await writeExclusive(path.join(received, "LICENSE"), downloads.license);
    await writeExclusive(path.join(received, "SOURCE-NOTICE.txt"), downloads.sourceNotice);
    await writeExclusive(path.join(received, "samedaydesk-caller-result-0.1.1.tar.gz"), downloads.archive);
    const caller = path.join(real, "caller");
    await mkdir(caller, { mode: 0o700 });
    extractPinnedArchive(downloads.archive, caller);
    await verifyCallerTree(caller);
    let npmInstall = "not_requested";
    if (flags.install === "yes") {
      const npmHome = path.join(real, "npm-home");
      await mkdir(npmHome, { mode: 0o700 });
      const npm = path.join(path.dirname(process.execPath), "npm");
      const installed = await runBounded(npm, ["ci", "--ignore-scripts", "--no-audit", "--no-fund"], {
        cwd: caller,
        timeoutMs: NPM_TIMEOUT_MS,
        env: {
          PATH: path.dirname(process.execPath),
          HOME: npmHome,
          CI: "true",
          npm_config_registry: PIN.npmRegistry,
          LANG: "C",
          LC_ALL: "C",
        },
      });
      if (installed.code !== 0) {
        return { exit: 2, body: baseResult({ outcome: "install_failed", callerDir: caller, npmInstall: "failed", npmPublished: false, registryPackageClaim: false, packageNameInstalledFromRegistry: false, reason: installed.reason }) };
      }
      const sdk = JSON.parse(await readFile(path.join(caller, "node_modules/@modelcontextprotocol/sdk/package.json"), "utf8"));
      if (sdk.version !== PIN.dependencies["@modelcontextprotocol/sdk"]) throw code("source_disagreement");
      npmInstall = "completed";
    }
    return {
      exit: 0,
      body: baseResult({
        outcome: "acquired",
        version: PIN.version,
        archiveSha256: PIN.files.archive.sha256,
        bytes: PIN.files.archive.bytes,
        callerDir: caller,
        receiving: root.receiving,
        hostedAcceptance: false,
        npmPublished: false,
        registryPackageClaim: false,
        packageNameInstalledFromRegistry: false,
        npmInstall,
        dataRoute: PIN.dataRoute,
        optionalProjection: PIN.optionalProjection,
        projectionIsArchive: false,
        descriptorSource: descriptor.source ?? null,
        descriptorSourceFetched: false,
        memberCount: PIN.members.length,
      }),
    };
  } catch (error) {
    await rm(created, { recursive: true, force: true });
    throw error;
  }
}

async function retain(flags) {
  if (!flags.result || !flags.out) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Pass --result with the caller-owned CallToolResult JSON and --out with a new file. This command does not load a bundled example." }) };
  }
  const out = path.resolve(flags.out);
  let bytes;
  try {
    bytes = await readCapped(flags.result);
  } catch (error) {
    if (error?.code === "missing_input") {
      return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "The result file is absent. Pass the caller-owned CallToolResult JSON. This command does not load a bundled example." }) };
    }
    throw error;
  }
  const parsed = parseJson(bytes);
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw code("result_rejected");
  try {
    await writeExclusive(out, bytes);
  } catch (error) {
    if (error?.code === "EEXIST") throw code("overwrite_refused");
    throw error;
  }
  const written = await readFile(out);
  if (!written.equals(bytes)) throw code("tampered_source");
  return {
    exit: 0,
    body: baseResult({
      outcome: parsed.isError === true ? "tool_refusal" : "retained",
      out,
      bytes: bytes.length,
      sha256: sha256(bytes),
      isError: parsed.isError === true,
      retainedBytesMatch: true,
    }),
  };
}

async function loadInstalled(caller) {
  const root = await verifyCallerTree(caller);
  const sdkManifest = path.join(root, "node_modules/@modelcontextprotocol/sdk/package.json");
  let sdk;
  try { sdk = JSON.parse(await readFile(sdkManifest, "utf8")); } catch (error) {
    if (error?.code === "ENOENT") throw code("install_required");
    throw error;
  }
  if (sdk.version !== PIN.dependencies["@modelcontextprotocol/sdk"]) throw code("source_disagreement");
  const clientHref = pathToFileURL(path.join(root, "node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js")).href;
  const transportHref = pathToFileURL(path.join(root, "node_modules/@modelcontextprotocol/sdk/dist/esm/client/streamableHttp.js")).href;
  const recoveryHref = pathToFileURL(path.join(root, "src/mcp-recovery.mjs")).href;
  const mcpHref = pathToFileURL(path.join(root, "src/mcp-caller-result.mjs")).href;
  const httpHref = pathToFileURL(path.join(root, "src/http-caller-result.mjs")).href;
  const [clientMod, transportMod, recovery, mcp, http] = await Promise.all([
    import(clientHref), import(transportHref), import(recoveryHref), import(mcpHref), import(httpHref),
  ]);
  return { root, Client: clientMod.Client, Transport: transportMod.StreamableHTTPClientTransport, recovery, mcp, http };
}

function assertMcpEndpoint(value) {
  let url;
  try { url = new URL(value); } catch { throw code("endpoint_rejected"); }
  const loopback = url.protocol === "http:" && (url.hostname === "127.0.0.1" || url.hostname === "[::1]");
  if (url.username || url.password || url.search || url.hash || url.pathname !== "/mcp" || (url.protocol !== "https:" && !loopback)) {
    throw code("endpoint_rejected");
  }
  return url.href;
}

function recoveryOutcome(checkpoint, last) {
  const failure = checkpoint?.failure ?? null;
  if (typeof failure === "string" && failure.startsWith("grant_")) {
    return { outcome: "handle_rejected", exit: 3, failure };
  }
  if (checkpoint?.state === "pending") return { outcome: "recovery_pending", exit: 0, failure };
  if (checkpoint?.state === "completed" && checkpoint.result?.isError === true) return { outcome: "tool_refusal", exit: 0, failure: null };
  if (checkpoint?.state === "completed") return { outcome: "restored_result", exit: 0, failure: null };
  if (checkpoint?.state === "unresolved" && last?.isError === true) return { outcome: "recovery_pending", exit: 0, failure };
  if (checkpoint?.state === "unresolved" && failure === "transport_or_authority_failed") return { outcome: "transport_failure", exit: 0, failure };
  if (checkpoint?.state === "unresolved") return { outcome: "unresolved", exit: 0, failure };
  return { outcome: "transport_failure", exit: 0, failure };
}

async function recover(flags) {
  if (!flags.caller || !flags.checkpoint || !flags.grant || !flags.action) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Pass --caller, --action start or resume, --checkpoint, and --grant. Start also needs --operation. This command does not invent a purchase or load an example." }) };
  }
  if (!["start", "resume"].includes(flags.action)) throw code("flag_rejected");
  if (flags.action === "start" && !flags.operation) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Pass --operation with the caller-owned operation file. This command does not create a payment." }) };
  }
  let installed;
  try { installed = await loadInstalled(flags.caller); } catch (error) {
    if (error?.code === "install_required") {
      return { exit: 0, body: baseResult({ outcome: "install_required", nextAction: "Run acquire --install yes for this caller directory before recovery." }) };
    }
    if (error?.code === "missing_input") {
      return { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Pass --caller with the directory acquire wrote. This command does not create a caller or load an example." }) };
    }
    throw error;
  }
  const names = [];
  let last = null;
  let sdk;
  const endpointFor = async () => {
    if (flags.action === "start") {
      const input = await readCallerJson(flags.operation);
      return assertMcpEndpoint(input.endpointUrl);
    }
    const stored = await readCallerJson(flags.checkpoint);
    return assertMcpEndpoint(stored?.input?.endpointUrl);
  };
  const client = {
    async listTools(...args) {
      const endpoint = await endpointFor();
      sdk ??= new installed.Client({ name: "samedaydesk-task-result", version: "0.1.0" });
      if (!client.connected) client.connected = sdk.connect(new installed.Transport(new URL(endpoint)));
      await client.connected;
      return sdk.listTools(...args);
    },
    async callTool(...args) {
      names.push(args[0]?.name ?? null);
      const result = await sdk.callTool(...args);
      last = result;
      return result;
    },
    getToolOutputValidator: (...args) => sdk.getToolOutputValidator(...args),
    close: () => sdk?.close() ?? Promise.resolve(),
  };
  try {
    const loadGrant = async () => await readCallerJson(flags.grant);
    const store = installed.recovery.mcpRecoveryFileStore(path.resolve(flags.checkpoint));
    const handle = flags.action === "start"
      ? await installed.recovery.startPaidMcpResult({ client, store, input: await readCallerJson(flags.operation), loadGrant })
      : await installed.recovery.resumePaidMcpResult({ client, store, loadGrant });
    const checkpoint = await handle.handoff();
    const classified = recoveryOutcome(checkpoint, last);
    const budget = checkpoint?.state ? installed.recovery.mcpRecoveryBudget(checkpoint) : null;
    return {
      exit: classified.exit,
      body: baseResult({
        outcome: classified.outcome,
        state: checkpoint.state,
        failure: classified.failure,
        newPaymentPermitted: budget ? budget.newPaymentPermitted : false,
        budgetUsefulness: budget ? budget.usefulness : "unknown",
        toolCalls: names,
        retainedResult: checkpoint.result ?? null,
      }),
    };
  } finally {
    await client.close().catch(() => {});
  }
}

function statementView(body) {
  if (!body || typeof body !== "object") return null;
  return {
    ok: body.ok === true,
    accepted: body.accepted === true,
    bound: body.bound === true,
    charged: false,
    usefulness: "unknown",
    code: typeof body.code === "string" ? body.code : null,
    disposition: body.disposition === "useful" || body.disposition === "not_useful" ? body.disposition : null,
    reasonCategory: typeof body.reasonCategory === "string" || body.reasonCategory === null ? body.reasonCategory ?? null : null,
  };
}

async function feedback(flags) {
  if (!flags.channel) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "Pass --channel mcp or --channel http, plus the caller-owned result and disposition." }) };
  }
  if (flags.channel === "http" && flags.send !== "yes") {
    return { exit: 0, body: baseResult({ outcome: "feedback_not_sent", connected: false, posted: false, nextAction: "Pass --send yes to post one optional statement through the acquired https client. The default does not post." }) };
  }
  if (!flags.caller || !flags.disposition) {
    return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "Pass --caller and --disposition useful or not_useful. A missing disposition does not connect." }) };
  }
  if (flags.channel === "http") {
    if (!flags.purchase || !flags.resource || !flags["header-file"]) {
      return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "Pass --purchase, --resource, and --header-file. The default HTTP path does not post." }) };
    }
    const root = await verifyCallerTree(flags.caller);
    const http = await import(pathToFileURL(path.join(root, "src/http-caller-result.mjs")).href);
    const purchase = await readCallerJson(flags.purchase);
    const headers = await readCallerJson(flags["header-file"]);
    http.bindCallerResultFeedback(purchase, { response: { headers: new Headers(headers) }, resourceUrl: flags.resource });
    const statement = { disposition: flags.disposition };
    if (flags.reason !== undefined) statement.reasonCategory = flags.reason;
    const reported = await http.reportCallerResult(purchase, statement);
    const view = statementView(reported);
    const outcome = view?.code === "untrusted_origin" ? "untrusted_origin" : view?.accepted === true ? "caller_asserted_acceptance" : (view?.code || "transport_failure");
    const posted = ["transport_failed", "redirect_refused", "malformed_response", "transport_timeout", "response_too_large", "header_too_large"].includes(view?.code) || outcome === "caller_asserted_acceptance";
    return { exit: 0, body: baseResult({ outcome, connected: false, posted, accepted: outcome === "caller_asserted_acceptance", charged: false, statement: view }) };
  }
  let installed;
  try { installed = await loadInstalled(flags.caller); } catch (error) {
    if (error?.code === "install_required") {
      return { exit: 0, body: baseResult({ outcome: "install_required", connected: false, posted: false, nextAction: "Run acquire --install yes for this caller directory before feedback." }) };
    }
    if (error?.code === "missing_input") {
      return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "Pass --caller with the directory acquire wrote. This command does not create a caller or load an example." }) };
    }
    throw error;
  }
  if (flags.channel === "mcp") {
    if (!flags.endpoint || !flags.result) {
      return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "Pass --endpoint and --result. A missing token or result does not connect." }) };
    }
    const result = await readCallerJson(flags.result);
    const capability = installed.mcp.readMcpCallerResultCapability(result);
    if (capability.present !== true) {
      return { exit: 0, body: baseResult({ outcome: "missing_input", connected: false, posted: false, nextAction: "The result has no caller feedback token. Supply the retained result that carries one. This command does not invent a token." }) };
    }
    const endpoint = assertMcpEndpoint(flags.endpoint);
    let sdk;
    let raw = null;
    const client = {
      async callTool(params) {
        sdk ??= new installed.Client({ name: "samedaydesk-task-result", version: "0.1.0" });
        if (!client.connected) client.connected = sdk.connect(new installed.Transport(new URL(endpoint)));
        await client.connected;
        raw = await sdk.callTool(params);
        return raw;
      },
      close: () => sdk?.close() ?? Promise.resolve(),
    };
    try {
      const input = { token: capability.token, disposition: flags.disposition };
      if (flags.reason !== undefined) input.reasonCategory = flags.reason;
      const statement = await installed.mcp.reportMcpCallerResult(client, input);
      const view = statementView(statement);
      let outcome = "transport_failure";
      if (raw?.isError === true) outcome = "tool_refusal";
      else if (view?.accepted === true) outcome = "caller_asserted_acceptance";
      else if (view?.code === "transport_failed") outcome = "transport_failure";
      else outcome = view?.code || "transport_failure";
      const encoded = JSON.stringify(raw ?? {});
      const tokenEcho = encoded.includes(capability.token);
      return {
        exit: 0,
        body: baseResult({
          outcome,
          connected: true,
          posted: false,
          mcpCalled: true,
          accepted: outcome === "caller_asserted_acceptance",
          isError: raw?.isError === true,
          charged: false,
          statement: view,
          retainedResult: tokenEcho ? null : raw,
          tokenEcho,
        }),
      };
    } finally {
      await client.close().catch(() => {});
    }
  }
  throw code("flag_rejected");
}

function mapError(error) {
  const name = typeof error?.code === "string" ? error.code : "failed";
  if (name === "missing_input" || name === "install_required") {
    return { exit: 0, body: baseResult({ outcome: name, nextAction: "Supply the caller-owned file named by the command." }) };
  }
  if (typeof name === "string" && (name.startsWith("grant_") || name === "grant_revoked_or_missing")) {
    return { exit: 3, body: baseResult({ outcome: "handle_rejected", failure: name, toolCalls: [], newPaymentPermitted: false }) };
  }
  if (name === "EEXIST" || name === "overwrite_refused") return { exit: 2, body: baseResult({ outcome: "overwrite_refused" }) };
  if (AUTHORITY_CODES.has(name) || ["redirect_refused", "cross_origin_refused", "public_root_rejected", "tampered_archive", "tampered_descriptor", "tampered_provenance", "tampered_license", "tampered_source_notice", "tampered_source", "truncated_archive", "source_disagreement", "traversal_refused", "link_refused", "body_too_large", "result_rejected", "input_rejected", "flag_rejected", "fetch_failed"].includes(name)) {
    return { exit: 2, body: baseResult({ outcome: name }) };
  }
  return { exit: 0, body: baseResult({ outcome: "transport_failure", failure: "unexpected_failure" }) };
}

async function main() {
  let parsed;
  try { parsed = parseArgs(process.argv.slice(2)); } catch (error) {
    const mapped = mapError(error);
    finish(mapped.exit, mapped.body);
    return;
  }
  if (parsed.flags.pay || parsed.flags.settle || parsed.flags.sign || parsed.flags.wallet) {
    finish(2, baseResult({ outcome: "payment_refused", nextAction: "Payment, signing, and wallet access stay outside this skill." }));
    return;
  }
  try {
    const command = parsed.command;
    const result = command === "acquire" ? await acquire(parsed.flags)
      : command === "retain" ? await retain(parsed.flags)
        : command === "recover" ? await recover(parsed.flags)
          : command === "feedback" ? await feedback(parsed.flags)
            : { exit: 0, body: baseResult({ outcome: "missing_input", nextAction: "Run acquire, retain, recover, or feedback. A missing command does not run a bundled example." }) };
    finish(result.exit, result.body);
  } catch (error) {
    const mapped = mapError(error);
    finish(mapped.exit, mapped.body);
  }
}

const entry = process.argv[1] ? pathToFileURL(path.resolve(process.argv[1])).href : "";
if (import.meta.url === entry) await main();
