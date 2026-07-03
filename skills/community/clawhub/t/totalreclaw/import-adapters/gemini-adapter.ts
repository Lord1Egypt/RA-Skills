import { BaseImportAdapter } from './base-adapter.js';
import type {
  ImportSource,
  AdapterParseResult,
  ConversationChunk,
  ProgressCallback,
} from './types.js';
import fs from 'node:fs';
import os from 'node:os';
import { createRequire } from 'node:module';

// All Gemini format parsing (MyActivity.json, legacy HTML, Saved-info paste)
// lives in the shared Rust core (`@totalreclaw/core` WASM) so the logic —
// including the locale-robust, lossless timestamp handling — is identical across
// every client (Python/Hermes via PyO3, TS via WASM). This adapter is a thin
// shim: it owns only file I/O + the size/RAM preflight, then delegates parsing.
const requireWasm = createRequire(import.meta.url);
let _wasm: typeof import('@totalreclaw/core') | null = null;
function getWasm() {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core');
  return _wasm!;
}

/** Shape returned by core `parseGemini` (serde -> JS object, snake_case). */
interface CoreParseResult {
  chunks: ConversationChunk[];
  total_messages: number;
  warnings: string[];
  errors: string[];
  format: string;
  records_count?: number;
  skipped?: number;
}

export class GeminiAdapter extends BaseImportAdapter {
  readonly source: ImportSource = 'gemini';
  readonly displayName = 'Google Gemini';

  async parse(
    input: { content?: string; file_path?: string },
    onProgress?: ProgressCallback,
  ): Promise<AdapterParseResult> {
    const warnings: string[] = [];
    const errors: string[] = [];

    let content: string;

    if (input.content) {
      content = input.content;
    } else if (input.file_path) {
      try {
        const resolved = input.file_path.replace(/^~/, os.homedir());
        const fileStat = fs.statSync(resolved);
        const fileSizeMB = fileStat.size / (1024 * 1024);
        if (fileSizeMB > 500) {
          errors.push(
            `File is too large to import: ${fileSizeMB.toFixed(1)}MB exceeds the 500MB cap. ` +
            'Split the file into smaller chunks and import each separately.',
          );
          return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
        }
        const freeMem = os.freemem();
        if (freeMem < fileStat.size * 2) {
          errors.push(
            `Not enough free memory: ${(freeMem / (1024 * 1024)).toFixed(0)}MB available, ` +
            `~${Math.ceil(fileStat.size * 2 / (1024 * 1024))}MB needed (2× file size). ` +
            'Close other applications or split the file.',
          );
          return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
        }
        content = fs.readFileSync(resolved, 'utf-8');
      } catch (e) {
        errors.push(`Failed to read file: ${e instanceof Error ? e.message : 'Unknown error'}`);
        return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
      }
    } else {
      errors.push(
        'Gemini import requires either content or file_path. ' +
        'Export from Google Takeout: takeout.google.com → "My Activity" → "Gemini Apps". ' +
        'Provide the "My Activity.html" (or MyActivity.json) file path, or paste your Saved info.',
      );
      return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
    }

    if (onProgress) {
      onProgress({ current: 0, total: 0, phase: 'parsing', message: 'Parsing Gemini export...' });
    }

    // Delegate ALL format parsing to the shared core.
    const result = getWasm().parseGemini(content) as CoreParseResult;

    if (onProgress) {
      onProgress({
        current: result.chunks.length,
        total: result.chunks.length,
        phase: 'parsing',
        message: `Parsed ${result.total_messages} messages into ${result.chunks.length} chunks`,
      });
    }

    return {
      facts: [],
      chunks: result.chunks,
      totalMessages: result.total_messages,
      warnings: [...warnings, ...result.warnings],
      errors: [...errors, ...result.errors],
      source_metadata: {
        format: result.format,
        chunks_count: result.chunks.length,
        total_messages: result.total_messages,
        ...(result.records_count ? { records_count: result.records_count } : {}),
        ...(result.skipped ? { skipped_non_gemini: result.skipped } : {}),
      },
    };
  }
}
