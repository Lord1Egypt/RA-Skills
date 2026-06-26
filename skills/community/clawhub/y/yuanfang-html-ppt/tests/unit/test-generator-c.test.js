const test = require('node:test');
const assert = require('node:assert');
const {
  renderSection, renderTwoColumn, renderData, renderQuote,
  buildSection, buildTwoColumn, buildData, buildQuote,
  applyFeatureFlags, DEFAULT_DIMS,
} = require('../../scripts/generator-c');

const baseTheme = {
  bg: '#ffffff', text: '#111111', textSecondary: '#666666',
  accent: '#4f46e5', secondary: '#64748b', bgAlt: '#f5f5f5',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif',
  sizeH1: 60, sizeH2: 28, sizeBase: 18, sizeSm: 12, sizeH3: 20,
  spacing: 12, space1: 6, space3: 18, rectRadius: 8, shadow: 'none',
  accentLine: 'none', accentBlock: 'none', terminalBar: 'none',
};

function makeMockPres() {
  const calls = [];
  const slide = {
    background: null,
    addText: function(text, opts) { calls.push({ type: 'text', text, opts }); return this; },
    addShape: function(shape, opts) { calls.push({ type: 'shape', shape, opts }); return this; },
    addImage: function(opts) { calls.push({ type: 'image', opts }); return this; },
  };
  return {
    addSlide: function() { return slide; },
    _calls: calls,
    _slide: slide,
  };
}

test('buildTwoColumn uses theme.space3 for inter-column gap (not hardcoded 0.3in)', () => {
  const pres = makeMockPres();
  buildTwoColumn(pres, {
    title: '对比', leftTitle: '我们', leftPoints: ['a'],
    rightTitle: '竞品', rightPoints: ['b'],
  }, baseTheme, DEFAULT_DIMS);
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'roundRect');
  assert.strictEqual(rects.length, 2);
  // Left card right edge + gap = right card left edge
  const leftRightEdge = rects[0].opts.x + rects[0].opts.w;
  const gap = rects[1].opts.x - leftRightEdge;
  assert.ok(gap > 0, `col gap should be positive, got ${gap}`);
  const textOpts = pres._calls.filter(c => c.type === 'text' && c.text === '我们').map(c => c.opts);
  assert.ok(textOpts[0].x > rects[0].opts.x, 'title should be indented inside card');
});

test('buildData uses theme.space3 for inter-card gap', () => {
  const pres = makeMockPres();
  buildData(pres, {
    title: '指标',
    metrics: [
      { label: 'MAU', value: '120 万', change: '+15%' },
      { label: '营收', value: '¥580 万', change: '+22%' },
      { label: '用户', value: '50 万', change: '+8%' },
    ],
  }, baseTheme, DEFAULT_DIMS);
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'roundRect');
  assert.strictEqual(rects.length, 3);
  // Cards should not overlap
  for (let i = 1; i < rects.length; i++) {
    assert.ok(rects[i].opts.x >= rects[i - 1].opts.x + rects[i - 1].opts.w,
      `card ${i} overlaps card ${i - 1}`);
  }
  const textCalls = pres._calls.filter(c => c.type === 'text' && c.text === '120 万');
  assert.ok(textCalls[0].opts.x > rects[0].opts.x, 'value should be padded inside card');
});

test('buildSection emits title twice (accent watermark + main) and accent line', () => {
  const pres = makeMockPres();
  buildSection(pres, { title: '战略方向' }, baseTheme, DEFAULT_DIMS);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.filter(t => t === '战略方向').length >= 2);
  const shapes = pres._calls.filter(c => c.type === 'shape');
  assert.ok(shapes.some(s => s.shape === 'line'));
});

test('buildTwoColumn emits 2 roundRect cards with both titles', () => {
  const pres = makeMockPres();
  buildTwoColumn(pres, {
    title: '对比', leftTitle: '我们', leftPoints: ['a', 'b'],
    rightTitle: '竞品', rightPoints: ['x', 'y'],
  }, baseTheme, DEFAULT_DIMS);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('我们'));
  assert.ok(texts.includes('竞品'));
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'roundRect');
  assert.strictEqual(rects.length, 2);
});

test('buildData emits one card per metric, value text + change text', () => {
  const pres = makeMockPres();
  buildData(pres, {
    title: '指标',
    metrics: [
      { label: 'MAU', value: '120 万', change: '+15%' },
      { label: '营收', value: '¥580 万', change: '+22%' },
    ],
  }, baseTheme, DEFAULT_DIMS);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('120 万'));
  assert.ok(texts.includes('+15%'));
  assert.ok(texts.includes('¥580 万'));
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'roundRect');
  assert.strictEqual(rects.length, 2);
});

test('buildData with empty metrics still produces title-only slide', () => {
  const pres = makeMockPres();
  buildData(pres, { title: '指标', metrics: [] }, baseTheme, DEFAULT_DIMS);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('指标'));
});

test('buildQuote emits quote mark, quote text, and attribution', () => {
  const pres = makeMockPres();
  buildQuote(pres, {
    title: '客户评价', quote: '改变工作方式', attribution: '张伟',
  }, baseTheme, DEFAULT_DIMS);
  const texts = pres._calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('"'));
  assert.ok(texts.includes('改变工作方式'));
  assert.ok(texts.some(t => t.includes('张伟')));
});

test('applyFeatureFlags adds accent-line when accentLine is set', () => {
  const pres = makeMockPres();
  const theme = { ...baseTheme, accentLine: 'block' };
  const slide = pres._slide;
  applyFeatureFlags(slide, theme, DEFAULT_DIMS);
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'rect');
  assert.ok(rects.length >= 1);
});

test('applyFeatureFlags adds 3 terminal-bar dots when terminalBar is set', () => {
  const pres = makeMockPres();
  const theme = { ...baseTheme, terminalBar: 'flex' };
  const slide = pres._slide;
  applyFeatureFlags(slide, theme, DEFAULT_DIMS);
  const dots = pres._calls.filter(c => c.type === 'shape' && c.shape === 'ellipse');
  assert.strictEqual(dots.length, 3);
});

test('applyFeatureFlags is no-op when all flags are none', () => {
  const pres = makeMockPres();
  applyFeatureFlags(pres._slide, baseTheme, DEFAULT_DIMS);
  const extras = pres._calls.filter(c => c.type === 'shape');
  assert.strictEqual(extras.length, 0);
});

test('renderSection, renderTwoColumn, renderData, renderQuote are async functions', () => {
  assert.strictEqual(renderSection.constructor.name, 'AsyncFunction');
  assert.strictEqual(renderTwoColumn.constructor.name, 'AsyncFunction');
  assert.strictEqual(renderData.constructor.name, 'AsyncFunction');
  assert.strictEqual(renderQuote.constructor.name, 'AsyncFunction');
});

test('4-3 platform: buildTwoColumn does not overflow (w <= slide width)', () => {
  const pres = makeMockPres();
  const dims43 = { w: 10, h: 7.5 };
  buildTwoColumn(pres, {
    title: '对比', leftTitle: 'A', leftPoints: ['x'],
    rightTitle: 'B', rightPoints: ['y'],
  }, baseTheme, dims43);
  const rects = pres._calls.filter(c => c.type === 'shape' && c.shape === 'roundRect');
  for (const r of rects) {
    assert.ok(r.opts.x >= 0, `x should be non-negative, got ${r.opts.x}`);
    assert.ok(r.opts.x + r.opts.w <= dims43.w + 0.01, `card overflows slide: x=${r.opts.x}, w=${r.opts.w}, slideW=${dims43.w}`);
  }
});
