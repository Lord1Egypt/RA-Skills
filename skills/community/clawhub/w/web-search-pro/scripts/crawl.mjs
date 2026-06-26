#!/usr/bin/env node

import { fail, parseCommaList, readOptionValue } from "./lib/cli-utils.mjs";
import {
  buildCacheTelemetry,
  buildCrawlCacheKey,
  readCacheRecord,
  writeCacheEntry,
} from "./lib/cache.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import { crawlSite } from "./lib/crawl-runner.mjs";
import { buildCrawlOutput, finalizeCommandOutput, formatCrawlMarkdown } from "./lib/output.mjs";
import { loadHealthState } from "./lib/health-state.mjs";
import { planCrawlRoute } from "./lib/planner.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro crawl — Safe multi-page crawl for static sites

Usage:
  crawl.mjs "url1" ["url2" ...] [options]

Options:
  --depth <n>            Crawl depth from the entry URL (default: 1)
  --max-pages <n>        Maximum successfully visited pages (default: 10)
  --same-origin          Restrict discovery to the entry origin (default: true)
  --no-same-origin       Allow cross-origin discovery
  --include-path <p,...> Only queue paths with these prefixes
  --exclude-path <p,...> Exclude paths with these prefixes
  --max-chars <n>        Limit extracted readable text per page (default: 12000)
  --json                 Output stable JSON schema

Notes:
  - Only http/https URLs are allowed
  - Localhost, link-local, and private-network targets are rejected
  - JS execution is disabled; this command targets static HTML/text pages`);
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
  maxChars: null,
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
  if (arg === "--max-chars") {
    cli.maxChars = Number.parseInt(readOptionValue(args, i, "--max-chars"), 10);
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
if (cli.maxChars !== null && (!Number.isInteger(cli.maxChars) || cli.maxChars < 100)) {
  fail("--max-chars must be an integer >= 100");
}

const cwd = process.cwd();
const env = process.env;
const { config } = loadRuntimeConfig({
  cwd,
  env,
  overrides: {
    fetch: cli.maxChars !== null ? { maxChars: cli.maxChars } : {},
    crawl: {
      ...(cli.depth !== null ? { defaultDepth: cli.depth } : {}),
      ...(cli.maxPages !== null ? { defaultMaxPages: cli.maxPages } : {}),
    },
  },
});
const healthState = await loadHealthState({ cwd, config });
const plan = planCrawlRoute(
  {
    urls,
  },
  {
    env,
    config,
    healthState,
    now: Date.now(),
  },
);

if (!plan.selected) {
  console.error(`Error: ${plan.error?.message ?? "No crawl route selected"}`);
  process.exit(1);
}

const cacheKey = buildCrawlCacheKey({
  entryUrls: urls,
  depth: config.crawl.defaultDepth,
  maxPages: config.crawl.defaultMaxPages,
  sameOrigin: cli.sameOrigin,
  includePathPrefixes: cli.includePathPrefixes,
  excludePathPrefixes: cli.excludePathPrefixes,
});
const cacheRecord = await readCacheRecord("crawl", cacheKey, { cwd, config });

if (cacheRecord) {
  const payload = finalizeCommandOutput(cacheRecord.value, {
    plan,
    cache: buildCacheTelemetry("crawl", {
      config,
      record: cacheRecord,
    }),
  });
  if (cli.json) {
    console.log(JSON.stringify(payload, null, 2));
  } else {
    console.log(formatCrawlMarkdown(payload));
  }
  process.exit(payload.results.length > 0 ? 0 : 1);
}

const result = await crawlSite(urls, {
  depth: config.crawl.defaultDepth,
  maxPages: config.crawl.defaultMaxPages,
  sameOrigin: cli.sameOrigin,
  includePathPrefixes: cli.includePathPrefixes,
  excludePathPrefixes: cli.excludePathPrefixes,
  maxChars: config.fetch.maxChars,
  timeoutMs: config.fetch.timeoutMs,
  maxRedirects: config.fetch.maxRedirects,
  respectRobotsTxt: config.crawl.respectRobotsTxt,
});

const cacheWriteNow = Date.now();
const payload = buildCrawlOutput({
  result,
  plan,
  cache: buildCacheTelemetry("crawl", {
    config,
    now: cacheWriteNow,
    ttlSeconds: config.cache.crawlTtlSeconds,
  }),
});
await writeCacheEntry("crawl", cacheKey, payload, {
  cwd,
  config,
  ttlSeconds: config.cache.crawlTtlSeconds,
  now: cacheWriteNow,
});

if (cli.json) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatCrawlMarkdown(payload));
}

process.exit(payload.results.length > 0 ? 0 : 1);
