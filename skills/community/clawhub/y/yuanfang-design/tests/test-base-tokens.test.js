const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

const BASE_CSS_PATH = path.join(__dirname, '..', 'base.css');

test('base.css exists', () => {
  assert.ok(fs.existsSync(BASE_CSS_PATH), 'base.css should exist');
});

test('base.css defines required color tokens', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  for (const token of ['--bg', '--text', '--accent', '--secondary', '--bg-alt']) {
    assert.ok(css.includes(`${token}:`), `base.css must define ${token}`);
  }
});

test('base.css defines required type tokens', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  for (const token of ['--font-title', '--font-body']) {
    assert.ok(css.includes(`${token}:`), `base.css must define ${token}`);
  }
});

test('base.css defines required size tokens (5 ratios)', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  for (const token of ['--title-size-v', '--title-size-s', '--title-size-w', '--title-size-c', '--content-size']) {
    assert.ok(css.includes(`${token}:`), `base.css must define ${token}`);
  }
});

test('base.css defines decor tokens', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  for (const token of ['--decor-tl', '--decor-tr', '--decor-bl', '--decor-br']) {
    assert.ok(css.includes(`${token}:`), `base.css must define ${token}`);
  }
});

test('base.css defines feature flags', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  for (const token of ['--accent-line', '--accent-block', '--terminal-bar', '--grid-bg', '--seal']) {
    assert.ok(css.includes(`${token}:`), `base.css must define ${token}`);
  }
});

test('base.css has zero hardcoded color literals in .cover rules', () => {
  const css = fs.readFileSync(BASE_CSS_PATH, 'utf-8');
  const coverBlocks = css.match(/(?:^|\s)\.cover[\w_-]*\s*\{[^}]*\}/g) || [];
  for (const block of coverBlocks) {
    assert.ok(!/#[0-9a-fA-F]{3,6}\b/.test(block), 'cover block must not contain hex colors; use var(--*)');
  }
});
