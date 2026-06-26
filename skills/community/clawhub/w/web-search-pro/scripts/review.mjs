#!/usr/bin/env node

import { loadRuntimeConfig } from "./lib/config.mjs";
import { buildDoctorReport } from "./lib/doctor.mjs";
import { buildReviewOutput } from "./lib/output.mjs";
import { buildCapabilitySnapshot } from "./lib/providers.mjs";

function usage(exitCode = 2) {
  console.error(`web-search-pro review

Usage:
  review.mjs [--json]`);
  process.exit(exitCode);
}

function formatReviewMarkdown(report) {
  const lines = [];

  lines.push("# web-search-pro review");
  lines.push("");
  lines.push("## Optional Env Disclosure");
  lines.push("");
  for (const envVar of report.optionalEnvDisclosure) {
    lines.push(`- ${envVar.name}: ${envVar.description}`);
  }

  lines.push("");
  lines.push("## No-Key Baseline");
  lines.push("");
  lines.push(`- Enabled: ${report.noKeyBaseline.enabled ? "yes" : "no"}`);
  lines.push(`- Status: ${report.noKeyBaseline.status}`);
  lines.push(`- Search provider: ${report.noKeyBaseline.searchProvider}`);
  lines.push(`- Extract/crawl provider: ${report.noKeyBaseline.extractProvider}`);

  lines.push("");
  lines.push("## Federated Retrieval");
  lines.push("");
  lines.push(`- Enabled: ${report.federation.enabled ? "yes" : "no"}`);
  lines.push(`- Triggers: ${report.federation.triggers.join(", ")}`);
  lines.push(`- Merge policy: ${report.federation.mergePolicy}`);

  if (report.degradedProviders.length > 0 || report.cooldownProviders.length > 0) {
    lines.push("");
    lines.push("## Runtime Degradation");
    lines.push("");
    lines.push(
      `- Degraded providers: ${report.degradedProviders.length > 0 ? report.degradedProviders.join(", ") : "none"}`,
    );
    lines.push(
      `- Cooldown providers: ${report.cooldownProviders.length > 0 ? report.cooldownProviders.join(", ") : "none"}`,
    );
  }

  lines.push("");
  lines.push("");
  lines.push("## Blocked URL Classes");
  lines.push("");
  for (const value of report.blockedUrlClasses) {
    lines.push(`- ${value}`);
  }

  lines.push("");
  lines.push("## Current Providers");
  lines.push("");
  for (const provider of report.providerMatrix) {
    lines.push(
      `- ${provider.id}: configured=${provider.configured ? "yes" : "no"}, env=${
        provider.env.map((entry) => entry.name).join(", ") || "none"
      }`,
    );
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
const runtime = loadRuntimeConfig({ cwd, env });
const capabilitySnapshot = buildCapabilitySnapshot({ env, config: runtime.config });
const doctor = await buildDoctorReport({
  cwd,
  env,
  config: runtime.config,
  configMeta: runtime.meta,
  now: Date.now(),
});
const optionalEnvDisclosure = Array.from(
  new Map(
    capabilitySnapshot.providers
      .flatMap((provider) => provider.env)
      .map((entry) => [entry.name, entry]),
  ).values(),
);

const payload = buildReviewOutput({
  optionalEnvDisclosure,
  noKeyBaseline: {
    enabled: runtime.config.routing.allowNoKeyBaseline,
    status: doctor.baselineStatus,
    searchProvider: runtime.config.routing.allowNoKeyBaseline ? "ddg" : "disabled",
    extractProvider: runtime.config.routing.allowNoKeyBaseline ? "fetch" : "disabled",
  },
  federation: doctor.federation,
  degradedProviders: doctor.degradedProviders,
  cooldownProviders: doctor.cooldownProviders,
  healthyProviders: doctor.healthyProviders,
  blockedUrlClasses: doctor.safeFetch.blockedUrlClasses,
  providerMatrix: capabilitySnapshot.providers,
  config: runtime.config,
  configPath: runtime.meta.path,
});

if (args.includes("--json")) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  console.log(formatReviewMarkdown(payload));
}
