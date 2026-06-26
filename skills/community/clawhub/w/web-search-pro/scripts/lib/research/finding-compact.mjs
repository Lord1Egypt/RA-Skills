const STATUS_RANK = Object.freeze({
  supported: 3,
  conflicted: 2,
  "weakly-supported": 1,
});

const SOURCE_PRIORITY_RANK = Object.freeze({
  official: 3,
  preferred: 2,
  standard: 1,
  low: 0,
});

const DOCUMENT_QUALITY_RANK = Object.freeze({
  high: 2,
  medium: 1,
  low: 0,
});

const MAX_FINDINGS_PER_SUBQUESTION = 2;

function sortFindings(left, right) {
  const statusDiff = (STATUS_RANK[right.status] ?? 0) - (STATUS_RANK[left.status] ?? 0);
  if (statusDiff !== 0) {
    return statusDiff;
  }
  const confidenceDiff = (right.confidence ?? 0) - (left.confidence ?? 0);
  if (confidenceDiff !== 0) {
    return confidenceDiff;
  }
  const sourceDiff =
    (SOURCE_PRIORITY_RANK[right.supportProfile?.sourcePriority] ?? 0) -
    (SOURCE_PRIORITY_RANK[left.supportProfile?.sourcePriority] ?? 0);
  if (sourceDiff !== 0) {
    return sourceDiff;
  }
  return (
    (DOCUMENT_QUALITY_RANK[right.supportProfile?.documentQuality] ?? 0) -
    (DOCUMENT_QUALITY_RANK[left.supportProfile?.documentQuality] ?? 0)
  );
}

function isLowValueWeakFinding(finding) {
  return (
    finding.status === "weakly-supported" &&
    finding.confidence < 0.6 &&
    finding.supportProfile?.documentQuality === "low" &&
    finding.supportProfile?.sourcePriority === "low"
  );
}

function shouldSuppressWeakSupportingFinding(finding, candidates) {
  const hasPreferredAnchor = candidates.some((entry) =>
    ["official", "preferred"].includes(entry.supportProfile?.sourcePriority),
  );
  if (!hasPreferredAnchor) {
    return false;
  }
  return (
    finding.status === "weakly-supported" &&
    finding.supportProfile?.sourcePriority === "standard" &&
    finding.confidence < 0.72
  );
}

function shouldSuppressTitleOnlyFinding(finding) {
  return finding.status === "weakly-supported" && finding.hasTextClaim !== true;
}

function pickTopEvidenceIds(subquestionId, candidateFindings, evidence = []) {
  const evidenceIds = [];
  for (const finding of candidateFindings) {
    for (const evidenceId of finding.evidenceIds ?? []) {
      if (!evidenceIds.includes(evidenceId)) {
        evidenceIds.push(evidenceId);
      }
    }
  }

  if (evidenceIds.length > 0) {
    return evidenceIds.slice(0, 5);
  }

  const rankedEvidence = evidence
    .filter((entry) => entry.subquestionId === subquestionId)
    .sort((left, right) => {
      const sourceDiff =
        (SOURCE_PRIORITY_RANK[right.sourcePriority] ?? 0) -
        (SOURCE_PRIORITY_RANK[left.sourcePriority] ?? 0);
      if (sourceDiff !== 0) {
        return sourceDiff;
      }
      return (
        (DOCUMENT_QUALITY_RANK[right.documentQuality] ?? 0) -
        (DOCUMENT_QUALITY_RANK[left.documentQuality] ?? 0)
      );
    });
  return rankedEvidence.map((entry) => entry.id).slice(0, 5);
}

export function compactResearchFindings({
  subquestions = [],
  candidateFindings = [],
  uncertainties = [],
  evidence = [],
}) {
  const compacted = [];
  const subquestionBriefs = [];

  for (const subquestion of subquestions) {
    const candidates = candidateFindings
      .filter((entry) => entry.subquestionIds?.includes(subquestion.id))
      .sort(sortFindings);
    const kept = [];

    for (const finding of candidates) {
      if (kept.length >= MAX_FINDINGS_PER_SUBQUESTION) {
        break;
      }
      if (isLowValueWeakFinding(finding) && kept.length > 0) {
        continue;
      }
      if (shouldSuppressWeakSupportingFinding(finding, candidates) && kept.length > 0) {
        continue;
      }
      if (shouldSuppressTitleOnlyFinding(finding)) {
        continue;
      }
      if (
        finding.supportProfile?.sourcePriority === "low" &&
        finding.status === "weakly-supported"
      ) {
        continue;
      }
      kept.push(finding);
    }

    if (
      kept.length === 0 &&
      candidates[0] &&
      (candidates[0].status !== "weakly-supported" || candidates[0].hasTextClaim === true)
    ) {
      kept.push(candidates[0]);
    }

    compacted.push(...kept);

    const relatedUncertainties = uncertainties.filter(
      (entry) => entry.subquestionId === subquestion.id,
    );
    subquestionBriefs.push({
      subquestionId: subquestion.id,
      supportedFacts: kept
        .filter((entry) => entry.status !== "conflicted")
        .map((entry) => entry.statement)
        .slice(0, 3),
      conflicts: relatedUncertainties
        .filter((entry) => entry.type === "source-conflict")
        .map((entry) => entry.description),
      missing: relatedUncertainties
        .filter((entry) => entry.type !== "source-conflict")
        .map((entry) => entry.description),
      topEvidenceIds: pickTopEvidenceIds(subquestion.id, kept, evidence),
    });
    if (kept.length === 0 && candidates.length > 0) {
      subquestionBriefs[subquestionBriefs.length - 1].missing.push(
        "Collected evidence was too weak or too noisy to promote into a compact finding.",
      );
    }
  }

  return {
    candidateFindings: compacted,
    subquestionBriefs,
  };
}
