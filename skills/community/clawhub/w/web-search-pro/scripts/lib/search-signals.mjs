const SIGNAL_SPECS = Object.freeze([
  {
    id: "direct-answer.question",
    category: "direct-answer",
    label: "Question-style query favors cited direct answers",
    weight: 140,
    match(query) {
      return (
        /\?$/.test(query) ||
        /^(who|what|when|where|why|how|is|are|can|should|could|would|do|does|did)\b/.test(query)
      );
    },
    providerDeltas: {
      perplexity: 140,
      querit: 120,
      you: 60,
    },
  },
  {
    id: "direct-answer.current-change",
    category: "direct-answer",
    label: "Current-change question favors answer-first current-information providers",
    weight: 180,
    match(query) {
      return /\b(what changed|changed?|recently|current status|current state|status)\b/.test(
        query,
      );
    },
    providerDeltas: {
      perplexity: 180,
      you: 140,
      querit: 60,
      serper: 40,
    },
  },
  {
    id: "freshness.latest",
    category: "freshness",
    label: "Freshness-oriented query favors current-information providers",
    weight: 130,
    match(query) {
      return /\b(latest|current|recent|recently|today|update|updates|breaking|new)\b/.test(
        query,
      );
    },
    providerDeltas: {
      you: 130,
      serper: 80,
      brave: 70,
      querit: 70,
      searxng: 20,
    },
  },
  {
    id: "freshness.summary",
    category: "freshness",
    label: "Summary-oriented query favors LLM-ready search providers",
    weight: 120,
    match(query) {
      return /\b(summarize|summarise|summary|overview|brief|key points?)\b/.test(query);
    },
    providerDeltas: {
      you: 120,
      querit: 60,
      perplexity: 40,
    },
  },
  {
    id: "privacy.private-search",
    category: "privacy",
    label: "Privacy-oriented query favors private search providers",
    weight: 220,
    match(query) {
      return /\b(private|privacy|tracking|anonymous|metasearch|meta search|self-hosted|self hosted|searxng)\b/.test(
        query,
      );
    },
    providerDeltas: {
      searxng: 220,
      brave: 80,
      ddg: 60,
    },
  },
  {
    id: "comparison.compare",
    category: "comparison",
    label: "Comparison-style query favors research-oriented providers",
    weight: 90,
    match(query) {
      return /\b(compare|comparison|versus|vs\.?|benchmark|trade-?offs?|alternatives?)\b/.test(
        query,
      );
    },
    providerDeltas: {
      exa: 90,
      tavily: 70,
      querit: 50,
    },
  },
  {
    id: "discovery.list",
    category: "discovery",
    label: "Discovery query favors broad result coverage",
    weight: 70,
    match(query) {
      return /\b(best|top|tools|tooling|examples|ideas|list|recommend|recommendations?)\b/.test(
        query,
      );
    },
    providerDeltas: {
      brave: 70,
      serper: 60,
      querit: 60,
      you: 40,
    },
  },
  {
    id: "multilingual.non-latin",
    category: "multilingual",
    label: "Non-Latin query suggests multilingual search coverage",
    weight: 240,
    match(query) {
      return /[^\u0000-\u007f]/.test(query) || /\b(multilingual|translation|translate)\b/.test(query);
    },
    providerDeltas: {
      querit: 240,
      serpapi: 100,
      brave: 60,
      you: 40,
    },
  },
]);

const PRESET_SIGNAL_SPECS = Object.freeze({
  general: null,
  code: {
    id: "preset.code",
    category: "code",
    label: "Code preset favors documentation and implementation coverage",
    providerDeltas: {
      exa: 140,
      brave: 50,
      querit: 30,
      serper: 20,
    },
  },
  company: {
    id: "preset.company",
    category: "company",
    label: "Company preset favors entity and business-information coverage",
    providerDeltas: {
      brave: 80,
      serper: 70,
      you: 50,
      querit: 40,
    },
  },
  docs: {
    id: "preset.docs",
    category: "docs",
    label: "Docs preset favors reference and official-source coverage",
    providerDeltas: {
      exa: 120,
      brave: 50,
      serpapi: 30,
      you: 20,
    },
  },
  research: {
    id: "preset.research",
    category: "research",
    label: "Research preset favors breadth, comparison, and synthesis-friendly providers",
    providerDeltas: {
      exa: 90,
      tavily: 80,
      querit: 60,
      brave: 30,
    },
  },
});

function normalizeQuery(query) {
  return String(query ?? "").trim().toLowerCase();
}

export function analyzeSearchSignals(request) {
  const query = normalizeQuery(request.query);
  const matchedSignals = query
    ? SIGNAL_SPECS.flatMap((spec) => {
        if (!spec.match(query, request)) {
          return [];
        }
        return [
          {
            id: spec.id,
            category: spec.category,
            label: spec.label,
            weight: spec.weight,
            evidence: request.query,
            providerDeltas: { ...spec.providerDeltas },
          },
        ];
      })
    : [];

  const preset = PRESET_SIGNAL_SPECS[request.intentPreset ?? "general"] ?? null;
  if (!preset) {
    return matchedSignals;
  }

  return [
    ...matchedSignals,
    {
      id: preset.id,
      category: preset.category,
      label: preset.label,
      weight: 100,
      evidence: request.intentPreset,
      providerDeltas: { ...preset.providerDeltas },
    },
  ];
}

export function requestHasSelectionRequirements(request) {
  return Boolean(
    request.deep ||
      request.news ||
      request.days !== null ||
      request.timeRange ||
      request.fromDate ||
      request.toDate ||
      request.searchEngine ||
      request.country ||
      request.lang,
  );
}

export const requestHasStrictSearchRequirements = requestHasSelectionRequirements;
