function normalizeText(value) {
  return typeof value === "string" ? value : value == null ? "" : String(value);
}

function normalizeScore(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

export function normalizeProviderSearchResult(providerId, providerResult, options = {}) {
  const maxItems = options.maxItems ?? providerResult.results?.length ?? 0;

  return (providerResult.results ?? []).slice(0, maxItems).map((item, index) => ({
    title: normalizeText(item.title),
    url: normalizeText(item.url),
    content: normalizeText(item.content),
    score: normalizeScore(item.score),
    publishedDate: item.publishedDate ?? null,
    date: item.date ?? null,
    sourceType: "federated",
    providerId,
    providerIds: [providerId],
    providerEngine: providerResult.engine ?? providerId,
    providerRank: index,
  }));
}
