const DEFAULT_TIMEOUT_MS = 3500;
const DEFAULT_CACHE_SECONDS = 8;
const DEFAULT_MODALITY_LEARN_BODY_BYTES = 2097152;
const DEFAULT_RETRY_STATUSES = [502, 503, 504];
const PUBLIC_EDGE_HEALTH_ERROR = "origin health did not prove public edge controls";
const HOP_BY_HOP_HEADERS = new Set([
  "connection",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailer",
  "transfer-encoding",
  "upgrade",
]);
const MODEL_MODALITY_VALUES = new Set(["text", "image", "audio", "video", "document"]);

let cachedHealth = {
  expiresAt: 0,
  checks: [],
};

function parseOrigins(env) {
  const raw = (env.SAGE_ROUTER_ORIGINS || "").trim();
  if (raw) {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      throw new Error("SAGE_ROUTER_ORIGINS must be a JSON array");
    }
    return parsed.map(normalizeOrigin);
  }

  const legacy = (env.SAGE_ROUTER_EDGE_ORIGIN || "").trim();
  if (legacy) {
    return [normalizeOrigin({ name: "tailnet-edge", url: legacy, healthPath: "/edge/health" })];
  }

  throw new Error("SAGE_ROUTER_ORIGINS is not configured");
}

function normalizeOrigin(origin) {
  if (!origin || !origin.url) {
    throw new Error("each origin needs a url");
  }
  const url = new URL(origin.url);
  url.pathname = url.pathname.replace(/\/+$/, "");
  url.search = "";
  url.hash = "";
  return {
    name: origin.name || url.hostname,
    url: url.toString().replace(/\/$/, ""),
    healthPath: origin.healthPath || "/health",
    timeoutMs: Number(origin.timeoutMs || DEFAULT_TIMEOUT_MS),
  };
}

function originTarget(origin, incomingUrl) {
  return new URL(incomingUrl.pathname + incomingUrl.search, origin.url);
}

function truthyEnv(value, defaultValue = true) {
  if (value === undefined || value === null || value === "") {
    return defaultValue;
  }
  return !["0", "false", "no", "off"].includes(String(value).trim().toLowerCase());
}

function modelModalitiesSharedEnabled(env) {
  return truthyEnv(env.SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED, true)
    && !!env.SAGE_ROUTER_SUPABASE_URL
    && !!env.SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY;
}

function modelModalitiesState(env) {
  const rpcName = String(env.SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC || "sage_router_record_model_modalities").trim();
  return {
    sharedEnabled: modelModalitiesSharedEnabled(env) && !!rpcName,
    supabaseConfigured: !!env.SAGE_ROUTER_SUPABASE_URL && !!env.SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY,
    rpcConfigured: !!rpcName,
  };
}

function normalizeModelModalities(value) {
  const values = Array.isArray(value) ? value : String(value || "").split(",");
  return [...new Set(values
    .map((item) => String(item || "").trim().toLowerCase())
    .filter((item) => MODEL_MODALITY_VALUES.has(item)))]
    .sort();
}

function requestModalitiesFromBodyText(bodyText) {
  const modalities = new Set(["text"]);
  if (!bodyText) {
    return [...modalities].sort();
  }
  let payload;
  try {
    payload = JSON.parse(bodyText);
  } catch (_error) {
    return [...modalities].sort();
  }
  const visit = (value) => {
    if (Array.isArray(value)) {
      value.forEach(visit);
      return;
    }
    if (value && typeof value === "object") {
      const keys = new Set(Object.keys(value).map((key) => String(key).toLowerCase()));
      const type = String(value.type || "").toLowerCase();
      if (type === "image_url" || type === "input_image" || keys.has("image_url")) {
        modalities.add("image");
      }
      if (type === "input_audio" || type === "audio" || keys.has("audio_url") || keys.has("input_audio")) {
        modalities.add("audio");
      }
      if (type === "input_video" || type === "video" || keys.has("video_url") || keys.has("input_video")) {
        modalities.add("video");
      }
      if (type === "input_file" || type === "file" || type === "document" || keys.has("file_id") || keys.has("document")) {
        modalities.add("document");
      }
      Object.values(value).forEach(visit);
      return;
    }
    if (typeof value === "string") {
      const lowered = value.toLowerCase();
      if (lowered.startsWith("data:image/")) modalities.add("image");
      if (lowered.startsWith("data:audio/")) modalities.add("audio");
      if (lowered.startsWith("data:video/")) modalities.add("video");
    }
  };
  visit(payload);
  return [...modalities].sort();
}

async function boundedStreamText(stream, maxBytes) {
  if (!stream || typeof stream.getReader !== "function") {
    return "";
  }
  const reader = stream.getReader();
  const chunks = [];
  let received = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }
    received += value.byteLength;
    if (received > maxBytes) {
      await reader.cancel();
      return "";
    }
    chunks.push(value);
  }
  const buffer = new Uint8Array(received);
  let offset = 0;
  for (const chunk of chunks) {
    buffer.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(buffer);
}

async function boundedText(response, maxBytes) {
  const length = Number(response.headers.get("content-length") || 0);
  const type = String(response.headers.get("content-type") || "").toLowerCase();
  if (length > maxBytes || !type.includes("application/json") || response.headers.has("content-encoding")) {
    return "";
  }
  return boundedStreamText(response.body, maxBytes);
}

function modalityRecordFromResponse(headers, status, requestBodyText = "", responseBodyText = "") {
  if (!(Number(status || 0) >= 200 && Number(status || 0) < 300)) {
    return null;
  }
  let provider = (headers.get("x-sage-router-provider") || "").trim();
  let model = (headers.get("x-sage-router-model-name") || "").trim();
  const modelHeader = (headers.get("x-sage-router-model") || "").trim();
  if (!model && modelHeader.includes("/")) {
    const parts = modelHeader.split("/");
    provider = provider || parts.shift().trim();
    model = parts.join("/").trim();
  } else if (!model) {
    model = modelHeader;
  }
  if ((!provider || !model) && responseBodyText) {
    try {
      const payload = JSON.parse(responseBodyText);
      const responseModel = String((payload && payload.model) || "").trim();
      if (responseModel.includes("/")) {
        const parts = responseModel.split("/");
        provider = provider || parts.shift().trim();
        model = model || parts.join("/").trim();
      } else if (responseModel) {
        model = model || responseModel;
      }
    } catch (_error) {}
  }
  const modalities = normalizeModelModalities(headers.get("x-sage-router-modalities") || "")
    .concat(headers.get("x-sage-router-modalities") ? [] : requestModalitiesFromBodyText(requestBodyText));
  if (!provider || !model || !modalities.length) {
    return null;
  }
  return { provider, model, modalities: normalizeModelModalities(modalities) };
}

function modalityRecordFromResponseHeaders(headers, status) {
  return modalityRecordFromResponse(headers, status);
}

function applyModalityHeaders(headers, record) {
  if (!record) {
    return;
  }
  if (!headers.has("x-sage-router-provider")) {
    headers.set("x-sage-router-provider", record.provider);
  }
  if (!headers.has("x-sage-router-model-name")) {
    headers.set("x-sage-router-model-name", record.model);
  }
  if (!headers.has("x-sage-router-model")) {
    headers.set("x-sage-router-model", `${record.provider}/${record.model}`);
  }
  if (!headers.has("x-sage-router-modalities")) {
    headers.set("x-sage-router-modalities", record.modalities.join(","));
  }
}

async function recordModelModalities(env, record) {
  if (!modelModalitiesSharedEnabled(env)) {
    return false;
  }
  if (!record) {
    return false;
  }
  const baseUrl = String(env.SAGE_ROUTER_SUPABASE_URL || "").replace(/\/+$/, "");
  const rpcName = env.SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC || "sage_router_record_model_modalities";
  const response = await fetch(`${baseUrl}/rest/v1/rpc/${rpcName}`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY}`,
      apikey: env.SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      provider_name: record.provider,
      model_name: record.model,
      modalities_in: record.modalities,
      seen_at_epoch_ms: Date.now(),
    }),
  });
  return response.ok;
}

function privateHostname(hostname) {
  return hostname === "localhost"
    || hostname === "127.0.0.1"
    || hostname === "::1"
    || hostname.startsWith("10.")
    || hostname.startsWith("192.168.")
    || /^172\.(1[6-9]|2\d|3[0-1])\./.test(hostname)
    || /^100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\./.test(hostname);
}

function originKind(originUrl) {
  try {
    const hostname = new URL(originUrl).hostname.toLowerCase();
    if (hostname.endsWith(".ts.net")) {
      return "tailnet";
    }
    if (privateHostname(hostname)) {
      return "private";
    }
    if (hostname.endsWith(".run.app") || hostname.includes(".cloudfunctions.") || hostname.includes(".googleapis.")) {
      return "cloud fallback";
    }
    if (hostname.endsWith("sagerouter.dev")) {
      return "public edge";
    }
    return "public origin";
  } catch (_error) {
    return "unknown";
  }
}

function publicOriginId(index) {
  return `origin-${index + 1}`;
}

function publicOriginSnapshot(check, index) {
  return {
    id: publicOriginId(index),
    originKind: originKind(check.url),
    healthy: check.healthy,
    status: check.status,
    latencyMs: check.latencyMs,
    checkedAt: check.checkedAt,
    error: check.error || null,
  };
}

function publicOriginsSnapshot(checks) {
  return checks.map(publicOriginSnapshot);
}

function selectedOriginId(checks, selected) {
  if (!selected) {
    return null;
  }
  const index = checks.findIndex((check) => check.name === selected.name && check.url === selected.url);
  return index >= 0 ? publicOriginId(index) : null;
}

function retryStatuses(env) {
  const raw = String(env.SAGE_ROUTER_EDGE_RETRY_STATUSES || DEFAULT_RETRY_STATUSES.join(","));
  const statuses = raw
    .split(",")
    .map((item) => Number(String(item || "").trim()))
    .filter((status) => Number.isInteger(status) && status >= 400 && status <= 599);
  return new Set(statuses.length ? statuses : DEFAULT_RETRY_STATUSES);
}

function shouldRetryOriginStatus(env, status) {
  return retryStatuses(env).has(Number(status || 0));
}

function retryCountFromFailedAttempts(failedAttempts, finalResponseReturned) {
  if (finalResponseReturned) {
    return failedAttempts.length;
  }
  return Math.max(0, failedAttempts.length - 1);
}

function sortedHealthyChecks(checks) {
  return checks
    .filter((check) => check.healthy)
    .sort((a, b) => (a.latencyMs ?? Number.MAX_SAFE_INTEGER) - (b.latencyMs ?? Number.MAX_SAFE_INTEGER));
}

function originForCheck(origins, check) {
  return origins.find((candidate) => candidate.name === check.name && candidate.url === check.url);
}

function hasRawOriginUrl(value) {
  if (!value || typeof value !== "object") {
    return false;
  }
  if (Object.prototype.hasOwnProperty.call(value, "url") || Object.prototype.hasOwnProperty.call(value, "healthPath")) {
    return true;
  }
  return Object.values(value).some((item) => {
    if (Array.isArray(item)) {
      return item.some(hasRawOriginUrl);
    }
    return hasRawOriginUrl(item);
  });
}

function publicEdgeHealthSatisfied(payload) {
  if (!payload || typeof payload !== "object") {
    return false;
  }
  const enforcement = payload.enforcement || {};
  const failover = payload.failover || {};
  const modelModalities = payload.modelModalities || {};
  const retryStatuses = Array.isArray(failover.retryStatuses) ? failover.retryStatuses : [];
  return payload.status === "ok"
    && payload.authMode === "supabase"
    && enforcement.rateLimitEnabled === true
    && enforcement.authAttemptRateLimitEnabled === true
    && Number(enforcement.authAttemptRateLimit || 0) > 0
    && enforcement.quotaEnabled === true
    && Number(enforcement.apiKeyAuthCacheSeconds) === 0
    && enforcement.corsWildcardAllowed === false
    && enforcement.corsExplicitOriginRequired === true
    && Number(enforcement.corsAllowedOriginsCount || 0) > 0
    && failover.mode === "lowest-latency-healthy"
    && failover.retryEnabled === true
    && retryStatuses.includes(502)
    && retryStatuses.includes(503)
    && retryStatuses.includes(504)
    && failover.retryHeader === "X-Sage-Router-Retry-Count"
    && modelModalities.sharedEnabled === true
    && modelModalities.rpcConfigured === true
    && !hasRawOriginUrl(payload.upstreams || [])
    && !hasRawOriginUrl(payload.controlPlane || {});
}

async function timedFetch(url, init, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort("timeout"), timeoutMs);
  const started = Date.now();
  try {
    const response = await fetch(url, { ...init, signal: controller.signal });
    return {
      response,
      latencyMs: Date.now() - started,
    };
  } finally {
    clearTimeout(timer);
  }
}

async function checkOrigin(origin, requirePublicEdgeHealth) {
  const healthUrl = new URL(origin.healthPath, origin.url);
  try {
    const result = await timedFetch(healthUrl, {
      method: "GET",
      headers: {
        accept: "application/json",
        "cache-control": "no-cache",
        "user-agent": "sage-router-api-edge/1.0",
      },
      cf: {
        cacheTtl: 0,
        cacheEverything: false,
      },
    }, origin.timeoutMs);

    const body = await result.response.text();
    let health = null;
    try {
      health = body ? JSON.parse(body) : null;
    } catch (_error) {
      health = null;
    }
    const statusHealthy = result.response.status >= 200 && result.response.status < 300;
    const publicEdgeHealthy = !requirePublicEdgeHealth || publicEdgeHealthSatisfied(health);
    return {
      name: origin.name,
      url: origin.url,
      healthPath: origin.healthPath,
      healthy: statusHealthy && publicEdgeHealthy,
      status: result.response.status,
      latencyMs: result.latencyMs,
      checkedAt: new Date().toISOString(),
      error: statusHealthy && !publicEdgeHealthy ? PUBLIC_EDGE_HEALTH_ERROR : null,
    };
  } catch (error) {
    return {
      name: origin.name,
      url: origin.url,
      healthPath: origin.healthPath,
      healthy: false,
      status: 0,
      latencyMs: null,
      checkedAt: new Date().toISOString(),
      error: String(error && error.message ? error.message : error),
    };
  }
}

async function getHealth(env, force = false) {
  const now = Date.now();
  if (!force && cachedHealth.expiresAt > now && cachedHealth.checks.length) {
    return cachedHealth.checks;
  }

  const origins = parseOrigins(env);
  const requirePublicEdgeHealth = truthyEnv(env.SAGE_ROUTER_REQUIRE_PUBLIC_EDGE_HEALTH, true);
  const checks = await Promise.all(origins.map((origin) => checkOrigin(origin, requirePublicEdgeHealth)));
  cachedHealth = {
    checks,
    expiresAt: now + Number(env.SAGE_ROUTER_ORIGIN_CACHE_SECONDS || DEFAULT_CACHE_SECONDS) * 1000,
  };
  return checks;
}

async function chooseOriginCandidates(env) {
  const origins = parseOrigins(env);
  const checks = await getHealth(env);
  const candidates = sortedHealthyChecks(checks)
    .map((check) => ({
      check,
      origin: originForCheck(origins, check),
      originId: selectedOriginId(checks, check),
      originKind: originKind(check.url),
    }))
    .filter((candidate) => candidate.origin);
  return { candidates, checks };
}

function responseJson(payload, status = 200, extraHeaders = {}) {
  return Response.json(payload, {
    status,
    headers: {
      "cache-control": "no-store",
      "x-sage-router-cloudflare-edge": "api.sagerouter.dev",
      ...extraHeaders,
    },
  });
}

function outboundHeaders(request, selectedOriginId) {
  const headers = new Headers(request.headers);
  for (const header of HOP_BY_HOP_HEADERS) {
    headers.delete(header);
  }
  headers.delete("host");
  headers.set("x-sage-router-cloudflare-edge", "api.sagerouter.dev");
  headers.set("x-sage-router-origin", selectedOriginId || "origin-unknown");
  return headers;
}

export default {
  async fetch(request, env, ctx) {
    try {
      const incoming = new URL(request.url);
      if (incoming.pathname === "/edge/health") {
        const checks = await getHealth(env, incoming.searchParams.get("refresh") === "1");
        const healthy = sortedHealthyChecks(checks);
        const selectedId = selectedOriginId(checks, healthy[0]);
        return responseJson({
          status: healthy.length ? "ok" : "degraded",
          selected: selectedId,
          selectedOriginId: selectedId,
          origins: publicOriginsSnapshot(checks),
          failover: {
            mode: "lowest-latency-healthy",
            retryEnabled: healthy.length > 1,
            retryStatuses: [...retryStatuses(env)].sort((a, b) => a - b),
            retryHeader: "X-Sage-Router-Retry-Count",
            replayableBodyRequired: true,
          },
          modelModalities: modelModalitiesState(env),
        }, healthy.length ? 200 : 503, {
          "x-sage-router-api-origin": selectedId || "origin-none",
          "x-sage-router-api-origin-kind": healthy[0] ? originKind(healthy[0].url) : "none",
        });
      }

      const { candidates, checks } = await chooseOriginCandidates(env);
      if (!candidates.length) {
        return responseJson({ error: "no healthy sage-router origins", origins: publicOriginsSnapshot(checks) }, 503);
      }

      const maxModalityBodyBytes = Number(env.SAGE_ROUTER_EDGE_MODALITY_LEARN_BODY_BYTES || DEFAULT_MODALITY_LEARN_BODY_BYTES);
      let requestBodyText = "";
      let requestForOrigin = request;
      const methodHasBody = request.method !== "GET" && request.method !== "HEAD";
      let replayableBody = !methodHasBody;
      let bufferedBody = undefined;
      if (methodHasBody) {
        const requestLengthHeader = request.headers.get("content-length");
        const requestLength = Number(requestLengthHeader || 0);
        const requestLengthKnown = requestLengthHeader !== null && requestLengthHeader !== "";
        const requestType = String(request.headers.get("content-type") || "").toLowerCase();
        replayableBody = requestLengthKnown && requestLength === 0;
        bufferedBody = replayableBody ? "" : undefined;
        if ((!requestLengthKnown || requestLength <= maxModalityBodyBytes) && requestType.includes("application/json")) {
          requestForOrigin = request.clone();
          requestBodyText = await boundedStreamText(request.clone().body, maxModalityBodyBytes);
          if (requestBodyText || !requestLengthKnown || requestLength > 0) {
            replayableBody = true;
            bufferedBody = requestBodyText;
          }
        }
      }

      const retryableCandidates = replayableBody ? candidates : candidates.slice(0, 1);
      const failedAttempts = [];
      for (let index = 0; index < retryableCandidates.length; index += 1) {
        const candidate = retryableCandidates[index];
        const { origin, originId, originKind: selectedKind } = candidate;
        const target = originTarget(origin, incoming);
        const body = !methodHasBody ? undefined : (replayableBody ? bufferedBody : requestForOrigin.body);
        let response;
        try {
          response = await timedFetch(target, {
            method: request.method,
            headers: outboundHeaders(request, originId),
            body,
            redirect: "manual",
          }, origin.timeoutMs);
        } catch (error) {
          failedAttempts.push({
            originId,
            originKind: selectedKind || "unknown",
            status: 0,
            latencyMs: null,
            error: "origin fetch failed",
          });
          if (index < retryableCandidates.length - 1) {
            continue;
          }
          return responseJson({
            error: "all healthy sage-router origins failed",
            attempts: failedAttempts,
          }, 502, {
            "x-sage-router-api-origin": originId || "origin-unknown",
            "x-sage-router-api-origin-kind": selectedKind || "unknown",
            "x-sage-router-retry-count": String(retryCountFromFailedAttempts(failedAttempts, false)),
          });
        }

        if (index < retryableCandidates.length - 1 && shouldRetryOriginStatus(env, response.response.status)) {
          failedAttempts.push({
            originId,
            originKind: selectedKind || "unknown",
            status: response.response.status,
            latencyMs: response.latencyMs,
            error: "retryable origin response",
          });
          continue;
        }

        const headers = new Headers(response.response.headers);
        for (const header of HOP_BY_HOP_HEADERS) {
          headers.delete(header);
        }
        headers.set("x-sage-router-api-origin", originId || "origin-unknown");
        headers.set("x-sage-router-api-origin-kind", selectedKind || "unknown");
        headers.set("x-sage-router-api-origin-latency-ms", String(response.latencyMs));
        headers.set("x-sage-router-retry-count", String(retryCountFromFailedAttempts(failedAttempts, true)));
        const responseBodyTextPromise = boundedText(response.response.clone(), maxModalityBodyBytes)
          .catch(() => "");
        const modalityRecordPromise = responseBodyTextPromise
          .then((responseBodyText) => modalityRecordFromResponse(headers, response.response.status, requestBodyText, responseBodyText));
        const modalityRecord = modalityRecordPromise
          .then((record) => recordModelModalities(env, record))
          .catch((error) => console.log("sage-router modality edge record failed", error && error.message ? error.message : error));
        if (ctx && typeof ctx.waitUntil === "function") {
          ctx.waitUntil(modalityRecord);
        } else {
          await modalityRecord;
        }
        if (!headers.has("x-sage-router-modalities")) {
          applyModalityHeaders(headers, await modalityRecordPromise);
        }
        return new Response(response.response.body, {
          status: response.response.status,
          statusText: response.response.statusText,
          headers,
        });
      }

      return responseJson({ error: "all healthy sage-router origins failed", attempts: failedAttempts }, 502, {
        "x-sage-router-retry-count": String(retryCountFromFailedAttempts(failedAttempts, false)),
      });
    } catch (error) {
      return responseJson({
        error: "sage-router api edge failed",
        detail: String(error && error.message ? error.message : error),
      }, 500);
    }
  },
};
