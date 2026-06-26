#!/usr/bin/env node

import { fail, parseCommaList, readOptionValue } from "./lib/cli-utils.mjs";
import {
  buildCacheTelemetry,
  buildMapCacheKey,
  readCacheRecord,
  writeCacheEntry,
} from "./lib/cache.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import { loadHealthState } from "./lib/health-state.mjs";
import { mapSite } from "./lib/map-runner.mjs";
import { buildMapOutput, finalizeCommandOutput, formatMapMarkdown } from "./lib/output.mjs";
import { planMapRoute } from "./lib/planner.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro map — Discover site structure without extracting full content

Usage:
  map.mjs "url1" ["url2" ...] [options]

Options:
  --depth <n>            Discovery depth from the entry URL (default: 1)
  --max-pages <n>        Maximum successfully visited pages (default: 50)
  --same-origin          Restrict discovery to the entry origin (default: true)
  --no-same-origin       Allow cross-origin discovery
  --include-path <p,...> Only queue paths with these prefixes
  --exclude-path <p,...> Exclude paths with these prefixes
  --json                 Output stable JSON schema`);
  process.exit(exitCode);
}

const args = process.argv.slice(2);
if (args.length === 0) {
  usage();
}

const cli = {
  depth: null,
  maxPages: null,
  sameOrigin: true,
  includePathPrefixes: [],
  excludePathPrefixes: [],
  json: false,
};
const urls = [];

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "-h" || arg === "--help") {
    usage(0);
  }
  if (arg === "--depth") {
    cli.depth = Number.parseInt(readOptionValue(args, i, "--depth"), 10);
    i++;
    continue;
  }
  if (arg === "--max-pages") {
    cli.maxPages = Number.parseInt(readOptionValue(args, i, "--max-pages"), 10);
    i++;
    continue;
  }
  if (arg === "--same-origin") {
    cli.sameOrigin = true;
    continue;
  }
  if (arg === "--no-same-origin") {
    cli.sameOrigin = false;
    continue;
  }
  if (arg === "--include-path") {
    cli.includePathPrefixes = parseCommaList(readOptionValue(args, i, "--include-path"), "--include-path");
    i++;
    continue;
  }
  if (arg === "--exclude-path") {
    cli.excludePathPrefixes = parseCommaList(readOptionValue(args, i, "--exclude-path"), "--exclude-path");
    i++;
    continue;
  }
  if (arg === "--json") {
    cli.json = true;
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
if (cli.depth !== null && (!Number.isInteger(cli.depth) || cli.depth < 0)) {
  fail("--depth must be an integer >= 0");
}
if (cli.maxPages !== null && (!Number.isInteger(cli.maxPages) || cli.maxPages < 1)) {
  fail("--max-pages must be an integer >= 1");
}

const cwd = process.cwd();
const env = process.env;
const { config } = loadRuntimeConfig({
  cwd,
  env,
  overrides: {
    crawl: {
      ...(cli.depth !== null ? { defaultDepth: cli.depth } : {}),
      ...(cli.maxPages !== null ? { defaultMaxPages: cli.maxPages } : {}),
    },
  },
});
const healthState = await loadHealthState({ cwd, config });
const plan = planMapRoute(
  { urls },
  {
    env,
    config,
    healthState,
    now: Date.now(),
  },
);

if (!plan.selected) {
  console.error(`Error: ${plan.error?.message ?? "No map route selected"}`);
  process.exit(1);
}

const cacheKey = buildMapCacheKey({
  entryUrls: urls,
  depth: config.crawl.defaultDepth,
  maxPages: config.crawl.defaultMaxPages,
  sameOrigin: cli.sameOrigin,
  includePathPrefixes: cli.includePathPrefixes,
  excludePathPrefixes: cli.excludePathPrefixes,
});
const cacheRecord = await readCacheRecord("map", cacheKey, { cwd, config });

if (cacheRecord) {
  const payload = finalizeCommandOutput(cacheRecord.value, {
    plan,
    cache: buildCacheTelemetry("map", {
      config,
      record: cacheRecord,
    }),
  });
  if (cli.json) {
    console.log(JSON.stringify(payload, null, 2));
  } else {
    console.log(formatMapMarkdown(payload));
  }
  process.exit(payload.nodes.length > 0 ? 0 : 1);
}

const result = await mapSite(urls, {
  depth: config.crawl.defaultDepth,
  maxPages: config.crawl.defaultMaxPages,
  sameOrigin: cli.sameOrigin,
  includePathPrefixes: cli.includePathPrefixes,
  excludePathPrefixes: cli.excludePathPrefixes,
  timeoutMs: config.fetch.timeoutMs,
  maxRedirects: config.fetch.maxRedirects,
  respectRobotsTxt: config.crawl.respectRobotsTxt,
});

const cacheWriteNow = Date.now();
const payload = buildMapOutput({
  result,
  plan,
  cache: buildCacheTelemetry("map", {
    config,
    now: cacheWriteNow,
    ttlSeconds: config.cache.crawlTtlSeconds,
  }),
});
await writeCacheEntry("map", cacheKey, payload, {
  cwd,
  config,
  ttlSeconds: config.cache.crawlTtlSeconds,
  now: cacheWriteNow,
});

if (cli.json) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatMapMarkdown(payload));
}

process.exit(payload.nodes.length > 0 ? 0 : 1);
