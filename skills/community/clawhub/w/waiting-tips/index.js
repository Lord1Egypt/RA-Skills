/**
 * OpenClaw Waiting Tips Plugin
 *
 * Registers a `waiting_tip` tool that returns a random bilingual tip.
 * OpenClaw calls this before sending the AI response, filling the wait time.
 *
 * Install: openclaw plugins install -l /path/to/openclaw-waiting-tips
 * Or:      clawhub install waiting-tips
 */
import { readFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TIPS_DIR = join(__dirname, 'tips');

let cachedTips = null;

function loadTips() {
  if (cachedTips) return cachedTips;
  const tips = [];
  const files = readdirSync(TIPS_DIR).filter(f => f.endsWith('.txt'));
  for (const file of files) {
    const content = readFileSync(join(TIPS_DIR, file), 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('##')) continue;
      tips.push(trimmed);
    }
  }
  cachedTips = tips;
  return tips;
}

function getRandomTip() {
  const tips = loadTips();
  return tips[Math.floor(Math.random() * tips.length)];
}

function formatTip(tip, style = 'emoji') {
  const [zh, en] = tip.split(' | ');
  switch (style) {
    case 'zh-only':
      return `💡 ${zh || tip}`;
    case 'en-only':
      return `💡 ${en || tip}`;
    case 'card':
      return `━━━━━━━━━━━━━━━\n💡 Tips while you wait\n\n${zh || tip}\n${en ? `\n${en}` : ''}\n━━━━━━━━━━━━━━━`;
    default:
      return `💡 ${tip}`;
  }
}

export default function (api) {
  // Register the waiting_tip tool
  api.registerTool(
    {
      name: "waiting_tip",
      description:
        "Get a random bilingual learning tip to show the user while waiting for AI response. " +
        "Call this BEFORE processing a complex request to fill the wait time with useful knowledge. " +
        "Also use when the user asks for a tip, learning content, or says '来个tip'.",
      parameters: {
        type: "object",
        properties: {
          style: {
            type: "string",
            enum: ["emoji", "card", "zh-only", "en-only"],
            description: "Display style. Default: emoji",
          },
          count: {
            type: "number",
            description: "Number of tips to return (1-5). Default: 1",
          },
        },
      },
      async execute(_id, params) {
        const style = params.style || "emoji";
        const count = Math.min(Math.max(params.count || 1, 1), 5);

        const tips = loadTips();
        const shuffled = [...tips].sort(() => Math.random() - 0.5);
        const selected = shuffled.slice(0, count);

        const formatted = selected.map(t => formatTip(t, style)).join("\n\n");

        return {
          content: [{ type: "text", text: formatted }],
        };
      },
    },
    { optional: true }
  );
}
