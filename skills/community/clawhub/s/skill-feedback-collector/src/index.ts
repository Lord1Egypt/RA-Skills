import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { WebSocketServer, WebSocket } from "ws";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { URL } from "node:url";

const WS_PORT = parseInt(process.env.FEEDBACK_PORT || "18061", 10);
const AUTH_TOKEN = process.env.FEEDBACK_TOKEN || "";
const BASE_DIR = path.resolve(
  path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1")),
  ".."
);
const CLIENT_DIR = path.join(BASE_DIR, "client");
const HISTORY_FILE = path.join(BASE_DIR, "feedback-history.json");
const HEARTBEAT_INTERVAL = 30_000;
const HEARTBEAT_TIMEOUT = 35_000;

interface HistoryEntry {
  id: number;
  timestamp: string;
  role: "ai" | "human";
  text: string;
}

let history: HistoryEntry[] = [];
let historyCounter = 0;

function loadHistory() {
  try {
    if (fs.existsSync(HISTORY_FILE)) {
      const raw = fs.readFileSync(HISTORY_FILE, "utf-8");
      history = JSON.parse(raw);
      historyCounter = history.reduce((max, e) => Math.max(max, e.id), 0);
    }
  } catch {
    history = [];
    historyCounter = 0;
  }
}

function saveHistory() {
  try {
    fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2), "utf-8");
  } catch (err) {
    console.error("[feedback-collector] Failed to save history:", err);
  }
}

function addHistoryEntry(role: "ai" | "human", text: string): HistoryEntry {
  const entry: HistoryEntry = {
    id: ++historyCounter,
    timestamp: new Date().toISOString(),
    role,
    text,
  };
  history.push(entry);
  if (history.length > 500) {
    history = history.slice(-500);
  }
  saveHistory();
  return entry;
}

loadHistory();

let pendingResolve: ((value: string) => void) | null = null;
let pendingReason: string | null = null;
let feedbackEnabled = true;

const taskQueue: string[] = [];
let autoMode = false;
const AUTO_DELAY_MS = 1500;

interface TrackedSocket extends WebSocket {
  isAlive: boolean;
}

const connectedClients = new Set<TrackedSocket>();

function broadcastQueueState() {
  broadcast({ type: "queue", tasks: [...taskQueue], autoMode });
}

function checkAuth(req: http.IncomingMessage): boolean {
  if (!AUTH_TOKEN) return true;
  const url = new URL(req.url || "/", `http://localhost:${WS_PORT}`);
  const tokenParam = url.searchParams.get("token");
  if (tokenParam === AUTH_TOKEN) return true;
  const authHeader = req.headers.authorization;
  if (authHeader === `Bearer ${AUTH_TOKEN}`) return true;
  return false;
}

const pollWaiters: Array<{
  res: http.ServerResponse;
  timer: ReturnType<typeof setTimeout>;
}> = [];
let pollSeq = 0;

function notifyPollWaiters() {
  const snapshot = {
    seq: ++pollSeq,
    pending: pendingResolve !== null,
    reason: pendingReason,
    enabled: feedbackEnabled,
  };
  while (pollWaiters.length > 0) {
    const w = pollWaiters.shift()!;
    clearTimeout(w.timer);
    try {
      w.res.writeHead(200, {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      });
      w.res.end(JSON.stringify(snapshot));
    } catch {
      /* client gone */
    }
  }
}

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((resolve) => {
    const chunks: Buffer[] = [];
    req.on("data", (c: Buffer) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf-8")));
  });
}

const httpServer = http.createServer(async (req, res) => {
  const cors: Record<string, string> = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };

  if (req.method === "OPTIONS") {
    res.writeHead(204, cors);
    res.end();
    return;
  }

  if (req.url === "/" || req.url?.startsWith("/index.html") || req.url?.startsWith("/?")) {
    const filePath = path.join(CLIENT_DIR, "index.html");
    fs.readFile(filePath, "utf-8", (err, data) => {
      if (err) {
        res.writeHead(500, { "Content-Type": "text/plain", ...cors });
        res.end("Failed to load client page");
        return;
      }
      res.writeHead(200, {
        "Content-Type": "text/html; charset=utf-8",
        ...cors,
      });
      res.end(data);
    });
    return;
  }

  if (req.url?.startsWith("/api/")) {
    if (!checkAuth(req)) {
      res.writeHead(401, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ error: "Unauthorized. Provide ?token=xxx or Authorization: Bearer xxx" }));
      return;
    }
  }

  if (req.url === "/api/history") {
    const recent = history.slice(-100).reverse();
    res.writeHead(200, {
      "Content-Type": "application/json; charset=utf-8",
      ...cors,
    });
    res.end(JSON.stringify(recent));
    return;
  }

  if (req.url === "/api/history/export") {
    res.writeHead(200, {
      "Content-Type": "application/json; charset=utf-8",
      "Content-Disposition": `attachment; filename="feedback-history-${new Date().toISOString().slice(0, 10)}.json"`,
      ...cors,
    });
    res.end(JSON.stringify(history, null, 2));
    return;
  }

  if (req.url === "/api/status") {
    res.writeHead(200, { "Content-Type": "application/json", ...cors });
    res.end(
      JSON.stringify({
        seq: pollSeq,
        pending: pendingResolve !== null,
        reason: pendingReason,
        enabled: feedbackEnabled,
      })
    );
    return;
  }

  if (req.url?.startsWith("/api/poll")) {
    const url = new URL(req.url, `http://localhost:${WS_PORT}`);
    const lastSeq = parseInt(url.searchParams.get("seq") || "0", 10);

    if (lastSeq < pollSeq) {
      res.writeHead(200, { "Content-Type": "application/json", ...cors });
      res.end(
        JSON.stringify({
          seq: pollSeq,
          pending: pendingResolve !== null,
          reason: pendingReason,
          enabled: feedbackEnabled,
        })
      );
      return;
    }

    const timer = setTimeout(() => {
      const idx = pollWaiters.findIndex((w) => w.res === res);
      if (idx >= 0) pollWaiters.splice(idx, 1);
      res.writeHead(200, { "Content-Type": "application/json", ...cors });
      res.end(
        JSON.stringify({
          seq: pollSeq,
          pending: pendingResolve !== null,
          reason: pendingReason,
          enabled: feedbackEnabled,
        })
      );
    }, 25000);

    pollWaiters.push({ res, timer });
    return;
  }

  if (req.url === "/api/feedback" && req.method === "POST") {
    const body = await readBody(req);
    try {
      const data = JSON.parse(body);
      if (data.text && pendingResolve) {
        addHistoryEntry("human", data.text);
        const resolve = pendingResolve;
        pendingResolve = null;
        pendingReason = null;
        resolve(data.text);
        broadcast({
          type: "resolved",
          message: "Feedback received. AI is continuing...",
        });
        notifyPollWaiters();
        res.writeHead(200, { "Content-Type": "application/json", ...cors });
        res.end(JSON.stringify({ ok: true }));
      } else {
        res.writeHead(400, { "Content-Type": "application/json", ...cors });
        res.end(JSON.stringify({ error: "No pending request or empty text" }));
      }
    } catch {
      res.writeHead(400, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ error: "Invalid JSON" }));
    }
    return;
  }

  if (req.url === "/api/toggle" && req.method === "POST") {
    const body = await readBody(req);
    try {
      const data = JSON.parse(body);
      feedbackEnabled = !!data.enabled;
      console.error(
        `[feedback-collector] Feedback mode ${feedbackEnabled ? "ENABLED" : "DISABLED"} via HTTP`
      );
      broadcast({ type: "mode", enabled: feedbackEnabled });
      notifyPollWaiters();
      res.writeHead(200, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ ok: true, enabled: feedbackEnabled }));
    } catch {
      res.writeHead(400, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ error: "Invalid JSON" }));
    }
    return;
  }

  if (req.url === "/api/queue" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json", ...cors });
    res.end(JSON.stringify({ tasks: [...taskQueue], autoMode }));
    return;
  }

  if (req.url === "/api/queue" && req.method === "POST") {
    const body = await readBody(req);
    try {
      const data = JSON.parse(body);
      if (data.action === "add" && typeof data.task === "string" && data.task.trim()) {
        taskQueue.push(data.task.trim());
        broadcastQueueState();
      } else if (data.action === "remove" && typeof data.index === "number") {
        if (data.index >= 0 && data.index < taskQueue.length) {
          taskQueue.splice(data.index, 1);
          broadcastQueueState();
        }
      } else if (data.action === "clear") {
        taskQueue.length = 0;
        broadcastQueueState();
      } else if (data.action === "reorder" && Array.isArray(data.tasks)) {
        taskQueue.length = 0;
        taskQueue.push(...data.tasks.filter((t: unknown) => typeof t === "string" && (t as string).trim()));
        broadcastQueueState();
      } else if (data.action === "autoMode" && typeof data.enabled === "boolean") {
        autoMode = data.enabled;
        broadcastQueueState();
      }
      res.writeHead(200, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ ok: true, tasks: [...taskQueue], autoMode }));
    } catch {
      res.writeHead(400, { "Content-Type": "application/json", ...cors });
      res.end(JSON.stringify({ error: "Invalid JSON" }));
    }
    return;
  }

  if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json", ...cors });
    res.end(
      JSON.stringify({
        status: "ok",
        pending: pendingResolve !== null,
        clients: connectedClients.size,
        historyCount: history.length,
        feedbackEnabled,
        queueLength: taskQueue.length,
        autoMode,
      })
    );
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain", ...cors });
  res.end("Not Found");
});

const wss = new WebSocketServer({ server: httpServer });

// --- WebSocket heartbeat ---
const heartbeatInterval = setInterval(() => {
  for (const ws of connectedClients) {
    if (!ws.isAlive) {
      ws.terminate();
      connectedClients.delete(ws);
      continue;
    }
    ws.isAlive = false;
    ws.ping();
  }
}, HEARTBEAT_INTERVAL);

wss.on("close", () => clearInterval(heartbeatInterval));

wss.on("connection", (rawWs, req) => {
  if (AUTH_TOKEN && !checkAuth(req)) {
    rawWs.close(4001, "Unauthorized");
    return;
  }

  const ws = rawWs as TrackedSocket;
  ws.isAlive = true;
  connectedClients.add(ws);
  console.error(
    `[feedback-collector] Client connected. Total: ${connectedClients.size}`
  );

  ws.on("pong", () => {
    ws.isAlive = true;
  });

  ws.send(JSON.stringify({ type: "mode", enabled: feedbackEnabled }));
  ws.send(JSON.stringify({ type: "queue", tasks: [...taskQueue], autoMode }));

  if (pendingResolve && pendingReason) {
    ws.send(
      JSON.stringify({
        type: "question",
        reason: pendingReason,
      })
    );
  }

  ws.on("message", (raw) => {
    ws.isAlive = true;
    try {
      const data = JSON.parse(raw.toString());
      if (data.type === "feedback" && data.text && pendingResolve) {
        addHistoryEntry("human", data.text);
        const resolve = pendingResolve;
        pendingResolve = null;
        pendingReason = null;
        resolve(data.text);
        broadcast({
          type: "resolved",
          message: "Feedback received. AI is continuing...",
        });
        notifyPollWaiters();
      } else if (data.type === "toggle") {
        feedbackEnabled = !!data.enabled;
        console.error(
          `[feedback-collector] Feedback mode ${feedbackEnabled ? "ENABLED" : "DISABLED"} via UI`
        );
        broadcast({ type: "mode", enabled: feedbackEnabled });
        notifyPollWaiters();
      } else if (data.type === "queue") {
        if (data.action === "add" && typeof data.task === "string" && data.task.trim()) {
          taskQueue.push(data.task.trim());
          broadcastQueueState();
        } else if (data.action === "remove" && typeof data.index === "number") {
          if (data.index >= 0 && data.index < taskQueue.length) {
            taskQueue.splice(data.index, 1);
            broadcastQueueState();
          }
        } else if (data.action === "clear") {
          taskQueue.length = 0;
          broadcastQueueState();
        } else if (data.action === "autoMode" && typeof data.enabled === "boolean") {
          autoMode = data.enabled;
          broadcastQueueState();
        }
      }
    } catch {
      console.error("[feedback-collector] Invalid message from client");
    }
  });

  ws.on("close", () => {
    connectedClients.delete(ws);
    console.error(
      `[feedback-collector] Client disconnected. Total: ${connectedClients.size}`
    );
  });
});

function broadcast(payload: Record<string, unknown>) {
  const msg = JSON.stringify(payload);
  for (const client of connectedClients) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg);
    }
  }
}

httpServer.listen(WS_PORT, "0.0.0.0", () => {
  console.error(
    `[feedback-collector] UI & WebSocket server listening on http://0.0.0.0:${WS_PORT}`
  );
  if (AUTH_TOKEN) {
    console.error(`[feedback-collector] Auth enabled. Use ?token=${AUTH_TOKEN} or Authorization header.`);
  }
});

const mcpServer = new Server(
  { name: "skill-feedback-collector", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

mcpServer.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "ask_human_feedback",
      description:
        "Suspend the current AI thread and wait for human feedback via a WebSocket-connected UI. " +
        "Use this tool whenever you finish a task, encounter uncertainty, or need user confirmation " +
        "before proceeding. This prevents the AI from ending the conversation prematurely. " +
        "If feedback mode is disabled, this tool returns immediately with a bypass message.",
      inputSchema: {
        type: "object" as const,
        properties: {
          reason: {
            type: "string",
            description:
              "A clear summary of what you have done so far and what you need from the user. " +
              "Be specific about completed work and questions for the user.",
          },
        },
        required: ["reason"],
      },
    },
    {
      name: "set_feedback_mode",
      description:
        "Enable or disable the feedback confirmation mode. " +
        "When disabled, ask_human_feedback will return immediately without waiting. " +
        "When enabled (default), ask_human_feedback will suspend the thread and wait for human input. " +
        "Call this when the user says things like '自由模式/free mode' (disable) or '确认模式/feedback mode' (enable).",
      inputSchema: {
        type: "object" as const,
        properties: {
          enabled: {
            type: "boolean",
            description: "true to enable feedback mode (default), false to disable it.",
          },
        },
        required: ["enabled"],
      },
    },
  ],
}));

mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;

  if (toolName === "set_feedback_mode") {
    const enabled = Boolean(request.params.arguments?.enabled);
    feedbackEnabled = enabled;
    console.error(
      `[feedback-collector] Feedback mode ${enabled ? "ENABLED" : "DISABLED"} via MCP tool`
    );
    broadcast({ type: "mode", enabled: feedbackEnabled });
    notifyPollWaiters();
    return {
      content: [
        {
          type: "text",
          text: `Feedback mode is now ${enabled ? "ENABLED — I will wait for your confirmation after each task." : "DISABLED — I will work freely without pausing for confirmation."}`,
        },
      ],
    };
  }

  if (toolName === "ask_human_feedback") {
    const reason = String(
      request.params.arguments?.reason ?? "AI is waiting for your input."
    );

    if (!feedbackEnabled) {
      console.error(
        `[feedback-collector] Feedback mode disabled, bypassing: ${reason}`
      );
      addHistoryEntry("ai", `[BYPASSED] ${reason}`);
      return {
        content: [
          {
            type: "text",
            text: "Feedback mode is currently disabled. Continue working autonomously. The user will re-enable feedback mode when needed.",
          },
        ],
      };
    }

    console.error(`[feedback-collector] AI is asking: ${reason}`);

    addHistoryEntry("ai", reason);
    pendingReason = reason;
    broadcast({ type: "question", reason });
    notifyPollWaiters();

    if (taskQueue.length > 0) {
      const nextTask = taskQueue.shift()!;
      broadcastQueueState();
      console.error(`[feedback-collector] Auto-dequeued task: ${nextTask}`);

      await new Promise((r) => setTimeout(r, AUTO_DELAY_MS));

      addHistoryEntry("human", `[QUEUE] ${nextTask}`);
      pendingReason = null;
      broadcast({
        type: "resolved",
        message: `Queue task dispatched: ${nextTask}`,
        autoTask: nextTask,
      });
      notifyPollWaiters();

      return {
        content: [{ type: "text", text: nextTask }],
      };
    }

    const humanResponse = await new Promise<string>((resolve) => {
      pendingResolve = resolve;
    });

    console.error(`[feedback-collector] Human responded: ${humanResponse}`);

    return {
      content: [{ type: "text", text: humanResponse }],
    };
  }

  return {
    content: [
      { type: "text", text: `Unknown tool: ${request.params.name}` },
    ],
    isError: true,
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await mcpServer.connect(transport);
  console.error("[feedback-collector] MCP Server started via stdio");
}

main().catch((err) => {
  console.error("[feedback-collector] Fatal error:", err);
  process.exit(1);
});
