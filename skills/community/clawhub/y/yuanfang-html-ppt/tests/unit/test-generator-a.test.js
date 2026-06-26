const test = require('node:test');
const assert = require('node:assert');
const { renderCover, renderContent, renderSummary } = require('../../scripts/generator-a');

const theme = {
  bg: '#ffffff', text: '#111111', textSecondary: '#666666',
  accent: '#4f46e5', secondary: '#a855f7', bgAlt: '#f5f5f5',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif',
  sizeH1: 44, sizeH2: 28, sizeBase: 18, sizeSm: 12, sizeH3: 22,
  spacing: 6, space1: 6, space3: 18, rectRadius: 6,
};

function makeMockPres() {
  const calls = [];
  const slide = {
    background: null,
    addText: function(text, opts) { calls.push({ type: 'text', text, opts }); return this; },
    addShape: function(shape, opts) { calls.push({ type: 'shape', shape, opts }); return this; },
    addImage: function(opts) { calls.push({ type: 'image', opts }); return this; },
  };
  const pres = {
    addSlide: function() { calls.unshift({ type: 'slide' }); return slide; },
    _calls: calls,
    _slide: slide,
  };
  return pres;
}

test('renderContent uses theme.space1 for paraSpaceAfter (not hardcoded 8)', () => {
  const pres = makeMockPres();
  const slide = { title: 'X', points: ['A', 'B'] };
  renderContent(pres, slide, theme);
  const bodyCall = pres._calls.filter(c => c.type === 'text' && c.text === 'A\nB');
  assert.strictEqual(bodyCall.length, 1);
  assert.strictEqual(bodyCall[0].opts.paraSpaceAfter, theme.space1);
  // Also verify title y is within slide bounds (was off-screen before bugfix)
  const titleCall = pres._calls.filter(c => c.type === 'text' && c.text === 'X');
  assert.strictEqual(titleCall.length, 1);
  assert.ok(titleCall[0].opts.y < 1, `title y should be near top, got ${titleCall[0].opts.y}`);
});

test('renderCover sets background and adds title/subtitle/author text', () => {
  const pres = makeMockPres();
  const slide = { title: 'My Deck', subtitle: 'Subtitle here', author: 'Me', date: '2026-06-07' };
  renderCover(pres, slide, theme);
  const calls = pres._calls;
  assert.strictEqual(calls[0].type, 'slide');
  assert.strictEqual(pres._slide.background.color, '#ffffff');
  const texts = calls.filter(c => c.type === 'text').map(c => c.text);
  assert.ok(texts.includes('My Deck'));
  assert.ok(texts.includes('Subtitle here'));
  assert.ok(texts.some(t => t.includes('Me') && t.includes('2026-06-07')));
});

test('renderContent adds bulleted title + body points', () => {
  const pres = makeMockPres();
  const slide = { title: 'Goals', points: ['A', 'B', 'C'] };
  renderContent(pres, slide, theme);
  const calls = pres._calls;
  assert.strictEqual(calls[0].type, 'slide');
  const textCalls = calls.filter(c => c.type === 'text' && c.opts.fontSize > 12);
  assert.strictEqual(textCalls.length, 2);
  assert.strictEqual(textCalls[0].text, 'Goals');
  assert.strictEqual(textCalls[0].opts.bold, true);
  assert.strictEqual(textCalls[1].text, 'A\nB\nC');
  assert.ok(textCalls[1].opts.bullet !== false);
});

test('renderSummary adds title + points + closing text', () => {
  const pres = makeMockPres();
  const slide = { title: 'Next Steps', points: ['Do X', 'Do Y'] };
  renderSummary(pres, slide, theme);
  const calls = pres._calls;
  const textCalls = calls.filter(c => c.type === 'text');
  assert.ok(textCalls.length >= 3);
  assert.ok(textCalls.some(c => c.text === 'Next Steps'));
  assert.ok(textCalls.some(c => c.text === 'Do X\nDo Y'));
  assert.ok(textCalls.some(c => /谢|Thank|Thanks/i.test(c.text)));
});
