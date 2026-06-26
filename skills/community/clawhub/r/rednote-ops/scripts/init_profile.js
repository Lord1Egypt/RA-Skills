const fs = require('fs');
const path = require('path');

const output = process.argv[2] || path.join(process.cwd(), 'data/xiaohongshu/profile.json');
const raw = process.argv[3];
if (!raw) {
  console.error('Usage: node init_profile.js <outputPath> <jsonString>');
  process.exit(1);
}

const obj = JSON.parse(raw);
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, JSON.stringify(obj, null, 2), 'utf8');
console.log(`Wrote profile to ${output}`);
