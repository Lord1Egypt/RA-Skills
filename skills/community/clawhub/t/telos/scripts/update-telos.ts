#!/usr/bin/env bun
/**
 * update-telos - Update Telos life context with automatic backups and change tracking
 *
 * Usage:
 *   bun update-telos.ts <file> "<content>" "<change-description>"
 *
 * Example:
 *   bun update-telos.ts BOOKS.md "- *Project Hail Mary* by Andy Weir — survival through science" "Added favorite book"
 *
 * Valid files:
 *   BELIEFS.md, BOOKS.md, CHALLENGES.md, FRAMES.md, GOALS.md, IDEAS.md,
 *   LEARNED.md, MISSION.md, MODELS.md, MOVIES.md, NARRATIVES.md,
 *   PREDICTIONS.md, PROBLEMS.md, PROJECTS.md, STATUS.md, STRATEGIES.md,
 *   TELOS.md, TRAUMAS.md, WISDOM.md, WRONG.md
 */

import { readFileSync, writeFileSync, copyFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";

// Resolve workspace: respect OPENCLAW_WORKSPACE env var (set by OpenClaw runtime)
// Falls back to ~/openclaw/telos for standard installs, or ~/clawd/telos for legacy
const _workspace = process.env.OPENCLAW_WORKSPACE || process.env.CLAWD_WORKSPACE || join(homedir(), "openclaw");
const TELOS_DIR = join(_workspace, "telos");
const BACKUPS_DIR = join(TELOS_DIR, "backups");
const UPDATES_FILE = join(TELOS_DIR, "updates.md");

const VALID_FILES = [
  "BELIEFS.md", "BOOKS.md", "CHALLENGES.md", "FRAMES.md", "GOALS.md", "IDEAS.md",
  "LEARNED.md", "MISSION.md", "MODELS.md", "MOVIES.md", "NARRATIVES.md",
  "PREDICTIONS.md", "PROBLEMS.md", "PROJECTS.md", "STATUS.md", "STRATEGIES.md",
  "TELOS.md", "TRAUMAS.md", "WISDOM.md", "WRONG.md",
];

function getTimestamp(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}T${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
}

function getDateForLog(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`;
}

function main() {
  const args = process.argv.slice(2);

  if (args.length < 3) {
    console.error('Usage: bun update-telos.ts <file> "<content>" "<change-description>"');
    console.error('\nExample: bun update-telos.ts BOOKS.md "- *Dune* by Frank Herbert" "Added favorite book"');
    console.error("\nValid files:", VALID_FILES.join(", "));
    process.exit(1);
  }

  const [filename, content, changeDescription] = args;

  if (!VALID_FILES.includes(filename)) {
    console.error(`Invalid file: ${filename}`);
    console.error(`Valid files: ${VALID_FILES.join(", ")}`);
    process.exit(1);
  }

  if (!existsSync(TELOS_DIR)) {
    console.error(`Telos directory not found: ${TELOS_DIR}`);
    console.error("Run: bun init-telos.ts");
    process.exit(1);
  }

  const targetFile = join(TELOS_DIR, filename);
  if (!existsSync(targetFile)) {
    console.error(`File not found: ${targetFile}`);
    process.exit(1);
  }

  // 1. Create timestamped backup
  if (!existsSync(BACKUPS_DIR)) mkdirSync(BACKUPS_DIR, { recursive: true });
  const timestamp = getTimestamp();
  const backupFilename = `${filename.replace(".md", "")}_${timestamp}.md`;
  const backupPath = join(BACKUPS_DIR, backupFilename);

  try {
    copyFileSync(targetFile, backupPath);
    console.log(`Backup: backups/${backupFilename}`);
  } catch (error) {
    console.error(`Failed to create backup: ${error}`);
    process.exit(1);
  }

  // 2. Append content (never overwrite)
  try {
    const current = readFileSync(targetFile, "utf-8");
    writeFileSync(targetFile, current.trimEnd() + "\n\n" + content + "\n", "utf-8");
    console.log(`Updated: ${filename}`);
  } catch (error) {
    console.error(`Failed to update: ${error}`);
    process.exit(1);
  }

  // 3. Log change to updates.md
  try {
    const logDate = getDateForLog();
    const logEntry = `\n## ${logDate}\n- [${filename}] ${changeDescription}\n`;

    if (existsSync(UPDATES_FILE)) {
      const updates = readFileSync(UPDATES_FILE, "utf-8");
      writeFileSync(UPDATES_FILE, updates.trimEnd() + "\n" + logEntry, "utf-8");
    } else {
      writeFileSync(UPDATES_FILE, `# TELOS Updates Log\n\n---\n${logEntry}`, "utf-8");
    }
    console.log("Logged in updates.md");
  } catch (error) {
    console.error(`Failed to log change: ${error}`);
  }

  console.log(`\nDone: ${filename} — ${changeDescription}`);
}

main();
