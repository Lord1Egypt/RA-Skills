import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { resolveDefaultAgentId } from "../../agents/agent-scope.js";
import { loadConfig } from "../../config/config.js";
import { loadSessionStore } from "../../config/sessions.js";
import { ErrorCodes, errorShape } from "../protocol/index.js";
import { loadSessionEntry, readSessionMessages } from "../session-utils.js";
import type { GatewayRequestHandlers } from "./types.js";

// ── helpers ──────────────────────────────────────────────────────────────────

function resolveAgentsDir(agentId: string): string {
  return path.join(os.homedir(), ".openclaw", "agents", agentId, "sessions");
}

function isCronOrIsolatedKey(key: string): boolean {
  // Isolated/cron sessions have keys like agent:main:<uuid> that aren't "main"
  const parts = key.split(":");
  if (parts.length < 3) return false;
  const sessionPart = parts[2];
  // Regular session keys are short names; UUIDs indicate isolated sessions
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(sessionPart);
}

function extractSessionLabel(key: string, transcriptPath: string): string {
  // Try to read the cron job label from the first user message
  try {
    const lines = fs.readFileSync(transcriptPath, "utf-8").split("\n");
    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const parsed = JSON.parse(line) as Record<string, unknown>;
        if (parsed?.type === "message") {
          const msg = parsed.message as Record<string, unknown> | undefined;
          if (msg?.role === "user") {
            const content = msg.content;
            const text =
              typeof content === "string"
                ? content
                : Array.isArray(content)
                  ? (content[0] as Record<string, unknown>)?.type === "text"
                    ? String((content[0] as Record<string, unknown>).text ?? "")
                    : ""
                  : "";
            // Extract cron label: [cron:uuid Name] prefix
            const cronMatch = text.match(/^\[cron:[^\]]*?\s+([^\]]+)\]/);
            if (cronMatch?.[1]) return cronMatch[1];
            // Fallback: first 60 chars of message
            return text.slice(0, 60).replace(/\n/g, " ").trim();
          }
        }
      } catch {
        // skip
      }
    }
  } catch {
    // ignore
  }
  // Last resort: use session key fragment
  const parts = key.split(":");
  return parts[parts.length - 1]?.slice(0, 8) ?? key;
}

function simplifyMessages(
  rawMessages: unknown[],
): Array<{ role: string; text: string; timestamp?: number; toolName?: string }> {
  const result: Array<{ role: string; text: string; timestamp?: number; toolName?: string }> = [];
  for (const msg of rawMessages) {
    const m = msg as Record<string, unknown>;
    const role = typeof m.role === "string" ? m.role : "unknown";
    const ts = typeof m.timestamp === "number" ? m.timestamp : undefined;
    const content = m.content;

    if (typeof content === "string") {
      if (content.trim()) result.push({ role, text: content.trim(), timestamp: ts });
      continue;
    }

    if (Array.isArray(content)) {
      for (const part of content) {
        const p = part as Record<string, unknown>;
        if (p.type === "text" && typeof p.text === "string" && p.text.trim()) {
          result.push({ role, text: p.text.trim(), timestamp: ts });
        } else if (p.type === "toolCall") {
          const args = p.arguments ? JSON.stringify(p.arguments).slice(0, 120) : "";
          result.push({
            role: "tool",
            text: `${String(p.name ?? "?")}(${args})`,
            timestamp: ts,
            toolName: typeof p.name === "string" ? p.name : undefined,
          });
        } else if (p.type === "toolResult") {
          const r = p.result;
          const text =
            typeof r === "string"
              ? r.slice(0, 200)
              : Array.isArray(r)
                ? (r[0] as Record<string, unknown>)?.text?.toString().slice(0, 200) ?? ""
                : JSON.stringify(r).slice(0, 200);
          if (text.trim()) {
            result.push({ role: "tool_result", text: text.trim(), timestamp: ts });
          }
        } else if (p.type === "thinking" && typeof p.thinking === "string") {
          // Skip thinking content
        }
      }
    }
  }
  return result;
}

// ── handlers ─────────────────────────────────────────────────────────────────

export const bgSessionsHandlers: GatewayRequestHandlers = {
  "bgSessions.list": ({ respond }) => {
    try {
      const cfg = loadConfig();
      const agentId = resolveDefaultAgentId(cfg) ?? "main";
      const store = loadSessionStore({ agentId, cfg });
      const sessions = store?.sessions ?? {};
      const agentsDir = resolveAgentsDir(agentId);

      const rows: Array<{
        key: string;
        sessionId: string;
        label: string;
        updatedAt: number;
        running: boolean;
      }> = [];

      for (const [key, entry] of Object.entries(sessions)) {
        if (!isCronOrIsolatedKey(key)) continue;
        const e = entry as Record<string, unknown>;
        const sessionId = typeof e.sessionId === "string" ? e.sessionId : "";
        if (!sessionId) continue;

        const transcriptPath = path.join(agentsDir, `${sessionId}.jsonl`);
        const exists = fs.existsSync(transcriptPath);
        if (!exists) continue;

        const updatedAt =
          typeof e.updatedAt === "number"
            ? e.updatedAt
            : fs.statSync(transcriptPath).mtimeMs;

        // Check if running: lock file exists
        const lockPath = `${transcriptPath}.lock`;
        const running = fs.existsSync(lockPath);

        const label = extractSessionLabel(key, transcriptPath);

        rows.push({ key, sessionId, label, updatedAt, running });
      }

      // Sort by most recently updated
      rows.sort((a, b) => b.updatedAt - a.updatedAt);

      respond(true, { sessions: rows.slice(0, 20) });
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.INTERNAL_ERROR, String(err)));
    }
  },

  "bgSessions.history": ({ params, respond }) => {
    try {
      const p = params as { sessionKey?: string; limit?: number };
      if (!p.sessionKey) {
        respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "sessionKey required"));
        return;
      }

      const { entry, storePath } = loadSessionEntry(p.sessionKey);
      if (!entry?.sessionId) {
        respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "session not found"));
        return;
      }

      const rawMessages = readSessionMessages(entry.sessionId, storePath, entry.sessionFile);
      const messages = simplifyMessages(rawMessages);
      const limit = typeof p.limit === "number" ? p.limit : 100;
      const sliced = messages.slice(-limit);

      respond(true, { messages: sliced, sessionId: entry.sessionId });
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.INTERNAL_ERROR, String(err)));
    }
  },

  // bgSessions.send is intentionally omitted here.
  // Use chat.send with the sessionKey directly — it handles all routing.
  // The UI panel calls chat.send({ sessionKey, message, idempotencyKey }) directly.
};

