// =============================================================================
// modes/rateMyRizz.ts — Mode 1: Rate My Rizz
//
// Evaluates a user's flirting message across 5 dimensions (0–20 each)
// and returns a structured RizzScore with grade, title, and callouts.
// =============================================================================

import Anthropic from "@anthropic-ai/sdk";
import type { RateMyRizzInput, RateMyRizzResult, RizzDimensions } from "../types.js";
import { checkInput, checkOutput, detectsRejection } from "../core/safety.js";
import { buildScore, heuristicScore } from "../core/scorer.js";
import { buildRatePrompt, SYSTEM_PROMPT } from "../core/prompts.js";

const client = new Anthropic();

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Rates a flirting message and returns a full RizzScore.
 *
 * @param input  The message to evaluate + optional context
 * @returns      RateMyRizzResult with structured score, or throws on safety block
 */
export async function rateMyRizz(
  input: RateMyRizzInput
): Promise<RateMyRizzResult> {
  const { message, context } = input;

  // ------------------------------------------------------------------
  // 1. Safety check on input
  // ------------------------------------------------------------------
  const inputSafety = checkInput(message + (context ?? ""));
  if (!inputSafety.safe) {
    throw new SafetyError(inputSafety.message ?? "Safety check failed.");
  }

  // ------------------------------------------------------------------
  // 2. Special case: if context reveals a clear rejection, give
  //    respectful-move-on advice rather than scoring tactics
  // ------------------------------------------------------------------
  if (context && detectsRejection(context)) {
    return buildRejectionResult(input);
  }

  // ------------------------------------------------------------------
  // 3. Call Claude to score the message
  // ------------------------------------------------------------------
  const prompt = buildRatePrompt(message, context);

  let rawJson: string;
  try {
    const response = await client.messages.create({
      model: "claude-opus-4-5",
      max_tokens: 512,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: prompt }],
    });

    rawJson = extractText(response.content);
  } catch (err) {
    // Fallback: use heuristic scoring if the API is unavailable
    console.warn("[rateMyRizz] LLM unavailable, falling back to heuristic scorer.");
    return { input, score: heuristicScore(message) };
  }

  // ------------------------------------------------------------------
  // 4. Parse and validate the LLM response
  // ------------------------------------------------------------------
  let parsed: LLMScoreResponse;
  try {
    parsed = JSON.parse(rawJson) as LLMScoreResponse;
  } catch {
    // LLM returned non-JSON — fall back gracefully
    console.warn("[rateMyRizz] Could not parse LLM response, using heuristic fallback.");
    return { input, score: heuristicScore(message) };
  }

  // ------------------------------------------------------------------
  // 5. Safety check on LLM output before returning
  // ------------------------------------------------------------------
  const outputText = `${parsed.bestMove ?? ""} ${parsed.weakSpot ?? ""}`;
  const outputSafety = checkOutput(outputText);
  if (!outputSafety.safe) {
    // Silently fall back — don't expose the unsafe output
    return { input, score: heuristicScore(message) };
  }

  // ------------------------------------------------------------------
  // 6. Build and return the RizzScore
  // ------------------------------------------------------------------
  const dimensions: Partial<RizzDimensions> = {
    confidence: parsed.confidence,
    wit:        parsed.wit,
    warmth:     parsed.warmth,
    clarity:    parsed.clarity,
    vibeMatch:  parsed.vibeMatch,
  };

  const score = buildScore(
    dimensions,
    parsed.bestMove ?? "",
    parsed.weakSpot ?? ""
  );

  return { input, score };
}

// ---------------------------------------------------------------------------
// Rejection result builder
// ---------------------------------------------------------------------------

/**
 * Returns a special result when context indicates the person has rejected the user.
 * Score is neutral; coaching focuses on graceful exit.
 */
function buildRejectionResult(input: RateMyRizzInput): RateMyRizzResult {
  return {
    input,
    score: buildScore(
      { confidence: 0, wit: 0, warmth: 0, clarity: 0, vibeMatch: 0 },
      "Respecting someone's answer is genuinely the most attractive thing you can do.",
      "When someone says no, the move is to thank them for their honesty and move on with grace."
    ),
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Extracts plain text from Anthropic SDK content blocks */
function extractText(content: Anthropic.ContentBlock[]): string {
  return content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text.trim())
    .join("");
}

/** Expected shape of the LLM's JSON response */
interface LLMScoreResponse {
  confidence?: number;
  wit?: number;
  warmth?: number;
  clarity?: number;
  vibeMatch?: number;
  bestMove?: string;
  weakSpot?: string;
}

// ---------------------------------------------------------------------------
// Safety error (used to bubble up safety blocks to the CLI)
// ---------------------------------------------------------------------------

export class SafetyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "SafetyError";
  }
}
