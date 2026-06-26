import { buildClaimClusters } from "./claim-cluster.mjs";
import { compactResearchFindings } from "./finding-compact.mjs";

const AUTHORITY_SCORE = Object.freeze({
  official: 1,
  primary: 0.85,
  "reputable-third-party": 0.65,
  unknown: 0.45,
});

const FRESHNESS_SCORE = Object.freeze({
  current: 1,
  recent: 0.8,
  stale: 0.45,
  unknown: 0.55,
});

const COVERAGE_SCORE = Object.freeze({
  high: 1,
  medium: 0.7,
  low: 0.4,
});

const SOURCE_DIVERSITY_SCORE = Object.freeze({
  high: 1,
  medium: 0.7,
  low: 0.35,
});

const CLAIM_CONSISTENCY_SCORE = Object.freeze({
  high: 1,
  medium: 0.75,
  low: 0.3,
});

const DOCUMENT_QUALITY_SCORE = Object.freeze({
  high: 1,
  medium: 0.7,
  low: 0.35,
});

const SOURCE_PRIORITY_SCORE = Object.freeze({
  official: 1,
  preferred: 0.8,
  standard: 0.6,
  low: 0.25,
});

function buildCitations(evidence = []) {
  return evidence.map((entry) => ({
    id: `cit-${entry.id}`,
    evidenceId: entry.id,
    url: entry.url,
    title: entry.title,
    publishedDate: entry.publishedDate ?? null,
    sourceType: entry.sourceType,
  }));
}

function buildConflictUncertainties(claimClusters = []) {
  const uncertainties = [];
  const seenPairs = new Set();

  for (const cluster of claimClusters) {
    if (cluster.hasInternalConflict) {
      uncertainties.push({
        id: `unc-${cluster.id}-internal-conflict`,
        type: "source-conflict",
        description: `Claim cluster ${cluster.id} contains conflicting evidence about the same claim.`,
        subquestionId: cluster.subquestionId,
        relatedEvidenceIds: [...cluster.evidenceIds],
        priority: "low",
        followupEligible: false,
        recommendedNextAction: "Collect another primary source before synthesizing a final answer.",
      });
    }
    for (const relatedId of cluster.conflictsWith ?? []) {
      const pair = [cluster.id, relatedId].sort().join(":");
      if (seenPairs.has(pair)) {
        continue;
      }
      seenPairs.add(pair);
      uncertainties.push({
        id: `unc-${pair}`,
        type: "source-conflict",
        description: `Claim cluster ${cluster.id} conflicts with ${relatedId}.`,
        subquestionId: cluster.subquestionId,
        relatedEvidenceIds: [cluster.id, relatedId],
        priority: "low",
        followupEligible: false,
        recommendedNextAction: "Collect another primary source before synthesizing a final answer.",
      });
    }
  }

  return uncertainties;
}

function clusterSizeScore(cluster) {
  return Math.min(1, 0.45 + cluster.evidenceIds.length * 0.18);
}

function computeClusterConfidence(cluster) {
  const score =
    (AUTHORITY_SCORE[cluster.authority] ?? 0.45) * 0.22 +
    (FRESHNESS_SCORE[cluster.freshness] ?? 0.55) * 0.13 +
    (COVERAGE_SCORE[cluster.coverage] ?? 0.4) * 0.14 +
    (SOURCE_DIVERSITY_SCORE[cluster.sourceDiversity] ?? 0.35) * 0.16 +
    (CLAIM_CONSISTENCY_SCORE[cluster.claimConsistency] ?? 0.3) * 0.15 +
    (DOCUMENT_QUALITY_SCORE[cluster.documentQuality] ?? 0.35) * 0.07 +
    (SOURCE_PRIORITY_SCORE[cluster.sourcePriority] ?? 0.25) * 0.05 +
    clusterSizeScore(cluster) * 0.08;
  const bounded = Math.max(0.1, Math.min(1, score));
  if (cluster.hasInternalConflict || cluster.conflictsWith.length > 0) {
    return Math.min(bounded, 0.69);
  }
  return bounded;
}

function buildSupportProfile(cluster) {
  return {
    authority: cluster.authority,
    freshness: cluster.freshness,
    coverage: cluster.coverage,
    sourceDiversity: cluster.sourceDiversity,
    claimConsistency: cluster.claimConsistency,
    documentQuality: cluster.documentQuality,
    sourcePriority: cluster.sourcePriority,
  };
}

function buildGapSensitive(cluster) {
  return (
    cluster.stalenessFlag === true ||
    cluster.hasAuthoritativeEvidence !== true ||
    cluster.sourceDiversity === "low" ||
    cluster.claimConsistency !== "high" ||
    cluster.documentQuality !== "high"
  );
}

function buildRawCandidateFindings(claimClusters = []) {
  return claimClusters.map((cluster, index) => {
    const confidence = computeClusterConfidence(cluster);
    return {
      id: `finding-${index + 1}`,
      statement: cluster.statement || `Evidence exists in ${cluster.id}.`,
      subquestionIds: [cluster.subquestionId],
      claimClusterIds: [cluster.id],
      evidenceIds: cluster.evidenceIds,
      supportProfile: buildSupportProfile(cluster),
      gapSensitive: buildGapSensitive(cluster),
      hasTextClaim: cluster.hasTextClaim,
      confidence,
      status:
        cluster.hasInternalConflict || cluster.conflictsWith.length > 0
          ? "conflicted"
          : confidence >= 0.78 &&
              cluster.hasAuthoritativeEvidence &&
              cluster.claimConsistency !== "low"
            ? "supported"
            : "weakly-supported",
    };
  });
}

export function analyzeResearchEvidence({ request = {}, subquestions = [], evidence = [] }) {
  const uncertainties = [];
  const claimClusters = buildClaimClusters(evidence);
  const officialSourcesPreferred = request.constraints?.officialSourcesPreferred ?? true;
  const recentInformationPreferred = request.constraints?.recentInformationPreferred ?? true;

  for (const subquestion of subquestions) {
    const records = evidence.filter((entry) => entry.subquestionId === subquestion.id);
    const clusters = claimClusters.filter((entry) => entry.subquestionId === subquestion.id);

    if (records.length === 0) {
      uncertainties.push({
        id: `unc-${subquestion.id}-missing`,
        type: "missing-evidence",
        description: `No evidence was collected for subquestion ${subquestion.id}.`,
        subquestionId: subquestion.id,
        relatedEvidenceIds: [],
        priority: "medium",
        followupEligible: true,
        recommendedNextAction: "Run another targeted retrieval task for this subquestion.",
      });
      continue;
    }

    const hasAuthoritativeEvidence = clusters.some((entry) => entry.hasAuthoritativeEvidence);
    if (officialSourcesPreferred && !hasAuthoritativeEvidence) {
      uncertainties.push({
        id: `unc-${subquestion.id}-official`,
        type: "insufficient-official-sources",
        description: `No official or primary source was collected for subquestion ${subquestion.id}.`,
        subquestionId: subquestion.id,
        relatedEvidenceIds: records.map((entry) => entry.id),
        priority: "high",
        followupEligible: true,
        recommendedNextAction: "Look for an official or primary source to strengthen this pack.",
      });
    }

    if (
      recentInformationPreferred &&
      clusters.length > 0 &&
      clusters.every((entry) => entry.stalenessFlag === true)
    ) {
      uncertainties.push({
        id: `unc-${subquestion.id}-stale`,
        type: "stale-information",
        description: `All evidence collected for ${subquestion.id} appears stale relative to the request.`,
        subquestionId: subquestion.id,
        relatedEvidenceIds: clusters.flatMap((entry) => entry.evidenceIds),
        priority: "high",
        followupEligible: true,
        recommendedNextAction: "Collect a more recent source before producing a final answer.",
      });
    }
  }

  uncertainties.push(...buildConflictUncertainties(claimClusters));

  const rawCandidateFindings = buildRawCandidateFindings(claimClusters);
  const compacted = compactResearchFindings({
    subquestions,
    candidateFindings: rawCandidateFindings,
    uncertainties,
    evidence,
  });

  return {
    claimClusters,
    candidateFindings: compacted.candidateFindings,
    subquestionBriefs: compacted.subquestionBriefs,
    uncertainties,
    citations: buildCitations(evidence),
  };
}
