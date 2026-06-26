// memory-crystal/bulk-copy.ts — Copy raw session files to LDM transcripts.
// Idempotent: skips files that already exist with the same size.
// Raw files are NEVER modified (read-only copy).
//
// Used by: crystal init (bulk copy after discovery)
//          crystal backfill (ensure files are in LDM before embedding)

import { existsSync, mkdirSync, copyFileSync, statSync, readdirSync } from 'node:fs';
import { join, basename, relative } from 'node:path';
import { ldmPaths } from './ldm.js';

// ── Types ──

export interface BulkCopyResult {
  filesCopied: number;
  filesSkipped: number;    // already exist with same size
  bytesWritten: number;
  durationMs: number;
}

export interface BulkCopyOptions {
  workspace?: boolean;       // also copy workspace .md files
  workspaceSrc?: string;     // source dir for workspace (e.g. ~/.openclaw/workspace/)
}

// ── Bulk copy ──

/** Copy session JSONL files from source locations to LDM transcripts.
 *  sessionPaths: array of absolute paths to JSONL files.
 *  agentId: target agent in ~/.ldm/agents/{agentId}/.
 *  Returns copy stats. */
export function bulkCopyToLdm(
  sessionPaths: string[],
  agentId: string,
  options?: BulkCopyOptions
): BulkCopyResult {
  const start = Date.now();
  const paths = ldmPaths(agentId);
  let filesCopied = 0;
  let filesSkipped = 0;
  let bytesWritten = 0;

  // Ensure target directories exist
  mkdirSync(paths.transcripts, { recursive: true });

  // Copy session JSONLs
  for (const srcPath of sessionPaths) {
    const destPath = join(paths.transcripts, basename(srcPath));

    if (existsSync(destPath)) {
      try {
        const srcSize = statSync(srcPath).size;
        const destSize = statSync(destPath).size;
        if (srcSize === destSize) {
          filesSkipped++;
          continue;
        }
      } catch {}
    }

    try {
      copyFileSync(srcPath, destPath);
      bytesWritten += statSync(destPath).size;
      filesCopied++;
    } catch {
      // Skip files that fail to copy (non-fatal)
    }
  }

  // Copy workspace .md files (recursive, preserving structure)
  if (options?.workspace && options.workspaceSrc) {
    mkdirSync(paths.workspace, { recursive: true });
    const wsResult = copyWorkspaceRecursive(options.workspaceSrc, paths.workspace);
    filesCopied += wsResult.copied;
    filesSkipped += wsResult.skipped;
    bytesWritten += wsResult.bytes;
  }

  return {
    filesCopied,
    filesSkipped,
    bytesWritten,
    durationMs: Date.now() - start,
  };
}

// ── Workspace copy (recursive, preserves directory structure) ──

function copyWorkspaceRecursive(
  srcDir: string,
  destDir: string
): { copied: number; skipped: number; bytes: number } {
  let copied = 0;
  let skipped = 0;
  let bytes = 0;

  try {
    for (const entry of readdirSync(srcDir)) {
      // Skip hidden dirs and .git
      if (entry.startsWith('.')) continue;

      const srcPath = join(srcDir, entry);
      const destPath = join(destDir, entry);

      try {
        const stat = statSync(srcPath);

        if (stat.isDirectory()) {
          mkdirSync(destPath, { recursive: true });
          const sub = copyWorkspaceRecursive(srcPath, destPath);
          copied += sub.copied;
          skipped += sub.skipped;
          bytes += sub.bytes;
        } else if (entry.endsWith('.md')) {
          if (existsSync(destPath)) {
            try {
              if (stat.size === statSync(destPath).size) {
                skipped++;
                continue;
              }
            } catch {}
          }

          copyFileSync(srcPath, destPath);
          bytes += stat.size;
          copied++;
        }
      } catch { continue; }
    }
  } catch {}

  return { copied, skipped, bytes };
}
