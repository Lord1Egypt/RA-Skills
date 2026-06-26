#!/usr/bin/env node
/**
 * Tolstoy MCP — OpenClaw setup script
 * Adds the Tolstoy MCP server to your openclaw.json config.
 *
 * Usage: node setup.js
 * Or from skill dir: node setup.js
 *
 * Respects OPENCLAW_CONFIG_PATH env var. Default: ~/.openclaw/openclaw.json
 */

const fs = require('fs');
const path = require('path');

const TOLSTOY_MCP_ENTRY = {
  type: 'http',
  url: 'https://apilb.gotolstoy.com/mcp/v1/mcp',
  auth: 'oauth',
};

function getConfigPath() {
  if (process.env.OPENCLAW_CONFIG_PATH) {
    return path.resolve(process.env.OPENCLAW_CONFIG_PATH);
  }
  const home = process.env.HOME || process.env.USERPROFILE || process.env.HOMEPATH;
  if (!home) {
    console.error('Could not determine home directory. Set OPENCLAW_CONFIG_PATH.');
    process.exit(1);
  }
  return path.join(home, '.openclaw', 'openclaw.json');
}

function main() {
  const configPath = getConfigPath();

  let config;
  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    config = JSON.parse(raw);
  } catch (err) {
    if (err.code === 'ENOENT') {
      config = {};
    } else {
      console.error(`Failed to parse ${configPath}:`, err.message);
      console.error('If your config uses JSON5 (comments, trailing commas), add the Tolstoy MCP entry manually.');
      console.error('\nAdd this to mcpServers in your config:');
      console.error(JSON.stringify({ tolstoy: TOLSTOY_MCP_ENTRY }, null, 2));
      process.exit(1);
    }
  }

  config.mcpServers = config.mcpServers || {};
  if (config.mcpServers.tolstoy) {
    console.log('Tolstoy MCP already configured. Updating to latest.');
  }
  config.mcpServers.tolstoy = TOLSTOY_MCP_ENTRY;

  const dir = path.dirname(configPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
  console.log(`✓ Tolstoy MCP added to ${configPath}`);
  console.log('  Restart OpenClaw. On first use, you will be prompted to log in to Tolstoy.');
}

main();
