export const API_BASE_URL = "https://ai.redreplier.com/ai-app/api/v1";
const TOKEN_PREFIX = "redreplier_";

export type PluginConfig = { apiToken?: string };

export function readConfig(api: { config?: unknown }): PluginConfig {
  const root = api.config as
    | { plugins?: { entries?: Record<string, { config?: PluginConfig }> } }
    | undefined;
  return root?.plugins?.entries?.["redreplier"]?.config ?? {};
}

function requireToken(cfg: PluginConfig): string {
  if (!cfg.apiToken) {
    throw new Error(
      "No RedReplier API token configured. Set plugins.entries.redreplier.config.apiToken. Create a token at https://redreplier.com under Settings then API Tokens.",
    );
  }
  if (!cfg.apiToken.startsWith(TOKEN_PREFIX)) {
    throw new Error(
      `RedReplier API tokens start with "${TOKEN_PREFIX}". The configured value does not, so the API will reject it.`,
    );
  }
  return cfg.apiToken;
}

function buildQuery(params: Record<string, unknown>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null) continue;
    if (Array.isArray(value)) {
      for (const item of value) search.append(key, String(item));
    } else {
      search.append(key, String(value));
    }
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

export async function callApi(
  cfg: PluginConfig,
  method: "GET" | "POST" | "PATCH" | "DELETE",
  path: string,
  options: { body?: unknown; query?: Record<string, unknown>; signal?: AbortSignal } = {},
): Promise<unknown> {
  const token = requireToken(cfg);
  const url = `${API_BASE_URL}${path}${options.query ? buildQuery(options.query) : ""}`;

  const res = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
    redirect: "error",
    signal: options.signal,
  });

  const text = await res.text();
  let parsed: unknown = text;
  try {
    parsed = text ? JSON.parse(text) : null;
  } catch {
    /* non-JSON error body */
  }

  if (!res.ok) {
    if (res.status === 429) {
      const retryAfter = res.headers.get("Retry-After");
      throw new Error(
        `RedReplier rate limit reached (600 requests per minute per token).${retryAfter ? ` Retry after ${retryAfter}s.` : ""} Wait rather than retrying immediately.`,
      );
    }
    const message =
      typeof parsed === "object" && parsed !== null && "message" in parsed
        ? String((parsed as { message: unknown }).message)
        : typeof parsed === "string"
          ? parsed
          : JSON.stringify(parsed);
    throw new Error(`RedReplier API ${res.status}: ${message}`);
  }

  return parsed;
}
