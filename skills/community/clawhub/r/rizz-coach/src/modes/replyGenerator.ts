// =============================================================================
// modes/replyGenerator.ts — Mode 3: Reply Generator
//
// Given a message the user received, generates 3 reply options across
// different vibes (playful, confident, chill, etc.) with risk level labels.
// =============================================================================

import Anthropic from "@anthropic-ai/sdk";
import type {
  ReplyGeneratorInput,
  ReplyGeneratorResult,
  ReplyOption,
  ReplyVibe,
} from "../types.js";
import { checkInput, checkOutput } from "../core/safety.js";
import { buildReplyPrompt, SYSTEM_PROMPT } from "../core/prompts.js";
import { SafetyError } from "./rateMyRizz.js";

const client = new Anthropic();

// Default vibes if the user doesn't specify
const DEFAULT_VIBES: ReplyVibe[] = ["playful", "confident", "chill"];

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Generates reply options for a received message.
 *
 * @param input  The received message + optional context and vibe preferences
 * @returns      ReplyGeneratorResult with an array of ReplyOption
 */
export async function generateReplies(
  input: ReplyGeneratorInput
): Promise<ReplyGeneratorResult> {
  const { theirMessage, context, preferredVibes } = input;

  // ------------------------------------------------------------------
  // 1. Safety check on the received message + context
  // ------------------------------------------------------------------
  const safety = checkInput(theirMessage + (context ?? ""));
  if (!safety.safe) {
    throw new SafetyError(safety.message ?? "Safety check failed.");
  }

  // ------------------------------------------------------------------
  // 2. Generate replies via Claude
  // ------------------------------------------------------------------
  const vibes = preferredVibes && preferredVibes.length > 0
    ? preferredVibes
    : DEFAULT_VIBES;

  const replies = await generateReplyOptions(theirMessage, vibes, context);

  return {
    theirMessage,
    replies,
  };
}

// ---------------------------------------------------------------------------
// Reply generation
// ---------------------------------------------------------------------------

/**
 * Calls Claude to generate reply options and validates the response.
 * Falls back to safe placeholder replies if the LLM is unavailable.
 */
async function generateReplyOptions(
  theirMessage: string,
  vibes: ReplyVibe[],
  context?: string
): Promise<ReplyOption[]> {
  const prompt = buildReplyPrompt(theirMessage, context, vibes);

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
    console.warn("[replyGenerator] LLM unavailable, using fallback replies.");
    return fallbackReplies(vibes);
  }

  // Parse response
  let parsed: { replies?: RawReplyOption[] };
  try {
    parsed = JSON.parse(rawJson) as { replies?: RawReplyOption[] };
  } catch {
    console.warn("[replyGenerator] Could not parse LLM response.");
    return fallbackReplies(vibes);
  }

  if (!Array.isArray(parsed.replies) || parsed.replies.length === 0) {
    return fallbackReplies(vibes);
  }

  // Validate and sanitize each reply
  const validated: ReplyOption[] = [];
  for (const raw of parsed.replies) {
    if (!raw.vibe || !raw.text) continue;

    // Safety check on generated text
    const outputSafety = checkOutput(raw.text);
    if (!outputSafety.safe) continue;

    validated.push({
      vibe: sanitiseVibe(raw.vibe),
      text: raw.text.trim(),
      riskLevel: sanitiseRisk(raw.riskLevel),
    });
  }

  // If safety filtering killed all replies, fall back
  if (validated.length === 0) {
    return fallbackReplies(vibes);
  }

  return validated;
}

// ---------------------------------------------------------------------------
// Fallback replies (no LLM)
// ---------------------------------------------------------------------------

function fallbackReplies(vibes: ReplyVibe[]): ReplyOption[] {
  const templates: Record<ReplyVibe, Omit<ReplyOption, "vibe">> = {
    playful:   { text: "haha okay okay, I see you 😄",         riskLevel: "safe" },
    confident: { text: "That tracks. So when are we doing this?", riskLevel: "medium" },
    chill:     { text: "no pressure, just thinking out loud",   riskLevel: "safe" },
    romantic:  { text: "honestly you make it easy to say yes",  riskLevel: "medium" },
    witty:     { text: "I was going to play it cool but... yeah", riskLevel: "safe" },
  };

  return vibes.map((vibe) => ({
    vibe,
    ...(templates[vibe] ?? { text: "sounds good to me", riskLevel: "safe" as const }),
  }));
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

const VALID_VIBES = new Set<ReplyVibe>(["playful", "confident", "chill", "romantic", "witty"]);
const VALID_RISKS = new Set<ReplyOption["riskLevel"]>(["safe", "medium", "spicy"]);

function sanitiseVibe(v: unknown): ReplyVibe {
  if (typeof v === "string" && VALID_VIBES.has(v as ReplyVibe)) {
    return v as ReplyVibe;
  }
  return "chill";
}

function sanitiseRisk(r: unknown): ReplyOption["riskLevel"] {
  if (typeof r === "string" && VALID_RISKS.has(r as ReplyOption["riskLevel"])) {
    return r as ReplyOption["riskLevel"];
  }
  return "safe";
}

/** Raw shape from LLM before validation */
interface RawReplyOption {
  vibe?: unknown;
  text?: string;
  riskLevel?: unknown;
}
