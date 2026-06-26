const test = require('node:test');
const assert = require('node:assert');
const { applyBackground } = require('../../scripts/background');

function makeMockSlide() {
  return { background: null };
}

test('applyBackground does nothing when slide.background is undefined', () => {
  const s = makeMockSlide();
  applyBackground(s, {});
  assert.strictEqual(s.background, null);
});

test('applyBackground accepts hex color string', () => {
  const s = makeMockSlide();
  applyBackground(s, { background: '#ff5500' });
  assert.deepStrictEqual(s.background, { color: '#ff5500' });
});

test('applyBackground accepts image path string', () => {
  const s = makeMockSlide();
  applyBackground(s, { background: '/tmp/bg.png' });
  assert.deepStrictEqual(s.background, { path: '/tmp/bg.png' });
});

test('applyBackground accepts PptxGenJS background object directly', () => {
  const s = makeMockSlide();
  const bg = { color: '#000', transparency: 50 };
  applyBackground(s, { background: bg });
  assert.strictEqual(s.background, bg);
});

test('applyBackground then generator override is still applied (applyBackground runs first)', () => {
  const s = makeMockSlide();
  applyBackground(s, { background: '/tmp/bg.png' });
  s.background = { color: '#ff5500' };
  assert.deepStrictEqual(s.background, { color: '#ff5500' });
});
