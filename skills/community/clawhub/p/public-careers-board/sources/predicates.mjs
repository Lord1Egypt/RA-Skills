// Role selection for the Magnite example in Firecrawl issue 3552.
// None of these readings is selected. A reading that needs a model stays unknown.
// This module does not fetch and does not change coverage.roleFilter.

const EXACT_PHRASE = "account executive advertising solutions engineer";
const ACCOUNT_EXECUTIVE = "account executive";
const SOLUTIONS_ENGINEER = "advertising solutions engineer";
const CONTENT_WORDS = ["account", "executive", "advertising", "solutions", "engineer"];

export function normalizeTitle(title) {
  return String(title ?? "").toLowerCase().replace(/\s+/g, " ").trim();
}

export function titleWords(title) {
  return normalizeTitle(title).split(/[^a-z0-9]+/).filter(Boolean);
}

export const PREDICATE_DEFINITIONS = [
  {
    id: "exact_unpunctuated_phrase",
    reading: "The issue text names one title, with no slash and no extra words.",
    match(title) {
      return normalizeTitle(title) === EXACT_PHRASE;
    },
  },
  {
    id: "either_exact_title",
    reading: "The contract slash names two exact titles: Account Executive, or Advertising Solutions Engineer.",
    match(title) {
      return normalizeTitle(title) === ACCOUNT_EXECUTIVE || normalizeTitle(title) === SOLUTIONS_ENGINEER;
    },
  },
  {
    id: "either_phrase_contained",
    reading: "The slash names two phrases. A longer title matches when it contains either phrase.",
    match(title) {
      const normalized = normalizeTitle(title);
      return normalized.includes(ACCOUNT_EXECUTIVE) || normalized.includes(SOLUTIONS_ENGINEER);
    },
  },
  {
    id: "both_phrases_contained",
    reading: "One title has to contain both phrases.",
    match(title) {
      const normalized = normalizeTitle(title);
      return normalized.includes(ACCOUNT_EXECUTIVE) && normalized.includes(SOLUTIONS_ENGINEER);
    },
  },
  {
    id: "all_content_words",
    reading: "Each content word in the issue sentence appears as a whole word in the title.",
    match(title) {
      const words = new Set(titleWords(title));
      return CONTENT_WORDS.every((word) => words.has(word));
    },
  },
];

export const UNKNOWN_INTERPRETATIONS = [
  {
    id: "semantic_role_family",
    status: "unknown",
    applied: false,
    reason: "Calling a title an account-executive role or an advertising-solutions-engineer role without an exact phrase needs a model or a company taxonomy. That reading is not applied.",
  },
  {
    id: "department_inference",
    status: "unknown",
    applied: false,
    reason: "The Workday list schema used here is title, locationsText, and externalPath. It has no department field. A department reading is unknown.",
  },
];

function rowView(row) {
  return { title: row.title, location: row.location ?? null, url: row.url };
}

export function applyPredicates(rows) {
  const list = Array.isArray(rows) ? rows : [];
  const alternatives = PREDICATE_DEFINITIONS.map((definition) => {
    const matches = list.filter((row) => definition.match(row?.title)).map(rowView);
    return {
      id: definition.id,
      reading: definition.reading,
      matchCount: matches.length,
      matches,
    };
  });
  return {
    appliedPredicate: null,
    method: "casefold_exact_no_model",
    casefold: "String.toLowerCase with whitespace collapsed; whole words split on non-alphanumeric characters",
    employmentDecision: false,
    alternatives,
    unknown: UNKNOWN_INTERPRETATIONS,
  };
}
