/**
 * telos-context hook — Injects TELOS context into OpenClaw sessions
 *
 * Events:
 *   agent:bootstrap — Load core TELOS files at session start
 *   message:preprocessed — Inject relevant TELOS files before processing personal questions
 *
 * Install:
 *   Add to ~/.openclaw/hooks/ or register in openclaw config
 */

const fs = require("fs");
const path = require("path");

// Resolve workspace from OpenClaw runtime env var
const _workspace = process.env.OPENCLAW_WORKSPACE || process.env.CLAWD_WORKSPACE || path.join(require("os").homedir(), "openclaw");
const TELOS_DIR = path.join(_workspace, "telos");

// Core files loaded at every session start (lightweight, high-value)
const CORE_FILES = ["MISSION.md", "GOALS.md", "BELIEFS.md"];

// Topic → files mapping for on-demand loading
const TOPIC_FILES = {
  career: ["MISSION.md", "GOALS.md", "BELIEFS.md", "STRATEGIES.md"],
  investment: ["MISSION.md", "GOALS.md", "BELIEFS.md", "STRATEGIES.md"],
  decision: ["MISSION.md", "GOALS.md", "BELIEFS.md"],
  stuck: ["CHALLENGES.md", "STRATEGIES.md", "GOALS.md"],
  learning: ["LEARNED.md", "MODELS.md", "FRAMES.md"],
  book: ["BOOKS.md"],
  mistake: ["WRONG.md", "LEARNED.md"],
  idea: ["IDEAS.md", "GOALS.md"],
  predict: ["PREDICTIONS.md"],
  project: ["PROJECTS.md", "GOALS.md", "STRATEGIES.md"],
  trauma: ["TRAUMAS.md"],  // NOTE: not auto-triggered by keyword; requires explicit "my trauma" or "telos trauma"
  status: ["STATUS.md"],
};

// Keywords that signal personal topics
// NOTE: "trauma" is intentionally excluded from PERSONAL_KEYWORDS to prevent
// accidental injection of TRAUMAS.md in group chats or unrelated conversations.
// Use "my trauma", "telos trauma", or "traumas" to explicitly trigger it.
const PERSONAL_KEYWORDS = [
  "should i", "what do you think", "my goal", "my belief", "career",
  "job offer", "invest", "decision", "stuck", "frustrated", "challenge",
  "i learned", "i was wrong", "add to telos", "update telos", "telos",
  "my mission", "life", "priority", "strategy", "what should i do",
];

function readTelosFile(filename) {
  const filepath = path.join(TELOS_DIR, filename);
  if (!fs.existsSync(filepath)) return null;
  const content = fs.readFileSync(filepath, "utf-8");
  // Skip if only template content (less than 200 chars of real content)
  if (content.replace(/^#.*$/gm, "").replace(/\[.*?\]/g, "").trim().length < 50) return null;
  return content;
}

function detectTopics(message) {
  const lower = message.toLowerCase();
  const topics = new Set();
  for (const [topic, _] of Object.entries(TOPIC_FILES)) {
    // "trauma" requires explicit match to avoid accidental injection of sensitive content
    if (topic === "trauma") {
      if (lower.includes("my trauma") || lower.includes("telos trauma") || lower.includes("traumas")) {
        topics.add(topic);
      }
    } else {
      if (lower.includes(topic)) topics.add(topic);
    }
  }
  // Check personal keywords
  if (PERSONAL_KEYWORDS.some((kw) => lower.includes(kw))) {
    topics.add("decision"); // default to core files
  }
  return [...topics];
}

function getFilesForTopics(topics) {
  const files = new Set();
  for (const topic of topics) {
    const topicFiles = TOPIC_FILES[topic] || CORE_FILES;
    topicFiles.forEach((f) => files.add(f));
  }
  return [...files];
}

module.exports = {
  name: "telos-context",

  // Load core TELOS at session start
  on: {
    "agent:bootstrap": async (ctx) => {
      if (!fs.existsSync(TELOS_DIR)) return;

      const context = [];
      for (const file of CORE_FILES) {
        const content = readTelosFile(file);
        if (content) context.push(`--- ${file} ---\n${content}`);
      }

      if (context.length > 0) {
        ctx.inject = ctx.inject || [];
        ctx.inject.push({
          role: "system",
          content: `[TELOS Context — User's life framework]\n\n${context.join("\n\n")}`,
        });
      }
    },

    // Inject relevant TELOS files for personal questions
    "message:preprocessed": async (ctx) => {
      if (!fs.existsSync(TELOS_DIR)) return;
      if (!ctx.message || !ctx.message.content) return;

      const topics = detectTopics(ctx.message.content);
      if (topics.length === 0) return;

      const files = getFilesForTopics(topics);
      const context = [];
      for (const file of files) {
        const content = readTelosFile(file);
        if (content) context.push(`--- ${file} ---\n${content}`);
      }

      if (context.length > 0) {
        ctx.inject = ctx.inject || [];
        ctx.inject.push({
          role: "system",
          content: `[TELOS Context — Relevant to this question]\n\n${context.join("\n\n")}`,
        });
      }
    },
  },
};
