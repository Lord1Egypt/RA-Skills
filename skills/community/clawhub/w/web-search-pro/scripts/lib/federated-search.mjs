import { dedupeFederatedResults } from "./dedupe.mjs";
import { normalizeProviderSearchResult } from "./normalize-result.mjs";
import { getProvider } from "./providers.mjs";
import { rerankFederatedResults } from "./rerank.mjs";

function isAmbiguousQuery(request) {
  const query = String(request.query ?? "").trim();
  if (!query) {
    return false;
  }
  if (
    request.deep ||
    request.news ||
    request.searchEngine ||
    request.country ||
    request.lang ||
    request.fromDate ||
    request.toDate ||
    request.timeRange ||
    request.includeDomains?.length ||
    request.excludeDomains?.length
  ) {
    return false;
  }

  const tokens = query.split(/\s+/).filter(Boolean);
  if (tokens.length > 3) {
    return false;
  }
  return !/["':]/.test(query);
}

function isComparisonQuery(request) {
  const query = String(request.query ?? "").trim().toLowerCase();
  if (!query) {
    return false;
  }
  return /\b(vs|versus|compare|comparison|differences?|tradeoffs?)\b/.test(query);
}

function buildTriggerReasons(request, config) {
  const reasons = [];
  if (request.news && config.routing.federationTriggers.includes("news")) {
    reasons.push("news");
  }
  if (request.mode === "research" && config.routing.federationTriggers.includes("research")) {
    reasons.push("research");
  }
  if (isComparisonQuery(request) && config.routing.federationTriggers.includes("comparison")) {
    reasons.push("comparison");
  }
  if (
    (request.includeDomains?.length || request.excludeDomains?.length) &&
    config.routing.federationTriggers.includes("domain-critical")
  ) {
    reasons.push("domain-critical");
  }
  if (
    request.mode !== "research" &&
    isAmbiguousQuery(request) &&
    config.routing.federationTriggers.includes("ambiguous")
  ) {
    reasons.push("ambiguous");
  }
  return reasons;
}

function scoreFanoutCandidate(candidate, primaryCandidate, config, request) {
  let score = candidate.score ?? 0;
  const reasons = [];
  const primaryCapabilities = primaryCandidate.provider.capabilities;
  const candidateCapabilities = candidate.provider.capabilities;

  if (
    (request.includeDomains?.length || request.excludeDomains?.length) &&
    candidateCapabilities.domainFilterMode !== primaryCapabilities.domainFilterMode
  ) {
    score += 90;
    reasons.push("different domain filter mode adds coverage diversity");
  }
  if (
    (request.country || request.lang) &&
    candidateCapabilities.localeFiltering !== primaryCapabilities.localeFiltering
  ) {
    score += 70;
    reasons.push("different locale support complements the primary provider");
  }
  if (candidateCapabilities.answerSynthesis !== primaryCapabilities.answerSynthesis) {
    score += 45;
    reasons.push("different answer synthesis behavior improves source diversity");
  }
  if (
    request.searchEngine &&
    (candidateCapabilities.subEngines?.length ?? 0) > (primaryCapabilities.subEngines?.length ?? 0)
  ) {
    score += 55;
    reasons.push("additional sub-engine coverage improves fallback breadth");
  }
  if (
    request.news ||
    request.timeRange ||
    request.fromDate ||
    request.toDate ||
    request.mode === "research"
  ) {
    if (candidateCapabilities.newsSearch || candidateCapabilities.dateRange || candidateCapabilities.timeRange) {
      score += 50;
      reasons.push("supports fresher or time-aware search behavior");
    }
  }
  score += (candidate.provider.routing.qualityScore ?? 0) * 10;
  if (
    candidate.provider.activation === "baseline" &&
    primaryCandidate.provider.activation !== "baseline"
  ) {
    score -= 160;
    reasons.push("baseline fallback stays behind credentialed fanout options");
  }
  if (candidate.health?.status === "degraded") {
    score -= 80;
    reasons.push("recent degraded health lowers fanout desirability");
  }

  if (config.routing.mergePolicy === "diversity-first") {
    score += 60;
    reasons.push("diversity-first policy boosts complementary fanout providers");
  }

  return {
    score,
    reasons,
  };
}

function resolveFanoutLimit(triggerReasons, config) {
  const preferredMax = triggerReasons.some((value) =>
    ["news", "research", "comparison"].includes(value),
  )
    ? 2
    : 1;
  return Math.min(config.routing.maxFanoutProviders, preferredMax);
}

function buildFanoutSummary(fanoutCandidates, maxFanoutProviders) {
  return {
    plannedCount: fanoutCandidates.length,
    maxFanoutProviders,
    providerIds: fanoutCandidates.map((candidate) => candidate.provider.id),
  };
}

function countProviderHits(results = []) {
  return results.reduce((acc, item) => {
    acc[item.providerId] = (acc[item.providerId] ?? 0) + 1;
    return acc;
  }, {});
}

export function buildFederationPlan(plan, config) {
  const base = {
    enabled: config.routing.enableFederation,
    triggered: false,
    primaryProvider: plan.selected?.provider.id ?? null,
    providersPlanned: plan.selected?.provider.id ? [plan.selected.provider.id] : [],
    providersUsed: [],
    triggerReasons: [],
    mergePolicy: config.routing.mergePolicy,
    maxFanoutProviders: config.routing.maxFanoutProviders,
    maxPerProvider: config.routing.maxPerProvider,
    fanoutPolicy: "disabled",
    fanoutSummary: buildFanoutSummary([], config.routing.maxFanoutProviders),
    resultStats: null,
    mergeSummary: null,
    reason: "",
  };

  if (!config.routing.enableFederation) {
    return {
      ...base,
      reason: "disabled by config.routing.enableFederation",
    };
  }
  if (!plan.selected) {
    return {
      ...base,
      reason: "no primary provider selected",
    };
  }
  if (plan.request.engine) {
    return {
      ...base,
      fanoutPolicy: "explicit-primary-only",
      reason: "disabled because an explicit --engine was requested",
    };
  }
  if (config.routing.mergePolicy === "primary-only") {
    return {
      ...base,
      fanoutPolicy: "explicit-primary-only",
      reason: "disabled because routing.mergePolicy=primary-only",
    };
  }

  const triggerReasons = buildTriggerReasons(plan.request, config);
  if (triggerReasons.length === 0) {
    return {
      ...base,
      reason: "no federation trigger matched the current request",
    };
  }

  const primaryCandidate = plan.selected;
  const maxFanoutProviders = resolveFanoutLimit(triggerReasons, config);
  const fanoutCandidates = plan.candidates
    .filter(
      (candidate) =>
        candidate.status !== "rejected" &&
        candidate.status !== "skipped" &&
        candidate.provider.id !== primaryCandidate.provider.id,
    )
    .map((candidate) => {
      const federationScore = scoreFanoutCandidate(
        candidate,
        primaryCandidate,
        config,
        plan.request,
      );
      return {
        ...candidate,
        federationScore: federationScore.score,
        federationReasons: federationScore.reasons,
      };
    })
    .filter((candidate) => candidate.federationScore > 0)
    .sort((left, right) => right.federationScore - left.federationScore)
    .slice(0, maxFanoutProviders);

  const providersPlanned = [
    primaryCandidate.provider.id,
    ...fanoutCandidates.map((candidate) => candidate.provider.id),
  ];

  return {
    ...base,
    triggered: fanoutCandidates.length > 0,
    providersPlanned,
    triggerReasons,
    maxFanoutProviders,
    fanoutPolicy: fanoutCandidates.length > 0 ? "triggered" : "disabled",
    fanoutSummary: buildFanoutSummary(fanoutCandidates, maxFanoutProviders),
    fanoutProviders: fanoutCandidates.map((candidate) => ({
      providerId: candidate.provider.id,
      score: candidate.federationScore,
      reason: candidate.summary,
      reasons: candidate.federationReasons,
    })),
    reason:
      fanoutCandidates.length > 0
        ? `triggered by ${triggerReasons.join(", ")}`
        : "no additional provider candidates survived federation planning",
  };
}

function getProviderExecutor(providerId, providerExecutors) {
  if (providerExecutors?.[providerId]) {
    return providerExecutors[providerId];
  }
  const provider = getProvider(providerId);
  if (!provider?.adapter?.search) {
    throw new Error(`No search executor available for provider ${providerId}`);
  }
  return provider.adapter.search;
}

function buildProviderOutcome(providerId, status, role, error = null) {
  return {
    providerId,
    status,
    role,
    ...(error ? { error } : {}),
  };
}

function createFederatedExecutionError(message, providerOutcomes, failedProviders, federation) {
  const error = new Error(message);
  error.providerOutcomes = providerOutcomes;
  error.failedProviders = failedProviders;
  error.federation = federation;
  return error;
}

function createProviderOptions(request, providerId, config, primaryProviderId) {
  const isPrimary = providerId === primaryProviderId;
  return {
    ...request,
    count: isPrimary
      ? Math.max(request.count ?? 5, config.routing.maxPerProvider)
      : config.routing.maxPerProvider,
  };
}

export async function executeFederatedSearch(options) {
  const {
    query,
    request,
    plan,
    config,
    providerExecutors,
  } = options;
  const federation = plan.federation ?? buildFederationPlan(plan, config);
  const providersPlanned = federation.triggered
    ? federation.providersPlanned
    : plan.selected
      ? [plan.selected.provider.id]
      : [];

  const outcomes = await Promise.allSettled(
    providersPlanned.map(async (providerId) => {
      const executor = getProviderExecutor(providerId, providerExecutors);
      const providerResult = await executor(
        query,
        createProviderOptions(request, providerId, config, plan.selected?.provider.id ?? null),
      );
      return {
        providerId,
        providerResult,
      };
    }),
  );

  const successes = [];
  const failedProviders = [];
  const providerOutcomes = [];

  for (let index = 0; index < outcomes.length; index++) {
    const providerId = providersPlanned[index];
    const outcome = outcomes[index];
    const role = providerId === federation.primaryProvider ? "primary" : "fanout";
    if (outcome.status === "fulfilled") {
      successes.push(outcome.value);
      providerOutcomes.push(buildProviderOutcome(providerId, "success", role));
      continue;
    }
    const errorMessage = outcome.reason?.message ?? String(outcome.reason);
    failedProviders.push({
      providerId,
      error: errorMessage,
    });
    providerOutcomes.push(
      buildProviderOutcome(providerId, "failure", role, new Error(errorMessage)),
    );
  }

  if (successes.length === 0) {
    throw createFederatedExecutionError(
      failedProviders[0]?.error ?? "All federated providers failed",
      providerOutcomes,
      failedProviders,
      federation,
    );
  }

  const normalizedResults = successes.flatMap(({ providerId, providerResult }) =>
    normalizeProviderSearchResult(providerId, providerResult, {
      maxItems: providerId === federation.primaryProvider
        ? Math.max(request.count ?? 5, config.routing.maxPerProvider)
        : config.routing.maxPerProvider,
    }),
  );

  const reranked = rerankFederatedResults(normalizedResults, {
    primaryProviderId: federation.primaryProvider,
    request,
    mergePolicy: federation.mergePolicy,
  });
  const deduped = dedupeFederatedResults(reranked);
  const finalResults = deduped.results.slice(0, request.count ?? 5);

  const primarySuccess = successes.some(
    (entry) => entry.providerId === federation.primaryProvider,
  );
  const answerProvider =
    successes.find((entry) => entry.providerId === federation.primaryProvider && entry.providerResult.answer)
      ?.providerId ??
    successes.find((entry) => entry.providerResult.answer)?.providerId ??
    null;
  const answer =
    successes.find((entry) => entry.providerId === federation.primaryProvider)?.providerResult.answer ??
    successes.find((entry) => entry.providerResult.answer)?.providerResult.answer ??
    null;
  const providersUsed = successes.map((entry) => entry.providerId);

  return {
    primarySucceeded: primarySuccess,
    providersUsed,
    failedProviders,
    providerOutcomes,
    federation: {
      enabled: federation.enabled,
      triggered: federation.triggered,
      primaryProvider: federation.primaryProvider,
      providersPlanned: federation.providersPlanned,
      providersUsed,
      mergePolicy: federation.mergePolicy,
      maxPerProvider: federation.maxPerProvider,
      triggerReasons: federation.triggerReasons,
      fanoutPolicy: federation.fanoutPolicy,
      fanoutSummary: federation.fanoutSummary,
      resultStats: {
        rawResultCount: normalizedResults.length,
        dedupedResultCount: finalResults.length,
        providerHitCounts: countProviderHits(normalizedResults),
      },
      mergeSummary: {
        dedupedUrls: deduped.stats.dedupedUrls,
        nearDuplicateDrops: deduped.stats.nearDuplicateDrops,
        reranked: true,
        answerProvider,
      },
      failedProviders,
      primarySucceeded: primarySuccess,
    },
    result: {
      engine: federation.triggered ? "federated" : successes[0].providerResult.engine,
      answer,
      results: finalResults,
      failed: failedProviders.map((entry) => ({
        providerId: entry.providerId,
        error: entry.error,
      })),
    },
  };
}
