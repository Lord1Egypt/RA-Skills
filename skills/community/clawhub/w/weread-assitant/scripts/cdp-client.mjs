import fs from "node:fs/promises";

const DEFAULT_BASE_URL = process.env.WEREAD_CDP_BASE || "http://localhost:3456";

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function parseResponse(response) {
  const text = await response.text();

  if (!response.ok) {
    throw new Error(`CDP request failed (${response.status}): ${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export function unwrapValue(payload) {
  if (payload == null) return payload;
  if (typeof payload !== "object") return payload;
  if ("result" in payload) return unwrapValue(payload.result);
  if ("value" in payload) return unwrapValue(payload.value);
  if ("data" in payload) return unwrapValue(payload.data);
  return payload;
}

export async function cdpRequest(path, { method = "GET", body, headers = {}, baseUrl = DEFAULT_BASE_URL } = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    method,
    body,
    headers,
  });

  return parseResponse(response);
}

export async function listTargets() {
  return cdpRequest("/targets");
}

export async function createTarget(url) {
  return unwrapValue(await cdpRequest(`/new?url=${encodeURIComponent(url)}`));
}

export async function closeTarget(targetId) {
  return cdpRequest(`/close?target=${encodeURIComponent(targetId)}`);
}

export async function navigateTarget(targetId, url) {
  return cdpRequest(`/navigate?target=${encodeURIComponent(targetId)}&url=${encodeURIComponent(url)}`);
}

export async function infoTarget(targetId) {
  return unwrapValue(await cdpRequest(`/info?target=${encodeURIComponent(targetId)}`));
}

export async function scrollTarget(targetId, { y, direction } = {}) {
  const params = new URLSearchParams({ target: targetId });
  if (typeof y === "number") params.set("y", String(y));
  if (direction) params.set("direction", direction);
  return cdpRequest(`/scroll?${params.toString()}`);
}

export async function screenshotTarget(targetId, filePath) {
  await fs.mkdir(new URL(".", `file://${filePath}`).pathname, { recursive: true }).catch(() => {});
  return cdpRequest(`/screenshot?target=${encodeURIComponent(targetId)}&file=${encodeURIComponent(filePath)}`);
}

export async function evalTarget(targetId, expression) {
  const payload = await cdpRequest(`/eval?target=${encodeURIComponent(targetId)}`, {
    method: "POST",
    body: expression,
    headers: { "content-type": "text/plain; charset=utf-8" },
  });

  return unwrapValue(payload);
}

export async function withNewTarget(url, fn, { keepOpen = false } = {}) {
  const created = await createTarget(url);
  const targetId =
    typeof created === "string"
      ? created
      : created?.targetId || created?.id || created?.target?.id || created?.targetId;

  if (!targetId) {
    throw new Error(`Could not determine target id from /new response: ${JSON.stringify(created)}`);
  }

  try {
    return await fn(targetId);
  } finally {
    if (!keepOpen) {
      await closeTarget(targetId).catch(() => {});
    }
  }
}
