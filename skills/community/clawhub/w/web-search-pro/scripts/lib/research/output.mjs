import { SCHEMA_VERSION } from "../output.mjs";

function buildFallbackSubquestionBriefs({
  subquestions = [],
  candidateFindings = [],
  uncertainties = [],
  evidence = [],
}) {
  return subquestions.map((subquestion) => {
    const findings = candidateFindings.filter((entry) =>
      entry.subquestionIds?.includes(subquestion.id),
    );
    const relatedUncertainties = uncertainties.filter(
      (entry) => entry.subquestionId === subquestion.id,
    );
    const topEvidenceIds = Array.from(
      new Set(
        findings.flatMap((entry) => entry.evidenceIds ?? []).concat(
          evidence
            .filter((entry) => entry.subquestionId === subquestion.id)
            .map((entry) => entry.id),
        ),
      ),
    ).slice(0, 5);

    return {
      subquestionId: subquestion.id,
      supportedFacts: findings
        .filter((entry) => entry.status !== "conflicted")
        .map((entry) => entry.statement)
        .slice(0, 3),
      conflicts: relatedUncertainties
        .filter((entry) => entry.type === "source-conflict")
        .map((entry) => entry.description),
      missing: relatedUncertainties
        .filter((entry) => entry.type !== "source-conflict")
        .map((entry) => entry.description),
      topEvidenceIds,
    };
  });
}

export function buildResearchOutput({
  request,
  plan,
  claimClusters = [],
  evidence = [],
  candidateFindings = [],
  subquestionBriefs = [],
  uncertainties = [],
  citations = [],
  taskExecutions = [],
  gapResolutionSummary = null,
  planOnly = false,
}) {
  const executionTaskStatus = new Map(
    taskExecutions.map((entry) => [entry.task.id, entry.task.status]),
  );
  const tasks = plan.tasks.map((task) => ({
    ...task,
    status: executionTaskStatus.get(task.id) ?? task.status,
  }));
  const taskCounts = tasks.reduce(
    (counts, entry) => {
      counts[entry.status] = (counts[entry.status] ?? 0) + 1;
      return counts;
    },
    { planned: 0, completed: 0, failed: 0, skipped: 0 },
  );

  const providersUsed = Array.from(
    new Set(
      taskExecutions
        .flatMap((entry) => entry.providersUsed ?? [])
        .filter(Boolean),
    ),
  );

  const primitivesPlanned = Array.from(new Set(plan.tasks.map((task) => task.kind)));

  return {
    schemaVersion: SCHEMA_VERSION,
    command: "research",
    topic: request.topic,
    topicType: plan.topicType,
    topicSignals: plan.topicSignals ?? [],
    researchAxes: plan.researchAxes ?? [],
    objective: request.objective,
    subquestions: plan.subquestions,
    tasks,
    claimClusters,
    evidence,
    candidateFindings,
    subquestionBriefs:
      planOnly || subquestionBriefs.length > 0
        ? subquestionBriefs
        : buildFallbackSubquestionBriefs({
            subquestions: plan.subquestions,
            candidateFindings,
            uncertainties,
            evidence,
          }),
    uncertainties,
    citations,
    gapResolutionSummary: gapResolutionSummary ?? {
      attempted: false,
      triggeredBy: [],
      followupTasksPlanned: 0,
      followupTasksExecuted: 0,
      resolvedUncertaintyIds: [],
      remainingUncertaintyIds: [],
    },
    execution: {
      planOnly,
      primitivesPlanned,
      taskCounts,
      providersUsed,
      federationUsed: taskExecutions.some((entry) => entry.federated === true),
      renderAllowed: request.budgets.allowRender,
      budgetLimits: {
        maxQuestions: request.budgets.maxQuestions,
        maxSearches: request.budgets.maxSearches,
        maxExtracts: request.budgets.maxExtracts,
        maxCrawlPages: request.budgets.maxCrawlPages,
      },
      budgetReached: {
        maxQuestions: plan.subquestions.length >= request.budgets.maxQuestions,
        maxSearches:
          plan.tasks.filter((entry) => entry.kind === "search").length >= request.budgets.maxSearches,
        maxExtracts:
          plan.tasks.filter((entry) => entry.kind === "extract").length >= request.budgets.maxExtracts,
      },
    },
    meta: {
      planOnly,
      format: request.output.format,
      language: request.output.language,
    },
  };
}

export function formatResearchMarkdown(payload) {
  const lines = [];
  lines.push(`# Research Pack: ${payload.topic}`);
  lines.push("");
  lines.push(`- Topic type: ${payload.topicType}`);
  lines.push(`- Topic signals: ${payload.topicSignals.join(", ") || "none"}`);
  lines.push(`- Research axes: ${payload.researchAxes.join(", ") || "none"}`);
  lines.push(`- Objective: ${payload.objective}`);
  lines.push(`- Plan only: ${payload.meta.planOnly ? "yes" : "no"}`);
  lines.push(`- Planned primitives: ${payload.execution.primitivesPlanned.join(", ") || "none"}`);
  lines.push("");

  lines.push("## Subquestions");
  lines.push("");
  for (const subquestion of payload.subquestions) {
    lines.push(`- ${subquestion.id}: ${subquestion.question}`);
  }
  lines.push("");

  if (payload.candidateFindings.length > 0) {
    lines.push("## Candidate Findings");
    lines.push("");
    for (const finding of payload.candidateFindings) {
      lines.push(`- ${finding.statement}`);
    }
    lines.push("");
  }

  if (payload.subquestionBriefs.length > 0) {
    lines.push("## Subquestion Briefs");
    lines.push("");
    for (const brief of payload.subquestionBriefs) {
      lines.push(`- ${brief.subquestionId}: ${brief.supportedFacts[0] ?? "No supported fact yet."}`);
    }
    lines.push("");
  }

  if (payload.claimClusters.length > 0) {
    lines.push("## Claim Clusters");
    lines.push("");
    for (const cluster of payload.claimClusters) {
      lines.push(`- ${cluster.id}: ${cluster.statement}`);
    }
    lines.push("");
  }

  if (payload.uncertainties.length > 0) {
    lines.push("## Uncertainties");
    lines.push("");
    for (const uncertainty of payload.uncertainties) {
      lines.push(`- ${uncertainty.type}: ${uncertainty.description}`);
    }
  }

  if (payload.gapResolutionSummary.attempted) {
    lines.push("");
    lines.push("## Gap Resolution");
    lines.push("");
    lines.push(`- Triggered by: ${payload.gapResolutionSummary.triggeredBy.join(", ") || "none"}`);
    lines.push(`- Follow-up tasks planned: ${payload.gapResolutionSummary.followupTasksPlanned}`);
    lines.push(`- Follow-up tasks executed: ${payload.gapResolutionSummary.followupTasksExecuted}`);
  }

  return lines.join("\n");
}
