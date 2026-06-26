#!/usr/bin/env node
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { validateSkillFrontmatter } from '../lib/deploy.mjs';

const dir = mkdtempSync(join(tmpdir(), 'ldm-skill-frontmatter-'));
const bad = join(dir, 'bad-SKILL.md');
const good = join(dir, 'good-SKILL.md');

writeFileSync(bad, [
  '---',
  'name: bad',
  'description: Read when: guard blocks a tool call',
  '---',
  '',
  '# Bad',
  '',
].join('\n'));

writeFileSync(good, [
  '---',
  'name: good',
  'description: "Read when: guard blocks a tool call"',
  '---',
  '',
  '# Good',
  '',
].join('\n'));

const badResult = validateSkillFrontmatter(bad);
if (badResult.ok) {
  throw new Error('expected unquoted colon frontmatter to be rejected');
}
if (badResult.line !== 3) {
  throw new Error(`expected failure on line 3, got line ${badResult.line}`);
}

const goodResult = validateSkillFrontmatter(good);
if (!goodResult.ok) {
  throw new Error(`expected quoted frontmatter to pass: ${goodResult.message}`);
}

console.log('skill frontmatter regression passed');
