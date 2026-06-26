import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { generateProject, runCli } from './src/index.js';

// Test generateProject
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-starter-'));
const projectRoot = path.join(tmpDir, 'test-skill');

const manifest = generateProject({
  name: 'test-skill',
  description: 'A test skill',
  category: 'Test',
  template: 'standard',
  includeCI: true,
  projectRoot
});

assert.equal(manifest.template, 'standard');
assert.equal(manifest.files.includes('SKILL.md'), true);
assert.equal(manifest.files.includes('package.json'), true);
assert.equal(fs.existsSync(path.join(projectRoot, 'SKILL.md')), true);
assert.equal(fs.existsSync(path.join(projectRoot, 'package.json')), true);

// Test strict-security template
const strictDir = path.join(tmpDir, 'strict-skill');
const strictManifest = generateProject({
  name: 'strict-skill',
  description: 'A strict skill',
  category: 'Security',
  template: 'strict-security',
  includeCI: true,
  projectRoot: strictDir
});

assert.equal(strictManifest.template, 'strict-security');
assert.equal(fs.existsSync(path.join(strictDir, '.openclaw-tools/safe-install.policy.json')), true);
assert.equal(fs.existsSync(path.join(strictDir, '.github/workflows/security-scan.yml')), true);

// Test CLI with --no-prompts
const outDir = path.join(tmpDir, 'cli-test');
const code = await runCli(['my-skill', '--no-prompts', '--out', outDir, '--template', 'standard', '--ci']);
assert.equal(code, 0);
assert.equal(fs.existsSync(path.join(outDir, 'my-skill')), true);

console.log('skill-starter tests passed');
