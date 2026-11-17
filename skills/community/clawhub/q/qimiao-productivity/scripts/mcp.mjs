#!/usr/bin/env node
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';

// The endpoint is fixed. Never forward business credentials to an arbitrary host.
const endpoint = new URL('https://mcp.longxia.sale/mcp');
const [action = 'overview', toolName] = process.argv.slice(2);
const usage = 'Usage: node scripts/mcp.mjs overview | tools | call TOOL_NAME < arguments.json';
if (!['overview', 'tools', 'call'].includes(action) || (action === 'call' && !toolName)) {
  console.error(usage);
  process.exit(2);
}


let args = {};
if (action === 'call') {
  if (process.stdin.isTTY) {
    console.error('Provide a JSON object on stdin; do not put private credentials in command arguments.');
    process.exit(2);
  }
  let input = '';
  for await (const chunk of process.stdin) {
    input += chunk;
    if (Buffer.byteLength(input) > 1024 * 1024) {
      console.error('Tool arguments exceed 1 MiB. Upload files using the returned upload protocol.');
      process.exit(2);
    }
  }
  try {
    args = JSON.parse(input || '{}');
    if (!args || typeof args !== 'object' || Array.isArray(args)) throw new Error();
  } catch {
    console.error('stdin must contain one JSON object.');
    process.exit(2);
  }
}

// No native elicitation UI. Conversational user confirmation is forwarded as
// supplied by the Agent; this helper never invents or fills confirmation.
const client = new Client(
  { name: 'qimiao-productivity-skill', version: '1.0.2' },
  { versionNegotiation: { mode: 'legacy' } },
);
try {
  await client.connect(new StreamableHTTPClientTransport(endpoint, {
    requestInit: { redirect: 'error', signal: AbortSignal.timeout(120_000) },
  }));
  let result;
  if (action === 'tools') {
    result = await client.listTools();
  } else {
    result = await client.callTool({
      name: action === 'overview' ? 'get_service_overview' : toolName,
      arguments: action === 'overview' ? { mode: 'compact' } : args,
    }, undefined, { timeout: 90_000 });
  }
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  if (result.isError) process.exitCode = 1;
} catch (error) {
  // Do not dump SDK/HTTP errors: they can contain private tool arguments or URLs.
  console.error(`MCP request failed (${error?.name || 'Error'}). Check connectivity and the original task status before retrying.`);
  process.exitCode = 1;
} finally {
  await client.close().catch(() => {});
}
