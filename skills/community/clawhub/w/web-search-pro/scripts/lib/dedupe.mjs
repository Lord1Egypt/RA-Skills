function normalizePathname(pathname) {
  if (!pathname || pathname === "/") {
    return "/";
  }
  return pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
}

function isTrackingParam(name) {
  return /^utm_/i.test(name) || ["gclid", "fbclid"].includes(name.toLowerCase());
}

function normalizeTitle(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");
}

function normalizeSnippet(value) {
  return String(value ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/\s+/g, " ");
}

function getHostname(rawUrl) {
  try {
    return new URL(rawUrl).hostname.toLowerCase();
  } catch {
    return "";
  }
}

function getDateKey(item) {
  const raw = item.publishedDate ?? item.date;
  if (!raw) {
    return "";
  }
  const parsed = new Date(raw);
  if (Number.isNaN(parsed.getTime())) {
    return String(raw).slice(0, 10);
  }
  return parsed.toISOString().slice(0, 10);
}

function hasSimilarContent(left, right) {
  const leftSnippet = normalizeSnippet(left.content ?? left.snippet ?? "");
  const rightSnippet = normalizeSnippet(right.content ?? right.snippet ?? "");

  if (leftSnippet.length < 40 || rightSnippet.length < 40) {
    return false;
  }

  const leftHead = leftSnippet.slice(0, 120);
  const rightHead = rightSnippet.slice(0, 120);
  return (
    leftHead === rightHead ||
    leftSnippet.includes(rightHead) ||
    rightSnippet.includes(leftHead)
  );
}

function areNearDuplicates(left, right) {
  const leftHost = getHostname(left.url);
  const rightHost = getHostname(right.url);
  if (!leftHost || leftHost !== rightHost) {
    return false;
  }

  const leftTitle = normalizeTitle(left.title);
  const rightTitle = normalizeTitle(right.title);
  if (!leftTitle || leftTitle !== rightTitle) {
    return false;
  }

  const leftDate = getDateKey(left);
  const rightDate = getDateKey(right);
  if (leftDate && rightDate && leftDate !== rightDate) {
    return false;
  }

  return hasSimilarContent(left, right) || (Boolean(leftDate) && leftDate === rightDate);
}

function mergeDuplicate(existing, incoming) {
  const preferred =
    (incoming.federationScore ?? -1) > (existing.federationScore ?? -1)
      ? incoming
      : existing;
  return {
    ...preferred,
    providerIds: Array.from(
      new Set([
        ...(existing.providerIds ?? [existing.providerId]),
        ...(incoming.providerIds ?? [incoming.providerId]),
      ]),
    ),
  };
}

export function canonicalizeUrl(rawUrl) {
  if (!rawUrl) {
    return "";
  }

  try {
    const url = new URL(rawUrl);
    url.hash = "";
    url.hostname = url.hostname.toLowerCase();
    url.pathname = normalizePathname(url.pathname);

    const params = new URLSearchParams(url.search);
    const kept = [];
    for (const [name, value] of params.entries()) {
      if (!isTrackingParam(name)) {
        kept.push([name, value]);
      }
    }
    kept.sort(([left], [right]) => left.localeCompare(right));
    url.search = kept.length > 0 ? new URLSearchParams(kept).toString() : "";

    return url.toString();
  } catch {
    return String(rawUrl);
  }
}

export function dedupeFederatedResults(results = []) {
  const exactDeduped = new Map();
  let dedupedUrls = 0;
  let nearDuplicateDrops = 0;

  for (const item of results) {
    const canonicalUrl = canonicalizeUrl(item.url);
    const normalizedItem = {
      ...item,
      url: canonicalUrl || item.url,
      providerIds: Array.from(new Set([...(item.providerIds ?? [item.providerId])])),
    };
    const existing = exactDeduped.get(canonicalUrl);

    if (!existing) {
      exactDeduped.set(canonicalUrl, normalizedItem);
      continue;
    }

    dedupedUrls += 1;
    exactDeduped.set(canonicalUrl, mergeDuplicate(existing, normalizedItem));
  }

  const nearDeduped = [];

  for (const item of exactDeduped.values()) {
    const duplicateIndex = nearDeduped.findIndex((entry) => areNearDuplicates(entry, item));
    if (duplicateIndex === -1) {
      nearDeduped.push(item);
      continue;
    }

    nearDuplicateDrops += 1;
    nearDeduped[duplicateIndex] = mergeDuplicate(nearDeduped[duplicateIndex], item);
  }

  return {
    results: nearDeduped,
    stats: {
      dedupedUrls,
      nearDuplicateDrops,
    },
  };
}
