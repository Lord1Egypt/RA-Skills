import type { AnyAgentTool, OpenClawPluginApi } from "openclaw/plugin-sdk";

type PluginConfig = {
  baseUrl?: string;
  timeoutSeconds?: number;
  maxResults?: number;
  defaultLanguage?: string;
  defaultCategories?: string;
  defaultSafeSearch?: number;
};

type SearxngSearchResponse = {
  query?: string;
  number_of_results?: number;
  results?: Array<Record<string, unknown>>;
  answers?: unknown[];
  corrections?: unknown[];
  infoboxes?: unknown[];
  suggestions?: unknown[];
  unresponsive_engines?: unknown[];
};

const DEFAULT_BASE_URL = "http://127.0.0.1:8888";
const DEFAULT_TIMEOUT_SECONDS = 20;
const DEFAULT_MAX_RESULTS = 8;

function normalizeString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function normalizeNumber(value: unknown): number | undefined {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim()) {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) {
      return parsed;
    }
  }
  return undefined;
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function resolveConfig(
  api: OpenClawPluginApi,
): Required<Pick<PluginConfig, "baseUrl" | "timeoutSeconds" | "maxResults">> & PluginConfig {
  const raw = (api.pluginConfig ?? {}) as PluginConfig;
  return {
    ...raw,
    baseUrl: normalizeString(raw.baseUrl) ?? DEFAULT_BASE_URL,
    timeoutSeconds: clamp(
      normalizeNumber(raw.timeoutSeconds) ?? DEFAULT_TIMEOUT_SECONDS,
      1,
      120,
    ),
    maxResults: clamp(normalizeNumber(raw.maxResults) ?? DEFAULT_MAX_RESULTS, 1, 50),
  };
}

function createSearxngTool(api: OpenClawPluginApi): AnyAgentTool {
  return {
    name: "searxng_search",
    label: "SearXNG Search",
    description:
      "Search the web through your own SearXNG instance and return structured results to OpenClaw.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: {
          type: "string",
          description: "Search query.",
        },
        categories: {
          type: "string",
          description: "Optional SearXNG categories, comma-separated, for example general,it or news.",
        },
        language: {
          type: "string",
          description: "Optional SearXNG language code, for example auto, en, or en-US.",
        },
        safesearch: {
          type: "number",
          minimum: 0,
          maximum: 2,
          description: "Safe search level: 0 none, 1 moderate, 2 strict.",
        },
        pageno: {
          type: "number",
          minimum: 1,
          description: "Results page number.",
        },
        time_range: {
          type: "string",
          description: "Optional time range supported by SearXNG, for example day, month, or year.",
        },
        engines: {
          type: "array",
          items: { type: "string" },
          description: "Optional engine allowlist.",
        },
        limit: {
          type: "number",
          minimum: 1,
          maximum: 50,
          description: "Maximum number of results to return.",
        },
      },
      required: ["query"],
    },
    async execute(_id: string, params: Record<string, unknown>) {
      const cfg = resolveConfig(api);
      const query = normalizeString(params.query);
      if (!query) {
        throw new Error("query required");
      }

      const categories =
        normalizeString(params.categories) ?? normalizeString(cfg.defaultCategories);
      const language =
        normalizeString(params.language) ?? normalizeString(cfg.defaultLanguage);
      const safesearch =
        normalizeNumber(params.safesearch) ?? normalizeNumber(cfg.defaultSafeSearch);
      const pageno = clamp(normalizeNumber(params.pageno) ?? 1, 1, 100);
      const limit = clamp(normalizeNumber(params.limit) ?? cfg.maxResults, 1, 50);
      const timeRange = normalizeString(params.time_range);
      const engines = Array.isArray(params.engines)
        ? params.engines
            .map((entry) => normalizeString(entry))
            .filter((entry): entry is string => Boolean(entry))
        : [];

      const url = new URL("/search", cfg.baseUrl.endsWith("/") ? cfg.baseUrl : `${cfg.baseUrl}/`);
      url.searchParams.set("q", query);
      url.searchParams.set("format", "json");
      url.searchParams.set("pageno", String(pageno));
      if (categories) {
        url.searchParams.set("categories", categories);
      }
      if (language) {
        url.searchParams.set("language", language);
      }
      if (typeof safesearch === "number" && Number.isFinite(safesearch)) {
        url.searchParams.set("safesearch", String(clamp(safesearch, 0, 2)));
      }
      if (timeRange) {
        url.searchParams.set("time_range", timeRange);
      }
      if (engines.length > 0) {
        url.searchParams.set("engines", engines.join(","));
      }

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), cfg.timeoutSeconds * 1000);

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            accept: "application/json",
          },
          signal: controller.signal,
        });

        if (!response.ok) {
          const body = await response.text().catch(() => "");
          throw new Error(
            `SearXNG request failed: HTTP ${response.status}${body ? ` - ${body.slice(0, 300)}` : ""}`,
          );
        }

        const payload = (await response.json()) as SearxngSearchResponse;
        const results = Array.isArray(payload.results) ? payload.results.slice(0, limit) : [];

        return {
          query,
          source: cfg.baseUrl,
          resultCount: results.length,
          numberOfResults: payload.number_of_results,
          results: results.map((result) => ({
            title: typeof result.title === "string" ? result.title : undefined,
            url: typeof result.url === "string" ? result.url : undefined,
            content: typeof result.content === "string" ? result.content : undefined,
            engine: typeof result.engine === "string" ? result.engine : undefined,
            category: typeof result.category === "string" ? result.category : undefined,
            score: typeof result.score === "number" ? result.score : undefined,
            publishedDate:
              typeof result.publishedDate === "string"
                ? result.publishedDate
                : typeof result.published_date === "string"
                  ? result.published_date
                  : undefined,
          })),
          answers: Array.isArray(payload.answers) ? payload.answers : [],
          suggestions: Array.isArray(payload.suggestions) ? payload.suggestions : [],
          corrections: Array.isArray(payload.corrections) ? payload.corrections : [],
          infoboxes: Array.isArray(payload.infoboxes) ? payload.infoboxes : [],
          unresponsiveEngines: Array.isArray(payload.unresponsive_engines)
            ? payload.unresponsive_engines
            : [],
        };
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          throw new Error(`SearXNG request timed out after ${cfg.timeoutSeconds}s`);
        }
        throw error;
      } finally {
        clearTimeout(timer);
      }
    },
  } as AnyAgentTool;
}

export default function register(api: OpenClawPluginApi) {
  api.registerTool(createSearxngTool(api), { optional: true });
}
