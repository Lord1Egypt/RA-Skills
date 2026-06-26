#!/usr/bin/env node
/**
 * Recall context from Supermemory for a given container.
 * Prints static facts, dynamic (recent) context, and relevant memories.
 * Designed to be run at agent session startup.
 *
 * Usage:
 *   node recall.js --container my-agent
 *   node recall.js --container my-agent --query "recent projects"
 *   node recall.js --container my-agent --limit 5
 */

const Supermemory = require('supermemory').default;

const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };

const container = get('--container') || get('-c');
const query = get('--query') || get('-q') || 'identity, recent context, active projects, key decisions';
const limit = parseInt(get('--limit') || '8', 10);

if (!container) { console.error('Error: --container is required'); process.exit(1); }

const apiKey = process.env.SUPERMEMORY_API_KEY;
if (!apiKey) { console.error('Error: SUPERMEMORY_API_KEY not set'); process.exit(1); }

const client = new Supermemory({ apiKey });

async function main() {
  let profile;
  try {
    profile = await client.profile({
      containerTag: container,
      q: query,
      threshold: 0.4,
    });
  } catch (e) {
    console.error('Recall failed:', e.message);
    process.exit(1);
  }

  const staticFacts = profile.profile?.static || [];
  const dynamic = profile.profile?.dynamic || [];
  const memories = profile.searchResults?.results || [];

  console.log(`=== MEMORY RECALL [${container}] ===\n`);

  if (staticFacts.length) {
    console.log('## Identity & Static Facts');
    staticFacts.forEach(s => console.log(' -', s));
    console.log();
  }

  if (dynamic.length) {
    console.log('## Recent Context');
    dynamic.forEach(d => console.log(' -', d));
    console.log();
  }

  if (memories.length) {
    console.log('## Relevant Memories');
    memories.slice(0, limit).forEach(m => {
      const chunk = m.chunks?.[0]?.content || '';
      const text = chunk || m.title || m.memory || m.content || JSON.stringify(m);
      console.log(' -', text.slice(0, 200));
    });
    console.log();
  }

  if (!staticFacts.length && !dynamic.length && !memories.length) {
    console.log('(no memories found for this container)');
  }

  console.log(`=== END RECALL ===`);
}

main().catch(e => { console.error(e.message); process.exit(1); });
