import { normalizeAccountContext } from "./account.js";
import type { WTTCommandExecutionContext, WTTFetchLike, WTTFetchResponseLike } from "./types.js";

const DEFAULT_TIMEOUT_MS = 12_000;

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

export type WTTApiErrorCode =
  | "UNAUTHORIZED"
  | "ENDPOINT_UNAVAILABLE"
  | "HTTP_ERROR"
  | "NETWORK_ERROR"
  | "TIMEOUT";

export class WTTApiError extends Error {
  code: WTTApiErrorCode;
  status?: number;
  endpoint?: string;
  tried?: string[];

  constructor(
    code: WTTApiErrorCode,
    message: string,
    opts?: { status?: number; endpoint?: string; tried?: string[] },
  ) {
    super(message);
    this.name = "WTTApiError";
    this.code = code;
    this.status = opts?.status;
    this.endpoint = opts?.endpoint;
    this.tried = opts?.tried;
  }
}

interface ApiRequestOptions {
  method: HttpMethod;
  path: string;
  fallbackPaths?: string[];
  query?: Record<string, string | number | boolean | undefined>;
  body?: unknown;
  timeoutMs?: number;
}

function defaultFetchImpl(input: string, init?: Parameters<typeof fetch>[1]) {
  return fetch(input, init);
}

function hasJsonContentType(resp: WTTFetchResponseLike): boolean {
  const headers = resp as unknown as { headers?: { get?: (name: string) => string | null } };
  const contentType = headers.headers?.get?.("content-type") ?? "";
  return contentType.toLowerCase().includes("application/json");
}

async function parseResponseBody(resp: WTTFetchResponseLike): Promise<unknown> {
  if (resp.status === 204) return {};

  if (hasJsonContentType(resp)) {
    try {
      return await resp.json();
    } catch {
      // fall through to text
    }
  }

  const text = await resp.text();
  if (!text) return {};

  try {
    return JSON.parse(text);
  } catch {
    return { message: text };
  }
}

function extractErrorMessage(payload: unknown): string {
  if (typeof payload === "string" && payload.trim()) return payload.trim();

  if (typeof payload === "object" && payload !== null) {
    const data = payload as Record<string, unknown>;
    const detail = data.detail;

    if (typeof detail === "string" && detail.trim()) return detail.trim();
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0];
      if (typeof first === "string" && first.trim()) return first.trim();
      if (typeof first === "object" && first !== null) {
        const msg = (first as Record<string, unknown>).msg;
        if (typeof msg === "string" && msg.trim()) return msg.trim();
      }
    }

    for (const key of ["error", "message", "msg", "reason"]) {
      const value = data[key];
      if (typeof value === "string" && value.trim()) return value.trim();
    }
  }

  return "服务端返回异常";
}

function toQueryString(query?: Record<string, string | number | boolean | undefined>): string {
  if (!query) return "";

  const params = new URLSearchParams();
  for (const [k, v] of Object.entries(query)) {
    if (v === undefined) continue;
    params.set(k, String(v));
  }

  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

function withApiPrefixCandidates(path: string): string[] {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  const candidates = new Set<string>([normalized]);

  if (!normalized.startsWith("/api/")) {
    candidates.add(`/api${normalized}`);
    candidates.add(`/api/v1${normalized}`);
  }

  return Array.from(candidates);
}

function isAbortError(error: unknown): boolean {
  if (!(error instanceof Error)) return false;
  return error.name === "AbortError" || /aborted/i.test(error.message);
}

export async function wttApiRequestJson(
  ctx: WTTCommandExecutionContext,
  options: ApiRequestOptions,
): Promise<unknown> {
  const account = normalizeAccountContext(ctx.accountId, ctx.account);
  const fetchImpl: WTTFetchLike = ctx.fetchImpl ?? (defaultFetchImpl as WTTFetchLike);

  const headers: Record<string, string> = {
    Accept: "application/json",
  };
  if (options.body !== undefined) headers["Content-Type"] = "application/json";
  if (account.hasToken) {
    headers.Authorization = `Bearer ${account.token}`;
    headers["X-Agent-Token"] = account.token;
  }

  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const pathCandidates = [
    ...withApiPrefixCandidates(options.path),
    ...(options.fallbackPaths ?? []),
  ];

  const tried: string[] = [];

  for (const path of pathCandidates) {
    const query = toQueryString(options.query);
    const endpoint = `${account.cloudUrl.replace(/\/$/, "")}${path}${query}`;
    tried.push(endpoint);

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const resp = await fetchImpl(endpoint, {
        method: options.method,
        headers,
        body: options.body === undefined ? undefined : JSON.stringify(options.body),
        signal: controller.signal,
      });
      const payload = await parseResponseBody(resp);

      if (resp.ok) return payload;

      if (resp.status === 401 || resp.status === 403) {
        throw new WTTApiError("UNAUTHORIZED", "鉴权失败", {
          status: resp.status,
          endpoint,
          tried,
        });
      }

      if (resp.status === 404 || resp.status === 405) {
        continue;
      }

      const msg = extractErrorMessage(payload);
      throw new WTTApiError("HTTP_ERROR", msg, {
        status: resp.status,
        endpoint,
        tried,
      });
    } catch (error) {
      if (error instanceof WTTApiError) {
        if (error.code === "HTTP_ERROR" || error.code === "UNAUTHORIZED") throw error;
        continue;
      }

      if (isAbortError(error)) {
        throw new WTTApiError("TIMEOUT", "请求超时", { endpoint, tried });
      }

      const msg = error instanceof Error ? error.message : String(error);
      throw new WTTApiError("NETWORK_ERROR", msg, { endpoint, tried });
    } finally {
      clearTimeout(timer);
    }
  }

  throw new WTTApiError(
    "ENDPOINT_UNAVAILABLE",
    "服务端暂未暴露该接口",
    { tried },
  );
}

export function formatApiError(actionLabel: string, error: unknown): string {
  if (error instanceof WTTApiError) {
    if (error.code === "UNAUTHORIZED") {
      return `${actionLabel}失败：鉴权失败（401/403），请检查 token 配置。`;
    }
    if (error.code === "ENDPOINT_UNAVAILABLE") {
      const hint = error.tried?.length
        ? `\n已尝试：${error.tried.map((url) => url.replace(/^https?:\/\//, "")).join(" | ")}`
        : "";
      return `${actionLabel}暂不可用：当前后端未提供该 API。${hint}`;
    }
    if (error.code === "TIMEOUT") {
      return `${actionLabel}失败：请求超时，请稍后重试。`;
    }
    if (error.code === "NETWORK_ERROR") {
      return `${actionLabel}失败：网络异常（${error.message}）。`;
    }

    const statusText = error.status ? `（HTTP ${error.status}）` : "";
    return `${actionLabel}失败${statusText}：${error.message}`;
  }

  const msg = error instanceof Error ? error.message : String(error);
  return `${actionLabel}失败：${msg}`;
}
