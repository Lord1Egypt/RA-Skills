#!/usr/bin/env node

import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildCapabilitiesOutput } from "./lib/output.mjs";
import { buildCapabilitySnapshot } from "./lib/providers.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro capabilities

Usage:
  capabilities.mjs [--json]`);
  process.exit(exitCode);
}

function formatCapabilitiesMarkdown(snapshot) {
  const lines = [];

  lines.push("# web-search-pro capabilities");
  lines.push("");
  lines.push(
    `- Configured providers: ${
      snapshot.configuredProviders.length > 0 ? snapshot.configuredProviders.join(", ") : "none"
    }`,
  );
  lines.push("- Providers:");

  for (const provider of snapshot.providers) {
    const envNames = provider.env.map((entry) => entry.name).join(", ") || "none";
    lines.push(
      `  - ${provider.id}: configured=${provider.configured ? "yes" : "no"}, search=${
        provider.capabilities.search ? "yes" : "no"
      }, deep=${provider.capabilities.deepSearch ? "yes" : "no"}, news=${
        provider.capabilities.newsSearch ? "yes" : "no"
      }, extract=${provider.capabilities.extract ? "yes" : "no"}, crawl=${
        provider.capabilities.crawl ? "yes" : "no"
      }, map=${provider.capabilities.map ? "yes" : "no"}`,
    );
    lines.push(
      `    domainFilter=${provider.capabilities.domainFilterMode}, locale=${
        provider.capabilities.localeFiltering ? "yes" : "no"
      }, env=${envNames}`,
    );
  }

  if (snapshot.availableFeatures.subEngines.length > 0) {
    lines.push("");
    lines.push(`- Available sub-engines: ${snapshot.availableFeatures.subEngines.join(", ")}`);
  }

  return lines.join("\n");
}

const args = process.argv.slice(2);
if (args.some((arg) => arg === "-h" || arg === "--help")) {
  usage(0);
}
if (args.some((arg) => arg !== "--json")) {
  usage();
}

const cwd = process.cwd();
const env = process.env;
const { config } = loadRuntimeConfig({ cwd, env });
const snapshot = buildCapabilitySnapshot({ env, config });
const payload = buildCapabilitiesOutput(snapshot);

if (args.includes("--json")) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatCapabilitiesMarkdown(payload));
}
