// inbox.mjs: File-based message inbox for hosted MCP server.
// Each message is a JSON file. Same format as local bridge.

import { randomUUID } from "node:crypto";
import { mkdirSync, readdirSync, readFileSync, writeFileSync, unlinkSync } from "node:fs";
import { join } from "node:path";

const INBOX_DIR = process.env.MCP_INBOX_DIR || "/var/www/wip.computer/app/mcp-server/inbox";
mkdirSync(INBOX_DIR, { recursive: true });

/** Push a message into the inbox. Returns message ID. */
export function pushMessage({ from, to, body, type = "chat" }) {
  const id = randomUUID();
  const msg = { id, type, from, to, body, timestamp: new Date().toISOString(), read: false };
  writeFileSync(join(INBOX_DIR, `${Date.now()}-${id}.json`), JSON.stringify(msg, null, 2));
  return id;
}

/** Get messages for a recipient. If markRead, consumed messages are deleted. */
export function getMessages(to, markRead = false) {
  const files = readdirSync(INBOX_DIR).filter((f) => f.endsWith(".json")).sort();
  const matched = [];
  for (const file of files) {
    const fp = join(INBOX_DIR, file);
    let msg;
    try { msg = JSON.parse(readFileSync(fp, "utf-8")); } catch { continue; }
    if (msg.read || !matches(msg.to, to)) continue;
    matched.push(msg);
    if (markRead) { try { unlinkSync(fp); } catch {} }
  }
  return matched;
}

/** Count pending (unread) messages for a recipient. */
export function countPending(to) {
  const files = readdirSync(INBOX_DIR).filter((f) => f.endsWith(".json"));
  let n = 0;
  for (const file of files) {
    try {
      const msg = JSON.parse(readFileSync(join(INBOX_DIR, file), "utf-8"));
      if (!msg.read && matches(msg.to, to)) n++;
    } catch { continue; }
  }
  return n;
}

/**
 * Recipient matching. Supports:
 *   "agent", "agent:session", "agent:*" (all sessions), "*" (broadcast)
 */
function matches(msgTo, query) {
  if (msgTo === "*" || query === "*" || msgTo === query) return true;
  if (query.endsWith(":*")) {
    const p = query.slice(0, -2);
    if (msgTo === p || msgTo.startsWith(p + ":")) return true;
  }
  if (msgTo.endsWith(":*")) {
    const p = msgTo.slice(0, -2);
    if (query === p || query.startsWith(p + ":")) return true;
  }
  if (!query.includes(":") && msgTo === query + ":default") return true;
  if (!msgTo.includes(":") && query === msgTo + ":default") return true;
  return false;
}
