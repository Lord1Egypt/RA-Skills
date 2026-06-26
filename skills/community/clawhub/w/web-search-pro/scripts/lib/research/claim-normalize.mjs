const SYNONYM_RULES = Object.freeze([
  [/\bdocs?\b/g, "documentation"],
  [/\bmanuals?\b/g, "documentation"],
  [/\breferences?\b/g, "documentation"],
  [/\bguides?\b/g, "documentation"],
  [/\bupdates?\b/g, "release"],
  [/\bupgrades?\b/g, "release"],
  [/\breleases?\b/g, "release"],
  [/\bchangelog\b/g, "release"],
  [/\bversions?\b/g, "version"],
  [/\bproviders?\b/g, "provider"],
]);

const NEGATION_RULES = Object.freeze([
  [/\bdoes not\b/g, " not "],
  [/\bdo not\b/g, " not "],
  [/\bdid not\b/g, " not "],
  [/\bis not\b/g, " not "],
  [/\baren't\b/g, " not "],
  [/\bisn't\b/g, " not "],
  [/\bcan't\b/g, " not "],
  [/\bcannot\b/g, " not "],
  [/\bwithout\b/g, " not "],
  [/\bnever\b/g, " not "],
  [/\bno\b/g, " not "],
  [/\blacks?\b/g, " not "],
]);

export function normalizeClaimText(value = "") {
  let normalized = String(value ?? "").toLowerCase().trim();
  if (!normalized) {
    return "";
  }

  normalized = normalized.replace(/\bv(\d+(?:\.\d+)+)\b/g, "version $1");
  for (const [pattern, replacement] of NEGATION_RULES) {
    normalized = normalized.replace(pattern, replacement);
  }
  for (const [pattern, replacement] of SYNONYM_RULES) {
    normalized = normalized.replace(pattern, replacement);
  }

  normalized = normalized
    .replace(/[^a-z0-9%.\s-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  return normalized;
}

export function extractClaimFacts(value = "") {
  const text = String(value ?? "");
  if (!text.trim()) {
    return [];
  }
  const matches = text.match(/v\d+(?:\.\d+)+|\d+(?:\.\d+)?%|\d{4}-\d{1,2}-\d{1,2}|\b\d+(?:\.\d+)?\b/gi);
  if (!matches) {
    return [];
  }
  return Array.from(new Set(matches.map((entry) => entry.toLowerCase())));
}

export function buildNormalizedClaimKey(value = "") {
  const normalizedText = normalizeClaimText(value);
  const facts = extractClaimFacts(value);
  if (!normalizedText) {
    return facts.length > 0 ? `facts:${facts.join("|")}` : "";
  }
  return facts.length > 0
    ? `${normalizedText}__facts:${facts.join("|")}`
    : normalizedText;
}
