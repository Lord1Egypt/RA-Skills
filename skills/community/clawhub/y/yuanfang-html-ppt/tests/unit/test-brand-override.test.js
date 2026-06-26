const test = require('node:test');
const assert = require('node:assert');
const { applyBrandOverride, isHexColor, getBrandField } = require('../../scripts/brand-override');

test('isHexColor accepts #RGB, #RRGGBB, #RRGGBBAA', () => {
  assert.ok(isHexColor('#fff'));
  assert.ok(isHexColor('#FFFFFF'));
  assert.ok(isHexColor('#aabbccdd'));
  assert.ok(!isHexColor('blue'));
  assert.ok(!isHexColor('rgb(0,0,0)'));
  assert.ok(!isHexColor(123));
});

test('getBrandField handles both flat and nested brand spec formats', () => {
  const flat = { primary: '#ff0000' };
  const nested = { colors: { primary: '#00ff00' } };
  assert.strictEqual(getBrandField(flat, [['primary', 'x'], ['colors.primary', 'x']]), '#ff0000');
  assert.strictEqual(getBrandField(nested, [['primary', 'x'], ['colors.primary', 'x']]), '#00ff00');
});

test('applyBrandOverride: spec.primary overrides theme.accent', () => {
  const theme = { accent: '#4f46e5', secondary: '#64748b' };
  const spec = { primary: '#ff5500' };
  const next = applyBrandOverride(theme, spec);
  assert.strictEqual(next.accent, '#ff5500');
  assert.strictEqual(next.secondary, '#64748b');
});

test('applyBrandOverride: nested colors.primary also works', () => {
  const theme = { accent: '#4f46e5' };
  const spec = { colors: { primary: '#abcdef' } };
  const next = applyBrandOverride(theme, spec);
  assert.strictEqual(next.accent, '#abcdef');
});

test('applyBrandOverride: invalid color is ignored (not crashed)', () => {
  const theme = { accent: '#4f46e5' };
  const spec = { primary: 'not-a-color' };
  const next = applyBrandOverride(theme, spec);
  assert.strictEqual(next.accent, '#4f46e5');
});

test('applyBrandOverride: spec.secondary overrides theme.secondary', () => {
  const theme = { accent: '#4f46e5', secondary: '#64748b' };
  const spec = { secondary: '#123456' };
  const next = applyBrandOverride(theme, spec);
  assert.strictEqual(next.secondary, '#123456');
});

test('applyBrandOverride: empty / null spec returns theme unchanged (immutable)', () => {
  const theme = { accent: '#4f46e5' };
  assert.deepStrictEqual(applyBrandOverride(theme, null), theme);
  assert.deepStrictEqual(applyBrandOverride(theme, undefined), theme);
  assert.deepStrictEqual(applyBrandOverride(theme, {}), theme);
});

test('applyBrandOverride: returns new object (does not mutate input)', () => {
  const theme = { accent: '#4f46e5' };
  const next = applyBrandOverride(theme, { primary: '#ff0000' });
  assert.notStrictEqual(next, theme);
  assert.strictEqual(theme.accent, '#4f46e5');
});
