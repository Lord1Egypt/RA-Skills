// =============================================================================
// modes/glowUp.ts — Mode 2: Glow Up My Text
//
// Takes a weak or mediocre message and rewrites it in three intensity tiers:
// subtle / confident / bold. Returns the original score alongside the rewrites
// so the user can see the before/after delta.
// =============================================================================

import Anthropic from "@anthropic-ai/sdk";
import type { GlowUpInput, GlowUpResult, GlowUpTiers } from "../types.js";
import { checkInput, checkOutput } from "../core/safety.js";
import { heuristicScore } from "../core/scorer.js";
import { buildGlowUpPrompt, SYSTEM_PROMPT } from "../core/prompts.js";
import { rateMyRizz, SafetyError } from "./rateMyRizz.js";

const client = new Anthropic();

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Rewrites a message in three intensity tiers and scores the original.
 *
 * @param input  Original message + optional context
 * @returns      GlowUpResult with original score and three rewrites
 */
export async function glowUp(input: GlowUpInput): Promise<GlowUpResult> {
  const { message, context } = input;

  // ------------------------------------------------------------------
  // 1. Safety check
  // ------------------------------------------------------------------
  const safety = checkInput(message + (context ?? ""));
  if (!safety.safe) {
    throw new SafetyError(safety.message ?? "Safety check failed.");
  }

  // ------------------------------------------------------------------
  // 2. Score the original message (run in parallel with the glow-up call)
  // ------------------------------------------------------------------
  const [originalScore, tiers] = await Promise.all([
    rateMyRizz({ message, context })
      .then((r) => r.score)
      .catch(() => heuristicScore(message)), // fallback if rate fails
    generateTiers(message, context),
  ]);

  return {
    original: message,
    tiers,
    originalScore,
  };
}

// ---------------------------------------------------------------------------
// Tier generation
// ---------------------------------------------------------------------------

/**
 * Calls Claude to generate the three rewritten message tiers.
 * Falls back to a rule-based placeholder if the API is unavailable.
 */
async function generateTiers(
  message: string,
  context?: string
): Promise<GlowUpTiers> {
  const prompt = buildGlowUpPrompt(message, context);

  let rawJson: string;
  try {
    const response = await client.messages.create({
      model: "claude-opus-4-5",
      max_tokens: 512,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: prompt }],
    });
    rawJson = extractText(response.content);
  } catch {
    console.warn("[glowUp] LLM unavailable, using fallback tiers.");
    return fallbackTiers(message);
  }

  // Parse LLM response
  let parsed: Partial<GlowUpTiers>;
  try {
    parsed = JSON.parse(rawJson) as Partial<GlowUpTiers>;
  } catch {
    console.warn("[glowUp] Could not parse LLM response, using fallback.");
    return fallbackTiers(message);
  }

  // Safety check on generated text
  const allText = `${parsed.subtle ?? ""} ${parsed.confident ?? ""} ${parsed.bold ?? ""}`;
  const outputSafety = checkOutput(allText);
  if (!outputSafety.safe) {
    console.warn("[glowUp] LLM output failed safety check, using fallback.");
    return fallbackTiers(message);
  }

  return {
    subtle:    parsed.subtle    ?? fallbackTier(message, "subtle"),
    confident: parsed.confident ?? fallbackTier(message, "confident"),
    bold:      parsed.bold      ?? fallbackTier(message, "bold"),
  };
}

// ---------------------------------------------------------------------------
// Fallback tier generator (no LLM)
// ---------------------------------------------------------------------------

/**
 * Simple rule-based fallback when the LLM is unavailable.
 * Not as good as the real thing, but keeps the app functional.
 */
function fallbackTiers(message: string): GlowUpTiers {
  return {
    subtle:    fallbackTier(message, "subtle"),
    confident: fallbackTier(message, "confident"),
    bold:      fallbackTier(message, "bold"),
  };
}

function fallbackTier(
  message: string,
  tier: "subtle" | "confident" | "bold"
): string {
  const base = message.replace(/[?.!]+$/, "").trim();

  switch (tier) {
    case "subtle":
      return `${base} — what do you think?`;
    case "confident":
      return `${base}. Let's make it happen.`;
    case "bold":
      return `${base}. Non-negotiable. (okay maybe a little negotiable)`;
  }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function extractText(content: Anthropic.ContentBlock[]): string {
  return content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text.trim())
    .join("");
}
