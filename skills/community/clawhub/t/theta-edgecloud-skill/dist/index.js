// build/config.js
var processEnv = process.env;
function readInt(name, fallback, opts) {
  const raw = processEnv[name];
  if (!raw)
    return fallback;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed))
    return fallback;
  const min = opts?.min;
  const max = opts?.max;
  if (min !== void 0 && parsed < min)
    return min;
  if (max !== void 0 && parsed > max)
    return max;
  return parsed;
}
function loadConfig() {
  const user = processEnv.THETA_INFERENCE_AUTH_USER;
  const pass = processEnv.THETA_INFERENCE_AUTH_PASS;
  return {
    dryRun: ["1", "true", "yes", "on"].includes(String(processEnv.THETA_DRY_RUN ?? "").trim().toLowerCase()),
    edgecloudApiKey: processEnv.THETA_EC_API_KEY,
    edgecloudProjectId: processEnv.THETA_EC_PROJECT_ID,
    edgecloudOrgId: processEnv.THETA_ORG_ID,
    videoSaId: processEnv.THETA_VIDEO_SA_ID,
    videoSaSecret: processEnv.THETA_VIDEO_SA_SECRET,
    charactersApiKey: processEnv.THETA_CHARACTERS_API_KEY,
    inferenceEndpoint: processEnv.THETA_INFERENCE_ENDPOINT,
    inferenceAuth: user && pass ? { user, pass } : void 0,
    onDemandApiToken: processEnv.THETA_ONDEMAND_API_TOKEN ?? processEnv.THETA_ONDEMAND_API_KEY ?? processEnv.THETA_API_KEY,
    onDemandApiBaseUrl: processEnv.THETA_ONDEMAND_API_BASE_URL ?? processEnv.THETA_API_BASE_URL,
    httpTimeoutMs: readInt("THETA_HTTP_TIMEOUT_MS", 2e4, { min: 1e3, max: 12e4 }),
    httpMaxRetries: readInt("THETA_HTTP_MAX_RETRIES", 2, { min: 0, max: 6 }),
    httpRetryBackoffMs: readInt("THETA_HTTP_RETRY_BACKOFF_MS", 250, { min: 25, max: 1e4 })
  };
}

// build/redaction.js
var SECRET_KEYS = ["apikey", "authorization", "secret", "password", "token", "credential", "privatekey", "mnemonic", "streamkey"];
function isSecretKey(key, value) {
  const normalized = key.toLowerCase().replace(/[^a-z]/g, "");
  if (typeof value === "number" && normalized.endsWith("tokens"))
    return false;
  return SECRET_KEYS.some((needle) => normalized.includes(needle));
}
var PLAINTEXT_SECRET_KEYS = ["cookie", "phrase", "seedword", "accesskey", "jwt"];
function isSecretLabel(label) {
  const normalized = label.toLowerCase().replace(/[^a-z]/g, "");
  return [...SECRET_KEYS, ...PLAINTEXT_SECRET_KEYS].some((needle) => normalized.includes(needle));
}
function redact(value) {
  if (!value)
    return "";
  return "[redacted]";
}
function redactAny(value, parentKey, seen = /* @__PURE__ */ new WeakSet()) {
  if (value === null || value === void 0)
    return value;
  if (typeof value === "string") {
    return parentKey && isSecretKey(parentKey) ? redact(value) : value;
  }
  if (typeof value !== "object")
    return value;
  if (seen.has(value))
    return "[circular]";
  seen.add(value);
  try {
    return redactContainer(value, parentKey, seen);
  } finally {
    seen.delete(value);
  }
}
function redactContainer(value, parentKey, seen) {
  if (Array.isArray(value)) {
    return value.map((entry) => redactAny(entry, parentKey, seen));
  }
  const out = {};
  const namedSecret = Object.entries(value).some(([k2, v]) => ["name", "key"].includes(k2) && typeof v === "string" && isSecretKey(v));
  for (const [k2, v] of Object.entries(value)) {
    if (["__proto__", "constructor", "prototype"].includes(k2))
      continue;
    if (isSecretKey(k2, v) || namedSecret && k2 === "value") {
      out[k2] = typeof v === "string" ? redact(v) : "[redacted]";
      continue;
    }
    out[k2] = redactAny(v, k2, seen);
  }
  return out;
}
function redactObject(obj) {
  return redactAny(obj);
}

// build/approval.js
function operatorDryRun() {
  return ["1", "true", "yes", "on"].includes(String(process.env.THETA_DRY_RUN ?? "").trim().toLowerCase());
}
function assertLive(cfg, action) {
  if (cfg.dryRun || operatorDryRun())
    throw new Error(`${action} blocked by THETA_DRY_RUN`);
}
function assertApproved(cfg, confirm, action) {
  assertLive(cfg, action);
  if (confirm !== true) {
    throw new Error(`${action} creates, changes, bills or deletes remote resources. Preview with THETA_DRY_RUN=1, get explicit user approval for this exact action, then pass confirm:true.`);
  }
}
function snapshotBody(value) {
  let copy;
  try {
    copy = JSON.parse(JSON.stringify(value));
  } catch {
    throw new Error("Request body must be JSON-serializable");
  }
  if (!copy || typeof copy !== "object" || Array.isArray(copy))
    throw new Error("Request body must be an object");
  return copy;
}
var CALLBACK_KEY = /webhook|callback/i;
function findCallbackFields(value, path = "") {
  if (!value || typeof value !== "object")
    return [];
  const found = [];
  for (const [key, item] of Object.entries(value)) {
    const here = path ? `${path}.${key}` : key;
    if (CALLBACK_KEY.test(key))
      found.push({ path: here, value: item });
    found.push(...findCallbackFields(item, here));
  }
  return found;
}
var MAX_CHAT_TOKENS = 5e3;
var FANOUT_OR_LENGTH_KEY = /^(?:max|min)_?.*tokens?$|^maxtokens$|^n$|^best_of$|^num_(?:beams|return_sequences|outputs|images)$|^max_length$/i;
function boundChatParams(input, defaultMaxTokens = 500) {
  if (!input || typeof input !== "object" || Array.isArray(input))
    return input;
  const out = { ...input };
  for (const key of Object.keys(out))
    if (FANOUT_OR_LENGTH_KEY.test(key) && key !== "max_tokens")
      delete out[key];
  if (Array.isArray(out.messages) || out.max_tokens !== void 0) {
    const requested = Number(out.max_tokens);
    const value = Number.isFinite(requested) ? Math.trunc(requested) : defaultMaxTokens;
    out.max_tokens = Math.min(Math.max(value, 1), MAX_CHAT_TOKENS);
  }
  return out;
}

// build/errors.js
var MAX_MESSAGE_LEN = 280;
var MAX_SCAN_LEN = 8192;
function thetaError(input) {
  return input;
}
var LABEL_PAIR = /(\\?["'`\u2018\u2019\u201c\u201d]?)([A-Za-z][\w.-]{0,63}(?: [A-Za-z][\w.-]{0,63})?)\\?["'`\u2018\u2019\u201c\u201d]?(\s*(?::=|=>|=|:|\uff1a|\uff1d)\s*)/g;
var MULTI_WORD_SECRETS = ["mnemonic", "phrase", "seedword", "privatekey"];
var PEM_BLOCK = /-----BEGIN [A-Z0-9 ]{1,40}-----[\s\S]*?(?:-----END [A-Z0-9 ]{1,40}-----|$)/gi;
var QUOTE_CLOSE = { '"': '"', "'": "'", "`": "`", "\u201C": "\u201D", "\u2018": "\u2019", "\u201D": "\u201D", "\u2019": "\u2019" };
function labelledValueEnd(text, start, multiWord = false) {
  const first = text[start];
  const skipQuoted = (i) => {
    const close = QUOTE_CLOSE[text[i]];
    for (let j = i + 1; j < text.length; j++) {
      if (text[j] === "\\") {
        j++;
        continue;
      }
      if (text[j] === close)
        return j + 1;
    }
    return text.length;
  };
  if (first === "\\" && text[start + 1] in QUOTE_CLOSE) {
    const close = `\\${QUOTE_CLOSE[text[start + 1]]}`;
    const end = text.indexOf(close, start + 2);
    return end === -1 ? text.length : end + close.length;
  }
  if (first in QUOTE_CLOSE)
    return skipQuoted(start);
  if (first === "[" || first === "{") {
    let depth = 0;
    for (let i = start; i < text.length; ) {
      const ch = text[i];
      if (ch in QUOTE_CLOSE) {
        i = skipQuoted(i);
        continue;
      }
      if (ch === "[" || ch === "{")
        depth++;
      else if (ch === "]" || ch === "}") {
        depth--;
        if (depth === 0)
          return i + 1;
      }
      i++;
    }
    return text.length;
  }
  if (multiWord)
    return text.length;
  const match = /^(?:(?:Bearer|Basic|Token) )?\S+/i.exec(text.slice(start, start + MAX_SCAN_LEN));
  return start + (match ? match[0].length : 0);
}
function redactLabelledSecrets(text) {
  const label = new RegExp(LABEL_PAIR.source, "g");
  let out = "";
  let last = 0;
  let match;
  while (match = label.exec(text)) {
    const name = match[2];
    const valueStart = match.index + match[0].length;
    if (!isSecretLabel(name)) {
      label.lastIndex = match.index + match[1].length + name.split(" ")[0].length;
      continue;
    }
    const normalized = name.toLowerCase().replace(/[^a-z]/g, "");
    const valueEnd = labelledValueEnd(text, valueStart, MULTI_WORD_SECRETS.some((n) => normalized.includes(n)));
    if (valueEnd === valueStart)
      continue;
    const value = text.slice(valueStart, valueEnd);
    if (/tokens$/i.test(name.replace(/[^A-Za-z]/g, "")) && /^\d+[,;]?$/.test(value))
      continue;
    const scheme = /^(Bearer|Basic|Token)\s+/i.exec(value);
    out += `${text.slice(last, valueStart)}${scheme ? `${scheme[1]} ` : ""}[redacted]`;
    last = valueEnd;
    label.lastIndex = valueEnd;
  }
  return out + text.slice(last);
}
function sanitizeHttpErrorMessage(message) {
  if (!message)
    return "HTTP request failed";
  message = message.slice(0, MAX_SCAN_LEN);
  try {
    const parsed = JSON.parse(message);
    if (parsed && typeof parsed === "object")
      message = JSON.stringify(redactObject(parsed));
  } catch {
  }
  const scanned = message.slice(0, MAX_SCAN_LEN).replace(/\s+/g, " ").replace(PEM_BLOCK, "[redacted]");
  let out = redactLabelledSecrets(scanned).replace(/\b(Bearer|Basic)\s+(?!\[redacted\])([A-Za-z0-9\-._~+/]+=*)/gi, (_m, scheme, token) => `${scheme} ${redact(token)}`).trim();
  if (out.length > MAX_MESSAGE_LEN) {
    out = `${out.slice(0, MAX_MESSAGE_LEN - 3)}...`;
  }
  return out || "HTTP request failed";
}
function isThetaOnDemandCapacityError(status, message) {
  return status === 409 && /no\s+instances\s+available/i.test(message);
}
function isRetriableHttpError(status, message) {
  return status >= 500 || status === 429 || status === 408 || isThetaOnDemandCapacityError(status, message);
}
function fromHttpError(service, endpoint2, status, message) {
  const sanitized = sanitizeHttpErrorMessage(message);
  const capacityExhausted = isThetaOnDemandCapacityError(status, message);
  return {
    code: capacityExhausted ? "THETA_ONDEMAND_CAPACITY_EXHAUSTED" : `HTTP_${status}`,
    message: capacityExhausted ? `Temporary Theta on-demand capacity exhaustion: ${sanitized}` : sanitized,
    retriable: isRetriableHttpError(status, message),
    service,
    endpoint: endpoint2,
    status
  };
}
function isStructuredError(value) {
  if (!value || typeof value !== "object")
    return false;
  const candidate = value;
  return typeof candidate.code === "string" && typeof candidate.message === "string" && typeof candidate.retriable === "boolean";
}
function fromTransportError(service, endpoint2, error) {
  const asAny = error;
  const isTimeout = asAny?.name === "AbortError" || asAny?.name === "TimeoutError";
  const message = sanitizeHttpErrorMessage(asAny?.message ?? String(error ?? "Network request failed"));
  return {
    code: isTimeout ? "HTTP_408" : "NETWORK_ERROR",
    message,
    retriable: true,
    service,
    endpoint: endpoint2,
    status: isTimeout ? 408 : void 0
  };
}

// build/clients/http.js
var RETRIABLE_STATUS = /* @__PURE__ */ new Set([408, 425, 429, 500, 502, 503, 504]);
function withAuth(headers = {}, auth2) {
  if (!auth2)
    return headers;
  const token = Buffer.from(`${auth2.user}:${auth2.pass}`).toString("base64");
  return { ...headers, Authorization: `Basic ${token}` };
}
function toPositiveInt(value, fallback, opts) {
  if (!Number.isFinite(value))
    return fallback;
  const asInt = Math.trunc(value);
  const min = opts?.min ?? Number.MIN_SAFE_INTEGER;
  const max = opts?.max ?? Number.MAX_SAFE_INTEGER;
  return Math.min(Math.max(asInt, min), max);
}
function backoffDelayMs(attempt, baseMs) {
  return baseMs * Math.max(1, 2 ** (attempt - 1));
}
var sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function request(url2, method, body, opts) {
  if (!/^https:\/\//i.test(url2))
    throw new Error("Only https:// URLs are allowed");
  const timeoutMs = toPositiveInt(opts?.timeoutMs, 2e4, { min: 1e3, max: 3e5 });
  const maxRetries = method === "GET" ? toPositiveInt(opts?.maxRetries, 2, { min: 0, max: 6 }) : 0;
  const retryBackoffMs = toPositiveInt(opts?.retryBackoffMs, 250, { min: 25, max: 1e4 });
  for (let attempt = 0; attempt <= maxRetries; attempt += 1) {
    const canRetry = attempt < maxRetries;
    try {
      const signal = AbortSignal.timeout(timeoutMs);
      const res = await fetch(url2, {
        redirect: "error",
        method,
        headers: withAuth(opts?.headers, opts?.auth),
        body,
        signal
      });
      if (res.ok)
        return res;
      const errorBody = await res.text();
      if (canRetry && (RETRIABLE_STATUS.has(res.status) || isRetriableHttpError(res.status, errorBody))) {
        await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
        continue;
      }
      throw fromHttpError(opts?.service ?? "unknown", url2, res.status, errorBody);
    } catch (error) {
      if (isStructuredError(error)) {
        throw error;
      }
      if (canRetry) {
        await sleep(backoffDelayMs(attempt + 1, retryBackoffMs));
        continue;
      }
      throw fromTransportError(opts?.service ?? "unknown", url2, error);
    }
  }
  throw fromTransportError(opts?.service ?? "unknown", url2, new Error("HTTP request failed after retries"));
}
async function getJson(url2, opts) {
  const res = await request(url2, "GET", void 0, opts);
  return res.json();
}
async function postJson(url2, body, opts) {
  const res = await request(url2, "POST", JSON.stringify(body), {
    ...opts,
    headers: withAuth({ "content-type": "application/json", ...opts?.headers ?? {} }, opts?.auth),
    auth: void 0
  });
  return res.json();
}
async function putEmpty(url2, opts) {
  await request(url2, "PUT", void 0, opts);
}
async function putJson(url2, body, opts) {
  const res = await request(url2, "PUT", JSON.stringify(body), {
    ...opts,
    headers: { "content-type": "application/json", ...opts?.headers ?? {} }
  });
  return res.json();
}
async function deleteEmpty(url2, opts) {
  await request(url2, "DELETE", void 0, opts);
}

// build/security.js
function thetaUrl(raw, kind) {
  let u;
  try {
    u = new URL(raw);
  } catch {
    throw new Error("Invalid Theta endpoint URL");
  }
  const allowed = kind === "ondemand" ? u.hostname === "ondemand.thetaedgecloud.com" : u.hostname.endsWith(".thetaedgecloud.com") || u.hostname.endsWith(".onthetaedgecloud.com");
  if (u.protocol !== "https:" || !allowed || u.username || u.password || u.port && u.port !== "443" || u.search || u.hash || u.pathname !== "/" && u.pathname !== "") {
    throw new Error("Theta endpoint must be an approved HTTPS origin without credentials, path, query, or fragment");
  }
  return u.origin;
}
function validateProbe(value) {
  if (value === void 0)
    return "openai";
  if (value === "openai" || value === "gradio")
    return value;
  throw new Error('probe must be exactly "openai" or "gradio"');
}
function pathSegment(value, label) {
  if (typeof value !== "string" || !value.trim() || value.trim() === "." || value.trim() === ".." || /[\x00-\x1f\x7f]/.test(value))
    throw new Error(`${label} must be a non-empty string and safe identifier`);
  return encodeURIComponent(value.trim());
}

// build/clients/edgecloudController.js
var BASE_CTRL = "https://controller.thetaedgecloud.com";
var BASE_API = "https://api.thetaedgecloud.com";
var CONTROLLER_DEFAULT_HEADERS = {
  accept: "application/json, text/plain, */*",
  "user-agent": "theta-edgecloud-skill"
};
function k(cfg) {
  if (!cfg.edgecloudApiKey)
    throw new Error("THETA_EC_API_KEY missing");
  return { ...CONTROLLER_DEFAULT_HEADERS, "x-api-key": cfg.edgecloudApiKey };
}
function net(cfg, service, headers) {
  return {
    service,
    headers,
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
function segment(value, field) {
  return pathSegment(value, field);
}
function url(base, path, params = {}) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === void 0 || value === null)
      continue;
    query.set(key, String(value));
  }
  const qs = query.toString();
  return `${base}${path}${qs ? `?${qs}` : ""}`;
}
function shouldTryNextRoute(error) {
  if (!isStructuredError(error))
    return false;
  return error.status === 404 || error.status === 405;
}
async function firstRoute(routes, request2) {
  const errors = [];
  for (const route of routes) {
    try {
      return await request2(route);
    } catch (error) {
      errors.push(error);
      if (!shouldTryNextRoute(error))
        throw error;
    }
  }
  throw errors[errors.length - 1] ?? new Error("No controller routes attempted");
}
function documentForm(projectId, file, metadata) {
  if (!file || typeof file !== "object")
    throw new Error("file must be an object");
  if (!file.filename?.trim())
    throw new Error("file.filename is required");
  if (typeof file.content !== "string")
    throw new Error("file.content must be a string");
  const bytes = file.encoding === "base64" ? Buffer.from(file.content, "base64") : Buffer.from(file.content, "utf8");
  const form = new FormData();
  form.set("project_id", projectId);
  form.set("metadata", JSON.stringify(metadata ?? {}));
  form.set("file", new Blob([bytes], { type: file.contentType ?? "text/plain" }), file.filename);
  return form;
}
async function postForm(targetUrl, form, cfg) {
  const res = await fetch(targetUrl, {
    redirect: "error",
    method: "POST",
    headers: k(cfg),
    body: form,
    signal: AbortSignal.timeout(cfg.httpTimeoutMs)
  });
  if (!res.ok)
    throw fromHttpError("edgecloud-controller", targetUrl, res.status, await res.text());
  return res.json();
}
async function putForm(targetUrl, form, cfg) {
  const res = await fetch(targetUrl, {
    redirect: "error",
    method: "PUT",
    headers: k(cfg),
    body: form,
    signal: AbortSignal.timeout(cfg.httpTimeoutMs)
  });
  if (!res.ok)
    throw fromHttpError("edgecloud-controller", targetUrl, res.status, await res.text());
  return res.json();
}
var edgecloudControllerClient = {
  startDeploymentByBaseId: (cfg, projectId, baseId, confirm) => assertApproved(cfg, confirm, "theta.deployments.startByBaseId") ?? putEmpty(url(BASE_CTRL, `/deployments/base/${segment(baseId, "baseId")}/start`, { project_id: projectId }), net(cfg, "edgecloud-controller", k(cfg))),
  listStandardTemplates: (cfg, category) => getJson(url(BASE_CTRL, "/deployment_template/list_standard_templates", { category }), net(cfg, "edgecloud-controller", k(cfg))),
  listCustomTemplates: (cfg, projectId) => getJson(url(BASE_CTRL, "/deployment_template/list_custom_templates", { project_id: projectId }), net(cfg, "edgecloud-controller", k(cfg))),
  listVmTypes: (cfg) => getJson(`${BASE_API}/resource/vm/list`, net(cfg, "edgecloud-controller", CONTROLLER_DEFAULT_HEADERS)),
  createDeployment: (cfg, payload, confirm) => assertApproved(cfg, confirm, "theta.deployments.create") ?? postJson(`${BASE_CTRL}/deployment`, payload, net(cfg, "edgecloud-controller", k(cfg))),
  listDeployments: (cfg, projectId) => firstRoute([
    url(BASE_CTRL, "/deployment/list", { project_id: projectId }),
    url(BASE_CTRL, "/deployments/list", { project_id: projectId })
  ], (route) => getJson(route, net(cfg, "edgecloud-controller", k(cfg)))),
  routeProbeDeploymentsList: async (cfg, projectId) => {
    const routes = [
      url(BASE_CTRL, "/deployment/list", { project_id: projectId }),
      url(BASE_CTRL, "/deployments/list", { project_id: projectId })
    ];
    const attempts = [];
    for (const route of routes) {
      try {
        const response = await getJson(route, net(cfg, "edgecloud-controller", k(cfg)));
        attempts.push({ route, ok: true });
        return { ok: true, selectedRoute: route, attempts, response };
      } catch (error) {
        attempts.push({
          route,
          ok: false,
          status: isStructuredError(error) ? error.status : void 0,
          code: isStructuredError(error) ? error.code : error?.name,
          message: error?.message ?? String(error)
        });
      }
    }
    return { ok: false, attempts };
  },
  balance: (cfg, orgId) => getJson(url(BASE_API, "/balance", { orgID: orgId }), net(cfg, "edgecloud-controller", k(cfg))),
  createChatbot: (cfg, payload, confirm) => assertApproved(cfg, confirm, "theta.ai.agent.create") ?? postJson(`${BASE_CTRL}/chatbot`, payload, net(cfg, "edgecloud-controller", k(cfg))),
  getChatbot: (cfg, chatbotId, projectId) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, "chatbotId")}`, { project_id: projectId }), net(cfg, "edgecloud-controller", k(cfg))),
  updateChatbot: (cfg, chatbotId, payload, confirm) => assertApproved(cfg, confirm, "theta.ai.agent.update") ?? putJson(`${BASE_CTRL}/chatbot/${segment(chatbotId, "chatbotId")}`, payload, net(cfg, "edgecloud-controller", k(cfg))),
  listChatbots: (cfg, projectId, page = 0, number = 100) => getJson(url(BASE_CTRL, "/chatbot/list", { project_id: projectId, page, number }), net(cfg, "edgecloud-controller", k(cfg))),
  createChatbotDocument: (cfg, chatbotId, projectId, file, metadata, confirm) => assertApproved(cfg, confirm, "theta.ai.agent.document.create") ?? postForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, "chatbotId")}/document`), documentForm(projectId, file, metadata), cfg),
  updateChatbotDocument: (cfg, chatbotId, documentId, projectId, file, metadata, confirm) => assertApproved(cfg, confirm, "theta.ai.agent.document.update") ?? putForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, "chatbotId")}/document/${segment(documentId, "documentId")}`), documentForm(projectId, file, metadata), cfg),
  getChatbotDocument: (cfg, chatbotId, documentId) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, "chatbotId")}/document/${segment(documentId, "documentId")}`), net(cfg, "edgecloud-controller", k(cfg))),
  listChatbotDocuments: (cfg, chatbotId, projectId, page = 0, number = 30) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, "chatbotId")}/document/list`, { project_id: projectId, page, number }), net(cfg, "edgecloud-controller", k(cfg))),
  stopDeployment: (cfg, projectId, shard, suffix, confirm) => assertApproved(cfg, confirm, "theta.deployments.stop") ?? firstRoute([
    url(BASE_CTRL, `/deployment/${segment(shard, "shard")}/${segment(suffix, "suffix")}/stop`, { project_id: projectId }),
    url(BASE_CTRL, `/deployments/${segment(shard, "shard")}/${segment(suffix, "suffix")}/stop`, { project_id: projectId })
  ], (route) => putEmpty(route, net(cfg, "edgecloud-controller", k(cfg)))),
  startDeployment: (cfg, projectId, shard, suffix, confirm) => assertApproved(cfg, confirm, "theta.deployments.start") ?? firstRoute([
    url(BASE_CTRL, `/deployment/${segment(shard, "shard")}/${segment(suffix, "suffix")}/start`, { project_id: projectId }),
    url(BASE_CTRL, `/deployments/${segment(shard, "shard")}/${segment(suffix, "suffix")}/start`, { project_id: projectId })
  ], (route) => putEmpty(route, net(cfg, "edgecloud-controller", k(cfg)))),
  deleteDeployment: (cfg, projectId, shard, suffix, confirm) => assertApproved(cfg, confirm, "theta.deployments.delete") ?? firstRoute([
    url(BASE_CTRL, `/deployment/${segment(shard, "shard")}/${segment(suffix, "suffix")}`, { project_id: projectId }),
    url(BASE_CTRL, `/deployments/${segment(shard, "shard")}/${segment(suffix, "suffix")}`, { project_id: projectId })
  ], (route) => deleteEmpty(route, net(cfg, "edgecloud-controller", k(cfg))))
};

// build/clients/edgecloudInference.js
var ALLOWED_INFERENCE_DOMAIN_SUFFIXES = [".thetaedgecloud.com", ".onthetaedgecloud.com"];
function isLoopbackOrPrivateHost(hostname) {
  const host = hostname.toLowerCase();
  if (host === "localhost" || host === "::1" || host === "0.0.0.0" || host === "::ffff:127.0.0.1")
    return true;
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(host)) {
    const parts = host.split(".").map((p) => Number.parseInt(p, 10));
    if (parts.some((p) => !Number.isInteger(p) || p < 0 || p > 255))
      return true;
    if (parts[0] === 10 || parts[0] === 127)
      return true;
    if (parts[0] === 169 && parts[1] === 254)
      return true;
    if (parts[0] === 192 && parts[1] === 168)
      return true;
    if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31)
      return true;
  }
  return host.startsWith("fe80:") || host.startsWith("fc") || host.startsWith("fd");
}
function parseEndpoint(raw, label) {
  try {
    const parsed = new URL(raw.trim());
    if (parsed.protocol !== "https:")
      throw new Error(`${label} must use https://`);
    if (parsed.username || parsed.password)
      throw new Error(`${label} must not include embedded credentials`);
    if (!parsed.hostname || isLoopbackOrPrivateHost(parsed.hostname)) {
      throw new Error(`${label} host is unsafe (private/loopback not allowed)`);
    }
    return parsed;
  } catch (error) {
    if (error instanceof Error && error.message.includes(label))
      throw error;
    throw new Error(`${label} must be an absolute https URL`);
  }
}
function isAllowedHost(hostname) {
  const host = hostname.toLowerCase();
  if (["controller.thetaedgecloud.com", "ondemand.thetaedgecloud.com", "api.thetaedgecloud.com", "ai-chars-api.thetaedgecloud.com"].includes(host))
    return false;
  return ALLOWED_INFERENCE_DOMAIN_SUFFIXES.some((suffix) => host.endsWith(suffix));
}
function endpoint(cfg, e) {
  const v = e ?? cfg.inferenceEndpoint;
  if (!v)
    throw new Error("THETA_INFERENCE_ENDPOINT missing");
  const parsed = parseEndpoint(thetaUrl(v, "dedicated"), "THETA_INFERENCE_ENDPOINT");
  if (!isAllowedHost(parsed.hostname)) {
    throw new Error("THETA_INFERENCE_ENDPOINT host is not allowed; use a Theta EdgeCloud endpoint");
  }
  return parsed.href.replace(/\/$/, "");
}
function auth(cfg, e, a) {
  if (a)
    return a;
  if (e && (!cfg.inferenceEndpoint || new URL(e.trim()).origin !== new URL(cfg.inferenceEndpoint.trim()).origin))
    return void 0;
  return cfg.inferenceAuth;
}
function net2(cfg, service, authOverride) {
  return {
    service,
    auth: authOverride,
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
var edgecloudInferenceClient = {
  listModels: (cfg, e, a) => getJson(`${endpoint(cfg, e)}/v1/models`, net2(cfg, "edgecloud-inference", auth(cfg, e, a))),
  gradioConfig: (cfg, e, a) => getJson(`${endpoint(cfg, e)}/config`, net2(cfg, "edgecloud-inference", auth(cfg, e, a))),
  chat: (cfg, body, e, a) => {
    assertLive(cfg, "Dedicated inference chat");
    const finalBody = boundChatParams(snapshotBody(body));
    if (!Array.isArray(finalBody.messages) || finalBody.messages.length === 0) {
      throw new Error("body must be an object with a non-empty messages array");
    }
    const hooks = findCallbackFields(finalBody);
    if (hooks.length)
      throw new Error(`Dedicated chat does not support webhook/callback fields (${hooks.map((h3) => h3.path).join(", ")})`);
    return postJson(`${endpoint(cfg, e)}/v1/chat/completions`, finalBody, net2(cfg, "edgecloud-inference", auth(cfg, e, a)));
  }
};

// build/commands/deployments.js
import { randomBytes } from "node:crypto";
var sleep2 = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function requireText(value, field) {
  if (value === void 0 || value === null || String(value).trim() === "") {
    throw new Error(`${field} must be a non-empty string`);
  }
  return String(value).trim();
}
function clampInt(value, fallback, min, max) {
  if (!Number.isFinite(value))
    return fallback;
  return Math.min(Math.max(Math.trunc(value), min), max);
}
function generatedPassword() {
  return randomBytes(18).toString("base64url");
}
function findKey(obj, names) {
  if (obj && typeof obj === "object") {
    if (Array.isArray(obj)) {
      for (const item of obj) {
        const found = findKey(item, names);
        if (found !== void 0 && found !== null && found !== "")
          return found;
      }
      return void 0;
    }
    for (const [key, value] of Object.entries(obj)) {
      if (names.has(key.toLowerCase()) && value !== void 0 && value !== null && value !== "")
        return value;
    }
    for (const value of Object.values(obj)) {
      const found = findKey(value, names);
      if (found !== void 0 && found !== null && found !== "")
        return found;
    }
  }
  return void 0;
}
function extractNumericValue(obj, names) {
  if (obj && typeof obj === "object") {
    if (Array.isArray(obj)) {
      for (const item of obj) {
        const found = extractNumericValue(item, names);
        if (found !== void 0)
          return found;
      }
      return void 0;
    }
    for (const [key, value] of Object.entries(obj)) {
      if (!names.has(key.toLowerCase()))
        continue;
      const parsed = Number(value);
      if (Number.isFinite(parsed))
        return parsed;
    }
    for (const value of Object.values(obj)) {
      const found = extractNumericValue(value, names);
      if (found !== void 0)
        return found;
    }
  }
  return void 0;
}
function balanceValue(response) {
  return extractNumericValue(response, /* @__PURE__ */ new Set(["balance", "amount", "available", "credit", "credits", "remaining", "total"]));
}
async function balanceSnapshot(cfg, orgId) {
  const resolvedOrgId = orgId ?? cfg.edgecloudOrgId;
  if (!resolvedOrgId)
    return { skipped: true, reason: "missing_org_id" };
  if (!cfg.edgecloudApiKey)
    return { skipped: true, reason: "missing_THETA_EC_API_KEY" };
  try {
    const response = await edgecloudControllerClient.balance(cfg, resolvedOrgId);
    return { skipped: false, orgId: resolvedOrgId, value: balanceValue(response), response };
  } catch (error) {
    return {
      skipped: true,
      reason: "balance_lookup_failed",
      error: error?.message ?? String(error)
    };
  }
}
function balanceDelta(before, after) {
  const beforeValue = typeof before.value === "number" ? before.value : void 0;
  const afterValue = typeof after.value === "number" ? after.value : void 0;
  return {
    before,
    after,
    delta: beforeValue !== void 0 && afterValue !== void 0 ? afterValue - beforeValue : null
  };
}
async function waitForDedicatedProbe(cfg, endpoint2, auth2, probe, timeoutMs, intervalMs) {
  validateProbe(probe);
  const startedAt = Date.now();
  const attempts = [];
  while (Date.now() - startedAt < timeoutMs) {
    const attemptStartedAt = Date.now();
    try {
      const response = probe === "gradio" ? await edgecloudInferenceClient.gradioConfig(cfg, endpoint2, auth2) : await edgecloudInferenceClient.listModels(cfg, endpoint2, auth2);
      attempts.push({ ok: true, elapsedMs: Date.now() - attemptStartedAt });
      return { ready: true, probe, endpoint: endpoint2, elapsedMs: Date.now() - startedAt, attempts, response };
    } catch (error) {
      attempts.push({
        ok: false,
        elapsedMs: Date.now() - attemptStartedAt,
        status: error?.status,
        code: error?.code ?? error?.name,
        message: error?.message ?? String(error)
      });
    }
    const remainingMs = timeoutMs - (Date.now() - startedAt);
    if (remainingMs <= 0)
      break;
    await sleep2(Math.min(intervalMs, remainingMs));
  }
  return { ready: false, probe, endpoint: endpoint2, elapsedMs: Date.now() - startedAt, attempts };
}
var deployments = {
  startByBaseId: (cfg, projectId, baseId, confirm) => cfg.dryRun ? { dryRun: true, action: "startByBaseId", projectId, baseId } : edgecloudControllerClient.startDeploymentByBaseId(cfg, projectId, baseId, confirm),
  listStandard: (cfg, category) => edgecloudControllerClient.listStandardTemplates(cfg, category),
  listCustom: (cfg, projectId) => edgecloudControllerClient.listCustomTemplates(cfg, projectId),
  listVm: (cfg) => edgecloudControllerClient.listVmTypes(cfg),
  balance: (cfg, orgId) => edgecloudControllerClient.balance(cfg, requireText(orgId ?? cfg.edgecloudOrgId, "orgId")),
  balanceSnapshot,
  routeProbe: (cfg, projectId) => edgecloudControllerClient.routeProbeDeploymentsList(cfg, projectId),
  create: (cfg, payload, confirm) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : edgecloudControllerClient.createDeployment(cfg, payload, confirm),
  list: (cfg, projectId) => edgecloudControllerClient.listDeployments(cfg, projectId),
  start: (cfg, projectId, shard, suffix, confirm) => cfg.dryRun ? { dryRun: true, action: "start", projectId, shard, suffix } : edgecloudControllerClient.startDeployment(cfg, projectId, shard, suffix, confirm),
  stop: (cfg, projectId, shard, suffix, confirm) => cfg.dryRun ? { dryRun: true, action: "stop", projectId, shard, suffix } : edgecloudControllerClient.stopDeployment(cfg, projectId, shard, suffix, confirm),
  delete: (cfg, projectId, shard, suffix, confirm) => cfg.dryRun ? { dryRun: true, action: "delete", projectId, shard, suffix } : edgecloudControllerClient.deleteDeployment(cfg, projectId, shard, suffix, confirm),
  validateDisposable: async (cfg, opts) => {
    const probe = validateProbe(opts.probe);
    const payload = { ...opts.payload };
    const projectId = String(opts.projectId ?? payload.project_id ?? cfg.edgecloudProjectId ?? "").trim();
    if (!projectId)
      throw new Error("projectId or payload.project_id is required");
    payload.project_id = projectId;
    const authUser = String(payload.auth_username ?? `openclaw_${randomBytes(4).toString("hex")}`);
    const authPass = String(payload.auth_password ?? generatedPassword());
    payload.auth_username = authUser;
    payload.auth_password = authPass;
    const auth2 = { user: authUser, pass: authPass };
    const readyTimeoutMs = clampInt(opts.readyTimeoutMs, 12e4, 1e3, 18e5);
    const intervalMs = clampInt(opts.intervalMs, 1e4, 500, 6e4);
    if (cfg.dryRun) {
      return redactObject({
        dryRun: true,
        would: [
          "read org balance before if orgId is configured",
          "create deployment with generated Basic Auth",
          `poll ${probe} readiness`,
          "run one minimal smoke call for OpenAI-compatible probes",
          "delete deployment in cleanup",
          "verify cleanup from deployment list",
          "read org balance after and report delta"
        ],
        payload,
        probe,
        readyTimeoutMs,
        intervalMs,
        orgIdConfigured: Boolean(opts.orgId ?? cfg.edgecloudOrgId)
      });
    }
    assertApproved(cfg, opts.confirm, "theta.deployments.validateDisposable");
    let created;
    let readiness;
    let smoke;
    let deleteResult;
    let cleanupVerification;
    let operationFailure;
    const before = await balanceSnapshot(cfg, opts.orgId);
    try {
      created = await edgecloudControllerClient.createDeployment(cfg, payload, opts.confirm);
      const endpoint2 = String(findKey(created, /* @__PURE__ */ new Set(["endpoint", "endpointurl", "url"])) ?? "").trim();
      if (!endpoint2)
        throw new Error("Deployment create response did not include an endpoint");
      readiness = await waitForDedicatedProbe(cfg, endpoint2, auth2, probe, readyTimeoutMs, intervalMs);
      if (probe === "openai" && readiness.ready && opts.smokeMessage) {
        const readinessModel = findKey(readiness.response, /* @__PURE__ */ new Set(["id", "model"]));
        smoke = await edgecloudInferenceClient.chat(cfg, {
          model: opts.model ?? String(readinessModel ?? "default"),
          messages: [{ role: "user", content: opts.smokeMessage }],
          max_tokens: 32
        }, endpoint2, auth2);
      }
    } catch (error) {
      operationFailure = error?.message ?? String(error);
    } finally {
      const baseId = created ? findKey(created, /* @__PURE__ */ new Set(["baseid", "base_id", "deployment_id", "id"])) : void 0;
      const shard = created ? findKey(created, /* @__PURE__ */ new Set(["shard"])) : void 0;
      const suffix = created ? findKey(created, /* @__PURE__ */ new Set(["suffix"])) : void 0;
      if (created && shard !== void 0 && shard !== null && String(shard) !== "" && suffix !== void 0 && suffix !== null && String(suffix) !== "") {
        try {
          await edgecloudControllerClient.deleteDeployment(cfg, projectId, String(shard), String(suffix), opts.confirm);
          deleteResult = { ok: true, shard, suffix };
        } catch (error) {
          deleteResult = { ok: false, error: error?.message ?? String(error) };
        }
      } else {
        deleteResult = { ok: false, warning: "could_not_determine_delete_handle", baseId, shard, suffix };
      }
      try {
        const listed = await edgecloudControllerClient.listDeployments(cfg, projectId);
        const needleValues = [baseId, suffix].filter((value) => value !== void 0 && value !== null && value !== "").map(String);
        const response = listed;
        const body = response?.body ?? listed;
        const rows = Array.isArray(body) ? body : body?.deployments;
        const identifiable = (entry) => !!entry && typeof entry === "object" && Object.entries(entry).some(([key, value]) => ["baseid", "base_id", "deployment_id", "id", "suffix"].includes(key.toLowerCase()) && ["string", "number"].includes(typeof value) && String(value).length > 0 || typeof value === "object" && identifiable(value));
        const knownList = Array.isArray(rows) && rows.every(identifiable);
        const containsHandle = (entry) => {
          if (!entry || typeof entry !== "object")
            return false;
          return Object.entries(entry).some(([key, value]) => ["baseid", "base_id", "deployment_id", "id", "suffix"].includes(key.toLowerCase()) && needleValues.includes(String(value)) || typeof value === "object" && containsHandle(value));
        };
        cleanupVerification = {
          checked: knownList && needleValues.length > 0,
          projectId,
          deletedHandlesAbsent: knownList && needleValues.length > 0 && !rows.some(containsHandle),
          handlesChecked: needleValues
        };
      } catch (error) {
        cleanupVerification = { checked: false, error: error?.message ?? String(error) };
      }
    }
    const after = await balanceSnapshot(cfg, opts.orgId);
    return redactObject({
      // ok = create, readiness and verified cleanup all succeeded, plus (for the default openai
      // probe) a successful inference smoke call, which needs smokeMessage. smokeTested says
      // whether inference was exercised.
      ok: !operationFailure && readiness?.ready === true && deleteResult?.ok === true && cleanupVerification?.deletedHandlesAbsent === true && (probe !== "openai" || smoke !== void 0),
      smokeTested: smoke !== void 0,
      operationFailure,
      createResponse: created,
      readiness,
      smokeResponse: smoke,
      deleteResult,
      cleanupVerification,
      balance: balanceDelta(before, after)
    });
  },
  chatbotCreate: (cfg, payload, confirm) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : edgecloudControllerClient.createChatbot(cfg, payload, confirm),
  chatbotGet: (cfg, chatbotId, projectId) => edgecloudControllerClient.getChatbot(cfg, chatbotId, projectId),
  chatbotUpdate: (cfg, chatbotId, payload, confirm) => cfg.dryRun ? redactObject({ dryRun: true, chatbotId, payload }) : edgecloudControllerClient.updateChatbot(cfg, chatbotId, payload, confirm),
  chatbotList: (cfg, projectId, page = 0, number = 100) => edgecloudControllerClient.listChatbots(cfg, projectId, page, number),
  chatbotDocumentCreate: (cfg, chatbotId, projectId, file, metadata, confirm) => cfg.dryRun ? { dryRun: true, chatbotId, projectId, file: { ...file, content: "[redacted]" }, metadata } : edgecloudControllerClient.createChatbotDocument(cfg, chatbotId, projectId, file, metadata, confirm),
  chatbotDocumentUpdate: (cfg, chatbotId, documentId, projectId, file, metadata, confirm) => cfg.dryRun ? { dryRun: true, chatbotId, documentId, projectId, file: { ...file, content: "[redacted]" }, metadata } : edgecloudControllerClient.updateChatbotDocument(cfg, chatbotId, documentId, projectId, file, metadata, confirm),
  chatbotDocumentGet: (cfg, chatbotId, documentId) => edgecloudControllerClient.getChatbotDocument(cfg, chatbotId, documentId),
  chatbotDocumentList: (cfg, chatbotId, projectId, page = 0, number = 30) => edgecloudControllerClient.listChatbotDocuments(cfg, chatbotId, projectId, page, number)
};

// build/commands/inference.js
var sleep3 = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function clampInt2(value, fallback, min, max) {
  if (!Number.isFinite(value))
    return fallback;
  return Math.min(Math.max(Math.trunc(value), min), max);
}
function annotateEndpointReadinessError(error) {
  if (isStructuredError(error) && (error.status === 502 || error.status === 503)) {
    throw thetaError({
      ...error,
      code: "THETA_DEDICATED_ENDPOINT_UPSTREAM_UNREADY",
      retriable: true,
      message: `Dedicated inference endpoint is not ready upstream (HTTP ${error.status}). Auth layer may be active while upstream service remains unavailable. Likely platform ingress/backend readiness mismatch; retry or verify endpoint health from Theta dashboard logs.`
    });
  }
  throw error;
}
var inference = {
  models: async (cfg, endpoint2) => {
    try {
      return await edgecloudInferenceClient.listModels(cfg, endpoint2);
    } catch (error) {
      annotateEndpointReadinessError(error);
    }
  },
  chat: async (cfg, body, endpoint2) => {
    if (cfg.dryRun)
      return { dryRun: true, endpoint: endpoint2, body: boundChatParams(snapshotBody(body)) };
    try {
      return await edgecloudInferenceClient.chat(cfg, body, endpoint2);
    } catch (error) {
      annotateEndpointReadinessError(error);
    }
  },
  ready: async (cfg, opts = {}) => {
    const probe = validateProbe(opts.probe);
    const timeoutMs = clampInt2(opts.timeoutMs, 12e4, 1e3, 18e5);
    const intervalMs = clampInt2(opts.intervalMs, 5e3, 500, 6e4);
    if (cfg.dryRun)
      return { dryRun: true, probe, timeoutMs, intervalMs };
    const startedAt = Date.now();
    const attempts = [];
    while (Date.now() - startedAt < timeoutMs) {
      const attemptStartedAt = Date.now();
      try {
        const response = probe === "gradio" ? await edgecloudInferenceClient.gradioConfig(cfg) : await edgecloudInferenceClient.listModels(cfg);
        attempts.push({ ok: true, elapsedMs: Date.now() - attemptStartedAt });
        return {
          ready: true,
          probe,
          elapsedMs: Date.now() - startedAt,
          attempts,
          response
        };
      } catch (error) {
        attempts.push({
          ok: false,
          elapsedMs: Date.now() - attemptStartedAt,
          status: isStructuredError(error) ? error.status : void 0,
          code: isStructuredError(error) ? error.code : error?.name,
          message: error?.message ?? String(error)
        });
      }
      const remainingMs = timeoutMs - (Date.now() - startedAt);
      if (remainingMs <= 0)
        break;
      await sleep3(Math.min(intervalMs, remainingMs));
    }
    return {
      ready: false,
      probe,
      elapsedMs: Date.now() - startedAt,
      attempts
    };
  }
};

// build/clients/thetaVideo.js
var BASE = "https://api.thetavideoapi.com";
var RESERVED_QUERY = /* @__PURE__ */ new Set(["page", "number", "operator"]);
var FILTER_KEY = /^[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}$/;
var MAX_FILTERS = 10;
function boundedInt(value, label, fallback, min, max) {
  if (value === void 0)
    return fallback;
  if (typeof value !== "number" || !Number.isInteger(value) || value < min || value > max)
    throw new Error(`${label} must be an integer from ${min} to ${max}`);
  return value;
}
function videoSearchQuery(filters, operator, page, number) {
  if (!filters || typeof filters !== "object" || Array.isArray(filters))
    throw new Error("filters must be an object of metadata key -> string value");
  const entries = Object.entries(filters);
  if (entries.length < 1 || entries.length > MAX_FILTERS)
    throw new Error(`filters must have 1 to ${MAX_FILTERS} keys`);
  const params = new URLSearchParams();
  for (const [key, value] of entries) {
    if (!FILTER_KEY.test(key) || RESERVED_QUERY.has(key.toLowerCase()))
      throw new Error(`invalid filter key: ${key.slice(0, 64)}`);
    if (typeof value !== "string" || value.length > 256 || /[\x00-\x1f\x7f]/.test(value))
      throw new Error(`filter ${key} must be a string of at most 256 printable characters`);
    params.append(key, value);
  }
  if (operator !== void 0 && operator !== "and" && operator !== "or")
    throw new Error('operator must be "and" or "or"');
  if (operator)
    params.set("operator", operator);
  params.set("page", String(boundedInt(page, "page", 1, 1, 1e4)));
  params.set("number", String(boundedInt(number, "number", 10, 1, 100)));
  return params.toString();
}
async function redacted(result) {
  const value = await result;
  return value && typeof value === "object" ? redactObject(value) : value;
}
function h(cfg) {
  if (!cfg.videoSaId || !cfg.videoSaSecret)
    throw new Error("THETA_VIDEO_SA_ID / THETA_VIDEO_SA_SECRET missing");
  return { "x-tva-sa-id": cfg.videoSaId, "x-tva-sa-secret": cfg.videoSaSecret };
}
function net3(cfg, headers) {
  return {
    headers,
    service: "theta-video",
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
var thetaVideoClient = {
  createUploadSession: (cfg, confirm) => redacted(assertApproved(cfg, confirm, "theta.video.uploadCreate") ?? postJson(`${BASE}/upload`, {}, net3(cfg, h(cfg)))),
  createVideo: (cfg, payload, confirm) => redacted(assertApproved(cfg, confirm, "theta.video.create") ?? postJson(`${BASE}/video`, payload, net3(cfg, h(cfg)))),
  getVideo: (cfg, videoId) => redacted(getJson(`${BASE}/video/${pathSegment(videoId, "videoId")}`, net3(cfg, h(cfg)))),
  listVideos: (cfg, serviceAccountId, page = 1, number = 10) => redacted(getJson(`${BASE}/video/${pathSegment(serviceAccountId, "serviceAccountId")}/list?${new URLSearchParams({ page: String(page), number: String(number) })}`, net3(cfg, h(cfg)))),
  // Stream responses carry the livestream key; it is redacted here before returning.
  createStream: (cfg, payload, confirm) => redacted(assertApproved(cfg, confirm, "theta.video.streamCreate") ?? postJson(`${BASE}/stream`, payload, net3(cfg, h(cfg)))),
  getStream: (cfg, streamId) => redacted(getJson(`${BASE}/stream/${pathSegment(streamId, "streamId")}`, net3(cfg, h(cfg)))),
  searchVideos: (cfg, serviceAccountId, filters, operator, page, number) => {
    const query = videoSearchQuery(filters, operator, page, number);
    return redacted(getJson(`${BASE}/video/${pathSegment(serviceAccountId, "serviceAccountId")}/search?${query}`, net3(cfg, h(cfg))));
  },
  listStreams: (cfg, serviceAccountId, status) => {
    if (status !== void 0 && status !== "on" && status !== "off")
      throw new Error('status must be "on" or "off"');
    const query = status ? `?${new URLSearchParams({ status })}` : "";
    return redacted(getJson(`${BASE}/service_account/${pathSegment(serviceAccountId, "serviceAccountId")}/streams${query}`, net3(cfg, h(cfg))));
  },
  listIngestors: (cfg) => redacted(getJson(`${BASE}/ingestor/filter`, net3(cfg, h(cfg)))),
  selectIngestor: (cfg, ingestorId, body, confirm) => redacted(assertApproved(cfg, confirm, "theta.video.ingestorSelect") ?? putJson(`${BASE}/ingestor/${pathSegment(ingestorId, "ingestorId")}/select`, body, net3(cfg, h(cfg)))),
  // Frees the ingestor and invalidates the live stream key. Body is always exactly {}.
  unselectIngestor: (cfg, ingestorId, confirm) => redacted(assertApproved(cfg, confirm, "theta.video.ingestorUnselect") ?? putJson(`${BASE}/ingestor/${pathSegment(ingestorId, "ingestorId")}/unselect`, {}, net3(cfg, h(cfg))))
};

// build/commands/video.js
var video = {
  uploadCreate: (cfg, confirm) => cfg.dryRun ? { dryRun: true } : thetaVideoClient.createUploadSession(cfg, confirm),
  videoCreate: (cfg, payload, confirm) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : thetaVideoClient.createVideo(cfg, payload, confirm),
  videoGet: (cfg, videoId) => thetaVideoClient.getVideo(cfg, videoId),
  videoList: (cfg, serviceAccountId, page = 1, number = 10) => thetaVideoClient.listVideos(cfg, serviceAccountId, page, number),
  streamCreate: (cfg, payload, confirm) => cfg.dryRun ? redactObject({ dryRun: true, payload }) : thetaVideoClient.createStream(cfg, payload, confirm),
  streamGet: (cfg, streamId) => thetaVideoClient.getStream(cfg, streamId),
  videoSearch: (cfg, serviceAccountId, filters, operator, page, number) => thetaVideoClient.searchVideos(cfg, serviceAccountId, filters, operator, page, number),
  streamList: (cfg, serviceAccountId, status) => thetaVideoClient.listStreams(cfg, serviceAccountId, status),
  ingestorList: (cfg) => thetaVideoClient.listIngestors(cfg),
  ingestorUnselect: (cfg, ingestorId, confirm) => cfg.dryRun ? { dryRun: true, method: "PUT", path: `/ingestor/${pathSegment(ingestorId, "ingestorId")}/unselect`, body: {} } : thetaVideoClient.unselectIngestor(cfg, ingestorId, confirm),
  ingestorSelect: (cfg, ingestorId, body, confirm) => cfg.dryRun ? redactObject({ dryRun: true, ingestorId, body }) : thetaVideoClient.selectIngestor(cfg, ingestorId, body, confirm)
};

// build/commands/ondemandCatalog.js
var ONDEMAND_CHAT_SERVICE_SLUGS = Object.freeze([
  "glm_5_2",
  "qwen3",
  "minimax_m2_5",
  "gpt_oss_120b",
  "llama_3_1_70b",
  "llama_3_8b",
  "glm_5_3",
  "glm_5_3_flash",
  "qwen3_8_max",
  "qwen3_8_flash",
  "ling_3_0_flash_fin"
]);
var OPENAI_CHAT_COMPLETION_SERVICES = Object.freeze([
  "gpt_oss_120b",
  "glm_5_3",
  "glm_5_3_flash",
  "qwen3_8_max",
  "qwen3_8_flash",
  "ling_3_0_flash_fin"
]);
var TOOL_CALLING_CHAT_SERVICES = Object.freeze(["glm_5_3", "glm_5_3_flash"]);
function isOnDemandChatService(slug) {
  return ONDEMAND_CHAT_SERVICE_SLUGS.includes(slug);
}
var ONDEMAND_SERVICE_CATALOG = {
  qwen3_8_max: { slug: "qwen3_8_max", name: "Qwen3.8-Max", category: "LLM", requiredInputFields: ["messages"], supportsInputPresignedUrls: false, defaultPrediction: "completions", inputSchemaKind: "chat_messages", pricingHint: "live list 2026-10-03: input=220/output=660 credits per 1M tokens (1 credit = USD 0.01)", notes: "OpenAI-compatible chat/completions. Optional enable_thinking. Tools are ignored; use GLM-5.3 for tool calls." },
  qwen3_8_flash: { slug: "qwen3_8_flash", name: "Qwen3.8-Flash", category: "LLM", requiredInputFields: ["messages"], supportsInputPresignedUrls: false, defaultPrediction: "completions", inputSchemaKind: "chat_messages", pricingHint: "live list 2026-10-03: input=17/output=52 credits per 1M tokens (1 credit = USD 0.01)", notes: "Cheapest live chat model. Optional enable_thinking. Tools are ignored." },
  ling_3_0_flash_fin: { slug: "ling_3_0_flash_fin", name: "Ling-3.0-flash-Fin", category: "LLM", requiredInputFields: ["messages"], supportsInputPresignedUrls: false, defaultPrediction: "completions", inputSchemaKind: "chat_messages", maxTokensDefault: 2048, contextWindow: 256e3, pricingHint: "live list 2026-10-03 shows 0/0; treat cost as UNKNOWN, not free", notes: "Finance model via ZAN Router. Writes reasoning into content; allow >=1024 max_tokens. Tools are ignored." },
  seedance_2_5: { slug: "seedance_2_5", name: "Seedance 2.5", category: "VideoGen", requiredInputFields: ["prompt"], supportsInputPresignedUrls: true, defaultPrediction: "default", inputSchemaKind: "service_specific", pricingHint: "live list: 1177 credits per 1M video tokens; resolution/reference multipliers apply", notes: 'BytePlus external route. duration 4-30 (MCP example of 1 is invalid), ratio 16:9|9:16|1:1, resolution 480p|720p|1080p, generate_audio, watermark, one reference_image_url/reference_video_url/reference_audio_url. 2026-10-03: API returned 503 "temporarily unavailable".' },
  glm_5_3: { slug: "glm_5_3", name: "GLM 5.3", category: "LLM", requiredInputFields: ["messages"], supportsInputPresignedUrls: false, defaultPrediction: "completions", inputSchemaKind: "chat_messages", notes: "Use OpenAI-compatible chat/completions for structured tools; discover live capacity before use." },
  glm_5_3_flash: { slug: "glm_5_3_flash", name: "GLM 5.3 Flash", category: "LLM", requiredInputFields: ["messages"], supportsInputPresignedUrls: false, defaultPrediction: "completions", inputSchemaKind: "chat_messages", notes: "Public catalog does not guarantee available workers." },
  image_to_image: { slug: "image_to_image", name: "Image to image", category: "ImageRestore", requiredInputFields: [], supportsInputPresignedUrls: true, inputSchemaKind: "service_specific", notes: "Discover prediction-specific required fields and variants live; do not assume one input contract." },
  glm_5_2: {
    slug: "glm_5_2",
    name: "GLM 5.2",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    variants: ["default"],
    maxTokensDefault: 5e3,
    contextWindow: 1e6,
    license: "MIT",
    pricingHint: "live list: input=154/output=484, divisor=1000000; raw split-price units, currency unverified",
    liveStatus: "live-public-2026-08-05",
    notes: "Canonical slug is glm_5_2. Live schema includes enable_thinking. Keep opt-in for bounded, verifiable worker tasks."
  },
  qwen3: {
    slug: "qwen3",
    name: "Qwen3",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    variants: ["default", "parallax_32b_fp8"],
    pricingHint: "live list: input=20/output=40 per 1M tokens; split pricing",
    liveStatus: "live-public-2026-05-26",
    notes: "Canonical slug is qwen3. Use input.messages chat-array payloads; capacity may return retriable 409 No instances available."
  },
  minimax_m2_5: {
    slug: "minimax_m2_5",
    name: "MiniMax M2.5",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    pricingHint: "live list: input=20/output=120 per 1M tokens; split pricing; context_length=196608",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26",
    notes: "Observed on 2026-04-25 but absent from the 2026-05-26 live public service list."
  },
  gpt_oss_120b: {
    slug: "gpt_oss_120b",
    name: "GPT OSS 120B",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    pricingHint: "live list: input=4/output=20 per 1M tokens; split pricing; context_length=131072",
    liveStatus: "live-public-2026-05-26"
  },
  flux: {
    slug: "flux",
    name: "FLUX",
    category: "ImageGen",
    requiredInputFields: ["prompt"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "generate_image",
    inputSchemaKind: "prompt",
    variants: ["default", "quantized"],
    observedUnitPriceUsd: "0.01 / image",
    liveStatus: "live-public-2026-05-26"
  },
  llama_3_1_70b: {
    slug: "llama_3_1_70b",
    name: "Llama 3.1 70B",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    variants: ["default", "quantized"],
    pricingHint: "live list: input=20/output=40 per 1M tokens; split pricing; context_length=131072",
    liveStatus: "live-public-2026-05-26",
    notes: "Observed occasional 409: No instances available."
  },
  llama_3_8b: {
    slug: "llama_3_8b",
    name: "Llama 3 8B",
    category: "LLM",
    requiredInputFields: ["messages"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "completions",
    inputSchemaKind: "chat_messages",
    variants: ["default", "quantized"],
    pricingHint: "live list: input=20/output=40 per 1M tokens; split pricing; context_length=8192",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26",
    notes: "Observed on 2026-04-25 but absent from the 2026-05-26 live public service list."
  },
  step_video: {
    slug: "step_video",
    name: "Step Video",
    category: "VideoGen",
    requiredInputFields: ["prompt"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "generate",
    inputSchemaKind: "prompt",
    observedUnitPriceUsd: "0.20 / video",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26",
    notes: "Often asynchronous and long-running. Observed on 2026-04-25 but absent from the 2026-05-26 live public service list."
  },
  grounding_dino: {
    slug: "grounding_dino",
    name: "Grounding Dino",
    category: "ObjectDetection",
    requiredInputFields: ["input_img", "detection_prompt"],
    supportsInputPresignedUrls: true,
    defaultPrediction: "0",
    inputSchemaKind: "file",
    observedUnitPriceUsd: "0.01 / image",
    liveStatus: "live-public-2026-05-26"
  },
  blip: {
    slug: "blip",
    name: "Blip",
    category: "ImageCaption",
    requiredInputFields: ["input_img"],
    supportsInputPresignedUrls: true,
    defaultPrediction: "predict",
    inputSchemaKind: "file",
    observedUnitPriceUsd: "0.01 / image",
    liveStatus: "live-public-2026-05-26",
    notes: "Prefer presigned upload to avoid external URL fetch failures."
  },
  whisper: {
    slug: "whisper",
    name: "Whisper",
    category: "SpeechRec",
    requiredInputFields: ["audio_filename"],
    supportsInputPresignedUrls: true,
    defaultPrediction: "stt",
    inputSchemaKind: "file",
    observedUnitPriceUsd: "low fractional / clip",
    liveStatus: "live-public-2026-05-26"
  },
  stable_diffusion_xl_turbo: {
    slug: "stable_diffusion_xl_turbo",
    name: "Stable Diffusion XL Turbo",
    category: "ImageGen",
    requiredInputFields: ["prompt"],
    supportsInputPresignedUrls: false,
    defaultPrediction: "predict",
    inputSchemaKind: "prompt",
    observedUnitPriceUsd: "0.01 / image",
    liveStatus: "live-public-2026-05-26"
  },
  llava: {
    slug: "llava",
    name: "LLaVA",
    category: "VisionLanguage",
    requiredInputFields: ["input_img", "question"],
    supportsInputPresignedUrls: true,
    defaultPrediction: "predict",
    inputSchemaKind: "image_question",
    variants: ["quantized"],
    observedUnitPriceUsd: "0.01 / image",
    liveStatus: "live-public-2026-05-26",
    notes: "Vision-language question answering over images."
  },
  esrgan: {
    slug: "esrgan",
    name: "ESRGAN",
    category: "ImageRestore",
    requiredInputFields: ["input_img"],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: "0.02 / image",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26"
  },
  voice_cloning: {
    slug: "voice_cloning",
    name: "Voice Cloning",
    category: "TextToSpeech",
    requiredInputFields: ["text", "language", "voice"],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: "0.01 / audio",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26"
  },
  instant_id: {
    slug: "instant_id",
    name: "Instant ID",
    category: "ImageGen",
    requiredInputFields: ["face_img", "prompt"],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: "0.24 / image",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26"
  },
  talking_head: {
    slug: "talking_head",
    name: "Talking Head",
    category: "VideoGen",
    requiredInputFields: ["img", "audio"],
    supportsInputPresignedUrls: true,
    observedUnitPriceUsd: "0.02 / video",
    liveStatus: "catalog-only-not-in-live-list-2026-05-26"
  }
};
var LIVE_SERVICES_2026_10_03 = Object.freeze([
  "ling_3_0_flash_fin",
  "qwen3_8_max",
  "qwen3_8_flash",
  "glm_5_3",
  "glm_5_3_flash",
  "qwen3",
  "seedance_2_5",
  "blip",
  "esrgan",
  "image_to_image",
  "stable_diffusion_xl_turbo",
  "llava",
  "whisper"
]);
for (const spec of Object.values(ONDEMAND_SERVICE_CATALOG)) {
  spec.liveStatus = LIVE_SERVICES_2026_10_03.includes(spec.slug) ? "live-public-2026-10-03" : "retired-not-in-live-list-2026-10-03";
}
var UNGATED_INFERENCE_SERVICES = Object.freeze([
  ...ONDEMAND_CHAT_SERVICE_SLUGS.filter((slug) => LIVE_SERVICES_2026_10_03.includes(slug)),
  "stable_diffusion_xl_turbo",
  "image_to_image",
  "esrgan",
  "blip",
  "llava",
  "whisper"
]);
function inferenceRequiresConfirm(service) {
  return !UNGATED_INFERENCE_SERVICES.includes(String(service ?? "").trim());
}
function listOnDemandServices() {
  return Object.values(ONDEMAND_SERVICE_CATALOG);
}

// build/clients/ondemandApi.js
var DEFAULT_BASE = "https://ondemand.thetaedgecloud.com";
var RETRIABLE_STATUS2 = /* @__PURE__ */ new Set([408, 425, 429, 500, 502, 503, 504]);
function baseUrl(cfg) {
  const raw = cfg.onDemandApiBaseUrl?.trim() || DEFAULT_BASE;
  return thetaUrl(raw, "ondemand");
}
function h2(cfg) {
  if (!cfg.onDemandApiToken)
    throw new Error("THETA_ONDEMAND_API_TOKEN missing");
  return {
    Authorization: `Bearer ${cfg.onDemandApiToken}`,
    "content-type": "application/json"
  };
}
function optionalHeaders(cfg) {
  return cfg.onDemandApiToken ? { Authorization: `Bearer ${cfg.onDemandApiToken}`, "content-type": "application/json" } : { "content-type": "application/json" };
}
function net4(cfg) {
  return {
    headers: h2(cfg),
    service: "theta-ondemand-api",
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
function optionalNet(cfg) {
  return {
    headers: optionalHeaders(cfg),
    service: "theta-ondemand-api",
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
function encodePathSegment(value, label) {
  return pathSegment(value, label);
}
function inferPath(service, opts = {}) {
  const params = new URLSearchParams();
  if (opts.wait !== void 0) {
    const wait = Number(opts.wait);
    params.set("wait", String(Number.isFinite(wait) ? Math.min(Math.max(Math.trunc(wait), 0), 60) : 30));
  }
  if (opts.prediction)
    params.set("prediction", opts.prediction);
  const query = params.toString();
  return `/infer_request/${encodePathSegment(service, "service")}${query ? `?${query}` : ""}`;
}
function chatCompletionsPath() {
  return "/infer_request/chat/completions";
}
function roundUpMs(value, bucketMs) {
  return Math.ceil(value / bucketMs) * bucketMs;
}
function readPositiveInt(value) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0)
    return void 0;
  return parsed;
}
function isTimeoutAbort(error) {
  if (!error || typeof error !== "object")
    return false;
  const err = error;
  const name = typeof err.name === "string" ? err.name : "";
  const message = typeof err.message === "string" ? err.message.toLowerCase() : "";
  return name === "TimeoutError" || name === "AbortError" || message.includes("operation was aborted") || message.includes("timeout");
}
function normalizeInferPayload(payload) {
  const sourceInput = payload.input;
  const input = sourceInput && typeof sourceInput === "object" && !Array.isArray(sourceInput) ? { ...sourceInput } : { ...payload };
  const normalized = sourceInput && typeof sourceInput === "object" && !Array.isArray(sourceInput) ? { ...payload, input } : { input };
  if (Array.isArray(input.messages) && input.stream === void 0) {
    input.stream = false;
  }
  return normalized;
}
function resolveStepVideoFrames(payload) {
  const input = payload.input && typeof payload.input === "object" && !Array.isArray(payload.input) ? payload.input : payload;
  return readPositiveInt(input.frames);
}
function resolveCreateInferTimeoutMs(cfg, service, payload) {
  if (service.trim().toLowerCase() === "step_video") {
    const frames = resolveStepVideoFrames(payload) ?? 30;
    const derivedMs = 12e4 + frames * 500;
    return Math.min(3e5, Math.max(cfg.httpTimeoutMs, roundUpMs(derivedMs, 5e3)));
  }
  const input = payload.input && typeof payload.input === "object" && !Array.isArray(payload.input) ? payload.input : payload;
  if (Array.isArray(input.messages)) {
    return Math.max(cfg.httpTimeoutMs, 12e4);
  }
  return cfg.httpTimeoutMs;
}
function parseSseResponse(text) {
  if (!/^data:/m.test(text))
    return void 0;
  let id;
  let model;
  let finishReason;
  let usage;
  let message = "";
  let reasoning = "";
  const toolCalls = /* @__PURE__ */ new Map();
  const chunks = [];
  let done = false;
  let malformed = false;
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith("data:"))
      continue;
    const data = line.slice("data:".length).trim();
    if (data === "[DONE]") {
      done = true;
      continue;
    }
    if (!data)
      continue;
    try {
      const chunk = JSON.parse(data);
      chunks.push(chunk);
      id = id ?? chunk.id;
      model = model ?? chunk.model;
      usage = chunk.usage ?? usage;
      const choice = Array.isArray(chunk.choices) ? chunk.choices[0] : void 0;
      finishReason = choice?.finish_reason ?? finishReason;
      const delta = choice?.delta && typeof choice.delta === "object" ? choice.delta : {};
      const messageObj = choice?.message && typeof choice.message === "object" ? choice.message : {};
      const content = delta.content ?? messageObj.content ?? choice?.text;
      const reasoningChunk = delta.reasoning_content ?? delta.reasoning ?? messageObj.reasoning_content ?? messageObj.reasoning;
      if (typeof content === "string")
        message += content;
      if (typeof reasoningChunk === "string")
        reasoning += reasoningChunk;
      const incoming = delta.tool_calls ?? messageObj.tool_calls;
      if (Array.isArray(incoming))
        for (const [position, part] of incoming.entries()) {
          const index = part.index ?? position;
          const current = toolCalls.get(index) ?? { type: "function", function: { name: "", arguments: "" } };
          if (part.id)
            current.id = part.id;
          if (part.type)
            current.type = part.type;
          if (part.function?.name)
            current.function.name += part.function.name;
          if (part.function?.arguments)
            current.function.arguments += part.function.arguments;
          toolCalls.set(index, current);
        }
    } catch {
      malformed = true;
    }
  }
  if (malformed || !chunks.length || !done && !finishReason)
    throw new Error("Malformed or incomplete Theta event stream");
  return {
    status: "success",
    body: {
      stream: true,
      infer_requests: [
        {
          id: id ?? "streaming-response",
          state: "success",
          output: { message, ...toolCalls.size ? { tool_calls: [...toolCalls.entries()].sort(([a], [b]) => a - b).map(([, call]) => call) } : {} },
          model,
          finish_reason: finishReason,
          usage,
          metadata: {
            reasoning,
            reasoning_length: reasoning.length,
            content_length: message.length
          },
          chunks
        }
      ]
    }
  };
}
function normalizeChatCompletionsJson(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const choices = Array.isArray(body.choices) ? body.choices : [];
  const firstChoice = choices[0] && typeof choices[0] === "object" ? choices[0] : {};
  const messageObj = firstChoice.message && typeof firstChoice.message === "object" ? firstChoice.message : {};
  const message = typeof messageObj.content === "string" ? messageObj.content : typeof firstChoice.text === "string" ? firstChoice.text : null;
  const reasoning = typeof messageObj.reasoning_content === "string" ? messageObj.reasoning_content : typeof messageObj.reasoning === "string" ? messageObj.reasoning : typeof firstChoice.reasoning === "string" ? firstChoice.reasoning : "";
  const usage = body.usage && typeof body.usage === "object" ? { ...body.usage } : body.usage;
  return {
    status: "success",
    body: {
      chat_completions: body,
      infer_requests: [
        {
          id: body.id ?? "chat-completions-response",
          state: "success",
          output: { message, ...Array.isArray(messageObj.tool_calls) ? { tool_calls: messageObj.tool_calls } : {} },
          model: body.model,
          finish_reason: firstChoice.finish_reason,
          usage,
          metadata: {
            reasoning,
            reasoning_length: reasoning.length,
            content_length: typeof message === "string" ? message.length : 0
          }
        }
      ]
    }
  };
}
async function postJsonOrSse(cfg, url2, body, timeoutMs) {
  for (let attempt = 0; attempt < 1; attempt += 1) {
    const canRetry = false;
    try {
      const res = await fetch(url2, {
        redirect: "error",
        method: "POST",
        headers: h2(cfg),
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(timeoutMs)
      });
      const text = await res.text();
      if (!res.ok) {
        if (canRetry && (RETRIABLE_STATUS2.has(res.status) || isRetriableHttpError(res.status, text))) {
          await sleep4(backoffDelayMs2(attempt + 1, cfg.httpRetryBackoffMs));
          continue;
        }
        throw fromHttpError("theta-ondemand-api", url2, res.status, text);
      }
      const unreadable = () => ({
        code: "THETA_ONDEMAND_MALFORMED_STREAM",
        message: "Malformed or incomplete Theta event stream (the request may already have been billed; it was not retried)",
        retriable: false,
        service: "theta-ondemand-api",
        endpoint: url2,
        status: res.status
      });
      try {
        return JSON.parse(text);
      } catch {
        let parsedSse;
        try {
          parsedSse = parseSseResponse(text);
        } catch {
          throw unreadable();
        }
        if (parsedSse)
          return parsedSse;
        const contentType = res.headers.get("content-type") ?? "";
        if (/event-stream/i.test(contentType) || /^\s*data\s*:/m.test(text))
          throw unreadable();
        return { status: "success", raw: text };
      }
    } catch (error) {
      if (isStructuredError(error))
        throw error;
      if (isTimeoutAbort(error)) {
        throw fromTransportError("theta-ondemand-api", url2, error);
      }
      if (canRetry) {
        await sleep4(backoffDelayMs2(attempt + 1, cfg.httpRetryBackoffMs));
        continue;
      }
      throw fromTransportError("theta-ondemand-api", url2, error);
    }
  }
  throw fromTransportError("theta-ondemand-api", url2, new Error("HTTP request failed after retries"));
}
function backoffDelayMs2(attempt, baseMs) {
  return baseMs * Math.max(1, 2 ** (attempt - 1));
}
var sleep4 = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function enforceWebhookGate(cfg, body, confirm) {
  const hooks = findCallbackFields(body);
  for (const hook of hooks) {
    let url2;
    try {
      url2 = new URL(String(hook.value));
    } catch {
      throw new Error(`${hook.path} must be an https URL`);
    }
    if (url2.protocol !== "https:")
      throw new Error(`${hook.path} must be an https URL`);
  }
  if (hooks.length)
    assertApproved(cfg, confirm, "Sending inference results to a webhook");
}
var PREDICTION_NAME = /^[A-Za-z0-9_.-]{1,64}$/;
function enforceToolSupport(model, body, allowUnverifiedTools) {
  const input = body.input && typeof body.input === "object" ? body.input : {};
  const hasTools = ["tools", "tool_choice", "functions"].some((k2) => body[k2] !== void 0 || input[k2] !== void 0);
  if (hasTools && !TOOL_CALLING_CHAT_SERVICES.includes(model) && allowUnverifiedTools !== true) {
    throw new Error(`Service ${model} does not return structured tool calls. Use glm_5_3 or glm_5_3_flash, or set allowUnverifiedTools:true (exactly) to send anyway.`);
  }
}
var onDemandApiClient = {
  listServices: (cfg) => getJson(`${baseUrl(cfg)}/service/list?expand=template_id`, optionalNet(cfg)),
  createInferRequest: (cfg, service, payload, opts) => {
    assertLive(cfg, "On-demand inference");
    encodePathSegment(service, "service");
    if (opts?.prediction !== void 0 && (typeof opts.prediction !== "string" || !PREDICTION_NAME.test(opts.prediction))) {
      throw new Error("prediction must be a prediction name string");
    }
    if (opts?.wait !== void 0 && !Number.isFinite(Number(opts.wait)))
      throw new Error("wait must be a number");
    const raw = normalizeInferPayload(snapshotBody(payload));
    const bounded = raw.input && typeof raw.input === "object" && !Array.isArray(raw.input) ? { ...boundChatParams(raw), input: boundChatParams(raw.input) } : boundChatParams(raw);
    const finalBody = opts?.prediction && bounded.prediction === void 0 ? { ...bounded, prediction: opts.prediction } : bounded;
    if (finalBody.prediction !== void 0 && (typeof finalBody.prediction !== "string" || !PREDICTION_NAME.test(finalBody.prediction))) {
      throw new Error("prediction must be a prediction name string");
    }
    if (inferenceRequiresConfirm(service))
      assertApproved(cfg, opts?.confirm, `Inference on ${service} (video, unknown, retired or high-cost service)`);
    enforceWebhookGate(cfg, finalBody, opts?.confirm);
    enforceToolSupport(service, finalBody, opts?.allowUnverifiedTools);
    const timeoutMs = resolveCreateInferTimeoutMs(cfg, service, finalBody);
    return postJsonOrSse(cfg, `${baseUrl(cfg)}${inferPath(service, { wait: opts?.wait, prediction: opts?.prediction })}`, finalBody, timeoutMs);
  },
  createChatCompletionRequest: async (cfg, rawBody, opts) => {
    assertLive(cfg, "On-demand chat completion");
    const snapshot = snapshotBody(rawBody);
    const body = snapshot.input && typeof snapshot.input === "object" && !Array.isArray(snapshot.input) ? { ...boundChatParams(snapshot), input: boundChatParams(snapshot.input) } : boundChatParams(snapshot);
    if (!Array.isArray(body.messages) || !body.messages.length)
      throw new Error("messages must be a non-empty array");
    const model = String(body.model);
    if (!OPENAI_CHAT_COMPLETION_SERVICES.includes(model) || inferenceRequiresConfirm(model)) {
      assertApproved(cfg, opts?.confirm, `Chat completion on retired or unlisted model ${model}`);
    }
    enforceWebhookGate(cfg, body, opts?.confirm);
    enforceToolSupport(model, body, opts?.allowUnverifiedTools);
    const timeoutMs = Array.isArray(body.messages) && body.stream === false ? Math.max(cfg.httpTimeoutMs, 12e4) : cfg.httpTimeoutMs;
    const result = await postJsonOrSse(cfg, `${baseUrl(cfg)}${chatCompletionsPath()}`, body, timeoutMs);
    if (result && typeof result === "object" && result.body)
      return result;
    return normalizeChatCompletionsJson(result);
  },
  getInferRequest: (cfg, requestId) => getJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(requestId, "requestId")}`, net4(cfg)),
  createInputPresignedUrls: async (cfg, service, inputFields) => {
    assertLive(cfg, "Presigned upload URL creation");
    return normalizePresignedUrls(await postJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(service, "service")}/input_presigned_urls`, inputFields?.length ? { input_fields: inputFields } : {}, net4(cfg)));
  }
};
var PRESIGNED_UPLOAD_CONTENT_TYPE = "application/octet-stream";
function normalizePresignedUrls(response) {
  if (!response || typeof response !== "object")
    return response;
  const body = response.body;
  if (!body || typeof body !== "object")
    return response;
  const source = body.urls && typeof body.urls === "object" ? body.urls : body;
  const uploads = {};
  for (const [field, raw] of Object.entries(source)) {
    if (!raw || typeof raw !== "object")
      continue;
    const info = raw;
    const uploadUrl = info.presigned_url ?? info.upload_url;
    if (typeof uploadUrl === "string" && /^https:\/\//i.test(uploadUrl) && typeof info.filename === "string") {
      uploads[field] = { upload_url: uploadUrl, filename: info.filename };
    }
  }
  return {
    ...response,
    uploads,
    uploadInstructions: `PUT the file bytes to upload_url with header Content-Type: ${PRESIGNED_UPLOAD_CONTENT_TYPE} (any other type fails signature check with 403), then pass filename as the input field value.`
  };
}

// build/commands/ondemand.js
function getFirstInferRequest(payload) {
  if (!payload || typeof payload !== "object")
    return void 0;
  const body = payload.body;
  if (!body?.infer_requests?.length)
    return void 0;
  return body.infer_requests[0];
}
function isTerminal(state) {
  return state === "success" || state === "error" || state === "failed" || state === "cancelled";
}
function clampInt3(value, fallback, min, max) {
  if (!Number.isFinite(value))
    return fallback;
  return Math.min(Math.max(Math.trunc(value), min), max);
}
function clampFloat(value, fallback, min, max) {
  if (!Number.isFinite(value))
    return fallback;
  return Math.min(Math.max(value, min), max);
}
function roundUpMs2(value, bucketMs) {
  return Math.ceil(value / bucketMs) * bucketMs;
}
function readPositiveInt2(value) {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0)
    return void 0;
  return parsed;
}
function deriveAdaptivePollTimeoutMs(inferRequest) {
  const input = inferRequest?.input;
  if (!input || typeof input !== "object")
    return void 0;
  const frames = readPositiveInt2(input.frames);
  if (!frames)
    return void 0;
  const fps = readPositiveInt2(input.fps) ?? 10;
  const renderSeconds = Math.max(1, Math.ceil(frames / Math.max(1, fps)));
  const queueAndVarianceBufferMs = 24e4;
  const frameScaledMs = frames * 4e3;
  const durationScaledMs = renderSeconds * 6e4;
  const derivedMs = queueAndVarianceBufferMs + Math.max(frameScaledMs, durationScaledMs);
  const roundedMs = roundUpMs2(derivedMs, 3e4);
  return Math.min(18e5, Math.max(36e4, roundedMs));
}
function errorSummary(error) {
  if (isStructuredError(error)) {
    return {
      code: error.code,
      message: error.message,
      retriable: error.retriable,
      status: error.status,
      service: error.service
    };
  }
  const asError = error;
  return {
    code: asError?.name ?? "ERROR",
    message: asError?.message ?? String(error ?? "Unknown error")
  };
}
function normalizeMessages(messages) {
  if (!Array.isArray(messages) || messages.length === 0) {
    throw new Error("messages must be a non-empty array");
  }
  return messages.map((message, index) => {
    if (!message || typeof message !== "object") {
      throw new Error(`messages[${index}] must be an object`);
    }
    if (typeof message.role !== "string" || !message.role.trim()) {
      throw new Error(`messages[${index}].role must be a non-empty string`);
    }
    const toolOnly = message.role === "assistant" && Array.isArray(message.tool_calls) && message.tool_calls.length > 0;
    if ((typeof message.content !== "string" || !message.content.trim()) && !toolOnly) {
      throw new Error(`messages[${index}].content must be a non-empty string`);
    }
    if (message.role === "tool" && !message.tool_call_id?.trim())
      throw new Error(`messages[${index}].tool_call_id is required`);
    return {
      role: message.role.trim(),
      content: message.content,
      ...message.tool_calls ? { tool_calls: message.tool_calls } : {},
      ...message.tool_call_id ? { tool_call_id: message.tool_call_id } : {}
    };
  });
}
function resolveDefaultMaxTokens(service) {
  if (service === "gpt_oss_120b")
    return 1800;
  if (service === "ling_3_0_flash_fin")
    return 2048;
  return 500;
}
function buildChatPayload(messages, opts = {}, service) {
  const permittedExtra = /* @__PURE__ */ new Set(["stop", "seed", "presence_penalty", "frequency_penalty", "response_format", "top_k", "reasoning_effort", "enable_thinking", "variant", "style_image_filename", "image_filename", "input_img", "frames", "fps", "duration", "ratio", "resolution", "reference_image_url", "reference_video_url", "reference_audio_url", "generate_audio", "watermark", "audio_filename", "detection_prompt", "question", "prompt", "filename", "strength", "guidance_scale", "negative_prompt"]);
  const safeExtra = Object.fromEntries(Object.entries(opts.extraInput ?? {}).filter(([key]) => permittedExtra.has(key)));
  const input = {
    ...safeExtra,
    messages: normalizeMessages(messages),
    max_tokens: clampInt3(opts.maxTokens, resolveDefaultMaxTokens(service), 1, 5e3),
    temperature: clampFloat(opts.temperature, 0.5, 0, 2),
    top_p: clampFloat(opts.topP, 0.7, 0, 1),
    stream: opts.stream ?? false
  };
  if (opts.reasoningEffort !== void 0) {
    input.reasoning_effort = opts.reasoningEffort;
  }
  if (opts.enableThinking !== void 0) {
    input.enable_thinking = opts.enableThinking;
  }
  if (opts.tools !== void 0)
    input.tools = opts.tools;
  if (opts.toolChoice !== void 0)
    input.tool_choice = opts.toolChoice;
  if (opts.parallelToolCalls !== void 0)
    input.parallel_tool_calls = opts.parallelToolCalls;
  const payload = { input: boundChatParams(input, resolveDefaultMaxTokens(service)) };
  if (opts.variant)
    payload.variant = opts.variant;
  if (opts.webhook)
    payload.webhook = opts.webhook;
  const requestOptions = {
    wait: clampInt3(opts.wait, 30, 0, 60),
    prediction: opts.prediction ?? "completions"
  };
  return { payload, requestOptions };
}
function summarizeLiveService(service) {
  const predictions = service.predictions && typeof service.predictions === "object" ? service.predictions : {};
  const defaultPrediction = typeof service.default_prediction === "string" ? service.default_prediction : Object.keys(predictions)[0];
  const prediction = defaultPrediction ? predictions[defaultPrediction] : void 0;
  const inputVars = prediction?.input_vars && typeof prediction.input_vars === "object" ? prediction.input_vars : void 0;
  return {
    source: "live",
    alias: service.alias,
    name: service.name,
    category: categorizeOnDemandService(service),
    state: service.state,
    workloadType: service.workload_type,
    rank: service.rank,
    defaultPrediction,
    inputFields: inputVars ? Object.keys(inputVars) : [],
    inputExample: inputVars ? buildInputExample(inputVars) : {},
    variants: prediction?.variants,
    workers: service.workers,
    updateTime: service.update_time,
    pricing: prediction?.instructions,
    inputSchema: inputVars,
    predictions,
    openrouter: prediction?.openrouter_metadata
  };
}
function normalizeCategory(value) {
  if (typeof value !== "string")
    return void 0;
  const normalized = value.trim().toLowerCase();
  return normalized || void 0;
}
function categorizeOnDemandService(service) {
  const alias = typeof service.alias === "string" ? service.alias.toLowerCase() : "";
  const name = typeof service.name === "string" ? service.name.toLowerCase() : "";
  const text = `${alias} ${name}`;
  if (text.includes("whisper") || text.includes("audio") || text.includes("voice"))
    return "audio";
  if (text.includes("video") || text.includes("talking_head"))
    return "video";
  if (text.includes("llava") || text.includes("vision"))
    return "vision";
  if (text.includes("blip") || text.includes("grounding") || text.includes("dino"))
    return "vision";
  if (text.includes("flux") || text.includes("stable") || text.includes("sdxl") || text.includes("image") || text.includes("upscale") || text.includes("esrgan"))
    return "image";
  if (text.includes("glm") || text.includes("qwen") || text.includes("gpt") || text.includes("llama") || text.includes("mistral") || text.includes("chat"))
    return "text";
  return "other";
}
function categorizeCatalogService(service) {
  const category = service.category.toLowerCase();
  if (category.includes("speech") || category.includes("audio") || category.includes("voice"))
    return "audio";
  if (category.includes("video"))
    return "video";
  if (category.includes("vision") || category.includes("caption") || category.includes("detection"))
    return "vision";
  if (category.includes("image"))
    return "image";
  if (category.includes("llm") || category.includes("text"))
    return "text";
  return "other";
}
function buildInputExample(inputVars) {
  const example = {};
  for (const [field, rawSpec] of Object.entries(inputVars)) {
    const spec = rawSpec && typeof rawSpec === "object" ? rawSpec : {};
    const defaultValue = spec.default_value ?? spec.default;
    const type = typeof spec.type === "string" ? spec.type : "";
    if (defaultValue !== void 0) {
      example[field] = defaultValue;
    } else if (field === "messages" || type === "chat_array") {
      example[field] = [{ role: "user", content: "Hello" }];
    } else if (field.includes("filename") || field.includes("input_img") || type === "filename") {
      example[field] = "<filename from get_upload_url>";
    } else if (field === "prompt") {
      example[field] = "Your prompt here";
    } else if (type === "integer" || type === "number" || type === "float") {
      example[field] = 1;
    } else if (type === "bool" || type === "boolean") {
      example[field] = false;
    } else {
      example[field] = "string value";
    }
  }
  return example;
}
function filterLiveSummaries(services, opts = {}) {
  const category = normalizeCategory(opts.category);
  return services.map(summarizeLiveService).filter((service) => !category || service.category === category);
}
function filterCatalogServices(opts = {}) {
  const category = normalizeCategory(opts.category);
  return listOnDemandServices().filter((service) => !category || categorizeCatalogService(service) === category).map((service) => ({
    ...service,
    normalizedCategory: categorizeCatalogService(service)
  }));
}
var sleep5 = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
var ondemand = {
  catalog: ONDEMAND_SERVICE_CATALOG,
  listServices: (opts = {}) => filterCatalogServices(opts),
  listLiveServices: async (cfg, opts = {}) => {
    try {
      const response = await onDemandApiClient.listServices(cfg);
      const live = response.body?.services ?? [];
      return {
        source: "live",
        category: normalizeCategory(opts.category),
        services: filterLiveSummaries(live, opts),
        catalogFallbackAvailable: true
      };
    } catch (error) {
      return {
        source: "catalog",
        category: normalizeCategory(opts.category),
        warning: "Live service discovery failed; returning bundled catalog fallback.",
        error: errorSummary(error),
        services: filterCatalogServices(opts)
      };
    }
  },
  // Sends the payload to Theta on-demand inference (billable). The client enforces the approval
  // allowlist (video/unknown services and webhooks need confirm:true) and chat token bounds.
  infer: (cfg, service, payload, opts) => cfg.dryRun ? { dryRun: true, service, payload: payload?.input && typeof payload.input === "object" && !Array.isArray(payload.input) ? { ...payload, input: boundChatParams(payload.input) } : payload, requestOptions: opts } : onDemandApiClient.createInferRequest(cfg, service, payload, opts),
  chat: (cfg, service, messages, opts = {}) => {
    if (!opts.allowUnknownService && !isOnDemandChatService(service)) {
      throw new Error(`Unsupported on-demand chat service: ${service}. Known chat services: ${ONDEMAND_CHAT_SERVICE_SLUGS.join(", ")}`);
    }
    if (opts.tools?.length && opts.allowUnverifiedTools !== true && !TOOL_CALLING_CHAT_SERVICES.includes(service)) {
      throw new Error(`Service ${service} does not return structured tool calls (live-verified 2026-10-03). Use ${TOOL_CALLING_CHAT_SERVICES.join(" or ")} for tool use, or set allowUnverifiedTools:true (exactly) to send anyway.`);
    }
    const effectiveOpts = service === "qwen3" ? { ...opts, stream: opts.stream ?? true, wait: opts.wait ?? 60 } : ["gpt_oss_120b", "glm_5_3", "glm_5_3_flash"].includes(service) ? { ...opts, reasoningEffort: opts.reasoningEffort ?? "low" } : opts;
    const { payload, requestOptions } = buildChatPayload(messages, effectiveOpts, service);
    if (OPENAI_CHAT_COMPLETION_SERVICES.includes(service)) {
      const input = payload.input;
      const body = {
        ...input,
        model: service
      };
      return cfg.dryRun ? { dryRun: true, service, endpoint: "chat/completions", payload: body } : onDemandApiClient.createChatCompletionRequest(cfg, body, { confirm: opts.confirm, allowUnverifiedTools: opts.allowUnverifiedTools === true });
    }
    return cfg.dryRun ? { dryRun: true, service, payload, requestOptions } : onDemandApiClient.createInferRequest(cfg, service, payload, { ...requestOptions, confirm: opts.confirm, allowUnverifiedTools: opts.allowUnverifiedTools === true });
  },
  status: (cfg, requestId) => onDemandApiClient.getInferRequest(cfg, requestId),
  inputPresignedUrls: (cfg, service, inputFields) => cfg.dryRun ? { dryRun: true, service, inputFields } : onDemandApiClient.createInputPresignedUrls(cfg, service, inputFields),
  pollUntilDone: async (cfg, requestId, opts = {}) => {
    if (!requestId)
      throw new Error("requestId is required");
    const intervalMs = clampInt3(opts.intervalMs, 3e3, 100, 6e4);
    const explicitTimeoutMs = opts.timeoutMs === void 0 ? void 0 : clampInt3(opts.timeoutMs, 12e4, 1e3, 36e5);
    let timeoutMs = explicitTimeoutMs ?? 12e4;
    const maxAttempts = clampInt3(opts.maxAttempts, 1e3, 1, 2e4);
    const startedAt = Date.now();
    let attempts = 0;
    let lastResult;
    while (attempts < maxAttempts) {
      const elapsedBeforeRequest = Date.now() - startedAt;
      if (elapsedBeforeRequest >= timeoutMs) {
        return {
          attempts,
          elapsedMs: elapsedBeforeRequest,
          terminalState: "timeout",
          result: lastResult
        };
      }
      attempts += 1;
      const result = await onDemandApiClient.getInferRequest(cfg, requestId);
      lastResult = result;
      const inferRequest = getFirstInferRequest(result);
      if (explicitTimeoutMs === void 0) {
        const adaptiveTimeoutMs = deriveAdaptivePollTimeoutMs(inferRequest);
        if (adaptiveTimeoutMs !== void 0)
          timeoutMs = adaptiveTimeoutMs;
      }
      if (isTerminal(inferRequest?.state)) {
        return {
          attempts,
          elapsedMs: Date.now() - startedAt,
          terminalState: inferRequest?.state,
          result
        };
      }
      const elapsedAfterRequest = Date.now() - startedAt;
      if (elapsedAfterRequest >= timeoutMs) {
        return {
          attempts,
          elapsedMs: elapsedAfterRequest,
          terminalState: "timeout",
          result
        };
      }
      const sleepMs = Math.min(intervalMs, Math.max(0, timeoutMs - elapsedAfterRequest));
      if (sleepMs > 0)
        await sleep5(sleepMs);
    }
    return {
      attempts,
      elapsedMs: Date.now() - startedAt,
      terminalState: "max-attempts",
      result: lastResult
    };
  }
};

// build/commands/health.js
async function healthCheck(cfg) {
  const vm = await edgecloudControllerClient.listVmTypes(cfg);
  return {
    ok: true,
    vmCount: Array.isArray(vm?.body?.vms) ? vm.body.vms.length : void 0,
    timestamp: (/* @__PURE__ */ new Date()).toISOString()
  };
}

// build/clients/edgecloudMcp.js
var THETA_MCP_ENDPOINT = "https://controller.thetaedgecloud.com/mcp";
var requestSeq = 0;
function projectKey(cfg) {
  if (!cfg.edgecloudApiKey)
    throw new Error("THETA_EC_API_KEY missing (project-scoped EdgeCloud API key)");
  return cfg.edgecloudApiKey;
}
function parseRpcEnvelope(text, contentType) {
  if (contentType.includes("text/event-stream")) {
    const data = text.split(/\r?\n/).filter((line) => line.startsWith("data:")).map((line) => line.slice(5).trim()).filter(Boolean);
    for (let i = data.length - 1; i >= 0; i -= 1) {
      const parsed = JSON.parse(data[i]);
      if ("result" in parsed || "error" in parsed)
        return parsed;
    }
    throw new Error("Theta MCP stream ended without a JSON-RPC result");
  }
  return JSON.parse(text);
}
function decodeToolResult(name, result) {
  const content = Array.isArray(result.content) ? result.content : [];
  const texts = content.filter((item) => item.type === "text" && typeof item.text === "string").map((item) => item.text);
  const joined = texts.join("\n");
  if (result.isError)
    throw new Error(`Theta MCP ${name} failed: ${sanitizeHttpErrorMessage(joined).slice(0, 300) || "unknown error"}`);
  if (result.structuredContent !== void 0)
    return result.structuredContent;
  try {
    return JSON.parse(joined);
  } catch {
    return { text: joined };
  }
}
async function enforceGpuPriceCap(cfg, args) {
  const cap = Number(args.max_price_per_hour_usd);
  if (typeof args.max_price_per_hour_usd !== "number" || !Number.isFinite(cap) || cap <= 0) {
    throw new Error("create_gpu_deployment requires max_price_per_hour_usd (a positive hourly price cap)");
  }
  if (typeof args.resource_id !== "string" || !args.resource_id.trim())
    throw new Error("create_gpu_deployment requires resource_id");
  const lookup = await callThetaMcpTool(cfg, "get_gpu_resource", { project_id: args.project_id, resource_id: args.resource_id, region: args.region });
  const price = lookup?.price_per_hour_usd ?? lookup?.resource?.price_per_hour_usd;
  if (typeof price !== "number" || !Number.isFinite(price))
    throw new Error(`Could not verify the listed price of ${args.resource_id}; not provisioning`);
  if (price > cap)
    throw new Error(`Resource ${args.resource_id} lists USD ${price}/h, above the approved cap of USD ${cap}/h`);
}
var READ_ONLY_TOOLS = /* @__PURE__ */ new Set([
  "list_gpu_resources",
  "get_gpu_resource",
  "list_gpu_deployment_templates",
  "list_gpu_deployments",
  "get_gpu_deployment",
  "get_gpu_deployment_events",
  "get_gpu_deployment_logs",
  "get_billing_balance",
  "get_billing_usage",
  "list_billing_top_ups",
  "get_billing_pricing"
]);
var MUTATING_TOOLS = /* @__PURE__ */ new Set(["create_gpu_deployment", "start_gpu_deployment", "stop_gpu_deployment", "delete_gpu_deployment"]);
async function callThetaMcpTool(cfg, name, rawArgs) {
  const args = snapshotBody(rawArgs ?? {});
  if (!READ_ONLY_TOOLS.has(name)) {
    if (!MUTATING_TOOLS.has(name))
      throw new Error(`Theta MCP tool ${name} is not supported by this skill`);
    assertApproved(cfg, args.confirm, `Theta MCP ${name}`);
    if (name === "create_gpu_deployment")
      await enforceGpuPriceCap(cfg, args);
  }
  requestSeq += 1;
  const body = JSON.stringify({ jsonrpc: "2.0", id: requestSeq, method: "tools/call", params: { name, arguments: args } });
  let res;
  try {
    res = await fetch(THETA_MCP_ENDPOINT, {
      method: "POST",
      redirect: "error",
      headers: {
        "x-api-key": projectKey(cfg),
        "content-type": "application/json",
        accept: "application/json, text/event-stream"
      },
      body,
      signal: AbortSignal.timeout(cfg.httpTimeoutMs)
    });
  } catch (error) {
    throw fromTransportError("edgecloud-mcp", THETA_MCP_ENDPOINT, error);
  }
  const text = await res.text();
  if (!res.ok)
    throw fromHttpError("edgecloud-mcp", THETA_MCP_ENDPOINT, res.status, text);
  const envelope = parseRpcEnvelope(text, res.headers.get("content-type") ?? "");
  if (envelope.error) {
    const err = envelope.error;
    throw new Error(`Theta MCP ${name} JSON-RPC error ${err.code ?? ""}: ${sanitizeHttpErrorMessage(String(err.message ?? "unknown")).slice(0, 300)}`);
  }
  return decodeToolResult(name, envelope.result ?? {});
}

// build/commands/gpu.js
function withProject(projectId, args = {}) {
  const out = { project_id: projectId };
  for (const [key, value] of Object.entries(args))
    if (value !== void 0 && value !== null && value !== "")
      out[key] = value;
  return out;
}
function requireConfirm(action, confirm) {
  if (confirm !== true) {
    throw new Error(`${action} changes billable GPU capacity. State the price, get explicit approval, then pass confirm:true.`);
  }
}
function filterResources(resources, filter) {
  const model = filter.gpuModel?.toLowerCase();
  const region = filter.region?.toLowerCase();
  const filtered = resources.filter((r) => (!filter.provider || r.provider === filter.provider) && (!model || String(r.gpu_model ?? "").toLowerCase().includes(model)) && (!region || `${r.country ?? ""} ${r.region ?? ""}`.toLowerCase().includes(region)) && (filter.maxPricePerHourUsd === void 0 || typeof r.price_per_hour_usd === "number" && r.price_per_hour_usd <= filter.maxPricePerHourUsd) && (!filter.availableOnly || (r.gpu_count_available ?? 0) > 0));
  filtered.sort((a, b) => (a.price_per_hour_usd ?? Infinity) - (b.price_per_hour_usd ?? Infinity));
  return filter.limit ? filtered.slice(0, Math.max(1, Math.trunc(filter.limit))) : filtered;
}
function mutationPreview(tool, args) {
  return { dryRun: true, transport: "theta-hosted-mcp", tool, arguments: args };
}
var gpu = {
  listResources: async (cfg, projectId, filter = {}) => {
    const result = await callThetaMcpTool(cfg, "list_gpu_resources", withProject(projectId));
    const all = Array.isArray(result?.resources) ? result.resources : [];
    const resources = filterResources(all, filter);
    return { ...result, totalResources: all.length, matchedResources: resources.length, resources, priceCurrency: "USD per hour" };
  },
  getResource: (cfg, projectId, resourceId, region) => callThetaMcpTool(cfg, "get_gpu_resource", withProject(projectId, { resource_id: resourceId, region })),
  listTemplates: (cfg, projectId) => callThetaMcpTool(cfg, "list_gpu_deployment_templates", withProject(projectId)),
  listDeployments: (cfg, projectId) => callThetaMcpTool(cfg, "list_gpu_deployments", withProject(projectId)),
  getDeployment: (cfg, projectId, deploymentId) => callThetaMcpTool(cfg, "get_gpu_deployment", withProject(projectId, { deployment_id: deploymentId })),
  deploymentEvents: (cfg, projectId, deploymentId) => callThetaMcpTool(cfg, "get_gpu_deployment_events", withProject(projectId, { deployment_id: deploymentId })),
  deploymentLogs: (cfg, projectId, deploymentId) => callThetaMcpTool(cfg, "get_gpu_deployment_logs", withProject(projectId, { deployment_id: deploymentId })),
  createDeployment: async (cfg, projectId, req) => {
    if (!Number.isFinite(req.maxPricePerHourUsd) || req.maxPricePerHourUsd <= 0) {
      throw new Error("maxPricePerHourUsd is required: it is sent as Theta's provider-side hourly price cap");
    }
    const args = withProject(projectId, {
      name: req.name,
      display_name: req.displayName,
      deployment_template_id: req.deploymentTemplateId,
      resource_id: req.resourceId,
      region: req.region,
      container_image: req.containerImage,
      ssh_public_key: req.sshPublicKey,
      ssh_port: req.sshPort,
      http_port: req.httpPort,
      max_price_per_hour_usd: req.maxPricePerHourUsd,
      confirm: req.confirm === true
    });
    if (cfg.dryRun)
      return mutationPreview("create_gpu_deployment", args);
    requireConfirm("create_gpu_deployment", req.confirm);
    return callThetaMcpTool(cfg, "create_gpu_deployment", args);
  },
  lifecycle: async (cfg, projectId, action, deploymentId, confirm) => {
    const tool = `${action}_gpu_deployment`;
    const args = withProject(projectId, { deployment_id: deploymentId, confirm: confirm === true });
    if (cfg.dryRun)
      return mutationPreview(tool, args);
    requireConfirm(tool, confirm);
    return callThetaMcpTool(cfg, tool, args);
  }
};
var billing = {
  balanceUsd: (cfg, projectId) => callThetaMcpTool(cfg, "get_billing_balance", withProject(projectId)),
  usage: (cfg, projectId, startDate, endDate) => {
    const parse = (label, value) => {
      if (value === void 0)
        return void 0;
      const ms = /^\d{4}-\d{2}-\d{2}$/.test(value) ? Date.parse(`${value}T00:00:00Z`) : NaN;
      if (!Number.isFinite(ms) || new Date(ms).toISOString().slice(0, 10) !== value)
        throw new Error(`${label} must be a real date in YYYY-MM-DD`);
      return ms;
    };
    const start = parse("startDate", startDate);
    const end = parse("endDate", endDate);
    if (start !== void 0 && end !== void 0) {
      if (end < start)
        throw new Error("endDate must not be before startDate");
      if ((end - start) / 864e5 > 366)
        throw new Error("usage range is limited to 366 days");
    }
    return callThetaMcpTool(cfg, "get_billing_usage", withProject(projectId, { start_date: startDate, end_date: endDate }));
  },
  topUps: (cfg, projectId, page, number) => callThetaMcpTool(cfg, "list_billing_top_ups", withProject(projectId, { page, number })),
  // Usage labels are normalized first (they need the raw `token` value), then the whole result is
  // name-redacted here, so any other value under `token` never leaves this module.
  pricing: async (cfg, projectId) => {
    const normalized = normalizePricing(await callThetaMcpTool(cfg, "get_billing_pricing", withProject(projectId)));
    return normalized && typeof normalized === "object" ? redactObject(normalized) : normalized;
  }
};
var USAGE_LABELS = /* @__PURE__ */ new Set(["prompt_tokens", "completion_tokens", "embedding_tokens"]);
function creditsToUsd(value) {
  const n = typeof value === "number" ? value : typeof value === "string" && value.trim() !== "" ? Number(value) : NaN;
  return Number.isFinite(n) ? Math.round(n * 1e4) / 1e6 : void 0;
}
function normalizePricing(result) {
  if (!result || typeof result !== "object" || Array.isArray(result))
    return result;
  const out = { ...result };
  if (Array.isArray(out.chatbot)) {
    out.chatbot = out.chatbot.map((row) => {
      if (!row || typeof row !== "object" || Array.isArray(row))
        return row;
      const { token, ...rest } = row;
      const usd = creditsToUsd(rest.price);
      const priced = usd === void 0 ? rest : { ...rest, price_usd: usd };
      return typeof token === "string" && USAGE_LABELS.has(token) ? { usage_type: token, ...priced } : { token, ...priced };
    });
  }
  if (out.storage && typeof out.storage === "object" && !Array.isArray(out.storage)) {
    const usd = creditsToUsd(out.storage.price);
    if (usd !== void 0)
      out.storage = { ...out.storage, price_usd: usd };
  }
  out.priceUnit = "price is in Theta credits; price_usd = credits / 100";
  return out;
}

// build/commands/characters.js
var HOST = "https://ai-chars-api.thetaedgecloud.com";
function oneOf(path, value, allowed) {
  if (value !== void 0 && !(typeof value === "string" && allowed.includes(value))) {
    throw new Error(`${path} must be one of: ${allowed.join(", ")}`);
  }
}
function idString(value, label) {
  if (typeof value !== "string" || !value.trim() || value.length > 200 || /[\x00-\x1f\x7f]/.test(value)) {
    throw new Error(`${label} must be a non-empty identifier string`);
  }
}
function idList(value, label, max, required) {
  if (value === void 0 && !required)
    return;
  if (!Array.isArray(value) || value.length < 1 || value.length > max)
    throw new Error(`${label} must be an array of 1 to ${max} IDs`);
  value.forEach((entry, i) => idString(entry, `${label}[${i}]`));
}
var validateCharacter = (p) => {
  const style = p.speaking_style;
  if (style === void 0)
    return;
  if (!style || typeof style !== "object" || Array.isArray(style))
    throw new Error("speaking_style must be an object");
  const s = style;
  oneOf("speaking_style.formality", s.formality, ["casual", "formal", "neutral"]);
  oneOf("speaking_style.gesture_frequency", s.gesture_frequency, ["low", "medium", "high"]);
  oneOf("speaking_style.verbosity", s.verbosity, ["concise", "normal", "verbose"]);
};
var MESSAGE_TYPES = ["chat", "action", "event", "add_participant", "remove_participant"];
var validateSessionMessage = (p) => {
  if (!MESSAGE_TYPES.includes(p.type))
    throw new Error(`type must be one of: ${MESSAGE_TYPES.join(", ")}`);
  if (p.type === "chat" || p.type === "action") {
    idString(p.from_id, "from_id");
    if (typeof p.content !== "string" || !p.content.trim())
      throw new Error("content must be a non-empty string");
  }
  if (p.type === "event" && (typeof p.content !== "string" || !p.content.trim()))
    throw new Error("content must be a non-empty string");
  if (p.type === "add_participant" || p.type === "remove_participant") {
    oneOf("participant_type", p.participant_type, ["npc", "user"]);
    if (p.participant_type === void 0)
      throw new Error("participant_type is required");
    idString(p.participant_id, "participant_id");
  }
};
var validateGrouping = (p) => {
  if (p.name !== void 0 && (typeof p.name !== "string" || !p.name.trim()))
    throw new Error("name must be a non-empty string");
  if (p.order_index !== void 0 && (!Number.isInteger(p.order_index) || p.order_index < 0))
    throw new Error("order_index must be a non-negative integer");
};
var validateLibraryMessage = (p) => {
  if (p.content !== void 0 && (typeof p.content !== "string" || !p.content.trim()))
    throw new Error("content must be a non-empty string");
  if (p.type !== void 0 && typeof p.type !== "string")
    throw new Error("type must be a string");
};
var MAX_GROUPINGS = 20;
var validateStoryline = (required) => (p) => {
  if (required)
    idString(p.npc_id, "npc_id");
  else if (p.npc_id !== void 0)
    idString(p.npc_id, "npc_id");
  idList(p.grouping_ids, "grouping_ids", MAX_GROUPINGS, required);
};
var validateDialog = (p) => {
  idString(p.npc_id, "npc_id");
  const refs = p.message_refs;
  if (!Array.isArray(refs) || refs.length < 1 || refs.length > MAX_GROUPINGS)
    throw new Error(`message_refs must be an array of 1 to ${MAX_GROUPINGS} references`);
  refs.forEach((ref, i) => {
    if (!ref || typeof ref !== "object" || Array.isArray(ref))
      throw new Error(`message_refs[${i}] must be an object`);
    idString(ref.grouping_id, `message_refs[${i}].grouping_id`);
    idString(ref.message_id, `message_refs[${i}].message_id`);
  });
};
var characterRoutes = {
  list: { method: "GET", path: "/game/{gameId}/character/list", fields: ["gameId"] },
  get: { method: "GET", path: "/game/{gameId}/character/{characterId}", fields: ["gameId", "characterId"] },
  create: { method: "POST", path: "/game/{gameId}/character", fields: ["gameId"], validate: validateCharacter },
  update: { method: "PUT", path: "/game/{gameId}/character/{characterId}", fields: ["gameId", "characterId"], validate: validateCharacter },
  delete: { method: "DELETE", path: "/game/{gameId}/character/{characterId}", fields: ["gameId", "characterId"] },
  "session.create": { method: "POST", path: "/session", fields: [] },
  "session.get": { method: "GET", path: "/session/{sessionId}", fields: ["sessionId"] },
  "session.delete": { method: "DELETE", path: "/session/{sessionId}", fields: ["sessionId"] },
  "session.list": { method: "GET", path: "/session/{gameId}/list", fields: ["gameId"] },
  "session.context": { method: "PUT", path: "/session/{sessionId}/context", fields: ["sessionId"] },
  "session.message": { method: "POST", path: "/session/{sessionId}/message", fields: ["sessionId"], validate: validateSessionMessage, billable: true },
  "session.messages": { method: "GET", path: "/session/{sessionId}/message/list", fields: ["sessionId"], paginated: true },
  // Story mode: groupings (in-fiction events) hold library messages (authored player outcomes).
  "grouping.create": { method: "POST", path: "/game/{gameId}/grouping", fields: ["gameId"], validate: validateGrouping },
  "grouping.list": { method: "GET", path: "/game/{gameId}/grouping/list", fields: ["gameId"] },
  "grouping.get": { method: "GET", path: "/game/{gameId}/grouping/{groupingId}", fields: ["gameId", "groupingId"] },
  "grouping.update": { method: "PUT", path: "/game/{gameId}/grouping/{groupingId}", fields: ["gameId", "groupingId"], validate: validateGrouping },
  "grouping.delete": { method: "DELETE", path: "/game/{gameId}/grouping/{groupingId}", fields: ["gameId", "groupingId"] },
  "library.create": { method: "POST", path: "/grouping/{groupingId}/message", fields: ["groupingId"], validate: validateLibraryMessage },
  "library.list": { method: "GET", path: "/grouping/{groupingId}/message/list", fields: ["groupingId"] },
  "library.update": { method: "PUT", path: "/grouping/{groupingId}/message/{messageId}", fields: ["groupingId", "messageId"], validate: validateLibraryMessage },
  "library.delete": { method: "DELETE", path: "/grouping/{groupingId}/message/{messageId}", fields: ["groupingId", "messageId"] },
  // Story lines: ordered groupings + one NPC. Generation is handled by storylineGenerateAll below.
  "storyline.create": { method: "POST", path: "/game/{gameId}/storyline", fields: ["gameId"], validate: validateStoryline(true) },
  "storyline.list": { method: "GET", path: "/game/{gameId}/storyline/list", fields: ["gameId"] },
  "storyline.get": { method: "GET", path: "/storyline/{storylineId}", fields: ["storylineId"] },
  "storyline.update": { method: "PUT", path: "/storyline/{storylineId}", fields: ["storylineId"], validate: validateStoryline(false) },
  "storyline.delete": { method: "DELETE", path: "/storyline/{storylineId}", fields: ["storylineId"] },
  "storyline.queue": { method: "GET", path: "/storyline/{storylineId}/queue", fields: ["storylineId"] },
  "storyline.dialogs": { method: "GET", path: "/storyline/{storylineId}/dialog/list", fields: ["storylineId"] },
  // Dialogs: one generated conversation for an explicit path of library messages.
  "dialog.create": { method: "POST", path: "/game/{gameId}/dialog", fields: ["gameId"], validate: validateDialog, billable: true },
  "dialog.list": { method: "GET", path: "/game/{gameId}/dialog/list", fields: ["gameId"] },
  "dialog.get": { method: "GET", path: "/dialog/{dialogId}", fields: ["dialogId"] },
  "dialog.recreate": { method: "POST", path: "/dialog/{dialogId}/recreate", fields: ["dialogId"], fixedBody: {}, billable: true },
  "dialog.delete": { method: "DELETE", path: "/dialog/{dialogId}", fields: ["dialogId"] }
};
function buildPath(route, args) {
  let path = route.path;
  for (const field of route.fields) {
    if (typeof args[field] !== "string" || !args[field].trim())
      throw new Error(`${field} must be a non-empty string`);
    path = path.replace(`{${field}}`, pathSegment(args[field], field));
  }
  if (route.paginated && (args.page !== void 0 || args.number !== void 0)) {
    const page = args.page ?? 1;
    const number = args.number ?? 100;
    if (!Number.isInteger(page) || page < 1 || page > 1e4)
      throw new Error("page must be an integer from 1 to 10000");
    if (!Number.isInteger(number) || number < 1 || number > 100)
      throw new Error("number must be an integer from 1 to 100");
    path += `?${new URLSearchParams({ page: String(page), number: String(number) })}`;
  }
  return path;
}
function netOpts(cfg, method) {
  if (!cfg.charactersApiKey)
    throw new Error("THETA_CHARACTERS_API_KEY missing; use a game-scoped key, not an on-demand key");
  return {
    headers: { Authorization: `Bearer ${cfg.charactersApiKey}` },
    service: "theta-characters",
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: method === "GET" ? cfg.httpMaxRetries : 0,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}
function characterRequest(cfg, name, args) {
  const route = Object.hasOwn(characterRoutes, name) ? characterRoutes[name] : void 0;
  if (!route)
    throw new Error("Unknown AI Characters operation");
  const path = buildPath(route, args);
  let body;
  if (route.method === "POST" || route.method === "PUT") {
    if (route.fixedBody)
      body = { ...route.fixedBody };
    else {
      if (!args.payload || typeof args.payload !== "object" || Array.isArray(args.payload))
        throw new Error("payload must be an object");
      body = snapshotBody(args.payload);
      route.validate?.(body);
    }
  }
  if (cfg.dryRun && route.method !== "GET") {
    return { dryRun: true, method: route.method, path, billable: route.billable === true, payload: redactObject(body ?? {}) };
  }
  if (route.method !== "GET")
    assertApproved(cfg, args.confirm, `theta.characters.${name}`);
  const url2 = `${HOST}${path}`;
  const opts = netOpts(cfg, route.method);
  if (route.method === "GET")
    return getJson(url2, opts);
  if (route.method === "POST")
    return postJson(url2, body, opts);
  if (route.method === "PUT")
    return putJson(url2, body, opts);
  return deleteEmpty(url2, opts);
}
var STORYLINE_PATH_CAP = 5e3;
function pick(obj, keys) {
  if (!obj || typeof obj !== "object")
    return void 0;
  const o = obj;
  for (const key of keys)
    if (o[key] !== void 0)
      return o[key];
  return void 0;
}
function storylineGroupingIds(response) {
  const body = pick(response, ["body"]) ?? response;
  const storyline = pick(body, ["storyline"]) ?? body;
  const copies = [response, body, storyline].filter((c, i, all) => all.indexOf(c) === i).map((c) => pick(c, ["grouping_ids"])).filter((v) => v !== void 0);
  if (new Set(copies.map((v) => JSON.stringify(v))).size > 1) {
    throw new Error("Story line response has conflicting grouping_ids; refusing to generate without a path count");
  }
  const ids = pick(storyline, ["grouping_ids"]);
  if (!Array.isArray(ids) || ids.length < 1 || ids.length > MAX_GROUPINGS || !ids.every((id) => typeof id === "string" && id.trim())) {
    throw new Error("Could not read the story line grouping_ids; refusing to generate without a path count");
  }
  return ids;
}
var LIST_ALIASES = ["messages", "library_messages", "items"];
var TOTAL_FIELDS = ["total_count", "totalCount", "total", "count"];
var MORE_FIELDS = ["has_more", "hasMore", "has_next", "hasNext"];
var NEXT_FIELDS = ["next", "next_page", "nextPage", "next_cursor", "nextCursor", "next_page_token", "nextPageToken"];
var PAGES_FIELDS = ["total_pages", "totalPages", "page_count", "pageCount", "pages"];
var PAGE_FIELDS = ["page", "page_number", "pageNumber", "current_page", "currentPage"];
var PAGE_SIZE_FIELDS = ["number", "per_page", "perPage", "page_size", "pageSize", "limit", "size", "offset"];
var PAGINATION_FIELDS = /* @__PURE__ */ new Set([...TOTAL_FIELDS, ...MORE_FIELDS, ...NEXT_FIELDS, ...PAGES_FIELDS, ...PAGE_FIELDS, ...PAGE_SIZE_FIELDS]);
var INFO_FIELDS = /* @__PURE__ */ new Set([
  "status",
  "message",
  "code",
  "success",
  "error",
  "request_id",
  "requestId",
  "id",
  "grouping_id",
  "groupingId",
  "storyline_id",
  "storylineId",
  "npc_id",
  "npcId",
  "name",
  "title",
  "created_at",
  "createdAt",
  "updated_at",
  "updatedAt"
]);
function assertOnlyKnownFields(container, allowed) {
  for (const key of Object.keys(container)) {
    if (allowed.has(key) || PAGINATION_FIELDS.has(key))
      continue;
    const value = container[key];
    if (INFO_FIELDS.has(key) && (value === null || typeof value !== "object"))
      continue;
    refuseCount(`response has an unrecognised field (${key.slice(0, 40)})`);
  }
}
function assertNotFailure(container) {
  const success = own(container, "success");
  const status = own(container, "status");
  const error = own(container, "error");
  const statusText = typeof status === "string" ? status.trim() : "";
  const statusCode = typeof status === "number" ? status : /^\d{3}$/.test(statusText) ? Number(statusText) : void 0;
  if (success !== void 0 && success !== true || /^(err|error|errors|fail|failed|failure)$/i.test(statusText) || statusCode !== void 0 && statusCode >= 400 || error !== void 0 && error !== null && error !== false && error !== "") {
    refuseCount("list response reports a failure");
  }
}
function isPlainObject(value) {
  return !!value && typeof value === "object" && !Array.isArray(value);
}
function refuseCount(reason) {
  throw new Error(`Library message ${reason}; refusing to generate without a reliable path count`);
}
function own(obj, key) {
  return Object.prototype.hasOwnProperty.call(obj, key) ? obj[key] : void 0;
}
function libraryMessageCount(response) {
  if (!isPlainObject(response) && !Array.isArray(response))
    refuseCount("list response is malformed");
  const containers = [];
  let body = response;
  if (isPlainObject(response) && Object.prototype.hasOwnProperty.call(response, "body")) {
    body = response.body;
    if (!isPlainObject(body) && !Array.isArray(body))
      refuseCount("list response body is malformed");
    assertOnlyKnownFields(response, /* @__PURE__ */ new Set(["body", "pagination"]));
    containers.push(response);
  }
  let list;
  if (Array.isArray(body))
    list = body;
  else {
    const b = body;
    containers.push(b);
    const present = LIST_ALIASES.filter((key) => own(b, key) !== void 0);
    if (present.length === 0)
      refuseCount("list is missing");
    if (present.length > 1)
      refuseCount(`response has conflicting list fields (${present.join(", ")})`);
    const value = b[present[0]];
    if (!Array.isArray(value))
      refuseCount("list is malformed");
    assertOnlyKnownFields(b, /* @__PURE__ */ new Set([present[0], "pagination"]));
    list = value;
  }
  for (const c of containers)
    assertNotFailure(c);
  for (const container of [...containers]) {
    const pagination = own(container, "pagination");
    if (pagination === void 0)
      continue;
    if (!isPlainObject(pagination))
      refuseCount("pagination metadata is malformed");
    for (const key of Object.keys(pagination)) {
      if (!PAGINATION_FIELDS.has(key))
        refuseCount(`pagination metadata has an unsupported field (${key.slice(0, 40)})`);
    }
    containers.push(pagination);
  }
  const totals = [];
  const pageSizes = [];
  let reportedComplete = false;
  const safeInt = (value) => typeof value === "number" && Number.isSafeInteger(value) && value >= 0;
  for (const container of containers) {
    for (const key of TOTAL_FIELDS) {
      const value = own(container, key);
      if (value === void 0)
        continue;
      if (!safeInt(value))
        refuseCount("pagination total is malformed");
      totals.push(value);
    }
    for (const key of MORE_FIELDS) {
      const value = own(container, key);
      if (value === void 0)
        continue;
      if (typeof value !== "boolean")
        refuseCount("pagination completeness flag is malformed");
      if (value)
        refuseCount("list page is incomplete (more pages reported)");
    }
    for (const key of NEXT_FIELDS) {
      const value = own(container, key);
      if (value === void 0 || value === null || value === "" || value === false)
        continue;
      refuseCount("list page is incomplete (a next page is reported)");
    }
    for (const key of PAGES_FIELDS) {
      const value = own(container, key);
      if (value === void 0)
        continue;
      if (!safeInt(value))
        refuseCount("pagination page count is malformed");
      if (value > 1)
        refuseCount("list page is incomplete (more than one page reported)");
    }
    for (const key of PAGE_FIELDS) {
      const value = own(container, key);
      if (value === void 0)
        continue;
      if (!safeInt(value) || value > 1)
        refuseCount("pagination page is malformed or not the first page");
    }
    for (const key of PAGE_SIZE_FIELDS) {
      const value = own(container, key);
      if (value === void 0)
        continue;
      if (!safeInt(value))
        refuseCount("pagination page size or offset is malformed");
      if (key === "offset" && value !== 0)
        refuseCount("list page is not the first page (offset is not 0)");
      if (key !== "offset")
        pageSizes.push(value);
    }
    for (const key of MORE_FIELDS)
      if (own(container, key) === false)
        reportedComplete = true;
  }
  if (totals.length > 1 && new Set(totals).size > 1)
    refuseCount("pagination totals conflict");
  const total = totals[0];
  if (total === void 0 && !reportedComplete && pageSizes.some((size) => list.length >= size)) {
    refuseCount("list page is full and may be incomplete (no total or has_more:false reported)");
  }
  if (total !== void 0 && total < list.length)
    refuseCount("pagination total is smaller than the returned page");
  return total !== void 0 ? Math.max(total, list.length) : list.length;
}
async function storylineGenerateAll(cfg, args) {
  const storylineId = pathSegment(String(args.storylineId ?? ""), "storylineId");
  const maxPaths = args.maxPaths;
  if (!Number.isInteger(maxPaths) || maxPaths < 1 || maxPaths > STORYLINE_PATH_CAP) {
    throw new Error(`maxPaths must be an integer from 1 to ${STORYLINE_PATH_CAP}: the most dialog paths you approve generating`);
  }
  if (!cfg.dryRun)
    assertApproved(cfg, args.confirm, "theta.characters.storyline.generateAll");
  if (cfg.dryRun && !cfg.charactersApiKey) {
    return { dryRun: true, requiresKeyForPathCount: true, method: "POST", path: `/storyline/${storylineId}/generate_all`, maxPaths };
  }
  const read = netOpts(cfg, "GET");
  const storyline = await getJson(`${HOST}/storyline/${storylineId}`, read);
  const groupingIds = storylineGroupingIds(storyline);
  const perGrouping = [];
  let pathCount = 1;
  const effectiveLimit = Math.min(maxPaths, STORYLINE_PATH_CAP);
  for (const groupingId of groupingIds) {
    const count = libraryMessageCount(await getJson(`${HOST}/grouping/${pathSegment(groupingId, "grouping_id")}/message/list`, read));
    if (count < 1)
      throw new Error(`A grouping has no library messages, so there is nothing to generate: ${JSON.stringify(perGrouping)}`);
    perGrouping.push({ grouping_id: groupingId, library_messages: count });
    if (pathCount > Math.floor(effectiveLimit / count)) {
      throw new Error(`This story line exceeds ${effectiveLimit === STORYLINE_PATH_CAP ? `Theta's ${STORYLINE_PATH_CAP}-path cap` : `the approved maxPaths ${maxPaths}`} paths; nothing was generated. Counted so far: ${JSON.stringify(perGrouping)}`);
    }
    pathCount *= count;
  }
  const summary = { storylineId: args.storylineId, groupings: perGrouping, pathCount, maxPaths, serviceCap: STORYLINE_PATH_CAP };
  if (!Number.isSafeInteger(pathCount) || pathCount < 1 || pathCount > effectiveLimit) {
    throw new Error(`Path count failed the final safety check (${pathCount}); refusing to generate`);
  }
  if (cfg.dryRun)
    return { dryRun: true, method: "POST", path: `/storyline/${storylineId}/generate_all`, billable: true, ...summary };
  const result = await postJson(`${HOST}/storyline/${storylineId}/generate_all`, {}, netOpts(cfg, "POST"));
  return { ...summary, result };
}
var CHARACTERS_PUBLISHED_PRICES = Object.freeze({ inputPer1M: 7.5, outputPer1M: 20, embeddingPer1M: 0.2, source: "published-2026-11-11" });
function estimateCharactersCost(args) {
  const tokens = (label) => {
    const v = args[label];
    if (v === void 0)
      return 0;
    if (typeof v !== "number" || !Number.isFinite(v) || v < 0 || v > 1e12)
      throw new Error(`${label} must be a number from 0 to 1e12`);
    return v;
  };
  const input = tokens("inputTokens");
  const output = tokens("outputTokens");
  const embedding = tokens("embeddingTokens");
  const p = CHARACTERS_PUBLISHED_PRICES;
  const round = (n) => Math.round(n * 1e6) / 1e6;
  const breakdown = {
    inputUsd: round(input / 1e6 * p.inputPer1M),
    outputUsd: round(output / 1e6 * p.outputPer1M),
    embeddingUsd: round(embedding / 1e6 * p.embeddingPer1M)
  };
  return {
    estimateUsd: round(breakdown.inputUsd + breakdown.outputUsd + breakdown.embeddingUsd),
    breakdown,
    usage: { inputTokens: input, outputTokens: output, embeddingTokens: embedding },
    prices: p,
    note: "Estimate only, from Theta published prices; actual charges depend on usage. Verify current prices with theta.billing.pricing and spend with theta.billing.usage."
  };
}

// build/runtime/secretResolver.js
async function resolveThetaOnDemandToken(ctx, baseToken) {
  const callerEnv = ctx.env ?? {};
  if (ctx.getSecret) {
    for (const key of ["THETA_ONDEMAND_API_TOKEN", "THETA_ONDEMAND_API_KEY", "THETA_API_KEY"]) {
      try {
        const secret = await ctx.getSecret(key);
        if (secret && secret.trim())
          return secret.trim();
      } catch {
      }
    }
  }
  for (const key of ["THETA_ONDEMAND_API_TOKEN", "THETA_ONDEMAND_API_KEY", "THETA_API_KEY"]) {
    const envToken = callerEnv[key];
    if (envToken && envToken.trim())
      return envToken.trim();
  }
  if (baseToken && baseToken.trim())
    return baseToken.trim();
  return void 0;
}

// build/runtime/handlers.js
function coerceBool(value, fallback) {
  if (value === void 0)
    return fallback;
  const normalized = value.trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized))
    return true;
  if (["0", "false", "no", "off"].includes(normalized))
    return false;
  return fallback;
}
function coerceInt(value, fallback, min, max) {
  if (!value)
    return fallback;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed))
    return fallback;
  return Math.min(Math.max(parsed, min), max);
}
var CALLER_ENV_KEYS = [
  "THETA_DRY_RUN",
  "THETA_EC_API_KEY",
  "THETA_EC_PROJECT_ID",
  "THETA_ORG_ID",
  "THETA_VIDEO_SA_ID",
  "THETA_VIDEO_SA_SECRET",
  "THETA_CHARACTERS_API_KEY",
  "THETA_INFERENCE_ENDPOINT",
  "THETA_INFERENCE_AUTH_USER",
  "THETA_INFERENCE_AUTH_PASS",
  "THETA_ONDEMAND_API_TOKEN",
  "THETA_ONDEMAND_API_KEY",
  "THETA_API_KEY",
  "THETA_ONDEMAND_API_BASE_URL",
  "THETA_API_BASE_URL",
  "THETA_HTTP_TIMEOUT_MS",
  "THETA_HTTP_MAX_RETRIES",
  "THETA_HTTP_RETRY_BACKOFF_MS"
];
function snapshotCallerEnv(env) {
  const out = {};
  if (!env || typeof env !== "object")
    return out;
  for (const key of CALLER_ENV_KEYS) {
    const value = env[key];
    if (typeof value === "string")
      out[key] = value;
  }
  return Object.freeze(out);
}
async function buildRuntimeConfig(ctx) {
  const base = loadConfig();
  const callerEnv = snapshotCallerEnv(ctx.env);
  const onDemandApiToken = await resolveThetaOnDemandToken({ env: callerEnv, getSecret: ctx.getSecret }, base.onDemandApiToken);
  if (callerEnv.THETA_INFERENCE_ENDPOINT && base.inferenceEndpoint && new URL(callerEnv.THETA_INFERENCE_ENDPOINT.trim()).origin !== new URL(base.inferenceEndpoint.trim()).origin) {
    throw new Error("Request-level THETA_INFERENCE_ENDPOINT override is disabled; configure the operator endpoint instead");
  }
  const sameInferenceOrigin = !callerEnv.THETA_INFERENCE_ENDPOINT || base.inferenceEndpoint && new URL(callerEnv.THETA_INFERENCE_ENDPOINT.trim()).origin === new URL(base.inferenceEndpoint.trim()).origin;
  const inferenceAuthUser = callerEnv.THETA_INFERENCE_AUTH_USER ?? (sameInferenceOrigin ? base.inferenceAuth?.user : void 0);
  const inferenceAuthPass = callerEnv.THETA_INFERENCE_AUTH_PASS ?? (sameInferenceOrigin ? base.inferenceAuth?.pass : void 0);
  return {
    ...base,
    // A caller-supplied ctx.env can turn dry-run ON but never OFF an operator-enabled dry-run.
    dryRun: base.dryRun || coerceBool(callerEnv.THETA_DRY_RUN, false),
    edgecloudApiKey: callerEnv.THETA_EC_API_KEY ?? base.edgecloudApiKey,
    edgecloudProjectId: callerEnv.THETA_EC_PROJECT_ID ?? base.edgecloudProjectId,
    edgecloudOrgId: callerEnv.THETA_ORG_ID ?? base.edgecloudOrgId,
    videoSaId: callerEnv.THETA_VIDEO_SA_ID ?? base.videoSaId,
    videoSaSecret: callerEnv.THETA_VIDEO_SA_SECRET ?? base.videoSaSecret,
    charactersApiKey: callerEnv.THETA_CHARACTERS_API_KEY ?? base.charactersApiKey,
    inferenceEndpoint: callerEnv.THETA_INFERENCE_ENDPOINT ?? base.inferenceEndpoint,
    inferenceAuth: inferenceAuthUser && inferenceAuthPass ? { user: inferenceAuthUser, pass: inferenceAuthPass } : void 0,
    onDemandApiToken,
    onDemandApiBaseUrl: callerEnv.THETA_ONDEMAND_API_BASE_URL ?? callerEnv.THETA_API_BASE_URL ?? base.onDemandApiBaseUrl,
    httpTimeoutMs: coerceInt(callerEnv.THETA_HTTP_TIMEOUT_MS, base.httpTimeoutMs, 1e3, 12e4),
    httpMaxRetries: coerceInt(callerEnv.THETA_HTTP_MAX_RETRIES, base.httpMaxRetries, 0, 6),
    httpRetryBackoffMs: coerceInt(callerEnv.THETA_HTTP_RETRY_BACKOFF_MS, base.httpRetryBackoffMs, 25, 1e4)
  };
}
function requireFields(args, fields) {
  for (const field of fields) {
    if (!(field in args) || args[field] === void 0 || args[field] === null || args[field] === "") {
      throw new Error(`Missing required field: ${field}`);
    }
  }
}
function requireObject(value, field) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${field} must be an object`);
  }
  return value;
}
function requireText2(value, field) {
  if (value === void 0 || value === null || String(value).trim() === "") {
    throw new Error(`Missing required field: ${field}`);
  }
  return String(value).trim();
}
function resolveInputFields(args) {
  if (Array.isArray(args.input_fields))
    return args.input_fields.map((field) => requireText2(field, "input_fields[]"));
  if (Array.isArray(args.inputFields))
    return args.inputFields.map((field) => requireText2(field, "inputFields[]"));
  const single = args.input_field ?? args.inputField;
  if (single !== void 0 && single !== null && String(single).trim() !== "")
    return [requireText2(single, "input_field")];
  return void 0;
}
function resolveProjectId(cfg, args) {
  return requireText2(args.projectId ?? cfg.edgecloudProjectId, "projectId");
}
var commandRegistry = {
  "theta.deployments.startByBaseId": {
    schema: { command: "theta.deployments.startByBaseId", description: "Restart stopped GPU node using its base ID", required: ["baseId"] },
    handler: (cfg, args) => deployments.startByBaseId(cfg, resolveProjectId(cfg, args), requireText2(args.baseId, "baseId"), args.confirm === true)
  },
  "theta.templates.listStandard": {
    schema: { command: "theta.templates.listStandard", description: "List standard templates including training GPU nodes", required: ["category"] },
    handler: (cfg, args) => {
      if (!["prototyping", "serving", "training"].includes(String(args.category)))
        throw new Error("Invalid template category");
      return deployments.listStandard(cfg, args.category);
    }
  },
  "theta.templates.listCustom": {
    schema: { command: "theta.templates.listCustom", description: "List project custom deployment templates", required: [] },
    handler: (cfg, args) => deployments.listCustom(cfg, resolveProjectId(cfg, args))
  },
  "theta.video.uploadCreate": {
    schema: { command: "theta.video.uploadCreate", description: "Create video upload session; does not read local files", required: [] },
    handler: (cfg, args) => video.uploadCreate(cfg, args.confirm === true)
  },
  "theta.video.create": {
    schema: { command: "theta.video.create", description: "Create video from supplied remote-source payload", required: ["payload"] },
    handler: (cfg, args) => video.videoCreate(cfg, requireObject(args.payload, "payload"), args.confirm === true)
  },
  "theta.video.get": {
    schema: { command: "theta.video.get", description: "Inspect a video", required: ["videoId"] },
    handler: (cfg, args) => video.videoGet(cfg, requireText2(args.videoId, "videoId"))
  },
  "theta.video.streamCreate": {
    schema: { command: "theta.video.streamCreate", description: "Create a livestream", required: ["payload"] },
    handler: (cfg, args) => video.streamCreate(cfg, requireObject(args.payload, "payload"), args.confirm === true)
  },
  "theta.video.streamGet": {
    schema: { command: "theta.video.streamGet", description: "Inspect a livestream", required: ["streamId"] },
    handler: (cfg, args) => video.streamGet(cfg, requireText2(args.streamId, "streamId"))
  },
  "theta.video.ingestorList": {
    schema: { command: "theta.video.ingestorList", description: "List stream ingestors", required: [] },
    handler: (cfg) => video.ingestorList(cfg)
  },
  "theta.video.search": {
    schema: { command: "theta.video.search", description: "Search a service account's videos by metadata filters (1-10 key/value pairs, operator and|or, page, number<=100)", required: ["serviceAccountId", "filters"] },
    handler: (cfg, args) => video.videoSearch(cfg, requireText2(args.serviceAccountId, "serviceAccountId"), args.filters, args.operator, args.page, args.number)
  },
  "theta.video.streamList": {
    schema: { command: "theta.video.streamList", description: "List a service account's livestreams (optional status on|off); stream keys are redacted", required: ["serviceAccountId"] },
    handler: (cfg, args) => video.streamList(cfg, requireText2(args.serviceAccountId, "serviceAccountId"), args.status)
  },
  "theta.video.ingestorUnselect": {
    schema: { command: "theta.video.ingestorUnselect", description: "Release a selected stream ingestor (invalidates the live stream key)", required: ["ingestorId"] },
    handler: (cfg, args) => video.ingestorUnselect(cfg, requireText2(args.ingestorId, "ingestorId"), args.confirm === true)
  },
  "theta.video.ingestorSelect": {
    schema: { command: "theta.video.ingestorSelect", description: "Select stream ingestor", required: ["ingestorId", "body"] },
    handler: (cfg, args) => video.ingestorSelect(cfg, requireText2(args.ingestorId, "ingestorId"), requireObject(args.body, "body"), args.confirm === true)
  },
  "theta.health": {
    schema: { command: "theta.health", description: "EdgeCloud health check via controller VM listing", required: [] },
    handler: (cfg) => healthCheck(cfg)
  },
  "theta.inference.models": {
    schema: { command: "theta.inference.models", description: "List models from dedicated inference endpoint", required: [] },
    handler: (cfg, args) => {
      if (args.endpoint !== void 0 && String(args.endpoint).trim() !== "") {
        throw new Error("args.endpoint override is disabled for security. Set THETA_INFERENCE_ENDPOINT instead.");
      }
      return inference.models(cfg);
    }
  },
  "theta.inference.chat": {
    schema: { command: "theta.inference.chat", description: "Run chat completion on dedicated inference endpoint", required: ["body"] },
    handler: (cfg, args) => {
      if (args.endpoint !== void 0 && String(args.endpoint).trim() !== "") {
        throw new Error("args.endpoint override is disabled for security. Set THETA_INFERENCE_ENDPOINT instead.");
      }
      return inference.chat(cfg, args.body);
    }
  },
  "theta.inference.ready": {
    schema: { command: "theta.inference.ready", description: "Poll dedicated inference endpoint readiness with openai or gradio probe", required: [] },
    handler: (cfg, args) => inference.ready(cfg, {
      probe: validateProbe(args.probe),
      timeoutMs: args.timeoutMs,
      intervalMs: args.intervalMs
    })
  },
  "theta.ondemand.listServices": {
    schema: { command: "theta.ondemand.listServices", description: "List live on-demand services with catalog fallback", required: [] },
    handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category })
  },
  "list_services": {
    schema: { command: "list_services", description: "MCP-compatible alias: list available Theta on-demand services", required: [] },
    handler: (cfg, args) => ondemand.listLiveServices(cfg, { category: args.category })
  },
  "theta.ondemand.infer": {
    schema: { command: "theta.ondemand.infer", description: "Create on-demand infer request (video, unknown or high-cost services and webhooks require confirm:true)", required: ["service", "payload"] },
    handler: (cfg, args) => ondemand.infer(cfg, args.service, args.payload, { ...args.options, confirm: args.confirm === true })
  },
  "infer": {
    schema: { command: "infer", description: "MCP-compatible alias: create on-demand infer request (video, unknown or high-cost services and webhooks require confirm:true)", required: ["service"] },
    handler: (cfg, args) => ondemand.infer(cfg, requireText2(args.service, "service"), args.payload ?? {
      input: args.input ?? {},
      ...args.variant ? { variant: args.variant } : {},
      ...args.webhook ? { webhook: args.webhook } : {}
    }, {
      wait: args.wait,
      prediction: args.prediction,
      confirm: args.confirm === true
    })
  },
  "theta.ondemand.chat": {
    schema: { command: "theta.ondemand.chat", description: "Run chat on-demand inference (GLM-5.3, Qwen3.8, Ling, Qwen3); tools only on GLM-5.3; defaults to Qwen3", required: ["messages"] },
    handler: (cfg, args) => ondemand.chat(cfg, args.service ?? "qwen3", args.messages, {
      maxTokens: args.max_tokens,
      temperature: args.temperature,
      topP: args.top_p,
      stream: args.stream,
      wait: args.wait,
      prediction: args.prediction,
      variant: args.variant,
      webhook: args.webhook,
      reasoningEffort: args.reasoning_effort,
      enableThinking: args.enable_thinking,
      tools: args.tools,
      toolChoice: args.tool_choice,
      parallelToolCalls: args.parallel_tool_calls,
      extraInput: args.extraInput,
      allowUnknownService: args.allowUnknownService,
      allowUnverifiedTools: args.allowUnverifiedTools === true,
      confirm: args.confirm === true
    })
  },
  "theta.ondemand.status": {
    schema: { command: "theta.ondemand.status", description: "Get on-demand infer request status", required: ["requestId"] },
    handler: (cfg, args) => ondemand.status(cfg, args.requestId)
  },
  "get_request_status": {
    schema: { command: "get_request_status", description: "MCP-compatible alias: get on-demand infer request status", required: [] },
    handler: (cfg, args) => ondemand.status(cfg, requireText2(args.request_id ?? args.requestId, "request_id"))
  },
  "theta.ondemand.inputPresignedUrls": {
    schema: { command: "theta.ondemand.inputPresignedUrls", description: "Create presigned URLs for on-demand inputs", required: ["service"] },
    handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, args.service, resolveInputFields(args))
  },
  "get_upload_url": {
    schema: { command: "get_upload_url", description: "MCP-compatible alias: create presigned URLs for on-demand inputs", required: ["service"] },
    handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, requireText2(args.service, "service"), resolveInputFields(args))
  },
  "theta.ondemand.pollUntilDone": {
    schema: { command: "theta.ondemand.pollUntilDone", description: "Poll on-demand request until terminal state", required: ["requestId"] },
    handler: (cfg, args) => ondemand.pollUntilDone(cfg, args.requestId, args.options)
  },
  "theta.deployments.list": {
    schema: { command: "theta.deployments.list", description: "List deployments for project", required: [] },
    handler: (cfg, args) => deployments.list(cfg, resolveProjectId(cfg, args))
  },
  "theta.deployments.routeProbe": {
    schema: { command: "theta.deployments.routeProbe", description: "Probe singular/plural deployment list routes for project", required: [] },
    handler: (cfg, args) => deployments.routeProbe(cfg, resolveProjectId(cfg, args))
  },
  "theta.deployments.create": {
    schema: { command: "theta.deployments.create", description: "Create deployment from payload", required: ["payload"] },
    handler: (cfg, args) => deployments.create(cfg, { ...requireObject(args.payload, "payload"), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  "theta.deployments.start": {
    schema: { command: "theta.deployments.start", description: "Start deployment by shard/suffix with route fallback", required: ["shard", "suffix"] },
    handler: (cfg, args) => deployments.start(cfg, resolveProjectId(cfg, args), requireText2(args.shard, "shard"), requireText2(args.suffix, "suffix"), args.confirm === true)
  },
  "theta.deployments.stop": {
    schema: { command: "theta.deployments.stop", description: "Stop deployment by shard/suffix with route fallback", required: ["shard", "suffix"] },
    handler: (cfg, args) => deployments.stop(cfg, resolveProjectId(cfg, args), requireText2(args.shard, "shard"), requireText2(args.suffix, "suffix"), args.confirm === true)
  },
  "theta.deployments.delete": {
    schema: { command: "theta.deployments.delete", description: "Delete deployment by shard/suffix with route fallback", required: ["shard", "suffix"] },
    handler: (cfg, args) => deployments.delete(cfg, resolveProjectId(cfg, args), requireText2(args.shard, "shard"), requireText2(args.suffix, "suffix"), args.confirm === true)
  },
  "theta.deployments.validateDisposable": {
    schema: { command: "theta.deployments.validateDisposable", description: "Create, probe, smoke, delete, and report balance delta for one disposable deployment", required: ["payload"] },
    handler: (cfg, args) => deployments.validateDisposable(cfg, {
      payload: requireObject(args.payload, "payload"),
      confirm: args.confirm === true,
      projectId: args.projectId,
      orgId: args.orgId,
      probe: validateProbe(args.probe),
      readyTimeoutMs: args.readyTimeoutMs,
      intervalMs: args.intervalMs,
      smokeMessage: args.smokeMessage,
      model: args.model
    })
  },
  "theta.billing.balance": {
    schema: { command: "theta.billing.balance", description: "Read org balance in credits and USD (hosted MCP); falls back to raw controller credits", required: [] },
    handler: async (cfg, args) => {
      try {
        return { source: "theta-hosted-mcp", ...await billing.balanceUsd(cfg, resolveProjectId(cfg, args)) };
      } catch (error) {
        return {
          source: "controller-raw",
          warning: `Hosted MCP balance failed (${sanitizeHttpErrorMessage(String(error.message)).slice(0, 300)}); raw value is credits, 1 credit = USD 0.01 on 2026-10-03`,
          response: await deployments.balance(cfg, args.orgId)
        };
      }
    }
  },
  "theta.billing.usage": {
    schema: { command: "theta.billing.usage", description: "Project usage by category and day in credits and USD (default last 7 days, max 366)", required: [] },
    handler: (cfg, args) => billing.usage(cfg, resolveProjectId(cfg, args), args.startDate, args.endDate)
  },
  "theta.billing.topUps": {
    schema: { command: "theta.billing.topUps", description: "Organization top-up history, newest first", required: [] },
    handler: (cfg, args) => billing.topUps(cfg, resolveProjectId(cfg, args), args.page, args.number)
  },
  "theta.billing.pricing": {
    schema: { command: "theta.billing.pricing", description: "Current chatbot, storage and on-demand prices (GPU prices come from theta.gpu.resources.list)", required: [] },
    handler: (cfg, args) => billing.pricing(cfg, resolveProjectId(cfg, args))
  },
  "theta.gpu.resources.list": {
    schema: { command: "theta.gpu.resources.list", description: "Hosted and community GPU capacity with region, availability and USD/hour; optional provider/gpuModel/region/maxPricePerHourUsd/availableOnly/limit filters", required: [] },
    handler: (cfg, args) => gpu.listResources(cfg, resolveProjectId(cfg, args), {
      provider: args.provider,
      gpuModel: args.gpuModel,
      region: args.region,
      maxPricePerHourUsd: args.maxPricePerHourUsd,
      availableOnly: args.availableOnly,
      limit: args.limit
    })
  },
  "theta.gpu.resources.get": {
    schema: { command: "theta.gpu.resources.get", description: "Details and current availability of one GPU resource", required: ["resourceId"] },
    handler: (cfg, args) => gpu.getResource(cfg, resolveProjectId(cfg, args), requireText2(args.resourceId, "resourceId"), args.region)
  },
  "theta.gpu.templates.list": {
    schema: { command: "theta.gpu.templates.list", description: "GPU Node deployment templates with allowed container images", required: [] },
    handler: (cfg, args) => gpu.listTemplates(cfg, resolveProjectId(cfg, args))
  },
  "theta.gpu.deployments.list": {
    schema: { command: "theta.gpu.deployments.list", description: "GPU Node deployments with state, resource and price", required: [] },
    handler: (cfg, args) => gpu.listDeployments(cfg, resolveProjectId(cfg, args))
  },
  "theta.gpu.deployments.get": {
    schema: { command: "theta.gpu.deployments.get", description: "One GPU Node deployment including endpoints and status", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.getDeployment(cfg, resolveProjectId(cfg, args), requireText2(args.deploymentId, "deploymentId"))
  },
  "theta.gpu.deployments.events": {
    schema: { command: "theta.gpu.deployments.events", description: "Scheduling and lifecycle events of a GPU Node deployment", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.deploymentEvents(cfg, resolveProjectId(cfg, args), requireText2(args.deploymentId, "deploymentId"))
  },
  "theta.gpu.deployments.logs": {
    schema: { command: "theta.gpu.deployments.logs", description: "Recent container logs of a GPU Node deployment", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.deploymentLogs(cfg, resolveProjectId(cfg, args), requireText2(args.deploymentId, "deploymentId"))
  },
  "theta.gpu.deployments.create": {
    schema: { command: "theta.gpu.deployments.create", description: "PAID: create a GPU Node with a provider-side max_price_per_hour_usd cap; requires confirm:true after approval", required: ["name", "deploymentTemplateId", "resourceId", "maxPricePerHourUsd"] },
    handler: (cfg, args) => gpu.createDeployment(cfg, resolveProjectId(cfg, args), {
      name: requireText2(args.name, "name"),
      deploymentTemplateId: requireText2(args.deploymentTemplateId, "deploymentTemplateId"),
      resourceId: requireText2(args.resourceId, "resourceId"),
      maxPricePerHourUsd: Number(args.maxPricePerHourUsd),
      confirm: args.confirm,
      region: args.region,
      displayName: args.displayName,
      containerImage: args.containerImage,
      sshPublicKey: args.sshPublicKey,
      sshPort: args.sshPort,
      httpPort: args.httpPort
    })
  },
  "theta.gpu.deployments.start": {
    schema: { command: "theta.gpu.deployments.start", description: "PAID: start a stopped GPU Node (resumes hourly billing); requires confirm:true", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), "start", requireText2(args.deploymentId, "deploymentId"), args.confirm)
  },
  "theta.gpu.deployments.stop": {
    schema: { command: "theta.gpu.deployments.stop", description: "Stop a running GPU Node (billing stops, config kept); requires confirm:true", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), "stop", requireText2(args.deploymentId, "deploymentId"), args.confirm)
  },
  "theta.gpu.deployments.delete": {
    schema: { command: "theta.gpu.deployments.delete", description: "PERMANENT: delete a GPU Node and its configuration; requires confirm:true", required: ["deploymentId"] },
    handler: (cfg, args) => gpu.lifecycle(cfg, resolveProjectId(cfg, args), "delete", requireText2(args.deploymentId, "deploymentId"), args.confirm)
  },
  "theta.billing.balanceSnapshot": {
    schema: { command: "theta.billing.balanceSnapshot", description: "Read Theta org balance and extract numeric value when possible", required: [] },
    handler: (cfg, args) => deployments.balanceSnapshot(cfg, args.orgId)
  },
  "theta.ai.agent.create": {
    schema: { command: "theta.ai.agent.create", description: "Create Theta EdgeCloud AI Agent/RAG chatbot", required: ["payload"] },
    handler: (cfg, args) => deployments.chatbotCreate(cfg, { ...requireObject(args.payload, "payload"), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  "theta.ai.agent.get": {
    schema: { command: "theta.ai.agent.get", description: "Fetch Theta EdgeCloud AI Agent/RAG chatbot details", required: ["chatbotId"] },
    handler: (cfg, args) => deployments.chatbotGet(cfg, requireText2(args.chatbotId, "chatbotId"), resolveProjectId(cfg, args))
  },
  "theta.ai.agent.update": {
    schema: { command: "theta.ai.agent.update", description: "Update Theta EdgeCloud AI Agent/RAG chatbot settings", required: ["chatbotId", "payload"] },
    handler: (cfg, args) => deployments.chatbotUpdate(cfg, requireText2(args.chatbotId, "chatbotId"), { ...requireObject(args.payload, "payload"), project_id: resolveProjectId(cfg, args) }, args.confirm === true)
  },
  "theta.ai.agent.list": {
    schema: { command: "theta.ai.agent.list", description: "List Theta EdgeCloud AI Agent/RAG chatbots", required: [] },
    handler: (cfg, args) => deployments.chatbotList(cfg, resolveProjectId(cfg, args), args.page, args.number)
  },
  "theta.ai.agent.document.create": {
    schema: { command: "theta.ai.agent.document.create", description: "Create AI Agent knowledge-base document from provided content", required: ["chatbotId", "file"] },
    handler: (cfg, args) => deployments.chatbotDocumentCreate(cfg, requireText2(args.chatbotId, "chatbotId"), resolveProjectId(cfg, args), requireObject(args.file, "file"), args.metadata, args.confirm === true)
  },
  "theta.ai.agent.document.update": {
    schema: { command: "theta.ai.agent.document.update", description: "Update AI Agent knowledge-base document from provided content", required: ["chatbotId", "documentId", "file"] },
    handler: (cfg, args) => deployments.chatbotDocumentUpdate(cfg, requireText2(args.chatbotId, "chatbotId"), requireText2(args.documentId, "documentId"), resolveProjectId(cfg, args), requireObject(args.file, "file"), args.metadata, args.confirm === true)
  },
  "theta.ai.agent.document.get": {
    schema: { command: "theta.ai.agent.document.get", description: "Fetch AI Agent knowledge-base document", required: ["chatbotId", "documentId"] },
    handler: (cfg, args) => deployments.chatbotDocumentGet(cfg, requireText2(args.chatbotId, "chatbotId"), requireText2(args.documentId, "documentId"))
  },
  "theta.ai.agent.document.list": {
    schema: { command: "theta.ai.agent.document.list", description: "List AI Agent knowledge-base documents", required: ["chatbotId"] },
    handler: (cfg, args) => deployments.chatbotDocumentList(cfg, requireText2(args.chatbotId, "chatbotId"), resolveProjectId(cfg, args), args.page, args.number)
  },
  "theta.deployments.listVm": {
    schema: { command: "theta.deployments.listVm", description: "List EdgeCloud VM types", required: [] },
    handler: (cfg) => deployments.listVm(cfg)
  },
  "theta.video.list": {
    schema: { command: "theta.video.list", description: "List videos for service account", required: ["serviceAccountId"] },
    handler: (cfg, args) => video.videoList(cfg, args.serviceAccountId, args.page ?? 1, args.number ?? 10)
  }
};
var onDemandTokenCommands = /* @__PURE__ */ new Set([
  "theta.ondemand.infer",
  "theta.ondemand.chat",
  "theta.ondemand.status",
  "theta.ondemand.inputPresignedUrls",
  "theta.ondemand.pollUntilDone",
  "infer",
  "get_request_status",
  "get_upload_url"
]);
var confirmRequiredCommands = /* @__PURE__ */ new Set([
  "theta.deployments.create",
  "theta.deployments.start",
  "theta.deployments.stop",
  "theta.deployments.delete",
  "theta.deployments.startByBaseId",
  "theta.deployments.validateDisposable",
  "theta.ai.agent.create",
  "theta.ai.agent.update",
  "theta.ai.agent.document.create",
  "theta.ai.agent.document.update",
  "theta.video.uploadCreate",
  "theta.video.create",
  "theta.video.streamCreate",
  "theta.video.ingestorSelect",
  "theta.video.ingestorUnselect",
  // Every non-GET AI Characters route (characters, sessions, Story mode) is added below from the route table.
  "theta.characters.storyline.generateAll",
  "theta.gpu.deployments.create",
  "theta.gpu.deployments.start",
  "theta.gpu.deployments.stop",
  "theta.gpu.deployments.delete"
]);
function thetaCommandRequiresConfirm(command) {
  return confirmRequiredCommands.has(command);
}
for (const [name, route] of Object.entries(characterRoutes)) {
  const command = `theta.characters.${name}`;
  const needsPayload = ["POST", "PUT"].includes(route.method) && !route.fixedBody;
  commandRegistry[command] = {
    schema: {
      command,
      description: `AI Characters ${route.method} ${route.path}${route.billable ? " (BILLABLE: generates tokens)" : ""}${route.paginated ? "; optional page/number" : ""}; game-scoped key required`,
      required: [...route.fields, ...needsPayload ? ["payload"] : []]
    },
    handler: (cfg, args) => characterRequest(cfg, name, args)
  };
  if (route.method !== "GET")
    confirmRequiredCommands.add(command);
}
commandRegistry["theta.characters.storyline.generateAll"] = {
  schema: {
    command: "theta.characters.storyline.generateAll",
    description: `BILLABLE BULK: generate every dialog path of a story line. Counts paths first (one library message per grouping) and refuses above maxPaths or ${STORYLINE_PATH_CAP}; game-scoped key required`,
    required: ["storylineId", "maxPaths"]
  },
  handler: (cfg, args) => storylineGenerateAll(cfg, args)
};
commandRegistry["theta.characters.estimateCost"] = {
  schema: {
    command: "theta.characters.estimateCost",
    description: "Offline AI Characters cost estimate from token counts (inputTokens, outputTokens, embeddingTokens) at Theta published prices; makes no network request",
    required: []
  },
  handler: (_cfg, args) => estimateCharactersCost(args)
};
var thetaRuntimeCommandSchemas = Object.fromEntries(Object.entries(commandRegistry).map(([cmd, reg]) => [cmd, confirmRequiredCommands.has(cmd) ? { ...reg.schema, description: `${reg.schema.description} [requires confirm:true outside dry-run]` } : reg.schema]));
function listThetaRuntimeCommands() {
  return Object.keys(commandRegistry).sort();
}
async function executeThetaRuntimeCommand(args, ctx = {}) {
  const registration = Object.hasOwn(commandRegistry, args.command) ? commandRegistry[args.command] : void 0;
  if (!registration) {
    throw new Error(`Unsupported theta runtime command: ${args.command}`);
  }
  requireFields(args, registration.schema.required);
  const cfg = await buildRuntimeConfig(ctx);
  if (onDemandTokenCommands.has(args.command) && !cfg.dryRun && !cfg.onDemandApiToken) {
    throw new Error("THETA_ONDEMAND_API_TOKEN missing (runtime secret/env resolver)");
  }
  if (confirmRequiredCommands.has(args.command) && !cfg.dryRun && args.confirm !== true) {
    throw new Error(`${args.command} creates, changes, bills or deletes remote resources. Preview with THETA_DRY_RUN=1, get explicit user approval for this exact action, then pass confirm:true.`);
  }
  const result = await registration.handler(cfg, args);
  return result && typeof result === "object" ? redactObject(result) : result;
}

// build/index.js
async function safe(value) {
  const result = await value;
  return result && typeof result === "object" ? redactObject(result) : result;
}
function theta() {
  const cfg = loadConfig();
  return {
    // Which credential families are configured. Never the credential values themselves.
    configured: {
      onDemand: Boolean(cfg.onDemandApiToken),
      controller: Boolean(cfg.edgecloudApiKey),
      project: Boolean(cfg.edgecloudProjectId),
      video: Boolean(cfg.videoSaId && cfg.videoSaSecret),
      characters: Boolean(cfg.charactersApiKey),
      dedicatedEndpoint: Boolean(cfg.inferenceEndpoint),
      dryRun: cfg.dryRun
    },
    deploy: {
      listStandard: (category) => safe(deployments.listStandard(cfg, category)),
      listCustom: (projectId) => safe(deployments.listCustom(cfg, projectId)),
      listVm: () => safe(deployments.listVm(cfg)),
      list: (projectId) => safe(deployments.list(cfg, projectId)),
      routeProbe: (projectId) => safe(deployments.routeProbe(cfg, projectId)),
      balance: (orgId) => safe(deployments.balance(cfg, orgId)),
      chatbotGet: (chatbotId, projectId) => safe(deployments.chatbotGet(cfg, chatbotId, projectId)),
      chatbotList: (projectId, page, number) => safe(deployments.chatbotList(cfg, projectId, page, number)),
      chatbotDocumentGet: (chatbotId, documentId) => safe(deployments.chatbotDocumentGet(cfg, chatbotId, documentId)),
      chatbotDocumentList: (chatbotId, projectId, page, number) => safe(deployments.chatbotDocumentList(cfg, chatbotId, projectId, page, number))
    },
    inference: {
      models: () => safe(inference.models(cfg)),
      ready: (opts) => safe(inference.ready(cfg, opts))
    },
    video: {
      videoGet: (videoId) => safe(video.videoGet(cfg, videoId)),
      videoList: (serviceAccountId, page, number) => safe(video.videoList(cfg, serviceAccountId, page, number)),
      streamGet: (streamId) => safe(video.streamGet(cfg, streamId)),
      ingestorList: () => safe(video.ingestorList(cfg))
    },
    ondemand: {
      catalog: ondemand.catalog,
      listServices: (opts) => safe(ondemand.listServices(opts)),
      listLiveServices: (opts) => safe(ondemand.listLiveServices(cfg, opts)),
      status: (requestId) => safe(ondemand.status(cfg, requestId)),
      pollUntilDone: (requestId, opts) => safe(ondemand.pollUntilDone(cfg, requestId, opts))
    },
    healthCheck: () => safe(healthCheck(cfg))
  };
}
export {
  executeThetaRuntimeCommand,
  listThetaRuntimeCommands,
  theta,
  thetaCommandRequiresConfirm,
  thetaRuntimeCommandSchemas
};
