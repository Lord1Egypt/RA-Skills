const test = require('node:test');
const assert = require('node:assert');

const { listThemes, listLayouts } = require('../scripts/render');

test('listThemes returns themes from yuanfang-design/themes/', () => {
  const themes = listThemes();
  assert.ok(themes.length >= 1, 'should find at least 1 theme');
  assert.ok(themes.includes('minimal-white'));
});

test('listLayouts returns at least 1 layout', () => {
  const layouts = listLayouts();
  assert.ok(layouts.includes('cover'), 'should include cover');
});
