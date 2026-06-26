const NATIVE_API_URL = "https://api.perplexity.ai/v1/sonar";
const OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions";
const KILO_API_URL = "https://api.kilo.ai/api/gateway/chat/completions";
const DEFAULT_NATIVE_MODEL = "sonar-pro";
const DEFAULT_GATEWAY_MODEL = "perplexity/sonar-pro";
const DEFAULT_OPENROUTER_MODEL = "perplexity/sonar";
const SONAR_MODEL_PATTERN = /^(?:perplexity\/)?(sonar(?:-[a-z0-9-]+)*)$/i;

function trimEnv(name, env = process.env) {
  const value = env[name];
  return typeof value === "string" ? value.trim() : "";
}

function normalizeCount(value, max = 20) {
  const n = Number.parseInt(String(value ?? 5), 10);
  if (!Number.isFinite(n)) return 5;
  return Math.max(1, Math.min(n, max));
}

function toUsDate(dateStr) {
  if (!dateStr) {
    return null;
  }
  const [year, month, day] = String(dateStr).split("-");
  if (!year || !month || !day) {
    return null;
  }
  return `${month}/${day}/${year}`;
}

function buildDomainFilter(opts = {}) {
  const include = [...(opts.includeDomains ?? [])];
  const exclude = [...(opts.excludeDomains ?? [])].map((domain) => `-${domain}`);
  const values = [...include, ...exclude];
  return values.length > 0 ? values : null;
}

function buildGatewayQuery(query, opts = {}) {
  const baseQuery = String(query ?? "").trim();
  const includeDomains = [...(opts.includeDomains ?? [])];
  const excludeDomains = [...(opts.excludeDomains ?? [])];
  const queryParts = [];

  if (includeDomains.length === 1) {
    queryParts.push(`site:${includeDomains[0]}`);
  } else if (includeDomains.length > 1) {
    queryParts.push(`(${includeDomains.map((domain) => `site:${domain}`).join(" OR ")})`);
  }

  queryParts.push(baseQuery);

  if (excludeDomains.length > 0) {
    queryParts.push(excludeDomains.map((domain) => `-site:${domain}`).join(" "));
  }

  return queryParts.filter(Boolean).join(" ").trim();
}

function buildGatewayConstraintText(opts = {}) {
  const constraints = [];

  if (opts.country) {
    constraints.push(`country=${String(opts.country).toUpperCase()}`);
  }
  if (opts.lang) {
    constraints.push(`language=${String(opts.lang)}`);
  }
  if (opts.timeRange) {
    constraints.push(`recency=${String(opts.timeRange)}`);
  }
  if (opts.fromDate || opts.toDate) {
    constraints.push(
      `publishedRange=${opts.fromDate ?? "*"}..${opts.toDate ?? "*"}`,
    );
  }

  return constraints.length > 0
    ? `Search constraints: ${constraints.join(", ")}. Honor them when gathering sources.`
    : "";
}

function stripCitationMarkers(text = "") {
  return String(text).replace(/\[(\d+)\]/g, "").trim();
}

function extractTextContent(value) {
  if (typeof value === "string") {
    return value;
  }
  if (!Array.isArray(value)) {
    return "";
  }
  return value
    .map((item) => {
      if (typeof item === "string") {
        return item;
      }
      if (item?.type === "text" && typeof item.text === "string") {
        return item.text;
      }
      if (typeof item?.content === "string") {
        return item.content;
      }
      return "";
    })
    .filter(Boolean)
    .join(" ")
    .trim();
}

function titleFromUrl(url) {
  try {
    const parsed = new URL(url);
    const pathSegments = parsed.pathname.split("/").filter(Boolean);
    const tail = pathSegments.at(-1);
    if (tail) {
      return tail
        .replace(/[-_]+/g, " ")
        .replace(/\.[a-z0-9]+$/i, "")
        .trim();
    }
    return parsed.hostname;
  } catch {
    return url;
  }
}

function normalizeSource(item) {
  if (!item) {
    return null;
  }

  if (typeof item === "string") {
    return {
      title: titleFromUrl(item),
      url: item,
      content: "",
      score: null,
      publishedDate: null,
      date: null,
    };
  }

  const url = item.url ?? item.link ?? item.uri ?? "";
  if (!url) {
    return null;
  }

  return {
    title: item.title ?? item.name ?? titleFromUrl(url),
    url,
    content: item.snippet ?? item.description ?? item.text ?? item.content ?? "",
    score: null,
    publishedDate:
      item.date ??
      item.last_updated ??
      item.published_at ??
      item.publishedDate ??
      null,
    date:
      item.date ??
      item.last_updated ??
      item.published_at ??
      item.publishedDate ??
      null,
  };
}

function normalizeAnnotation(annotation) {
  const citation = annotation?.url_citation;
  if (!citation?.url) {
    return null;
  }

  return {
    title: citation.title ?? titleFromUrl(citation.url),
    url: citation.url,
    content: "",
    score: null,
    publishedDate: null,
    date: null,
  };
}

function extractUrlsFromText(text = "") {
  const matches = String(text).match(/https?:\/\/[^\s)\]}>\"']+/g) ?? [];
  return Array.from(new Set(matches));
}

function dedupeSources(items = []) {
  const seen = new Set();
  const deduped = [];

  for (const item of items) {
    const normalized = normalizeSource(item);
    const url = normalized?.url ?? "";
    if (!url || seen.has(url)) {
      continue;
    }
    seen.add(url);
    deduped.push(normalized);
  }

  return deduped;
}

function normalizeGatewayUrl(value, fallback) {
  const base =
    String(value ?? "").trim() ||
    String(fallback ?? "").trim();
  if (!base) {
    return "";
  }
  if (/\/chat\/completions\/?$/i.test(base)) {
    return base.replace(/\/+$/, "");
  }
  return `${base.replace(/\/+$/, "")}/chat/completions`;
}

function normalizePerplexityModel(value, options = {}) {
  const transportId = options.transportId ?? "gateway";
  const fallback = options.fallback ?? "";
  const raw = String(value ?? "").trim();
  if (!raw) {
    return fallback;
  }

  const match = raw.match(SONAR_MODEL_PATTERN);
  if (!match) {
    throw new Error(
      `PERPLEXITY_MODEL must reference a Perplexity Sonar model; received "${raw}".`,
    );
  }

  const canonical = match[1].toLowerCase();
  if (transportId === "native") {
    return canonical;
  }
  return `perplexity/${canonical}`;
}

export function resolveTransport(env = process.env) {
  const explicitGatewayKey = trimEnv("PERPLEXITY_GATEWAY_API_KEY", env);
  const explicitGatewayBaseUrl = trimEnv("PERPLEXITY_BASE_URL", env);
  if (explicitGatewayKey && explicitGatewayBaseUrl) {
    return {
      id: "gateway",
      apiKey: explicitGatewayKey,
      apiUrl: normalizeGatewayUrl(explicitGatewayBaseUrl),
      model: normalizePerplexityModel(trimEnv("PERPLEXITY_MODEL", env), {
        transportId: "gateway",
        fallback: DEFAULT_GATEWAY_MODEL,
      }),
      supportsNativeFilters: false,
    };
  }

  const nativeKey = trimEnv("PERPLEXITY_API_KEY", env);
  if (nativeKey) {
    return {
      id: "native",
      apiKey: nativeKey,
      apiUrl: NATIVE_API_URL,
      model: normalizePerplexityModel(trimEnv("PERPLEXITY_MODEL", env), {
        transportId: "native",
        fallback: DEFAULT_NATIVE_MODEL,
      }),
      supportsNativeFilters: true,
    };
  }

  const openRouterKey = trimEnv("OPENROUTER_API_KEY", env);
  if (openRouterKey) {
    return {
      id: "openrouter",
      apiKey: openRouterKey,
      apiUrl: normalizeGatewayUrl(
        trimEnv("OPENROUTER_BASE_URL", env) || OPENROUTER_API_URL,
        OPENROUTER_API_URL,
      ),
      model: normalizePerplexityModel(trimEnv("PERPLEXITY_MODEL", env), {
        transportId: "openrouter",
        fallback: DEFAULT_OPENROUTER_MODEL,
      }),
      supportsNativeFilters: false,
    };
  }

  const kiloKey = trimEnv("KILOCODE_API_KEY", env);
  if (kiloKey) {
    return {
      id: "kilo",
      apiKey: kiloKey,
      apiUrl: KILO_API_URL,
      model: normalizePerplexityModel(trimEnv("PERPLEXITY_MODEL", env), {
        transportId: "kilo",
        fallback: DEFAULT_GATEWAY_MODEL,
      }),
      supportsNativeFilters: false,
    };
  }

  return null;
}

function buildNativeBody(query, opts = {}, transport) {
  const webSearchOptions = {};
  const recency = opts.timeRange ?? null;
  if (recency) {
    webSearchOptions.search_recency_filter = recency;
  }
  if (opts.fromDate) {
    webSearchOptions.search_after_date_filter = toUsDate(opts.fromDate);
  }
  if (opts.toDate) {
    webSearchOptions.search_before_date_filter = toUsDate(opts.toDate);
  }
  const domainFilter = buildDomainFilter(opts);
  if (domainFilter) {
    webSearchOptions.search_domain_filter = domainFilter;
  }
  if (opts.lang) {
    webSearchOptions.search_language_filter = [String(opts.lang)];
  }

  return {
    model: transport.model,
    messages: [
      {
        role: "system",
        content: "Answer with a concise factual summary and preserve source grounding.",
      },
      {
        role: "user",
        content: String(query ?? "").trim(),
      },
    ],
    temperature: 0.2,
    ...(Object.keys(webSearchOptions).length > 0
      ? { web_search_options: webSearchOptions }
      : {}),
  };
}

function buildGatewayBody(query, opts = {}, transport) {
  const scopedQuery = buildGatewayQuery(query, opts);
  const constraintText = buildGatewayConstraintText(opts);
  const userContent = [scopedQuery, constraintText].filter(Boolean).join("\n\n");

  return {
    model: transport.model,
    messages: [
      {
        role: "system",
        content: "Answer with concise factual summary and include source URLs.",
      },
      {
        role: "user",
        content: userContent,
      },
    ],
    temperature: 0.2,
  };
}

function buildRequestBody(query, opts, transport) {
  if (transport.supportsNativeFilters) {
    return buildNativeBody(query, opts, transport);
  }
  return buildGatewayBody(query, opts, transport);
}

function buildSources(data, transportId, answer) {
  const sources = [];

  if (Array.isArray(data.search_results)) {
    sources.push(...data.search_results);
  }
  if (Array.isArray(data.citations)) {
    sources.push(...data.citations);
  }

  const annotations = data.choices?.[0]?.message?.annotations;
  if (Array.isArray(annotations)) {
    sources.push(...annotations.map(normalizeAnnotation));
  }

  const deduped = dedupeSources(sources);
  if (deduped.length > 0) {
    return deduped;
  }

  if (transportId === "native") {
    return [];
  }

  return dedupeSources(extractUrlsFromText(answer));
}

function buildMissingCredentialsError() {
  return [
    "Missing Perplexity credentials.",
    "Set PERPLEXITY_API_KEY, OPENROUTER_API_KEY, KILOCODE_API_KEY,",
    "or PERPLEXITY_GATEWAY_API_KEY + PERPLEXITY_BASE_URL.",
  ].join(" ");
}

export function isAvailable(env = process.env) {
  try {
    return resolveTransport(env) !== null;
  } catch {
    return false;
  }
}

export function name() {
  return "perplexity";
}

export async function search(query, opts = {}) {
  const transport = resolveTransport(process.env);
  if (!transport) {
    throw new Error(buildMissingCredentialsError());
  }

  const body = buildRequestBody(query, opts, transport);

  const resp = await fetch(transport.apiUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${transport.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Perplexity search failed (${resp.status}): ${text}`);
  }

  const data = await resp.json();
  const answer =
    data.output_text ??
    extractTextContent(data.choices?.[0]?.message?.content) ??
    "";
  const cleanAnswer = stripCitationMarkers(answer);
  const sources = buildSources(data, transport.id, answer);
  const results = [];

  if (cleanAnswer) {
    results.push({
      title: `Perplexity Answer: ${String(query ?? "").slice(0, 80)}`,
      url: "https://www.perplexity.ai",
      content: cleanAnswer.slice(0, 1500),
      score: 1,
      publishedDate: null,
    });
  }

  const remainingSlots = Math.max(0, normalizeCount(opts.count, 20) - results.length);
  results.push(...sources.slice(0, remainingSlots));

  return {
    engine: "perplexity",
    transport: transport.id,
    answer: answer || null,
    results,
  };
}

export async function extract(_urls) {
  throw new Error(
    "Perplexity does not support content extraction. Use Tavily, Exa, or fetch instead.",
  );
}
