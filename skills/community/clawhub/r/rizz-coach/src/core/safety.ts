// =============================================================================
// core/safety.ts — Content safety filter
// Runs on ALL inputs before they reach the LLM, and on ALL outputs before
// they reach the user. Keeps Rizz Coach fun, healthy, and never creepy.
// =============================================================================

import type { SafetyCheckResult, SafetyFlag } from "../types.js";

// ---------------------------------------------------------------------------
// Blocked pattern registry
// Each entry maps a SafetyFlag to a list of regex patterns that trigger it.
// Patterns are intentionally broad — better a false positive than a miss.
// ---------------------------------------------------------------------------

const BLOCKED_PATTERNS: Record<SafetyFlag, RegExp[]> = {
  harassment: [
    /\b(ugly|disgusting|pathetic|worthless|loser|freak|trash)\b/i,
    /\bshut up\b/i,
    /\byou('re| are) nothing\b/i,
  ],

  coercion: [
    /\byou (have to|must|better|owe me)\b/i,
    /\bor else\b/i,
    /\bif you (don'?t|won'?t).{0,30}(i will|i'?ll|you'?ll regret)\b/i,
    /\b(force|coerce|make you)\b/i,
  ],

  stalking: [
    /\b(follow|track|locate|find out where|watch you|spy on|show up at)\b/i,
    /\b(your (address|location|house|home|work|school))\b/i,
    /\bwhere (do|does) (you|she|he|they) live\b/i,
  ],

  manipulation: [
    /\b(gaslight|manipulate|trick (them|her|him)|make (them|her|him) feel guilty)\b/i,
    /\b(negging|neg them|tear (them|her|him) down)\b/i,
    /\bfake (crying|emotion|caring)\b/i,
    /\bpretend (to|that you)\b/i,
  ],

  explicit: [
    /\b(sex|sexual|nude|naked|nudes|dick pic|send pics|onlyfans)\b/i,
    /\b(f+u+c+k+|s+h+i+t+|b+i+t+c+h+|c+u+n+t+)\b/i, // common obfuscations
    /\b(hook ?up|sleep with|get in (bed|pants))\b/i,
  ],

  minor_risk: [
    /\b(minor|underage|16|15|14|13|12|11|10|child|kid|teen|middle school|high school (fresh|soph))\b/i,
  ],

  rejection_escalation: [
    /\b(they said no but|she said no but|he said no but|keep (trying|texting|calling) after)\b/i,
    /\b(won'?t take no|doesn'?t mean no|no means maybe)\b/i,
    /\b(blocked me so i|new number|different account)\b/i,
  ],
};

// ---------------------------------------------------------------------------
// Rejection detection — if someone clearly rejected the user, give the
// "respect and move on" response rather than more tactics
// ---------------------------------------------------------------------------

const REJECTION_SIGNALS = [
  /\b(not interested|leave me alone|stop (texting|messaging|contacting)|blocked|don'?t (text|message|contact) me)\b/i,
  /\b(i have a (boyfriend|girlfriend|partner)|i'?m (taken|in a relationship|married|engaged))\b/i,
  /\b(please stop|i said no)\b/i,
];

/** Returns true if the message context signals a clear rejection */
export function detectsRejection(text: string): boolean {
  return REJECTION_SIGNALS.some((pattern) => pattern.test(text));
}

// ---------------------------------------------------------------------------
// Core safety check — call this on all user inputs
// ---------------------------------------------------------------------------

/**
 * Checks a string for policy violations.
 * @param text  The user input (message, context, etc.) to check
 * @returns     SafetyCheckResult with safe=false and flags if violations found
 */
export function checkInput(text: string): SafetyCheckResult {
  const flags: SafetyFlag[] = [];

  for (const [flag, patterns] of Object.entries(BLOCKED_PATTERNS) as [
    SafetyFlag,
    RegExp[]
  ][]) {
    if (patterns.some((pattern) => pattern.test(text))) {
      flags.push(flag);
    }
  }

  if (flags.length === 0) {
    return { safe: true, flags: [] };
  }

  return {
    safe: false,
    flags,
    message: buildBlockedMessage(flags),
  };
}

// ---------------------------------------------------------------------------
// Output safety check — lightweight scan on LLM responses before display
// ---------------------------------------------------------------------------

/**
 * Sanity-checks an LLM-generated output for anything that slipped through.
 * Less strict than input check — we trust our prompts — but still a backstop.
 */
export function checkOutput(text: string): SafetyCheckResult {
  // Only check the most critical categories on output
  const outputChecks: SafetyFlag[] = ["explicit", "coercion", "manipulation"];
  const flags: SafetyFlag[] = [];

  for (const flag of outputChecks) {
    const patterns = BLOCKED_PATTERNS[flag];
    if (patterns.some((pattern) => pattern.test(text))) {
      flags.push(flag);
    }
  }

  if (flags.length === 0) {
    return { safe: true, flags: [] };
  }

  return {
    safe: false,
    flags,
    message: "Something in that response didn't pass the vibe check. Try rephrasing your input.",
  };
}

// ---------------------------------------------------------------------------
// User-facing messages for each flag type
// ---------------------------------------------------------------------------

function buildBlockedMessage(flags: SafetyFlag[]): string {
  const messages: Record<SafetyFlag, string> = {
    harassment:
      "That's not the vibe — Rizz Coach only helps with confident, respectful connection. We don't do insults.",
    coercion:
      "Rizz Coach keeps things consensual. Pressure tactics aren't in the playbook.",
    stalking:
      "Tracking someone's location or movements isn't flirting — it's not something we can help with.",
    manipulation:
      "Real game doesn't need mind games. We don't coach deception or manipulation tactics.",
    explicit:
      "Keep it PG-13 in here. Rizz Coach is for charm, not explicit content.",
    minor_risk:
      "Rizz Coach is for adults interacting with adults. We can't help with this.",
    rejection_escalation:
      "Sounds like they've made their feelings clear. Real confidence means respecting a no and moving on — that's actually the most attractive thing you can do.",
  };

  // Return the most specific / serious message from the flagged set
  const priority: SafetyFlag[] = [
    "minor_risk",
    "stalking",
    "coercion",
    "manipulation",
    "harassment",
    "rejection_escalation",
    "explicit",
  ];

  for (const flag of priority) {
    if (flags.includes(flag)) {
      return messages[flag];
    }
  }

  return "This one's outside what Rizz Coach can help with. Keep it respectful!";
}
