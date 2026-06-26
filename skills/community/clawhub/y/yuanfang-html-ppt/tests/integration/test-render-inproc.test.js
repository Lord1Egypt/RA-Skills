const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { render } = require('../../scripts/render');

const FIXTURES = path.join(__dirname, '..', 'fixtures');
const OUT_DIR = path.join(__dirname, '..', 'output');

test.before(() => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
});

function countSlidesInPptx(filePath) {
  const buf = fs.readFileSync(filePath);
  const text = buf.toString('binary');
  const matches = text.match(/ppt\/slides\/slide\d+\.xml/g) || [];
  return new Set(matches).size;
}

for (const layout of ['cover', 'section', 'content', 'two-column', 'data', 'quote', 'summary']) {
  test(`renders ${layout} fixture to a valid 1-slide .pptx (in-process)`, async () => {
    const fixture = path.join(FIXTURES, `content-${layout}.json`);
    const out = path.join(OUT_DIR, `inproc-${layout}.pptx`);
    await render({ file: fixture, 'skip-confirm': true, output: out });
    assert.ok(fs.existsSync(out), `${out} should exist`);
    const size = fs.statSync(out).size;
    assert.ok(size > 5000, `${out} size ${size} should be > 5KB`);
    const head = fs.readFileSync(out).slice(0, 2).toString();
    assert.strictEqual(head, 'PK');
    const slideCount = countSlidesInPptx(out);
    assert.strictEqual(slideCount, 1, `${layout} should produce exactly 1 slide, got ${slideCount}`);
  });
}

test('in-process multi-page fixture produces exactly 7 slides', async () => {
  const fixture = path.join(FIXTURES, 'content-multipage.json');
  const out = path.join(OUT_DIR, 'inproc-multipage.pptx');
  await render({ file: fixture, 'skip-confirm': true, output: out });
  const slideCount = countSlidesInPptx(out);
  assert.strictEqual(slideCount, 7);
});

test('in-process hard gate rejects missing brand (Error thrown)', async () => {
  const tmpFile = path.join(OUT_DIR, 'inproc-no-brand.json');
  fs.writeFileSync(tmpFile, JSON.stringify({ theme: 'minimal-white', layout: 'content', title: 'Hi' }));
  await assert.rejects(
    () => render({ file: tmpFile, 'skip-confirm': true, output: '/tmp/x.pptx' }),
    /缺少 brand 字段/
  );
});

test('in-process hard gate rejects unknown theme (Error thrown)', async () => {
  const tmpFile = path.join(OUT_DIR, 'inproc-bad-theme.json');
  fs.writeFileSync(tmpFile, JSON.stringify({
    brand: 'minimal-white', theme: 'minimalist', layout: 'content', title: 'Hi',
  }));
  await assert.rejects(
    () => render({ file: tmpFile, 'skip-confirm': true, output: '/tmp/x.pptx' }),
    /主题 'minimalist' 不存在/
  );
});
