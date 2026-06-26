import { buildResearchSearchQuery } from "./question-templates.mjs";
import {
  buildResearchExtractTask,
  buildResearchMapTask,
  buildResearchSearchTask,
} from "./task-builders.mjs";

const FOLLOWUP_PRIORITY = Object.freeze({
  high: 3,
  medium: 2,
  low: 1,
});

function countTasksByKind(tasks = []) {
  return tasks.reduce((acc, task) => {
    acc[task.kind] = (acc[task.kind] ?? 0) + 1;
    return acc;
  }, {});
}

function uniqueTasks(tasks = []) {
  const seen = new Set();
  const output = [];
  for (const task of tasks) {
    const key = task.id ?? taskSignature(task);
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    output.push(task);
  }
  return output;
}

function taskSignature(task) {
  return JSON.stringify({
    kind: task.kind,
    subquestionId: task.subquestionId,
    query: task.query ?? null,
    urls: [...(task.urls ?? [])].sort(),
    phase: task.phase ?? "primary",
  });
}

function prioritizeUncertainties(uncertainties = []) {
  return [...uncertainties]
    .filter((entry) => entry.followupEligible === true)
    .sort((left, right) => {
      const priorityDiff =
        (FOLLOWUP_PRIORITY[right.priority] ?? 0) - (FOLLOWUP_PRIORITY[left.priority] ?? 0);
      if (priorityDiff !== 0) {
        return priorityDiff;
      }
      return left.id.localeCompare(right.id);
    });
}

function remainingBudget(request, tasksByKind, kind) {
  if (kind === "search") {
    return Math.max(0, request.budgets.maxSearches - (tasksByKind.search ?? 0));
  }
  if (kind === "extract") {
    return Math.max(0, request.budgets.maxExtracts - (tasksByKind.extract ?? 0));
  }
  return Number.POSITIVE_INFINITY;
}

function pushTaskIfAllowed(task, followupTasks, seenSignatures, tasksByKind) {
  if (!task) {
    return false;
  }
  const signature = taskSignature(task);
  if (seenSignatures.has(signature)) {
    return false;
  }
  seenSignatures.add(signature);
  followupTasks.push(task);
  tasksByKind[task.kind] = (tasksByKind[task.kind] ?? 0) + 1;
  return true;
}

function buildFollowupTasksForUncertainty({
  request,
  plan,
  uncertainty,
  subquestion,
  sequence,
  tasksByKind,
  followupTasks,
  seenSignatures,
}) {
  const nextTasks = [];
  const nextId = () => `task-followup-${sequence.value++}`;

  if (uncertainty.type === "insufficient-official-sources") {
    if (remainingBudget(request, tasksByKind, "search") > 0) {
      nextTasks.push(
        buildResearchSearchTask({
          id: nextId(),
          subquestion,
          request,
          topicType: plan.topicType,
          query: buildResearchSearchQuery(request.topic, "official-sources", plan.topicType),
          reason: "Follow up with a constrained official-source search for a missing primary source.",
          phase: "followup",
          includeDomains: request.scope.includeDomains.length > 0
            ? request.scope.includeDomains
            : request.scope.seedUrls.map((url) => {
                try {
                  return new URL(url).hostname;
                } catch {
                  return null;
                }
              }).filter(Boolean),
          followupEligible: false,
        }),
      );
    }
    if (
      request.scope.seedUrls.length > 0 &&
      remainingBudget(request, tasksByKind, "extract") > 0
    ) {
      nextTasks.push(
        buildResearchExtractTask({
          id: nextId(),
          subquestion,
          request,
          urls: request.scope.seedUrls.slice(0, 1),
          reason: "Follow up by extracting a seed URL as a primary source candidate.",
          phase: "followup",
          followupEligible: false,
        }),
      );
    }
  } else if (uncertainty.type === "stale-information") {
    if (remainingBudget(request, tasksByKind, "search") > 0) {
      nextTasks.push(
        buildResearchSearchTask({
          id: nextId(),
          subquestion,
          request,
          topicType: plan.topicType,
          query: buildResearchSearchQuery(
            request.topic,
            subquestion.intent === "timeline" ? "timeline" : "latest",
            plan.topicType,
          ),
          reason: "Follow up with a recent-search pass because the current evidence is stale.",
          phase: "followup",
          timeRange: "year",
          followupEligible: false,
        }),
      );
    }
  } else if (uncertainty.type === "missing-evidence") {
    if (
      ["site-structure"].includes(subquestion.intent) &&
      request.scope.seedUrls.length > 0
    ) {
      nextTasks.push(
        buildResearchMapTask({
          id: nextId(),
          subquestion,
          request,
          urls: request.scope.seedUrls.slice(0, 1),
          reason: "Follow up with a site map because the structure subquestion is still empty.",
          phase: "followup",
          followupEligible: false,
        }),
      );
      if (remainingBudget(request, tasksByKind, "extract") > 0) {
        nextTasks.push(
          buildResearchExtractTask({
            id: nextId(),
            subquestion,
            request,
            urls: request.scope.seedUrls.slice(0, 1),
            reason: "Follow up with a seed extraction because the structure research needs more evidence.",
            phase: "followup",
            followupEligible: false,
          }),
        );
      }
    } else if (remainingBudget(request, tasksByKind, "search") > 0) {
      nextTasks.push(
        buildResearchSearchTask({
          id: nextId(),
          subquestion,
          request,
          topicType: plan.topicType,
          reason: "Follow up with another targeted search because this subquestion still has no evidence.",
          phase: "followup",
          followupEligible: false,
        }),
      );
    }
  }

  for (const task of nextTasks) {
    if (followupTasks.length >= 2) {
      break;
    }
    pushTaskIfAllowed(task, followupTasks, seenSignatures, tasksByKind);
  }
}

export function buildResearchGapFillPlan({
  request,
  plan,
  analysis,
  taskExecutions = [],
}) {
  const prioritized = prioritizeUncertainties(analysis.uncertainties ?? []);
  if (prioritized.length === 0) {
    return {
      attempted: false,
      triggeredBy: [],
      followupTasks: [],
    };
  }

  const knownTasks = uniqueTasks([
    ...(plan.tasks ?? []),
    ...taskExecutions.map((entry) => entry.task),
  ]);
  const tasksByKind = countTasksByKind(knownTasks);
  const seenSignatures = new Set(
    knownTasks.map((task) => taskSignature(task)),
  );
  const subquestions = new Map((plan.subquestions ?? []).map((entry) => [entry.id, entry]));
  const followupTasks = [];
  const sequence = { value: 1 };

  for (const uncertainty of prioritized) {
    if (followupTasks.length >= 2) {
      break;
    }
    const subquestion = subquestions.get(uncertainty.subquestionId);
    if (!subquestion) {
      continue;
    }
    buildFollowupTasksForUncertainty({
      request,
      plan,
      uncertainty,
      subquestion,
      sequence,
      tasksByKind,
      followupTasks,
      seenSignatures,
    });
  }

  return {
    attempted: true,
    triggeredBy: Array.from(new Set(prioritized.map((entry) => entry.type))),
    followupTasks,
  };
}
