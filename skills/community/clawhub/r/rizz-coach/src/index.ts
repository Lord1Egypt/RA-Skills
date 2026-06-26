// =============================================================================
// index.ts — Rizz Coach CLI entry point
//
// Interactive REPL for local testing. Uses readline for a smooth
// menu-driven experience. All modes are accessible from the main menu.
//
// Run with:  npm start  (or: npx tsx src/index.ts)
// =============================================================================

import * as readline from "readline";
import type { SimState, ReplyVibe } from "./types.js";
import { rateMyRizz, SafetyError } from "./modes/rateMyRizz.js";
import { glowUp } from "./modes/glowUp.js";
import { generateReplies } from "./modes/replyGenerator.js";
import {
  createSimSession,
  sendSimMessage,
  PERSONAS,
} from "./modes/conversationSim.js";
import { generateShareCard } from "./shareCard/cardGenerator.js";
import {
  formatRateMyRizz,
  formatGlowUp,
  formatReplyGenerator,
  formatSimState,
  formatSafetyBlock,
  formatError,
} from "./core/formatter.js";

// ---------------------------------------------------------------------------
// readline setup
// ---------------------------------------------------------------------------

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

/** Prompts the user and returns their input as a promise */
function ask(prompt: string): Promise<string> {
  return new Promise((resolve) => rl.question(prompt, resolve));
}

// ---------------------------------------------------------------------------
// Main loop
// ---------------------------------------------------------------------------

async function main() {
  console.clear();
  printBanner();

  let running = true;
  while (running) {
    printMainMenu();
    const choice = (await ask("\nYour choice: ")).trim();

    switch (choice) {
      case "1":
        await runRateMyRizz();
        break;
      case "2":
        await runGlowUp();
        break;
      case "3":
        await runReplyGenerator();
        break;
      case "4":
        await runConversationSim();
        break;
      case "q":
      case "Q":
        console.log("\n✌️  Stay confident. Rizz Coach out.\n");
        running = false;
        break;
      default:
        console.log(formatError("Invalid choice — pick 1–4 or Q to quit."));
    }

    if (running) {
      await ask("\nPress Enter to return to menu...");
    }
  }

  rl.close();
}

// ---------------------------------------------------------------------------
// Mode 1: Rate My Rizz
// ---------------------------------------------------------------------------

async function runRateMyRizz() {
  console.log("\n" + "━".repeat(40));
  console.log("📊  RATE MY RIZZ");
  console.log("━".repeat(40));

  const message = await ask("\nPaste your message: ");
  if (!message.trim()) {
    console.log(formatError("No message entered."));
    return;
  }

  const context = await ask("Context (optional — e.g. 'first text after a party', or press Enter to skip): ");

  console.log("\n⏳  Analyzing your rizz...\n");

  try {
    const result = await rateMyRizz({
      message: message.trim(),
      context: context.trim() || undefined,
    });

    console.log(formatRateMyRizz(result));

    // Offer share card
    const share = await ask("\n🃏  Generate a share card? (y/N): ");
    if (share.trim().toLowerCase() === "y") {
      const card = generateShareCard({
        mode: "rate",
        score: result.score,
      });
      console.log("\n" + card.card);
    }
  } catch (err) {
    if (err instanceof SafetyError) {
      console.log(formatSafetyBlock(err.message));
    } else {
      console.log(formatError("Something went wrong. Please try again."));
    }
  }
}

// ---------------------------------------------------------------------------
// Mode 2: Glow Up My Text
// ---------------------------------------------------------------------------

async function runGlowUp() {
  console.log("\n" + "━".repeat(40));
  console.log("✨  GLOW UP MY TEXT");
  console.log("━".repeat(40));

  const message = await ask("\nPaste your original message: ");
  if (!message.trim()) {
    console.log(formatError("No message entered."));
    return;
  }

  const context = await ask("Context (optional): ");

  console.log("\n⏳  Cooking up your glow up...\n");

  try {
    const result = await glowUp({
      message: message.trim(),
      context: context.trim() || undefined,
    });

    console.log(formatGlowUp(result));
  } catch (err) {
    if (err instanceof SafetyError) {
      console.log(formatSafetyBlock(err.message));
    } else {
      console.log(formatError("Something went wrong. Please try again."));
    }
  }
}

// ---------------------------------------------------------------------------
// Mode 3: Reply Generator
// ---------------------------------------------------------------------------

async function runReplyGenerator() {
  console.log("\n" + "━".repeat(40));
  console.log("💬  REPLY GENERATOR");
  console.log("━".repeat(40));

  const theirMessage = await ask("\nWhat did they say? Paste their message: ");
  if (!theirMessage.trim()) {
    console.log(formatError("No message entered."));
    return;
  }

  const context = await ask("Context (optional): ");

  console.log("\nVibes available: playful, confident, chill, romantic, witty");
  const vibeInput = await ask("Pick up to 3 vibes (comma-separated, or press Enter for defaults): ");

  const preferredVibes: ReplyVibe[] = vibeInput.trim()
    ? (vibeInput
        .split(",")
        .map((v) => v.trim().toLowerCase())
        .filter((v): v is ReplyVibe =>
          ["playful", "confident", "chill", "romantic", "witty"].includes(v)
        ))
    : [];

  console.log("\n⏳  Generating replies...\n");

  try {
    const result = await generateReplies({
      theirMessage: theirMessage.trim(),
      context: context.trim() || undefined,
      preferredVibes: preferredVibes.length > 0 ? preferredVibes : undefined,
    });

    console.log(formatReplyGenerator(result));
  } catch (err) {
    if (err instanceof SafetyError) {
      console.log(formatSafetyBlock(err.message));
    } else {
      console.log(formatError("Something went wrong. Please try again."));
    }
  }
}

// ---------------------------------------------------------------------------
// Mode 4: Conversation Simulator
// ---------------------------------------------------------------------------

async function runConversationSim() {
  console.log("\n" + "━".repeat(40));
  console.log("🎮  CONVERSATION SIMULATOR");
  console.log("━".repeat(40));

  // Persona selection
  console.log("\nChoose a persona to practice with:\n");
  PERSONAS.forEach((p, i) => {
    console.log(`  [${i + 1}] ${p.name} — ${p.archetype}`);
  });

  const personaChoice = await ask("\nYour choice (or press Enter for Alex): ");
  const personaIndex = parseInt(personaChoice.trim()) - 1;
  const persona = PERSONAS[personaIndex] ?? PERSONAS[0];

  console.log(`\n🎭  You're now talking to ${persona.name}. Good luck.\n`);
  console.log("     (Type /quit to end · /score for breakdown · /share for share card)\n");
  console.log("─".repeat(40));

  let state: SimState = createSimSession(persona.name);
  let lastCoachingTip: string | undefined;

  // Main sim loop
  while (!state.sessionOver) {
    // Show current state
    if (state.turns.length > 0) {
      console.log(formatSimState(state, lastCoachingTip));
      lastCoachingTip = undefined;
    } else {
      console.log(`\n${persona.name} is waiting... send the first message.\n`);
    }

    const userMessage = await ask("> ");

    // Handle special commands
    if (userMessage.trim() === "/quit") {
      state = { ...state, sessionOver: true };
      console.log(formatSimState(state));
      break;
    }

    if (userMessage.trim() === "/score") {
      console.log(`\n📊  Current score: ${state.currentScore}/100  |  Momentum: ${state.momentum}`);
      continue;
    }

    if (userMessage.trim() === "/share") {
      const card = generateShareCard({
        mode: "sim",
        headline: `Sim Score: ${state.currentScore}/100`,
        subtitle: `Persona: ${persona.name} · Momentum: ${state.momentum}`,
      });
      console.log("\n" + card.card);
      continue;
    }

    if (!userMessage.trim()) continue;

    // Process message
    console.log("\n⏳\n");

    try {
      const result = await sendSimMessage({ userMessage: userMessage.trim(), state });
      state = result.updatedState;
      lastCoachingTip = result.feedback;

      // Show persona reply immediately (before full state render on next loop)
      console.log(`\n${persona.name}: "${result.personaReply}"\n`);
    } catch (err) {
      if (err instanceof SafetyError) {
        console.log(formatSafetyBlock(err.message));
      } else {
        console.log(formatError("Something went wrong. Please try again."));
      }
    }
  }
}

// ---------------------------------------------------------------------------
// UI: banner + menu
// ---------------------------------------------------------------------------

function printBanner() {
  console.log(`
╔══════════════════════════════════════╗
║                                      ║
║   💬  RIZZ COACH  v1.0               ║
║   Rate · Upgrade · Simulate · Share  ║
║                                      ║
╚══════════════════════════════════════╝
`);
}

function printMainMenu() {
  console.log(`
What do you want to work on?

  [1]  📊  Rate My Rizz        — score a message 0–100
  [2]  ✨  Glow Up My Text     — rewrite it, 3 intensity tiers
  [3]  💬  Reply Generator     — generate replies to their message
  [4]  🎮  Conversation Sim    — practice with a simulated persona

  [Q]  Quit
`);
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

main().catch((err) => {
  console.error("Fatal error:", err);
  rl.close();
  process.exit(1);
});
