// tools.mjs: MCP tool definitions. Bridge (messaging) + placeholder memory tools.

import { z } from "zod";
import { pushMessage, getMessages, countPending } from "./inbox.mjs";

/** Register all tools on an McpServer instance. */
export function registerTools(server, getIdentity) {

  server.registerTool("send_message", {
    description: "Send a message to any agent. Stored in inbox until read. " +
      "Target: 'agent', 'agent:session', 'agent:*' (all sessions), '*' (broadcast).",
    inputSchema: {
      to: z.string().describe("Recipient"),
      body: z.string().describe("Message body"),
      type: z.string().optional().default("chat").describe("chat, system, or task"),
    },
  }, async ({ to, body, type }) => {
    const id = pushMessage({ from: getIdentity().agentId, to, body, type });
    return { content: [{ type: "text", text: `Sent (id: ${id}) to ${to}` }] };
  });

  server.registerTool("check_inbox", {
    description: "Check for pending messages. Returns unread messages and marks them read.",
    inputSchema: {},
  }, async () => {
    const msgs = getMessages(getIdentity().agentId, true);
    if (!msgs.length) return { content: [{ type: "text", text: "No pending messages." }] };
    const text = msgs.map((m) => `**${m.from}** [${m.type}] (${m.timestamp}):\n${m.body}`).join("\n\n---\n\n");
    return { content: [{ type: "text", text: `${msgs.length} message(s):\n\n${text}` }] };
  });

  server.registerTool("search_memory", {
    description: "Search semantic memory (Crystal). Placeholder... coming soon.",
    inputSchema: { query: z.string().describe("Search query") },
  }, async ({ query }) => {
    return { content: [{ type: "text", text: `Memory search coming soon. Query: "${query}"` }] };
  });

  server.registerTool("remember", {
    description: "Store a fact in memory (Crystal). Placeholder... coming soon.",
    inputSchema: {
      text: z.string().describe("What to remember"),
      tags: z.string().optional().describe("Comma-separated tags"),
    },
  }, async ({ text, tags }) => {
    return { content: [{ type: "text", text: `Memory storage coming soon. Would remember: "${text}"${tags ? ` (tags: ${tags})` : ""}` }] };
  });

  server.registerTool("status", {
    description: "Show connection info and pending message count.",
    inputSchema: {},
  }, async () => {
    const { agentId, apiKey } = getIdentity();
    const masked = apiKey.slice(0, 7) + "..." + apiKey.slice(-4);
    return { content: [{ type: "text", text: `Agent: ${agentId}\nAPI key: ${masked}\nPending: ${countPending(agentId)}\nServer: wip.computer hosted MCP` }] };
  });

  server.registerTool("list_agents", {
    description: "List all known agents on the Bridge. Shows who you can send messages to.",
    inputSchema: {},
  }, async () => {
    // Read API_KEYS from server to find known agents
    // For now, return hardcoded list plus any OAuth-registered agents
    const known = [
      { id: "cc-mini", description: "Claude Code on Mac mini (CLI)" },
      { id: "lesa", description: "Lesa (OpenClaw agent on Mac mini)" },
      { id: "parker", description: "Parker (human, any device)" },
    ];
    const text = known.map(a => `**${a.id}** ... ${a.description}`).join("\n");
    return { content: [{ type: "text", text: `Known agents:\n\n${text}\n\nSend with: send_message(to: "agent-id", body: "your message")` }] };
  });

}
