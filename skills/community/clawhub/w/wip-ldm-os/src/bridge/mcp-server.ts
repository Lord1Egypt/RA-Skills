// wip-bridge/mcp-server.ts: MCP server wrapping core.
// Thin layer: registers tools, starts inbox HTTP server, connects transport.

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer, IncomingMessage, ServerResponse } from "node:http";
import { appendFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { z } from "zod";

import {
  resolveConfig,
  sendMessage,
  sendLdmMessage,
  drainInbox,
  pushInbox,
  inboxCount,
  inboxCountBySession,
  setSessionIdentity,
  getSessionIdentity,
  registerBridgeSession,
  listActiveSessions,
  searchConversations,
  searchWorkspace,
  readWorkspaceFile,
  discoverSkills,
  executeSkillScript,
  type BridgeConfig,
  type InboxMessage,
  type SkillInfo,
} from "./core.js";

// ── Config ───────────────────────────────────────────────────────────

const config = resolveConfig();

const METRICS_DIR = join(process.env.HOME || homedir(), '.openclaw', 'memory');
const METRICS_PATH = join(METRICS_DIR, 'search-metrics.jsonl');

function logSearchMetric(tool: string, query: string, resultCount: number) {
  try {
    mkdirSync(METRICS_DIR, { recursive: true });
    const entry = JSON.stringify({
      ts: new Date().toISOString(),
      tool,
      query,
      results: resultCount,
    });
    appendFileSync(METRICS_PATH, entry + '\n');
  } catch {}
}

// ── Inbox HTTP server ────────────────────────────────────────────────

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
    req.on("error", reject);
  });
}

function startInboxServer(cfg: BridgeConfig): void {
  const httpServer = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const remoteAddr = req.socket.remoteAddress;
    if (remoteAddr !== "127.0.0.1" && remoteAddr !== "::1" && remoteAddr !== "::ffff:127.0.0.1") {
      res.writeHead(403, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "localhost only" }));
      return;
    }

    // POST /message: Write to file-based inbox (Phase 1 + 2 + 4)
    // Accepts: { from, message|body, to?, type? }
    // The "to" field supports: "cc-mini", "cc-mini:brainstorm", "cc-mini:*", "*"
    if (req.method === "POST" && req.url === "/message") {
      try {
        const body = JSON.parse(await readBody(req));
        const { agentId, sessionName } = getSessionIdentity();
        const queued = pushInbox({
          from: body.from || "agent",
          body: body.body || body.message || "",
          to: body.to || `${agentId}:${sessionName}`,
          type: body.type || "chat",
        });
        const messageBody = body.body || body.message || "";
        console.error(`wip-bridge inbox: message from ${body.from || "agent"} to ${body.to || "default"}`);

        try {
          server.sendLoggingMessage({
            level: "info",
            logger: "wip-bridge",
            data: `[inbox] ${body.from || "agent"}: ${messageBody}`,
          });
        } catch {}

        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: true, queued }));
      } catch (err: any) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: err.message }));
      }
      return;
    }

    // GET /status: Pending message counts (Phase 1 + 2)
    if (req.method === "GET" && req.url === "/status") {
      const pending = inboxCount();
      const bySession = inboxCountBySession();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true, pending, bySession }));
      return;
    }

    // GET /sessions: List active sessions (Phase 2)
    if (req.method === "GET" && req.url === "/sessions") {
      const sessions = listActiveSessions();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true, sessions }));
      return;
    }

    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "not found" }));
  });

  httpServer.listen(cfg.inboxPort, "127.0.0.1", () => {
    console.error(`wip-bridge inbox listening on 127.0.0.1:${cfg.inboxPort}`);
  });

  httpServer.on("error", (err: Error) => {
    // Port already bound by another bridge process. That's fine.
    // This process reads from filesystem directly via check_inbox.
    console.error(`wip-bridge inbox server error: ${err.message}`);
  });
}

// ── MCP Server ───────────────────────────────────────────────────────

const server = new McpServer({
  name: "wip-bridge",
  version: "0.3.0",
});

// Tool 1: Semantic search over conversation history
server.registerTool(
  "lesa_conversation_search",
  {
    description:
      "Search embedded conversation history. Returns semantically similar excerpts " +
      "from past conversations. Use this to find what was discussed about a topic, " +
      "decisions made, or technical details from earlier sessions.",
    inputSchema: {
      query: z.string().describe("What to search for in past conversations"),
      limit: z.number().optional().default(5).describe("Max results to return (default: 5)"),
    },
  },
  async ({ query, limit }) => {
    try {
      const results = await searchConversations(config, query, limit);
      logSearchMetric('lesa_conversation_search', query, results.length);

      if (results.length === 0) {
        return { content: [{ type: "text" as const, text: "No conversation history found." }] };
      }

      const hasEmbeddings = results[0].similarity !== undefined;
      const freshnessIcon = { fresh: "🟢", recent: "🟡", aging: "🟠", stale: "🔴" };
      const text = results
        .map((r, i) => {
          const sim = r.similarity !== undefined ? `score: ${r.similarity.toFixed(3)}, ` : "";
          const fresh = r.freshness ? `${freshnessIcon[r.freshness]} ${r.freshness}, ` : "";
          return `[${i + 1}] (${fresh}${sim}session: ${r.sessionKey}, date: ${r.date})\n${r.text}`;
        })
        .join("\n\n---\n\n");

      const prefix = hasEmbeddings
        ? "(Recency-weighted. 🟢 fresh <3d, 🟡 recent <7d, 🟠 aging <14d, 🔴 stale 14d+)\n\n"
        : "(Text search; no API key for semantic search)\n\n";
      return { content: [{ type: "text" as const, text: `${prefix}${text}` }] };
    } catch (err: any) {
      return { content: [{ type: "text" as const, text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// Tool 2: Search workspace markdown files
server.registerTool(
  "lesa_memory_search",
  {
    description:
      "Search workspace memory files (MEMORY.md, daily logs, notes, identity docs). " +
      "Returns matching excerpts from .md files. Use this to find written memory, " +
      "observations, todos, and notes.",
    inputSchema: {
      query: z.string().describe("Keywords to search for in workspace files"),
    },
  },
  async ({ query }) => {
    try {
      const results = searchWorkspace(config.workspaceDir, query);
      logSearchMetric('lesa_memory_search', query, results.length);

      if (results.length === 0) {
        return { content: [{ type: "text" as const, text: `No workspace files matched "${query}".` }] };
      }

      const text = results
        .map((r) => {
          const excerpts = r.excerpts.map((e) => `  ${e.replace(/\n/g, "\n  ")}`).join("\n  ...\n");
          return `### ${r.path}\n${excerpts}`;
        })
        .join("\n\n---\n\n");

      return { content: [{ type: "text" as const, text }] };
    } catch (err: any) {
      return { content: [{ type: "text" as const, text: `Error: ${err.message}` }], isError: true };
    }
  }
);

// Tool 3: Read a specific workspace file
server.registerTool(
  "lesa_read_workspace",
  {
    description:
      "Read a specific file from the agent workspace. Paths are relative to the workspace directory. " +
      "Common files: MEMORY.md, IDENTITY.md, SOUL.md, USER.md, AGENTS.md, TOOLS.md, " +
      "memory/YYYY-MM-DD.md (daily logs), memory/todos.md, memory/observations.md, notes/*.",
    inputSchema: {
      path: z.string().describe("File path relative to workspace/ (e.g. 'MEMORY.md', 'memory/2026-02-07.md')"),
    },
  },
  async ({ path: filePath }) => {
    try {
      const result = readWorkspaceFile(config.workspaceDir, filePath);
      return { content: [{ type: "text" as const, text: `# ${result.relativePath}\n\n${result.content}` }] };
    } catch (err: any) {
      return { content: [{ type: "text" as const, text: err.message }], isError: !err.message.includes("Available files") };
    }
  }
);

// Tool 4: Send a message to the OpenClaw agent (async, non-blocking)
//
// Sends via fire-and-forget to the gateway so CC is not blocked waiting for
// the reply. The message hits Lēsa's full pipeline (visible in Parker's TUI).
// Lēsa's reply arrives in the file inbox (~/.ldm/messages/) which CC picks up
// via the UserPromptSubmit hook or check_inbox tool.
//
// Also writes the outbound message to the file inbox as a "sent" record so
// there's a complete file trail of both sides of the conversation.
//
// Changed 2026-04-06: was synchronous (blocked up to 120s). Now async.
// See ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md
server.registerTool(
  "lesa_send_message",
  {
    description:
      "Send a message to the OpenClaw agent through the gateway. Routes through the agent's " +
      "full pipeline: memory, tools, personality, workspace. Use this for direct communication: " +
      "asking questions, sharing findings, coordinating work, or having a discussion. " +
      "Messages are prefixed with [Claude Code] so the agent knows the source.\n\n" +
      "This is async: returns immediately after sending. The agent's reply will arrive in " +
      "your inbox (check via lesa_check_inbox or it appears automatically on your next turn).",
    inputSchema: {
      message: z.string().describe("Message to send to the OpenClaw agent"),
    },
  },
  async ({ message }) => {
    try {
      // 1. Fire-and-forget to gateway (Lēsa sees it in TUI, Parker sees it)
      await sendMessage(config.openclawDir, message, { fireAndForget: true });

      // 2. Write outbound record to file inbox so the conversation trail is complete
      const { agentId, sessionName } = getSessionIdentity();
      sendLdmMessage({
        from: `${agentId}:${sessionName}`,
        to: "lesa",
        body: message,
        type: "chat",
      });

      return {
        content: [{
          type: "text" as const,
          text: `Sent to Lēsa: "${message}"\n\nMessage delivered to the gateway (fire-and-forget). ` +
            `Lēsa will process it through her full pipeline. Her reply will arrive in your inbox. ` +
            `Use lesa_check_inbox to check, or it will appear automatically on your next turn.`,
        }],
      };
    } catch (err: any) {
      return { content: [{ type: "text" as const, text: `Error sending message: ${err.message}` }], isError: true };
    }
  }
);

// Tool 5: Check inbox for messages (file-based, Phase 1)
server.registerTool(
  "lesa_check_inbox",
  {
    description:
      "Check for pending messages in the file-based inbox (~/.ldm/messages/). " +
      "Messages can come from OpenClaw agents, other Claude Code sessions, or CLI. " +
      "Returns all pending messages for this session and marks them as read. " +
      "Each entry includes [id: <uuid>] so you can pass it to lesa_reply_to_sender " +
      "when replying to a specific message.",
    inputSchema: {},
  },
  async () => {
    const messages = drainInbox();

    if (messages.length === 0) {
      return { content: [{ type: "text" as const, text: "No pending messages." }] };
    }

    const text = messages
      .map((m) => `**${m.from}** [${m.type}] (${m.timestamp}) [id: ${m.id}]:\n${m.body || m.message}`)
      .join("\n\n---\n\n");

    return { content: [{ type: "text" as const, text: `${messages.length} message(s):\n\n${text}` }] };
  }
);

// Tool 5b: Reply to a specific message, routing back to the original sender.
// Added 2026-04-20 to fix the "agent-only reply broadcasts to every session"
// footgun. Caller passes the message id from lesa_check_inbox output; the
// bridge resolves `to` to the original sender's fully-qualified identity,
// so replies land at exactly one session instead of every session of the
// agent. See ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md
server.registerTool(
  "lesa_reply_to_sender",
  {
    description:
      "Reply to a specific inbox message, routing back to the exact session " +
      "that sent it (not broadcast). Use this instead of ldm_send_message when " +
      "responding to something you saw in lesa_check_inbox. The message id is " +
      "printed as [id: <uuid>] in the inbox output.\n\n" +
      "If the message id can't be found (already deleted, typo, etc.) the reply " +
      "is still written with a best-effort target derived from the message sender " +
      "field you pass in as fallback.",
    inputSchema: {
      messageId: z.string().describe("The inbox message id you are replying to (from the [id: ...] field in lesa_check_inbox output)"),
      body: z.string().describe("Reply body"),
      type: z.string().optional().default("chat").describe("Message type: chat, system, task (default: chat)"),
    },
  },
  async ({ messageId, body, type }) => {
    try {
      const { agentId, sessionName } = getSessionIdentity();
      sendLdmMessage({
        from: `${agentId}:${sessionName}`,
        body,
        type: type || "chat",
        inReplyTo: messageId,
      });
      return {
        content: [{
          type: "text" as const,
          text: `Replied to message ${messageId}. Routed back to the original sender (not broadcast).`,
        }],
      };
    } catch (err: any) {
      return { content: [{ type: "text" as const, text: `Error replying: ${err.message}` }], isError: true };
    }
  }
);

// Tool 6: Send message to any agent via file-based inbox (Phase 4)
server.registerTool(
  "ldm_send_message",
  {
    description:
      "Send a message to any agent or session via the file-based inbox (~/.ldm/messages/). " +
      "Works for agent-to-agent communication. For OpenClaw agents (like Lesa), use lesa_send_message " +
      "instead (goes through the gateway). This tool writes directly to the shared inbox.\n\n" +
      "Target formats:\n" +
      "  'cc-mini' ... default session\n" +
      "  'cc-mini:brainstorm' ... named session\n" +
      "  'cc-mini:*' ... broadcast to all sessions of that agent\n" +
      "  '*' ... broadcast to all agents",
    inputSchema: {
      to: z.string().describe("Target: 'agent', 'agent:session', 'agent:*', or '*'"),
      message: z.string().describe("Message body"),
      type: z.string().optional().default("chat").describe("Message type: chat, system, task (default: chat)"),
    },
  },
  async ({ to, message, type }) => {
    const { agentId, sessionName } = getSessionIdentity();
    const id = sendLdmMessage({
      from: `${agentId}:${sessionName}`,
      to,
      body: message,
      type,
    });

    if (id) {
      return { content: [{ type: "text" as const, text: `Message sent (id: ${id}) to ${to}` }] };
    } else {
      return { content: [{ type: "text" as const, text: "Failed to send message." }], isError: true };
    }
  }
);

// ── OpenClaw Skill Bridge ────────────────────────────────────────────

function registerSkillTools(skills: SkillInfo[]): void {
  const executableSkills = skills.filter(s => s.hasScripts);
  const toolNameMap = new Map<string, SkillInfo>();

  // Register executable skills as individual tools
  for (const skill of executableSkills) {
    const toolName = `oc_skill_${skill.name.replace(/-/g, "_")}`;
    toolNameMap.set(toolName, skill);

    const scriptList = skill.scripts.length > 1
      ? ` Available scripts: ${skill.scripts.join(", ")}.`
      : "";

    server.registerTool(
      toolName,
      {
        description: `[OpenClaw skill] ${skill.description}${scriptList}`,
        inputSchema: {
          args: z.string().describe("Arguments to pass to the skill script (e.g. file paths, flags)"),
          script: z.string().optional().describe(
            skill.scripts.length > 1
              ? `Which script to run: ${skill.scripts.join(", ")}. Defaults to first .sh script.`
              : "Script to run (optional, defaults to the only available script)"
          ),
        },
      },
      async ({ args, script }) => {
        try {
          const result = await executeSkillScript(skill.skillDir, skill.scripts, script, args);
          return { content: [{ type: "text" as const, text: result }] };
        } catch (err: any) {
          return { content: [{ type: "text" as const, text: `Error: ${err.message}` }], isError: true };
        }
      }
    );
  }

  // Register a list tool for all skills
  server.registerTool(
    "oc_skills_list",
    {
      description:
        "List all available OpenClaw skills and their descriptions. " +
        "Skills with scripts can be called directly as oc_skill_{name} tools. " +
        "Instruction-only skills describe how to use external CLIs.",
      inputSchema: {
        filter: z.string().optional().describe("Filter skills by name or description keyword"),
      },
    },
    async ({ filter }) => {
      let filtered = skills;
      if (filter) {
        const f = filter.toLowerCase();
        filtered = skills.filter(s =>
          s.name.toLowerCase().includes(f) ||
          s.description.toLowerCase().includes(f)
        );
      }

      if (filtered.length === 0) {
        return { content: [{ type: "text" as const, text: "No skills matched the filter." }] };
      }

      const lines = filtered.map(s => {
        const prefix = s.hasScripts ? `oc_skill_${s.name.replace(/-/g, "_")}` : "(instruction-only)";
        const emoji = s.emoji ? `${s.emoji} ` : "";
        return `- ${emoji}**${s.name}** [${prefix}]: ${s.description}`;
      });

      const header = `${filtered.length} skill(s)` +
        (filter ? ` matching "${filter}"` : "") +
        ` (${executableSkills.length} executable, ${skills.length - executableSkills.length} instruction-only)`;

      return { content: [{ type: "text" as const, text: `${header}\n\n${lines.join("\n")}` }] };
    }
  );

  console.error(`wip-bridge: registered ${executableSkills.length} skill tools + oc_skills_list (${skills.length} total skills)`);
}

// ── Start ────────────────────────────────────────────────────────────

/**
 * Resolve session name from Claude Code's session metadata.
 *
 * CC writes session files to ~/.claude/sessions/<pid>.json with the
 * /rename label as the "name" field. The bridge MCP server is a child
 * process of CC, so process.ppid gives the CC PID. Reading the parent's
 * session file gives us the label automatically, no env var needed.
 *
 * Fallback chain: CC session file -> LDM_SESSION_NAME env -> "default"
 */
function resolveSessionName(): string {
  // 1. Try CC session file for parent PID.
  // CC and the bridge MCP server start concurrently. CC writes the session
  // file after boot, but the bridge may read it before it exists or before
  // the /rename label is written. Retry with a brief delay to handle the
  // race. Three attempts, 500ms apart = up to 1s total wait. If it still
  // fails, fall through to env var or default.
  const ccSessionDir = join(process.env.HOME || homedir(), ".claude", "sessions");
  const ccSessionPath = join(ccSessionDir, `${process.ppid}.json`);

  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const data = JSON.parse(readFileSync(ccSessionPath, "utf-8"));
      if (data.name && typeof data.name === "string") {
        return data.name;
      }
      // File exists but no name yet. CC hasn't written /rename label.
      // On the last attempt, break to fallback. Otherwise wait and retry.
      if (attempt < 2) {
        const { execSync } = require("node:child_process");
        execSync("sleep 0.5", { stdio: "ignore" });
      }
    } catch {
      // File doesn't exist yet. Wait and retry.
      if (attempt < 2) {
        try {
          const { execSync } = require("node:child_process");
          execSync("sleep 0.5", { stdio: "ignore" });
        } catch {}
      }
    }
  }

  // 2. Try env var (explicit override)
  if (process.env.LDM_SESSION_NAME) {
    return process.env.LDM_SESSION_NAME;
  }

  // 3. Default
  return "default";
}

async function main() {
  // Set session identity: auto-detect from CC session metadata, env, or default
  const agentId = process.env.LDM_AGENT_ID || "cc-mini";
  const sessionName = resolveSessionName();
  setSessionIdentity(agentId, sessionName);
  console.error(`wip-bridge: session identity: ${agentId}:${sessionName} (resolved from ${
    sessionName !== "default" ? "CC session file or env" : "default"
  })`);

  // Phase 2: Register session in ~/.ldm/sessions/
  const session = registerBridgeSession();
  if (session) {
    console.error(`wip-bridge: registered session ${agentId}--${sessionName} (pid ${session.pid})`);
  }

  startInboxServer(config);

  // Discover and register OpenClaw skills
  try {
    const skills = discoverSkills(config.openclawDir);
    registerSkillTools(skills);
  } catch (err: any) {
    console.error(`wip-bridge: skill discovery failed: ${err.message}`);
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`wip-bridge MCP server running (openclaw: ${config.openclawDir})`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
