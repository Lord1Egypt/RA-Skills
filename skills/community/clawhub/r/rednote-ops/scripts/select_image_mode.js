const fs = require('fs');
const path = require('path');

const profilePath = process.argv[2] || path.join(process.cwd(), 'data/xiaohongshu/profile.json');
const outPath = process.argv[3] || '/tmp/openclaw/uploads/xhs_image_mode.json';

const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const result = {
  imageMode: profile.imageMode || 'mixed',
  publishPath: profile.publishPath || 'independent-browser',
  generateCardsByDefault: !!profile.generateCardsByDefault,
  preferredSources: ['Unsplash', 'Pexels', 'Pixabay'],
  fallback: 'cards-lite',
  watermarkPolicy: 'forbid-removal'
};

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf8');
console.log(`IMAGE_MODE_READY ${outPath}`);
console.log(JSON.stringify(result, null, 2));
