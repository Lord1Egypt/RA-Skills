#!/usr/bin/env node

import { fail, parseCommaList, readOptionValue } from "./lib/cli-utils.mjs";
import { loadRuntimeConfig } from "./lib/config.mjs";
import { runResearch } from "./lib/research/orchestrator.mjs";
import { formatResearchMarkdown } from "./lib/research/output.mjs";
import { normalizeResearchRequest } from "./lib/research/request.mjs";

const VALID_FORMATS = new Set(["pack", "brief", "comparison", "timeline", "dossier"]);

function usage(exitCode = 2) {
  console.error(`web-search-pro research — Structured plan + evidence pack for models

Usage:
  research.mjs "topic" [options]

Options:
  --objective <text>         Research objective override
  --format <name>            Output format: pack|brief|comparison|timeline|dossier
  --include-domains <d,...>  Restrict research search tasks to these domains
  --exclude-domains <d,...>  Exclude these domains from search tasks
  --seed-url <url>           Seed an official page for extract/map/crawl planning
  --max-questions <n>        Maximum number of subquestions (default: 4)
  --max-searches <n>         Maximum number of search tasks (default: 8)
  --max-extracts <n>         Maximum number of extract tasks (default: 6)
  --max-crawl-pages <n>      Maximum crawl pages for research tasks (default: 12)
  --no-crawl                 Disable crawl tasks even when the planner would use them
  --no-federation            Disable federated search inside research
  --lang <code>              Output language hint: match-input|en|zh|de|fr|ja
  --json                     Output stable JSON schema
  --plan                     Output the research plan only (no retrieval execution)`);
  process.exit(exitCode);
}

const args = process.argv.slice(2);
if (args.length === 0) {
  usage();
}

const cli = {
  objective: null,
  format: "pack",
  includeDomains: [],
  excludeDomains: [],
  seedUrls: [],
  maxQuestions: null,
  maxSearches: null,
  maxExtracts: null,
  maxCrawlPages: null,
  allowCrawl: true,
  allowFederation: true,
  language: "match-input",
  json: false,
  plan: false,
};
const positionals = [];

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "-h" || arg === "--help") {
    usage(0);
  }
  if (arg === "--objective") {
    cli.objective = readOptionValue(args, i, "--objective");
    i++;
    continue;
  }
  if (arg === "--format") {
    cli.format = readOptionValue(args, i, "--format");
    i++;
    continue;
  }
  if (arg === "--include-domains") {
    cli.includeDomains = parseCommaList(readOptionValue(args, i, "--include-domains"), "--include-domains");
    i++;
    continue;
  }
  if (arg === "--exclude-domains") {
    cli.excludeDomains = parseCommaList(readOptionValue(args, i, "--exclude-domains"), "--exclude-domains");
    i++;
    continue;
  }
  if (arg === "--seed-url") {
    cli.seedUrls.push(readOptionValue(args, i, "--seed-url"));
    i++;
    continue;
  }
  if (arg === "--max-questions") {
    cli.maxQuestions = Number.parseInt(readOptionValue(args, i, "--max-questions"), 10);
    i++;
    continue;
  }
  if (arg === "--max-searches") {
    cli.maxSearches = Number.parseInt(readOptionValue(args, i, "--max-searches"), 10);
    i++;
    continue;
  }
  if (arg === "--max-extracts") {
    cli.maxExtracts = Number.parseInt(readOptionValue(args, i, "--max-extracts"), 10);
    i++;
    continue;
  }
  if (arg === "--max-crawl-pages") {
    cli.maxCrawlPages = Number.parseInt(readOptionValue(args, i, "--max-crawl-pages"), 10);
    i++;
    continue;
  }
  if (arg === "--no-crawl") {
    cli.allowCrawl = false;
    continue;
  }
  if (arg === "--no-federation") {
    cli.allowFederation = false;
    continue;
  }
  if (arg === "--lang") {
    cli.language = readOptionValue(args, i, "--lang");
    i++;
    continue;
  }
  if (arg === "--json") {
    cli.json = true;
    continue;
  }
  if (arg === "--plan") {
    cli.plan = true;
    continue;
  }
  if (arg.startsWith("-")) {
    fail(`Unknown option: ${arg}`);
  }
  positionals.push(arg);
}

const topic = positionals.join(" ").trim();
if (!topic) {
  usage();
}
if (!VALID_FORMATS.has(cli.format)) {
  fail(`--format must be one of: ${Array.from(VALID_FORMATS).join(", ")}`);
}

const request = normalizeResearchRequest({
  topic,
  objective: cli.objective,
  scope: {
    includeDomains: cli.includeDomains,
    excludeDomains: cli.excludeDomains,
    seedUrls: cli.seedUrls,
  },
  budgets: {
    ...(cli.maxQuestions !== null ? { maxQuestions: cli.maxQuestions } : {}),
    ...(cli.maxSearches !== null ? { maxSearches: cli.maxSearches } : {}),
    ...(cli.maxExtracts !== null ? { maxExtracts: cli.maxExtracts } : {}),
    ...(cli.maxCrawlPages !== null ? { maxCrawlPages: cli.maxCrawlPages } : {}),
    allowFederation: cli.allowFederation,
    allowCrawl: cli.allowCrawl,
    allowRender: false,
  },
  output: {
    format: cli.format,
    language: cli.language,
  },
});

const cwd = process.cwd();
const env = process.env;
const configOverrides = {
  ...(request.budgets.allowFederation ? {} : { routing: { enableFederation: false } }),
  ...(request.budgets.allowRender ? {} : { render: { enabled: false, policy: "off" } }),
};
const { config } = loadRuntimeConfig({
  cwd,
  env,
  overrides: configOverrides,
});

const payload = await runResearch(request, {
  cwd,
  env,
  config,
  planOnly: cli.plan,
});

if (cli.json) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatResearchMarkdown(payload));
}
