// PM2 config for the hosted MCP server.
// API keys are resolved from 1Password at runtime via the op-secrets plugin.
// NEVER hardcode keys here. Use environment variables set by the deploy process,
// or read from 1Password at server startup.
module.exports = {
  apps: [{
    name: "mcp-server",
    script: "server.mjs",
    env: {
      // XAI_API_KEY: resolved from 1Password at runtime (item: "x.ai - wip-computer-beta", field: "credential")
      // DATABASE_URL: set in .env (gitignored)
    }
  }]
};
