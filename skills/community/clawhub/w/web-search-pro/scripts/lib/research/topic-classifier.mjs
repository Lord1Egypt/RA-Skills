import {
  detectResearchTopicSignals,
  inferPrimaryResearchTopicType,
  topicSignalsNeedTimeline,
} from "./topic-signals.mjs";

export function classifyResearchTopic(topic, request = {}) {
  const topicSignals = detectResearchTopicSignals({
    topic,
    output: request.output,
  });
  return inferPrimaryResearchTopicType(topicSignals);
}

export function topicNeedsTimelineIntent(request, topicType) {
  if (topicType !== "latest" && request.output?.format !== "timeline") {
    return false;
  }
  return topicSignalsNeedTimeline(
    detectResearchTopicSignals(request),
    request.output?.format,
  );
}
