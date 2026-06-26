#!/usr/bin/env bun
/**
 * init-telos - Initialize Telos by copying templates to ~/clawd/telos/
 *
 * Usage:
 *   bun init-telos.ts
 *
 * Copies all template files from assets/templates/ to ~/clawd/telos/
 * and creates the backups directory and updates.md log.
 */

import { existsSync, mkdirSync, readdirSync, copyFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { homedir } from "os";

// Resolve workspace: respect OPENCLAW_WORKSPACE env var (set by OpenClaw runtime)
// Falls back to ~/openclaw/telos for standard installs, or ~/clawd/telos for legacy
const _workspace = process.env.OPENCLAW_WORKSPACE || process.env.CLAWD_WORKSPACE || join(homedir(), "openclaw");
const TELOS_DIR = join(_workspace, "telos");
const BACKUPS_DIR = join(TELOS_DIR, "backups");
const UPDATES_FILE = join(TELOS_DIR, "updates.md");

// Resolve templates directory relative to this script
const SCRIPT_DIR = dirname(new URL(import.meta.url).pathname);
const TEMPLATES_DIR = join(SCRIPT_DIR, "..", "assets", "templates");

function main() {
  if (!existsSync(TEMPLATES_DIR)) {
    console.error(`Templates not found: ${TEMPLATES_DIR}`);
    process.exit(1);
  }

  // Create directories
  mkdirSync(TELOS_DIR, { recursive: true });
  mkdirSync(BACKUPS_DIR, { recursive: true });

  // Copy templates
  let copied = 0;
  let skipped = 0;
  for (const file of readdirSync(TEMPLATES_DIR)) {
    if (!file.endsWith(".md")) continue;
    const dst = join(TELOS_DIR, file);
    if (existsSync(dst)) {
      console.log(`  Exists, skipped: ${file}`);
      skipped++;
    } else {
      copyFileSync(join(TEMPLATES_DIR, file), dst);
      console.log(`  Copied: ${file}`);
      copied++;
    }
  }

  // Create updates.md if not exists
  if (!existsSync(UPDATES_FILE)) {
    const date = new Date().toISOString().split("T")[0];
    writeFileSync(UPDATES_FILE, `# TELOS Updates Log\n\n---\n\n## ${date}\n- [INIT] telos initialized\n`, "utf-8");
    console.log("  Created: updates.md");
  }

  console.log(`\nTelos initialized at ${TELOS_DIR}/`);
  console.log(`  ${copied} files copied, ${skipped} skipped (already exist).`);
  console.log("\nStart by filling MISSION.md, then GOALS.md and BELIEFS.md.");
  console.log('Say "setup telos" for guided onboarding.');
}

main();
