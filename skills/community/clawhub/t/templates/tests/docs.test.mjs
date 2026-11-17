import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { describe, it } from 'node:test';

const skillRoot = path.resolve(import.meta.dirname, '..');
const repoRoot = path.resolve(skillRoot, '../..');

async function readText(relativePath) {
  return fs.readFile(path.join(repoRoot, relativePath), 'utf8');
}

function extractFigmaSection(text) {
  const start = text.indexOf('# Figma 设计稿读取规则');
  const end = text.indexOf('# 必须遵守的约定', start);
  return text.slice(start, end);
}

describe('read-figma-design docs', () => {
  it('keeps the skill entrypoint short, relative, and explicit about offline diagnostics', async () => {
    const skill = await readText('outer-skills/read-figma-design/SKILL.md');

    assert.match(skill, /^name: read-figma-design$/m);
    assert.match(skill, /node scripts\/read-figma-context\.mjs/);
    assert.match(skill, /node scripts\/smoke-figma-context\.mjs/);
    assert.match(skill, /--help.*without reading credentials or network/i);
    assert.match(skill, /--version.*without reading credentials or network/i);
    assert.doesNotMatch(skill, /\/Users\/bytedance|\/home\/dujuncheng/);
    assert.doesNotMatch(skill, /figd_[A-Za-z0-9_-]+|FIGMA_ACCESS_TOKEN=/);
  });

  it('ships a fixed summary template for the generated summary contract', async () => {
    const template = await readText('outer-skills/read-figma-design/templates/figma-context-summary.md');

    assert.match(template, /# Figma Context Summary/);
    assert.match(template, /## URL <ordinal>/);
    assert.match(template, /Source URL/);
    assert.match(template, /Canonical node id/);
    assert.match(template, /Target screenshot/);
    assert.match(template, /Parent screenshot/);
    assert.match(template, /Code Connect/);
    assert.match(template, /Visual requirements/);
    assert.match(template, /Open questions/);
  });

  it('aligns the repair expert Figma section with the skill contract without machine-specific command paths', async () => {
    const doc = await readText('.docs/done/自动处理issue/修复专家的指令.md');
    const figmaSection = extractFigmaSection(doc);

    assert.match(figmaSection, /figma_urls/);
    assert.match(figmaSection, /read-figma-design/);
    assert.match(figmaSection, /summary\.md/);
    assert.match(figmaSection, /manifest\.json/);
    assert.match(figmaSection, /design-properties\.json/);
    assert.match(figmaSection, /code-connect\.json/);
    assert.match(figmaSection, /截图/);
    assert.match(figmaSection, /node scripts\/read-figma-context\.mjs/);
    assert.match(figmaSection, /Code Connect 不可用不阻断修复/);
    assert.doesNotMatch(figmaSection, /\/Users\/bytedance|\/home\/dujuncheng|10\.37\.206\.166/);
  });
});
