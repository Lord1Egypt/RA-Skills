#!/usr/bin/env bun
import process from "node:process";
import { mkdir, writeFile, access } from "node:fs/promises";
import { constants } from "node:fs";
import path from "node:path";

type CliArgs = {
  outputDir: string | null;
  theme: string;
  audience: string;
  style: string;
  layout: string;
  language: string;
  aspect: string;
  cards: number;
  force: boolean;
  help: boolean;
};

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/scaffold.ts --output-dir rednote-images/topic-slug --theme "Topic" [options]

Options:
  --output-dir <path>   Target RedNote working directory
  --theme <text>        Main topic or thesis
  --audience <text>     Audience placeholder (default: general audience)
  --style <name>        Visual style (default: notion)
  --layout <name>       Layout style (default: balanced)
  --lang <code>         On-canvas text language when needed (default placeholder: zh)
  --aspect <ratio>      Aspect ratio (default: 3:4)
  --cards <count>       Number of cards to scaffold (default: 5)
  --force               Overwrite existing files
  -h, --help            Show help`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    outputDir: null,
    theme: "Topic",
    audience: "general audience",
    style: "notion",
    layout: "balanced",
    language: "zh",
    aspect: "3:4",
    cards: 5,
    force: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--output-dir") args.outputDir = argv[++i] ?? null;
    else if (current === "--theme") args.theme = argv[++i] ?? args.theme;
    else if (current === "--audience") args.audience = argv[++i] ?? args.audience;
    else if (current === "--style") args.style = argv[++i] ?? args.style;
    else if (current === "--layout") args.layout = argv[++i] ?? args.layout;
    else if (current === "--lang") args.language = argv[++i] ?? args.language;
    else if (current === "--aspect") args.aspect = argv[++i] ?? args.aspect;
    else if (current === "--cards") {
      const value = parseInt(argv[++i] ?? "", 10);
      if (Number.isFinite(value) && value >= 1) args.cards = value;
    } else if (current === "--force") args.force = true;
    else if (current === "--help" || current === "-h") args.help = true;
  }

  return args;
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await access(filePath, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function writeScaffoldFile(filePath: string, content: string, force: boolean): Promise<void> {
  if (!force && (await exists(filePath))) {
    throw new Error(`File already exists: ${filePath}. Use --force to overwrite.`);
  }
  await writeFile(filePath, content, "utf8");
}

function promptFileName(index: number, total: number): string {
  const prefix = String(index).padStart(2, "0");
  if (index === 1) return `${prefix}-cover.md`;
  if (index === total) return `${prefix}-ending.md`;
  return `${prefix}-content.md`;
}

function cardRole(index: number, total: number): string {
  if (index === 1) return "cover";
  if (index === total) return "ending";
  return "content";
}

function outlineTemplate(args: CliArgs): string {
  const cardBlocks = Array.from({ length: args.cards }, (_, offset) => {
    const index = offset + 1;
    return `## Card ${index}
**Role**: ${cardRole(index, args.cards)}
**Filename**: ${promptFileName(index, args.cards)}
**Goal**: Deliver one clear takeaway for this card in the series
**Visual Focus**: A single strong subject + 3 supporting icons/blocks
**Continuity Anchors**:
- Keep palette, mascot, and layout rhythm consistent across cards
**Key Points**:
- Takeaway 1
- Takeaway 2
`;
  }).join("\n");

  return `# RedNote Outline

**Theme**: ${args.theme}
**Audience**: ${args.audience}
**Style**: ${args.style}
**Layout**: ${args.layout}
**Language**: ${args.language}
**Aspect**: ${args.aspect}
**Card Count**: ${args.cards}
**Series Reference**: references/series-reference.png
**Series Anchors**:
- warm orange + off-white + deep navy accents
- recurring mascot: a lobster wearing sunglasses
- typography: bold, sparse titles; clear hierarchy; generous whitespace

${cardBlocks}`;
}

function seriesReferenceTemplate(args: CliArgs): string {
  return `Create a canonical RedNote series reference image for: ${args.theme}.

Purpose: establish one stable visual system that later cards must follow.
Target audience: ${args.audience}.
Style direction: ${args.style}.
Layout system: ${args.layout}.
Language: ${args.language}.
Aspect ratio: ${args.aspect}.

Include:
- the core palette for the whole series
- the main recurring subject, mascot, product, or presenter if relevant
- the preferred typography feel and spacing rhythm
- the overall card framing and decorative system

This is not a finished content card. It is the canonical visual reference for the full series.
Avoid: random style switching, inconsistent palette, clutter, watermark, distorted anatomy.
`;
}

function promptTemplate(args: CliArgs, index: number): string {
  const role = cardRole(index, args.cards);
  return `RedNote card: quick practical tips

Create a RedNote image card about: ${args.theme}.
Series role: ${role}.
Target audience: ${args.audience}.

Layout: ${args.layout}.
Visual focus: Sunglasses lobster centered; 3 bullet blocks with simple icons.
Aspect ratio: ${args.aspect}.

Style direction: ${args.style}.
Language: ${args.language}.

Series reference:
- reference image: references/series-reference.png
- priority rule: treat the series reference as the canonical source of truth for palette, recurring subject, typography feel, and layout rhythm

Series anchors:
- overall palette: warm orange + off-white + deep navy accents
- recurring subject / mascot / product: a lobster wearing sunglasses
- layout rhythm: title top, hero middle, 3 key points bottom

Card continuity:
- previous card recap: established the lobster mascot and palette
- current transition: keep the same mascot and layout rhythm
- next card hook: end with a short actionable summary

Key points to show:
- Takeaway 1
- Takeaway 2
- Takeaway 3

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
  if (!args.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  const outputDir = path.resolve(args.outputDir);
  const promptsDir = path.join(outputDir, "prompts");
  const referencesDir = path.join(outputDir, "references");
  await mkdir(promptsDir, { recursive: true });
  await mkdir(referencesDir, { recursive: true });

  await writeScaffoldFile(path.join(outputDir, "outline.md"), outlineTemplate(args), args.force);
  await writeScaffoldFile(path.join(referencesDir, "series-reference.md"), seriesReferenceTemplate(args), args.force);

  for (let index = 1; index <= args.cards; index++) {
    const promptPath = path.join(promptsDir, promptFileName(index, args.cards));
    await writeScaffoldFile(promptPath, promptTemplate(args, index), args.force);
  }

  console.log(`Scaffold created in: ${outputDir}`);
  console.log("Files:");
  console.log("- outline.md");
  console.log("- references/series-reference.md");
  console.log("- prompts/");
  for (let index = 1; index <= args.cards; index++) {
    console.log(`  - ${promptFileName(index, args.cards)}`);
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
