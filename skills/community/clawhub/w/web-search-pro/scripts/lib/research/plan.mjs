import { decomposeResearchRequest } from "./decompose.mjs";
import { deriveResearchAxes } from "./research-axes.mjs";
import {
  buildResearchCrawlTask,
  buildResearchExtractTask,
  buildResearchMapTask,
  buildResearchSearchTask,
} from "./task-builders.mjs";
import { classifyResearchTopic } from "./topic-classifier.mjs";
import { detectResearchTopicSignals } from "./topic-signals.mjs";

export function buildResearchPlan(request) {
  const topicSignals = detectResearchTopicSignals(request);
  const topicType = classifyResearchTopic(request.topic, request);
  const researchAxes = deriveResearchAxes({ request, topicType, topicSignals });
  const subquestions = decomposeResearchRequest(request, {
    topicType,
    topicSignals,
    researchAxes,
  });
  const tasks = [];
  let sequence = 1;
  let searchCount = 0;
  let extractCount = 0;

  for (const subquestion of subquestions) {
    if (searchCount < request.budgets.maxSearches) {
      tasks.push(
        buildResearchSearchTask({
          id: `task-${sequence++}`,
          subquestion,
          request,
          topicType,
        }),
      );
      searchCount += 1;
    }
  }

  if (request.scope.seedUrls.length > 0) {
    const officialSubquestion =
      subquestions.find((entry) => entry.intent === "official-sources") ?? subquestions[0];
    const structureSubquestion =
      subquestions.find((entry) => entry.intent === "site-structure") ??
      subquestions.find((entry) => entry.intent === "overview") ??
      subquestions[0];

    if (extractCount < request.budgets.maxExtracts) {
      tasks.push(
        buildResearchExtractTask({
          id: `task-${sequence++}`,
          subquestion: officialSubquestion,
          request,
        }),
      );
      extractCount += 1;
    }

    tasks.push(
      buildResearchMapTask({
        id: `task-${sequence++}`,
        subquestion: structureSubquestion,
        request,
      }),
    );

    if (request.budgets.allowCrawl && request.output.format === "dossier") {
      tasks.push(
        buildResearchCrawlTask({
          id: `task-${sequence++}`,
          subquestion: structureSubquestion,
          request,
        }),
      );
    }
  }

  const plannedActionsBySubquestion = new Map(subquestions.map((entry) => [entry.id, new Set()]));
  for (const task of tasks) {
    plannedActionsBySubquestion.get(task.subquestionId)?.add(task.kind);
  }

  const finalizedSubquestions = subquestions.map((entry) => ({
    ...entry,
    plannedActions: Array.from(plannedActionsBySubquestion.get(entry.id) ?? []),
  }));

  return {
    request,
    topicType,
    topicSignals,
    researchAxes,
    subquestions: finalizedSubquestions,
    tasks,
    execution: {
      maxSearches: request.budgets.maxSearches,
      maxExtracts: request.budgets.maxExtracts,
      maxCrawlPages: request.budgets.maxCrawlPages,
      allowFederation: request.budgets.allowFederation,
      allowCrawl: request.budgets.allowCrawl,
      allowRender: request.budgets.allowRender,
    },
  };
}
