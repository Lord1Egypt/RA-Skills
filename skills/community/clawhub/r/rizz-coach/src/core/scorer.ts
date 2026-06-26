// =============================================================================
// core/scorer.ts — Rubric-based rizz scoring model
//
// Scoring is deterministic via heuristic rules + LLM analysis.
// The LLM provides dimension scores and callouts; this module validates,
// normalises and enriches that data into a clean RizzScore object.
// =============================================================================

import type { RizzScore, RizzGrade, RizzDimensions } from "../types.js";

// ---------------------------------------------------------------------------
// Grade + Title lookup table
// ---------------------------------------------------------------------------

interface GradeTier {
  minScore: number;
  grade: RizzGrade;
  title: string;
}

const GRADE_TIERS: GradeTier[] = [
  { minScore: 90, grade: "S", title: "Certified Rizz God" },
  { minScore: 75, grade: "A", title: "Main Character Energy" },
  { minScore: 60, grade: "B", title: "Solid Game" },
  { minScore: 45, grade: "C", title: "Room to Grow" },
  { minScore: 30, grade: "D", title: "Needs Work" },
  { minScore: 0,  grade: "F", title: "Rizz Emergency" },
];

// ---------------------------------------------------------------------------
// Dimension names (used for display and validation)
// ---------------------------------------------------------------------------

export const DIMENSION_KEYS: (keyof RizzDimensions)[] = [
  "confidence",
  "wit",
  "warmth",
  "clarity",
  "vibeMatch",
];

export const DIMENSION_LABELS: Record<keyof RizzDimensions, string> = {
  confidence: "Confidence",
  wit:        "Wit",
  warmth:     "Warmth",
  clarity:    "Clarity",
  vibeMatch:  "Vibe Match",
};

// ---------------------------------------------------------------------------
// Score construction
// Takes raw dimension scores (0–20 each) from the LLM and builds RizzScore.
// ---------------------------------------------------------------------------

/**
 * Builds a complete RizzScore from LLM-supplied dimension scores and callouts.
 * Clamps all values to valid ranges to defend against LLM hallucination.
 */
export function buildScore(
  rawDimensions: Partial<RizzDimensions>,
  bestMove: string,
  weakSpot: string
): RizzScore {
  // Clamp each dimension to 0–20
  const dimensions: RizzDimensions = {
    confidence: clamp(rawDimensions.confidence ?? 10, 0, 20),
    wit:        clamp(rawDimensions.wit ?? 10, 0, 20),
    warmth:     clamp(rawDimensions.warmth ?? 10, 0, 20),
    clarity:    clamp(rawDimensions.clarity ?? 10, 0, 20),
    vibeMatch:  clamp(rawDimensions.vibeMatch ?? 10, 0, 20),
  };

  const total = clamp(
    dimensions.confidence +
    dimensions.wit +
    dimensions.warmth +
    dimensions.clarity +
    dimensions.vibeMatch,
    0,
    100
  );

  const { grade, title } = getGradeInfo(total);

  return {
    total,
    grade,
    title,
    dimensions,
    bestMove: bestMove.trim() || "You showed up — that's step one.",
    weakSpot: weakSpot.trim() || "Hard to pin down — keep experimenting.",
  };
}

// ---------------------------------------------------------------------------
// Grade resolution
// ---------------------------------------------------------------------------

/** Returns grade and title for a given 0–100 score */
export function getGradeInfo(score: number): { grade: RizzGrade; title: string } {
  for (const tier of GRADE_TIERS) {
    if (score >= tier.minScore) {
      return { grade: tier.grade, title: tier.title };
    }
  }
  // Fallback (should never hit)
  return { grade: "F", title: "Rizz Emergency" };
}

// ---------------------------------------------------------------------------
// Heuristic quick-score (no LLM needed)
// Used as a fast fallback or for unit testing. Returns rough dimension scores
// based on simple text features.
// ---------------------------------------------------------------------------

/**
 * Generates a heuristic RizzScore without calling the LLM.
 * Useful for testing, fallback, or very short inputs.
 */
export function heuristicScore(message: string): RizzScore {
  const text = message.trim();
  const wordCount = text.split(/\s+/).length;
  const hasQuestion = /\?/.test(text);
  const hasEmoji = /\p{Emoji}/u.test(text);
  const isJustHey = /^h+e+y+\s*[!.?]*$/i.test(text);
  const hasSpecificDetail = wordCount > 8;
  const endsAbruptly = /\b(idk|lol|lmao|haha|anyway)\s*\.?\s*$/i.test(text);
  const isAllLower = text === text.toLowerCase() && wordCount > 3;

  const dims: RizzDimensions = {
    // Confidence: short/vague = low, specific ask = high
    confidence: isJustHey ? 3 : hasSpecificDetail ? 14 : 8,

    // Wit: emojis and longer messages suggest more effort
    wit: hasEmoji && wordCount > 5 ? 13 : wordCount > 12 ? 12 : 7,

    // Warmth: question shows genuine interest; abrupt ending hurts
    warmth: hasQuestion ? 14 : endsAbruptly ? 6 : 10,

    // Clarity: a clear question is clear; trailing off = not clear
    clarity: hasQuestion && !endsAbruptly ? 15 : isJustHey ? 4 : 9,

    // Vibe match: we can't fully assess without context, give neutral
    vibeMatch: isAllLower && wordCount > 3 ? 11 : 10,
  };

  const bestMove = hasQuestion
    ? "Asking a question shows you're genuinely curious — good."
    : hasSpecificDetail
    ? "Including specific details shows you're paying attention."
    : "You sent something — that's braver than most.";

  const weakSpot = isJustHey
    ? '"Hey" by itself doesn\'t give them much to work with.'
    : endsAbruptly
    ? "The ending trails off — try landing with a question or a clear vibe."
    : !hasQuestion
    ? "No question means the ball stays in your court — give them an easy way to reply."
    : "Could push a little harder on your unique angle.";

  return buildScore(dims, bestMove, weakSpot);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(Math.round(value), min), max);
}
