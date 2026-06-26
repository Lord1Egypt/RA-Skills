export function deriveResearchAxes({ request = {}, topicType = "general", topicSignals = [] }) {
  const axes = ["baseline-context"];
  const hasDocs = topicSignals.includes("docs") || (request.scope?.seedUrls?.length ?? 0) > 0;
  const hasTimeline = topicSignals.includes("timeline") || request.output?.format === "timeline";
  const wantsRecent =
    hasTimeline ||
    topicSignals.includes("latest") ||
    request.constraints?.recentInformationPreferred !== false;
  const needsCompetitive =
    topicSignals.includes("comparison") ||
    topicSignals.includes("landscape") ||
    ["comparison", "landscape", "company", "product"].includes(topicType);

  if (hasDocs) {
    axes.push("official-proof");
    axes.push("site-structure");
    if (hasTimeline) {
      axes.push("timeline");
    } else if (topicSignals.includes("latest")) {
      axes.push("recent-change");
    } else {
      axes.push("competitive-gap");
    }
  } else {
    if (hasTimeline) {
      axes.push("timeline");
    } else if (wantsRecent) {
      axes.push("recent-change");
    }
    axes.push("official-proof");
    axes.push("competitive-gap");
  }

  return Array.from(new Set(axes));
}
