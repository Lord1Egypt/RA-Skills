#!/usr/bin/env node
/**
 * Search memories in a Supermemory container.
 *
 * Usage:
 *   node search.js --container my-agent --query "payment integration"
 *   node search.js --container my-agent --query "..." --limit 5 --threshold 0.6
 */

const Supermemory = require('supermemory').default;

const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };

const container = get('--container') || get('-c');
const query = get('--query') || get('-q');
const limit = parseInt(get('--limit') || '10', 10);
const threshold = parseFloat(get('--threshold') || '0.4');

if (!container) { console.error('Error: --container is required'); process.exit(1); }
if (!query) { console.error('Error: --query is required'); process.exit(1); }

const apiKey = process.env.SUPERMEMORY_API_KEY;
if (!apiKey) { console.error('Error: SUPERMEMORY_API_KEY not set'); process.exit(1); }

const client = new Supermemory({ apiKey });

async function main() {
  const results = await client.search.documents({
    q: query,
    containerTag: container,
    threshold,
    limit,
  });

  const hits = results.results || [];

  if (!hits.length) {
    console.log(`No memories found for "${query}" in [${container}]`);
    return;
  }

  console.log(`Found ${hits.length} result(s) for "${query}" in [${container}]:\n`);
  hits.forEach((r, i) => {
    const chunk = r.chunks?.[0]?.content || '';
    const text = chunk || r.title || JSON.stringify(r);
    const score = r.score ? ` (${(r.score * 100).toFixed(0)}%)` : '';
    console.log(`${i + 1}.${score} ${text.slice(0, 300)}`);
    if (text.length > 300) console.log('   ...');
    console.log();
  });
}

main().catch(e => { console.error(e.message); process.exit(1); });
