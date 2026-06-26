import { normalizeClaimText } from "./claim-normalize.mjs";

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

const DIVERSITY_RANK = Object.freeze({
  low: 0,
  medium: 1,
  high: 2,
});

const CONSISTENCY_RANK = Object.freeze({
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

function pickRanked(current, next, ranking) {
  if (!current) {
    return next;
  }
  return (ranking[next] ?? -1) > (ranking[current] ?? -1) ? next : current;
}

function pickRepresentativeClaim(records = []) {
  if (records.length === 0) {
    return "";
  }
  const sorted = [...records].sort((left, right) => {
    const authorityDiff =
      (AUTHORITY_RANK[right.authority] ?? 0) - (AUTHORITY_RANK[left.authority] ?? 0);
    if (authorityDiff !== 0) {
      return authorityDiff;
    }
    const sourceDiff =
      (SOURCE_PRIORITY_RANK[right.sourcePriority] ?? 0) -
      (SOURCE_PRIORITY_RANK[left.sourcePriority] ?? 0);
    if (sourceDiff !== 0) {
      return sourceDiff;
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
    return (String(right.content ?? "").length ?? 0) - (String(left.content ?? "").length ?? 0);
  });
  return sorted[0].claims?.[0] ?? sorted[0].title ?? "";
}

function inferSourceDiversity(records = []) {
  const sourceTypes = new Set(records.map((record) => record.sourceType ?? "unknown"));
  const authorities = new Set(records.map((record) => record.authority ?? "unknown"));
  const urls = new Set(records.map((record) => record.url ?? record.id));
  const providers = new Set(records.flatMap((record) => record.providerIds ?? []));

  if (sourceTypes.size >= 2 || authorities.size >= 2) {
    return "high";
  }
  if (urls.size >= 2 || providers.size >= 2) {
    return "medium";
  }
  return "low";
}

function inferClaimConsistency(records = [], hasConflict = false) {
  if (hasConflict) {
    return "low";
  }
  const normalizedClaims = new Set(
    records
      .flatMap((record) => record.claims ?? [])
      .map((claim) => normalizeClaimText(claim))
      .filter(Boolean),
  );
  return normalizedClaims.size <= 1 ? "high" : "medium";
}

export function buildClaimClusters(evidence = []) {
  const grouped = new Map();

  for (const record of evidence) {
    const clusterKey = `${record.subquestionId}:${record.claimKey || record.id}`;
    if (!grouped.has(clusterKey)) {
      grouped.set(clusterKey, []);
    }
    grouped.get(clusterKey).push(record);
  }

  const clusters = Array.from(grouped.entries()).map(([clusterKey, records], index) => {
    const [subquestionId, claimKey] = clusterKey.split(":");
    return {
      id: `cluster-${index + 1}`,
      subquestionId,
      claimKey,
      statement: pickRepresentativeClaim(records),
      evidenceIds: records.map((record) => record.id),
      providerIds: Array.from(
        new Set(records.flatMap((record) => record.providerIds ?? [])),
      ),
      authority: records.reduce(
        (value, record) => pickRanked(value, record.authority, AUTHORITY_RANK),
        null,
      ),
      freshness: records.reduce(
        (value, record) => pickRanked(value, record.freshness, FRESHNESS_RANK),
        null,
      ),
      coverage: records.reduce(
        (value, record) => pickRanked(value, record.coverage, COVERAGE_RANK),
        null,
      ),
      documentQuality: records.reduce(
        (value, record) => pickRanked(value, record.documentQuality, DOCUMENT_QUALITY_RANK),
        null,
      ),
      sourcePriority: records.reduce(
        (value, record) => pickRanked(value, record.sourcePriority, SOURCE_PRIORITY_RANK),
        null,
      ),
      conflictsWith: [],
      hasInternalConflict: false,
      hasTextClaim: records.some((record) => (record.claims ?? []).length > 0),
      hasAuthoritativeEvidence: records.some((record) =>
        ["official", "primary"].includes(record.authority),
      ),
      stalenessFlag: records.every(
        (record) => record.stalenessFlag === true || record.freshness === "stale",
      ),
      sourceDiversity: inferSourceDiversity(records),
      claimConsistency: inferClaimConsistency(records, false),
    };
  });

  const clusterByEvidenceId = new Map();
  for (const cluster of clusters) {
    for (const evidenceId of cluster.evidenceIds) {
      clusterByEvidenceId.set(evidenceId, cluster.id);
    }
  }

  const clusterMap = new Map(clusters.map((cluster) => [cluster.id, cluster]));
  for (const record of evidence) {
    const sourceClusterId = clusterByEvidenceId.get(record.id);
    for (const relatedEvidenceId of record.conflictsWith ?? []) {
      const targetClusterId = clusterByEvidenceId.get(relatedEvidenceId);
      if (!sourceClusterId || !targetClusterId) {
        continue;
      }
      const sourceCluster = clusterMap.get(sourceClusterId);
      if (sourceClusterId === targetClusterId) {
        sourceCluster.hasInternalConflict = true;
        continue;
      }
      const targetCluster = clusterMap.get(targetClusterId);
      sourceCluster.conflictsWith = Array.from(
        new Set([...(sourceCluster.conflictsWith ?? []), targetClusterId]),
      );
      targetCluster.conflictsWith = Array.from(
        new Set([...(targetCluster.conflictsWith ?? []), sourceClusterId]),
      );
    }
  }

  for (const cluster of clusters) {
    const records = evidence.filter((record) => cluster.evidenceIds.includes(record.id));
    cluster.claimConsistency = pickRanked(
      cluster.claimConsistency,
      inferClaimConsistency(records, cluster.hasInternalConflict || cluster.conflictsWith.length > 0),
      CONSISTENCY_RANK,
    );
    cluster.sourceDiversity = pickRanked(
      cluster.sourceDiversity,
      inferSourceDiversity(records),
      DIVERSITY_RANK,
    );
  }

  return clusters.sort((left, right) => left.id.localeCompare(right.id));
}
