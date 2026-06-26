import { canonicalizeUrl } from "../dedupe.mjs";
import { buildNormalizedClaimKey } from "./claim-normalize.mjs";
import { curateResearchEntry } from "./noise-filter.mjs";

const AUTHORITY_RANK = Object.freeze({
  unknown: 0,
  "reputable-third-party": 1,
  primary: 2,
  official: 3,
});

const FRESHNESS_RANK = Object.freeze({
  unknown: 0,
  stale: 1,
  recent: 2,
  current: 3,
});

const COVERAGE_RANK = Object.freeze({
  low: 0,
  medium: 1,
  high: 2,
});

const DOCUMENT_QUALITY_RANK = Object.freeze({
  low: 0,
  medium: 1,
  high: 2,
});

const SOURCE_PRIORITY_RANK = Object.freeze({
  low: 0,
  standard: 1,
  preferred: 2,
  official: 3,
});

const LOW_VALUE_HOST_PATTERNS = Object.freeze([
  /(^|\.)scribd\.com$/i,
  /(^|\.)slideshare\.net$/i,
  /(^|\.)issuu\.com$/i,
]);

function safeHostname(value = "") {
  try {
    return new URL(value).hostname.toLowerCase();
  } catch {
    return "";
  }
}

function pickFirstSentence(text) {
  const normalized = String(text ?? "").trim();
  if (!normalized || normalized.length < 20) {
    return null;
  }
  const match = normalized.match(/(.+?[.!?])(?:\s|$)/);
  const sentence = (match?.[1] ?? normalized).trim();
  return sentence.length >= 20 ? sentence : null;
}

function normalizeTimestamp(value) {
  if (typeof value === "number") {
    return value;
  }
  if (typeof value === "string" && value.trim()) {
    const parsed = Date.parse(value);
    return Number.isNaN(parsed) ? null : parsed;
  }
  return null;
}

function inferSourceType(taskKind, entry) {
  if (taskKind === "map") {
    return "site-map";
  }
  const url = String(entry.url ?? "");
  const sourceHint = `${url} ${entry.title ?? ""}`;
  if (/docs|documentation|reference/i.test(url)) {
    return "docs";
  }
  if (/api\//i.test(url) || /\bapi\b/i.test(sourceHint)) {
    return "docs";
  }
  if (taskKind === "crawl" || taskKind === "extract") {
    return /docs|documentation|reference|api/i.test(sourceHint) ? "docs" : "article";
  }
  if (/blog|news|updates/i.test(url)) {
    return "blog";
  }
  return entry.sourceType ?? "search-result";
}

function inferAuthority(entry, sourceType) {
  const url = String(entry.url ?? "");
  const hostname = safeHostname(url);
  if (sourceType === "docs" || sourceType === "site-map") {
    return "official";
  }
  if (/^(docs|api|reference)\./i.test(hostname)) {
    return "official";
  }
  if (sourceType === "article" && !/blog|news|github|forum|reddit|medium|scribd/i.test(url)) {
    return "primary";
  }
  if (/blog|news|github|forum|medium/i.test(url)) {
    return "reputable-third-party";
  }
  return "unknown";
}

function inferCredibility(authority) {
  if (authority === "official" || authority === "primary") {
    return "official";
  }
  if (authority === "reputable-third-party") {
    return "reputable-third-party";
  }
  return "unknown";
}

function buildClaims(entry) {
  const candidates = [
    pickFirstSentence(entry.content),
    pickFirstSentence(entry.snippet),
    pickFirstSentence(entry.title),
  ].filter(Boolean);
  return Array.from(new Set(candidates)).slice(0, 2);
}

function buildClaimKey(entry) {
  const base = buildClaims(entry)[0] ?? entry.title ?? entry.url ?? "";
  return buildNormalizedClaimKey(base);
}

export function classifyEvidenceFreshness(publishedDate, now = Date.now()) {
  const publishedAt = normalizeTimestamp(publishedDate);
  const currentTime = normalizeTimestamp(now) ?? Date.now();
  if (publishedAt === null) {
    return "unknown";
  }
  const ageDays = Math.floor((currentTime - publishedAt) / 86400000);
  if (ageDays <= 30) {
    return "current";
  }
  if (ageDays <= 180) {
    return "recent";
  }
  return "stale";
}

function inferCoverage(taskKind, entry) {
  const contentLength = String(entry.content ?? entry.snippet ?? "").trim().length;
  if ((taskKind === "crawl" || taskKind === "extract") && contentLength >= 30) {
    return "high";
  }
  if (taskKind === "search" && contentLength > 0) {
    return "medium";
  }
  if (taskKind === "crawl" || taskKind === "extract") {
    return "medium";
  }
  return "low";
}

function inferSourcePriority({
  authority,
  sourceType,
  documentQuality,
  hasPrimaryContent,
  url,
}) {
  const hostname = safeHostname(url);
  if (authority === "official") {
    return "official";
  }
  if (LOW_VALUE_HOST_PATTERNS.some((pattern) => pattern.test(hostname))) {
    return "low";
  }
  if (authority === "primary") {
    return "preferred";
  }
  if (sourceType === "site-map" || sourceType === "docs") {
    return "preferred";
  }
  if (documentQuality === "low" || hasPrimaryContent !== true) {
    return "low";
  }
  return authority === "reputable-third-party" ? "standard" : "standard";
}

function inferSelectionReason({
  sourcePriority,
  sourceType,
  authority,
}) {
  if (sourcePriority === "official") {
    return "official-source";
  }
  if (sourceType === "site-map") {
    return "structural-source";
  }
  if (authority === "primary") {
    return "primary-source";
  }
  if (sourcePriority === "low") {
    return "low-value-source";
  }
  return "supporting-source";
}

function pickRankedValue(current, next, ranking) {
  if (!current) {
    return next;
  }
  return (ranking[next] ?? -1) > (ranking[current] ?? -1) ? next : current;
}

function normalizeTaskResults(task, payload) {
  if (task.kind === "map") {
    return (payload.nodes ?? []).map((node) => ({
      title: node.title ?? node.url,
      url: node.url,
      snippet: `Discovered at depth ${node.depth}${node.discoveredFrom ? ` from ${node.discoveredFrom}` : ""}.`,
      content: "",
      publishedDate: null,
      sourceType: "site-map",
      conflictsWith: [],
      providerIds: payload.selectedProvider ? [payload.selectedProvider] : [],
    }));
  }

  const results = payload.results ?? payload.pages ?? [];
  return results.map((entry) => ({
    title: entry.title ?? entry.url ?? "",
    url: entry.url ?? "",
    snippet: entry.snippet ?? entry.content ?? "",
    content: entry.content ?? "",
    publishedDate: entry.publishedDate ?? entry.date ?? null,
    sourceType: entry.sourceType ?? null,
    conflictsWith: entry.conflictsWith ?? [],
    providerIds:
      entry.providers ??
      entry.providerIds ??
      (payload.selectedProvider ? [payload.selectedProvider] : []),
  }));
}

function mergeEvidenceRecord(existing, next) {
  const existingContent = existing.content?.length ?? 0;
  const nextContent = next.content?.length ?? 0;
  const base = nextContent >= existingContent ? next : existing;

  return {
    ...base,
    providerIds: Array.from(
      new Set([...(existing.providerIds ?? []), ...(next.providerIds ?? [])]),
    ),
    claims: Array.from(new Set([...(existing.claims ?? []), ...(next.claims ?? [])])).slice(0, 4),
    conflictsWith: Array.from(
      new Set([...(existing.conflictsWith ?? []), ...(next.conflictsWith ?? [])]),
    ),
    authority: pickRankedValue(existing.authority, next.authority, AUTHORITY_RANK),
    credibility: pickRankedValue(existing.credibility, next.credibility, AUTHORITY_RANK),
    freshness: pickRankedValue(existing.freshness, next.freshness, FRESHNESS_RANK),
    coverage: pickRankedValue(existing.coverage, next.coverage, COVERAGE_RANK),
    documentQuality: pickRankedValue(
      existing.documentQuality,
      next.documentQuality,
      DOCUMENT_QUALITY_RANK,
    ),
    sourcePriority: pickRankedValue(
      existing.sourcePriority,
      next.sourcePriority,
      SOURCE_PRIORITY_RANK,
    ),
    claimKey: base.claimKey ?? existing.claimKey ?? next.claimKey,
    stalenessFlag: existing.stalenessFlag && next.stalenessFlag,
    boilerplateRatio: Math.min(existing.boilerplateRatio ?? 1, next.boilerplateRatio ?? 1),
    hasPrimaryContent: existing.hasPrimaryContent || next.hasPrimaryContent,
    selectionReason:
      (SOURCE_PRIORITY_RANK[next.sourcePriority] ?? -1) >=
      (SOURCE_PRIORITY_RANK[existing.sourcePriority] ?? -1)
        ? next.selectionReason
        : existing.selectionReason,
  };
}

function sortEvidence(left, right) {
  if (left.subquestionId !== right.subquestionId) {
    return left.subquestionId.localeCompare(right.subquestionId);
  }
  const sourceDiff =
    (SOURCE_PRIORITY_RANK[right.sourcePriority] ?? 0) -
    (SOURCE_PRIORITY_RANK[left.sourcePriority] ?? 0);
  if (sourceDiff !== 0) {
    return sourceDiff;
  }
  const authorityDiff =
    (AUTHORITY_RANK[right.authority] ?? 0) - (AUTHORITY_RANK[left.authority] ?? 0);
  if (authorityDiff !== 0) {
    return authorityDiff;
  }
  const qualityDiff =
    (DOCUMENT_QUALITY_RANK[right.documentQuality] ?? 0) -
    (DOCUMENT_QUALITY_RANK[left.documentQuality] ?? 0);
  if (qualityDiff !== 0) {
    return qualityDiff;
  }
  const freshnessDiff =
    (FRESHNESS_RANK[right.freshness] ?? 0) - (FRESHNESS_RANK[left.freshness] ?? 0);
  if (freshnessDiff !== 0) {
    return freshnessDiff;
  }
  return left.id.localeCompare(right.id);
}

export function normalizeResearchEvidence(taskExecutions = [], options = {}) {
  const retrievedAt = options.retrievedAt ?? null;
  const recentInformationPreferred = options.recentInformationPreferred ?? true;
  const deduped = new Map();
  let sequence = 1;

  for (const execution of taskExecutions) {
    const task = execution.task;
    const payload = execution.result ?? {};
    const entries = normalizeTaskResults(task, payload);

    for (const rawEntry of entries) {
      const sourceType = inferSourceType(task.kind, rawEntry);
      const curated = curateResearchEntry({
        taskKind: task.kind,
        entry: rawEntry,
        sourceType,
      });
      if (curated.dropped) {
        continue;
      }

      const entry = curated.entry;
      const canonicalUrl = canonicalizeUrl(entry.url);
      const authority = inferAuthority(entry, sourceType);
      const claims = buildClaims(entry);
      if (
        curated.assessment.listHeavy === true &&
        claims.length === 0 &&
        task.kind !== "map"
      ) {
        continue;
      }
      const freshness = classifyEvidenceFreshness(entry.publishedDate, retrievedAt);
      const sourcePriority = inferSourcePriority({
        authority,
        sourceType,
        documentQuality: curated.assessment.documentQuality,
        hasPrimaryContent: curated.assessment.hasPrimaryContent,
        url: entry.url,
      });
      const record = {
        id: `ev-${sequence++}`,
        subquestionId: task.subquestionId,
        taskId: task.id,
        title: entry.title ?? entry.url,
        url: canonicalUrl || entry.url,
        snippet: entry.snippet ?? "",
        content: entry.content ?? "",
        sourceType,
        providerIds: Array.from(new Set(entry.providerIds ?? [])),
        retrievedAt,
        publishedDate: entry.publishedDate ?? null,
        authority,
        credibility: inferCredibility(authority),
        freshness,
        coverage: inferCoverage(task.kind, entry),
        documentQuality: curated.assessment.documentQuality,
        boilerplateRatio: curated.assessment.boilerplateRatio,
        hasPrimaryContent: curated.assessment.hasPrimaryContent,
        sourcePriority,
        selectionReason: inferSelectionReason({
          sourcePriority,
          sourceType,
          authority,
        }),
        claimKey: buildClaimKey(entry),
        stalenessFlag: recentInformationPreferred && freshness === "stale",
        claims,
        conflictsWith: Array.from(new Set(entry.conflictsWith ?? [])),
      };

      if (!canonicalUrl) {
        deduped.set(record.id, record);
        continue;
      }

      const existing = deduped.get(canonicalUrl);
      if (!existing) {
        deduped.set(canonicalUrl, record);
        continue;
      }

      deduped.set(canonicalUrl, mergeEvidenceRecord(existing, record));
    }
  }

  return Array.from(deduped.values()).sort(sortEvidence);
}
