import { HttpError } from "./errors.js";

export async function callRapidApi(input, rapidApiKey, allowNonRapidApiHosts, defaultTimeoutMs) {
  const method = (input.method || "GET").toUpperCase();
  const meta = { host: input.host, path: input.path, method };

  if (!input.host || String(input.host).includes("/") || String(input.host).includes(":")) {
    throw new HttpError(400, "Invalid host");
  }

  if (!input.path || !String(input.path).startsWith("/")) {
    throw new HttpError(400, "Path must start with '/' ");
  }

  if (!allowNonRapidApiHosts) {
    const host = String(input.host);
    const isRapidApiHost =
      host.endsWith(".rapidapi.com") || host.endsWith(".p.rapidapi.com") || host === "rapidapi.com";
    if (!isRapidApiHost) {
      throw new HttpError(400, "Non-RapidAPI host blocked by policy");
    }
  }

  const url = new URL(`https://${input.host}${input.path}`);
  if (input.query) {
    for (const [key, value] of Object.entries(input.query)) {
      if (value === undefined || value === null) continue;
      url.searchParams.set(key, String(value));
    }
  }

  const headers = {
    "X-RapidAPI-Key": rapidApiKey,
    "X-RapidAPI-Host": input.host,
    ...(input.headers || {})
  };
  delete headers["x-rapidapi-key"];
  delete headers["X-RapidAPI-Key"];
  headers["X-RapidAPI-Key"] = rapidApiKey;

  const hasBody = !["GET", "DELETE"].includes(method);
  let body = undefined;

  if (hasBody && input.body !== undefined) {
    if (typeof input.body === "string" || input.body instanceof Uint8Array) {
      body = input.body;
    } else {
      if (!headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
      }
      body = JSON.stringify(input.body);
    }
  }

  const timeoutMs = input.timeoutMs ?? defaultTimeoutMs;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  let response;
  try {
    response = await fetch(url.toString(), { method, headers, body, signal: controller.signal });
  } finally {
    clearTimeout(id);
  }

  const contentType = response.headers.get("content-type") || "";
  let data = null;

  if (input.responseType === "text") {
    data = await response.text();
  } else if (input.responseType === "blob") {
    data = await response.arrayBuffer();
  } else if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    throw new HttpError(response.status, "RapidAPI error", data);
  }

  return {
    ok: true,
    status: response.status,
    data,
    meta
  };
}
