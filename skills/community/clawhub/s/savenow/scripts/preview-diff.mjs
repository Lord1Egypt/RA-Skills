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
  findSectionByTitle,
  topJaccardMatches,
  normalizeText,
  tokenize,
  jaccard,
} from "./lib/memory.mjs";

function summarizeCounts(entries) {
  const counts = { add: 0, merge: 0, skip: 0 };
  for (const entry of entries) {
    counts[entry.action] = (counts[entry.action] ?? 0) + 1;
  }
  return counts;
}

function formatTimeOrEmpty(time) {
  return time ? ` (${time})` : "";
}

function renderEntry(entry, index, existingIndex) {
  const lines = [];
  const num = index + 1;
  const reasonLine = entry.reason ? `_reason: ${entry.reason}_` : null;

  if (entry.action === "add") {
    lines.push(`**${num}. ADD — ${entry.title}**`);
    for (const bullet of entry.bullets) {
      lines.push(`- ${bullet}`);
    }
    const matches = topJaccardMatches(entry, existingIndex, 2, 0.4);
    if (matches.length === 0) {
      lines.push(`_compared against:_ (no close match above 0.4)`);
    } else {
      const parts = matches.map(
        (m) => `"${m.section.title}"${formatTimeOrEmpty(m.section.time)} — sim ${m.similarity.toFixed(2)}`,
      );
      lines.push(`_compared against:_ ${parts.join("; ")}`);
    }
    if (reasonLine) lines.push(reasonLine);
    return lines.join("\n");
  }

  if (entry.action === "merge") {
    const target = entry.mergeTargetTitle
      ? findSectionByTitle(entry.mergeTargetTitle, existingIndex)
      : null;
    if (!target) {
      lines.push(`**${num}. MERGE → ADD (fallback) — ${entry.title}**`);
      lines.push(
        `_target_: "${entry.mergeTargetTitle || "(empty)"}" not found in today's memory — will add as new section._`,
      );
      if (reasonLine) lines.push(reasonLine);
      for (const bullet of entry.bullets) {
        lines.push(`- ${bullet}`);
      }
      return lines.join("\n");
    }
    lines.push(
      `**${num}. MERGE — ${entry.title} → existing "${target.title}"${formatTimeOrEmpty(target.time)}**`,
    );
    if (reasonLine) lines.push(reasonLine);
    const newBullets = entry.bullets.filter(
      (bullet) => !target.bulletKeys.has(normalizeText(bullet)),
    );
    const dupCount = entry.bullets.length - newBullets.length;
    if (newBullets.length === 0) {
      lines.push(`_all ${entry.bullets.length} bullet(s) already present — will be skipped by merge._`);
    } else {
      lines.push("new bullets:");
      for (const bullet of newBullets) {
        lines.push(`- ${bullet}`);
      }
      if (dupCount > 0) {
        lines.push(`_(${dupCount} duplicate bullet${dupCount === 1 ? "" : "s"} will be skipped by script)_`);
      }
    }
    return lines.join("\n");
  }

  // skip
  lines.push(`**${num}. SKIP — ${entry.title}**`);
  if (reasonLine) lines.push(reasonLine);
  const matches = topJaccardMatches(entry, existingIndex, 1, 0.2);
  if (matches.length === 0) {
    lines.push(`_(closest existing: none — agent skipped on judgement)_`);
  } else {
    const m = matches[0];
    lines.push(
      `_(closest existing: "${m.section.title}" — title sim ${m.similarity.toFixed(2)})_`,
    );
  }
  return lines.join("\n");
}

function renderPreview(entries, memoryPath, existingIndex, ttlMinutes) {
  const relMemory = path.relative(process.cwd(), memoryPath) || memoryPath;
  if (entries.length === 0) {
    return [
      `### /savenow preview — ${relMemory}`,
      "",
      `**0 candidates** — nothing durable in this session. No write performed.`,
      "",
    ].join("\n");
  }
  const counts = summarizeCounts(entries);
  const header = [
    `### /savenow preview — ${relMemory}`,
    "",
    `**${entries.length} candidate${entries.length === 1 ? "" : "s"}** → ${counts.add} add, ${counts.merge} merge, ${counts.skip} skip. No write performed.`,
    "",
    "---",
    "",
    "",
  ].join("\n");

  const blocks = entries.map((entry, idx) => renderEntry(entry, idx, existingIndex));

  const footer = [
    "",
    "",
    "---",
    "",
    `Buttons expire in ${ttlMinutes} min. Or \`/savenow auto\` next time to skip preview.`,
    "",
  ].join("\n");

  return header + blocks.join("\n\n") + footer;
}

async function readMemoryText(memoryPath) {
  try {
    return stripBom(await fs.readFile(memoryPath, "utf8"));
  } catch (error) {
    if (error && typeof error === "object" && error.code === "ENOENT") return "";
    throw error;
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
  const pendingFile = typeof args["pending-file"] === "string"
    ? path.resolve(cwd, args["pending-file"])
    : null;
  const ttlMinutes = Number.isFinite(Number(args["ttl-minutes"]))
    ? Number(args["ttl-minutes"])
    : 30;
  const sessionKey = typeof args["session-key"] === "string" ? args["session-key"] : "";
  const messageThreadId = typeof args["message-thread-id"] === "string"
    ? args["message-thread-id"]
    : "";

  const entriesRaw = stripBom(await fs.readFile(entriesFile, "utf8"));
  const parsedEntries = JSON.parse(entriesRaw);
  const entries = Array.isArray(parsedEntries)
    ? parsedEntries.map(sanitizeEntry).filter(Boolean)
    : [];

  const existingText = await readMemoryText(memoryPath);
  const { sections } = parseExistingSections(existingText);
  const existingIndex = buildExistingIndex(sections);

  const markdown = renderPreview(entries, memoryPath, existingIndex, ttlMinutes);
  process.stdout.write(markdown);
  if (!markdown.endsWith("\n")) process.stdout.write("\n");

  if (pendingFile && entries.length > 0) {
    const expiresAt = new Date(now.getTime() + ttlMinutes * 60 * 1000);
    const pending = {
      version: 1,
      sessionKey,
      messageThreadId,
      generatedAt: now.toISOString(),
      expiresAt: expiresAt.toISOString(),
      memoryPath,
      entriesFile,
      entries: parsedEntries,
    };
    await fs.mkdir(path.dirname(pendingFile), { recursive: true });
    await fs.writeFile(pendingFile, `${JSON.stringify(pending, null, 2)}\n`, "utf8");
    process.stderr.write(`pending written: ${pendingFile}\n`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
  process.exit(1);
});
