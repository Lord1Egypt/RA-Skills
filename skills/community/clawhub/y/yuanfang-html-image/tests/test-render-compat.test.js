const test = require('node:test');
const assert = require('node:assert');
const { parseArgs, resolveTemplate } = require('../scripts/render');

test('parseArgs accepts --theme and --layout', () => {
  const args = parseArgs(['node', 'render.js', '--theme', 'dark-gold', '--layout', 'cover']);
  assert.strictEqual(args.theme, 'dark-gold');
  assert.strictEqual(args.layout, 'cover');
});

test('parseArgs accepts legacy --template 1', () => {
  const args = parseArgs(['node', 'render.js', '--template', '1']);
  assert.strictEqual(args.template, '1');
});

test('resolveTemplate maps --template 1 to minimal-white/cover', () => {
  const args = { template: '1' };
  const resolved = resolveTemplate(args);
  assert.strictEqual(resolved.theme, 'minimal-white');
  assert.strictEqual(resolved.layout, 'cover');
});

test('resolveTemplate prioritizes --theme over --template', () => {
  const args = { template: '1', theme: 'dark-gold' };
  const resolved = resolveTemplate(args);
  assert.strictEqual(resolved.theme, 'dark-gold');
});
