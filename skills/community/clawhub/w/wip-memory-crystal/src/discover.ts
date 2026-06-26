// memory-crystal/discover.ts — Per-harness session discovery.
// Detects which agent platforms are installed on THIS machine and
// returns their session file locations. Does NOT look for other agents' data.
//
// Used by: crystal init (to offer bulk copy of raw files to LDM)
//          crystal backfill (to find files to embed)

import { existsSync, readdirSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';

const HOME = process.env.HOME || '';

// ── Types ──

export interface HarnessInfo {
  platform: 'claude-code' | 'openclaw';
  sessionDir: string;          // directory containing JSONL session files
  workspaceDir?: string;       // OpenClaw workspace (md files, only for openclaw)
  filePattern: string;          // glob pattern description
  agentIdDefault: string;       // suggested agent ID for this harness
}

export interface DiscoveryBreakdown {
  platform: string;
  files: number;
  sizeBytes: number;
  sessionPaths: string[];       // actual file paths found
}

export interface DiscoveryResult {
  harnesses: HarnessInfo[];
  totalFiles: number;
  totalSizeBytes: number;
  breakdown: DiscoveryBreakdown[];
}

// ── Harness detection ──

/** Detect which agent platforms are installed on this machine. */
export function discoverHarnesses(): HarnessInfo[] {
  const found: HarnessInfo[] = [];

  // Claude Code: check ~/.claude/projects/ for subdirs with *.jsonl
  const ccProjectsDir = join(HOME, '.claude', 'projects');
  if (existsSync(ccProjectsDir)) {
    // Check if any project dir has JSONL files
    let hasJsonl = false;
    try {
      for (const entry of readdirSync(ccProjectsDir)) {
        const dirPath = join(ccProjectsDir, entry);
        try {
          if (!statSync(dirPath).isDirectory()) continue;
          for (const file of readdirSync(dirPath)) {
            if (file.endsWith('.jsonl') && !file.startsWith('.')) {
              hasJsonl = true;
              break;
            }
          }
          if (hasJsonl) break;
        } catch { continue; }
      }
    } catch {}

    if (hasJsonl) {
      found.push({
        platform: 'claude-code',
        sessionDir: ccProjectsDir,
        filePattern: '*.jsonl',
        agentIdDefault: 'cc-mini',
      });
    }
  }

  // OpenClaw: check ~/.openclaw/agents/*/sessions/ for *.jsonl
  const ocAgentsDir = join(HOME, '.openclaw', 'agents');
  if (existsSync(ocAgentsDir)) {
    try {
      for (const agentDir of readdirSync(ocAgentsDir)) {
        const sessionsDir = join(ocAgentsDir, agentDir, 'sessions');
        if (!existsSync(sessionsDir)) continue;

        let hasJsonl = false;
        try {
          for (const file of readdirSync(sessionsDir)) {
            if (file.endsWith('.jsonl') && !file.startsWith('.')) {
              hasJsonl = true;
              break;
            }
          }
        } catch { continue; }

        if (hasJsonl) {
          const workspaceDir = join(HOME, '.openclaw', 'workspace');
          found.push({
            platform: 'openclaw',
            sessionDir: sessionsDir,
            workspaceDir: existsSync(workspaceDir) ? workspaceDir : undefined,
            filePattern: '*.jsonl',
            agentIdDefault: `oc-lesa-mini`,
          });
        }
      }
    } catch {}
  }

  return found;
}

// ── File discovery ──

/** Discover all session JSONL files for a given harness. */
export function discoverSessionFiles(harness: HarnessInfo): string[] {
  const files: string[] = [];

  if (harness.platform === 'claude-code') {
    // Claude Code stores sessions in ~/.claude/projects/{project-name}/*.jsonl
    if (!existsSync(harness.sessionDir)) return files;
    try {
      for (const projectDir of readdirSync(harness.sessionDir)) {
        const projectPath = join(harness.sessionDir, projectDir);
        try {
          if (!statSync(projectPath).isDirectory()) continue;
        } catch { continue; }

        try {
          for (const file of readdirSync(projectPath)) {
            if (file.endsWith('.jsonl') && !file.startsWith('.')) {
              files.push(join(projectPath, file));
            }
          }
        } catch { continue; }
      }
    } catch {}
  } else if (harness.platform === 'openclaw') {
    // OpenClaw stores sessions in the sessionsDir directly
    if (!existsSync(harness.sessionDir)) return files;
    try {
      for (const file of readdirSync(harness.sessionDir)) {
        if (file.endsWith('.jsonl') && !file.startsWith('.')) {
          files.push(join(harness.sessionDir, file));
        }
      }
    } catch {}
  }

  return files;
}

/** Discover workspace .md files for OpenClaw harness. */
export function discoverWorkspaceFiles(harness: HarnessInfo): string[] {
  if (!harness.workspaceDir || !existsSync(harness.workspaceDir)) return [];

  const files: string[] = [];
  walkMdFiles(harness.workspaceDir, files);
  return files;
}

function walkMdFiles(dir: string, results: string[]): void {
  try {
    for (const entry of readdirSync(dir)) {
      // Skip hidden dirs and .git
      if (entry.startsWith('.')) continue;
      const fullPath = join(dir, entry);
      try {
        const stat = statSync(fullPath);
        if (stat.isDirectory()) {
          walkMdFiles(fullPath, results);
        } else if (entry.endsWith('.md')) {
          results.push(fullPath);
        }
      } catch { continue; }
    }
  } catch {}
}

// ── Full discovery ──

/** Run full discovery: detect harnesses, find all files, compute sizes. */
export function discoverAll(): DiscoveryResult {
  const harnesses = discoverHarnesses();
  const breakdown: DiscoveryBreakdown[] = [];
  let totalFiles = 0;
  let totalSizeBytes = 0;

  for (const harness of harnesses) {
    const sessionPaths = discoverSessionFiles(harness);
    let sizeBytes = 0;

    for (const filePath of sessionPaths) {
      try {
        sizeBytes += statSync(filePath).size;
      } catch {}
    }

    // Include workspace files for OpenClaw
    const workspacePaths = discoverWorkspaceFiles(harness);
    for (const filePath of workspacePaths) {
      try {
        sizeBytes += statSync(filePath).size;
      } catch {}
    }

    const allPaths = [...sessionPaths, ...workspacePaths];
    breakdown.push({
      platform: harness.platform,
      files: allPaths.length,
      sizeBytes,
      sessionPaths: allPaths,
    });

    totalFiles += allPaths.length;
    totalSizeBytes += sizeBytes;
  }

  return { harnesses, totalFiles, totalSizeBytes, breakdown };
}

// ── Formatting helpers ──

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)}KB`;
  if (bytes < 1073741824) return `${(bytes / 1048576).toFixed(1)}MB`;
  return `${(bytes / 1073741824).toFixed(1)}GB`;
}
