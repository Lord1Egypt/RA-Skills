#!/usr/bin/env -S node --import tsx
// extract-imperatives.ts — Extract atomic imperatives from markdown into JSONL.
// Run from this skill: node --import tsx "${SKILL_DIR}/scripts/extract-imperatives.ts" <files...> [--output <path>]
// Or: "${SKILL_DIR}/scripts/extract-imperatives.ts" <files...> (if chmod +x and tsx installed)

import { readFileSync, writeFileSync } from "node:fs";
import { basename, relative } from "node:path";

const args = process.argv.slice(2);

if (args.includes("--help") || args.length === 0) {
  console.log(`Usage: node --import tsx "\${SKILL_DIR}/scripts/extract-imperatives.ts" <files...> [--output <path>]

Extracts imperative statements from markdown files and outputs JSONL.

Options:
  --output <path>  Write JSONL to file instead of stdout
  --help           Show this help

Examples:
  node --import tsx "\${SKILL_DIR}/scripts/extract-imperatives.ts" .claude/rules/*.md AGENTS.md
  node --import tsx "\${SKILL_DIR}/scripts/extract-imperatives.ts" --output out.jsonl ai-workspace/rules/*.md`);
  process.exit(0);
}

let outputPath: string | null = null;
const files: string[] = [];
for (let i = 0; i < args.length; i++) {
  const arg = args[i] as string;
  const next = args[i + 1];
  if (arg === "--output" && next) {
    outputPath = next;
    i++;
  } else if (!arg.startsWith("--")) {
    files.push(arg);
  }
}

interface Imperative {
  id: string;
  level: "MUST" | "SHOULD" | "MAY";
  polarity: "positive" | "negative";
  subject: string;
  predicate: string;
  when: string | null;
  source: { file: string; line: number };
  tool_scope: "general" | "claude-code" | "codex";
  tags: string[];
  raw: string;
}

type Level = "MUST" | "SHOULD" | "MAY";
type Polarity = "positive" | "negative";

// Ordered: negative variants before positive (longest-match-first)
const PATTERNS: Array<[RegExp, Level, Polarity]> = [
  [/\bMUST\s+NOT\b(.+?)(?:\.|$)/i, "MUST", "negative"],
  [/\bSHALL\s+NOT\b(.+?)(?:\.|$)/i, "MUST", "negative"],
  [/\bSHOULD\s+NOT\b(.+?)(?:\.|$)/i, "SHOULD", "negative"],
  [/\bMAY\s+NOT\b(.+?)(?:\.|$)/i, "MAY", "negative"],
  [/\bMUST\b(.+?)(?:\.|$)/i, "MUST", "positive"],
  [/\bSHALL\b(.+?)(?:\.|$)/i, "MUST", "positive"],
  [/\bREQUIRED\b(.+?)(?:\.|$)/i, "MUST", "positive"],
  [/\bSHOULD\b(.+?)(?:\.|$)/i, "SHOULD", "positive"],
  [/\bRECOMMENDED\b(.+?)(?:\.|$)/i, "SHOULD", "positive"],
  [/\bMAY\b(.+?)(?:\.|$)/i, "MAY", "positive"],
  [/\bOPTIONAL\b(.+?)(?:\.|$)/i, "MAY", "positive"],
  [/\bNever\b(.+?)(?:\.|$)/, "MUST", "negative"],
  [/\bNEVER\b(.+?)(?:\.|$)/, "MUST", "negative"],
  [/\bAlways\b(.+?)(?:\.|$)/, "MUST", "positive"],
  [/\bALWAYS\b(.+?)(?:\.|$)/, "MUST", "positive"],
  [/\bDo\s+NOT\b(.+?)(?:\.|$)/i, "MUST", "negative"],
  [/\bDon't\b(.+?)(?:\.|$)/, "MUST", "negative"],
  [/\bAvoid\b(.+?)(?:\.|$)/, "SHOULD", "negative"],
  [/\bPrefer\b(.+?)(?:\.|$)/, "SHOULD", "positive"],
  [/\bDefault\s+to\b(.+?)(?:\.|$)/, "SHOULD", "positive"],
  [/\bUse\b(.+?)(?:\.|$)/, "SHOULD", "positive"],
];

function slugify(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60);
}

function toolScope(filePath: string, line: string): "general" | "claude-code" | "codex" {
  const lower = line.toLowerCase();
  if (lower.includes("claude code") || lower.includes("claude-code") || filePath.includes(".claude/")) return "claude-code";
  if (lower.includes("codex") || filePath.includes(".codex/")) return "codex";
  return "general";
}

function extractSubject(text: string): { subject: string; predicate: string } {
  const trimmed = text.trim().replace(/^[,:\s]+/, "");
  const m = trimmed.match(/^(agents?|the agent|you|humans?|the human|bots?|reviewers?|teammates?)\s+(.+)/i);
  if (m) return { subject: m[1]!.toLowerCase(), predicate: m[2]!.trim() };
  return { subject: "agent", predicate: trimmed };
}

function extractWhen(line: string): string | null {
  const m = line.match(/\b(?:when|if|during|before|after|while|unless)\s+(.+?)(?:\s*[,.]|\s+(?:MUST|SHOULD|MAY|Never|Always|Do not))/i);
  return m ? m[1]!.trim() : null;
}

const results: Imperative[] = [];
const seenIds = new Set<string>();
const seenRaw = new Set<string>();
let inCodeBlock = false;

for (const filePath of files) {
  inCodeBlock = false;
  let content: string;
  try {
    content = readFileSync(filePath, "utf-8");
  } catch {
    process.stderr.write(`[warn] cannot read ${filePath}, skipping\n`);
    continue;
  }

  const lines = content.split("\n");
  const fileTags = [basename(filePath, ".md").toLowerCase().replace(/^(rule-|convention-)/, "")].filter(Boolean);
  const relPath = relative(process.cwd(), filePath);

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i] as string;

    if (line.startsWith("```")) { inCodeBlock = !inCodeBlock; continue; }
    if (inCodeBlock) continue;
    if (line.startsWith("<!--") || /^\|[\s-]+\|/.test(line) || line.startsWith("---")) continue;
    // Skip headings, table rows, and backtick-heavy lines
    if (/^#{1,6}\s/.test(line)) continue;
    if ((line.match(/`/g) || []).length > 3) continue;

    for (const [pattern, level, polarity] of PATTERNS) {
      const match = line.match(pattern);
      if (!match) continue;

      const raw = line.replace(/^[\s\-*>#]+/, "").trim();

      // Deduplicate by raw text (handles inlined rules appearing in multiple sources)
      if (seenRaw.has(raw)) break;
      seenRaw.add(raw);

      const when = extractWhen(line);
      let { subject, predicate } = extractSubject(match[1]!);

      // Strip the when-clause from predicate only if it appears at the end (after a "when" separator)
      if (when) {
        const whenIdx = predicate.toLowerCase().lastIndexOf(" when ");
        if (whenIdx > 20) {
          predicate = predicate.slice(0, whenIdx).trim();
        }
      }
      // Cap predicate length
      if (predicate.length > 100) {
        predicate = predicate.slice(0, 100).replace(/\s+\S*$/, "").trim();
      }
      // Skip if predicate is too short to be meaningful
      if (predicate.length < 10) break;

      const baseId = `${fileTags[0] || slugify(basename(filePath, ".md"))}:${slugify(predicate)}`;

      let id = baseId;
      let counter = 2;
      while (seenIds.has(id)) id = `${baseId}-${counter++}`;
      seenIds.add(id);

      results.push({
        id, level, polarity, subject, predicate, when,
        source: { file: relPath, line: i + 1 },
        tool_scope: toolScope(filePath, line),
        tags: fileTags,
        raw,
      });
      break;
    }
  }
}

const output = results.map((r) => JSON.stringify(r)).join("\n");

if (outputPath) {
  writeFileSync(outputPath, output + "\n", "utf-8");
  process.stderr.write(`Wrote ${results.length} imperatives to ${outputPath}\n`);
} else {
  if (output) console.log(output);
  process.stderr.write(`Total: ${results.length} imperatives from ${files.length} files\n`);
}
