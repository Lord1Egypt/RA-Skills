#!/usr/bin/env node
/**
 * 校验 slides.json：templateId、必填槽位、maxLength、type
 * 用法: node scripts/validate-slides.js [slides.json路径]
 * 默认: output/slides.json
 * 失败时输出 "Slide N: ..." 便于 Agent 定位修改
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, '..');

const slidesPath = resolve(process.cwd(), process.argv[2] || 'output/slides.json');
const manifestPath = join(SKILL_ROOT, 'templates/manifest.json');

if (!existsSync(slidesPath)) {
  console.error(`slides.json not found: ${slidesPath}`);
  process.exit(1);
}
if (!existsSync(manifestPath)) {
  console.error(`manifest not found: ${manifestPath}`);
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
const slides = JSON.parse(readFileSync(slidesPath, 'utf-8'));

const templateMap = new Map(manifest.templates.map((t) => [t.id, t]));
const errors = [];

if (!Array.isArray(slides)) {
  errors.push('slides.json root must be an array');
  errors.forEach((e) => console.error(e));
  process.exit(1);
}

for (let i = 0; i < slides.length; i++) {
  const slideIndex = i + 1;
  const slide = slides[i];
  const templateId = slide?.templateId;
  const slots = slide?.slots || {};

  const template = templateId ? templateMap.get(templateId) : null;
  if (!template) {
    errors.push(`Slide ${slideIndex}: Unknown templateId '${templateId || ''}'`);
    continue;
  }

  for (const slot of template.slots) {
    const value = slots[slot.id];
    const optional = slot.optional === true;

    if (value === undefined || value === null || (typeof value === 'string' && value.trim() === '')) {
      if (!optional) {
        errors.push(`Slide ${slideIndex} (${templateId}): missing required slot '${slot.id}'`);
      }
      continue;
    }

    if (slot.maxLength != null && typeof value === 'string' && value.length > slot.maxLength) {
      errors.push(
        `Slide ${slideIndex} (${templateId}): slot '${slot.id}' exceeds maxLength ${slot.maxLength} (got ${value.length})`
      );
    }

    if (slot.type === 'image') {
      const s = String(value).trim();
      const isUrl = s.startsWith('http') || s.startsWith('data:');
      const isLucide = s.toLowerCase().startsWith('lucide:');
      const isLocal = !isUrl && !isLucide;
      if (isLocal && !existsSync(resolve(process.cwd(), s))) {
        errors.push(`Slide ${slideIndex} (${templateId}): slot '${slot.id}' file not found: ${s}`);
      }
    }
  }
}

if (errors.length > 0) {
  errors.forEach((e) => console.error(e));
  process.exit(1);
}

console.log(`OK. Validated ${slides.length} slides.`);
process.exit(0);
