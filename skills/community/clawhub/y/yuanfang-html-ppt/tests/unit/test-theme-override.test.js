const test = require('node:test');
const assert = require('node:assert');
const { applyThemeOverride } = require('../../scripts/theme-override');

const baseTheme = {
  bg: '#ffffff', text: '#111111', accent: '#4f46e5', secondary: '#64748b',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif', sizeH1: 60, sizeBase: 18,
};

test('applyThemeOverride returns same theme when override absent', () => {
  const result = applyThemeOverride(baseTheme, {});
  assert.deepStrictEqual(result, baseTheme);
  assert.notStrictEqual(result, baseTheme);
});

test('applyThemeOverride overrides specified keys only', () => {
  const result = applyThemeOverride(baseTheme, { themeOverride: { accent: '#ff0000' } });
  assert.strictEqual(result.accent, '#ff0000');
  assert.strictEqual(result.bg, '#ffffff');
  assert.strictEqual(result.text, '#111111');
});

test('applyThemeOverride supports multiple keys at once', () => {
  const result = applyThemeOverride(baseTheme, {
    themeOverride: { accent: '#ff0000', bg: '#000000', sizeH1: 100 },
  });
  assert.strictEqual(result.accent, '#ff0000');
  assert.strictEqual(result.bg, '#000000');
  assert.strictEqual(result.sizeH1, 100);
});

test('applyThemeOverride ignores null/undefined values', () => {
  const result = applyThemeOverride(baseTheme, {
    themeOverride: { accent: null, bg: undefined },
  });
  assert.strictEqual(result.accent, baseTheme.accent);
  assert.strictEqual(result.bg, baseTheme.bg);
});

test('applyThemeOverride does not mutate base theme (immutable)', () => {
  const result = applyThemeOverride(baseTheme, { themeOverride: { accent: '#ff0000' } });
  assert.strictEqual(baseTheme.accent, '#4f46e5');
  assert.strictEqual(result.accent, '#ff0000');
});

test('applyThemeOverride is safe for unknown keys (forward-compat)', () => {
  const result = applyThemeOverride(baseTheme, {
    themeOverride: { futureField: 'new-value' },
  });
  assert.strictEqual(result.futureField, 'new-value');
});
