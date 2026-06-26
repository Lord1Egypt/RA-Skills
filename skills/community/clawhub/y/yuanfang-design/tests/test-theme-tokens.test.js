// Validates every theme defines the full set of required design tokens.
// Catches themes that miss --surface / --text-1, which silently break
// card contrast in dark themes (white text on white card).

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const THEMES_DIR = path.join(__dirname, '..', 'themes');
const REQUIRED_TOKENS = [
  '--bg',
  '--surface',
  '--surface-2',
  '--border',
  '--text-1',
  '--text-2',
  '--text-3',
  '--accent',
];

test('every theme defines the required tokens for proper contrast', () => {
  const files = fs.readdirSync(THEMES_DIR).filter(f => f.endsWith('.css'));
  assert.ok(files.length > 0, 'no theme files found');
  for (const f of files) {
    const css = fs.readFileSync(path.join(THEMES_DIR, f), 'utf8');
    for (const token of REQUIRED_TOKENS) {
      assert.ok(
        css.includes(`${token}:`),
        `${f} missing ${token}`
      );
    }
  }
});
