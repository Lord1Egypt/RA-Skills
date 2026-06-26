import { BaseImportAdapter } from './base-adapter.js';
import type {
  ImportSource,
  AdapterParseResult,
  ConversationChunk,
  ProgressCallback,
} from './types.js';
import fs from 'node:fs';
import os from 'node:os';

/**
 * Pattern for lines that start with a date prefix.
 * Claude memory entries sometimes have: [2026-03-15] - User prefers TypeScript
 */
const DATE_PREFIX_RE = /^\[(\d{4}-\d{2}-\d{2})\]\s*[-:]\s*/;

/**
 * Pattern for bullet-prefixed lines.
 */
const BULLET_PREFIX_RE = /^[-*\u2022]\s+/;

/**
 * Pattern for numbered list lines.
 */
const NUMBERED_PREFIX_RE = /^\d+[.)]\s+/;

/** Maximum messages per conversation chunk for LLM extraction. */
const CHUNK_SIZE = 20;

export class ClaudeAdapter extends BaseImportAdapter {
  readonly source: ImportSource = 'claude';
  readonly displayName = 'Claude';

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
        const resolvedPath = input.file_path.replace(/^~/, os.homedir());
        const fileStat = fs.statSync(resolvedPath);
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
        content = fs.readFileSync(resolvedPath, 'utf-8');
      } catch (e) {
        errors.push(`Failed to read file: ${e instanceof Error ? e.message : 'Unknown error'}`);
        return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
      }
    } else {
      errors.push(
        'Claude import requires either content (pasted text) or file_path. ' +
        'Copy your memories from Claude: Settings -> Memory -> select all and copy.',
      );
      return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
    }

    // Claude memory export is plain text, one fact per line.
    return this.parseMemoriesText(content.trim(), warnings, errors, onProgress);
  }

  /**
   * Parse Claude memories — plain text, one memory per line.
   * Returns conversation chunks for LLM extraction (no pattern matching).
   *
   * Each line is cleaned (date prefixes, bullets, numbers stripped) and
   * grouped into chunks for the LLM to process.
   */
  private parseMemoriesText(
    content: string,
    warnings: string[],
    errors: string[],
    onProgress?: ProgressCallback,
  ): AdapterParseResult {
    // Split by newlines and filter
    const lines = content.split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      // Skip common header lines
      .filter((line) => !/^(?:memories?|claude memories?|my memories?|saved memories?):?\s*$/i.test(line));

    if (onProgress) {
      onProgress({
        current: 0,
        total: lines.length,
        phase: 'parsing',
        message: `Parsing ${lines.length} Claude memories...`,
      });
    }

    // Clean each line: extract date, strip formatting
    const cleanedEntries: Array<{ text: string; timestamp?: string }> = [];
    for (const line of lines) {
      let cleaned = line;
      let timestamp: string | undefined;

      // Extract date prefix if present
      const dateMatch = cleaned.match(DATE_PREFIX_RE);
      if (dateMatch) {
        timestamp = dateMatch[1];
        cleaned = cleaned.replace(DATE_PREFIX_RE, '');
      }

      // Strip bullet/numbering markers
      cleaned = cleaned
        .replace(BULLET_PREFIX_RE, '')
        .replace(NUMBERED_PREFIX_RE, '')
        .trim();

      if (cleaned.length >= 3) {
        cleanedEntries.push({ text: cleaned, timestamp });
      }
    }

    // Group memories into chunks of CHUNK_SIZE for efficient LLM extraction
    const chunks: ConversationChunk[] = [];
    for (let i = 0; i < cleanedEntries.length; i += CHUNK_SIZE) {
      const batch = cleanedEntries.slice(i, i + CHUNK_SIZE);

      // Use the timestamp from the first entry in the batch (if available)
      const batchTimestamp = batch.find((e) => e.timestamp)?.timestamp;

      chunks.push({
        title: `Claude memories (${i + 1}-${Math.min(i + CHUNK_SIZE, cleanedEntries.length)})`,
        messages: batch.map((entry) => ({ role: 'user' as const, text: entry.text })),
        timestamp: batchTimestamp,
      });
    }

    return {
      facts: [],
      chunks,
      totalMessages: cleanedEntries.length,
      warnings,
      errors,
      source_metadata: {
        format: 'memories-text',
        total_lines: lines.length,
        chunks_count: chunks.length,
      },
    };
  }
}
