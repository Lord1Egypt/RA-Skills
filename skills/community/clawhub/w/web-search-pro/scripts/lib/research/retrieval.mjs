import {
  buildCrawlCacheKey,
  buildExtractCacheKey,
  buildMapCacheKey,
  buildSearchCacheKey,
  readCacheEntry,
  writeCacheEntry,
} from "../cache.mjs";
import { crawlSite } from "../crawl-runner.mjs";
import { executeFederatedSearch } from "../federated-search.mjs";
import { executeExtractFlow, extractProvidersUsed } from "../extract-flow.mjs";
import {
  loadHealthState,
  recordProviderFailure,
  recordProviderOutcomes,
} from "../health-state.mjs";
import { mapSite } from "../map-runner.mjs";
import {
  buildCrawlOutput,
  buildExtractOutput,
  buildMapOutput,
  buildSearchOutput,
} from "../output.mjs";
import {
  planCrawlRoute,
  planExtractRoute,
  planMapRoute,
  planSearchRoute,
  requireSelectedRoute,
} from "../planner.mjs";

async function executeSearchTask(task, context) {
  const healthState = await loadHealthState(context);
  const plan = planSearchRoute(
    {
      ...task.options,
      query: task.query,
      mode: "research",
    },
    {
      env: context.env,
      config: context.config,
      healthState,
      now: context.now(),
    },
  );
  const selected = requireSelectedRoute(plan);
  const cacheKey = buildSearchCacheKey({
    providerId: selected.provider.id,
    request: {
      ...plan.request,
      query: task.query,
    },
    federation: plan.federation,
  });
  const cached = await readCacheEntry("search", cacheKey, context);
  if (cached) {
    return {
      task: { ...task, status: "completed" },
      result: cached,
      providersUsed: cached.federated?.providersUsed ?? [cached.selectedProvider].filter(Boolean),
      federated: Boolean(cached.federated?.triggered),
      cached: true,
    };
  }

  try {
    const execution = await executeFederatedSearch({
      query: task.query,
      request: {
        ...plan.request,
        query: task.query,
      },
      plan,
      config: context.config,
    });
    await recordProviderOutcomes(execution.providerOutcomes ?? [], {
      cwd: context.cwd,
      config: context.config,
      now: context.now(),
    });

    const payload = buildSearchOutput({
      query: task.query,
      providerResult: execution.result,
      plan,
      federation: execution.federation,
    });
    await writeCacheEntry("search", cacheKey, payload, {
      cwd: context.cwd,
      config: context.config,
      ttlSeconds: context.config.cache.searchTtlSeconds,
      now: context.now(),
    });
    return {
      task: { ...task, status: "completed" },
      result: payload,
      providersUsed: execution.federation?.providersUsed ?? [payload.selectedProvider].filter(Boolean),
      federated: Boolean(execution.federation?.triggered),
      cached: false,
    };
  } catch (error) {
    if (error.providerOutcomes?.length) {
      await recordProviderOutcomes(error.providerOutcomes, {
        cwd: context.cwd,
        config: context.config,
        now: context.now(),
      });
    } else if (plan.selected) {
      await recordProviderFailure(plan.selected.provider.id, error, {
        cwd: context.cwd,
        config: context.config,
        now: context.now(),
      });
    }
    return {
      task: { ...task, status: "failed" },
      providersUsed: [],
      federated: false,
      error: error.message,
      result: {
        schemaVersion: "1.0",
        command: "search",
        selectedProvider: plan.selected?.provider.id ?? null,
        engine: plan.selected?.provider.id ?? null,
        results: [],
        failed: [{ providerId: plan.selected?.provider.id ?? null, error: error.message }],
        meta: {
          query: task.query,
          count: 0,
          answer: null,
        },
      },
    };
  }
}

async function executeExtractTask(task, context) {
  const healthState = await loadHealthState(context);
  const plan = planExtractRoute(
    {
      engine: null,
      urls: task.urls,
      maxChars: task.options.maxChars,
    },
    {
      env: context.env,
      config: context.config,
      healthState,
      now: context.now(),
    },
  );
  requireSelectedRoute(plan);
  const cacheKey = buildExtractCacheKey({
    command: "extract",
    providerId: plan.selected.provider.id,
    urls: task.urls,
    maxChars: task.options.maxChars,
    render:
      context.config.render.enabled && context.config.render.policy !== "off"
        ? context.config.render
        : null,
  });
  const cached = await readCacheEntry("extract", cacheKey, context);
  if (cached) {
    return {
      task: { ...task, status: "completed" },
      result: cached,
      providersUsed: [cached.selectedProvider].filter(Boolean),
      federated: false,
      cached: true,
    };
  }

  try {
    const execution = await executeExtractFlow({
      urls: task.urls,
      plan,
      config: context.config,
    });
    await recordProviderOutcomes(execution.outcomes ?? [], {
      cwd: context.cwd,
      config: context.config,
      now: context.now(),
    });
    const payload = buildExtractOutput({
      providerResult: execution.providerResult,
      plan,
      render: execution.providerResult.render ?? null,
    });
    await writeCacheEntry("extract", cacheKey, payload, {
      cwd: context.cwd,
      config: context.config,
      ttlSeconds: context.config.cache.extractTtlSeconds,
      now: context.now(),
    });
    return {
      task: { ...task, status: "completed" },
      result: payload,
      providersUsed: extractProvidersUsed(execution),
      federated: false,
      cached: false,
    };
  } catch (error) {
    if (error.providerOutcomes?.length) {
      await recordProviderOutcomes(error.providerOutcomes, {
        cwd: context.cwd,
        config: context.config,
        now: context.now(),
      });
    } else if (plan.selected) {
      await recordProviderFailure(plan.selected.provider.id, error, {
        cwd: context.cwd,
        config: context.config,
        now: context.now(),
      });
    }
    return {
      task: { ...task, status: "failed" },
      providersUsed: [],
      federated: false,
      error: error.message,
      result: {
        schemaVersion: "1.0",
        command: "extract",
        selectedProvider: plan.selected?.provider.id ?? null,
        engine: plan.selected?.provider.id ?? null,
        results: [],
        failed: task.urls.map((url) => ({ url, error: error.message })),
        render: null,
        meta: { count: 0 },
      },
    };
  }
}

async function executeCrawlTask(task, context) {
  const healthState = await loadHealthState(context);
  const plan = planCrawlRoute(
    { urls: task.urls },
    {
      env: context.env,
      config: context.config,
      healthState,
      now: context.now(),
    },
  );
  requireSelectedRoute(plan);
  const cacheKey = buildCrawlCacheKey({
    entryUrls: task.urls,
    depth: task.options.depth,
    maxPages: task.options.maxPages,
    sameOrigin: task.options.sameOrigin,
    includePathPrefixes: [],
    excludePathPrefixes: [],
  });
  const cached = await readCacheEntry("crawl", cacheKey, context);
  if (cached) {
    return {
      task: { ...task, status: "completed" },
      result: cached,
      providersUsed: [cached.selectedProvider].filter(Boolean),
      federated: false,
      cached: true,
    };
  }

  const result = await crawlSite(task.urls, {
    depth: task.options.depth,
    maxPages: task.options.maxPages,
    sameOrigin: task.options.sameOrigin,
    maxChars: context.config.fetch.maxChars,
    timeoutMs: context.config.fetch.timeoutMs,
    maxRedirects: context.config.fetch.maxRedirects,
    respectRobotsTxt: context.config.crawl.respectRobotsTxt,
  });
  const payload = buildCrawlOutput({ result, plan });
  await writeCacheEntry("crawl", cacheKey, payload, {
    cwd: context.cwd,
    config: context.config,
    ttlSeconds: context.config.cache.crawlTtlSeconds,
    now: context.now(),
  });
  return {
    task: { ...task, status: "completed" },
    result: payload,
    providersUsed: [payload.selectedProvider].filter(Boolean),
    federated: false,
    cached: false,
  };
}

async function executeMapTask(task, context) {
  const healthState = await loadHealthState(context);
  const plan = planMapRoute(
    { urls: task.urls },
    {
      env: context.env,
      config: context.config,
      healthState,
      now: context.now(),
    },
  );
  requireSelectedRoute(plan);
  const cacheKey = buildMapCacheKey({
    entryUrls: task.urls,
    depth: task.options.depth,
    maxPages: task.options.maxPages,
    sameOrigin: task.options.sameOrigin,
    includePathPrefixes: [],
    excludePathPrefixes: [],
  });
  const cached = await readCacheEntry("map", cacheKey, context);
  if (cached) {
    return {
      task: { ...task, status: "completed" },
      result: cached,
      providersUsed: [cached.selectedProvider].filter(Boolean),
      federated: false,
      cached: true,
    };
  }

  const result = await mapSite(task.urls, {
    depth: task.options.depth,
    maxPages: task.options.maxPages,
    sameOrigin: task.options.sameOrigin,
    timeoutMs: context.config.fetch.timeoutMs,
    maxRedirects: context.config.fetch.maxRedirects,
    respectRobotsTxt: context.config.crawl.respectRobotsTxt,
  });
  const payload = buildMapOutput({ result, plan });
  await writeCacheEntry("map", cacheKey, payload, {
    cwd: context.cwd,
    config: context.config,
    ttlSeconds: context.config.cache.crawlTtlSeconds,
    now: context.now(),
  });
  return {
    task: { ...task, status: "completed" },
    result: payload,
    providersUsed: [payload.selectedProvider].filter(Boolean),
    federated: false,
    cached: false,
  };
}

export async function executeResearchTask(task, context) {
  if (task.kind === "search") {
    return executeSearchTask(task, context);
  }
  if (task.kind === "extract") {
    return executeExtractTask(task, context);
  }
  if (task.kind === "crawl") {
    return executeCrawlTask(task, context);
  }
  if (task.kind === "map") {
    return executeMapTask(task, context);
  }
  throw new Error(`Unsupported research task kind: ${task.kind}`);
}
