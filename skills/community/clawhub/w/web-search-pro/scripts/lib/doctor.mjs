import { getCacheStats } from "./cache.mjs";
import { DEFAULT_CONFIG } from "./config.mjs";
import { buildHealthSnapshot } from "./health-state.mjs";
import { buildCapabilitySnapshot } from "./providers.mjs";

function buildWarnings({
  availableFeatures,
  credentialedProviders,
  degradedProviders,
  cooldownProviders,
  baselineStatus,
}) {
  const warnings = [];

  if (credentialedProviders.length === 0) {
    warnings.push("No provider credentials detected. Running on the no-key baseline only.");
  }
  if (!availableFeatures.deepSearch) {
    warnings.push("Deep search is unavailable without TAVILY_API_KEY or EXA_API_KEY.");
  }
  if (!availableFeatures.newsSearch) {
    warnings.push(
      "News search is unavailable without SERPER_API_KEY, TAVILY_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, or SEARXNG_INSTANCE_URL.",
    );
  }
  if (!availableFeatures.localeFiltering) {
    warnings.push(
      "Locale-aware search is unavailable without SERPER_API_KEY, SERPAPI_API_KEY, YOU_API_KEY, BRAVE_API_KEY, or QUERIT_API_KEY.",
    );
  }
  if (!availableFeatures.map) {
    warnings.push("Site map discovery is unavailable under the current routing policy.");
  }
  if (baselineStatus === "degraded") {
    warnings.push("The no-key baseline is currently degraded. Search or extract fallback behavior may be limited.");
  }
  if (cooldownProviders.length > 0) {
    warnings.push(`Providers in cooldown: ${cooldownProviders.join(", ")}.`);
  }
  if (degradedProviders.length > 0) {
    warnings.push(`Providers with recent non-cooldown failures: ${degradedProviders.join(", ")}.`);
  }

  return warnings;
}

export async function buildDoctorReport(options = {}) {
  const env = options.env ?? process.env;
  const config = options.config ?? DEFAULT_CONFIG;
  const cwd = options.cwd ?? process.cwd();
  const snapshot = buildCapabilitySnapshot({
    env,
    config,
    runtimeAvailability: options.runtimeAvailability,
  });
  const health = await buildHealthSnapshot({ cwd, config, now: options.now });
  const cache = await getCacheStats({ cwd, config, now: options.now });
  const configuredProviders = snapshot.configuredProviders;
  const availableFeatures = snapshot.availableFeatures;
  const credentialedProviders = snapshot.providers
    .filter((provider) => provider.env.length > 0 && provider.credentialed)
    .map((provider) => provider.id);
  const configuredProviderSet = new Set(configuredProviders);
  const degradedProviders = Object.entries(health.providers)
    .filter(([providerId, state]) => configuredProviderSet.has(providerId) && state.status === "degraded")
    .map(([providerId]) => providerId);
  const cooldownProviders = Object.entries(health.providers)
    .filter(([providerId, state]) => configuredProviderSet.has(providerId) && state.status === "cooldown")
    .map(([providerId]) => providerId);
  const healthyProviders = configuredProviders.filter(
    (providerId) => health.providers[providerId]?.status === "healthy",
  );
  const baselineProviders = snapshot.providers
    .filter((provider) => provider.activation === "baseline" && configuredProviderSet.has(provider.id))
    .map((provider) => provider.id);
  const baselineStatus = !config.routing.allowNoKeyBaseline
    ? "disabled"
    : baselineProviders.some((providerId) =>
          ["degraded", "cooldown"].includes(health.providers[providerId]?.status),
        )
      ? "degraded"
      : "ready";

  return {
    status:
      !(
        availableFeatures.search ||
        availableFeatures.extract ||
        availableFeatures.crawl ||
        availableFeatures.map
      )
        ? "missing_credentials"
        : degradedProviders.length > 0 || cooldownProviders.length > 0
          ? "degraded"
          : "ready",
    configuredProviders,
    credentialedProviders,
    healthyProviders,
    degradedProviders,
    cooldownProviders,
    baselineStatus,
    availableFeatures,
    warnings: buildWarnings({
      availableFeatures,
      credentialedProviders,
      degradedProviders,
      cooldownProviders,
      baselineStatus,
    }),
    providers: snapshot.providers,
    cache,
    health: health.providers,
    federation: {
      enabled: config.routing.enableFederation,
      triggers: config.routing.federationTriggers,
      mergePolicy: config.routing.mergePolicy,
    },
    safeFetch: {
      allowedProtocols: ["http", "https"],
      blockedUrlClasses: [
        "file/ftp/ws/wss/data/javascript schemes",
        "credential-bearing URLs",
        "localhost/.local/.internal hosts",
        "private, loopback, link-local, and metadata IPs",
      ],
      revalidateRedirects: true,
      blockBinaryDownloads: true,
      executeJavaScript: false,
      headlessBrowser: false,
    },
    config,
    configPath: options.configMeta?.path ?? null,
  };
}

export function formatDoctorMarkdown(report) {
  const lines = [];

  lines.push("# web-search-pro doctor");
  lines.push("");
  lines.push(`- Status: ${report.status}`);
  lines.push(
    `- Configured providers: ${
      report.configuredProviders.length > 0 ? report.configuredProviders.join(", ") : "none"
    }`,
  );
  lines.push(
    `- Credentialed providers: ${
      report.credentialedProviders.length > 0 ? report.credentialedProviders.join(", ") : "none"
    }`,
  );
  lines.push(`- Baseline status: ${report.baselineStatus}`);
  lines.push(
    `- Federation: ${report.federation.enabled ? "enabled" : "disabled"} (${report.federation.triggers.join(", ")}, merge=${report.federation.mergePolicy})`,
  );
  lines.push(
    `- Available features: ${Object.entries(report.availableFeatures)
      .filter(([, value]) => value === true || (Array.isArray(value) && value.length > 0))
      .map(([key, value]) => (Array.isArray(value) ? `${key}=${value.join(",")}` : key))
      .join(", ") || "none"}`,
  );
  lines.push(
    `- Degraded providers: ${report.degradedProviders.length > 0 ? report.degradedProviders.join(", ") : "none"}`,
  );
  lines.push(
    `- Cooldown providers: ${report.cooldownProviders.length > 0 ? report.cooldownProviders.join(", ") : "none"}`,
  );
  lines.push(`- Cache: ${report.cache.enabled ? `enabled (${report.cache.dir})` : "disabled"}`);
  lines.push("");

  if (report.warnings.length > 0) {
    lines.push("## Warnings");
    lines.push("");
    for (const warning of report.warnings) {
      lines.push(`- ${warning}`);
    }
    lines.push("");
  }

  lines.push("## Safe Fetch Policy");
  lines.push("");
  lines.push(`- Allowed protocols: ${report.safeFetch.allowedProtocols.join(", ")}`);
  lines.push(`- Redirects revalidated: ${report.safeFetch.revalidateRedirects ? "yes" : "no"}`);
  lines.push(`- Binary downloads blocked: ${report.safeFetch.blockBinaryDownloads ? "yes" : "no"}`);
  lines.push(`- Execute JavaScript: ${report.safeFetch.executeJavaScript ? "yes" : "no"}`);
  lines.push("");
  return lines.join("\n");
}
