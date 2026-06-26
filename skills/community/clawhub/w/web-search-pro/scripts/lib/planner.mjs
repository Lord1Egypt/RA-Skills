import { DEFAULT_CONFIG } from "./config.mjs";
import { buildFederationPlan } from "./federated-search.mjs";
import { getProviderHealthEntry } from "./health-state.mjs";
import { enrichPlanWithRoutingConfidence } from "./routing-confidence.mjs";
import {
  analyzeSearchSignals,
} from "./search-signals.mjs";
import {
  buildMissingCredentialMessage,
  getProvider,
  getProviderConfigurationError,
  hasProviderCredentials,
  isProviderRuntimeAvailable,
  listProviders,
  materializeProvider,
} from "./providers.mjs";

function normalizeSearchRequest(request) {
  const searchType =
    request.searchType ?? (request.news ? "news" : "web");
  return {
    query: String(request.query ?? "").trim(),
    engine: request.engine ?? null,
    count: request.count ?? 5,
    deep: request.deep ?? false,
    news: searchType === "news" || request.news === true,
    searchType,
    intentPreset: request.intentPreset ?? "general",
    days: request.days ?? null,
    includeDomains: request.includeDomains ?? null,
    excludeDomains: request.excludeDomains ?? null,
    timeRange: request.timeRange ?? null,
    fromDate: request.fromDate ?? null,
    toDate: request.toDate ?? null,
    searchEngine: request.searchEngine ?? null,
    country: request.country ?? null,
    lang: request.lang ?? null,
    mode: request.mode ?? "search",
  };
}

function normalizeExtractRequest(request) {
  return {
    engine: request.engine ?? null,
    urls: Array.isArray(request.urls) ? request.urls : [],
    maxChars: request.maxChars ?? null,
  };
}

function normalizeDiscoveryRequest(request) {
  return {
    engine: request.engine ?? null,
    urls: Array.isArray(request.urls) ? request.urls : [],
  };
}

function providerIsDisabled(provider, config) {
  return config.routing.disabledProviders.includes(provider.id);
}

function providerUsesNoKeyBaseline(provider) {
  return provider.activation === "baseline";
}

function providerIsAvailable(provider, env, config, options = {}) {
  if (providerIsDisabled(provider, config)) {
    return false;
  }
  if (!isProviderRuntimeAvailable(provider, { ...options, env })) {
    return false;
  }
  if (providerUsesNoKeyBaseline(provider)) {
    return config.routing.allowNoKeyBaseline;
  }
  if (provider.activation === "render") {
    return config.render.enabled && config.render.policy !== "off";
  }
  return hasProviderCredentials(provider, env) && !getProviderConfigurationError(provider, env);
}

function listEffectiveProviders(env, config, options = {}) {
  return listProviders()
    .filter((provider) => providerIsAvailable(provider, env, config, { ...options, env }))
    .map((provider) => materializeProvider(provider, env));
}

function buildHardConstraints() {
  return {
    explicitEngineMismatch: false,
    disabledByConfig: false,
    baselineDisallowed: false,
    runtimeUnavailable: false,
    missingCredentials: false,
    invalidConfiguration: false,
    missingCapability: [],
    providerSpecific: [],
  };
}

function addContribution(candidate, contribution) {
  candidate.contributions.push(contribution);
}

function addReasonContribution(candidate, contribution, reason, { prepend = false } = {}) {
  addContribution(candidate, contribution);
  if (prepend) {
    candidate.reasons.unshift(reason);
  } else {
    candidate.reasons.push(reason);
  }
}

function addIssue(candidate, message, assignment = null) {
  candidate.issues.push(message);
  if (!assignment) {
    return;
  }
  if (Array.isArray(candidate.hardConstraints[assignment.key])) {
    candidate.hardConstraints[assignment.key].push(assignment.value);
  } else {
    candidate.hardConstraints[assignment.key] = assignment.value;
  }
}

function buildCandidateBase(provider, env, config, healthState, now, options = {}) {
  const effectiveProvider = materializeProvider(provider, env);
  const credentialed = hasProviderCredentials(provider, env);
  const health = getProviderHealthEntry(healthState, provider.id, now);
  const configurationError = getProviderConfigurationError(provider, env);

  return {
    provider: effectiveProvider,
    configured: providerIsAvailable(provider, env, config, { ...options, env }),
    credentialed,
    configurationError,
    runtimeAvailable: isProviderRuntimeAvailable(provider, { ...options, env }),
    health,
    hardConstraints: buildHardConstraints(),
    contributions: [],
    issues: [],
    reasons: [],
    score: null,
    summary: "",
    status: "rejected",
  };
}

function finalizeCandidate(candidate, status) {
  return {
    ...candidate,
    status,
    summary: candidate.summary || candidate.reasons[0] || candidate.issues[0] || "",
  };
}

function applyRoutingPolicy(score, provider, config, candidate) {
  if (config.routing.fallbackPolicy === "quality-first") {
    addReasonContribution(
      candidate,
      {
        kind: "policy",
        id: "routing.quality-first",
        label: "Quality-first policy favors higher quality providers",
        delta: provider.routing.qualityScore * 40,
        category: "policy",
        evidence: config.routing.fallbackPolicy,
      },
      "quality-first policy favors higher quality providers",
    );
    return score + provider.routing.qualityScore * 40;
  }
  if (config.routing.fallbackPolicy === "cost-first") {
    addReasonContribution(
      candidate,
      {
        kind: "policy",
        id: "routing.cost-first",
        label: "Cost-first policy favors lower cost providers",
        delta: (10 - provider.routing.costScore) * 40,
        category: "policy",
        evidence: config.routing.fallbackPolicy,
      },
      "cost-first policy favors lower cost providers",
    );
    return score + (10 - provider.routing.costScore) * 40;
  }
  return score;
}

function applyPreferenceBonus(score, provider, config, candidate) {
  if (config.routing.preferredProviders.includes(provider.id)) {
    addReasonContribution(
      candidate,
      {
        kind: "preference",
        id: "routing.preferred-provider",
        label: "Preferred provider configured by routing.preferredProviders",
        delta: 280,
        category: "preference",
        evidence: provider.id,
      },
      `preferred via config.routing.preferredProviders (${provider.id})`,
      { prepend: true },
    );
    return score + 280;
  }
  return score;
}

function applyCooldownPenalty(score, provider, candidate) {
  if (candidate.health.status === "cooldown") {
    addReasonContribution(
      candidate,
      {
        kind: "health-penalty",
        id: "health.cooldown",
        label: "Cooldown penalty applied because the provider is temporarily unhealthy",
        delta: -1200,
        category: "health",
        evidence: candidate.health.cooldownUntil ?? null,
      },
      `${provider.label} is in cooldown until ${candidate.health.cooldownUntil}`,
      { prepend: true },
    );
    return score - 1200;
  }
  return score;
}

function evaluateSerpApiSearchEngineConstraints(request) {
  if (!request.searchEngine || request.searchEngine === "google") {
    return [];
  }

  const issues = [];
  if (request.news) {
    issues.push("SerpAPI news mode only works with the google sub-engine");
  }
  if (request.timeRange || request.fromDate || request.toDate) {
    issues.push("SerpAPI date and time filters only work with the google sub-engine");
  }
  return issues;
}

function applyQuerySignalBonus(score, provider, request, candidate) {
  return (candidate.signalMatches ?? []).reduce((total, signal) => {
    const delta = signal.providerDeltas?.[provider.id];
    if (!delta) {
      return total;
    }
    addReasonContribution(
      candidate,
      {
        kind: "signal",
        id: signal.id,
        label: signal.label,
        delta,
        category: signal.category,
        evidence: signal.evidence,
      },
      signal.label,
      { prepend: true },
    );
    return total + delta;
  }, score);
}

function evaluateSearchCandidate(provider, request, env, config, healthState, now, options = {}) {
  const candidate = buildCandidateBase(provider, env, config, healthState, now, options);
  candidate.signalMatches = options.signalMatches ?? [];
  const effectiveProvider = candidate.provider;

  if (request.engine && provider.id !== request.engine) {
    candidate.hardConstraints.explicitEngineMismatch = true;
    candidate.summary = `Skipped because --engine ${request.engine} was requested`;
    return finalizeCandidate(candidate, "skipped");
  }

  if (providerIsDisabled(provider, config)) {
    addIssue(candidate, `${provider.label} is disabled by config.routing.disabledProviders`, {
      key: "disabledByConfig",
      value: true,
    });
    return finalizeCandidate(candidate, "rejected");
  }
  if (providerUsesNoKeyBaseline(provider) && !config.routing.allowNoKeyBaseline) {
    addIssue(candidate, `${provider.label} is disabled by routing.allowNoKeyBaseline=false`, {
      key: "baselineDisallowed",
      value: true,
    });
    return finalizeCandidate(candidate, "rejected");
  }
  if (!effectiveProvider.capabilities.search) {
    addIssue(candidate, `${provider.label} does not support search`, {
      key: "missingCapability",
      value: "search",
    });
    return finalizeCandidate(candidate, "rejected");
  }
  if (!candidate.configured) {
    if (candidate.configurationError) {
      addIssue(candidate, candidate.configurationError, {
        key: "invalidConfiguration",
        value: true,
      });
    } else {
      addIssue(candidate, buildMissingCredentialMessage(provider), {
        key: "missingCredentials",
        value: true,
      });
    }
  }
  if (request.deep && !effectiveProvider.capabilities.deepSearch) {
    addIssue(candidate, `${provider.label} does not support --deep`, {
      key: "missingCapability",
      value: "deepSearch",
    });
  }
  if (request.news && !effectiveProvider.capabilities.newsSearch) {
    addIssue(candidate, `${provider.label} does not support --news`, {
      key: "missingCapability",
      value: "newsSearch",
    });
  }
  if (request.days !== null && !effectiveProvider.capabilities.newsDays) {
    addIssue(candidate, `${provider.label} does not support --days`, {
      key: "missingCapability",
      value: "newsDays",
    });
  }
  if ((request.country || request.lang) && !effectiveProvider.capabilities.localeFiltering) {
    addIssue(candidate, `${provider.label} does not support --country/--lang`, {
      key: "missingCapability",
      value: "localeFiltering",
    });
  }
  if (request.timeRange && !effectiveProvider.capabilities.timeRange) {
    addIssue(candidate, `${provider.label} does not support --time-range`, {
      key: "missingCapability",
      value: "timeRange",
    });
  }
  if ((request.fromDate || request.toDate) && !effectiveProvider.capabilities.dateRange) {
    addIssue(candidate, `${provider.label} does not support --from/--to`, {
      key: "missingCapability",
      value: "dateRange",
    });
  }
  if (
    request.searchEngine &&
    !effectiveProvider.capabilities.subEngines.includes(request.searchEngine)
  ) {
    addIssue(
      candidate,
      `${provider.label} does not support --search-engine ${request.searchEngine}`,
      {
        key: "missingCapability",
        value: `sub-engine:${request.searchEngine}`,
      },
    );
  }
  if (provider.id === "serpapi") {
    for (const issue of evaluateSerpApiSearchEngineConstraints(request)) {
      addIssue(candidate, issue, {
        key: "providerSpecific",
        value: issue,
      });
    }
  }

  if (candidate.issues.length > 0) {
    return finalizeCandidate(candidate, "rejected");
  }

  let score = provider.routing.defaultSearchPriority;
  addContribution(candidate, {
    kind: "base",
    id: "provider.default-search-priority",
    label: "Provider default search priority",
    delta: provider.routing.defaultSearchPriority,
    category: "provider",
    evidence: provider.id,
  });

  if (request.engine === provider.id) {
    score += 1000;
    addReasonContribution(
      candidate,
      {
        kind: "constraint",
        id: "request.explicit-engine",
        label: "Provider was selected explicitly via --engine",
        delta: 1000,
        category: "request",
        evidence: provider.id,
      },
      `selected explicitly via --engine ${provider.id}`,
    );
  }
  if (request.searchEngine) {
    score += 700;
    addReasonContribution(
      candidate,
      {
        kind: "constraint",
        id: "request.search-engine",
        label: "Supports the requested sub-engine",
        delta: 700,
        category: "request",
        evidence: request.searchEngine,
      },
      `supports requested sub-engine ${request.searchEngine}`,
      { prepend: true },
    );
  }

  if (request.news && request.days !== null) {
    score = 1000 + provider.routing.defaultSearchPriority;
    addReasonContribution(
      candidate,
      {
        kind: "constraint",
        id: "request.news-days",
        label: "Selected because --news --days requires Tavily support",
        delta: 1000,
        category: "request",
        evidence: "--news --days",
      },
      "required because --news --days is Tavily-only",
      { prepend: true },
    );
  } else if (request.news) {
    score = provider.routing.newsSearchPriority || provider.routing.defaultSearchPriority;
    if (provider.id === "serper") {
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.news-serper",
          label: "Preferred for news coverage",
          delta:
            (provider.routing.newsSearchPriority || provider.routing.defaultSearchPriority) -
            provider.routing.defaultSearchPriority,
          category: "request",
          evidence: "--news",
        },
        "preferred for news coverage",
        { prepend: true },
      );
    } else if (provider.id === "tavily") {
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.news-tavily",
          label: "Supports news search with AI-optimized ranking",
          delta:
            (provider.routing.newsSearchPriority || provider.routing.defaultSearchPriority) -
            provider.routing.defaultSearchPriority,
          category: "request",
          evidence: "--news",
        },
        "supports news search with AI-optimized ranking",
        { prepend: true },
      );
    } else if (provider.id === "serpapi") {
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.news-serpapi",
          label: "Supports news search as a multi-engine fallback",
          delta:
            (provider.routing.newsSearchPriority || provider.routing.defaultSearchPriority) -
            provider.routing.defaultSearchPriority,
          category: "request",
          evidence: "--news",
        },
        "supports news search as a multi-engine fallback",
        { prepend: true },
      );
    } else {
      addContribution(candidate, {
        kind: "constraint",
        id: "request.news-generic",
        label: "News search request uses provider news priority",
        delta:
          (provider.routing.newsSearchPriority || provider.routing.defaultSearchPriority) -
          provider.routing.defaultSearchPriority,
        category: "request",
        evidence: "--news",
      });
    }
  }

  if (request.deep) {
    score = provider.routing.deepSearchPriority || provider.routing.defaultSearchPriority;
    if (provider.id === "tavily") {
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.deep-tavily",
          label: "Supports deep search with advanced mode",
          delta:
            (provider.routing.deepSearchPriority || provider.routing.defaultSearchPriority) -
            provider.routing.defaultSearchPriority,
          category: "request",
          evidence: "--deep",
        },
        "supports deep search with advanced mode",
        { prepend: true },
      );
    } else if (provider.id === "exa") {
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.deep-exa",
          label: "Supports deep search as the strongest fallback",
          delta:
            (provider.routing.deepSearchPriority || provider.routing.defaultSearchPriority) -
            provider.routing.defaultSearchPriority,
          category: "request",
          evidence: "--deep",
        },
        "supports deep search as the strongest fallback",
        { prepend: true },
      );
    } else {
      addContribution(candidate, {
        kind: "constraint",
        id: "request.deep-generic",
        label: "Deep search request uses provider deep-search priority",
        delta:
          (provider.routing.deepSearchPriority || provider.routing.defaultSearchPriority) -
          provider.routing.defaultSearchPriority,
        category: "request",
        evidence: "--deep",
      });
    }
  }

  if (request.includeDomains?.length || request.excludeDomains?.length) {
    if (effectiveProvider.capabilities.domainFilterMode === "native") {
      score += 140;
      addReasonContribution(
        candidate,
        {
          kind: "constraint",
          id: "request.domain-filter-native",
          label: "Supports native domain filtering",
          delta: 140,
          category: "request",
          evidence: "domain-filter",
        },
        "supports native domain filtering",
        { prepend: true },
      );
    } else if (effectiveProvider.capabilities.domainFilterMode === "query") {
      score += 40;
      addReasonContribution(
        candidate,
        {
          kind: "fallback",
          id: "request.domain-filter-query",
          label: "Uses query-operator domain filtering fallback",
          delta: 40,
          category: "request",
          evidence: "domain-filter",
        },
        "uses query-operator domain filtering fallback",
      );
    }
  }

  if (request.country || request.lang) {
    score += 90;
    addReasonContribution(
      candidate,
      {
        kind: "constraint",
        id: "request.locale",
        label: "Supports locale-specific filtering",
        delta: 90,
        category: "request",
        evidence: `${request.country ?? ""}:${request.lang ?? ""}`,
      },
      "supports locale-specific filtering",
      { prepend: true },
    );
  }

  if (provider.id === "ddg" && !request.deep && !request.news) {
    addReasonContribution(
      candidate,
      {
        kind: "fallback",
        id: "provider.no-key-baseline",
        label: "No-key baseline search fallback",
        delta: 0,
        category: "availability",
        evidence: provider.id,
      },
      "no-key baseline search fallback",
      { prepend: true },
    );
  }

  score = applyQuerySignalBonus(score, provider, request, candidate);
  score = applyPreferenceBonus(score, provider, config, candidate);
  score = applyRoutingPolicy(score, provider, config, candidate);
  score = applyCooldownPenalty(score, provider, candidate);

  if (candidate.reasons.length === 0) {
    candidate.reasons.push(provider.routing.defaultReason);
  }

  candidate.score = score;
  return finalizeCandidate(candidate, "candidate");
}

function evaluateExtractCandidate(provider, request, env, config, healthState, now, options = {}) {
  const candidate = buildCandidateBase(provider, env, config, healthState, now, options);

  if (request.engine && provider.id !== request.engine) {
    candidate.summary = `Skipped because --engine ${request.engine} was requested`;
    return finalizeCandidate(candidate, "skipped");
  }

  if (providerIsDisabled(provider, config)) {
    candidate.issues.push(`${provider.label} is disabled by config.routing.disabledProviders`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (providerUsesNoKeyBaseline(provider) && !config.routing.allowNoKeyBaseline) {
    candidate.issues.push(`${provider.label} is disabled by routing.allowNoKeyBaseline=false`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (provider.activation === "render") {
    if (!config.render.enabled) {
      candidate.issues.push("Browser render lane is disabled by config.render.enabled=false");
      return finalizeCandidate(candidate, "rejected");
    }
    if (config.render.policy === "off") {
      candidate.issues.push("Browser render lane is disabled by config.render.policy=off");
      return finalizeCandidate(candidate, "rejected");
    }
    if (!candidate.runtimeAvailable) {
      candidate.issues.push("Browser render runtime is unavailable on this machine");
      return finalizeCandidate(candidate, "rejected");
    }
  }
  if (!provider.capabilities.extract) {
    candidate.issues.push(`${provider.label} does not support extraction`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (!candidate.configured && provider.activation !== "render") {
    candidate.issues.push(buildMissingCredentialMessage(provider));
    return finalizeCandidate(candidate, "rejected");
  }

  let score = provider.routing.extractPriority;
  if (request.engine === provider.id) {
    score += 1000;
    candidate.reasons.push(`selected explicitly via --engine ${provider.id}`);
  }
  if (provider.id === "tavily") {
    candidate.reasons.unshift("preferred extract provider");
  } else if (provider.id === "exa") {
    candidate.reasons.unshift("fallback extract provider");
  } else if (provider.id === "fetch") {
    candidate.reasons.unshift("no-key safe fetch fallback");
  } else if (provider.id === "render") {
    if (config.render.policy === "force") {
      score += 2000;
      candidate.reasons.unshift("browser render forced via config.render.policy=force");
    } else {
      candidate.reasons.unshift("browser render lane available as a JS-capable fallback");
    }
  }

  score = applyPreferenceBonus(score, provider, config, candidate);
  score = applyRoutingPolicy(score, provider, config, candidate);
  score = applyCooldownPenalty(score, provider, candidate);
  candidate.score = score;
  return finalizeCandidate(candidate, "candidate");
}

function evaluateDiscoveryCandidate(provider, request, env, config, healthState, now, capability) {
  const candidate = buildCandidateBase(provider, env, config, healthState, now);

  if (request.engine && provider.id !== request.engine) {
    candidate.summary = `Skipped because --engine ${request.engine} was requested`;
    return finalizeCandidate(candidate, "skipped");
  }

  if (providerIsDisabled(provider, config)) {
    candidate.issues.push(`${provider.label} is disabled by config.routing.disabledProviders`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (providerUsesNoKeyBaseline(provider) && !config.routing.allowNoKeyBaseline) {
    candidate.issues.push(`${provider.label} is disabled by routing.allowNoKeyBaseline=false`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (!provider.capabilities[capability]) {
    candidate.issues.push(`${provider.label} does not support ${capability}`);
    return finalizeCandidate(candidate, "rejected");
  }
  if (!candidate.configured) {
    candidate.issues.push(buildMissingCredentialMessage(provider));
    return finalizeCandidate(candidate, "rejected");
  }

  let score = capability === "crawl" ? provider.routing.extractPriority : 20;
  if (provider.id === "fetch") {
    candidate.reasons.unshift(`no-key ${capability} baseline`);
  }

  score = applyPreferenceBonus(score, provider, config, candidate);
  score = applyRoutingPolicy(score, provider, config, candidate);
  score = applyCooldownPenalty(score, provider, candidate);
  candidate.score = score;
  return finalizeCandidate(candidate, "candidate");
}

function findCandidate(candidates, providerId) {
  return candidates.find((candidate) => candidate.provider.id === providerId) ?? null;
}

function buildSearchRouteError(request, candidates, config) {
  if (request.engine) {
    const forcedCandidate = findCandidate(candidates, request.engine);
    if (forcedCandidate?.issues.length) {
      return forcedCandidate.issues[0];
    }
    return `Engine ${request.engine} selected but requirements are not satisfied.`;
  }
  if (!config.routing.allowNoKeyBaseline) {
    return [
      "No search engine configured.",
      "Set at least one API key or enable routing.allowNoKeyBaseline.",
    ].join(" ");
  }
  if (request.searchEngine) {
    const serpApiCandidate = findCandidate(candidates, "serpapi");
    const unsupportedSearchEngineIssue = serpApiCandidate?.issues.find(
      (issue) =>
        issue.includes("news mode only works with the google sub-engine") ||
        issue.includes("date and time filters only work with the google sub-engine"),
    );
    if (unsupportedSearchEngineIssue) {
      return unsupportedSearchEngineIssue;
    }
    return `--search-engine ${request.searchEngine} requires SERPAPI_API_KEY`;
  }
  if (request.news && request.days !== null) {
    return "--news --days requires TAVILY_API_KEY";
  }
  if (request.news) {
    return "--news requires SERPER_API_KEY, TAVILY_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, or SEARXNG_INSTANCE_URL";
  }
  if (request.deep) {
    return "--deep requires TAVILY_API_KEY or EXA_API_KEY";
  }
  if (request.country || request.lang) {
    return "--country/--lang requires SERPER_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, BRAVE_API_KEY, or QUERIT_API_KEY";
  }
  if (request.timeRange) {
    return "--time-range requires TAVILY_API_KEY, EXA_API_KEY, SERPER_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, BRAVE_API_KEY, SEARXNG_INSTANCE_URL, QUERIT_API_KEY, or native PERPLEXITY_API_KEY";
  }
  if (request.fromDate || request.toDate) {
    return "--from/--to requires TAVILY_API_KEY, EXA_API_KEY, SERPER_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, BRAVE_API_KEY, or native PERPLEXITY_API_KEY";
  }
  return [
    "No search engine configured.",
    "Set at least one provider credential or endpoint: TAVILY_API_KEY, EXA_API_KEY, QUERIT_API_KEY, SERPER_API_KEY, BRAVE_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, PERPLEXITY_API_KEY, OPENROUTER_API_KEY, KILOCODE_API_KEY, PERPLEXITY_GATEWAY_API_KEY + PERPLEXITY_BASE_URL, or SEARXNG_INSTANCE_URL",
  ].join(" ");
}

function buildExtractRouteError(request, config, candidates) {
  if (request.engine) {
    const forcedCandidate = findCandidate(candidates, request.engine);
    if (forcedCandidate?.issues.length) {
      return forcedCandidate.issues[0];
    }
    return `${request.engine} API key not configured or provider does not support extraction`;
  }
  if (!config.routing.allowNoKeyBaseline) {
    return "No extract engine available. Enable routing.allowNoKeyBaseline or set TAVILY_API_KEY / EXA_API_KEY";
  }
  const renderCandidate = findCandidate(candidates, "render");
  if (renderCandidate?.issues.length && config.render.enabled) {
    return renderCandidate.issues[0];
  }
  return "No extract engine available. Set TAVILY_API_KEY or EXA_API_KEY";
}

function buildDiscoveryRouteError(command, request, config) {
  if (request.engine) {
    return `${request.engine} does not support ${command} or is not configured`;
  }
  if (!config.routing.allowNoKeyBaseline) {
    return `${command} requires routing.allowNoKeyBaseline=true because the current implementation uses Safe Fetch`;
  }
  return `${command} requires the Safe Fetch baseline provider`;
}

function sortCandidates(a, b) {
  const order = { selected: 0, candidate: 1, rejected: 2, skipped: 3 };
  if (order[a.status] !== order[b.status]) {
    return order[a.status] - order[b.status];
  }
  return (b.score ?? -1) - (a.score ?? -1);
}

function buildPlan(command, request, candidates, env, config, options = {}) {
  const selected = [...candidates]
    .filter((candidate) => candidate.status === "candidate")
    .sort((left, right) => (right.score ?? 0) - (left.score ?? 0))[0];

  return {
    command,
    request,
    signalMatches: options.signalMatches ?? [],
    configuredProviders: listEffectiveProviders(env, config, options).map((provider) => provider.id),
    selected: selected ? { ...selected, status: "selected" } : null,
    candidates: candidates
      .map((candidate) =>
        candidate === selected ? { ...candidate, status: "selected" } : candidate,
      )
      .sort(sortCandidates),
  };
}

function buildRenderPlan(plan, config, options = {}) {
  const renderProvider = getProvider("render");
  if (!renderProvider) {
    return null;
  }
  const runtimeAvailable = renderProvider
    ? isProviderRuntimeAvailable(renderProvider, {
        env: options.env,
        runtimeAvailability: options.runtimeAvailability,
      })
    : false;
  const selectedRender = plan.selected?.provider.id === "render";

  let reason = null;
  if (!config.render.enabled) {
    reason = "render.enabled=false";
  } else if (config.render.policy === "off") {
    reason = "render.policy=off";
  } else if (!runtimeAvailable) {
    reason = "browser runtime unavailable";
  } else if (selectedRender) {
    reason = "browser render selected as the primary extract lane";
  } else if (config.render.policy === "fallback") {
    reason = "browser render available to recover failed or empty extractions";
  } else if (config.render.policy === "force") {
    reason = "browser render is forced as the primary extract lane";
  }

  return {
    enabled: config.render.enabled,
    policy: config.render.policy,
    runtimeAvailable,
    provider: renderProvider,
    waitUntil: config.render.waitUntil,
    budgetMs: config.render.budgetMs,
    blockTypes: config.render.blockTypes,
    sameOriginOnly: config.render.sameOriginOnly,
    fallbackAvailable:
      config.render.enabled &&
      config.render.policy === "fallback" &&
      runtimeAvailable &&
      !selectedRender,
    reason,
  };
}

export function planSearchRoute(requestInput, options = {}) {
  const env = options.env ?? process.env;
  const config = options.config ?? DEFAULT_CONFIG;
  const now = options.now ?? Date.now();
  const healthState = options.healthState ?? { providers: {} };
  const request = normalizeSearchRequest(requestInput);
  const signalMatches = analyzeSearchSignals(request);

  const providers = request.engine
    ? listProviders().filter((provider) => provider.id === request.engine)
    : listProviders();
  const candidates = providers.map((provider) =>
    evaluateSearchCandidate(provider, request, env, config, healthState, now, {
      ...options,
      signalMatches,
    }),
  );
  const plan = buildPlan("search", request, candidates, env, config, {
    ...options,
    signalMatches,
  });

  return enrichPlanWithRoutingConfidence({
    ...plan,
    federation: buildFederationPlan(plan, config),
    error: plan.selected ? null : { message: buildSearchRouteError(request, plan.candidates, config) },
  });
}

export function planExtractRoute(requestInput, options = {}) {
  const env = options.env ?? process.env;
  const config = options.config ?? DEFAULT_CONFIG;
  const now = options.now ?? Date.now();
  const healthState = options.healthState ?? { providers: {} };
  const request = normalizeExtractRequest(requestInput);

  const providers = request.engine
    ? listProviders().filter((provider) => provider.id === request.engine)
    : listProviders().filter((provider) => provider.capabilities.extract);
  const candidates = providers.map((provider) =>
    evaluateExtractCandidate(provider, request, env, config, healthState, now, options),
  );
  const plan = buildPlan("extract", request, candidates, env, config, options);

  return {
    ...plan,
    render: buildRenderPlan(plan, config, options),
    error: plan.selected
      ? null
      : { message: buildExtractRouteError(request, config, plan.candidates) },
  };
}

function planDiscoveryRoute(command, capability, requestInput, options = {}) {
  const env = options.env ?? process.env;
  const config = options.config ?? DEFAULT_CONFIG;
  const now = options.now ?? Date.now();
  const healthState = options.healthState ?? { providers: {} };
  const request = normalizeDiscoveryRequest(requestInput);

  const providers = request.engine
    ? listProviders().filter((provider) => provider.id === request.engine)
    : listProviders().filter((provider) => provider.capabilities[capability]);
  const candidates = providers.map((provider) =>
    evaluateDiscoveryCandidate(provider, request, env, config, healthState, now, capability),
  );
  const plan = buildPlan(command, request, candidates, env, config);

  return {
    ...plan,
    error: plan.selected ? null : { message: buildDiscoveryRouteError(command, request, config) },
  };
}

export function planCrawlRoute(requestInput, options = {}) {
  return planDiscoveryRoute("crawl", "crawl", requestInput, options);
}

export function planMapRoute(requestInput, options = {}) {
  return planDiscoveryRoute("map", "map", requestInput, options);
}

export function requireSelectedRoute(plan) {
  if (!plan.selected) {
    throw new Error(plan.error?.message ?? "No route selected");
  }
  return plan.selected;
}

function serializeProvider(provider) {
  return {
    id: provider.id,
    label: provider.label,
    envVars: provider.envVars,
    capabilities: provider.capabilities,
    limits: provider.limits,
  };
}

export function serializePlan(plan) {
  return {
    ...plan,
    render: plan.render
      ? {
          ...plan.render,
          provider: plan.render.provider ? serializeProvider(plan.render.provider) : null,
        }
      : undefined,
    selected: plan.selected
      ? {
          ...plan.selected,
          provider: serializeProvider(plan.selected.provider),
        }
      : null,
    candidates: plan.candidates.map((candidate) => ({
      ...candidate,
      provider: serializeProvider(candidate.provider),
    })),
  };
}

export function formatPlanMarkdown(plan) {
  const lines = [];
  const selected = plan.selected;

  lines.push(`# ${plan.command} route plan`);
  lines.push("");

  if (selected) {
    lines.push(`- Selected provider: ${selected.provider.id}`);
    lines.push(`- Why: ${selected.summary}`);
    if (selected.selectionMode) {
      lines.push(`- Selection mode: ${selected.selectionMode}`);
    }
    if (selected.confidenceLevel) {
      lines.push(`- Confidence: ${selected.confidenceLevel} (${selected.confidence})`);
    }
  } else {
    lines.push("- No provider selected");
    lines.push(`- Error: ${plan.error?.message ?? "Unknown routing error"}`);
  }

  if (plan.configuredProviders.length > 0) {
    lines.push(`- Configured providers: ${plan.configuredProviders.join(", ")}`);
  } else {
    lines.push("- Configured providers: none");
  }

  if (plan.render) {
    lines.push(
      `- Browser render lane: ${plan.render.enabled ? "enabled" : "disabled"} (policy=${plan.render.policy}, runtime=${plan.render.runtimeAvailable ? "ready" : "missing"})`,
    );
  }

  lines.push("");
  lines.push("## Candidates");
  lines.push("");

  for (const candidate of plan.candidates) {
    lines.push(
      `- ${candidate.provider.id}: ${candidate.status} - ${candidate.summary || "no summary"}`,
    );
  }

  return lines.join("\n");
}
