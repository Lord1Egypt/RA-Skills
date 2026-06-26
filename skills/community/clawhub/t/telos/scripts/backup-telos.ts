#!/usr/bin/env bun
/**
 * backup-telos - Full backup and restore for ~/clawd/telos/
 *
 * Commands:
 *   backup [--name <label>]     Full snapshot of ~/clawd/telos/
 *   restore <backup-name>       Restore from a snapshot
 *   list                        List all snapshots
 *   history <file>              Show backup history for a single file
 *   restore-file <file> <ver>   Restore a specific file version from backups/
 *
 * Usage:
 *   bun backup-telos.ts backup
 *   bun backup-telos.ts backup --name "before-major-update"
 *   bun backup-telos.ts list
 *   bun backup-telos.ts restore telos-snapshot-20260320T120000
 *   bun backup-telos.ts history BELIEFS.md
 *   bun backup-telos.ts restore-file BELIEFS.md BELIEFS_20260320T120000.md
 */

import { existsSync, readdirSync, statSync, readFileSync, cpSync, mkdirSync, writeFileSync, rmSync } from "fs";
import { join, basename } from "path";
import { homedir } from "os";

// Resolve workspace: respect OPENCLAW_WORKSPACE env var (set by OpenClaw runtime)
// Falls back to ~/openclaw/telos for standard installs, or ~/clawd/telos for legacy
const _workspace = process.env.OPENCLAW_WORKSPACE || process.env.CLAWD_WORKSPACE || join(homedir(), "openclaw");
const TELOS_DIR = join(_workspace, "telos");
const BACKUPS_DIR = join(TELOS_DIR, "backups");
const SNAPSHOTS_DIR = join(_workspace, "telos-snapshots");
const SNAPSHOT_PREFIX = "telos-snapshot-";

function getTimestamp(): string {
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}T${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getDirSize(dir: string): number {
  let size = 0;
  try {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const p = join(dir, entry.name);
      if (entry.isDirectory()) size += getDirSize(p);
      else size += statSync(p).size;
    }
  } catch { /* ignore */ }
  return size;
}

function cmdBackup(customName?: string) {
  if (!existsSync(TELOS_DIR)) {
    console.error(`Telos directory not found: ${TELOS_DIR}`);
    console.error("Run init-telos.ts first.");
    process.exit(1);
  }

  mkdirSync(SNAPSHOTS_DIR, { recursive: true });
  const timestamp = getTimestamp();
  const name = customName ? `${SNAPSHOT_PREFIX}${customName}-${timestamp}` : `${SNAPSHOT_PREFIX}${timestamp}`;
  const snapshotPath = join(SNAPSHOTS_DIR, name);

  if (existsSync(snapshotPath)) {
    console.error(`Snapshot already exists: ${name}`);
    process.exit(1);
  }

  console.log(`Creating snapshot: ${name}`);
  cpSync(TELOS_DIR, snapshotPath, { recursive: true });

  const fileCount = readdirSync(snapshotPath).filter((f) => f.endsWith(".md")).length;
  const size = getDirSize(snapshotPath);

  console.log(`\nSnapshot complete:`);
  console.log(`  Files: ${fileCount}`);
  console.log(`  Size:  ${formatSize(size)}`);
  console.log(`  Path:  ${snapshotPath}`);
}

function cmdRestore(snapshotName: string) {
  const snapshotPath = snapshotName.startsWith("/")
    ? snapshotName
    : join(SNAPSHOTS_DIR, snapshotName.startsWith(SNAPSHOT_PREFIX) ? snapshotName : `${SNAPSHOT_PREFIX}${snapshotName}`);

  if (!existsSync(snapshotPath)) {
    console.error(`Snapshot not found: ${snapshotPath}`);
    cmdList();
    process.exit(1);
  }

  // Safety: backup current state before restoring
  if (existsSync(TELOS_DIR)) {
    const safetyName = `${SNAPSHOT_PREFIX}pre-restore-${getTimestamp()}`;
    const safetyPath = join(SNAPSHOTS_DIR, safetyName);
    mkdirSync(SNAPSHOTS_DIR, { recursive: true });
    cpSync(TELOS_DIR, safetyPath, { recursive: true });
    console.log(`Safety snapshot created: ${safetyName}`);
  }

  // Restore
  rmSync(TELOS_DIR, { recursive: true, force: true });
  cpSync(snapshotPath, TELOS_DIR, { recursive: true });
  console.log(`\nRestored from: ${basename(snapshotPath)}`);
  console.log(`Location: ${TELOS_DIR}`);
}

function cmdList() {
  if (!existsSync(SNAPSHOTS_DIR)) {
    console.log("No snapshots found.");
    return;
  }

  const snapshots = readdirSync(SNAPSHOTS_DIR)
    .filter((d) => d.startsWith(SNAPSHOT_PREFIX))
    .sort()
    .reverse();

  if (snapshots.length === 0) {
    console.log("No snapshots found.");
    return;
  }

  console.log("Telos snapshots:\n");
  for (const snap of snapshots) {
    const path = join(SNAPSHOTS_DIR, snap);
    const stats = statSync(path);
    const size = getDirSize(path);
    console.log(`  ${snap}`);
    console.log(`    Date: ${stats.mtime.toLocaleString()}  Size: ${formatSize(size)}`);
  }
  console.log(`\n  Total: ${snapshots.length} snapshot(s) in ${SNAPSHOTS_DIR}`);
}

function cmdHistory(filename: string) {
  if (!existsSync(BACKUPS_DIR)) {
    console.log("No file backups found.");
    return;
  }

  const prefix = filename.replace(".md", "");
  const backups = readdirSync(BACKUPS_DIR)
    .filter((f) => f.startsWith(prefix + "_") && f.endsWith(".md"))
    .sort()
    .reverse();

  if (backups.length === 0) {
    console.log(`No backups found for ${filename}`);
    return;
  }

  console.log(`Backup history for ${filename}:\n`);
  for (const backup of backups) {
    const path = join(BACKUPS_DIR, backup);
    const stats = statSync(path);
    console.log(`  ${backup}`);
    console.log(`    Date: ${stats.mtime.toLocaleString()}  Size: ${formatSize(stats.size)}`);
  }
  console.log(`\n  Total: ${backups.length} version(s)`);
  console.log(`  Restore with: bun backup-telos.ts restore-file ${filename} <version>`);
}

function cmdRestoreFile(filename: string, version: string) {
  const backupPath = join(BACKUPS_DIR, version);
  if (!existsSync(backupPath)) {
    console.error(`Backup not found: ${backupPath}`);
    cmdHistory(filename);
    process.exit(1);
  }

  const targetPath = join(TELOS_DIR, filename);

  // Backup current version before restoring
  if (existsSync(targetPath)) {
    mkdirSync(BACKUPS_DIR, { recursive: true });
    const timestamp = getTimestamp();
    const safetyBackup = `${filename.replace(".md", "")}_pre-restore_${timestamp}.md`;
    cpSync(targetPath, join(BACKUPS_DIR, safetyBackup));
    console.log(`Current version backed up: backups/${safetyBackup}`);
  }

  cpSync(backupPath, targetPath);
  console.log(`Restored ${filename} from ${version}`);
}

function printUsage() {
  console.log(`
Telos Backup & Restore

Commands:
  backup [--name <label>]     Full snapshot of ~/clawd/telos/
  restore <snapshot-name>     Restore from a snapshot
  list                        List all snapshots
  history <file>              Show backup history for a single file
  restore-file <file> <ver>   Restore a specific file version

Examples:
  bun backup-telos.ts backup
  bun backup-telos.ts backup --name "before-major-update"
  bun backup-telos.ts list
  bun backup-telos.ts restore telos-snapshot-20260320T120000
  bun backup-telos.ts history BELIEFS.md
  bun backup-telos.ts restore-file BELIEFS.md BELIEFS_20260320T120000.md
`);
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case "backup": {
    let name: string | undefined;
    const idx = args.indexOf("--name");
    if (idx !== -1 && args[idx + 1]) name = args[idx + 1];
    cmdBackup(name);
    break;
  }
  case "restore": {
    if (!args[1]) { console.error("Usage: bun backup-telos.ts restore <snapshot-name>"); process.exit(1); }
    cmdRestore(args[1]);
    break;
  }
  case "list":
    cmdList();
    break;
  case "history": {
    if (!args[1]) { console.error("Usage: bun backup-telos.ts history <filename>"); process.exit(1); }
    cmdHistory(args[1]);
    break;
  }
  case "restore-file": {
    if (!args[1] || !args[2]) { console.error("Usage: bun backup-telos.ts restore-file <file> <version>"); process.exit(1); }
    cmdRestoreFile(args[1], args[2]);
    break;
  }
  default:
    printUsage();
}
