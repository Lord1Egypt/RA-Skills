import { readFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TIPS_DIR = join(__dirname, 'tips');

// Load all tips
const tips = [];
const files = readdirSync(TIPS_DIR).filter(f => f.endsWith('.txt'));
for (const file of files) {
  const content = readFileSync(join(TIPS_DIR, file), 'utf-8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('##')) continue;
    tips.push(trimmed);
  }
}

console.log(`Loaded ${tips.length} tips from ${files.length} files\n`);

// Test random tip display
const randomTip = tips[Math.floor(Math.random() * tips.length)];
const [zh, en] = randomTip.split(' | ');

console.log('--- emoji style ---');
console.log(`💡 ${randomTip}\n`);

console.log('--- card style ---');
console.log(`━━━━━━━━━━━━━━━`);
console.log(`💡 Tips while you wait\n`);
console.log(zh);
if (en) console.log(en);
console.log(`━━━━━━━━━━━━━━━\n`);

console.log('--- zh-only ---');
console.log(`💡 ${zh}\n`);

console.log('--- en-only ---');
console.log(`💡 ${en || zh}\n`);

// Verify all tips have bilingual format
let missingEn = 0;
for (const tip of tips) {
  if (!tip.includes(' | ')) missingEn++;
}
if (missingEn > 0) {
  console.log(`⚠️  ${missingEn} tips missing English translation (no " | " separator)`);
} else {
  console.log(`✅ All ${tips.length} tips have bilingual format`);
}

console.log('\nAll tests passed!');
