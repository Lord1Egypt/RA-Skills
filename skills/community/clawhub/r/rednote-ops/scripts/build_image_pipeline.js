const fs = require('fs');
const path = require('path');

const profilePath = process.argv[2] || path.join(process.cwd(), 'data/xiaohongshu/profile.json');
const topic = process.argv[3] || 'AI workflow';
const outDir = process.argv[4] || '/tmp/openclaw/uploads/xhs_image_pipeline';

const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const imageMode = profile.imageMode || 'mixed';
const plan = {
  topic,
  imageMode,
  publishPath: profile.publishPath || 'independent-browser',
  steps: [],
  outputs: {}
};

if (imageMode === 'stock' || imageMode === 'mixed') {
  plan.steps.push('generate-stock-search-plan');
  plan.outputs.stockPlan = path.join(outDir, 'stock-plan.json');
}

if (imageMode === 'cards-lite' || imageMode === 'mixed') {
  plan.steps.push('cards-lite-fallback');
  plan.outputs.cardsDir = path.join(outDir, 'cards-lite');
}

plan.steps.push('prepare-publish-assets');
plan.outputs.publishAssetDir = path.join(outDir, 'publish-assets');

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'pipeline-plan.json'), JSON.stringify(plan, null, 2), 'utf8');
console.log(`IMAGE_PIPELINE_READY ${path.join(outDir, 'pipeline-plan.json')}`);
console.log(JSON.stringify(plan, null, 2));
