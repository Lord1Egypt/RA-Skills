// =============================================================================
// types.ts — Shared TypeScript interfaces and enums for Rizz Coach
// =============================================================================

// ---------------------------------------------------------------------------
// Scoring
// ---------------------------------------------------------------------------

/** The five rubric dimensions, each scored 0–20 */
export interface RizzDimensions {
  confidence: number; // Assertive without being pushy
  wit: number;        // Humor, wordplay, originality
  warmth: number;     // Genuine interest, not transactional
  clarity: number;    // Clear intent, no vague trailing off
  vibeMatch: number;  // Tone appropriate to context/audience
}

/** Letter grade mapped from total score */
export type RizzGrade = "S" | "A" | "B" | "C" | "D" | "F";

/** Full scoring result returned by the scorer */
export interface RizzScore {
  total: number;          // 0–100
  grade: RizzGrade;       // S / A / B / C / D / F
  title: string;          // e.g. "Certified Rizz God"
  dimensions: RizzDimensions;
  bestMove: string;       // What worked well
  weakSpot: string;       // What dragged the score down
}

// ---------------------------------------------------------------------------
// Mode: Rate My Rizz
// ---------------------------------------------------------------------------

export interface RateMyRizzInput {
  message: string;        // The message to evaluate
  context?: string;       // Optional context (e.g. "first text", "after a date")
}

export interface RateMyRizzResult {
  input: RateMyRizzInput;
  score: RizzScore;
}

// ---------------------------------------------------------------------------
// Mode: Glow Up My Text
// ---------------------------------------------------------------------------

/** Three intensity tiers for rewritten messages */
export interface GlowUpTiers {
  subtle: string;         // Light improvement, still grounded
  confident: string;      // Assertive, clear, direct
  bold: string;           // High energy, memorable, a little cheeky
}

export interface GlowUpInput {
  message: string;        // The original message to rewrite
  context?: string;       // Optional context about the recipient/situation
}

export interface GlowUpResult {
  original: string;
  tiers: GlowUpTiers;
  originalScore: RizzScore; // Score of the original so user sees the delta
}

// ---------------------------------------------------------------------------
// Mode: Reply Generator
// ---------------------------------------------------------------------------

/** Vibe the user wants their reply to project */
export type ReplyVibe = "playful" | "confident" | "chill" | "romantic" | "witty";

export interface ReplyOption {
  vibe: ReplyVibe;
  text: string;
  riskLevel: "safe" | "medium" | "spicy"; // So user knows what they're picking
}

export interface ReplyGeneratorInput {
  theirMessage: string;   // The message you received
  context?: string;       // Relationship context, prior convo, etc.
  preferredVibes?: ReplyVibe[]; // Filter to specific vibes
}

export interface ReplyGeneratorResult {
  theirMessage: string;
  replies: ReplyOption[];
}

// ---------------------------------------------------------------------------
// Mode: Conversation Simulator
// ---------------------------------------------------------------------------

/** Persona the user is practicing against */
export interface SimPersona {
  name: string;
  archetype: string;        // e.g. "Witty & slightly guarded"
  description: string;      // Brief personality summary for the LLM
  warmthLevel: 1 | 2 | 3;  // 1 = reserved, 2 = moderate, 3 = warm
}

/** A single turn in the simulated conversation */
export interface SimTurn {
  speaker: "user" | "persona";
  message: string;
  momentumDelta?: number;   // Optional: how much this turn helped/hurt momentum
}

/** Running state of the simulation */
export interface SimState {
  persona: SimPersona;
  turns: SimTurn[];
  currentScore: number;     // Running rizz score for the conversation
  momentum: "building" | "steady" | "losing" | "dead";
  sessionOver: boolean;     // True if persona ends the convo or user types /quit
}

export interface ConversationSimInput {
  userMessage: string;      // The current message from the user
  state: SimState;          // Current sim state (carries conversation history)
}

export interface ConversationSimResult {
  personaReply: string;
  updatedState: SimState;
  feedback?: string;        // Optional coaching tip after certain turns
}

// ---------------------------------------------------------------------------
// Share Card
// ---------------------------------------------------------------------------

/** Source mode that generated the result being shared */
export type ShareCardMode = "rate" | "glowup" | "reply" | "sim";

export interface ShareCardInput {
  mode: ShareCardMode;
  score?: RizzScore;
  headline?: string;        // Custom headline override
  subtitle?: string;        // e.g. "Best move: genuine curiosity"
}

export interface ShareCardResult {
  card: string;             // ASCII/text formatted share card
  mode: ShareCardMode;
}

// ---------------------------------------------------------------------------
// Safety
// ---------------------------------------------------------------------------

export type SafetyFlag =
  | "harassment"
  | "coercion"
  | "stalking"
  | "manipulation"
  | "explicit"
  | "minor_risk"
  | "rejection_escalation"; // User getting pushy after a clear "no"

export interface SafetyCheckResult {
  safe: boolean;
  flags: SafetyFlag[];
  message?: string;         // User-facing explanation if blocked
}

// ---------------------------------------------------------------------------
// Skill I/O (OpenClaw / ClawHub adapter interface)
// ---------------------------------------------------------------------------

/** Top-level mode selector */
export type SkillMode = "rate" | "glowup" | "reply" | "sim" | "share";

export interface SkillInput {
  mode: SkillMode;
  payload: Record<string, unknown>; // Mode-specific input, deserialized per mode
}

export interface SkillOutput {
  success: boolean;
  mode: SkillMode;
  result?: unknown;         // Mode-specific result
  error?: string;
  safetyBlocked?: boolean;
}
