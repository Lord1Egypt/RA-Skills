// =============================================================================
// core/formatter.ts — Renders all mode results into display-ready text
//
// All visual formatting lives here. Mode files return structured data;
// this module turns it into the polished CLI output the user sees.
// =============================================================================

import type {
  RateMyRizzResult,
  GlowUpResult,
  ReplyGeneratorResult,
  SimState,
  RizzScore,
  RizzDimensions,
  ReplyOption,
} from "../types.js";
import { DIMENSION_KEYS, DIMENSION_LABELS } from "./scorer.js";

// ---------------------------------------------------------------------------
// Shared visual constants
// ---------------------------------------------------------------------------

const DIVIDER = "━".repeat(40);
const THIN_DIVIDER = "─".repeat(40);

// ---------------------------------------------------------------------------
// Format: Rate My Rizz
// ---------------------------------------------------------------------------

/**
 * Renders a Rate My Rizz result as a full terminal display.
 */
export function formatRateMyRizz(result: RateMyRizzResult): string {
  const { score } = result;
  const lines: string[] = [
    "",
    DIVIDER,
    "📊  RIZZ REPORT",
    DIVIDER,
    "",
    `Score: ${score.total} / 100   [${score.grade}]   "${score.title}"`,
    "",
    `✅  Best move:  ${score.bestMove}`,
    `⚠️   Weak spot:  ${score.weakSpot}`,
    "",
    "Breakdown:",
    ...formatDimensions(score.dimensions),
    "",
    THIN_DIVIDER,
  ];

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Format: Glow Up My Text
// ---------------------------------------------------------------------------

/**
 * Renders a Glow Up result showing original and all three rewritten tiers.
 */
export function formatGlowUp(result: GlowUpResult): string {
  const lines: string[] = [
    "",
    DIVIDER,
    "✨  GLOW UP COMPLETE",
    DIVIDER,
    "",
    `Original:    "${result.original}"`,
    `(Original score: ${result.originalScore.total}/100 · ${result.originalScore.title})`,
    "",
    `🌤  Subtle:    "${result.tiers.subtle}"`,
    "",
    `🔥  Confident: "${result.tiers.confident}"`,
    "",
    `💥  Bold:      "${result.tiers.bold}"`,
    "",
    THIN_DIVIDER,
  ];

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Format: Reply Generator
// ---------------------------------------------------------------------------

/**
 * Renders reply options with vibe labels and risk indicators.
 */
export function formatReplyGenerator(result: ReplyGeneratorResult): string {
  const lines: string[] = [
    "",
    DIVIDER,
    "💬  REPLY OPTIONS",
    DIVIDER,
    "",
    `They said: "${result.theirMessage}"`,
    "",
    "Pick your vibe:",
    "",
    ...result.replies.map((reply, i) => formatReplyOption(reply, i + 1)),
    THIN_DIVIDER,
  ];

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Format: Conversation Simulator
// ---------------------------------------------------------------------------

/**
 * Renders the current state of the conversation simulator.
 */
export function formatSimState(state: SimState, coachingTip?: string): string {
  const lastTurn = state.turns[state.turns.length - 1];
  const momentumEmoji = getMomentumEmoji(state.momentum);

  const lines: string[] = [
    "",
    DIVIDER,
    `🎮  SIM MODE  |  Persona: ${state.persona.name} (${state.persona.archetype})`,
    DIVIDER,
    "",
  ];

  // Show last exchange only (not full history — cleaner for CLI)
  if (lastTurn) {
    const prevTurn = state.turns[state.turns.length - 2];
    if (prevTurn && prevTurn.speaker === "user") {
      lines.push(`You:            "${prevTurn.message}"`);
    }
    if (lastTurn.speaker === "persona") {
      lines.push(`${state.persona.name}:  "${lastTurn.message}"`);
    }
    lines.push("");
  }

  lines.push(
    `[Score so far: ${state.currentScore}]  Momentum: ${momentumEmoji} ${capitalise(state.momentum)}`
  );

  if (coachingTip) {
    lines.push("", `💡  Coach tip: ${coachingTip}`);
  }

  if (state.sessionOver) {
    lines.push("", `— ${state.persona.name} has left the chat. Session over.`);
    lines.push(formatSimSummary(state));
  } else {
    lines.push("", "> Your next message (or /quit to end · /score for breakdown):");
  }

  lines.push("", THIN_DIVIDER);
  return lines.join("\n");
}

/**
 * Renders a session summary when the sim ends.
 */
function formatSimSummary(state: SimState): string {
  const userTurns = state.turns.filter((t) => t.speaker === "user").length;

  return [
    "",
    "━━  SESSION SUMMARY  ━━",
    `Final score:   ${state.currentScore} / 100`,
    `Turns played:  ${userTurns}`,
    `Outcome:       ${getOutcomeLabel(state.currentScore)}`,
    "",
    "Type /share to generate your share card, or press Enter to return to menu.",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Format: Dimensions bar chart (shared by rate + sim summary)
// ---------------------------------------------------------------------------

/**
 * Renders the 5-dimension breakdown as mini progress bars.
 */
function formatDimensions(dimensions: RizzDimensions): string[] {
  return DIMENSION_KEYS.map((key) => {
    const value = dimensions[key];
    const label = DIMENSION_LABELS[key].padEnd(12);
    const bar = buildBar(value, 20, 12);
    return `  ${label}  ${bar}  ${String(value).padStart(2)}/20`;
  });
}

/** Renders a filled/empty block bar for a 0–max value */
function buildBar(value: number, max: number, barWidth: number): string {
  const filled = Math.round((value / max) * barWidth);
  const empty = barWidth - filled;
  return "█".repeat(filled) + "░".repeat(empty);
}

// ---------------------------------------------------------------------------
// Format: Single reply option
// ---------------------------------------------------------------------------

function formatReplyOption(reply: ReplyOption, index: number): string {
  const riskLabel = getRiskLabel(reply.riskLevel);
  const vibeLabel = capitalise(reply.vibe).padEnd(10);
  return `  [${index}] ${vibeLabel}  ${riskLabel}  "${reply.text}"`;
}

// ---------------------------------------------------------------------------
// Safety blocked message (displayed instead of any mode output)
// ---------------------------------------------------------------------------

/**
 * Renders a friendly but firm safety block message.
 */
export function formatSafetyBlock(message: string): string {
  return [
    "",
    DIVIDER,
    "🚫  RIZZ COACH CAN'T HELP WITH THAT",
    DIVIDER,
    "",
    message,
    "",
    THIN_DIVIDER,
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Error display
// ---------------------------------------------------------------------------

export function formatError(message: string): string {
  return [
    "",
    `❌  ${message}`,
    "",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getMomentumEmoji(momentum: SimState["momentum"]): string {
  const map: Record<SimState["momentum"], string> = {
    building: "📈",
    steady:   "➡️ ",
    losing:   "📉",
    dead:     "💀",
  };
  return map[momentum];
}

function getRiskLabel(level: ReplyOption["riskLevel"]): string {
  const map: Record<ReplyOption["riskLevel"], string> = {
    safe:   "🟢",
    medium: "🟡",
    spicy:  "🌶️ ",
  };
  return map[level];
}

function getOutcomeLabel(score: number): string {
  if (score >= 75) return "🏆 You're in — they're interested.";
  if (score >= 50) return "📲 Decent showing — keep the convo going.";
  if (score >= 30) return "😬 A bit rough — check the coaching tips.";
  return "💀 It's a rebuild — but every Rizz God started somewhere.";
}

function capitalise(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ---------------------------------------------------------------------------
// Score formatter (standalone — used by share card and other contexts)
// ---------------------------------------------------------------------------

export function formatScoreLine(score: RizzScore): string {
  return `${score.total}/100  [${score.grade}]  "${score.title}"`;
}
