const AXIS_BLUEPRINTS = Object.freeze({
  "baseline-context": {
    intent: "overview",
    evidenceGoal: "comparison-signal",
    question: (topic, topicType) =>
      topicType === "docs"
        ? `What is the current structure and baseline context for ${topic}?`
        : `What is the current landscape and baseline context for ${topic}?`,
    why: (topicType) =>
      topicType === "docs"
        ? "Establishes the documentation baseline before extracting or mapping sources."
        : "Establishes the shared baseline before comparing providers, sources, or changes.",
  },
  "recent-change": {
    intent: "latest",
    evidenceGoal: "recent-change",
    question: (topic) => `What recent developments, changes, or updates matter for ${topic}?`,
    why: () => "Surfaces recent movement so downstream models do not reason over stale assumptions.",
  },
  "official-proof": {
    intent: "official-sources",
    evidenceGoal: "official-proof",
    question: (topic) => `What official or primary sources best document ${topic}?`,
    why: (topicType) =>
      topicType === "docs"
        ? "Anchors the pack in primary documentation rather than only commentary."
        : "Anchors the pack in primary evidence rather than only secondary commentary.",
  },
  "site-structure": {
    intent: "site-structure",
    evidenceGoal: "structure-map",
    question: (topic) => `What site structure or documentation topology is relevant to ${topic}?`,
    why: () => "Helps the agent decide whether a site map or crawl is needed before deeper extraction.",
  },
  "competitive-gap": {
    intent: "comparison",
    evidenceGoal: "comparison-signal",
    question: (topic, topicType) =>
      topicType === "docs"
        ? `What notable gaps, overlaps, or tradeoffs exist across documentation sources for ${topic}?`
        : `What meaningful comparisons, disagreements, or tradeoffs appear across sources about ${topic}?`,
    why: (topicType) =>
      topicType === "docs"
        ? "Surfaces structure and source differences across the documentation surface."
        : "Highlights disagreement and tradeoffs instead of collapsing everything into one answer.",
  },
  timeline: {
    intent: "timeline",
    evidenceGoal: "timeline-proof",
    question: (topic) => `What release, version, or milestone timeline matters for ${topic}?`,
    why: () => "Focuses the pack on chronology rather than only static descriptions.",
  },
});

export function selectResearchQuestionBlueprints(request, topicType, researchAxes = []) {
  if (researchAxes.length === 0) {
    const fallbackAxes = topicNeedsTimelineIntent(request, topicType)
      ? ["baseline-context", "timeline", "official-proof", "competitive-gap"]
      : topicType === "docs"
        ? ["baseline-context", "official-proof", "site-structure", "competitive-gap"]
        : ["baseline-context", "recent-change", "official-proof", "competitive-gap"];
    return fallbackAxes.map((axis) => {
      const blueprint = AXIS_BLUEPRINTS[axis];
      return {
        researchAxis: axis,
        intent: blueprint.intent,
        evidenceGoal: blueprint.evidenceGoal,
        question: (topic) => blueprint.question(topic, topicType),
        why: blueprint.why(topicType),
      };
    });
  }

  return researchAxes.map((axis) => {
    const blueprint = AXIS_BLUEPRINTS[axis];
    return {
      researchAxis: axis,
      intent: blueprint.intent,
      evidenceGoal: blueprint.evidenceGoal,
      question: (topic) => blueprint.question(topic, topicType),
      why: blueprint.why(topicType),
    };
  });
}

export function buildResearchSearchQuery(topic, intent, topicType) {
  if (intent === "overview") {
    if (topicType === "docs") {
      return `${topic} documentation overview`;
    }
    if (topicType === "landscape") {
      return `${topic} ecosystem overview`;
    }
    return topic;
  }
  if (intent === "latest") {
    return `${topic} latest updates`;
  }
  if (intent === "official-sources") {
    return `${topic} official documentation primary sources`;
  }
  if (intent === "comparison") {
    return `${topic} comparison tradeoffs differences`;
  }
  if (intent === "site-structure") {
    return `${topic} documentation sitemap structure`;
  }
  if (intent === "timeline") {
    return `${topic} release timeline version history`;
  }
  return topic;
}
