#!/usr/bin/env node

/**
 * TrendSwap CLI Helper for OpenClaw Skill
 * Zero-dependency Node.js script to interact with TrendSwap API & MCP endpoint.
 */

const BASE_URL = process.env.TRENDSWAP_BASE_URL || 'https://trendswap.app';
const API_KEY = process.env.TRENDSWAP_API_KEY || '';

async function callMcpTool(name, args = {}) {
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json, text/event-stream',
  };
  if (API_KEY) {
    headers['Authorization'] = `Bearer ${API_KEY}`;
  }

  const res = await fetch(`${BASE_URL}/api/mcp`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: {
        name,
        arguments: args,
      },
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }

  const raw = await res.text();
  let json;
  try {
    if (raw.includes('data:')) {
      const dataLine = raw.split('\n').find((l) => l.startsWith('data:'));
      json = JSON.parse(dataLine.replace(/^data:\s*/, ''));
    } else {
      json = JSON.parse(raw);
    }
  } catch (err) {
    throw new Error(`Failed to parse MCP response: ${raw}`);
  }

  if (json.error) {
    throw new Error(`MCP Error ${json.error.code}: ${json.error.message}`);
  }
  return json.result;
}

async function main() {
  const [,, cmd, ...rest] = process.argv;

  switch (cmd) {
    case 'list-templates': {
      const result = await callMcpTool('list_templates', {});
      console.log(result.content?.[0]?.text || JSON.stringify(result, null, 2));
      break;
    }

    case 'balance': {
      if (!API_KEY) {
        console.error('Error: TRENDSWAP_API_KEY is not set. Please set it via export TRENDSWAP_API_KEY="sk_..."');
        process.exit(1);
      }
      const result = await callMcpTool('get_credits_balance', {});
      console.log(result.content?.[0]?.text || JSON.stringify(result, null, 2));
      break;
    }

    case 'create': {
      if (!API_KEY) {
        console.error('Error: TRENDSWAP_API_KEY is not set.');
        process.exit(1);
      }
      let template = '';
      let imageUrl = '';
      let resolution = '720p';

      for (let i = 0; i < rest.length; i++) {
        if (rest[i] === '--template' && rest[i + 1]) template = rest[++i];
        if (rest[i] === '--image-url' && rest[i + 1]) imageUrl = rest[++i];
        if (rest[i] === '--resolution' && rest[i + 1]) resolution = rest[++i];
      }

      if (!template || !imageUrl) {
        console.error('Usage: trendswap.mjs create --template <id> --image-url <url> [--resolution <480p|720p|1080p>]');
        process.exit(1);
      }

      const result = await callMcpTool('create_generation_job', {
        template,
        image_url: imageUrl,
        resolution,
      });
      console.log(result.content?.[0]?.text || JSON.stringify(result, null, 2));
      break;
    }

    case 'status': {
      if (!API_KEY) {
        console.error('Error: TRENDSWAP_API_KEY is not set.');
        process.exit(1);
      }
      let jobId = '';
      for (let i = 0; i < rest.length; i++) {
        if (rest[i] === '--job-id' && rest[i + 1]) jobId = rest[++i];
      }
      if (!jobId) {
        console.error('Usage: trendswap.mjs status --job-id <id>');
        process.exit(1);
      }
      const result = await callMcpTool('get_job_status', { job_id: jobId });
      console.log(result.content?.[0]?.text || JSON.stringify(result, null, 2));
      break;
    }

    default:
      console.log(`TrendSwap CLI Helper
Commands:
  list-templates                         List all public video templates
  balance                                Check account credit balance
  create --template <id> --image-url <url> [--resolution <480p|720p|1080p>]
  status --job-id <id>                   Query generation job status
`);
      break;
  }
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
