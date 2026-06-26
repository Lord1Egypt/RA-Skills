// =============================================================================
// modes/conversationSim.ts — Mode 4: Conversation Simulator
//
// Lets the user practice a back-and-forth with a simulated persona.
// Tracks a running momentum score and delivers optional coaching tips.
// The persona's warmth and responses evolve based on user message quality.
// =============================================================================

import Anthropic from "@anthropic-ai/sdk";
import type {
  ConversationSimInput,
  ConversationSimResult,
  SimPersona,
  SimState,
} from "../types.js";
import { checkInput, checkOutput } from "../core/safety.js";
import { buildSimPersonaPrompt, momentumLabel, SYSTEM_PROMPT } from "../core/prompts.js";
import { SafetyError } from "./rateMyRizz.js";

const client = new Anthropic();

// ---------------------------------------------------------------------------
// Built-in persona roster
// ---------------------------------------------------------------------------

export const PERSONAS: SimPersona[] = [
  {
    name: "Alex",
    archetype: "Witty & Slightly Guarded",
    description:
      "Alex is quick with a comeback and appreciates clever messages. " +
      "They're friendly but don't open up immediately — you have to earn warmth. " +
      "They'll call out anything generic or low-effort without being mean about it.",
    warmthLevel: 2,
  },
  {
    name: "Jordan",
    archetype: "Warm & Playfully Sarcastic",
    description:
      "Jordan is genuinely warm and easy to talk to, but uses light sarcasm as a love language. " +
      "They respond well to humor and genuine curiosity. " +
      "They get bored quickly if you're too formal or too vague.",
    warmthLevel: 3,
  },
  {
    name: "Sam",
    archetype: "Low-key & Hard to Read",
    description:
      "Sam gives short replies by default and doesn't make things easy. " +
      "Not rude — just economical with words. " +
      "If you say something genuinely interesting, they'll open up, but bland messages get one-word replies.",
    warmthLevel: 1,
  },
];

// ---------------------------------------------------------------------------
// Session factory — creates a fresh SimState
// ---------------------------------------------------------------------------

/**
 * Creates a brand-new simulation session.
 *
 * @param personaName  Name of a persona from PERSONAS (defaults to "Alex")
 */
export function createSimSession(personaName?: string): SimState {
  const persona =
    PERSONAS.find((p) => p.name.toLowerCase() === personaName?.toLowerCase()) ??
    PERSONAS[0];

  return {
    persona,
    turns: [],
    currentScore: 50, // Start at neutral
    momentum: "steady",
    sessionOver: false,
  };
}

// ---------------------------------------------------------------------------
// Main entry point — process one user turn
// ---------------------------------------------------------------------------

/**
 * Sends the user's message to the simulated persona and returns the response.
 * Also updates the SimState with the new turns, score, and momentum.
 *
 * @param input  Current sim state + the user's latest message
 */
export async function sendSimMessage(
  input: ConversationSimInput
): Promise<ConversationSimResult> {
  const { userMessage, state } = input;

  // ------------------------------------------------------------------
  // Guard: session already over
  // ------------------------------------------------------------------
  if (state.sessionOver) {
    return {
      personaReply: "(session ended)",
      updatedState: state,
    };
  }

  // ------------------------------------------------------------------
  // 1. Safety check on user message
  // ------------------------------------------------------------------
  const safety = checkInput(userMessage);
  if (!safety.safe) {
    throw new SafetyError(safety.message ?? "Safety check failed.");
  }

  // ------------------------------------------------------------------
  // 2. Add user turn to state
  // ------------------------------------------------------------------
  const stateWithUserTurn: SimState = {
    ...state,
    turns: [
      ...state.turns,
      { speaker: "user", message: userMessage },
    ],
  };

  // ------------------------------------------------------------------
  // 3. Call Claude to get persona reply + momentum delta
  // ------------------------------------------------------------------
  const prompt = buildSimPersonaPrompt(
    state.persona,
    stateWithUserTurn.turns,
    userMessage
  );

  let personaReply: string;
  let momentumDelta = 0;
  let coachingTip: string | undefined;

  try {
    const response = await client.messages.create({
      model: "claude-opus-4-5",
      max_tokens: 512,
      system: SYSTEM_PROMPT,
      messages: [{ role: "user", content: prompt }],
    });

    const raw = extractText(response.content);
    const parsed = parseSimResponse(raw);

    personaReply = parsed.reply;
    momentumDelta = parsed.momentumDelta ?? 0;
    coachingTip = parsed.coachingTip ?? undefined;
  } catch {
    console.warn("[conversationSim] LLM unavailable, using fallback reply.");
    personaReply = fallbackPersonaReply(state.persona, userMessage);
  }

  // ------------------------------------------------------------------
  // 4. Safety check on persona reply
  // ------------------------------------------------------------------
  const outputSafety = checkOutput(personaReply);
  if (!outputSafety.safe) {
    personaReply = "...I don't know what to say to that.";
  }

  // ------------------------------------------------------------------
  // 5. Update state
  // ------------------------------------------------------------------
  const newScore = clamp(state.currentScore + momentumDelta * 3, 0, 100);
  const newTurns = [
    ...stateWithUserTurn.turns,
    { speaker: "persona" as const, message: personaReply, momentumDelta },
  ];

  // Check if persona would naturally end the conversation (very low score)
  const sessionOver = newScore <= 5;

  const updatedState: SimState = {
    ...stateWithUserTurn,
    turns: newTurns,
    currentScore: newScore,
    momentum: momentumLabel(newScore - 50), // -50 to +50 range for label
    sessionOver,
  };

  return {
    personaReply,
    updatedState,
    feedback: coachingTip,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Parse and validate the LLM's sim response JSON */
function parseSimResponse(raw: string): {
  reply: string;
  momentumDelta?: number;
  coachingTip?: string | null;
} {
  try {
    const parsed = JSON.parse(raw) as {
      reply?: string;
      momentumDelta?: unknown;
      coachingTip?: unknown;
    };

    const delta =
      typeof parsed.momentumDelta === "number"
        ? clamp(parsed.momentumDelta, -3, 3)
        : 0;

    const tip =
      typeof parsed.coachingTip === "string" && parsed.coachingTip.length > 0
        ? parsed.coachingTip
        : null;

    return {
      reply: typeof parsed.reply === "string" ? parsed.reply : "...",
      momentumDelta: delta,
      coachingTip: tip ?? undefined,
    };
  } catch {
    return { reply: raw.trim() || "...", momentumDelta: 0 };
  }
}

/** Fallback persona reply when LLM is unavailable */
function fallbackPersonaReply(persona: SimPersona, userMessage: string): string {
  const isShort = userMessage.trim().length < 15;

  if (persona.warmthLevel === 1) {
    return isShort ? "k" : "hmm. sure.";
  }
  if (persona.warmthLevel === 3) {
    return isShort ? "lol okay" : "haha that's actually kind of cute";
  }
  return isShort ? "lol okay" : "I mean... fair enough";
}

function extractText(content: Anthropic.ContentBlock[]): string {
  return content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text.trim())
    .join("");
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(Math.round(value), min), max);
}
