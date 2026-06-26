// SolCore Memory Plugin for OpenClaw
// Connects to webhook on port 5003

const SOLCORE_PLUGIN_ID = "solcore-memory";

interface PluginConfig {
  webhookUrl?: string;
}

function parsePluginConfig(value: unknown): PluginConfig {
  if (!value || typeof value !== "object") return {};
  const cfg = value as Record<string, unknown>;
  const webhookUrl = cfg.webhookUrl;
  return {
    webhookUrl: typeof webhookUrl === "string" ? webhookUrl : "http://localhost:5003",
  };
}

async function callSolCore(endpoint: string, payload: any, webhookUrl: string): Promise<any> {
  const response = await fetch(`${webhookUrl}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  if (!response.ok) {
    throw new Error(`SolCore error: ${response.status}`);
  }
  
  return await response.json();
}

const solcorePlugin = {
  id: SOLCORE_PLUGIN_ID,
  name: "SolCore Memory System",
  description: "SolCore memory integration - persistent memory with pattern detection",
  
  configSchema: {
    parse: parsePluginConfig,
  },
  
  register(api: any) {
    const webhookUrl = parsePluginConfig(api.pluginConfig).webhookUrl || "http://localhost:5003";
    
    // Tool: solcore_get_context
    api.registerTool({
      name: "solcore_get_context",
      label: "SolCore Get Context",
      description: "Retrieve relevant memories, patterns, and context from SolCore",
      parameters: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Current user query to find relevant context"
          },
          limit: {
            type: "number",
            description: "Maximum memories to retrieve (default: 5)"
          },
          include_patterns: {
            type: "boolean",
            description: "Include detected patterns (default: true)"
          }
        },
        required: ["query"]
      },
      execute: async (args: { query: string; limit?: number; include_patterns?: boolean }) => {
        try {
          const result = await callSolCore('/context', {
            query: args.query,
            limit: args.limit || 5,
            include_patterns: args.include_patterns !== false
          }, webhookUrl);
          
          return {
            content: [
              {
                type: "text",
                text: `Context retrieved for "${args.query}":\n\n${result.context || "No relevant memories found."}`
              }
            ]
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Failed to retrieve context: ${error}`
              }
            ],
            isError: true
          };
        }
      }
    });
    
    // Tool: solcore_store_memory
    api.registerTool({
      name: "solcore_store_memory",
      label: "SolCore Store Memory",
      description: "Store interaction into SolCore memory system",
      parameters: {
        type: "object",
        properties: {
          input: {
            type: "string",
            description: "The user's input/query"
          },
          output: {
            type: "string",
            description: "The assistant's response"
          },
          session_id: {
            type: "string",
            description: "Session identifier (optional)"
          },
          user_id: {
            type: "string",
            description: "User identifier (default: michael)"
          }
        },
        required: ["input", "output"]
      },
      execute: async (args: { input: string; output: string; session_id?: string; user_id?: string }) => {
        try {
          await callSolCore('/store', {
            input: args.input,
            output: args.output,
            session_id: args.session_id,
            user_id: args.user_id || "michael"
          }, webhookUrl);
          
          return {
            content: [
              {
                type: "text",
                text: "Memory stored successfully."
              }
            ]
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Failed to store memory: ${error}`
              }
            ],
            isError: true
          };
        }
      }
    });
  }
};

export default solcorePlugin;
