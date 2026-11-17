#!/usr/bin/env node
// Reads only the explicitly named input (a file, or standard input for "-"). No env/config, HTTP, wallet or signer imports.
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { preview, previewText, checkSummary, templates } from './preview-core.mjs';

const stdin = async () => { let text = ''; for await (const chunk of process.stdin) text += chunk; return text; };
const sha256Hex = text => createHash('sha256').update(text).digest('hex');

if (process.argv[2] === '--templates') console.log(JSON.stringify(templates, null, 2));
else {
  try {
    // --check prints a short summary for the agent; without it the full preview, the file the website and binder commit to.
    const check = process.argv[2] === '--check';
    const source = process.argv[check ? 3 : 2];
    if (!source) throw new Error('Usage: node scripts/preview.mjs [--check] assessment.json | - (read standard input) | --templates');
    const result = preview(JSON.parse(source === '-' ? await stdin() : await readFile(source, 'utf8')));
    process.stdout.write(check ? `${JSON.stringify(checkSummary(result, sha256Hex), null, 2)}\n` : previewText(result));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
