#!/usr/bin/env node
// Optional CLI for agents with a shell. Pure: reads only the file you name, makes no request.
//   node scripts/screen.mjs url <url> [--provenance <url>]... [--task-text <text>]... [--public-name <name>]...
//   node scripts/screen.mjs redirect <requested-url> <final-url>
//   node scripts/screen.mjs content <file>
import { readFile } from 'node:fs/promises';
import { screenUrl, screenRedirect, screenContent } from './url-screen.mjs';

const [command, ...rest] = process.argv.slice(2);
const take = (flag) => rest.flatMap((a, i) => (a === flag && rest[i + 1] !== undefined ? [rest[i + 1]] : []));
try {
  let result;
  if (command === 'url' && rest[0]) result = screenUrl(rest[0], { provenance: take('--provenance'), taskTexts: take('--task-text'), publicNames: take('--public-name') });
  else if (command === 'redirect' && rest[1]) result = screenRedirect(rest[0], rest[1]);
  else if (command === 'content' && rest[0]) result = screenContent(await readFile(rest[0], 'utf8'));
  else throw new Error('Usage: screen.mjs url <url> [--provenance U]... [--task-text T]... [--public-name N]... | redirect <requested> <final> | content <file>');
  console.log(JSON.stringify(result, null, 2));
  process.exitCode = result.verdict === 'BLOCK' ? 2 : 0;
} catch (error) { console.error(error.message); process.exitCode = 1; }
