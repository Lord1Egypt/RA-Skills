const test = require('node:test');
const assert = require('node:assert');
const { parseColorValue, applyDecorCorners } = require('../../scripts/decor');
const { renderCover } = require('../../scripts/generator-a');

test('parseColorValue: hex string passes through', () => {
  assert.strictEqual(parseColorValue('#ff5500', '#000'), '#ff5500');
});

test('parseColorValue: "none" / "" returns null (not rendered)', () => {
  assert.strictEqual(parseColorValue('none', '#000'), null);
  assert.strictEqual(parseColorValue('', '#000'), null);
});

test('parseColorValue: rgb() converts to hex', () => {
  assert.strictEqual(parseColorValue('rgb(255, 85, 0)', '#000'), '#FF5500');
  assert.strictEqual(parseColorValue('rgba(0, 0, 0, 0.5)', '#000'), '#000000');
});

test('parseColorValue: linear-gradient falls back to default (gradients not supported in pptxgenjs)', () => {
  assert.strictEqual(parseColorValue('linear-gradient(135deg, red, blue)', '#fallback'), '#fallback');
});

test('parseColorValue: non-string returns fallback', () => {
  assert.strictEqual(parseColorValue(null, '#fff'), '#fff');
  assert.strictEqual(parseColorValue(undefined, '#fff'), '#fff');
  assert.strictEqual(parseColorValue(123, '#fff'), '#fff');
});

test('applyDecorCorners: emits 4 rect shapes when all 4 decor tokens set', () => {
  const calls = [];
  const slide = { addShape: (shape, opts) => { calls.push({ shape, opts }); return slide; } };
  const theme = {
    decorTL: '#ff0000',
    decorTR: '#00ff00',
    decorBL: '#0000ff',
    decorBR: '#ffff00',
    accent: '#000000',
    space4: 48,
  };
  applyDecorCorners(slide, theme, { w: 13.333, h: 7.5 });
  assert.strictEqual(calls.length, 4);
  for (const c of calls) {
    assert.strictEqual(c.shape, 'rect');
    assert.ok(c.opts.fill.color);
  }
  const colors = calls.map(c => c.opts.fill.color);
  assert.ok(colors.includes('#ff0000'));
  assert.ok(colors.includes('#00ff00'));
  assert.ok(colors.includes('#0000ff'));
  assert.ok(colors.includes('#ffff00'));
});

test('applyDecorCorners: emits 0 shapes when all tokens are "none"', () => {
  const calls = [];
  const slide = { addShape: (shape, opts) => { calls.push({ shape, opts }); return slide; } };
  const theme = { decorTL: 'none', decorTR: 'none', decorBL: 'none', decorBR: 'none', space4: 48 };
  applyDecorCorners(slide, theme, { w: 13.333, h: 7.5 });
  assert.strictEqual(calls.length, 0);
});

test('applyDecorCorners: emits only non-none corners', () => {
  const calls = [];
  const slide = { addShape: (shape, opts) => { calls.push({ shape, opts }); return slide; } };
  const theme = { decorTL: '#ff0000', decorTR: 'none', decorBL: '', decorBR: 'block', space4: 48 };
  applyDecorCorners(slide, theme, { w: 13.333, h: 7.5 });
  assert.strictEqual(calls.length, 1);
  assert.strictEqual(calls[0].opts.fill.color, '#ff0000');
});

test('renderCover emits corner decorations for bold-poster-style themes', () => {
  const calls = [];
  const slide = {
    background: null,
    addText: () => slide,
    addShape: (shape, opts) => { calls.push({ shape, opts }); return slide; },
    addImage: () => slide,
    addNotes: () => slide,
  };
  const theme = {
    bg: '#fff', text: '#000', accent: '#4f46e5', fontBody: 'Arial', fontTitle: 'Arial',
    sizeH1: 60, sizeH2: 28, sizeBase: 18, sizeSm: 12, sizeH3: 20,
    spacing: 12, space4: 48, rectRadius: 8, textSecondary: '#666',
    decorTL: '#ff5500', decorTR: '#00aaff', decorBL: 'none', decorBR: 'none',
  };
  const pres = { addSlide: () => slide };
  renderCover(pres, { title: 'T' }, theme, { w: 13.333, h: 7.5 });
  const rects = calls.filter(c => c.shape === 'rect');
  assert.ok(rects.length >= 2, `should emit at least 2 corner rectangles, got ${rects.length}`);
  const colors = rects.map(r => r.opts.fill.color);
  assert.ok(colors.includes('#ff5500'));
  assert.ok(colors.includes('#00aaff'));
});
