import { getProvider } from "./providers.mjs";

function parseDate(value) {
  if (!value) {
    return null;
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function isDomainMatch(item, request) {
  if (!request.includeDomains?.length) {
    return false;
  }
  try {
    const hostname = new URL(item.url).hostname.toLowerCase();
    return request.includeDomains.some((domain) => hostname === domain || hostname.endsWith(`.${domain}`));
  } catch {
    return false;
  }
}

function contentCompleteness(item) {
  const length = String(item.content ?? "").trim().length;
  if (length >= 240) {
    return 1;
  }
  if (length >= 120) {
    return 0.6;
  }
  if (length >= 40) {
    return 0.3;
  }
  return 0;
}

function freshnessBonus(item, now) {
  const date = parseDate(item.publishedDate ?? item.date);
  if (!date) {
    return 0;
  }

  const ageDays = Math.max(0, Math.floor((now - date.getTime()) / 86400000));
  if (ageDays <= 7) {
    return 0.12;
  }
  if (ageDays <= 30) {
    return 0.08;
  }
  if (ageDays <= 180) {
    return 0.04;
  }
  return 0;
}

function sourceDiversityBonus(provider, primaryProvider, mergePolicy) {
  if (!provider || !primaryProvider || provider.id === primaryProvider.id) {
    return 0;
  }

  let bonus = 0.04;
  if (provider.capabilities.domainFilterMode !== primaryProvider.capabilities.domainFilterMode) {
    bonus += 0.03;
  }
  if (provider.capabilities.localeFiltering !== primaryProvider.capabilities.localeFiltering) {
    bonus += 0.03;
  }
  if (provider.capabilities.answerSynthesis !== primaryProvider.capabilities.answerSynthesis) {
    bonus += 0.02;
  }
  if ((provider.capabilities.subEngines?.length ?? 0) !== (primaryProvider.capabilities.subEngines?.length ?? 0)) {
    bonus += 0.02;
  }
  if (mergePolicy === "diversity-first") {
    bonus += 0.08;
  }

  return bonus;
}

export function rerankFederatedResults(results = [], options = {}) {
  const primaryProviderId = options.primaryProviderId ?? null;
  const request = options.request ?? {};
  const mergePolicy = options.mergePolicy ?? "balanced";
  const now = typeof options.now === "number" ? options.now : Date.now();
  const primaryProvider = primaryProviderId ? getProvider(primaryProviderId) : null;

  return results
    .map((item) => {
      const provider = getProvider(item.providerId);
      let federationScore = item.score ?? 0.45;

      federationScore += (provider?.routing.qualityScore ?? 0) * 0.025;
      federationScore += contentCompleteness(item) * 0.15;
      federationScore += freshnessBonus(item, now);
      federationScore += sourceDiversityBonus(provider, primaryProvider, mergePolicy);

      if (item.providerId === primaryProviderId) {
        federationScore += mergePolicy === "diversity-first" ? 0.04 : 0.14;
      }
      if (isDomainMatch(item, request)) {
        federationScore += 0.12;
      }

      return {
        ...item,
        federationScore,
      };
    })
    .sort((left, right) => {
      if ((right.federationScore ?? 0) !== (left.federationScore ?? 0)) {
        return (right.federationScore ?? 0) - (left.federationScore ?? 0);
      }
      return left.providerRank - right.providerRank;
    });
}
