const SIGNAL_SPECS = Object.freeze([
  {
    id: "docs",
    pattern: /\b(?:docs?|documentation|reference|guide|manual|api|sdk|schema|sitemap|structure)\b/i,
  },
  {
    id: "company",
    pattern: /\b(?:company|business|funding|ceo|revenue|headquarters|hq|team|market cap)\b/i,
  },
  {
    id: "product",
    pattern: /\b(?:product|feature(?:s)?|pricing|launch|service|tool|app|platform)\b/i,
  },
  {
    id: "latest",
    pattern: /\b(?:latest|recent|new|updates?|release(?:s| history)?|roadmap|changelog|version(?:s| history)?)\b/i,
  },
  {
    id: "comparison",
    pattern: /\b(?:vs|versus|compare|comparison|tradeoffs?|alternatives?|competitive)\b/i,
  },
  {
    id: "landscape",
    pattern: /\b(?:landscape|ecosystem|market|competitors?|vendors?|skills?|platforms?)\b/i,
  },
]);

const TIMELINE_PATTERN =
  /\b(?:timeline|release(?: history)?|version(?:s| history)?|milestone(?:s)?|chronology|changelog)\b/i;

function normalizeInput(input = {}) {
  if (typeof input === "string") {
    return {
      topic: input,
      output: {
        format: "pack",
      },
    };
  }
  return {
    topic: String(input.topic ?? ""),
    output: {
      format: String(input.output?.format ?? "pack"),
    },
  };
}

export function detectResearchTopicSignals(input = {}) {
  const request = normalizeInput(input);
  const topic = request.topic.trim();
  if (!topic) {
    return [];
  }

  const signals = [];
  for (const spec of SIGNAL_SPECS) {
    if (spec.pattern.test(topic)) {
      signals.push(spec.id);
    }
  }

  if (request.output.format === "timeline" || TIMELINE_PATTERN.test(topic)) {
    if (!signals.includes("latest")) {
      signals.push("latest");
    }
    signals.push("timeline");
  }

  return Array.from(new Set(signals));
}

export function inferPrimaryResearchTopicType(topicSignals = []) {
  const priority = ["docs", "comparison", "latest", "company", "product", "landscape"];
  for (const signal of priority) {
    if (topicSignals.includes(signal)) {
      return signal;
    }
  }
  return "general";
}

export function topicSignalsNeedTimeline(topicSignals = [], outputFormat = "pack") {
  return outputFormat === "timeline" || topicSignals.includes("timeline");
}
