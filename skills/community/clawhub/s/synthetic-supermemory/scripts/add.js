#!/usr/bin/env node
/**
 * Add a single memory to Supermemory.
 *
 * Usage:
 *   node add.js --container my-agent --content "User prefers TypeScript"
 *   echo "Some memory text" | node add.js --container my-agent
 *   node add.js --container my-agent --content "..." --tag project:tokteam
 */

const Supermemory = require('supermemory').default;
const fs = require('fs');

const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };

const container = get('--container') || get('-c');
const contentArg = get('--content');
const tag = get('--tag');

if (!container) { console.error('Error: --container is required'); process.exit(1); }

const apiKey = process.env.SUPERMEMORY_API_KEY;
if (!apiKey) { console.error('Error: SUPERMEMORY_API_KEY not set'); process.exit(1); }

const client = new Supermemory({ apiKey });

async function main() {
  let content = contentArg;

  // Read from stdin if no --content arg and stdin is piped
  if (!content && !process.stdin.isTTY) {
    content = fs.readFileSync('/dev/stdin', 'utf8').trim();
  }

  if (!content) {
    console.error('Error: provide --content or pipe content via stdin');
    process.exit(1);
  }

  const metadata = {
    source: 'manual',
    addedAt: new Date().toISOString(),
    ...(tag ? { tag } : {})
  };

  const result = await client.add({ content, containerTag: container, metadata });
  console.log(`✅ Memory added to [${container}]: ${result.id}`);
}

main().catch(e => { console.error(e.message); process.exit(1); });
