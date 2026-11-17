// HTTP layer for the tokei-agent CLI: URL construction, bearer auth,
// rate-limit header extraction, and error mapping. The caller injects a
// `fetch`-like implementation so tests never touch the network.

export interface HttpResponse {
  status: number;
  headers: { get(name: string): string | null };
  text(): Promise<string>;
}

export type FetchLike = (
  url: string,
  init: { method: string; headers: Record<string, string>; body?: string },
) => Promise<HttpResponse>;

export interface RateLimit {
  limit: number;
  remaining: number;
  reset: number;
}

export type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

// Separate from FetchLike (it carries a Uint8Array body — the multipart upload
// in media.ts): widening FetchLike's `body` to `string | Uint8Array` would
// break the ~31 existing `JSON.parse(init.body!)` test assertions across the
// suite via arrow-type contravariance. Kept side-by-side instead.
export type BinaryFetchLike = (
  url: string,
  init: { method: string; headers: Record<string, string>; body: Uint8Array },
) => Promise<HttpResponse>;

export interface RequestOptions {
  baseUrl: string;
  apiKey: string;
  path: string;
  query?: Record<string, string>;
  method?: HttpMethod;
  // JSON-serialised as the request body when defined. The CLI passes user
  // JSON through untouched — the API's 422 per-field errors are the
  // validation story.
  body?: unknown;
}

export interface RequestResult {
  payload: unknown;
  exitCode: 0 | 1;
  // HTTP status, or undefined when the request never reached a response
  // (network/DNS/timeout). Presentation-only: lets the interactive UI describe
  // a failure accurately instead of guessing. Never affects payload or exit
  // code.
  status?: number;
}

function extractRateLimit(res: HttpResponse): RateLimit | null {
  const limit = res.headers.get("X-RateLimit-Limit");
  const remaining = res.headers.get("X-RateLimit-Remaining");
  const reset = res.headers.get("X-RateLimit-Reset");
  if (limit === null || remaining === null || reset === null) return null;
  return { limit: Number(limit), remaining: Number(remaining), reset: Number(reset) };
}

function augment(body: unknown, rateLimit: RateLimit | null): unknown {
  if (body !== null && typeof body === "object" && !Array.isArray(body)) {
    return { ...(body as Record<string, unknown>), rate_limit: rateLimit };
  }
  return { data: body, rate_limit: rateLimit };
}

function networkError(err: unknown): RequestResult {
  const message = err instanceof Error ? err.message : String(err);
  return { payload: { ok: false, error: { type: "network_error", message } }, exitCode: 1 };
}

/**
 * Status/JSON/rate-limit handling shared by every request shape, so a
 * multipart upload reports a 422 exactly the way a JSON call does.
 */
async function toResult(res: HttpResponse): Promise<RequestResult> {
  const rateLimit = extractRateLimit(res);
  const text = await res.text();

  let parsed: unknown;
  let isJson = true;
  try {
    parsed = text.length === 0 ? {} : JSON.parse(text);
  } catch {
    isJson = false;
  }

  const success = res.status >= 200 && res.status < 300;
  if (success || isJson) {
    return { payload: augment(parsed, rateLimit), exitCode: success ? 0 : 1, status: res.status };
  }

  return {
    payload: {
      ok: false,
      error: { type: "http_error", status: res.status, message: text },
      rate_limit: rateLimit,
    },
    exitCode: 1,
    status: res.status,
  };
}

/** RFC 7578 body with a single `file` part. Boundary is random per call. */
function buildMultipartBody(
  filename: string,
  contentType: string,
  bytes: Uint8Array,
): { body: Uint8Array; contentType: string } {
  const boundary = `----tokei${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;
  // A quote or newline in the name would break the header; the server never
  // builds a path from it, so sanitising is purely about a well-formed body.
  const safeName = filename.replace(/[\r\n"]/g, "_");
  const encoder = new TextEncoder();
  const head = encoder.encode(
    `--${boundary}\r\n` +
      `Content-Disposition: form-data; name="file"; filename="${safeName}"\r\n` +
      `Content-Type: ${contentType}\r\n\r\n`,
  );
  const tail = encoder.encode(`\r\n--${boundary}--\r\n`);

  const body = new Uint8Array(head.length + bytes.length + tail.length);
  body.set(head, 0);
  body.set(bytes, head.length);
  body.set(tail, head.length + bytes.length);

  return { body, contentType: `multipart/form-data; boundary=${boundary}` };
}

/**
 * POST file bytes to a v1 endpoint as `multipart/form-data` (media:upload).
 * Same base URL, bearer auth and error mapping as `request` — only the body
 * encoding differs.
 */
export async function requestMultipart(
  opts: {
    baseUrl: string;
    apiKey: string;
    path: string;
    filename: string;
    contentType: string;
    bytes: Uint8Array;
  },
  fetchImpl: BinaryFetchLike,
): Promise<RequestResult> {
  const base = opts.baseUrl.replace(/\/+$/, "");
  const { body, contentType } = buildMultipartBody(opts.filename, opts.contentType, opts.bytes);

  let res: HttpResponse;
  try {
    res = await fetchImpl(`${base}/api/v1${opts.path}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${opts.apiKey}`,
        Accept: "application/json",
        "Content-Type": contentType,
      },
      body,
    });
  } catch (err) {
    return networkError(err);
  }

  return toResult(res);
}

export async function request(
  opts: RequestOptions,
  fetchImpl: FetchLike,
): Promise<RequestResult> {
  const base = opts.baseUrl.replace(/\/+$/, "");
  let url = `${base}/api/v1${opts.path}`;
  if (opts.query && Object.keys(opts.query).length > 0) {
    const qs = new URLSearchParams(opts.query).toString();
    url += `?${qs}`;
  }

  const headers: Record<string, string> = {
    Authorization: `Bearer ${opts.apiKey}`,
    Accept: "application/json",
  };
  const init: { method: string; headers: Record<string, string>; body?: string } = {
    method: opts.method ?? "GET",
    headers,
  };
  if (opts.body !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(opts.body);
  }

  let res: HttpResponse;
  try {
    res = await fetchImpl(url, init);
  } catch (err) {
    return networkError(err);
  }

  return toResult(res);
}
