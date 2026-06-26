#!/usr/bin/env node
/**
 * SLBrow CLI - Execute browser automation tools via REST API
 * Usage: node slbrow.js <tool> [--arg value] [--port 5556]
 * Example: node slbrow.js page_navigate --url "https://example.com"
 */

const path = require('path');
const fs = require('fs');
const DEFAULT_PORT = 5556;

// Dynamically load tool list from tools.json (single source of truth)
function loadTools() {
  try {
    const toolsPath = path.join(__dirname, '..', 'tools.json');
    const raw = fs.readFileSync(toolsPath, 'utf8');
    return JSON.parse(raw);
  } catch {
    return { browser: [], vai: [] };
  }
}

function getToolNames() {
  const config = loadTools();
  const browser = (config.browser || []).map(t => t.name);
  const vai = (config.vai || []).map(t => t.name);
  return { browser, vai, all: [...browser, ...vai] };
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const result = { tool: null, port: DEFAULT_PORT, args: {} };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--port' && args[i + 1]) {
      result.port = parseInt(args[++i], 10) || DEFAULT_PORT;
    } else if (arg === '--help' || arg === '-h') {
      return { help: true };
    } else if (arg === '--list') {
      return { list: true };
    } else if (arg.startsWith('--') && !arg.includes('=')) {
      const key = arg.slice(2).replace(/-/g, '_');
      const next = args[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        result.args[key] = next;
        i++;
      } else {
        result.args[key] = true;
      }
    } else if (arg.startsWith('--') && arg.includes('=')) {
      const [k, v] = arg.slice(2).split('=');
      result.args[k.replace(/-/g, '_')] = v;
    } else if (!result.tool && !arg.startsWith('--')) {
      result.tool = arg;
    }
  }

  return result;
}

function coerceArgs(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v === 'true') out[k] = true;
    else if (v === 'false') out[k] = false;
    else if (v === 'null') out[k] = null;
    else if (/^\d+$/.test(v)) out[k] = parseInt(v, 10);
    else if (/^\d+\.\d+$/.test(v)) out[k] = parseFloat(v);
    else if (v && typeof v === 'string' && (v.startsWith('[') || v.startsWith('{'))) {
      try {
        out[k] = JSON.parse(v);
      } catch {
        out[k] = v;
      }
    } else {
      out[k] = v;
    }
  }
  return out;
}

async function main() {
  const parsed = parseArgs(process.argv);

  if (parsed.help) {
    const { browser, vai } = getToolNames();
    console.log(`
SLBrow CLI - Execute browser automation tools

Usage: node slbrow.js <tool> [--arg value] [--port PORT]

Options:
  --port PORT    HTTP port (default: ${DEFAULT_PORT})
  --list         List all available tools by category
  --help, -h     Show this help

Examples:
  node slbrow.js page_navigate --url "https://example.com"
  node slbrow.js tab_list
  node slbrow.js page_analyze --intent_hint "article"
  node slbrow.js get_history --keywords "react" --max_results 10
  node slbrow.js get_page_seelink_player_list
  node slbrow.js use_seelink_players_ai --player_position_list "[0]" --ai_function_name "reduce_fog"

Browser Tools:
  ${browser.join(', ') || '(none)'}

VAI Tools (Seelink):
  ${vai.join(', ') || '(none)'}
`);
    process.exit(0);
  }

  if (parsed.list) {
    const { browser, vai } = getToolNames();
    console.log('Browser Tools:');
    browser.forEach(name => console.log(`  ${name}`));
    console.log('\nVAI Tools (Seelink):');
    vai.forEach(name => console.log(`  ${name}`));
    process.exit(0);
  }

  if (!parsed.tool) {
    console.error('Error: Missing tool name. Use --help for usage.');
    process.exit(1);
  }

  const port = parsed.port;
  const baseUrl = `http://127.0.0.1:${port}`;
  const args = coerceArgs(parsed.args);

  try {
    const res = await fetch(`${baseUrl}/api/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tool: parsed.tool, args }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      console.error('Error:', data.error || res.statusText);
      if (data.code === 'EXTENSION_DISCONNECTED') {
        console.error('Ensure the browser extension is installed and the server is running.');
      }
      process.exit(1);
    }

    if (data.formatted) {
      console.log(data.formatted);
    } else {
      console.log(JSON.stringify(data, null, 2));
    }
  } catch (err) {
    console.error('Error:', err.message);
    if (err.cause?.code === 'ECONNREFUSED') {
      console.error(`Cannot connect to ${baseUrl}. Is the SLBrow server running?`);
    }
    process.exit(1);
  }
}

main();
