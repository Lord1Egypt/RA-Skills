import { requestHasSelectionRequirements } from "./search-signals.mjs";

function sumContributions(candidate, predicate = () => true) {
  return (candidate?.contributions ?? []).reduce(
    (total, contribution) => (predicate(contribution) ? total + contribution.delta : total),
    0,
  );
}

function buildTopSignals(candidate) {
  return (candidate?.contributions ?? [])
    .filter((contribution) => contribution.kind === "signal" && contribution.delta > 0)
    .sort((left, right) => right.delta - left.delta)
    .slice(0, 5)
    .map((contribution) => ({
      id: contribution.id,
      label: contribution.label,
      category: contribution.category,
      delta: contribution.delta,
      evidence: contribution.evidence ?? null,
    }));
}

function buildRunnerUp(candidates, selectedProviderId) {
  const runnerUp = candidates
    .filter(
      (candidate) =>
        ["candidate", "selected"].includes(candidate.status) &&
        candidate.provider.id !== selectedProviderId,
    )
    .sort((left, right) => (right.score ?? 0) - (left.score ?? 0))[0];

  if (!runnerUp) {
    return null;
  }

  return {
    providerId: runnerUp.provider.id,
    score: runnerUp.score ?? null,
    summary: runnerUp.summary ?? null,
  };
}

function countCompetitiveCandidates(candidates) {
  return candidates.filter((candidate) => ["candidate", "selected"].includes(candidate.status)).length;
}

function isAvailabilityConstraint(candidate) {
  const constraints = candidate?.hardConstraints;
  if (!constraints) {
    return false;
  }
  return Boolean(
    constraints.missingCredentials ||
      constraints.runtimeUnavailable ||
      constraints.disabledByConfig ||
      constraints.baselineDisallowed,
  );
}

function hasNonAvailabilityConstraint(candidate) {
  const constraints = candidate?.hardConstraints;
  if (!constraints) {
    return false;
  }
  return Boolean(
    constraints.explicitEngineMismatch ||
      constraints.missingCapability?.length ||
      constraints.providerSpecific?.length,
  );
}

function isAvailabilityLimitedCompetitor(candidate) {
  return (
    candidate?.status === "rejected" &&
    isAvailabilityConstraint(candidate) &&
    !hasNonAvailabilityConstraint(candidate)
  );
}

function computeLimitedByAvailability(selected, candidates) {
  if (!selected) {
    return false;
  }
  if (selected.provider.activation === "baseline") {
    return true;
  }
  return candidates.some(
    (candidate) =>
      candidate.provider.id !== selected.provider.id &&
      isAvailabilityLimitedCompetitor(candidate),
  );
}

function computeHealthAdjusted(selected, candidates) {
  if (!selected) {
    return false;
  }

  const winnerWithoutHealth = [...candidates]
    .filter((candidate) => ["candidate", "selected"].includes(candidate.status))
    .map((candidate) => ({
      providerId: candidate.provider.id,
      score: sumContributions(candidate, (contribution) => contribution.kind !== "health-penalty"),
    }))
    .sort((left, right) => right.score - left.score)[0];

  return winnerWithoutHealth?.providerId !== selected.provider.id;
}

function determineSelectionMode({
  request,
  selected,
  candidates,
  limitedByAvailability,
  healthAdjusted,
}) {
  if (!selected) {
    return null;
  }
  if (request.engine) {
    return "explicit";
  }
  if (healthAdjusted) {
    return "fallback";
  }
  const topSignals = buildTopSignals(selected);
  const competitiveCandidateCount = countCompetitiveCandidates(candidates);
  const hasSelectionRequirements = requestHasSelectionRequirements(request);
  const availabilityDecisive = limitedByAvailability && competitiveCandidateCount <= 1;

  if (availabilityDecisive) {
    return "availability-only";
  }

  if (hasSelectionRequirements) {
    if (competitiveCandidateCount <= 1 || topSignals.length === 0) {
      return "hard-requirement";
    }
    return "intent-match";
  }
  if (topSignals.length > 0) {
    return "intent-match";
  }
  if (limitedByAvailability) {
    return "availability-only";
  }
  return "default-ranking";
}

function computeConfidenceValue({
  selectionMode,
  selected,
  runnerUp,
  limitedByAvailability,
  healthAdjusted,
}) {
  if (!selected) {
    return { value: null, level: null };
  }

  const margin = Math.max(0, (selected.score ?? 0) - (runnerUp?.score ?? 0));
  const normalizedMargin = Math.min(margin / 200, 0.3);
  const topSignals = buildTopSignals(selected);

  let value = 0.45;

  switch (selectionMode) {
    case "explicit":
      value = 0.98;
      break;
    case "hard-requirement":
      value = 0.9;
      break;
    case "intent-match":
      value = 0.66 + normalizedMargin;
      break;
    case "fallback":
      value = 0.58 + normalizedMargin / 2;
      break;
    case "availability-only":
      value = 0.22 + normalizedMargin / 3;
      break;
    default:
      value = 0.52 + normalizedMargin / 2;
      break;
  }

  if (topSignals.length >= 2 && selectionMode === "intent-match") {
    value += 0.05;
  }
  if (limitedByAvailability) {
    value -= 0.12;
  }
  if (healthAdjusted) {
    value -= 0.06;
  }

  const bounded = Math.max(0.05, Math.min(0.99, value));
  const level = bounded >= 0.75 ? "high" : bounded >= 0.45 ? "medium" : "low";

  return {
    value: Number(bounded.toFixed(2)),
    level,
    marginScore: margin,
  };
}

export function enrichPlanWithRoutingConfidence(plan) {
  if (!plan?.selected) {
    return {
      ...plan,
      diagnostics: {
        signalMatches: plan?.signalMatches ?? [],
        limitedByAvailability: false,
        healthAdjusted: false,
        runnerUp: null,
      },
    };
  }

  const selected = plan.selected;
  const runnerUp = buildRunnerUp(plan.candidates, selected.provider.id);
  const limitedByAvailability = computeLimitedByAvailability(selected, plan.candidates);
  const healthAdjusted = computeHealthAdjusted(selected, plan.candidates);
  const selectionMode = determineSelectionMode({
    request: plan.request,
    selected,
    candidates: plan.candidates,
    limitedByAvailability,
    healthAdjusted,
  });
  const topSignals = buildTopSignals(selected);
  const confidence = computeConfidenceValue({
    selectionMode,
    selected,
    runnerUp,
    limitedByAvailability,
    healthAdjusted,
  });

  return {
    ...plan,
    selected: {
      ...selected,
      selectionMode,
      topSignals,
      confidence: confidence.value,
      confidenceLevel: confidence.level,
    },
    candidates: plan.candidates.map((candidate) =>
      candidate.provider.id === selected.provider.id
        ? {
            ...candidate,
            selectionMode,
            topSignals,
            confidence: confidence.value,
            confidenceLevel: confidence.level,
          }
        : candidate,
    ),
    diagnostics: {
      signalMatches: plan.signalMatches ?? [],
      limitedByAvailability,
      healthAdjusted,
      requirementFiltered: requestHasSelectionRequirements(plan.request),
      competitiveCandidateCount: countCompetitiveCandidates(plan.candidates),
      runnerUp,
      confidence,
    },
  };
}
