import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "zopaf",
  name: "Zopaf Negotiation Engine",
  description:
    "Negotiation math engine — Pareto frontiers, iso-utility counteroffers, and preference inference via MILP optimization. Zero LLM tokens.",

  async register(api) {
    const config = api.config as { mcpUrl?: string };
    const url =
      config.mcpUrl || "https://zopaf-mcp-production.up.railway.app/mcp";

    api.registerMcpServer({
      id: "zopaf",
      name: "Zopaf Negotiation Engine",
      transport: "streamable-http",
      url,
    });
  },
});
