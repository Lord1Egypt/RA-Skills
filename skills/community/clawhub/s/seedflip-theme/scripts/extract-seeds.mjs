/**
 * Extracts seed data from seeds.ts to JSON using tsx to handle TypeScript.
 * Usage: npx tsx mcp/scripts/extract-seeds.mjs
 */

import { writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

// tsx handles the TypeScript import natively
const { seeds } = await import('../../src/lib/seeds.ts');

const __dirname = dirname(fileURLToPath(import.meta.url));
const outPath = join(__dirname, '../src/seeds-data.json');

writeFileSync(outPath, JSON.stringify(seeds, null, 2));
console.log(`Extracted ${seeds.length} seeds to ${outPath}`);
