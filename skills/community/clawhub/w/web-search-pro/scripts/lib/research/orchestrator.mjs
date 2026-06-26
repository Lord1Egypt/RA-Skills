import { analyzeResearchEvidence } from "./findings.mjs";
import { normalizeResearchEvidence } from "./evidence-normalize.mjs";
import { buildResearchGapFillPlan } from "./gap-fill.mjs";
import { buildResearchOutput } from "./output.mjs";
import { buildResearchPlan } from "./plan.mjs";
import { executeResearchTask } from "./retrieval.mjs";

function buildGapResolutionSummary({
  gapPlan,
  followupExecutions = [],
  initialUncertainties = [],
  finalUncertainties = [],
}) {
  if (!gapPlan.attempted) {
    return {
      attempted: false,
      triggeredBy: [],
      followupTasksPlanned: 0,
      followupTasksExecuted: 0,
      resolvedUncertaintyIds: [],
      remainingUncertaintyIds: [],
    };
  }

  const initialIds = new Set(initialUncertainties.map((entry) => entry.id));
  const finalIds = new Set(finalUncertainties.map((entry) => entry.id));
  const resolvedUncertaintyIds = Array.from(initialIds).filter((id) => !finalIds.has(id));

  return {
    attempted: true,
    triggeredBy: gapPlan.triggeredBy,
    followupTasksPlanned: gapPlan.followupTasks.length,
    followupTasksExecuted: followupExecutions.length,
    resolvedUncertaintyIds,
    remainingUncertaintyIds: Array.from(finalIds),
  };
}

export async function runResearch(request, options = {}) {
  const plan = buildResearchPlan(request);
  if (options.planOnly) {
    return buildResearchOutput({
      request,
      plan,
      claimClusters: [],
      gapResolutionSummary: {
        attempted: false,
        triggeredBy: [],
        followupTasksPlanned: 0,
        followupTasksExecuted: 0,
        resolvedUncertaintyIds: [],
        remainingUncertaintyIds: [],
      },
      subquestionBriefs: [],
      planOnly: true,
    });
  }

  const context = {
    cwd: options.cwd ?? process.cwd(),
    env: options.env ?? process.env,
    config: options.config,
    now: options.now ?? (() => Date.now()),
  };
  const executeTask = options.executeTask ?? executeResearchTask;
  const taskExecutions = [];

  for (const task of plan.tasks) {
    const execution = await executeTask(task, context);
    taskExecutions.push(execution);
  }

  let evidence = normalizeResearchEvidence(taskExecutions, {
    retrievedAt: context.now(),
    recentInformationPreferred: request.constraints?.recentInformationPreferred,
  });
  let analysis = analyzeResearchEvidence({
    request,
    subquestions: plan.subquestions,
    evidence,
  });
  const initialUncertainties = analysis.uncertainties;
  const gapPlan = buildResearchGapFillPlan({
    request,
    plan,
    analysis,
    taskExecutions,
  });
  const followupExecutions = [];

  for (const task of gapPlan.followupTasks) {
    const execution = await executeTask(task, context);
    followupExecutions.push(execution);
    taskExecutions.push(execution);
  }

  if (followupExecutions.length > 0) {
    evidence = normalizeResearchEvidence(taskExecutions, {
      retrievedAt: context.now(),
      recentInformationPreferred: request.constraints?.recentInformationPreferred,
    });
    analysis = analyzeResearchEvidence({
      request,
      subquestions: plan.subquestions,
      evidence,
    });
  }

  const effectivePlan =
    gapPlan.followupTasks.length > 0
      ? {
          ...plan,
          tasks: [...plan.tasks, ...gapPlan.followupTasks],
        }
      : plan;
  const gapResolutionSummary = buildGapResolutionSummary({
    gapPlan,
    followupExecutions,
    initialUncertainties,
    finalUncertainties: analysis.uncertainties,
  });

  return buildResearchOutput({
    request,
    plan: effectivePlan,
    claimClusters: analysis.claimClusters,
    evidence,
    candidateFindings: analysis.candidateFindings,
    subquestionBriefs: analysis.subquestionBriefs,
    uncertainties: analysis.uncertainties,
    citations: analysis.citations,
    taskExecutions,
    gapResolutionSummary,
    planOnly: false,
  });
}
