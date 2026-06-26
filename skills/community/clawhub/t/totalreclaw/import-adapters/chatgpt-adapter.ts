import { BaseImportAdapter } from './base-adapter.js';
import type {
  ImportSource,
  AdapterParseResult,
  ConversationChunk,
  ProgressCallback,
} from './types.js';
import fs from 'node:fs';
import os from 'node:os';

// ── ChatGPT conversations.json types ────────────────────────────────────────

interface ChatGPTMessage {
  id: string;
  author: { role: 'user' | 'assistant' | 'system' | 'tool'; name?: string };
  content: {
    content_type: string;
    parts?: (string | null | Record<string, unknown>)[];
  };
  create_time?: number;
  metadata?: Record<string, unknown>;
}

interface ChatGPTMappingNode {
  id: string;
  message?: ChatGPTMessage | null;
  parent?: string | null;
  children: string[];
}

interface ChatGPTConversation {
  id?: string;
  title?: string;
  create_time?: number;
  update_time?: number;
  mapping: Record<string, ChatGPTMappingNode>;
}

/** Maximum messages per conversation chunk for LLM extraction. */
const CHUNK_SIZE = 20;

// ── ChatGPT Adapter ─────────────────────────────────────────────────────────

export class ChatGPTAdapter extends BaseImportAdapter {
  readonly source: ImportSource = 'chatgpt';
  readonly displayName = 'ChatGPT';

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
        'ChatGPT import requires either content (pasted text or JSON) or file_path. ' +
        'Export from ChatGPT: Settings -> Data Controls -> Export Data (conversations.json), ' +
        'or copy from Settings -> Personalization -> Memory -> Manage.',
      );
      return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
    }

    // Detect format: JSON array = conversations.json, plain text = memories
    const trimmed = content.trim();

    if (trimmed.startsWith('[') || trimmed.startsWith('{')) {
      // Try to parse as JSON (conversations.json or memory list)
      return this.parseConversationsJson(trimmed, warnings, errors, onProgress);
    }

    // Plain text: ChatGPT memories (one per line)
    return this.parseMemoriesText(trimmed, warnings, errors, onProgress);
  }

  /**
   * Parse ChatGPT conversations.json — full export with mapping tree.
   * Returns conversation chunks for LLM extraction (no pattern matching).
   */
  private parseConversationsJson(
    content: string,
    warnings: string[],
    errors: string[],
    onProgress?: ProgressCallback,
  ): AdapterParseResult {
    let conversations: ChatGPTConversation[];

    try {
      const data = JSON.parse(content);

      if (Array.isArray(data)) {
        conversations = data;
      } else if (data.conversations && Array.isArray(data.conversations)) {
        conversations = data.conversations;
      } else if (data.mapping) {
        // Single conversation object
        conversations = [data];
      } else {
        errors.push(
          'Unrecognized ChatGPT format. Expected an array of conversation objects (conversations.json) ' +
          'or plain text (ChatGPT memories).',
        );
        return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
      }
    } catch (e) {
      errors.push(`Failed to parse ChatGPT JSON: ${e instanceof Error ? e.message : 'Unknown error'}`);
      return { facts: [], chunks: [], totalMessages: 0, warnings, errors };
    }

    if (onProgress) {
      onProgress({
        current: 0,
        total: conversations.length,
        phase: 'parsing',
        message: `Parsing ${conversations.length} ChatGPT conversations...`,
      });
    }

    const chunks: ConversationChunk[] = [];
    let totalMessages = 0;
    let convIndex = 0;

    for (const conv of conversations) {
      if (!conv.mapping) {
        warnings.push(`Conversation "${conv.title || 'untitled'}" has no mapping — skipped`);
        continue;
      }

      // Extract user + assistant messages in chronological order
      const messages = this.extractMessages(conv.mapping);
      if (messages.length === 0) continue;

      totalMessages += messages.length;

      // Determine timestamp from first message or conversation
      const timestamp = conv.create_time
        ? new Date(conv.create_time * 1000).toISOString()
        : undefined;

      const title = conv.title || 'Untitled Conversation';

      // Chunk into batches of CHUNK_SIZE messages
      for (let i = 0; i < messages.length; i += CHUNK_SIZE) {
        const batch = messages.slice(i, i + CHUNK_SIZE);
        const chunkIndex = Math.floor(i / CHUNK_SIZE) + 1;
        const totalChunks = Math.ceil(messages.length / CHUNK_SIZE);

        chunks.push({
          title: totalChunks > 1 ? `${title} (part ${chunkIndex}/${totalChunks})` : title,
          messages: batch,
          timestamp,
        });
      }

      convIndex++;
      if (onProgress && convIndex % 50 === 0) {
        onProgress({
          current: convIndex,
          total: conversations.length,
          phase: 'parsing',
          message: `Parsed ${convIndex}/${conversations.length} conversations (${chunks.length} chunks, ${totalMessages} messages)...`,
        });
      }
    }

    if (chunks.length === 0 && conversations.length > 0) {
      warnings.push(
        `Parsed ${conversations.length} conversations but found no messages with text content.`,
      );
    }

    return {
      facts: [],
      chunks,
      totalMessages,
      warnings,
      errors,
      source_metadata: {
        format: 'conversations.json',
        conversations_count: conversations.length,
        chunks_count: chunks.length,
        total_messages: totalMessages,
      },
    };
  }

  /**
   * Parse ChatGPT memories — plain text, one memory per line.
   * Users copy this from Settings -> Personalization -> Memory -> Manage.
   *
   * Each line becomes a single-message conversation chunk for LLM extraction.
   */
  private parseMemoriesText(
    content: string,
    warnings: string[],
    errors: string[],
    onProgress?: ProgressCallback,
  ): AdapterParseResult {
    // Split by newlines and filter empty lines
    const lines = content.split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      // Skip common header lines
      .filter((line) => !/^(?:memories?|chatgpt memories?|my memories?|saved memories?):?\s*$/i.test(line));

    if (onProgress) {
      onProgress({
        current: 0,
        total: lines.length,
        phase: 'parsing',
        message: `Parsing ${lines.length} ChatGPT memories...`,
      });
    }

    // Clean lines: strip bullet/dash/number markers
    const cleanedLines = lines.map((line) =>
      line
        .replace(/^[-*\u2022]\s+/, '')        // bullet points
        .replace(/^\d+[.)]\s+/, '')            // numbered lists
        .trim(),
    ).filter((line) => line.length >= 3);

    // Group all memories into chunks of CHUNK_SIZE for efficient LLM extraction
    const chunks: ConversationChunk[] = [];
    for (let i = 0; i < cleanedLines.length; i += CHUNK_SIZE) {
      const batch = cleanedLines.slice(i, i + CHUNK_SIZE);
      chunks.push({
        title: `ChatGPT memories (${i + 1}-${Math.min(i + CHUNK_SIZE, cleanedLines.length)})`,
        messages: batch.map((text) => ({ role: 'user' as const, text })),
      });
    }

    return {
      facts: [],
      chunks,
      totalMessages: cleanedLines.length,
      warnings,
      errors,
      source_metadata: {
        format: 'memories-text',
        total_lines: lines.length,
        chunks_count: chunks.length,
      },
    };
  }

  /**
   * Traverse the mapping tree and extract user + assistant messages in chronological order.
   * Both roles are included because the assistant's response often provides context
   * that helps the LLM understand what the user meant.
   */
  private extractMessages(
    mapping: Record<string, ChatGPTMappingNode>,
  ): Array<{ role: 'user' | 'assistant'; text: string }> {
    // Find the root node (the one with no parent or parent not in mapping)
    let rootId: string | undefined;
    for (const [id, node] of Object.entries(mapping)) {
      if (!node.parent || !mapping[node.parent]) {
        rootId = id;
        break;
      }
    }

    if (!rootId) return [];

    // Walk the tree breadth-first, following children in order (main thread)
    const messages: Array<{ role: 'user' | 'assistant'; text: string }> = [];
    const visited = new Set<string>();
    const queue: string[] = [rootId];

    while (queue.length > 0) {
      const nodeId = queue.shift()!;
      if (visited.has(nodeId)) continue;
      visited.add(nodeId);

      const node = mapping[nodeId];
      if (!node) continue;

      const role = node.message?.author?.role;
      // Only collect user and assistant messages (skip system, tool)
      if (role === 'user' || role === 'assistant') {
        const textParts = this.extractTextFromParts(node.message?.content?.parts);
        if (textParts && textParts.length >= 3) {
          messages.push({ role, text: textParts });
        }
      }

      // Follow children (add them to queue in order)
      for (const childId of node.children || []) {
        queue.push(childId);
      }
    }

    return messages;
  }

  /**
   * Extract plain text from message content parts.
   * Parts can be strings, null, or complex objects (images, etc.) -- we only want strings.
   */
  private extractTextFromParts(parts?: (string | null | Record<string, unknown>)[]): string | null {
    if (!parts || parts.length === 0) return null;

    const textParts = parts
      .filter((p): p is string => typeof p === 'string' && p.trim().length > 0);

    if (textParts.length === 0) return null;

    return textParts.join(' ').trim();
  }
}
