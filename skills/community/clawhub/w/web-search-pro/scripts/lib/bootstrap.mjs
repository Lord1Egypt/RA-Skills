import { buildDoctorReport } from "./doctor.mjs";
import { buildRoutingSummary, SCHEMA_VERSION } from "./output.mjs";
import {
  planCrawlRoute,
  planExtractRoute,
  planMapRoute,
  planSearchRoute,
} from "./planner.mjs";

function listUnlockedCapabilities(capabilities) {
  const unlocked = [];

  if (capabilities.search) unlocked.push("search");
  if (capabilities.deepSearch) unlocked.push("deepSearch");
  if (capabilities.newsSearch) unlocked.push("newsSearch");
  if (capabilities.newsDays) unlocked.push("newsDays");
  if (capabilities.extract) unlocked.push("extract");
  if (capabilities.crawl) unlocked.push("crawl");
  if (capabilities.map) unlocked.push("map");
  if (capabilities.answerSynthesis) unlocked.push("answerSynthesis");
  if (capabilities.localeFiltering) unlocked.push("localeFiltering");
  if (capabilities.dateRange) unlocked.push("dateRange");
  if (capabilities.timeRange) unlocked.push("timeRange");
  if ((capabilities.subEngines?.length ?? 0) > 0) {
    unlocked.push(`subEngines:${capabilities.subEngines.join(",")}`);
  }

  return unlocked;
}

function buildRouteProbe(plan, federation = null) {
  return {
    available: Boolean(plan.selected),
    selectedProvider: plan.selected?.provider.id ?? null,
    reason: plan.selected?.summary ?? plan.error?.message ?? "",
    routingSummary: buildRoutingSummary(plan, federation),
  };
}

function buildMissingProviderHints(providers = []) {
  return providers
    .filter((provider) => provider.env.length > 0 && provider.credentialed === false)
    .map((provider) => ({
      providerId: provider.id,
      label: provider.label,
      envVars: provider.env.map((entry) => entry.name),
      credentialRequirement: provider.credentialRequirement,
      unlocks: listUnlockedCapabilities(provider.capabilities),
    }));
}

function buildNextActions(doctor, missingProviderHints) {
  const actions = [];

  if (!doctor.availableFeatures.deepSearch) {
    actions.push("Set TAVILY_API_KEY or EXA_API_KEY to unlock deep search routing.");
  }
  if (!doctor.availableFeatures.newsSearch) {
    actions.push("Set SERPER_API_KEY, TAVILY_API_KEY, or SERPAPI_API_KEY to unlock news routing.");
  }
  if (!doctor.availableFeatures.localeFiltering) {
    actions.push("Set BRAVE_API_KEY, QUERIT_API_KEY, YOU_API_KEY, SERPER_API_KEY, or SERPAPI_API_KEY to unlock locale-aware routing.");
  }
  if (doctor.baselineStatus === "degraded") {
    actions.push("Investigate baseline provider health before relying on no-key fallback behavior.");
  }
  if (missingProviderHints.some((entry) => entry.providerId === "tavily")) {
    actions.push("Add TAVILY_API_KEY to unlock the strongest all-in-one search + extract provider.");
  }
  if (missingProviderHints.some((entry) => entry.providerId === "querit")) {
    actions.push("Add QUERIT_API_KEY to unlock multilingual AI search with native geo and language filters.");
  }
  if (missingProviderHints.some((entry) => entry.providerId === "brave")) {
    actions.push("Add BRAVE_API_KEY if you already rely on OpenClaw's Brave setup and want structured general web search here too.");
  }
  if (missingProviderHints.some((entry) => entry.providerId === "serpapi")) {
    actions.push("Add SERPAPI_API_KEY if Baidu, Yandex, or multi-engine fallback coverage matters.");
  }
  if (missingProviderHints.some((entry) => entry.providerId === "perplexity")) {
    actions.push(
      "Add PERPLEXITY_API_KEY, OPENROUTER_API_KEY, KILOCODE_API_KEY, or PERPLEXITY_GATEWAY_API_KEY + PERPLEXITY_BASE_URL to unlock answer-first grounded search.",
    );
  }

  return Array.from(new Set(actions));
}

export async function buildBootstrapReport(options = {}) {
  const doctor = await buildDoctorReport(options);
  const env = options.env ?? process.env;
  const config = options.config;
  const healthState = options.healthState ?? { providers: doctor.health ?? {} };
  const now = options.now ?? Date.now();

  const basicSearchPlan = planSearchRoute(
    {
      query: "OpenClaw bootstrap search",
      count: 5,
      mode: "search",
    },
    { env, config, healthState, now },
  );
  const deepSearchPlan = planSearchRoute(
    {
      query: "OpenClaw routing architecture analysis",
      count: 5,
      deep: true,
      mode: "search",
    },
    { env, config, healthState, now },
  );
  const newsSearchPlan = planSearchRoute(
    {
      query: "OpenClaw latest news",
      count: 5,
      news: true,
      mode: "search",
    },
    { env, config, healthState, now },
  );
  const extractPlan = planExtractRoute(
    {
      urls: ["https://example.com"],
      maxChars: config.fetch.maxChars,
    },
    { env, config, healthState, now },
  );
  const crawlPlan = planCrawlRoute(
    {
      urls: ["https://example.com"],
    },
    { env, config, healthState, now },
  );
  const mapPlan = planMapRoute(
    {
      urls: ["https://example.com"],
    },
    { env, config, healthState, now },
  );

  const missingProviderHints = buildMissingProviderHints(doctor.providers);

  return {
    status: doctor.status,
    configuredProviders: doctor.configuredProviders,
    credentialedProviders: doctor.credentialedProviders,
    availableFeatures: doctor.availableFeatures,
    warnings: doctor.warnings,
    cache: {
      ...doctor.cache,
      searchTtlSeconds: config.cache.searchTtlSeconds,
      extractTtlSeconds: config.cache.extractTtlSeconds,
      crawlTtlSeconds: config.cache.crawlTtlSeconds,
    },
    routingPolicy: {
      allowNoKeyBaseline: config.routing.allowNoKeyBaseline,
      enableFederation: config.routing.enableFederation,
      federationTriggers: config.routing.federationTriggers,
      maxFanoutProviders: config.routing.maxFanoutProviders,
      maxPerProvider: config.routing.maxPerProvider,
      mergePolicy: config.routing.mergePolicy,
      fallbackPolicy: config.routing.fallbackPolicy,
      preferredProviders: config.routing.preferredProviders,
      disabledProviders: config.routing.disabledProviders,
    },
    renderLane: doctor.renderLane,
    safeFetch: doctor.safeFetch,
    recommendedRoutes: {
      basicSearch: buildRouteProbe(basicSearchPlan, basicSearchPlan.federation),
      deepSearch: buildRouteProbe(deepSearchPlan, deepSearchPlan.federation),
      newsSearch: buildRouteProbe(newsSearchPlan, newsSearchPlan.federation),
      extract: buildRouteProbe(extractPlan),
      crawl: buildRouteProbe(crawlPlan),
      map: buildRouteProbe(mapPlan),
    },
    missingProviderHints,
    nextActions: buildNextActions(doctor, missingProviderHints),
    configPath: options.configMeta?.path ?? null,
    schemaVersion: SCHEMA_VERSION,
  };
}
