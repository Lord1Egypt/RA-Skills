import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
let cachedCurlAvailability;

async function hasCurl() {
  if (cachedCurlAvailability !== undefined) {
    return cachedCurlAvailability;
  }

  try {
    await execFileAsync("curl", ["--version"], { maxBuffer: 1024 * 1024 });
    cachedCurlAvailability = true;
  } catch {
    cachedCurlAvailability = false;
  }

  return cachedCurlAvailability;
}

async function requestTextViaCurl(url, options) {
  const marker = "__WEB_SEARCH_PRO_META__";
  const headers = options.headers ?? {};
  const timeoutSeconds = Math.max(1, Math.ceil((options.timeoutMs ?? 20000) / 1000));
  const args = [
    "-sS",
    "--max-redirs",
    "0",
    "--max-time",
    String(timeoutSeconds),
    "-X",
    options.method ?? "GET",
  ];

  for (const [name, value] of Object.entries(headers)) {
    args.push("-H", `${name}: ${value}`);
  }
  if (options.body !== undefined && options.body !== null) {
    args.push("--data", options.body);
  }

  args.push("--write-out", `\n${marker}%{http_code}|%{content_type}|%{redirect_url}`);
  args.push(url);

  const { stdout, stderr } = await execFileAsync("curl", args, {
    maxBuffer: 10 * 1024 * 1024,
    timeout: options.timeoutMs ?? 20000,
  });

  const markerIndex = stdout.lastIndexOf(`\n${marker}`);
  if (markerIndex === -1) {
    throw new Error("curl response metadata missing");
  }

  const body = stdout.slice(0, markerIndex);
  const meta = stdout.slice(markerIndex + marker.length + 1).trim();
  const [statusRaw, contentType = "", redirectUrl = ""] = meta.split("|");
  const status = Number.parseInt(statusRaw, 10);

  if (!Number.isInteger(status)) {
    throw new Error(stderr.trim() || "curl returned an invalid status");
  }

  return {
    status,
    body,
    contentType,
    redirectUrl,
  };
}

async function requestTextViaFetch(url, options) {
  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), options.timeoutMs ?? 20000);

  const response = await fetch(url, {
    method: options.method ?? "GET",
    headers: options.headers,
    body: options.body,
    redirect: "manual",
    signal: abortController.signal,
  }).finally(() => {
    clearTimeout(timeout);
  });

  return {
    status: response.status,
    body: await response.text(),
    contentType: response.headers.get("content-type") ?? "",
    redirectUrl: response.headers.get("location") ?? "",
  };
}

export async function requestText(url, options = {}) {
  if (options.transport === "fetch") {
    return requestTextViaFetch(url, options);
  }
  if (options.transport === "curl") {
    return requestTextViaCurl(url, options);
  }
  if (await hasCurl()) {
    return requestTextViaCurl(url, options);
  }
  return requestTextViaFetch(url, options);
}
