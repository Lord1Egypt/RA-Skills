const test = require('node:test');
const assert = require('node:assert');
const path = require('node:path');
const { parseCSSVariables, mapToPptxTheme, listThemes, loadTheme } = require('../../scripts/theme-mapper');

const DESIGN_DIR = path.resolve(__dirname, '..', '..', '..', 'yuanfang-design');

test('parseCSSVariables extracts --name: value pairs', () => {
  const css = `
    /* a comment */
    :root {
      --color-bg-primary: #ffffff;
      --font-size-h1: 32px;
      --spacing-unit: 8px;
    }
    body { color: red; }
  `;
  const vars = parseCSSVariables(css);
  assert.strictEqual(vars['--color-bg-primary'], '#ffffff');
  assert.strictEqual(vars['--font-size-h1'], '32px');
  assert.strictEqual(vars['--spacing-unit'], '8px');
  assert.strictEqual(vars['color'], undefined);
});

test('mapToPptxTheme converts px to pt (1px = 0.75pt) using real yuanfang-design tokens', () => {
  const tokens = {
    '--bg': '#ffffff',
    '--text': '#111111',
    '--accent': '#4f46e5',
    '--secondary': '#64748b',
    '--bg-alt': '#f8fafc',
    '--font-body': 'system-ui',
    '--font-title': 'Georgia, serif',
    '--content-size': '38px',
    '--title-size-w': '88px',
    '--title-size-s': '96px',
    '--title-size-c': '64px',
    '--source-size': '14px',
    '--space-2': '16px',
    '--radius': '12px',
  };
  const theme = mapToPptxTheme(tokens);
  assert.strictEqual(theme.bg, '#ffffff');
  assert.strictEqual(theme.text, '#111111');
  assert.strictEqual(theme.accent, '#4f46e5');
  assert.strictEqual(theme.bgAlt, '#f8fafc');
  assert.strictEqual(theme.fontBody, 'system-ui');
  assert.strictEqual(theme.fontTitle, 'Georgia, serif');
  assert.strictEqual(theme.sizeBase, 28.5);
  assert.strictEqual(theme.sizeH1, 66);
  assert.strictEqual(theme.sizeH2, 72);
  assert.strictEqual(theme.sizeH3, 48);
  assert.strictEqual(theme.sizeSm, 10.5);
  assert.strictEqual(theme.spacing, 12);
  assert.strictEqual(theme.rectRadius, 9);
});

test('listThemes returns all 12 theme names from real yuanfang-design', () => {
  const themes = listThemes(DESIGN_DIR);
  assert.ok(themes.length >= 12, `expected >=12 themes, got ${themes.length}`);
  assert.ok(themes.includes('minimal-white'));
  assert.ok(themes.includes('dark-gold'));
  assert.ok(themes.includes('eastern'));
});

test('loadTheme loads real minimal-white with all required fields', () => {
  const theme = loadTheme('minimal-white', DESIGN_DIR);
  assert.ok(theme.bg);
  assert.ok(theme.text);
  assert.ok(theme.accent);
  assert.ok(theme.fontBody);
  assert.ok(typeof theme.sizeH1 === 'number');
});

test('loadTheme loads eastern theme and exposes --seal', () => {
  const theme = loadTheme('eastern', DESIGN_DIR);
  assert.ok(theme.seal, 'eastern theme should have --seal set');
  assert.notStrictEqual(theme.seal, '""');
});

test('loadTheme loads tech-modern and exposes --terminal-bar', () => {
  const theme = loadTheme('tech-modern', DESIGN_DIR);
  assert.ok(theme.terminalBar, `tech-modern terminalBar should be set, got: ${theme.terminalBar}`);
  assert.notStrictEqual(theme.terminalBar, 'none');
});

test('loadTheme throws clear error for unknown theme', () => {
  assert.throws(() => loadTheme('minimalist', DESIGN_DIR), /主题 'minimalist' 不存在/);
});

test('mapToPptxTheme exposes space1, space2, space3, space4 + decor + feature flags', () => {
  const tokens = {
    '--space-1': '8px', '--space-2': '16px', '--space-3': '24px', '--space-4': '48px',
    '--decor-tl': 'block', '--accent-line': 'block', '--terminal-bar': 'flex',
  };
  const theme = mapToPptxTheme(tokens);
  assert.strictEqual(theme.space1, 6);
  assert.strictEqual(theme.space2, 12);
  assert.strictEqual(theme.space3, 18);
  assert.strictEqual(theme.space4, 36);
  assert.strictEqual(theme.decorTL, 'block');
  assert.strictEqual(theme.accentLine, 'block');
  assert.strictEqual(theme.terminalBar, 'flex');
});
