#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import {
  parseArgs,
  localDateStamp,
  stripBom,
  sanitizeEntry,
  parseExistingSections,
  buildExistingIndex,
  findExistingMatch,
  findSectionByTitle,
  formatEntry,
  spliceBulletsIntoSection,
  normalizeText,
  tokenize,
} from "./lib/memory.mjs";

async function readMemoryFile(memoryPath, dateStamp) {
  try {
    const text = stripBom(await fs.readFile(memoryPath, "utf8"));
    return { text, createdFile: false };
  } catch (error) {
    if (error && typeof error === "object" && error.code === "ENOENT") {
      return { text: `# ${dateStamp}\n`, createdFile: true };
    }
    throw error;
  }
}

function ensureTrailingBlankLine(text) {
  let out = text;
  if (!out.trim()) {
    return out;
  }
  if (!out.endsWith("\n")) out += "\n";
  if (!out.endsWith("\n\n")) out += "\n";
  return out;
}

function appendIndexEntry(existingIndex, entry) {
  const titleKey = normalizeText(entry.title);
  const titleTokens = tokenize(entry.title);
  const bulletKeys = new Set(entry.bullets.map((bullet) => normalizeText(bullet)).filter(Boolean));
  existingIndex.bySection.push({
    titleKey,
    titleTokens,
    bulletKeys,
    sectionIndex: existingIndex.bySection.length,
    title: entry.title,
    time: "",
  });
  for (const bulletKey of bulletKeys) {
    existingIndex.allBulletKeys.add(bulletKey);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const entriesFileArg = args["entries-file"];
  if (!entriesFileArg || typeof entriesFileArg !== "string") {
    throw new Error("Missing required --entries-file");
  }

  const cwd = process.cwd();
  const now = new Date();
  const dateStamp = typeof args.date === "string" ? args.date : localDateStamp(now);
  const entriesFile = path.resolve(cwd, entriesFileArg);
  const memoryPath = typeof args["memory-path"] === "string"
    ? path.resolve(cwd, args["memory-path"])
    : path.resolve(cwd, "memory", `${dateStamp}.md`);
  const allowMerge = args["allow-merge"] !== "false" && args["allow-merge"] !== false;

  const entriesRaw = stripBom(await fs.readFile(entriesFile, "utf8"));
  const parsedEntries = JSON.parse(entriesRaw);
  const entries = Array.isArray(parsedEntries)
    ? parsedEntries.map(sanitizeEntry).filter(Boolean)
    : [];

  const { text: existingText, createdFile } = await readMemoryFile(memoryPath, dateStamp);
  let { sections, lines } = parseExistingSections(existingText);
  let existingIndex = buildExistingIndex(sections);

  const addedEntries = [];
  const mergedTitles = [];
  const skippedTitles = [];
  const fallbackAdded = [];
  const fallbackSkipped = [];
  const reasonByTitle = {};
  let mergedBullets = 0;

  function recordSkip(title, reason) {
    skippedTitles.push(title);
    reasonByTitle[title] = reason;
  }

  // Pass 1: handle merges in-place over `lines`. We rebuild sections/index after each
  // merge so subsequent merge_target_title lookups remain accurate.
  // Add/Skip are deferred to pass 2.
  const adds = [];
  for (const entry of entries) {
    if (entry.action === "skip") {
      recordSkip(entry.title, "agent");
      continue;
    }
    if (entry.action === "merge") {
      if (!allowMerge || !entry.mergeTargetTitle) {
        adds.push({ ...entry, action: "add" });
        fallbackAdded.push(entry.title);
        reasonByTitle[entry.title] = "merge-disallowed-or-empty-target";
        continue;
      }
      const target = findSectionByTitle(entry.mergeTargetTitle, existingIndex);
      if (!target) {
        adds.push({ ...entry, action: "add" });
        fallbackAdded.push(entry.title);
        reasonByTitle[entry.title] = "merge-target-missing";
        continue;
      }
      const targetSection = sections[target.sectionIndex];
      const { newLines, addedBullets } = spliceBulletsIntoSection(
        lines,
        targetSection,
        entry.bullets,
        now,
      );
      if (addedBullets.length === 0) {
        recordSkip(entry.title, "all-bullets-duplicate");
        continue;
      }
      lines = newLines;
      mergedTitles.push(entry.title);
      mergedBullets += addedBullets.length;
      reasonByTitle[entry.title] = "merged";
      // Reparse so following entries see updated state.
      const reparsed = parseExistingSections(lines.join("\n"));
      sections = reparsed.sections;
      lines = reparsed.lines;
      existingIndex = buildExistingIndex(sections);
      continue;
    }
    // default: add
    adds.push(entry);
  }

  // Pass 2: handle adds with Jaccard fallback dedup against current state.
  for (const entry of adds) {
    const match = findExistingMatch(entry, existingIndex);
    if (match.duplicate) {
      fallbackSkipped.push(entry.title);
      reasonByTitle[entry.title] = `jaccard:${match.reason}`;
      continue;
    }
    addedEntries.push(entry);
    reasonByTitle[entry.title] ??= "added";
    appendIndexEntry(existingIndex, entry);
  }

  // Render. If we mutated lines (merges) or have adds, write the file.
  const hasMerges = mergedTitles.length > 0;
  const hasAdds = addedEntries.length > 0;

  if (hasMerges || hasAdds) {
    await fs.mkdir(path.dirname(memoryPath), { recursive: true });
    let nextText = lines.join("\n");
    if (hasAdds) {
      nextText = ensureTrailingBlankLine(nextText);
      const blocks = addedEntries.map((entry) => formatEntry(entry, now));
      if (!nextText.trim()) {
        nextText = `# ${dateStamp}\n\n`;
      }
      nextText += `${blocks.join("\n\n")}\n`;
    }
    if (!nextText.endsWith("\n")) nextText += "\n";
    await fs.writeFile(memoryPath, nextText, "utf8");
  }

  const result = {
    memoryPath,
    createdFile: createdFile && (hasMerges || hasAdds),
    added: addedEntries.length,
    skipped: skippedTitles.length,
    merged: mergedTitles.length,
    mergedBullets,
    addedTitles: addedEntries.map((entry) => entry.title),
    skippedTitles,
    mergedTitles,
    fallbackAdded,
    fallbackSkipped,
    reasonByTitle,
  };

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
  process.exit(1);
});
