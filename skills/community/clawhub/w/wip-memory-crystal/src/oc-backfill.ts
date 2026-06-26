// memory-crystal/oc-backfill.ts — OpenClaw JSONL session parser.
// Parses OpenClaw session files into ExtractedMessage format for backfill ingestion.
// OpenClaw JSONL format differs from Claude Code:
//   - type: "message" (not "user"/"assistant")
//   - message.content is always an array of blocks [{type: "text", text: "..."}]
//   - Has metadata lines: type: "session", "model_change", "thinking_level_change", "custom"

import { existsSync, statSync, openSync, readSync, closeSync } from 'node:fs';

// Same interface as cc-poller.ts ExtractedMessage
export interface ExtractedMessage {
  role: string;
  text: string;
  timestamp: string;
  sessionId: string;
}

/** Extract messages from an OpenClaw session JSONL file.
 *  Reads from lastByteOffset for incremental processing.
 *  Returns extracted messages and new byte offset. */
export function extractOpenClawMessages(
  filePath: string,
  lastByteOffset: number = 0
): { messages: ExtractedMessage[]; newByteOffset: number } {
  if (!existsSync(filePath)) {
    return { messages: [], newByteOffset: 0 };
  }

  const fileSize = statSync(filePath).size;
  if (lastByteOffset >= fileSize) {
    return { messages: [], newByteOffset: fileSize };
  }

  const fd = openSync(filePath, 'r');
  const bufSize = fileSize - lastByteOffset;
  const buf = Buffer.alloc(bufSize);
  readSync(fd, buf, 0, bufSize, lastByteOffset);
  closeSync(fd);

  const lines = buf.toString('utf-8').split('\n').filter(Boolean);
  const messages: ExtractedMessage[] = [];

  // Extract sessionId from the first "session" line
  let sessionId = 'unknown';

  for (const line of lines) {
    try {
      const obj = JSON.parse(line);

      // Capture session ID from session header
      if (obj.type === 'session' && obj.id) {
        sessionId = obj.id;
        continue;
      }

      // Only process message lines
      if (obj.type !== 'message') continue;

      const msg = obj.message;
      if (!msg || !msg.role) continue;

      // Skip system messages and tool results
      if (msg.role === 'system' || msg.role === 'tool') continue;

      let text = '';
      if (typeof msg.content === 'string') {
        text = msg.content;
      } else if (Array.isArray(msg.content)) {
        const parts: string[] = [];
        for (const block of msg.content) {
          if (block.type === 'text' && block.text) {
            parts.push(block.text);
          }
          if (block.type === 'thinking' && block.thinking) {
            parts.push(`[thinking] ${block.thinking}`);
          }
        }
        text = parts.join('\n\n');
      }

      // Skip very short messages (noise)
      if (text.length < 20) continue;

      messages.push({
        role: msg.role,
        text,
        timestamp: obj.timestamp || new Date().toISOString(),
        sessionId: obj.id || sessionId,
      });
    } catch {
      // Skip malformed lines
    }
  }

  return { messages, newByteOffset: fileSize };
}

/** Detect whether a JSONL file is OpenClaw format.
 *  Checks the first line for type:"session" with version field
 *  (OpenClaw uses this header; Claude Code does not). */
export function isOpenClawJsonl(filePath: string): boolean {
  try {
    const fd = openSync(filePath, 'r');
    const buf = Buffer.alloc(Math.min(1024, statSync(filePath).size));
    const bytesRead = readSync(fd, buf, 0, buf.length, 0);
    closeSync(fd);

    const firstLine = buf.toString('utf-8', 0, bytesRead).split('\n')[0];
    if (!firstLine) return false;

    const obj = JSON.parse(firstLine);
    return obj.type === 'session' && typeof obj.version === 'number';
  } catch {
    return false;
  }
}
