const test = require('node:test');
const assert = require('node:assert');
const { parseSlides } = require('../../scripts/parse-slides');

test('single-page shorthand wraps top-level fields into slides array', () => {
  const content = {
    brand: 'minimalist',
    theme: 'minimalist',
    layout: 'content',
    title: 'Hello',
    body: 'World',
  };
  const result = parseSlides(content);
  assert.ok(Array.isArray(result.slides), 'slides must be an array');
  assert.strictEqual(result.slides.length, 1);
  assert.strictEqual(result.slides[0].layout, 'content');
  assert.strictEqual(result.slides[0].title, 'Hello');
  assert.strictEqual(result.slides[0].body, 'World');
});

test('multi-page content passes through slides array as-is', () => {
  const content = {
    brand: 'minimalist',
    theme: 'minimalist',
    slides: [
      { layout: 'cover', title: 'A' },
      { layout: 'content', title: 'B', points: ['x', 'y'] },
    ],
  };
  const result = parseSlides(content);
  assert.strictEqual(result.slides.length, 2);
  assert.strictEqual(result.slides[1].points.length, 2);
});

test('throws when neither layout nor slides is provided', () => {
  assert.throws(() => parseSlides({ brand: 'x', theme: 'x' }), /缺少 slides 数组或单页 layout/);
});

test('data layout without metrics throws clear error', () => {
  assert.throws(
    () => parseSlides({ brand: 'x', theme: 'x', layout: 'data', title: 'T' }),
    /缺少必填字段 'metrics'/
  );
});

test('data layout with empty metrics array throws', () => {
  assert.throws(
    () => parseSlides({ brand: 'x', theme: 'x', layout: 'data', title: 'T', metrics: [] }),
    /缺少必填字段 'metrics'/
  );
});

test('two-column layout without leftPoints throws', () => {
  assert.throws(
    () => parseSlides({
      brand: 'x', theme: 'x', layout: 'two-column', title: 'T',
      leftTitle: 'A', rightPoints: ['x'],
    }),
    /缺少必填字段 'leftPoints'/
  );
});

test('quote layout without attribution throws', () => {
  assert.throws(
    () => parseSlides({
      brand: 'x', theme: 'x', layout: 'quote', title: 'T',
      quote: 'hello',
    }),
    /缺少必填字段 'attribution'/
  );
});

test('cover layout does not require additional fields beyond title', () => {
  const result = parseSlides({
    brand: 'x', theme: 'x', layout: 'cover', title: 'Hi',
  });
  assert.strictEqual(result.slides.length, 1);
});

test('content layout does not require points (body fallback allowed)', () => {
  const result = parseSlides({
    brand: 'x', theme: 'x', layout: 'content', title: 'Hi', body: 'text',
  });
  assert.strictEqual(result.slides.length, 1);
});

test('parseSlides exposes logo and company at top level', () => {
  const result = parseSlides({
    brand: 'x', theme: 'x', logo: '/tmp/logo.png', company: 'Acme',
    layout: 'cover', title: 'Hi',
  });
  assert.strictEqual(result.logo, '/tmp/logo.png');
  assert.strictEqual(result.company, 'Acme');
});

test('single-page shorthand preserves notes and background fields', () => {
  const result = parseSlides({
    brand: 'x', theme: 'x', layout: 'content', title: 'Hi',
    notes: 'speaker script', background: '/tmp/bg.png',
  });
  assert.strictEqual(result.slides[0].notes, 'speaker script');
  assert.strictEqual(result.slides[0].background, '/tmp/bg.png');
});

test('multi-page slides preserve notes field on each slide', () => {
  const result = parseSlides({
    brand: 'x', theme: 'x',
    slides: [
      { layout: 'cover', title: 'A', notes: 'note A' },
      { layout: 'content', title: 'B', points: ['x'], notes: 'note B' },
    ],
  });
  assert.strictEqual(result.slides[0].notes, 'note A');
  assert.strictEqual(result.slides[1].notes, 'note B');
});
