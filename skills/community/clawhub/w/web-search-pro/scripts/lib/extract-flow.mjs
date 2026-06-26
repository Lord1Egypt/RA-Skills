import { canonicalizeUrl } from "./dedupe.mjs";

export function isEmptyExtractContent(entry) {
  return !entry?.content || entry.content.trim().length === 0;
}

function attachProviderOutcomes(error, outcomes) {
  error.providerOutcomes = outcomes;
  return error;
}

function buildResultMap(results = []) {
  return new Map(results.map((entry) => [canonicalizeUrl(entry.url), entry]));
}

function buildFailureMap(failed = []) {
  return new Map(failed.map((entry) => [canonicalizeUrl(entry.url), entry]));
}

function normalizeUrls(urls = []) {
  return urls.map((url) => ({
    originalUrl: url,
    key: canonicalizeUrl(url),
  }));
}

function unresolvedUrlsForResults(urlEntries, resultMap) {
  return urlEntries
    .filter(({ key }) => {
      const entry = resultMap.get(key);
      return !entry || isEmptyExtractContent(entry);
    })
    .map(({ originalUrl }) => originalUrl);
}

function getExtractExecutor(provider, providerExecutors = {}) {
  if (providerExecutors[provider.id]) {
    return providerExecutors[provider.id];
  }
  return provider.adapter.extract.bind(provider.adapter);
}

function buildAttemptProviders(plan) {
  if (plan.selected?.provider.id === "render") {
    return [plan.selected.provider];
  }

  return plan.candidates
    .filter(
      (candidate) =>
        (candidate.status === "selected" || candidate.status === "candidate") &&
        candidate.provider.capabilities.extract &&
        candidate.provider.id !== "render",
    )
    .map((candidate) => candidate.provider);
}

function upsertResults(resultsByUrl, entries = []) {
  for (const entry of entries) {
    if (isEmptyExtractContent(entry)) {
      continue;
    }
    resultsByUrl.set(canonicalizeUrl(entry.url), entry);
  }
}

function upsertFailures(failuresByUrl, entries = [], fallbackError = null) {
  for (const entry of entries) {
    failuresByUrl.set(canonicalizeUrl(entry.url), entry);
  }
  if (!fallbackError) {
    return;
  }
  for (const entry of entries) {
    const key = canonicalizeUrl(entry.url);
    failuresByUrl.set(key, {
      url: entry.url,
      error: fallbackError.message,
    });
  }
}

function buildMergedResults(urls, resultsByUrl) {
  const merged = [];
  const seen = new Set();

  for (const url of urls) {
    const entry = resultsByUrl.get(canonicalizeUrl(url));
    if (!entry) {
      continue;
    }
    merged.push(entry);
    seen.add(canonicalizeUrl(entry.url));
  }

  for (const [key, entry] of resultsByUrl.entries()) {
    if (seen.has(key)) {
      continue;
    }
    merged.push(entry);
  }

  return merged;
}

function buildFinalFailures(urls, resultsByUrl, failuresByUrl) {
  const failures = [];

  for (const url of urls) {
    const key = canonicalizeUrl(url);
    const entry = resultsByUrl.get(key);
    if (entry && !isEmptyExtractContent(entry)) {
      continue;
    }
    failures.push(
      failuresByUrl.get(key) ?? {
        url,
        error: "No readable content extracted",
      },
    );
  }

  return failures;
}

function buildRenderFallbackMetadata(renderResult, renderTargets, renderConfig, error = null) {
  return {
    used: (renderResult?.results?.length ?? 0) > 0,
    policy: "fallback",
    fallbackAppliedTo: renderTargets,
    waitUntil: renderConfig.waitUntil,
    budgetMs: renderConfig.budgetMs,
    blockTypes: renderConfig.blockTypes,
    sameOriginOnly: renderConfig.sameOriginOnly,
    browserFamily: renderResult?.render?.browserFamily ?? null,
    browserPath: renderResult?.render?.browserPath ?? null,
    timedOut: Boolean(renderResult?.render?.timedOut),
    ...(error ? { error: error.message } : {}),
  };
}

function buildForcedRenderMetadata(renderResult, renderConfig) {
  return {
    ...(renderResult?.render ?? {}),
    used: (renderResult?.results?.length ?? 0) > 0,
    policy: "force",
    fallbackAppliedTo: [],
    waitUntil: renderConfig.waitUntil,
    budgetMs: renderConfig.budgetMs,
    blockTypes: renderConfig.blockTypes,
    sameOriginOnly: renderConfig.sameOriginOnly,
  };
}

function collectSuccessfulProviderIds(outcomes = []) {
  return [
    ...new Set(
      outcomes.filter((entry) => entry.status === "success").map((entry) => entry.providerId),
    ),
  ];
}

export function extractProvidersUsed(execution = {}) {
  if (execution.providersUsed?.length) {
    return execution.providersUsed;
  }
  return collectSuccessfulProviderIds(execution.outcomes ?? []);
}

export async function executeExtractFlow({
  urls,
  plan,
  config,
  providerExecutors = {},
}) {
  const outcomes = [];
  const selectedProvider = plan.selected?.provider;

  if (!selectedProvider) {
    throw new Error(plan.error?.message ?? "No extract route selected");
  }

  if (selectedProvider.id === "render") {
    try {
      const renderResult = await getExtractExecutor(selectedProvider, providerExecutors)(urls, {
        maxChars: config.fetch.maxChars,
        render: config.render,
      });
      outcomes.push({ providerId: "render", status: "success", role: "primary" });
      return {
        providerResult: {
          ...renderResult,
          render: buildForcedRenderMetadata(renderResult, config.render),
        },
        outcomes,
      };
    } catch (error) {
      outcomes.push({ providerId: "render", status: "failure", role: "primary", error });
      throw attachProviderOutcomes(error, outcomes);
    }
  }

  const urlEntries = normalizeUrls(urls);
  const resultsByUrl = new Map();
  const failuresByUrl = new Map();
  const attemptProviders = buildAttemptProviders(plan);
  const resultProviderIds = new Set();
  let unresolvedUrls = [...urls];
  let lastThrownError = null;
  let renderMetadata = null;

  for (const provider of attemptProviders) {
    if (unresolvedUrls.length === 0) {
      break;
    }

    try {
      const providerResult = await getExtractExecutor(provider, providerExecutors)(unresolvedUrls, {
        maxChars: config.fetch.maxChars,
        render: config.render,
      });
      outcomes.push({
        providerId: provider.id,
        status: "success",
        role: provider.id === selectedProvider.id ? "primary" : "fallback",
      });
      upsertResults(resultsByUrl, providerResult.results);
      upsertFailures(failuresByUrl, providerResult.failed);
      if ((providerResult.results ?? []).some((entry) => !isEmptyExtractContent(entry))) {
        resultProviderIds.add(provider.id);
      }
      unresolvedUrls = unresolvedUrlsForResults(urlEntries, resultsByUrl);
    } catch (error) {
      lastThrownError = error;
      outcomes.push({
        providerId: provider.id,
        status: "failure",
        role: provider.id === selectedProvider.id ? "primary" : "fallback",
        error,
      });
      upsertFailures(
        failuresByUrl,
        unresolvedUrls.map((url) => ({ url })),
        error,
      );
    }
  }

  if (unresolvedUrls.length > 0 && plan.render?.fallbackAvailable) {
    const renderTargets = [...unresolvedUrls];
    try {
      const renderResult = await getExtractExecutor(plan.render.provider, providerExecutors)(
        renderTargets,
        {
          maxChars: config.fetch.maxChars,
          render: config.render,
        },
      );
      outcomes.push({ providerId: "render", status: "success", role: "fallback" });
      upsertResults(resultsByUrl, renderResult.results);
      upsertFailures(failuresByUrl, renderResult.failed);
      if ((renderResult.results ?? []).some((entry) => !isEmptyExtractContent(entry))) {
        resultProviderIds.add("render");
      }
      unresolvedUrls = unresolvedUrlsForResults(urlEntries, resultsByUrl);
      renderMetadata = buildRenderFallbackMetadata(
        renderResult,
        renderTargets,
        config.render,
      );
    } catch (error) {
      lastThrownError = error;
      outcomes.push({ providerId: "render", status: "failure", role: "fallback", error });
      upsertFailures(
        failuresByUrl,
        renderTargets.map((url) => ({ url })),
        error,
      );
      renderMetadata = buildRenderFallbackMetadata(
        null,
        renderTargets,
        config.render,
        error,
      );
    }
  }

  const mergedResults = buildMergedResults(urls, resultsByUrl);
  const finalFailures = buildFinalFailures(urls, resultsByUrl, failuresByUrl);
  const usedProviders = [...resultProviderIds];

  if (mergedResults.length === 0 && finalFailures.length === urls.length && lastThrownError) {
    throw attachProviderOutcomes(lastThrownError, outcomes);
  }

  return {
    providerResult: {
      engine:
        usedProviders.length === 0
          ? selectedProvider.id
          : usedProviders.length === 1
            ? usedProviders[0]
            : "mixed",
      results: mergedResults,
      failed: finalFailures,
      render: renderMetadata,
    },
    providersUsed: usedProviders,
    outcomes,
  };
}
