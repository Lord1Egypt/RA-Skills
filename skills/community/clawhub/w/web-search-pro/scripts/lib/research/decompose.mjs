import { selectResearchQuestionBlueprints } from "./question-templates.mjs";
import { deriveResearchAxes } from "./research-axes.mjs";
import { classifyResearchTopic } from "./topic-classifier.mjs";
import { detectResearchTopicSignals } from "./topic-signals.mjs";

function defaultPlannedActions(intent) {
  if (intent === "site-structure") {
    return ["search", "map"];
  }
  if (intent === "official-sources") {
    return ["search", "extract"];
  }
  if (intent === "timeline") {
    return ["search"];
  }
  return ["search"];
}

export function decomposeResearchRequest(request, options = {}) {
  const topicSignals = options.topicSignals ?? detectResearchTopicSignals(request);
  const topicType = options.topicType ?? classifyResearchTopic(request.topic, request);
  const researchAxes =
    options.researchAxes ?? deriveResearchAxes({ request, topicType, topicSignals });
  const maxQuestions = request.budgets.maxQuestions;
  const blueprints = selectResearchQuestionBlueprints(request, topicType, researchAxes);

  return blueprints.slice(0, maxQuestions).map((blueprint, index) => ({
    id: `sq-${index + 1}`,
    question: blueprint.question(request.topic),
    intent: blueprint.intent,
    priority: index + 1,
    why: blueprint.why,
    researchAxis: blueprint.researchAxis,
    evidenceGoal: blueprint.evidenceGoal,
    plannedActions: [...defaultPlannedActions(blueprint.intent)],
  }));
}
