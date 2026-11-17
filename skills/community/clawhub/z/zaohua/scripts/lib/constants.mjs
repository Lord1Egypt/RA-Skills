export const FORGE_NAME = "AISoul Forge";
export const FORGE_VERSION = "0.2.0";
export const SOUL6_VERSION = "1.0.0";
export const EVALUATOR_VERSION = "0.1.0";
export const SOUL6_URL = "https://aisoulhub.io/about/review-metrics#soul6";

export const RUNTIME_FILES = Object.freeze([
  "IDENTITY.md",
  "USER.md",
  "SOUL.md",
  "AGENTS.md",
  "TOOLS.md",
  "MEMORY.md",
]);

export const DIMENSION_KEYS = Object.freeze([
  "personalityIntegrity",
  "behaviorExecutability",
  "styleConsistency",
  "relationBoundaries",
  "safetyEthicsInternalization",
  "lifecycleEvolution",
]);

export const CANONICAL_WEIGHTS = Object.freeze({
  personalityIntegrity: 0.22,
  behaviorExecutability: 0.18,
  styleConsistency: 0.16,
  relationBoundaries: 0.16,
  safetyEthicsInternalization: 0.18,
  lifecycleEvolution: 0.10,
});

export const DIMENSION_LABELS = Object.freeze({
  personalityIntegrity: "Selfhood / Personality Integrity",
  behaviorExecutability: "Operability / Behavior Executability",
  styleConsistency: "Unity / Style Consistency",
  relationBoundaries: "Limits / Relationship and Capability Boundaries",
  safetyEthicsInternalization: "Safeguards / Safety and Ethics Internalization",
  lifecycleEvolution: "Lifecycle / Long-Term Evolvability",
});

export const STANDARD_REFERENCE = Object.freeze({
  name: "SOUL-6",
  version: SOUL6_VERSION,
  profile: "canonical",
  source: "AISoulHub.io",
  url: SOUL6_URL,
});
