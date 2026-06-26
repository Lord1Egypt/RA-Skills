#!/usr/bin/env node

import { fail, readOptionValue } from "./lib/cli-utils.mjs";
import {
  buildCacheTelemetry,
  buildExtractCacheKey,
  readCacheRecord,
  writeCacheEntry,
} from "./lib/cache.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import {
  loadHealthState,
  recordProviderFailure,
  recordProviderOutcomes,
} from "./lib/health-state.mjs";
import {
  buildExtractOutput,
  buildPlanOutput,
  finalizeCommandOutput,
  formatExtractMarkdown,
} from "./lib/output.mjs";
import { executeExtractFlow } from "./lib/extract-flow.mjs";
import {
  formatPlanMarkdown,
  planExtractRoute,
  requireSelectedRoute,
  serializePlan,
} from "./lib/planner.mjs";

const EXTRACT_ENGINES = new Set(["tavily", "exa", "fetch"]);

function usage(exitCode = 2) {
  console.error(`web-search-pro extract — Extract readable content from URLs

Usage:
  extract.mjs "url1" ["url2" ...] [options]

Options:
  --engine <name>              Force engine: tavily|exa|fetch (default: auto)
  --max-chars <n>              Limit extracted readable text per URL
  --json                       Output stable JSON schema
  --plan                       Show route plan only (no provider API call)
  --explain-routing            Include route explanation in output

Environment variables:
  WEB_SEARCH_PRO_CONFIG  Optional path to config.json
  TAVILY_API_KEY         Tavily Extract API
  EXA_API_KEY            Exa contents API with livecrawl`);
  process.exit(exitCode);
}

const args = process.argv.slice(2);
if (args.length === 0) {
  usage();
}

const opts = {
  engine: null,
  maxChars: null,
  json: false,
  plan: false,
  explainRouting: false,
};
const urls = [];

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "-h" || arg === "--help") {
    usage(0);
  }
  if (arg === "--engine") {
    opts.engine = readOptionValue(args, i, "--engine");
    i++;
    continue;
  }
  if (arg === "--max-chars") {
    opts.maxChars = Number.parseInt(readOptionValue(args, i, "--max-chars"), 10);
    i++;
    continue;
  }
  if (arg === "--render-policy") {
    opts.renderPolicy = readOptionValue(args, i, "--render-policy");
    i++;
    continue;
  }
  if (arg === "--render-budget-ms") {
    opts.renderBudgetMs = Number.parseInt(readOptionValue(args, i, "--render-budget-ms"), 10);
    i++;
    continue;
  }
  if (arg === "--render-wait-until") {
    opts.renderWaitUntil = readOptionValue(args, i, "--render-wait-until");
    i++;
    continue;
  }
  if (arg === "--json") {
    opts.json = true;
    continue;
  }
  if (arg === "--plan") {
    opts.plan = true;
    continue;
  }
  if (arg === "--explain-routing") {
    opts.explainRouting = true;
    continue;
  }
  if (!arg.startsWith("-")) {
    urls.push(arg);
    continue;
  }
  fail(`Unknown option: ${arg}`);
}

if (urls.length === 0) {
  fail("No URLs provided");
}
if (opts.engine && !EXTRACT_ENGINES.has(opts.engine)) {
  fail(`Unknown extract engine: ${opts.engine}. Available: tavily, exa, fetch`);
}
if (opts.maxChars !== null && (!Number.isInteger(opts.maxChars) || opts.maxChars < 100)) {
  fail("--max-chars must be an integer >= 100");
}
const cwd = process.cwd();
const env = process.env;
const renderOverrides = {};
const { config } = loadRuntimeConfig({
  cwd,
  env,
  overrides: {
    ...(opts.maxChars !== null
      ? {
          fetch: {
            maxChars: opts.maxChars,
          },
        }
      : {}),
    ...renderOverrides,
  },
});
const healthState = await loadHealthState({ cwd, config });
const plan = planExtractRoute(
  {
    engine: opts.engine,
    urls,
    maxChars: config.fetch.maxChars,
  },
  {
    env,
    config,
    healthState,
    now: Date.now(),
  },
);

if (opts.plan) {
  if (opts.json) {
    console.log(
      JSON.stringify(
        buildPlanOutput({
          command: "extract",
          plan,
          meta: {
            count: 0,
          },
        }),
        null,
        2,
      ),
    );
  } else {
    console.log(formatPlanMarkdown(plan));
  }
  process.exit(plan.selected ? 0 : 1);
}

try {
  requireSelectedRoute(plan);
  const cacheKey = buildExtractCacheKey({
    command: "extract",
    providerId: plan.selected.provider.id,
    urls,
    maxChars: config.fetch.maxChars,
    render:
      config.render.enabled && config.render.policy !== "off"
        ? {
            policy: config.render.policy,
            budgetMs: config.render.budgetMs,
            waitUntil: config.render.waitUntil,
            blockTypes: config.render.blockTypes,
            sameOriginOnly: config.render.sameOriginOnly,
          }
        : null,
  });
  const cacheRecord = await readCacheRecord("extract", cacheKey, { cwd, config });

  if (cacheRecord) {
    const payload = finalizeCommandOutput(cacheRecord.value, {
      plan,
      includeRouting: opts.explainRouting,
      cache: buildCacheTelemetry("extract", {
        config,
        record: cacheRecord,
      }),
    });
    if (opts.json) {
      console.log(JSON.stringify(payload, null, 2));
    } else {
      console.log(formatExtractMarkdown(payload));
    }
    process.exit(0);
  }

  const execution = await executeExtractFlow({
    urls,
    plan,
    config,
  });
  await recordProviderOutcomes(execution.outcomes, {
    cwd,
    config,
    now: Date.now(),
  });

  const cacheWriteNow = Date.now();
  const cachedPayload = buildExtractOutput({
    providerResult: execution.providerResult,
    plan,
    includeRouting: false,
    render: execution.providerResult.render ?? null,
    cache: buildCacheTelemetry("extract", {
      config,
      now: cacheWriteNow,
      ttlSeconds: config.cache.extractTtlSeconds,
    }),
  });
  await writeCacheEntry("extract", cacheKey, cachedPayload, {
    cwd,
    config,
    ttlSeconds: config.cache.extractTtlSeconds,
    now: cacheWriteNow,
  });
  const payload = finalizeCommandOutput(cachedPayload, {
    plan,
    includeRouting: opts.explainRouting,
    cache: buildCacheTelemetry("extract", {
      config,
      now: cacheWriteNow,
      ttlSeconds: config.cache.extractTtlSeconds,
    }),
  });

  if (opts.json) {
    console.log(JSON.stringify(payload, null, 2));
  } else {
    console.log(formatExtractMarkdown(payload));
  }
} catch (error) {
  const outcomes = error.providerOutcomes ?? [];
  if (outcomes.length > 0) {
    await recordProviderOutcomes(outcomes, {
      cwd,
      config,
      now: Date.now(),
    });
  } else if (plan.selected) {
    await recordProviderFailure(plan.selected.provider.id, error, {
      cwd,
      config,
      now: Date.now(),
    });
  }
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
