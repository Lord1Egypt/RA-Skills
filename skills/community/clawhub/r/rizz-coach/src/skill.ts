// =============================================================================
// skill.ts — OpenClaw / ClawHub skill adapter
//
// This is the thin integration layer for the OpenClaw / ClawHub platform.
// It maps incoming SkillInput payloads to the appropriate mode handlers
// and returns a standardised SkillOutput.
//
// All actual logic lives in src/modes/ — this file is pure routing.
// =============================================================================

import type {
  SkillInput,
  SkillOutput,
  SkillMode,
  RateMyRizzInput,
  GlowUpInput,
  ReplyGeneratorInput,
  ConversationSimInput,
  ShareCardInput,
  SimState,
} from "./types.js";

import { rateMyRizz, SafetyError } from "./modes/rateMyRizz.js";
import { glowUp } from "./modes/glowUp.js";
import { generateReplies } from "./modes/replyGenerator.js";
import { sendSimMessage, createSimSession } from "./modes/conversationSim.js";
import { generateShareCard } from "./shareCard/cardGenerator.js";

import {
  formatRateMyRizz,
  formatGlowUp,
  formatReplyGenerator,
  formatSimState,
  formatSafetyBlock,
} from "./core/formatter.js";

// ---------------------------------------------------------------------------
// Skill handler — main export for OpenClaw / ClawHub
// ---------------------------------------------------------------------------

/**
 * Primary entry point for the ClawHub skill runtime.
 * Receives a typed SkillInput, routes to the correct mode, and returns SkillOutput.
 *
 * @param input  Parsed skill invocation payload
 */
export async function handleSkill(input: SkillInput): Promise<SkillOutput> {
  try {
    switch (input.mode) {
      case "rate":
        return await handleRate(input.payload);

      case "glowup":
        return await handleGlowUp(input.payload);

      case "reply":
        return await handleReply(input.payload);

      case "sim":
        return await handleSim(input.payload);

      case "share":
        return await handleShare(input.payload);

      default:
        return errorOutput(input.mode, `Unknown mode: "${input.mode as string}"`);
    }
  } catch (err) {
    if (err instanceof SafetyError) {
      return {
        success: false,
        mode: input.mode,
        safetyBlocked: true,
        result: { message: err.message, display: formatSafetyBlock(err.message) },
      };
    }
    const message = err instanceof Error ? err.message : "An unexpected error occurred.";
    return errorOutput(input.mode, message);
  }
}

// ---------------------------------------------------------------------------
// Mode handlers
// ---------------------------------------------------------------------------

/** Mode 1: Rate My Rizz */
async function handleRate(payload: Record<string, unknown>): Promise<SkillOutput> {
  const rateInput: RateMyRizzInput = {
    message: assertString(payload.message, "message"),
    context: optionalString(payload.context),
  };

  const result = await rateMyRizz(rateInput);

  return {
    success: true,
    mode: "rate",
    result: {
      ...result,
      display: formatRateMyRizz(result), // Pre-rendered text for the platform to display
    },
  };
}

/** Mode 2: Glow Up My Text */
async function handleGlowUp(payload: Record<string, unknown>): Promise<SkillOutput> {
  const glowUpInput: GlowUpInput = {
    message: assertString(payload.message, "message"),
    context: optionalString(payload.context),
  };

  const result = await glowUp(glowUpInput);

  return {
    success: true,
    mode: "glowup",
    result: {
      ...result,
      display: formatGlowUp(result),
    },
  };
}

/** Mode 3: Reply Generator */
async function handleReply(payload: Record<string, unknown>): Promise<SkillOutput> {
  const replyInput: ReplyGeneratorInput = {
    theirMessage: assertString(payload.theirMessage, "theirMessage"),
    context:      optionalString(payload.context),
    // preferredVibes is optional — let generateReplies use its defaults
  };

  const result = await generateReplies(replyInput);

  return {
    success: true,
    mode: "reply",
    result: {
      ...result,
      display: formatReplyGenerator(result),
    },
  };
}

/** Mode 4: Conversation Simulator */
async function handleSim(payload: Record<string, unknown>): Promise<SkillOutput> {
  // The platform sends either an existing state or signals a new session
  const userMessage = assertString(payload.userMessage, "userMessage");

  // Allow the platform to pass in an existing session state (serialised as JSON)
  const existingState = payload.state as SimState | undefined;
  const personaName = optionalString(payload.personaName);

  const state: SimState = existingState ?? createSimSession(personaName);

  const simInput: ConversationSimInput = { userMessage, state };
  const result = await sendSimMessage(simInput);

  return {
    success: true,
    mode: "sim",
    result: {
      ...result,
      display: formatSimState(result.updatedState, result.feedback),
    },
  };
}

/** Mode 5: Share Card */
async function handleShare(payload: Record<string, unknown>): Promise<SkillOutput> {
  // Share card is synchronous — no LLM call needed
  const shareInput: ShareCardInput = {
    mode:     assertShareMode(payload.sourceMode),
    headline: optionalString(payload.headline),
    subtitle: optionalString(payload.subtitle),
    // score is optional — platform may pass it from a prior rate result
    score:    payload.score as ShareCardInput["score"] | undefined,
  };

  const result = generateShareCard(shareInput);

  return {
    success: true,
    mode: "share",
    result: {
      ...result,
      display: result.card,
    },
  };
}

// ---------------------------------------------------------------------------
// Input validation helpers
// ---------------------------------------------------------------------------

function assertString(value: unknown, fieldName: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`Missing required field: "${fieldName}" must be a non-empty string.`);
  }
  return value.trim();
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() !== ""
    ? value.trim()
    : undefined;
}

function assertShareMode(value: unknown): ShareCardInput["mode"] {
  const valid: ShareCardInput["mode"][] = ["rate", "glowup", "reply", "sim"];
  if (typeof value === "string" && valid.includes(value as ShareCardInput["mode"])) {
    return value as ShareCardInput["mode"];
  }
  return "rate"; // Sensible default
}

function errorOutput(mode: SkillMode, message: string): SkillOutput {
  return { success: false, mode, error: message };
}
