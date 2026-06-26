#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { mkdir, readFile, writeFile } from "node:fs/promises";

type CliArgs = {
  outlinePath: string | null;
  outputDir: string | null;
  help: boolean;
};

type OutlineMeta = {
  theme: string;
  audience: string;
  style: string;
  layout: string;
  language: string;
  aspect: string;
  seriesReference: string;
  seriesAnchors: string[];
};

type CardEntry = {
  index: number;
  role: string;
  filename: string;
  goal: string;
  visualFocus: string;
  continuityAnchors: string[];
  keyPoints: string[];
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/build-prompts.ts --outline outline.md --output-dir prompts

Options:
  --outline <path>      Path to outline.md
  --output-dir <path>   Directory for generated prompt files
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outlinePath: null,
    outputDir: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--outline") args.outlinePath = argv[++i] ?? null;
    else if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

function extractField(block: string, label: string): string {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return block.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*(.+)`))?.[1]?.trim() ?? "";
}

function extractBullets(block: string, label: string): string[] {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = block.match(new RegExp(`\\*\\*${escaped}\\*\\*:\\s*\\n((?:- .+\\n?)*)`, "m"));
  if (!match?.[1]) return [];
  return match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

function parseOutline(content: string): { meta: OutlineMeta; cards: CardEntry[] } {
  const normalized = content.replace(/\r\n/g, "\n");
  const meta: OutlineMeta = {
    theme: normalized.match(/\*\*Theme\*\*:\s*(.+)/)?.[1]?.trim() ?? "Topic",
    audience: normalized.match(/\*\*Audience\*\*:\s*(.+)/)?.[1]?.trim() ?? "general audience",
    style: normalized.match(/\*\*Style\*\*:\s*(.+)/)?.[1]?.trim() ?? "notion",
    layout: normalized.match(/\*\*Layout\*\*:\s*(.+)/)?.[1]?.trim() ?? "balanced",
    language: normalized.match(/\*\*Language\*\*:\s*(.+)/)?.[1]?.trim() ?? "zh",
    aspect: normalized.match(/\*\*Aspect\*\*:\s*(.+)/)?.[1]?.trim() ?? "3:4",
    seriesReference: normalized.match(/\*\*Series Reference\*\*:\s*(.+)/)?.[1]?.trim() ?? "references/series-reference.png",
    seriesAnchors: extractBullets(normalized, "Series Anchors"),
  };

  const lines = normalized.split("\n");
  const cards: CardEntry[] = [];
  for (let i = 0; i < lines.length; i++) {
    const header = lines[i]!.match(/^## Card (\d+)$/);
    if (!header) continue;
    const body: string[] = [];
    for (let j = i + 1; j < lines.length; j++) {
      if (lines[j]!.startsWith("## Card ")) break;
      body.push(lines[j]!);
      i = j;
    }
    const text = body.join("\n");
    cards.push({
      index: Number.parseInt(header[1] ?? "0", 10),
      role: extractField(text, "Role") || "content",
      filename: extractField(text, "Filename"),
      goal: extractField(text, "Goal"),
      visualFocus: extractField(text, "Visual Focus"),
      continuityAnchors: extractBullets(text, "Continuity Anchors"),
      keyPoints: extractBullets(text, "Key Points"),
    });
  }

  const filteredCards = cards.filter((card) => Number.isFinite(card.index) && card.filename);

  return { meta, cards: filteredCards };
}

function buildPrompt(meta: OutlineMeta, card: CardEntry, previousCard: CardEntry | null, nextCard: CardEntry | null): string {
  const keyPoints = card.keyPoints.length
    ? card.keyPoints.map((point) => `- ${point}`).join("\n")
    : "- <point 1>\n- <point 2>\n- Takeaway 3";
  const seriesAnchors = meta.seriesAnchors.length
    ? meta.seriesAnchors.map((anchor) => `- ${anchor}`).join("\n")
    : "- <shared palette>\n- <shared recurring subject>\n- <shared layout rhythm>";
  const continuityAnchors = card.continuityAnchors.length
    ? card.continuityAnchors.map((anchor) => `- ${anchor}`).join("\n")
    : "- Keep the same palette, framing system, and recurring subject as the rest of the series.";
  const previousRecap = previousCard
    ? `${previousCard.role}: ${previousCard.goal || "<previous card goal>"} | Focus: ${previousCard.visualFocus || "<previous focus>"}`
    : "Opening setup for the series.";
  const nextHook = nextCard
    ? `${nextCard.role}: ${nextCard.goal || "<next card goal>"} | Focus: ${nextCard.visualFocus || "<next focus>"}`
    : "Closing takeaway for the series.";

  return `[${card.goal || "one-sentence topic for this card"}]

Create a RedNote image card about: ${meta.theme}.
Series role: ${card.role}.
Target audience: ${meta.audience}.

Layout: ${meta.layout}.
Visual focus: ${card.visualFocus || "<main visual focus for this card>"}.
Aspect ratio: ${meta.aspect}.

Style direction: ${meta.style}.
Language: ${meta.language}.

Series reference:
- reference image: ${meta.seriesReference}
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, typography feel, and layout rhythm

Series anchors:
${seriesAnchors}

Card continuity:
- previous card recap: ${previousRecap}
- current transition: continue the same series identity and visual system
- next card hook: ${nextHook}
- card-specific anchors:
${continuityAnchors}

Key points to show:
${keyPoints}

Text treatment: title-only.
If text is used, keep it bold, sparse, readable, and native to the target language.

Avoid: cluttered layout, too many tiny words, unreadable typography, weak hierarchy, watermark, distorted anatomy.
`;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }
  if (!args.outlinePath) {
    console.error("Error: --outline is required");
    process.exit(1);
  }
  if (!args.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  const content = await readFile(path.resolve(args.outlinePath), "utf8");
  const { meta, cards } = parseOutline(content);
  if (cards.length === 0) {
    console.error("No card entries found in outline.");
    process.exit(1);
  }

  const outputDir = path.resolve(args.outputDir);
  await mkdir(outputDir, { recursive: true });
  for (const card of cards) {
    const previousCard = cards.find((candidate) => candidate.index === card.index - 1) ?? null;
    const nextCard = cards.find((candidate) => candidate.index === card.index + 1) ?? null;
    await writeFile(path.join(outputDir, card.filename), buildPrompt(meta, card, previousCard, nextCard), "utf8");
  }

  console.log(`Prompts written: ${outputDir} (${cards.length} files)`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
