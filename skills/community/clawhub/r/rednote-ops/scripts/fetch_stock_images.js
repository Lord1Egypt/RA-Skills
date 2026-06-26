const fs = require('fs');
const path = require('path');
const https = require('https');

function mapTopicToQueries(topic) {
  const t = String(topic || '').toLowerCase();
  const queries = [];
  if (t.includes('ai')) queries.push('artificial intelligence workspace', 'laptop modern desk', 'digital technology office');
  if (t.includes('workflow')) queries.push('productivity desk', 'task planning workspace', 'organized desk setup');
  if (t.includes('效率')) queries.push('productivity workspace', 'focus desk setup');
  if (!queries.length) queries.push('modern workspace', 'office desk', 'creative work desk');
  return [...new Set(queries)];
}

function writeManifest(outDir, topic, queries) {
  const manifest = {
    topic,
    queries,
    sourcePolicy: 'watermark-free only',
    preferredSources: ['Unsplash', 'Pexels', 'Pixabay'],
    fetchedAt: new Date().toISOString()
  };
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'stock-plan.json'), JSON.stringify(manifest, null, 2), 'utf8');
}

async function main() {
  const topic = process.argv[2] || 'AI workflow';
  const outDir = process.argv[3] || '/tmp/openclaw/uploads/xhs_stock_plan';
  const queries = mapTopicToQueries(topic);
  writeManifest(outDir, topic, queries);
  console.log(`STOCK_IMAGE_PLAN_READY ${outDir}`);
  console.log(JSON.stringify({ topic, queries, outDir }, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
