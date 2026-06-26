import { DEFAULT_CONFIG } from "./config.mjs";
import * as tavily from "../engines/tavily.mjs";
import * as exa from "../engines/exa.mjs";
import * as querit from "../engines/querit.mjs";
import * as serper from "../engines/serper.mjs";
import * as brave from "../engines/brave.mjs";
import * as serpapi from "../engines/serpapi.mjs";
import * as you from "../engines/you.mjs";
import * as searxng from "../engines/searxng.mjs";
import * as perplexity from "../engines/perplexity.mjs";
import * as ddg from "../engines/ddg.mjs";
import * as fetchEngine from "../engines/fetch.mjs";

function freezeCapabilities(capabilities) {
  return Object.freeze({
    ...capabilities,
    subEngines: Object.freeze([...(capabilities.subEngines ?? [])]),
  });
}

function defineProvider(spec) {
  const credentialGroups = spec.credentialGroups ?? (spec.envVars.length > 0 ? [spec.envVars] : []);
  return Object.freeze({
    ...spec,
    activation: spec.activation ?? "credential",
    envVars: Object.freeze([...spec.envVars]),
    credentialGroups: Object.freeze(
      credentialGroups.map((group) => Object.freeze([...group])),
    ),
    capabilities: freezeCapabilities(spec.capabilities),
    limits: Object.freeze({
      search: Object.freeze({ ...(spec.limits.search ?? {}) }),
    }),
    routing: Object.freeze({ ...spec.routing }),
  });
}

const PROVIDERS = Object.freeze([
  defineProvider({
    id: "tavily",
    label: "Tavily",
    activation: "credential",
    envVars: ["TAVILY_API_KEY"],
    adapter: tavily,
    capabilities: {
      search: true,
      extract: true,
      deepSearch: true,
      newsSearch: true,
      newsDays: true,
      crawl: false,
      map: false,
      domainFilterMode: "native",
      dateRange: true,
      timeRange: true,
      localeFiltering: false,
      answerSynthesis: true,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 400,
      deepSearchPriority: 220,
      newsSearchPriority: 210,
      extractPriority: 220,
      qualityScore: 5,
      costScore: 5,
      defaultReason: "highest default search priority among configured providers",
    },
  }),
  defineProvider({
    id: "exa",
    label: "Exa",
    activation: "credential",
    envVars: ["EXA_API_KEY"],
    adapter: exa,
    capabilities: {
      search: true,
      extract: true,
      deepSearch: true,
      newsSearch: false,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "native",
      dateRange: true,
      timeRange: true,
      localeFiltering: false,
      answerSynthesis: false,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 100,
      },
    },
    routing: {
      defaultSearchPriority: 320,
      deepSearchPriority: 180,
      newsSearchPriority: 0,
      extractPriority: 180,
      qualityScore: 4,
      costScore: 4,
      defaultReason: "strong semantic search fallback",
    },
  }),
  defineProvider({
    id: "querit",
    label: "Querit",
    activation: "credential",
    envVars: ["QUERIT_API_KEY"],
    adapter: querit,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: false,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "native",
      dateRange: false,
      timeRange: true,
      localeFiltering: true,
      answerSynthesis: false,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 220,
      deepSearchPriority: 0,
      newsSearchPriority: 0,
      extractPriority: 0,
      qualityScore: 4,
      costScore: 3,
      defaultReason: "multilingual AI search provider with native geo and language filters",
    },
  }),
  defineProvider({
    id: "serper",
    label: "Serper",
    activation: "credential",
    envVars: ["SERPER_API_KEY"],
    adapter: serper,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: true,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: true,
      timeRange: true,
      localeFiltering: true,
      answerSynthesis: true,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 100,
      },
    },
    routing: {
      defaultSearchPriority: 240,
      deepSearchPriority: 0,
      newsSearchPriority: 240,
      extractPriority: 0,
      qualityScore: 3,
      costScore: 3,
      defaultReason: "Google SERP fallback with broad result coverage",
    },
  }),
  defineProvider({
    id: "brave",
    label: "Brave",
    activation: "credential",
    envVars: ["BRAVE_API_KEY"],
    adapter: brave,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: false,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: true,
      timeRange: true,
      localeFiltering: true,
      answerSynthesis: false,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 210,
      deepSearchPriority: 0,
      newsSearchPriority: 0,
      extractPriority: 0,
      qualityScore: 3,
      costScore: 2,
      defaultReason: "structured web search with strong general-purpose coverage",
    },
  }),
  defineProvider({
    id: "serpapi",
    label: "SerpAPI",
    activation: "credential",
    envVars: ["SERPAPI_API_KEY"],
    adapter: serpapi,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: true,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: true,
      timeRange: true,
      localeFiltering: true,
      answerSynthesis: true,
      subEngines: ["google", "bing", "baidu", "yandex", "duckduckgo"],
    },
    limits: {
      search: {
        maxResults: 100,
      },
    },
    routing: {
      defaultSearchPriority: 180,
      deepSearchPriority: 0,
      newsSearchPriority: 180,
      extractPriority: 0,
      qualityScore: 2,
      costScore: 2,
      defaultReason: "multi-engine fallback with sub-engine coverage",
    },
  }),
  defineProvider({
    id: "you",
    label: "You.com",
    activation: "credential",
    envVars: ["YOU_API_KEY"],
    adapter: you,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: true,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: true,
      timeRange: true,
      localeFiltering: true,
      answerSynthesis: true,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 100,
      },
    },
    routing: {
      defaultSearchPriority: 200,
      deepSearchPriority: 0,
      newsSearchPriority: 170,
      extractPriority: 0,
      qualityScore: 4,
      costScore: 4,
      defaultReason: "LLM-ready web search with freshness and locale support",
    },
  }),
  defineProvider({
    id: "searxng",
    label: "SearXNG",
    activation: "credential",
    envVars: ["SEARXNG_INSTANCE_URL"],
    adapter: searxng,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: true,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: false,
      timeRange: true,
      localeFiltering: false,
      answerSynthesis: true,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 120,
      deepSearchPriority: 0,
      newsSearchPriority: 140,
      extractPriority: 0,
      qualityScore: 2,
      costScore: 1,
      defaultReason: "privacy-first self-hosted metasearch fallback",
    },
  }),
  defineProvider({
    id: "perplexity",
    label: "Perplexity",
    activation: "credential",
    envVars: [
      "PERPLEXITY_API_KEY",
      "PERPLEXITY_GATEWAY_API_KEY",
      "PERPLEXITY_BASE_URL",
      "OPENROUTER_API_KEY",
      "KILOCODE_API_KEY",
    ],
    credentialGroups: [
      ["PERPLEXITY_API_KEY"],
      ["PERPLEXITY_GATEWAY_API_KEY", "PERPLEXITY_BASE_URL"],
      ["OPENROUTER_API_KEY"],
      ["KILOCODE_API_KEY"],
    ],
    adapter: perplexity,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: false,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: false,
      timeRange: false,
      localeFiltering: false,
      answerSynthesis: true,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 230,
      deepSearchPriority: 0,
      newsSearchPriority: 0,
      extractPriority: 0,
      qualityScore: 4,
      costScore: 5,
      defaultReason: "direct-answer provider with cited web grounding via native or gateway transports",
    },
  }),
  defineProvider({
    id: "ddg",
    label: "DuckDuckGo",
    activation: "baseline",
    envVars: [],
    adapter: ddg,
    capabilities: {
      search: true,
      extract: false,
      deepSearch: false,
      newsSearch: false,
      newsDays: false,
      crawl: false,
      map: false,
      domainFilterMode: "query",
      dateRange: false,
      timeRange: false,
      localeFiltering: false,
      answerSynthesis: false,
      subEngines: [],
    },
    limits: {
      search: {
        maxResults: 20,
      },
    },
    routing: {
      defaultSearchPriority: 60,
      deepSearchPriority: 0,
      newsSearchPriority: 0,
      extractPriority: 0,
      qualityScore: 1,
      costScore: 0,
      defaultReason: "no-key search fallback",
    },
  }),
  defineProvider({
    id: "fetch",
    label: "Safe Fetch",
    activation: "baseline",
    envVars: [],
    adapter: fetchEngine,
    capabilities: {
      search: false,
      extract: true,
      deepSearch: false,
      newsSearch: false,
      newsDays: false,
      crawl: true,
      map: true,
      domainFilterMode: "none",
      dateRange: false,
      timeRange: false,
      localeFiltering: false,
      answerSynthesis: false,
      subEngines: [],
    },
    limits: {
      search: {},
    },
    routing: {
      defaultSearchPriority: 0,
      deepSearchPriority: 0,
      newsSearchPriority: 0,
      extractPriority: 30,
      qualityScore: 1,
      costScore: 0,
      defaultReason: "no-key safe fetch fallback",
    },
  }),
]);

export function listProviders() {
  return PROVIDERS;
}

export function getProvider(providerId) {
  return PROVIDERS.find((provider) => provider.id === providerId) ?? null;
}

export function hasProviderCredentials(provider, env = process.env) {
  if ((provider.credentialGroups?.length ?? 0) === 0) {
    return false;
  }
  return provider.credentialGroups.some((group) =>
    group.every((name) => typeof env[name] === "string" && env[name].trim().length > 0),
  );
}

export function getProviderConfigurationError(provider, env = process.env) {
  if (!hasProviderCredentials(provider, env)) {
    return null;
  }
  if (typeof provider.adapter?.resolveTransport !== "function") {
    return null;
  }

  try {
    const transport = provider.adapter.resolveTransport(env);
    return transport ? null : "Invalid provider transport configuration";
  } catch (error) {
    return error instanceof Error ? error.message : String(error);
  }
}

export function getProviderCapabilities(provider, env = process.env) {
  if (typeof provider.adapter?.resolveTransport !== "function") {
    return provider.capabilities;
  }

  try {
    const transport = provider.adapter.resolveTransport(env);
    if (!transport) {
      return provider.capabilities;
    }
    if (transport.supportsNativeFilters) {
      return freezeCapabilities({
        ...provider.capabilities,
        dateRange: true,
        timeRange: true,
      });
    }
  } catch {
    return provider.capabilities;
  }

  return provider.capabilities;
}

export function materializeProvider(provider, env = process.env) {
  const capabilities = getProviderCapabilities(provider, env);
  if (capabilities === provider.capabilities) {
    return provider;
  }
  return Object.freeze({
    ...provider,
    capabilities,
  });
}

function formatCredentialGroup(group = []) {
  if (group.length <= 1) {
    return group[0] ?? "";
  }
  return group.join(" + ");
}

export function formatCredentialRequirement(provider) {
  const groups = provider.credentialGroups ?? [];
  if (groups.length === 0) {
    return "";
  }
  const variants = groups.map((group) => formatCredentialGroup(group)).filter(Boolean);
  if (variants.length === 0) {
    return "";
  }
  if (variants.length === 1) {
    return variants[0];
  }
  return `one of ${variants.join(" or ")}`;
}

export function buildMissingCredentialMessage(provider) {
  const requirement = formatCredentialRequirement(provider);
  return requirement ? `Missing ${requirement}` : "Missing provider credentials";
}

function resolveProviderRuntime() {
  return {
    available: true,
    browserFamily: null,
    browserPath: null,
    launcher: null,
  };
}

export function isProviderRuntimeAvailable(provider, options = {}) {
  return resolveProviderRuntime(provider, options).available;
}

function isProviderEnabled(provider, env, config, options = {}) {
  if (config.routing.disabledProviders.includes(provider.id)) {
    return false;
  }
  if (!isProviderRuntimeAvailable(provider, options)) {
    return false;
  }
  if (provider.activation === "baseline") {
    return config.routing.allowNoKeyBaseline;
  }
  if (provider.activation === "render") {
    return config.render.enabled && config.render.policy !== "off";
  }
  return hasProviderCredentials(provider, env) && !getProviderConfigurationError(provider, env);
}

export function listConfiguredProviders(env = process.env, config = DEFAULT_CONFIG, options = {}) {
  return PROVIDERS
    .filter((provider) => isProviderEnabled(provider, env, config, { ...options, env }))
    .map((provider) => materializeProvider(provider, env));
}

export function buildEnvDisclosure(provider) {
  return provider.envVars.map((name) => ({
    name,
    required: false,
    description:
      provider.credentialGroups.length > 1
        ? `One supported credential path for ${provider.label}; any complete group enables this provider.`
        : `Enables ${provider.label} features when that provider is selected.`,
  }));
}

export function buildAvailableFeatureSummary(providers) {
  const configured = providers ?? [];
  const subEngines = Array.from(
    new Set(configured.flatMap((provider) => provider.capabilities.subEngines)),
  );

  return {
    search: configured.some((provider) => provider.capabilities.search),
    deepSearch: configured.some((provider) => provider.capabilities.deepSearch),
    newsSearch: configured.some((provider) => provider.capabilities.newsSearch),
    newsDays: configured.some((provider) => provider.capabilities.newsDays),
    extract: configured.some((provider) => provider.capabilities.extract),
    crawl: configured.some((provider) => provider.capabilities.crawl),
    map: configured.some((provider) => provider.capabilities.map),
    browserRender: false,
    nativeDomainFiltering: configured.some(
      (provider) => provider.capabilities.domainFilterMode === "native",
    ),
    localeFiltering: configured.some((provider) => provider.capabilities.localeFiltering),
    answerSynthesis: configured.some((provider) => provider.capabilities.answerSynthesis),
    dateRange: configured.some((provider) => provider.capabilities.dateRange),
    timeRange: configured.some((provider) => provider.capabilities.timeRange),
    subEngines,
  };
}

export function buildCapabilitySnapshot(options = {}) {
  const env = options.env ?? process.env;
  const config = options.config ?? DEFAULT_CONFIG;
  const configuredProviders = listConfiguredProviders(env, config, options);
  return {
    providers: listProviders().map((provider) => ({
      id: provider.id,
      label: provider.label,
      activation: provider.activation,
      configured: isProviderEnabled(provider, env, config, options),
      credentialed: hasProviderCredentials(provider, env),
      configurationError: getProviderConfigurationError(provider, env),
      runtimeAvailable: isProviderRuntimeAvailable(provider, options),
      runtime: resolveProviderRuntime(provider, options),
      env: buildEnvDisclosure(provider),
      credentialGroups: provider.credentialGroups,
      credentialRequirement: formatCredentialRequirement(provider),
      capabilities: getProviderCapabilities(provider, env),
      limits: provider.limits,
    })),
    configuredProviders: configuredProviders.map((provider) => provider.id),
    availableFeatures: buildAvailableFeatureSummary(configuredProviders),
  };
}
