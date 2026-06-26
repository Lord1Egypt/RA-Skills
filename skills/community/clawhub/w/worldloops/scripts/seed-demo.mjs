import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');

const src = path.join(root, 'scripts/fixtures/openclaw-signal-intake/mixed-observations.json');
const dest = path.join(root, '.worldloops/inbox/openclaw-observations.json');

if (!fs.existsSync(src)) {
  process.stderr.write(`Error: source fixture not found: ${src}\n`);
  process.exit(1);
}

fs.mkdirSync(path.dirname(dest), { recursive: true });
fs.copyFileSync(src, dest);
console.log(`Demo seeded: ${dest}`);
console.log('Run: npm run telegram:test');
