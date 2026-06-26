import fs from "node:fs";
import path from "node:path";

import {
  VALID_RENDER_POLICIES,
  VALID_RENDER_WAIT_UNTIL,
  normalizeRenderBlockTypes,
} from "./render-safety.mjs";

const VALID_FALLBACK_POLICIES = new Set(["balanced", "quality-first", "cost-first"]);
const VALID_MERGE_POLICIES = new Set(["primary-only", "balanced", "diversity-first"]);
const VALID_FEDERATION_TRIGGERS = new Set([
  "news",
  "ambiguous",
  "domain-critical",
  "research",
  "comparison",
]);

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function deepFreeze(value) {
  if (!isPlainObject(value) && !Array.isArray(value)) {
    return value;
  }

  for (const entry of Object.values(value)) {
    deepFreeze(entry);
  }

  return Object.freeze(value);
}

function mergeObjects(base, overlay) {
  const next = Array.isArray(base) ? [...base] : { ...base };
  if (!isPlainObject(overlay)) {
    return next;
  }

  for (const [key, value] of Object.entries(overlay)) {
    if (value === undefined) {
      continue;
    }
    if (Array.isArray(value)) {
      next[key] = [...value];
      continue;
    }
    if (isPlainObject(value) && isPlainObject(next[key])) {
      next[key] = mergeObjects(next[key], value);
      continue;
    }
    next[key] = value;
  }

  return next;
}

function normalizeProviderList(value, fieldName) {
  if (!Array.isArray(value)) {
    throw new Error(`${fieldName} must be an array of provider ids`);
  }

  const normalized = value
    .map((entry) => String(entry).trim())
    .filter(Boolean);

  return Array.from(new Set(normalized));
}

function requireBoolean(value, fieldName) {
  if (typeof value !== "boolean") {
    throw new Error(`${fieldName} must be true or false`);
  }
  return value;
}

function requireInteger(value, fieldName, minimum = 0) {
  if (!Number.isInteger(value) || value < minimum) {
    throw new Error(`${fieldName} must be an integer >= ${minimum}`);
  }
  return value;
}

function parseBooleanString(value, fieldName) {
  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return false;
  }
  throw new Error(`${fieldName} must be true or false`);
}

function parseIntegerString(value, fieldName, minimum = 0) {
  const parsed = Number.parseInt(String(value).trim(), 10);
  if (!Number.isInteger(parsed) || parsed < minimum) {
    throw new Error(`${fieldName} must be an integer >= ${minimum}`);
  }
  return parsed;
}

function parseListString(value) {
  return Array.from(
    new Set(
      String(value)
        .split(",")
        .map((entry) => entry.trim())
        .filter(Boolean),
    ),
  );
}

function readJsonFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid JSON in ${filePath}: ${error.message}`);
  }
}

function buildEnvConfig(env) {
  const layer = {
    routing: {},
    cache: {},
    health: {},
    fetch: {},
    crawl: {},
    render: {},
  };

  if (env.WEB_SEARCH_PRO_ROUTING_PREFERRED_PROVIDERS) {
    layer.routing.preferredProviders = parseListString(
      env.WEB_SEARCH_PRO_ROUTING_PREFERRED_PROVIDERS,
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_DISABLED_PROVIDERS) {
    layer.routing.disabledProviders = parseListString(env.WEB_SEARCH_PRO_ROUTING_DISABLED_PROVIDERS);
  }
  if (env.WEB_SEARCH_PRO_ROUTING_ALLOW_NO_KEY_BASELINE) {
    layer.routing.allowNoKeyBaseline = parseBooleanString(
      env.WEB_SEARCH_PRO_ROUTING_ALLOW_NO_KEY_BASELINE,
      "WEB_SEARCH_PRO_ROUTING_ALLOW_NO_KEY_BASELINE",
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_FALLBACK_POLICY) {
    layer.routing.fallbackPolicy = String(env.WEB_SEARCH_PRO_ROUTING_FALLBACK_POLICY).trim();
  }
  if (env.WEB_SEARCH_PRO_ROUTING_ENABLE_FEDERATION) {
    layer.routing.enableFederation = parseBooleanString(
      env.WEB_SEARCH_PRO_ROUTING_ENABLE_FEDERATION,
      "WEB_SEARCH_PRO_ROUTING_ENABLE_FEDERATION",
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_FEDERATION_TRIGGERS) {
    layer.routing.federationTriggers = parseListString(
      env.WEB_SEARCH_PRO_ROUTING_FEDERATION_TRIGGERS,
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_MAX_FANOUT_PROVIDERS) {
    layer.routing.maxFanoutProviders = parseIntegerString(
      env.WEB_SEARCH_PRO_ROUTING_MAX_FANOUT_PROVIDERS,
      "WEB_SEARCH_PRO_ROUTING_MAX_FANOUT_PROVIDERS",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_MAX_PER_PROVIDER) {
    layer.routing.maxPerProvider = parseIntegerString(
      env.WEB_SEARCH_PRO_ROUTING_MAX_PER_PROVIDER,
      "WEB_SEARCH_PRO_ROUTING_MAX_PER_PROVIDER",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_ROUTING_MERGE_POLICY) {
    layer.routing.mergePolicy = String(env.WEB_SEARCH_PRO_ROUTING_MERGE_POLICY).trim();
  }

  if (env.WEB_SEARCH_PRO_CACHE_ENABLED) {
    layer.cache.enabled = parseBooleanString(
      env.WEB_SEARCH_PRO_CACHE_ENABLED,
      "WEB_SEARCH_PRO_CACHE_ENABLED",
    );
  }
  if (env.WEB_SEARCH_PRO_CACHE_DIR) {
    layer.cache.dir = String(env.WEB_SEARCH_PRO_CACHE_DIR).trim();
  }
  if (env.WEB_SEARCH_PRO_CACHE_SEARCH_TTL_SECONDS) {
    layer.cache.searchTtlSeconds = parseIntegerString(
      env.WEB_SEARCH_PRO_CACHE_SEARCH_TTL_SECONDS,
      "WEB_SEARCH_PRO_CACHE_SEARCH_TTL_SECONDS",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_CACHE_EXTRACT_TTL_SECONDS) {
    layer.cache.extractTtlSeconds = parseIntegerString(
      env.WEB_SEARCH_PRO_CACHE_EXTRACT_TTL_SECONDS,
      "WEB_SEARCH_PRO_CACHE_EXTRACT_TTL_SECONDS",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_CACHE_CRAWL_TTL_SECONDS) {
    layer.cache.crawlTtlSeconds = parseIntegerString(
      env.WEB_SEARCH_PRO_CACHE_CRAWL_TTL_SECONDS,
      "WEB_SEARCH_PRO_CACHE_CRAWL_TTL_SECONDS",
      1,
    );
  }

  if (env.WEB_SEARCH_PRO_HEALTH_ENABLED) {
    layer.health.enabled = parseBooleanString(
      env.WEB_SEARCH_PRO_HEALTH_ENABLED,
      "WEB_SEARCH_PRO_HEALTH_ENABLED",
    );
  }
  if (env.WEB_SEARCH_PRO_HEALTH_COOLDOWN_SECONDS) {
    layer.health.cooldownSeconds = parseIntegerString(
      env.WEB_SEARCH_PRO_HEALTH_COOLDOWN_SECONDS,
      "WEB_SEARCH_PRO_HEALTH_COOLDOWN_SECONDS",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_HEALTH_FAILURE_THRESHOLD) {
    layer.health.failureThreshold = parseIntegerString(
      env.WEB_SEARCH_PRO_HEALTH_FAILURE_THRESHOLD,
      "WEB_SEARCH_PRO_HEALTH_FAILURE_THRESHOLD",
      1,
    );
  }

  if (env.WEB_SEARCH_PRO_FETCH_TIMEOUT_MS) {
    layer.fetch.timeoutMs = parseIntegerString(
      env.WEB_SEARCH_PRO_FETCH_TIMEOUT_MS,
      "WEB_SEARCH_PRO_FETCH_TIMEOUT_MS",
      100,
    );
  }
  if (env.WEB_SEARCH_PRO_FETCH_MAX_REDIRECTS) {
    layer.fetch.maxRedirects = parseIntegerString(
      env.WEB_SEARCH_PRO_FETCH_MAX_REDIRECTS,
      "WEB_SEARCH_PRO_FETCH_MAX_REDIRECTS",
      0,
    );
  }
  if (env.WEB_SEARCH_PRO_FETCH_MAX_CHARS) {
    layer.fetch.maxChars = parseIntegerString(
      env.WEB_SEARCH_PRO_FETCH_MAX_CHARS,
      "WEB_SEARCH_PRO_FETCH_MAX_CHARS",
      100,
    );
  }

  if (env.WEB_SEARCH_PRO_CRAWL_DEFAULT_DEPTH) {
    layer.crawl.defaultDepth = parseIntegerString(
      env.WEB_SEARCH_PRO_CRAWL_DEFAULT_DEPTH,
      "WEB_SEARCH_PRO_CRAWL_DEFAULT_DEPTH",
      0,
    );
  }
  if (env.WEB_SEARCH_PRO_CRAWL_DEFAULT_MAX_PAGES) {
    layer.crawl.defaultMaxPages = parseIntegerString(
      env.WEB_SEARCH_PRO_CRAWL_DEFAULT_MAX_PAGES,
      "WEB_SEARCH_PRO_CRAWL_DEFAULT_MAX_PAGES",
      1,
    );
  }
  if (env.WEB_SEARCH_PRO_CRAWL_RESPECT_ROBOTS_TXT) {
    layer.crawl.respectRobotsTxt = parseBooleanString(
      env.WEB_SEARCH_PRO_CRAWL_RESPECT_ROBOTS_TXT,
      "WEB_SEARCH_PRO_CRAWL_RESPECT_ROBOTS_TXT",
    );
  }

  if (env.WEB_SEARCH_PRO_RENDER_ENABLED) {
    layer.render.enabled = parseBooleanString(
      env.WEB_SEARCH_PRO_RENDER_ENABLED,
      "WEB_SEARCH_PRO_RENDER_ENABLED",
    );
  }
  if (env.WEB_SEARCH_PRO_RENDER_POLICY) {
    layer.render.policy = String(env.WEB_SEARCH_PRO_RENDER_POLICY).trim();
  }
  if (env.WEB_SEARCH_PRO_RENDER_BUDGET_MS) {
    layer.render.budgetMs = parseIntegerString(
      env.WEB_SEARCH_PRO_RENDER_BUDGET_MS,
      "WEB_SEARCH_PRO_RENDER_BUDGET_MS",
      1000,
    );
  }
  if (env.WEB_SEARCH_PRO_RENDER_WAIT_UNTIL) {
    layer.render.waitUntil = String(env.WEB_SEARCH_PRO_RENDER_WAIT_UNTIL).trim();
  }
  if (env.WEB_SEARCH_PRO_RENDER_BLOCK_TYPES) {
    layer.render.blockTypes = parseListString(env.WEB_SEARCH_PRO_RENDER_BLOCK_TYPES);
  }
  if (env.WEB_SEARCH_PRO_RENDER_SAME_ORIGIN_ONLY) {
    layer.render.sameOriginOnly = parseBooleanString(
      env.WEB_SEARCH_PRO_RENDER_SAME_ORIGIN_ONLY,
      "WEB_SEARCH_PRO_RENDER_SAME_ORIGIN_ONLY",
    );
  }

  return layer;
}

function normalizeConfig(input) {
  const config = mergeObjects(DEFAULT_CONFIG, input);

  config.routing.preferredProviders = normalizeProviderList(
    config.routing.preferredProviders,
    "routing.preferredProviders",
  );
  config.routing.disabledProviders = normalizeProviderList(
    config.routing.disabledProviders,
    "routing.disabledProviders",
  );
  config.routing.allowNoKeyBaseline = requireBoolean(
    config.routing.allowNoKeyBaseline,
    "routing.allowNoKeyBaseline",
  );
  config.routing.enableFederation = requireBoolean(
    config.routing.enableFederation,
    "routing.enableFederation",
  );
  if (!VALID_FALLBACK_POLICIES.has(config.routing.fallbackPolicy)) {
    throw new Error(
      `routing.fallbackPolicy must be one of: ${Array.from(VALID_FALLBACK_POLICIES).join(", ")}`,
    );
  }
  config.routing.federationTriggers = normalizeProviderList(
    config.routing.federationTriggers,
    "routing.federationTriggers",
  );
  if (
    config.routing.federationTriggers.some((value) => !VALID_FEDERATION_TRIGGERS.has(value))
  ) {
    throw new Error(
      `routing.federationTriggers must only contain: ${Array.from(
        VALID_FEDERATION_TRIGGERS,
      ).join(", ")}`,
    );
  }
  config.routing.maxFanoutProviders = requireInteger(
    config.routing.maxFanoutProviders,
    "routing.maxFanoutProviders",
    1,
  );
  config.routing.maxPerProvider = requireInteger(
    config.routing.maxPerProvider,
    "routing.maxPerProvider",
    1,
  );
  if (!VALID_MERGE_POLICIES.has(config.routing.mergePolicy)) {
    throw new Error(
      `routing.mergePolicy must be one of: ${Array.from(VALID_MERGE_POLICIES).join(", ")}`,
    );
  }

  config.cache.enabled = requireBoolean(config.cache.enabled, "cache.enabled");
  if (typeof config.cache.dir !== "string" || config.cache.dir.trim().length === 0) {
    throw new Error("cache.dir must be a non-empty string");
  }
  config.cache.dir = config.cache.dir.trim();
  config.cache.searchTtlSeconds = requireInteger(
    config.cache.searchTtlSeconds,
    "cache.searchTtlSeconds",
    1,
  );
  config.cache.extractTtlSeconds = requireInteger(
    config.cache.extractTtlSeconds,
    "cache.extractTtlSeconds",
    1,
  );
  config.cache.crawlTtlSeconds = requireInteger(
    config.cache.crawlTtlSeconds,
    "cache.crawlTtlSeconds",
    1,
  );

  config.health.enabled = requireBoolean(config.health.enabled, "health.enabled");
  config.health.cooldownSeconds = requireInteger(
    config.health.cooldownSeconds,
    "health.cooldownSeconds",
    1,
  );
  config.health.failureThreshold = requireInteger(
    config.health.failureThreshold,
    "health.failureThreshold",
    1,
  );

  config.fetch.timeoutMs = requireInteger(config.fetch.timeoutMs, "fetch.timeoutMs", 100);
  config.fetch.maxRedirects = requireInteger(
    config.fetch.maxRedirects,
    "fetch.maxRedirects",
    0,
  );
  config.fetch.maxChars = requireInteger(config.fetch.maxChars, "fetch.maxChars", 100);

  config.crawl.defaultDepth = requireInteger(
    config.crawl.defaultDepth,
    "crawl.defaultDepth",
    0,
  );
  config.crawl.defaultMaxPages = requireInteger(
    config.crawl.defaultMaxPages,
    "crawl.defaultMaxPages",
    1,
  );
  config.crawl.respectRobotsTxt = requireBoolean(
    config.crawl.respectRobotsTxt,
    "crawl.respectRobotsTxt",
  );

  config.render.enabled = requireBoolean(config.render.enabled, "render.enabled");
  if (!VALID_RENDER_POLICIES.has(config.render.policy)) {
    throw new Error(
      `render.policy must be one of: ${Array.from(VALID_RENDER_POLICIES).join(", ")}`,
    );
  }
  config.render.budgetMs = requireInteger(config.render.budgetMs, "render.budgetMs", 1000);
  if (!VALID_RENDER_WAIT_UNTIL.has(config.render.waitUntil)) {
    throw new Error(
      `render.waitUntil must be one of: ${Array.from(VALID_RENDER_WAIT_UNTIL).join(", ")}`,
    );
  }
  config.render.blockTypes = normalizeRenderBlockTypes(
    config.render.blockTypes,
    "render.blockTypes",
  );
  config.render.sameOriginOnly = requireBoolean(
    config.render.sameOriginOnly,
    "render.sameOriginOnly",
  );

  return config;
}

export const DEFAULT_CONFIG = deepFreeze({
  routing: {
    preferredProviders: [],
    disabledProviders: [],
    allowNoKeyBaseline: true,
    fallbackPolicy: "balanced",
    enableFederation: false,
    federationTriggers: ["news", "ambiguous", "domain-critical", "research", "comparison"],
    maxFanoutProviders: 2,
    maxPerProvider: 5,
    mergePolicy: "balanced",
  },
  cache: {
    enabled: true,
    dir: ".cache/web-search-pro",
    searchTtlSeconds: 1800,
    extractTtlSeconds: 21600,
    crawlTtlSeconds: 21600,
  },
  health: {
    enabled: true,
    cooldownSeconds: 600,
    failureThreshold: 3,
  },
  fetch: {
    timeoutMs: 20000,
    maxRedirects: 4,
    maxChars: 12000,
  },
  crawl: {
    defaultDepth: 1,
    defaultMaxPages: 10,
    respectRobotsTxt: false,
  },
  render: {
    enabled: false,
    policy: "fallback",
    budgetMs: 8000,
    waitUntil: "domcontentloaded",
    blockTypes: ["image", "font", "media"],
    sameOriginOnly: true,
  },
});

export function resolveConfigPath(options = {}) {
  const cwd = options.cwd ?? process.cwd();
  const env = options.env ?? process.env;

  if (options.configPath) {
    return path.resolve(cwd, options.configPath);
  }
  if (env.WEB_SEARCH_PRO_CONFIG) {
    return path.resolve(cwd, env.WEB_SEARCH_PRO_CONFIG);
  }
  return path.join(cwd, "config.json");
}

export function loadRuntimeConfig(options = {}) {
  const cwd = options.cwd ?? process.cwd();
  const env = options.env ?? process.env;
  const configPath = resolveConfigPath(options);
  const exists = fs.existsSync(configPath);

  const fileConfig = exists ? readJsonFile(configPath) : {};
  const merged = mergeObjects(
    mergeObjects(mergeObjects(DEFAULT_CONFIG, fileConfig), buildEnvConfig(env)),
    options.overrides ?? {},
  );

  return {
    config: normalizeConfig(merged),
    meta: {
      path: configPath,
      exists,
    },
  };
}

export function resolveCacheDir(config, cwd = process.cwd()) {
  return path.resolve(cwd, config.cache.dir);
}
