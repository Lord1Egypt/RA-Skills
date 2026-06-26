const test = require('node:test');
const assert = require('node:assert');
const { renderCover, renderContent } = require('../../scripts/generator-a');

const theme = {
  bg: '#ffffff', text: '#111111', textSecondary: '#666666',
  accent: '#4f46e5', secondary: '#64748b', bgAlt: '#f5f5f5',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif',
  sizeH1: 60, sizeH2: 28, sizeBase: 18, sizeSm: 12, sizeH3: 20,
  spacing: 12, rectRadius: 8,
};

function makeMockPres() {
  const calls = [];
  let counter = 0;
  const slide = {
    _slideNum: ++counter,
    addText: function(text, opts) { calls.push({ type: 'text', text, opts }); return this; },
    addShape: function() { return this; },
    addImage: function() { return this; },
    addNotes: function() { return this; },
  };
  return { addSlide: () => slide, _calls: calls };
}

test('addSlideFooter emits slide number text at bottom-right', () => {
  const pres = makeMockPres();
  renderCover(pres, { title: 'T' }, theme);
  const numCalls = pres._calls.filter(c => c.text === '1' && c.opts.fontSize <= 12);
  assert.strictEqual(numCalls.length, 1);
  assert.strictEqual(numCalls[0].opts.align, 'right');
});

test('addSlideFooter uses slide._slideNum as text', () => {
  const pres = makeMockPres();
  renderContent(pres, { title: 'T', points: ['a'] }, theme);
  const numCalls = pres._calls.filter(c => c.text === '1');
  assert.ok(numCalls.length >= 1);
});

test('addSlideFooter can be disabled per-slide via showFooter: false', () => {
  const { addSlideFooter } = require('../../scripts/slide-footer');
  const pres = makeMockPres();
  const slide = pres.addSlide();
  addSlideFooter(slide, theme, { w: 13.333, h: 7.5 }, { showFooter: false });
  assert.strictEqual(pres._calls.length, 0);
});

test('all 7 generators emit slide footer (default on)', async () => {
  const { renderSummary } = require('../../scripts/generator-a');
  const { renderSection, renderTwoColumn, renderData, renderQuote } = require('../../scripts/generator-c');
  const layouts = [
    ['cover', pres => renderCover(pres, { title: 'T' }, theme)],
    ['content', pres => renderContent(pres, { title: 'T', points: ['a'] }, theme)],
    ['summary', pres => renderSummary(pres, { title: 'T', points: ['a'] }, theme)],
    ['section', async pres => await renderSection(pres, { title: 'T' }, theme)],
    ['two-column', async pres => await renderTwoColumn(pres, { title: 'T', leftTitle: 'A', leftPoints: ['x'], rightTitle: 'B', rightPoints: ['y'] }, theme)],
    ['data', async pres => await renderData(pres, { title: 'T', metrics: [{ label: 'L', value: 'V', change: 'C' }] }, theme)],
    ['quote', async pres => await renderQuote(pres, { title: 'T', quote: 'q', attribution: 'a' }, theme)],
  ];
  for (const [name, fn] of layouts) {
    const pres = makeMockPres();
    await fn(pres);
    const numCalls = pres._calls.filter(c => c.text === '1' && c.opts.fontSize <= 12);
    assert.strictEqual(numCalls.length, 1, `${name} should emit exactly 1 slide footer, got ${numCalls.length}`);
  }
});
