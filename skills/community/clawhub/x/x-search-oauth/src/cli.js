import { mkdirSync, readFileSync, writeFileSync, chmodSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { homedir } from "node:os";

const DEFAULT_TIMEOUT_MS = 45000;
const DEFAULT_MODEL = "grok-4-1-fast-non-reasoning";
const CLIENT_ID = "b1a00492-073a-47ea-816f-4c329264a828";
const SCOPE = "openid profile email offline_access grok-cli:access api:access";
const DISCOVERY_URL = "https://auth.x.ai/.well-known/openid-configuration";
const RESPONSES_ENDPOINT = "https://api.x.ai/v1/responses";
const DEVICE_GRANT = "urn:ietf:params:oauth:grant-type:device_code";
const USER_AGENT = "x-search-oauth/0.2.5";

export async function main(argv, io = {}) {
  const stdout = io.stdout ?? process.stdout;
  const stderr = io.stderr ?? process.stderr;
  const fetchImpl = io.fetchImpl ?? fetch;
  const env = io.env ?? process.env;
  const sleep = io.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  const now = io.now ?? (() => Date.now());
  const configPath = io.configPath ?? resolveConfigPath(env);

  const parsed = parseArgs(argv);
  if (parsed.command === "help") return stdout.write(helpText());
  if (parsed.command === "auth") {
    const credential = await loginDeviceCode({ fetchImpl, stdout, stderr, sleep, now, configPath, timeoutMs: parsed.timeoutMs });
    stdout.write(`\nAuthenticated as ${credential.email ?? credential.accountId ?? "xAI account"}.\n`);
    return;
  }
  if (parsed.command === "logout") {
    writeAuthConfig(configPath, {});
    stdout.write(`Removed ${configPath}\n`);
    return;
  }
  if (parsed.command === "doctor") {
    const auth = readAuthConfig(configPath);
    stdout.write(`config: ${configPath}\n`);
    stdout.write(`auth: ${auth.accessToken ? "present" : "missing"}\n`);
    if (auth.expires) stdout.write(`expires: ${new Date(auth.expires).toISOString()}\n`);
    return;
  }
  if (parsed.command === "search") {
    try {
      const result = await runSearch({ options: parsed, fetchImpl, now, configPath });
      stdout.write(formatSearchResult(result, parsed));
    } catch (error) {
      stderr.write(`x_search failed: ${formatError(error)}\n`);
      process.exitCode = 1;
    }
    return;
  }
  throw new Error(`unknown command: ${parsed.command}`);
}

export function parseArgs(argv) {
  const args = [...argv];
  if (args.length === 0) return { command: "help" };
  if (args[0] === "--help" || args[0] === "-h") return { command: "help" };

  const knownCommands = new Set(["auth", "doctor", "logout", "search"]);
  let command = "search";
  if (args[0] && !args[0].startsWith("-") && (knownCommands.has(args[0]) || args[0] === "help")) {
    command = args.shift();
  }
  if (command === "help") return { command: "help" };

  const parsed = parseOptions(command, args);
  if (command === "search" && !parsed.query) throw new Error("search requires --query <text> or a positional query");
  return parsed;
}

function parseOptions(command, args) {
  const parsed = {
    command,
    query: "",
    allowedXHandles: [],
    excludedXHandles: [],
    fromDate: "",
    toDate: "",
    json: false,
    raw: false,
    enableImageUnderstanding: false,
    enableVideoUnderstanding: false,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    model: DEFAULT_MODEL,
    maxTurns: 0
  };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    const next = () => {
      i += 1;
      if (i >= args.length) throw new Error(`${arg} requires a value`);
      return args[i];
    };
    if (arg === "--query" || arg === "-q") parsed.query = next();
    else if (arg === "--from-date") parsed.fromDate = next();
    else if (arg === "--to-date") parsed.toDate = next();
    else if (arg === "--handle" || arg === "--allowed-handle") parsed.allowedXHandles.push(...splitCsv(next()));
    else if (arg === "--exclude-handle") parsed.excludedXHandles.push(...splitCsv(next()));
    else if (arg === "--image") parsed.enableImageUnderstanding = true;
    else if (arg === "--video") parsed.enableVideoUnderstanding = true;
    else if (arg === "--json") parsed.json = true;
    else if (arg === "--raw") parsed.raw = true;
    else if (arg === "--timeout") parsed.timeoutMs = parseTimeout(next());
    else if (arg === "--model") parsed.model = next();
    else if (arg === "--max-turns") parsed.maxTurns = parsePositiveInt(next(), "--max-turns");
    else if (arg === "--help" || arg === "-h") return { command: "help" };
    else if (!arg.startsWith("-") && command === "search" && !parsed.query) parsed.query = arg;
    else throw new Error(`unknown option: ${arg}`);
  }
  return parsed;
}

function splitCsv(value) {
  return value.split(",").map((entry) => entry.trim().replace(/^@/, "")).filter(Boolean);
}

function parseTimeout(value) {
  const seconds = Number(value);
  if (!Number.isFinite(seconds) || seconds <= 0) throw new Error("--timeout must be a positive number of seconds");
  return Math.round(seconds * 1000);
}

function parsePositiveInt(value, label) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) throw new Error(`${label} must be a positive integer`);
  return parsed;
}

function resolveConfigPath(env) {
  const base = env.X_SEARCH_OAUTH_CONFIG_HOME || env.XDG_CONFIG_HOME || join(homedir(), ".config");
  return join(base, "x-search-oauth", "auth.json");
}

function readAuthConfig(configPath) {
  if (!existsSync(configPath)) return {};
  return JSON.parse(readFileSync(configPath, "utf8"));
}

function writeAuthConfig(configPath, payload) {
  mkdirSync(dirname(configPath), { recursive: true, mode: 0o700 });
  writeFileSync(configPath, JSON.stringify(payload, null, 2), { mode: 0o600 });
  chmodSync(configPath, 0o600);
}

async function readJsonResponse(response, label) {
  let body = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  if (!response.ok) {
    const message = body?.error_description || body?.error || response.statusText || "request failed";
    throw new Error(`${label} failed (${response.status}): ${message}`);
  }
  return body;
}

function requireTrustedXaiUrl(value, label) {
  const url = new URL(value);
  if (url.username || url.password || url.port || url.protocol !== "https:" || (url.hostname !== "x.ai" && !url.hostname.endsWith(".x.ai"))) {
    throw new Error(`xAI discovery returned untrusted ${label}`);
  }
  return value;
}

async function fetchDiscovery(fetchImpl) {
  const body = await readJsonResponse(await fetchImpl(DISCOVERY_URL, {
    redirect: "error",
    headers: { Accept: "application/json", "User-Agent": USER_AGENT }
  }), "xAI OAuth discovery");
  return {
    deviceAuthorizationEndpoint: requireTrustedXaiUrl(body.device_authorization_endpoint, "device authorization endpoint"),
    tokenEndpoint: requireTrustedXaiUrl(body.token_endpoint, "token endpoint")
  };
}

async function requestDeviceCode(fetchImpl, discovery) {
  const body = await readJsonResponse(await fetchImpl(discovery.deviceAuthorizationEndpoint, {
    redirect: "error",
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json", "User-Agent": USER_AGENT },
    body: new URLSearchParams({ client_id: CLIENT_ID, scope: SCOPE })
  }), "xAI device code request");
  if (!body.device_code || !body.user_code || !body.verification_uri) throw new Error("xAI device code response is malformed");
  return {
    deviceCode: body.device_code,
    userCode: body.user_code,
    verificationUri: requireTrustedXaiUrl(body.verification_uri, "verification URI"),
    verificationUriComplete: body.verification_uri_complete ? requireTrustedXaiUrl(body.verification_uri_complete, "complete verification URI") : "",
    expiresInMs: Math.max(1, Number(body.expires_in) || 300) * 1000,
    intervalMs: Math.max(1, Number(body.interval) || 5) * 1000
  };
}

async function pollDeviceCodeToken({ fetchImpl, tokenEndpoint, deviceCode, expiresInMs, intervalMs, sleep, now }) {
  const deadline = now() + expiresInMs;
  let delay = intervalMs;
  while (now() < deadline) {
    const response = await fetchImpl(tokenEndpoint, {
    redirect: "error",
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json", "User-Agent": USER_AGENT },
      body: new URLSearchParams({ grant_type: DEVICE_GRANT, client_id: CLIENT_ID, device_code: deviceCode })
    });
    let body = null;
    try { body = await response.json(); } catch { body = null; }
    if (response.ok) return parseTokenResponse(body, now);
    const error = body?.error;
    if (error === "authorization_pending") {
      await sleep(Math.min(delay, Math.max(0, deadline - now())));
      continue;
    }
    if (error === "slow_down") {
      delay += 5000;
      await sleep(Math.min(delay, Math.max(0, deadline - now())));
      continue;
    }
    if (error === "access_denied" || error === "authorization_denied") throw new Error("xAI device authorization was denied");
    if (error === "expired_token") throw new Error("xAI device code expired; run auth again");
    throw new Error(`xAI device token exchange failed (${response.status}): ${body?.error_description || error || response.statusText}`);
  }
  throw new Error("xAI device authorization timed out");
}

function parseTokenResponse(body, now) {
  if (!body?.access_token) throw new Error("xAI token response is missing access_token");
  if (!body?.refresh_token) throw new Error("xAI token response is missing refresh_token");
  return {
    accessToken: body.access_token,
    refreshToken: body.refresh_token,
    idToken: body.id_token || "",
    expires: body.expires_in ? now() + Number(body.expires_in) * 1000 : 0,
    tokenEndpoint: ""
  };
}

function jwtPayload(token) {
  const part = token?.split?.(".")?.[1];
  if (!part) return {};
  try { return JSON.parse(Buffer.from(part, "base64url").toString("utf8")); } catch { return {}; }
}

function credentialIdentity(tokens) {
  const payload = jwtPayload(tokens.idToken || tokens.accessToken);
  return {
    email: typeof payload.email === "string" ? payload.email : "",
    accountId: typeof payload.sub === "string" ? payload.sub : "",
    displayName: typeof payload.name === "string" ? payload.name : ""
  };
}

export async function loginDeviceCode({ fetchImpl, stdout, sleep, now, configPath }) {
  const discovery = await fetchDiscovery(fetchImpl);
  const device = await requestDeviceCode(fetchImpl, discovery);
  stdout.write(`Open this URL:\n${device.verificationUriComplete || device.verificationUri}\n\nCode: ${device.userCode}\n\nWaiting for approval...\n`);
  const tokens = await pollDeviceCodeToken({ fetchImpl, tokenEndpoint: discovery.tokenEndpoint, deviceCode: device.deviceCode, expiresInMs: device.expiresInMs, intervalMs: device.intervalMs, sleep, now });
  const identity = credentialIdentity(tokens);
  const credential = { ...tokens, tokenEndpoint: discovery.tokenEndpoint, ...identity };
  writeAuthConfig(configPath, credential);
  return credential;
}

async function refreshCredential({ credential, fetchImpl, now, configPath }) {
  if (!credential.refreshToken) throw new Error("not authenticated; run `xso auth`");
  const tokenEndpoint = requireTrustedXaiUrl(credential.tokenEndpoint || (await fetchDiscovery(fetchImpl)).tokenEndpoint, "stored token endpoint");
  const body = await readJsonResponse(await fetchImpl(tokenEndpoint, {
    redirect: "error",
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json", "User-Agent": USER_AGENT },
    body: new URLSearchParams({ grant_type: "refresh_token", client_id: CLIENT_ID, refresh_token: credential.refreshToken })
  }), "xAI OAuth refresh");
  const tokens = parseTokenResponse({ ...body, refresh_token: body.refresh_token || credential.refreshToken }, now);
  const next = { ...credential, ...tokens, tokenEndpoint };
  writeAuthConfig(configPath, next);
  return next;
}

async function loadUsableCredential({ fetchImpl, now, configPath }) {
  const credential = readAuthConfig(configPath);
  if (!credential.accessToken) throw new Error("not authenticated; run `xso auth` first");
  if (!credential.expires || credential.expires - now() > 60000) return credential;
  return refreshCredential({ credential, fetchImpl, now, configPath });
}

function buildXSearchTool(options) {
  return {
    type: "x_search",
    ...(options.allowedXHandles.length ? { allowed_x_handles: options.allowedXHandles } : {}),
    ...(options.excludedXHandles.length ? { excluded_x_handles: options.excludedXHandles } : {}),
    ...(options.fromDate ? { from_date: options.fromDate } : {}),
    ...(options.toDate ? { to_date: options.toDate } : {}),
    ...(options.enableImageUnderstanding ? { enable_image_understanding: true } : {}),
    ...(options.enableVideoUnderstanding ? { enable_video_understanding: true } : {})
  };
}

function extractCitations(annotations) {
  if (!Array.isArray(annotations)) return [];
  return annotations.filter((entry) => entry?.type === "url_citation" && typeof entry.url === "string").map((entry) => entry.url);
}

function parseResponsesResult(data) {
  for (const output of data.output || []) {
    if (output?.type !== "message") continue;
    for (const block of output.content || []) {
      if (block?.type === "output_text" && block.text) {
        return { content: block.text, citations: Array.from(new Set([...(data.citations || []), ...extractCitations(block.annotations)])) };
      }
    }
  }
  if (typeof data.output_text === "string") return { content: data.output_text, citations: data.citations || [] };
  throw new Error("xAI X search returned malformed response JSON");
}

export async function runSearch({ options, fetchImpl, now, configPath }) {
  const credential = await loadUsableCredential({ fetchImpl, now, configPath });
  const started = now();
  const body = {
    model: options.model,
    input: [{ role: "user", content: options.query }],
    tools: [buildXSearchTool(options)],
    ...(options.maxTurns ? { max_turns: options.maxTurns } : {})
  };
  const data = await readJsonResponse(await fetchImpl(RESPONSES_ENDPOINT, {
    redirect: "error",
    method: "POST",
    headers: { Authorization: `Bearer ${credential.accessToken}`, "Content-Type": "application/json", Accept: "application/json", "User-Agent": USER_AGENT },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(options.timeoutMs)
  }), "xAI X search");
  const parsed = parseResponsesResult(data);
  return {
    query: options.query,
    provider: "xai",
    model: options.model,
    tookMs: now() - started,
    ...parsed
  };
}

export function formatSearchResult(payload, options) {
  if (options.raw || options.json) return `${JSON.stringify(payload, null, 2)}\n`;
  const citations = Array.isArray(payload.citations) ? payload.citations : [];
  const lines = [`# query: ${payload.query} | model: ${payload.model} | took: ${payload.tookMs}ms`, String(payload.content || "").trim()];
  if (citations.length) {
    lines.push("", "Citations:");
    citations.forEach((citation, index) => lines.push(`${index + 1}. ${citation}`));
  }
  return `${lines.join("\n").trim()}\n`;
}

function formatError(error) {
  return error instanceof Error ? error.message : String(error);
}

export function helpText() {
  return `x-search-oauth - headless xAI OAuth X/Twitter search\n\nUsage:\n  x-search-oauth auth\n  x-search-oauth search --query "AI agents" [options]\n  xso auth\n  xso "OpenClaw xAI" --from-date 2026-05-20 --json\n  xso logout\n\nCommands:\n  auth                    Sign in with xAI device-code OAuth\n  search                  Search X using xAI x_search\n  doctor                  Show local auth file status\n  logout                  Remove local stored tokens\n\nSearch options:\n  -q, --query <text>          X search query\n      --handle <handle>       Restrict to handle; repeat or comma-separate\n      --exclude-handle <h>    Exclude handle; repeat or comma-separate\n      --from-date YYYY-MM-DD  Start date\n      --to-date YYYY-MM-DD    End date\n      --image                 Enable image understanding\n      --video                 Enable video understanding\n      --json                  Print normalized JSON payload\n      --raw                   Same as --json for this version\n      --timeout <seconds>     xAI request timeout, default 45\n      --model <model>         xAI model, default ${DEFAULT_MODEL}\n      --max-turns <n>         Optional xAI Responses max_turns\n\nTokens are stored at ~/.config/x-search-oauth/auth.json with file mode 0600.\n`;
}
