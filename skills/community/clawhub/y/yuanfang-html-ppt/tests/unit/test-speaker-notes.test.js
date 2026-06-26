const test = require('node:test');
const assert = require('node:assert');
const { renderCover, renderContent, renderSummary } = require('../../scripts/generator-a');
const { renderSection, renderTwoColumn, renderData, renderQuote } = require('../../scripts/generator-c');

const theme = {
  bg: '#ffffff', text: '#111111', textSecondary: '#666666',
  accent: '#4f46e5', secondary: '#64748b', bgAlt: '#f5f5f5',
  fontBody: 'system-ui', fontTitle: 'Georgia, serif',
  sizeH1: 60, sizeH2: 28, sizeBase: 18, sizeSm: 12, sizeH3: 20,
  spacing: 12, rectRadius: 8, shadow: 'none',
  accentLine: 'none', accentBlock: 'none', terminalBar: 'none',
  seal: 'none',
};

function makeMockPresWithNotes() {
  const notesCalls = [];
  const slide = {
    background: null,
    addText: function() { return this; },
    addShape: function() { return this; },
    addImage: function() { return this; },
    addNotes: function(notes) { notesCalls.push(notes); return this; },
  };
  return {
    addSlide: function() { return slide; },
    _notesCalls: notesCalls,
    _slide: slide,
  };
}

test('renderCover sets notes when slide.notes present', () => {
  const pres = makeMockPresWithNotes();
  renderCover(pres, { title: 'T', notes: 'speaker script for cover' }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['speaker script for cover']);
});

test('renderCover omits addNotes when slide.notes absent', () => {
  const pres = makeMockPresWithNotes();
  renderCover(pres, { title: 'T' }, theme);
  assert.strictEqual(pres._notesCalls.length, 0);
});

test('renderContent sets notes when present', () => {
  const pres = makeMockPresWithNotes();
  renderContent(pres, { title: 'T', points: ['a'], notes: 'walk through point 1' }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['walk through point 1']);
});

test('renderSummary sets notes', () => {
  const pres = makeMockPresWithNotes();
  renderSummary(pres, { title: 'T', notes: 'closing remarks' }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['closing remarks']);
});

test('renderSection sets notes', () => {
  const pres = makeMockPresWithNotes();
  renderSection(pres, { title: 'T', notes: 'transition to next chapter' }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['transition to next chapter']);
});

test('renderTwoColumn sets notes', () => {
  const pres = makeMockPresWithNotes();
  renderTwoColumn(pres, {
    title: 'T', leftTitle: 'A', leftPoints: ['x'], rightTitle: 'B', rightPoints: ['y'],
    notes: 'compare both columns',
  }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['compare both columns']);
});

test('renderData sets notes', () => {
  const pres = makeMockPresWithNotes();
  renderData(pres, {
    title: 'T', metrics: [{ label: 'L', value: 'V', change: 'C' }],
    notes: 'highlight MAU growth',
  }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['highlight MAU growth']);
});

test('renderQuote sets notes', () => {
  const pres = makeMockPresWithNotes();
  renderQuote(pres, {
    title: 'T', quote: 'q', attribution: 'a',
    notes: 'read quote slowly',
  }, theme);
  assert.deepStrictEqual(pres._notesCalls, ['read quote slowly']);
});
