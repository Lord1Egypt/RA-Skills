import { buildResearchSearchQuery } from "./question-templates.mjs";

function hostFromUrl(value) {
  try {
    return new URL(value).hostname;
  } catch {
    return null;
  }
}

function uniqueStrings(values = []) {
  return Array.from(new Set(values.filter(Boolean)));
}

export function evidencePriorityForSubquestion(subquestion) {
  if (subquestion.evidenceGoal === "official-proof") {
    return "official";
  }
  if (["recent-change", "timeline-proof"].includes(subquestion.evidenceGoal)) {
    return "recent";
  }
  if (subquestion.evidenceGoal === "structure-map") {
    return "structural";
  }
  return "diverse";
}

export function sourceDiversityTargetForSubquestion(subquestion) {
  if (["official-proof", "structure-map"].includes(subquestion.evidenceGoal)) {
    return "single-source-ok";
  }
  return "multi-source-preferred";
}

export function followupEligibleForSubquestion(subquestion) {
  return ["official-sources", "latest", "timeline", "site-structure"].includes(subquestion.intent);
}

function buildBaseTask({
  id,
  subquestion,
  kind,
  query = null,
  urls = [],
  reason,
  budget,
  options,
  phase = "primary",
  followupEligible = followupEligibleForSubquestion(subquestion),
}) {
  return {
    id,
    subquestionId: subquestion.id,
    kind,
    query,
    urls,
    reason,
    budget,
    evidencePriority: evidencePriorityForSubquestion(subquestion),
    sourceDiversityTarget: sourceDiversityTargetForSubquestion(subquestion),
    followupEligible,
    phase,
    status: "planned",
    options,
  };
}

export function buildResearchSearchTask({
  id,
  subquestion,
  request,
  topicType,
  query,
  reason,
  phase = "primary",
  includeDomains,
  timeRange,
  followupEligible,
}) {
  const scopedDomains = uniqueStrings([
    ...request.scope.includeDomains,
    ...request.scope.seedUrls.map((url) => hostFromUrl(url)),
  ]);
  const preferredDomains =
    includeDomains ??
    (subquestion.intent === "official-sources"
      ? scopedDomains
      : scopedDomains.length > 0
        ? scopedDomains
        : null);

  return buildBaseTask({
    id,
    subquestion,
    kind: "search",
    query: query ?? buildResearchSearchQuery(request.topic, subquestion.intent, topicType),
    reason: reason ?? subquestion.why,
    budget: {
      maxResults: Math.min(5, request.budgets.maxSearches || 0),
    },
    options: {
      count: 5,
      includeDomains: preferredDomains,
      excludeDomains:
        request.scope.excludeDomains.length > 0 ? request.scope.excludeDomains : null,
      fromDate: request.scope.fromDate,
      toDate: request.scope.toDate,
      timeRange:
        timeRange ??
        (["latest", "timeline"].includes(subquestion.intent) && !request.scope.fromDate
          ? "year"
          : null),
    },
    phase,
    followupEligible,
  });
}

export function buildResearchExtractTask({
  id,
  subquestion,
  request,
  urls,
  reason,
  phase = "primary",
  followupEligible,
}) {
  return buildBaseTask({
    id,
    subquestion,
    kind: "extract",
    urls: urls ?? request.scope.seedUrls.slice(0, 1),
    reason: reason ?? "Capture a readable primary-source page for the evidence pack.",
    budget: {
      maxChars: 4000,
    },
    options: {
      maxChars: 4000,
      allowRender: request.budgets.allowRender,
    },
    phase,
    followupEligible,
  });
}

export function buildResearchMapTask({
  id,
  subquestion,
  request,
  urls,
  reason,
  phase = "primary",
  followupEligible,
}) {
  return buildBaseTask({
    id,
    subquestion,
    kind: "map",
    urls: urls ?? request.scope.seedUrls.slice(0, 1),
    reason: reason ?? "Discover site structure before deeper extraction or crawl decisions.",
    budget: {
      depth: 1,
      maxPages: 20,
    },
    options: {
      depth: 1,
      maxPages: 20,
      sameOrigin: true,
    },
    phase,
    followupEligible,
  });
}

export function buildResearchCrawlTask({
  id,
  subquestion,
  request,
  urls,
  reason,
  phase = "primary",
  followupEligible,
}) {
  return buildBaseTask({
    id,
    subquestion,
    kind: "crawl",
    urls: urls ?? request.scope.seedUrls.slice(0, 1),
    reason: reason ?? "Collect a small same-origin document set for a deeper evidence pack.",
    budget: {
      depth: 1,
      maxPages: Math.min(request.budgets.maxCrawlPages, 10),
    },
    options: {
      depth: 1,
      maxPages: Math.min(request.budgets.maxCrawlPages, 10),
      sameOrigin: true,
    },
    phase,
    followupEligible,
  });
}
