// openclaw.ts ... Bridge plugin entry point.
// Skill-only plugin: all functionality lives in skills/ and the MCP server
// (mcp-server.js) which is launched out-of-process. No tools, CLI, or HTTP
// routes are registered with the OpenClaw runtime.
//
// This file exists only so OpenClaw's plugin loader can discover the plugin
// when package.json declares `openclaw.extensions: ["./dist/openclaw.js"]`.
// Without it, gateway startup logs a "plugin not found" warning.

export default {
  register(api: any) {
    api.logger.info('lesa-bridge plugin registered (skill-only; MCP server runs out of process)');
  },
};
