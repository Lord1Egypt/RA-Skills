const VALID_OUTPUT_FORMATS = new Set(["pack", "brief", "comparison", "timeline", "dossier"]);
const VALID_OUTPUT_LANGUAGES = new Set(["match-input", "en", "zh", "de", "fr", "ja"]);

function trimString(value, fallback = "") {
  const normalized = String(value ?? fallback).trim();
  return normalized;
}

function normalizeStringList(values = []) {
  if (!Array.isArray(values)) {
    return [];
  }
  return Array.from(
    new Set(
      values
        .map((value) => trimString(value))
        .filter(Boolean),
    ),
  );
}

function normalizeUrlList(values = []) {
  return normalizeStringList(values).map((value) => {
    try {
      return new URL(value).toString();
    } catch {
      return value;
    }
  });
}

function requirePositiveInteger(value, fieldName, minimum) {
  if (!Number.isInteger(value) || value < minimum) {
    throw new Error(`${fieldName} must be an integer >= ${minimum}`);
  }
  return value;
}

function requireBoolean(value, fieldName) {
  if (typeof value !== "boolean") {
    throw new Error(`${fieldName} must be true or false`);
  }
  return value;
}

export function normalizeResearchRequest(input = {}) {
  const topic = trimString(input.topic);
  if (!topic) {
    throw new Error("research.topic must be a non-empty string");
  }

  const request = {
    topic,
    objective: trimString(input.objective, "structured research pack") || "structured research pack",
    scope: {
      includeDomains: normalizeStringList(input.scope?.includeDomains),
      excludeDomains: normalizeStringList(input.scope?.excludeDomains),
      seedUrls: normalizeUrlList(input.scope?.seedUrls),
      fromDate: input.scope?.fromDate ?? null,
      toDate: input.scope?.toDate ?? null,
    },
    constraints: {
      officialSourcesPreferred: input.constraints?.officialSourcesPreferred ?? true,
      recentInformationPreferred: input.constraints?.recentInformationPreferred ?? true,
      language: trimString(input.constraints?.language) || null,
    },
    budgets: {
      maxQuestions: input.budgets?.maxQuestions ?? 4,
      maxSearches: input.budgets?.maxSearches ?? 8,
      maxExtracts: input.budgets?.maxExtracts ?? 6,
      maxCrawlPages: input.budgets?.maxCrawlPages ?? 12,
      allowFederation: input.budgets?.allowFederation ?? true,
      allowCrawl: input.budgets?.allowCrawl ?? true,
      allowRender: input.budgets?.allowRender ?? false,
    },
    output: {
      format: trimString(input.output?.format, "pack") || "pack",
      language: trimString(input.output?.language, "match-input") || "match-input",
    },
  };

  request.budgets.maxQuestions = requirePositiveInteger(
    request.budgets.maxQuestions,
    "research.budgets.maxQuestions",
    1,
  );
  request.budgets.maxSearches = requirePositiveInteger(
    request.budgets.maxSearches,
    "research.budgets.maxSearches",
    0,
  );
  request.budgets.maxExtracts = requirePositiveInteger(
    request.budgets.maxExtracts,
    "research.budgets.maxExtracts",
    0,
  );
  request.budgets.maxCrawlPages = requirePositiveInteger(
    request.budgets.maxCrawlPages,
    "research.budgets.maxCrawlPages",
    0,
  );
  request.budgets.allowFederation = requireBoolean(
    request.budgets.allowFederation,
    "research.budgets.allowFederation",
  );
  request.budgets.allowCrawl = requireBoolean(
    request.budgets.allowCrawl,
    "research.budgets.allowCrawl",
  );
  request.budgets.allowRender = requireBoolean(
    request.budgets.allowRender,
    "research.budgets.allowRender",
  );

  if (!VALID_OUTPUT_FORMATS.has(request.output.format)) {
    throw new Error(
      `research.output.format must be one of: ${Array.from(VALID_OUTPUT_FORMATS).join(", ")}`,
    );
  }
  if (!VALID_OUTPUT_LANGUAGES.has(request.output.language)) {
    throw new Error(
      `research.output.language must be one of: ${Array.from(VALID_OUTPUT_LANGUAGES).join(", ")}`,
    );
  }

  return request;
}
