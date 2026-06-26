#!/usr/bin/env node
/**
 * 一键流水线：校验 → 填充模板 → 转 PPTX
 * 用法: node scripts/run-pipeline.js [slides.json路径] [输出pptx路径]
 * 默认: output/slides.json → output/presentation.pptx
 * 便于 Agent 只跑一条命令完成步骤 3+4
 */

import { spawnSync } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync, mkdirSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPTS_DIR = __dirname;
const SKILL_ROOT = join(__dirname, '..');

const slidesPath = process.argv[2] || 'output/slides.json';

function defaultOutputPath() {
  const ts = new Date().toISOString().replace(/[:T]/g, '-').replace(/\..+/, '');
  return `output/presentation-${ts}.pptx`;
}

const outputPptxPath = process.argv[3] || defaultOutputPath();

function checkEnv() {
  const manifestPath = join(SKILL_ROOT, 'templates/manifest.json');
  const domToPptxPath = join(SKILL_ROOT, 'node_modules/dom-to-pptx');
  const puppeteerPath = join(SKILL_ROOT, 'node_modules/puppeteer');
  if (!existsSync(manifestPath)) {
    console.error('Error: templates/manifest.json not found. Is the skill path correct?');
    process.exit(1);
  }
  if (!existsSync(domToPptxPath)) {
    console.error('Error: dom-to-pptx not found. Please run "npm install" in the skill directory.');
    process.exit(1);
  }
  if (!existsSync(puppeteerPath)) {
    console.error('Error: puppeteer not found. Please run "npm install" in the skill directory.');
    process.exit(1);
  }
}

function ensureOutputDirs() {
  const cwd = process.cwd();
  const dirs = ['output', 'output/filled', 'output/images'];
  for (const d of dirs) {
    mkdirSync(join(cwd, d), { recursive: true });
  }
}

function run(scriptName, args = []) {
  const result = spawnSync('node', [join(SCRIPTS_DIR, scriptName), ...args], {
    stdio: 'inherit',
    cwd: process.cwd(),
  });
  return result.status;
}

checkEnv();
ensureOutputDirs();

console.log('Step 1/3: Validating slides.json...');
if (run('validate-slides.js', [slidesPath]) !== 0) {
  process.exit(1);
}

console.log('Step 2/3: Filling HTML templates...');
if (run('fill-template.js', [slidesPath]) !== 0) {
  process.exit(1);
}

console.log('Step 3/3: Converting to PPTX...');
if (run('html-to-pptx-dom.js', ['output/filled', outputPptxPath]) !== 0) {
  process.exit(1);
}

console.log(`Done. PPT saved to ${outputPptxPath}`);
