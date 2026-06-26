// =============================================================================
// shareCard/cardGenerator.ts — Mode 5: Share Card Generator
//
// Generates a screenshot-friendly ASCII text card from any mode result.
// Designed to be copy-pasteable, DM-able, and tweet-worthy.
// =============================================================================

import type {
  ShareCardInput,
  ShareCardResult,
  ShareCardMode,
  RizzScore,
} from "../types.js";

// ---------------------------------------------------------------------------
// Card dimensions
// ---------------------------------------------------------------------------

const CARD_WIDTH = 34; // inner content width (between borders)

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Generates a share card for any Rizz Coach mode result.
 *
 * @param input  Score, mode, headline, and optional subtitle
 * @returns      ShareCardResult with the formatted ASCII card string
 */
export function generateShareCard(input: ShareCardInput): ShareCardResult {
  const card = buildCard(input);
  return { card, mode: input.mode };
}

// ---------------------------------------------------------------------------
// Card builder
// ---------------------------------------------------------------------------

function buildCard(input: ShareCardInput): string {
  const { mode, score, headline, subtitle } = input;

  // Choose default headline based on mode if none provided
  const title = headline ?? defaultHeadline(mode, score);
  const sub = subtitle ?? (score ? defaultSubtitle(score) : "");

  const lines: string[] = [
    border("top"),
    padLine("🏆  RIZZ COACH REPORT"),
    borderLine(),
    padLine(""),
    padLine(title),
    padLine(""),
    ...(score ? scoreLines(score) : []),
    sub ? padLine(sub) : null,
    padLine(""),
    ...(score ? dimensionMiniBar(score) : []),
    padLine(""),
    borderLine(),
    padLine("rizz-coach.app"),
    border("bottom"),
  ].filter((l): l is string => l !== null);

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Score section
// ---------------------------------------------------------------------------

function scoreLines(score: RizzScore): string[] {
  const gradeDisplay = `${score.total}/100  ·  Grade: ${score.grade}`;
  const titleDisplay = `"${score.title}"`;

  return [
    padLine(gradeDisplay),
    padLine(titleDisplay),
    padLine(""),
  ];
}

/**
 * Compact single-line mini bars for each dimension — fits the card width.
 * Format: Conf ████░ · Wit ███░░
 */
function dimensionMiniBar(score: RizzScore): string[] {
  const dims: [string, number][] = [
    ["Conf",  score.dimensions.confidence],
    ["Wit",   score.dimensions.wit],
    ["Warmth",score.dimensions.warmth],
    ["Clear", score.dimensions.clarity],
    ["Vibe",  score.dimensions.vibeMatch],
  ];

  return dims.map(([label, value]) => {
    const bar = "█".repeat(Math.round(value / 4)) + "░".repeat(5 - Math.round(value / 4));
    const valueStr = `${value}/20`;
    const content = `${label.padEnd(6)} ${bar}  ${valueStr}`;
    return padLine(content);
  });
}

// ---------------------------------------------------------------------------
// Default text helpers
// ---------------------------------------------------------------------------

function defaultHeadline(mode: ShareCardMode, score?: RizzScore): string {
  if (score) {
    return `Score: ${score.total}/100  [${score.grade}]`;
  }
  const modeLabels: Record<ShareCardMode, string> = {
    rate:   "Rate My Rizz",
    glowup: "Glow Up Complete ✨",
    reply:  "Reply Options Generated",
    sim:    "Sim Session Complete",
  };
  return modeLabels[mode];
}

function defaultSubtitle(score: RizzScore): string {
  const topDim = getTopDimension(score);
  const lowDim = getLowDimension(score);
  return `💪 ${topDim}  ·  📈 Work on: ${lowDim}`;
}

function getTopDimension(score: RizzScore): string {
  const dims = score.dimensions;
  const entries = Object.entries(dims) as [keyof typeof dims, number][];
  const top = entries.sort(([, a], [, b]) => b - a)[0];
  return LABEL_MAP[top[0]];
}

function getLowDimension(score: RizzScore): string {
  const dims = score.dimensions;
  const entries = Object.entries(dims) as [keyof typeof dims, number][];
  const low = entries.sort(([, a], [, b]) => a - b)[0];
  return LABEL_MAP[low[0]];
}

const LABEL_MAP: Record<string, string> = {
  confidence: "Confidence",
  wit:        "Wit",
  warmth:     "Warmth",
  clarity:    "Clarity",
  vibeMatch:  "Vibe Match",
};

// ---------------------------------------------------------------------------
// ASCII border helpers
// ---------------------------------------------------------------------------

/** Top or bottom border */
function border(position: "top" | "bottom"): string {
  const line = "─".repeat(CARD_WIDTH);
  return position === "top"
    ? `┌${line}┐`
    : `└${line}┘`;
}

/** Horizontal divider inside the card */
function borderLine(): string {
  return `├${"─".repeat(CARD_WIDTH)}┤`;
}

/**
 * Pads content to fit within card borders.
 * Truncates if text is longer than CARD_WIDTH - 2.
 */
function padLine(content: string): string {
  const maxLen = CARD_WIDTH - 2;
  const truncated = content.length > maxLen
    ? content.slice(0, maxLen - 1) + "…"
    : content;
  const padded = ` ${truncated}`.padEnd(CARD_WIDTH - 1);
  return `│${padded}│`;
}
