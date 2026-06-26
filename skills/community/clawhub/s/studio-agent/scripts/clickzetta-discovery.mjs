import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { env as hostEnv } from "node:process";
import { atomicWriteJsonSync } from "./utils.mjs";

const DEFAULT_API_GATEWAY = "https://dev-api.clickzetta.com";
const DEFAULT_LANGUAGE = "zh_CN";
const DEFAULT_ENV = "prod";
const CACHE_VERSION = 2;
const WORKSPACE_SELECTION_VERSION = 1;
const CACHE_TTL_SKEW_MS = 5 * 60 * 1000;
const WORKSPACE_LIST_TTL_MS = 5 * 60 * 1000;

function isRecord(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function asString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  const text = String(value).trim();
  return text ? text : undefined;
}

function toScalarString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  if (typeof value === "bigint") {
    return value.toString();
  }
  if (typeof value === "number") {
    return Number.isFinite(value) ? String(value) : undefined;
  }
  return asString(value);
}

function toRequestNumber(value, fieldName) {
  const text = asString(value);
  if (!text) {
    throw new Error(`Missing request field: ${fieldName}`);
  }
  const numeric = Number(text);
  if (!Number.isFinite(numeric)) {
    throw new Error(`Invalid numeric request field: ${fieldName}`);
  }
  return numeric;
}

function normalizeComparableText(value) {
  const text = asString(value);
  return text ? text.toLowerCase().replace(/\s+/g, " ") : undefined;
}

function replaceApiHostSuffix(hostname) {
  if (hostname.startsWith("dev-api.")) {
    return hostname.replace(/^dev-api\./, "dev-app.");
  }
  if (hostname.startsWith("api.")) {
    return hostname.replace(/^api\./, "app.");
  }
  if (hostname.includes(".dev-api.")) {
    return hostname.replace(".dev-api.", ".dev-app.");
  }
  if (hostname.includes(".api.")) {
    return hostname.replace(".api.", ".app.");
  }
  if (hostname.includes("-api.")) {
    return hostname.replace("-api.", "-app.");
  }
  return hostname;
}

function parseClickZettaJdbcUrl(rawJdbcUrl) {
  const jdbcUrl = asString(rawJdbcUrl);
  if (!jdbcUrl) {
    return undefined;
  }
  const prefix = "jdbc:clickzetta://";
  if (!jdbcUrl.toLowerCase().startsWith(prefix)) {
    throw new Error("CZ_STUDIO_JDBC_URL must start with jdbc:clickzetta://");
  }

  let parsed;
  try {
    parsed = new URL(`https://${jdbcUrl.slice(prefix.length)}`);
  } catch {
    throw new Error("CZ_STUDIO_JDBC_URL is not a valid JDBC URL");
  }

  const hostname = asString(parsed.hostname);
  if (!hostname) {
    throw new Error("CZ_STUDIO_JDBC_URL is missing a hostname");
  }

  const hostParts = hostname.split(".");
  if (hostParts.length < 2) {
    throw new Error("CZ_STUDIO_JDBC_URL hostname must include an instance prefix");
  }

  const instanceName = asString(hostParts[0]);
  const apiHost = hostParts.slice(1).join(".");
  if (!instanceName || !apiHost) {
    throw new Error("CZ_STUDIO_JDBC_URL must include both instance name and api host");
  }

  const portSuffix = parsed.port ? `:${parsed.port}` : "";
  const username = asString(parsed.searchParams.get("username"));
  const password = asString(parsed.searchParams.get("password"));
  if (!username || !password) {
    throw new Error("CZ_STUDIO_JDBC_URL must include username and password query params");
  }

  return {
    jdbcUrl,
    domain: `${instanceName}.${replaceApiHostSuffix(apiHost)}${portSuffix}`,
    apiGateway: `https://${apiHost}${portSuffix}`,
    instanceName,
    username,
    password,
    workspace: asString(parsed.pathname.replace(/^\/+/, "")),
  };
}

function normalizeStudioOrigin(rawDomain) {
  const text = asString(rawDomain);
  if (!text) {
    return undefined;
  }
  const withScheme = /^[A-Za-z][A-Za-z0-9+.-]*:\/\//.test(text) ? text : `https://${text}`;
  const url = new URL(withScheme);
  url.username = "";
  url.password = "";
  url.hash = "";
  url.search = "";
  url.pathname = "/";
  return url.origin;
}

function deriveInstanceName(studioOrigin) {
  const url = new URL(studioOrigin);
  const [instanceName] = url.hostname.split(".");
  return asString(instanceName);
}

function resolveApiGateway(studioOrigin, explicitApiGateway) {
  const explicit = asString(explicitApiGateway);
  if (explicit) {
    return explicit.replace(/\/+$/, "");
  }

  const hostname = new URL(studioOrigin).hostname.toLowerCase();
  if (hostname.endsWith(".app.clickzetta.com")) {
    return "https://api.clickzetta.com";
  }
  return DEFAULT_API_GATEWAY;
}

function buildCommonHeaders(studioOrigin, instanceName, instanceId, token, extraHeaders = {}) {
  const headers = {
    accept: "application/json, text/plain, */*",
    "content-type": "application/json",
    "cz-lang": DEFAULT_LANGUAGE,
    origin: studioOrigin,
    referer: `${studioOrigin}/`,
    ...extraHeaders,
  };

  const normalizedInstanceName = asString(instanceName);
  const normalizedInstanceId = asString(instanceId);
  const normalizedToken = asString(token);

  if (normalizedInstanceName) {
    headers.instancename = normalizedInstanceName;
  }
  if (normalizedInstanceId) {
    headers.instanceid = normalizedInstanceId;
  }
  if (normalizedToken) {
    headers["x-clickzetta-token"] = normalizedToken;
  }
  return headers;
}

function parseJwtClaims(rawToken) {
  const token = asString(rawToken);
  if (!token) {
    return undefined;
  }
  const parts = token.split(".");
  if (parts.length < 2) {
    return undefined;
  }
  try {
    const payload = Buffer.from(parts[1], "base64url").toString("utf8");
    const parsed = JSON.parse(payload);
    return isRecord(parsed) ? parsed : undefined;
  } catch {
    return undefined;
  }
}

function getTokenExpiryMs(rawToken) {
  const claims = parseJwtClaims(rawToken);
  const exp = claims?.exp;
  if (typeof exp === "number" && Number.isFinite(exp)) {
    return exp * 1000;
  }
  if (typeof exp === "string") {
    const numeric = Number(exp);
    if (Number.isFinite(numeric)) {
      return numeric * 1000;
    }
  }
  return undefined;
}

function extractTokenFromWsUrl(rawUrl) {
  const text = asString(rawUrl);
  if (!text) {
    return undefined;
  }
  try {
    const url = new URL(text);
    return asString(url.searchParams.get("x-clickzetta-token"));
  } catch {
    return undefined;
  }
}

async function fetchJson(url, init, label) {
  const response = await fetch(url, init);
  const text = await response.text();

  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error(`${label} returned invalid JSON (${response.status})`);
  }

  if (!response.ok) {
    const message =
      asString(parsed?.message) ??
      asString(parsed?.msg) ??
      asString(parsed?.data) ??
      response.statusText;
    throw new Error(`${label} failed (${response.status}): ${message}`);
  }

  return parsed;
}

function unwrapApiData(payload, label) {
  if (!isRecord(payload)) {
    throw new Error(`${label} returned an unexpected payload`);
  }

  const code = payload.code;
  const success = code === 0 || code === "0" || code === 200 || code === "200";
  if (!success) {
    const message =
      asString(payload.message) ??
      asString(payload.msg) ??
      asString(payload.data) ??
      "unknown error";
    throw new Error(`${label} failed (${String(code)}): ${message}`);
  }

  return payload.data;
}

async function loginSingle({ apiGateway, username, password, instanceName }) {
  const payload = await fetchJson(
    `${apiGateway}/clickzetta-portal/user/loginSingle`,
    {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        instanceName,
      }),
    },
    "loginSingle",
  );

  const data = unwrapApiData(payload, "loginSingle");
  if (!isRecord(data)) {
    throw new Error("loginSingle returned an empty payload");
  }

  const token = asString(data.token);
  const instanceId = toScalarString(data.instanceId);
  const userId = toScalarString(data.userId);
  const expireTime =
    typeof data.expireTime === "number" && Number.isFinite(data.expireTime) ? data.expireTime : undefined;

  if (!token) {
    throw new Error("loginSingle returned no token");
  }
  if (!instanceId) {
    throw new Error("loginSingle returned no instanceId");
  }

  return { token, instanceId, userId, expireTime };
}

async function getCurrentUser({ apiGateway, studioOrigin, instanceName, instanceId, token }) {
  const payload = await fetchJson(
    `${apiGateway}/clickzetta-portal/user/getCurrentUser`,
    {
      method: "POST",
      headers: buildCommonHeaders(studioOrigin, instanceName, instanceId, token),
      body: "null",
    },
    "getCurrentUser",
  );

  const data = unwrapApiData(payload, "getCurrentUser");
  if (!isRecord(data)) {
    throw new Error("getCurrentUser returned an empty payload");
  }

  const userId = toScalarString(data.id) ?? toScalarString(data.userId);
  const tenantId = toScalarString(data.accountId) ?? toScalarString(data.tenantId);

  if (!userId) {
    throw new Error("getCurrentUser returned no user id");
  }
  if (!tenantId) {
    throw new Error("getCurrentUser returned no tenant id");
  }

  return {
    userId,
    tenantId,
    username: asString(data.name) ?? asString(data.displayName),
    accountDisplayName: asString(data.accountDisplayName),
  };
}

async function listUserWorkspaces({
  apiGateway,
  studioOrigin,
  instanceName,
  instanceId,
  token,
  userId,
  tenantId,
}) {
  const payload = await fetchJson(
    `${apiGateway}/ide-authority/v1/workspace/listUserWorkspaces`,
    {
      method: "POST",
      headers: buildCommonHeaders(studioOrigin, instanceName, instanceId, token, {
        env: DEFAULT_ENV,
      }),
      body: JSON.stringify({
        userId: toRequestNumber(userId, "userId"),
        tenantId: toRequestNumber(tenantId, "tenantId"),
        pageIndex: 1,
        pageSize: 99999,
        forWrite: true,
        listType: 4,
      }),
    },
    "listUserWorkspaces",
  );

  const data = unwrapApiData(payload, "listUserWorkspaces");
  return Array.isArray(data) ? data.filter(isRecord).map(normalizeWorkspaceRecord).filter(Boolean) : [];
}

function buildWsUrl(apiGateway, token) {
  const gateway = new URL(apiGateway);
  gateway.protocol = gateway.protocol === "http:" ? "ws:" : "wss:";
  gateway.pathname = "/ai";
  gateway.search = "";
  gateway.hash = "";
  gateway.searchParams.set("env", DEFAULT_ENV);
  gateway.searchParams.set("x-clickzetta-token", token);
  return gateway.toString();
}

function normalizeWorkspaceRecord(workspace) {
  if (!isRecord(workspace)) {
    return undefined;
  }

  const projectId = toScalarString(workspace.projectId);
  const projectName = asString(workspace.projectName) ?? asString(workspace.showName);
  const workspaceName = asString(workspace.showName) ?? asString(workspace.projectName);
  const workspaceId = toScalarString(workspace.workspaceId);

  if (!projectId && !workspaceId && !workspaceName && !projectName) {
    return undefined;
  }

  return {
    projectId,
    projectName,
    showName: workspaceName,
    workspaceId,
  };
}

function workspaceDisplayName(workspace) {
  return asString(workspace?.showName) ?? asString(workspace?.projectName);
}

function pickWorkspace(workspaces) {
  return workspaces.find((item) => asString(item.workspaceId) || asString(item.projectId));
}

function buildEnv({
  apiGateway,
  token,
  instanceName,
  instanceId,
  userId,
  tenantId,
  username,
  workspace,
}) {
  const env = {
    CZ_AGENT_WS_URL: buildWsUrl(apiGateway, token),
    CZ_INSTANCE_ID: instanceId,
    CZ_INSTANCE_NAME: instanceName,
    CZ_USER_ID: userId,
    CZ_TENANT_ID: tenantId,
  };

  const resolvedUsername = asString(username);
  if (resolvedUsername) {
    env.CZ_USERNAME = resolvedUsername;
  }

  const projectId = toScalarString(workspace?.projectId);
  const projectName = asString(workspace?.projectName) ?? asString(workspace?.showName);
  const workspaceName = asString(workspace?.showName) ?? asString(workspace?.projectName);
  const workspaceId = toScalarString(workspace?.workspaceId);

  if (projectId) {
    env.CZ_PROJECT_ID = projectId;
  }
  if (projectName) {
    env.CZ_PROJECT_NAME = projectName;
  }
  if (workspaceName) {
    env.CZ_WORKSPACE = workspaceName;
  }
  if (workspaceId) {
    env.CZ_WORKSPACE_ID = workspaceId;
  }

  return env;
}

function getCacheDir() {
  const stateDir = asString(hostEnv.OPENCLAW_STATE_DIR);
  if (stateDir) {
    return path.join(stateDir, "cache");
  }
  return path.join(os.homedir(), ".openclaw", "cache");
}

function getCachePath() {
  return path.join(getCacheDir(), "studio-agent-discovery.json");
}

function getWorkspaceSelectionPath() {
  return path.join(getCacheDir(), "studio-agent-workspace-selection.json");
}

function readDiscoveryCache() {
  const cachePath = getCachePath();
  if (!fs.existsSync(cachePath)) {
    return {};
  }
  try {
    const parsed = JSON.parse(fs.readFileSync(cachePath, "utf8"));
    if (!isRecord(parsed)) {
      return {};
    }
    // Prune entries from old cache versions or with expired tokens
    let pruned = false;
    for (const key of Object.keys(parsed)) {
      const entry = parsed[key];
      if (!isRecord(entry)) {
        delete parsed[key];
        pruned = true;
        continue;
      }
      const entryVersion = entry.version;
      if (entryVersion !== undefined && entryVersion !== CACHE_VERSION) {
        delete parsed[key];
        pruned = true;
        continue;
      }
      const expiresAtMs = entry.expiresAtMs;
      if (typeof expiresAtMs === "number" && expiresAtMs <= Date.now()) {
        delete parsed[key];
        pruned = true;
      }
    }
    if (pruned && Object.keys(parsed).length > 0) {
      writeDiscoveryCache(parsed);
    } else if (pruned) {
      try { fs.unlinkSync(cachePath); } catch { /* ignore */ }
    }
    return parsed;
  } catch {
    return {};
  }
}

function writeDiscoveryCache(cache) {
  atomicWriteJsonSync(getCachePath(), cache);
}

function readWorkspaceSelectionStore() {
  const selectionPath = getWorkspaceSelectionPath();
  if (!fs.existsSync(selectionPath)) {
    return {};
  }
  try {
    const parsed = JSON.parse(fs.readFileSync(selectionPath, "utf8"));
    if (!isRecord(parsed)) {
      return {};
    }
    return parsed;
  } catch {
    return {};
  }
}

function writeWorkspaceSelectionStore(store) {
  atomicWriteJsonSync(getWorkspaceSelectionPath(), store);
}

function buildCacheKey({ studioOrigin, username, instanceName, instanceId, apiGateway }) {
  return JSON.stringify({
    v: CACHE_VERSION,
    studioOrigin,
    username,
    instanceName: instanceName ?? "",
    instanceId: instanceId ?? "",
    apiGateway,
  });
}

function buildWorkspaceSelectionKey({ studioOrigin, username, instanceName, apiGateway }) {
  return JSON.stringify({
    v: WORKSPACE_SELECTION_VERSION,
    studioOrigin,
    username,
    instanceName: instanceName ?? "",
    apiGateway,
  });
}

function isUsableCachedEnv(env) {
  return (
    isRecord(env) &&
    Boolean(asString(env.CZ_AGENT_WS_URL)) &&
    Boolean(asString(env.CZ_INSTANCE_ID)) &&
    Boolean(asString(env.CZ_USER_ID)) &&
    Boolean(asString(env.CZ_TENANT_ID))
  );
}

function readCachedDiscovery({ studioOrigin, username, instanceName, instanceId, apiGateway }) {
  const key = buildCacheKey({ studioOrigin, username, instanceName, instanceId, apiGateway });
  const cache = readDiscoveryCache();
  const entry = cache[key];
  if (!isRecord(entry)) {
    return undefined;
  }

  const expiresAtMs =
    typeof entry.expiresAtMs === "number" && Number.isFinite(entry.expiresAtMs)
      ? entry.expiresAtMs
      : undefined;
  if (!expiresAtMs || expiresAtMs <= Date.now() + CACHE_TTL_SKEW_MS) {
    return undefined;
  }

  if (!isUsableCachedEnv(entry.env)) {
    return undefined;
  }

  const workspacesRefreshedAtMs =
    typeof entry.workspacesRefreshedAtMs === "number" && Number.isFinite(entry.workspacesRefreshedAtMs)
      ? entry.workspacesRefreshedAtMs
      : typeof entry.cachedAtMs === "number" && Number.isFinite(entry.cachedAtMs)
        ? entry.cachedAtMs
        : undefined;
  const workspacesFresh =
    typeof workspacesRefreshedAtMs === "number" && Date.now() - workspacesRefreshedAtMs < WORKSPACE_LIST_TTL_MS;

  return {
    env: entry.env,
    expiresAtMs,
    workspace: normalizeWorkspaceRecord(entry.workspace),
    workspaces: Array.isArray(entry.workspaces)
      ? entry.workspaces.map(normalizeWorkspaceRecord).filter(Boolean)
      : [],
    workspacesFresh,
    workspacesRefreshedAtMs,
  };
}

function normalizeDiscoveryContext(input) {
  const studioOrigin = normalizeStudioOrigin(input?.domain);
  if (!studioOrigin) {
    return undefined;
  }

  const instanceName = asString(input?.instanceName) ?? deriveInstanceName(studioOrigin);
  const username = asString(input?.username);
  const password = asString(input?.password);
  if (!instanceName || !username || !password) {
    return undefined;
  }

  return {
    studioOrigin,
    instanceName,
    username,
    password,
    apiGateway: resolveApiGateway(studioOrigin, input?.apiGateway),
    cacheInstanceId: asString(input?.instanceId),
    jdbcUrl: asString(input?.jdbcUrl),
    preferredWorkspace: asString(input?.workspace),
    preferredWorkspaceId: asString(input?.workspaceId),
    preferredProjectId: asString(input?.projectId),
  };
}

function hasConfiguredWorkspaceSelector(ctx) {
  return Boolean(ctx.preferredWorkspace || ctx.preferredWorkspaceId || ctx.preferredProjectId);
}

export function hasReusableDiscoveryCache(input) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    return false;
  }

  return Boolean(
    readCachedDiscovery({
      studioOrigin: ctx.studioOrigin,
      username: ctx.username,
      instanceName: ctx.instanceName,
      instanceId: ctx.cacheInstanceId,
      apiGateway: ctx.apiGateway,
    }),
  );
}

function persistCachedDiscovery({
  studioOrigin,
  username,
  instanceName,
  instanceId,
  apiGateway,
  env,
  expiresAtMs,
  workspace,
  workspaces,
  workspacesRefreshedAtMs,
}) {
  const key = buildCacheKey({ studioOrigin, username, instanceName, instanceId, apiGateway });
  const cache = readDiscoveryCache();
  const existingEntry = isRecord(cache[key]) ? cache[key] : {};
  cache[key] = {
    version: CACHE_VERSION,
    cachedAtMs: Date.now(),
    expiresAtMs,
    env,
    workspace: normalizeWorkspaceRecord(workspace),
    workspaces: Array.isArray(workspaces) ? workspaces.map(normalizeWorkspaceRecord).filter(Boolean) : [],
    workspacesRefreshedAtMs:
      typeof workspacesRefreshedAtMs === "number" && Number.isFinite(workspacesRefreshedAtMs)
        ? workspacesRefreshedAtMs
        : typeof existingEntry.workspacesRefreshedAtMs === "number" && Number.isFinite(existingEntry.workspacesRefreshedAtMs)
          ? existingEntry.workspacesRefreshedAtMs
          : Date.now(),
  };
  writeDiscoveryCache(cache);
}

async function refreshWorkspaceListWithCachedDiscovery(input, ctx, cached, options = {}) {
  if (!cached || !isUsableCachedEnv(cached.env)) {
    return undefined;
  }

  const forceRefresh = options.forceRefresh === true;
  if (!forceRefresh && cached.workspacesFresh && Array.isArray(cached.workspaces) && cached.workspaces.length > 0) {
    return {
      ...cached,
      env: applyContextEnv(cached.env, ctx),
    };
  }

  const token = extractTokenFromWsUrl(cached.env.CZ_AGENT_WS_URL);
  const instanceId = asString(cached.env.CZ_INSTANCE_ID) ?? ctx.cacheInstanceId;
  const userId = asString(cached.env.CZ_USER_ID);
  const tenantId = asString(cached.env.CZ_TENANT_ID);
  if (!token || !instanceId || !userId || !tenantId) {
    return undefined;
  }

  const workspaces = await listUserWorkspaces({
    apiGateway: ctx.apiGateway,
    studioOrigin: ctx.studioOrigin,
    instanceName: ctx.instanceName,
    instanceId,
    token,
    userId,
    tenantId,
  });
  const workspace = pickWorkspace(workspaces);
  const env = applyContextEnv(applyWorkspaceEnv(cached.env, workspace), ctx);
  const workspacesRefreshedAtMs = Date.now();

  persistCachedDiscovery({
    studioOrigin: ctx.studioOrigin,
    username: ctx.username,
    instanceName: ctx.instanceName,
    instanceId: ctx.cacheInstanceId,
    apiGateway: ctx.apiGateway,
    env,
    expiresAtMs: cached.expiresAtMs,
    workspace,
    workspaces,
    workspacesRefreshedAtMs,
  });

  return {
    env,
    expiresAtMs: cached.expiresAtMs,
    workspace,
    workspaces,
    workspacesFresh: true,
    workspacesRefreshedAtMs,
  };
}

function readWorkspaceSelection(input) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    return undefined;
  }
  const key = buildWorkspaceSelectionKey(ctx);
  const store = readWorkspaceSelectionStore();
  const entry = store[key];
  if (!isRecord(entry)) {
    return undefined;
  }
  return normalizeWorkspaceRecord(entry.workspace);
}

function persistWorkspaceSelection(input, workspace) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    throw new Error("Auto discovery requires domain");
  }
  const normalizedWorkspace = normalizeWorkspaceRecord(workspace);
  if (!normalizedWorkspace) {
    throw new Error("Cannot persist an empty workspace selection");
  }
  const key = buildWorkspaceSelectionKey(ctx);
  const store = readWorkspaceSelectionStore();
  store[key] = {
    version: WORKSPACE_SELECTION_VERSION,
    updatedAtMs: Date.now(),
    workspace: normalizedWorkspace,
  };
  writeWorkspaceSelectionStore(store);
}

export function clearWorkspaceSelection(input) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    return false;
  }
  const key = buildWorkspaceSelectionKey(ctx);
  const store = readWorkspaceSelectionStore();
  if (!Object.prototype.hasOwnProperty.call(store, key)) {
    return false;
  }
  delete store[key];
  writeWorkspaceSelectionStore(store);
  return true;
}

function buildWorkspaceEnv(workspace) {
  const normalizedWorkspace = normalizeWorkspaceRecord(workspace);
  const env = {};
  if (!normalizedWorkspace) {
    return env;
  }

  if (normalizedWorkspace.projectId) {
    env.CZ_PROJECT_ID = normalizedWorkspace.projectId;
  }
  if (normalizedWorkspace.projectName) {
    env.CZ_PROJECT_NAME = normalizedWorkspace.projectName;
  }
  if (normalizedWorkspace.showName) {
    env.CZ_WORKSPACE = normalizedWorkspace.showName;
  }
  if (normalizedWorkspace.workspaceId) {
    env.CZ_WORKSPACE_ID = normalizedWorkspace.workspaceId;
  }
  return env;
}

function applyWorkspaceEnv(baseEnv, workspace) {
  const env = { ...baseEnv };
  delete env.CZ_PROJECT_ID;
  delete env.CZ_PROJECT_NAME;
  delete env.CZ_WORKSPACE;
  delete env.CZ_WORKSPACE_ID;
  return {
    ...env,
    ...buildWorkspaceEnv(workspace),
  };
}

function applyContextEnv(baseEnv, ctx) {
  const env = { ...baseEnv };
  if (asString(ctx?.jdbcUrl)) {
    env.CZ_STUDIO_JDBC_URL = asString(ctx.jdbcUrl);
  }
  return env;
}

function findWorkspaceMatches(workspaces, target) {
  const normalizedTarget = normalizeComparableText(target);
  if (!normalizedTarget) {
    return [];
  }

  const exactMatches = workspaces.filter((workspace) => {
    const displayName = normalizeComparableText(workspaceDisplayName(workspace));
    const projectName = normalizeComparableText(workspace?.projectName);
    const workspaceId = normalizeComparableText(workspace?.workspaceId);
    const projectId = normalizeComparableText(workspace?.projectId);
    return (
      displayName === normalizedTarget ||
      projectName === normalizedTarget ||
      workspaceId === normalizedTarget ||
      projectId === normalizedTarget
    );
  });
  if (exactMatches.length > 0) {
    return exactMatches;
  }

  return workspaces.filter((workspace) => {
    const displayName = normalizeComparableText(workspaceDisplayName(workspace));
    const projectName = normalizeComparableText(workspace?.projectName);
    return displayName?.includes(normalizedTarget) || projectName?.includes(normalizedTarget);
  });
}

function resolvePersistedWorkspace(workspaces, selection) {
  const normalizedSelection = normalizeWorkspaceRecord(selection);
  if (!normalizedSelection) {
    return undefined;
  }

  const directMatch = workspaces.find(
    (workspace) =>
      (normalizedSelection.workspaceId && workspace.workspaceId === normalizedSelection.workspaceId) ||
      (normalizedSelection.projectId && workspace.projectId === normalizedSelection.projectId),
  );
  if (directMatch) {
    return directMatch;
  }

  const targetName = workspaceDisplayName(normalizedSelection) ?? normalizedSelection.projectName;
  const fuzzyMatches = findWorkspaceMatches(workspaces, targetName);
  return fuzzyMatches.length === 1 ? fuzzyMatches[0] : undefined;
}

function resolveConfiguredWorkspace(workspaces, ctx) {
  if (!hasConfiguredWorkspaceSelector(ctx)) {
    return {
      kind: "none",
      workspace: undefined,
      matches: [],
    };
  }

  let matches = workspaces;
  if (ctx.preferredWorkspaceId) {
    matches = matches.filter((workspace) => workspace.workspaceId === ctx.preferredWorkspaceId);
  }
  if (ctx.preferredProjectId) {
    matches = matches.filter((workspace) => workspace.projectId === ctx.preferredProjectId);
  }

  if (ctx.preferredWorkspace) {
    const nameMatches = findWorkspaceMatches(matches, ctx.preferredWorkspace);
    matches = nameMatches.length > 0 ? nameMatches : [];
  }

  if (matches.length === 1) {
    return {
      kind: "matched",
      workspace: matches[0],
      matches,
    };
  }

  const selectors = [
    ctx.preferredWorkspace ? `workspace=${ctx.preferredWorkspace}` : null,
    ctx.preferredWorkspaceId ? `workspaceId=${ctx.preferredWorkspaceId}` : null,
    ctx.preferredProjectId ? `projectId=${ctx.preferredProjectId}` : null,
  ]
    .filter(Boolean)
    .join(", ");

  if (matches.length === 0) {
    return {
      kind: "missing",
      workspace: undefined,
      matches: [],
      error: `Configured workspace selector did not match any accessible workspace (${selectors}).`,
    };
  }

  return {
    kind: "ambiguous",
    workspace: undefined,
    matches,
    error: `Configured workspace selector matched multiple accessible workspaces (${selectors}). Please use workspaceId or projectId for a unique match.`,
  };
}

export function resolveAutoDiscoveryInput(raw, env = {}) {
  const source = isRecord(raw) ? raw : {};
  const envSource = isRecord(env) ? env : {};
  const jdbcUrl =
    asString(source.jdbcUrl) ??
    asString(source.jdbc) ??
    asString(source.studioJdbcUrl) ??
    asString(envSource.CZ_STUDIO_JDBC_URL) ??
    asString(envSource.CZ_STUDIO_JDBC);
  const jdbcConfig = jdbcUrl ? parseClickZettaJdbcUrl(jdbcUrl) : undefined;

  const domain =
    asString(source.domain) ??
    asString(source.studioDomain) ??
    asString(source.studioHost) ??
    asString(source.appDomain) ??
    asString(source.appUrl) ??
    jdbcConfig?.domain ??
    asString(envSource.CZ_STUDIO_DOMAIN);
  const username =
    asString(source.username) ??
    asString(source.userId) ??
    jdbcConfig?.username ??
    asString(envSource.CZ_STUDIO_USERNAME) ??
    asString(envSource.CZ_USERNAME);
  const password =
    asString(source.password) ??
    jdbcConfig?.password ??
    asString(envSource.CZ_STUDIO_PASSWORD);

  if (!domain || !username || !password) {
    return undefined;
  }

  return {
    jdbcUrl: jdbcConfig?.jdbcUrl,
    domain,
    username,
    password,
    workspace:
      asString(source.workspace) ??
      jdbcConfig?.workspace ??
      asString(envSource.CZ_WORKSPACE),
    workspaceId:
      asString(source.workspaceId) ??
      asString(envSource.CZ_WORKSPACE_ID),
    projectId:
      asString(source.projectId) ??
      asString(envSource.CZ_PROJECT_ID),
    instanceId:
      asString(source.instanceId) ??
      asString(envSource.CZ_STUDIO_INSTANCE_ID) ??
      asString(envSource.CZ_INSTANCE_ID),
    instanceName:
      asString(source.instanceName) ??
      jdbcConfig?.instanceName ??
      asString(envSource.CZ_STUDIO_INSTANCE_NAME) ??
      asString(envSource.CZ_INSTANCE_NAME),
    apiGateway:
      asString(source.apiGateway) ??
      asString(source.apiBaseUrl) ??
      asString(source.gateway) ??
      jdbcConfig?.apiGateway ??
      asString(envSource.CZ_STUDIO_API_GATEWAY),
  };
}

export async function discoverStudioEnv(input, options = {}) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    throw new Error("Auto discovery requires domain");
  }

  const { studioOrigin, instanceName, username, password, apiGateway, cacheInstanceId } = ctx;
  const useCache = options.useCache !== false;
  const cached = useCache
    ? readCachedDiscovery({
        studioOrigin,
        username,
        instanceName,
        instanceId: cacheInstanceId,
        apiGateway,
      })
    : undefined;
  if (cached) {
    const refreshedCached =
      options.refreshWorkspaces === true || options.requireWorkspaces === true
        ? await refreshWorkspaceListWithCachedDiscovery(input, ctx, cached, {
            forceRefresh: options.refreshWorkspaces === true,
          })
        : cached;
    const effectiveCached = refreshedCached ?? cached;
    const expiresInSeconds = Math.max(0, Math.floor((cached.expiresAtMs - Date.now()) / 1000));
    return {
      env: applyContextEnv(effectiveCached.env, ctx),
      workspace: effectiveCached.workspace,
      workspaces: effectiveCached.workspaces,
      workspacesFresh: effectiveCached.workspacesFresh,
      workspacesRefreshedAtMs: effectiveCached.workspacesRefreshedAtMs,
      notes: [
        `Reused cached ClickZetta discovery for ${studioOrigin}.`,
        options.refreshWorkspaces === true
          ? `Cached token remains valid for about ${expiresInSeconds}s; refreshed workspace list without re-running loginSingle/getCurrentUser.`
          : options.requireWorkspaces === true && !cached.workspacesFresh
            ? `Cached token remains valid for about ${expiresInSeconds}s; workspace list TTL expired so listUserWorkspaces was refreshed without re-running loginSingle/getCurrentUser.`
            : `Cached token remains valid for about ${expiresInSeconds}s; skipped loginSingle/getCurrentUser/listUserWorkspaces.`,
      ],
    };
  }

  const login = await loginSingle({
    apiGateway,
    username,
    password,
    instanceName,
  });
  const instanceId = asString(input?.instanceId) ?? login.instanceId;
  const currentUser = await getCurrentUser({
    apiGateway,
    studioOrigin,
    instanceName,
    instanceId,
    token: login.token,
  });
  const workspaces = await listUserWorkspaces({
    apiGateway,
    studioOrigin,
    instanceName,
    instanceId,
    token: login.token,
    userId: currentUser.userId,
    tenantId: currentUser.tenantId,
  });
  const workspace = pickWorkspace(workspaces);

  const notes = [
    `Auto-discovered ClickZetta config from ${studioOrigin} via loginSingle -> getCurrentUser -> listUserWorkspaces.`,
    `Resolved instanceName=${instanceName}, instanceId=${instanceId}, userId=${currentUser.userId}, tenantId=${currentUser.tenantId}.`,
  ];

  if (workspace) {
    const workspaceName = asString(workspace.showName) ?? asString(workspace.projectName);
    const projectId = toScalarString(workspace.projectId);
    const workspaceId = toScalarString(workspace.workspaceId);
    notes.push(
      `Using first accessible workspace: projectId=${projectId ?? "n/a"}, workspaceId=${workspaceId ?? "n/a"}, name=${workspaceName ?? "n/a"}.`,
    );
  } else {
    notes.push("Workspace list returned no entries; project/workspace enrichments were skipped.");
  }

  const env = buildEnv({
    apiGateway,
    token: login.token,
    instanceName,
    instanceId,
    userId: currentUser.userId,
    tenantId: currentUser.tenantId,
    username: currentUser.username ?? username,
    workspace,
  });
  const expiresAtMs = login.expireTime ?? getTokenExpiryMs(login.token);
  if (typeof expiresAtMs === "number" && Number.isFinite(expiresAtMs)) {
    persistCachedDiscovery({
      studioOrigin,
      username,
      instanceName,
      instanceId: cacheInstanceId,
      apiGateway,
      env,
      expiresAtMs,
      workspace,
      workspaces,
      workspacesRefreshedAtMs: Date.now(),
    });
    notes.push("Cached ClickZetta discovery for reuse until token expiry.");
  }

  return {
    env,
    workspace,
    workspaces,
    workspacesFresh: true,
    workspacesRefreshedAtMs: Date.now(),
    notes,
  };
}

export async function getStudioWorkspaceState(input, options = {}) {
  const ctx = normalizeDiscoveryContext(input);
  if (!ctx) {
    throw new Error("Auto discovery requires domain");
  }

  let discovery = await discoverStudioEnv(input, options);
  if (
    options.requireWorkspaces &&
    (!Array.isArray(discovery.workspaces) ||
      discovery.workspaces.length === 0 ||
      discovery.workspacesFresh === false)
  ) {
    discovery = await discoverStudioEnv(input, {
      ...options,
      useCache: options.useCache !== false,
      refreshWorkspaces: true,
    });
  }

  const workspaces = Array.isArray(discovery.workspaces) ? discovery.workspaces : [];
  const defaultWorkspace = normalizeWorkspaceRecord(discovery.workspace);
  const configuredResolution = resolveConfiguredWorkspace(workspaces, ctx);
  if (configuredResolution.error) {
    throw new Error(configuredResolution.error);
  }
  const configuredWorkspace = configuredResolution.workspace;
  const persistedSelection = readWorkspaceSelection(input);
  const persistedWorkspace = resolvePersistedWorkspace(workspaces, persistedSelection);
  const selectedWorkspace = configuredWorkspace ?? persistedWorkspace ?? defaultWorkspace;
  const selectedBy = configuredWorkspace ? "configured" : persistedWorkspace ? "persisted" : "default";

  return {
    ...discovery,
    env: selectedWorkspace ? applyWorkspaceEnv(discovery.env, selectedWorkspace) : { ...discovery.env },
    defaultWorkspace,
    configuredWorkspace,
    selectedWorkspace,
    selectedBy,
    workspaces,
  };
}

export async function selectWorkspace(input, target) {
  const state = await getStudioWorkspaceState(input, { requireWorkspaces: true });
  const matches = findWorkspaceMatches(state.workspaces, target);
  if (matches.length !== 1) {
    return {
      ok: false,
      matches,
      state,
    };
  }

  persistWorkspaceSelection(input, matches[0]);
  return {
    ok: true,
    workspace: matches[0],
    state: {
      ...state,
      env: applyWorkspaceEnv(state.env, matches[0]),
      selectedWorkspace: matches[0],
      selectedBy: "persisted",
    },
  };
}

export async function refreshStudioWorkspaces(input) {
  return getStudioWorkspaceState(input, {
    requireWorkspaces: true,
    refreshWorkspaces: true,
  });
}
