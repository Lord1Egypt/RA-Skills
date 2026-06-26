const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const FIXTURES = path.join(__dirname, '..', 'fixtures');
const OUT_DIR = path.join(__dirname, '..', 'output');
const RENDER = path.resolve(__dirname, '..', '..', 'scripts', 'render.js');

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
  test(`renders ${layout} fixture to a valid 1-slide .pptx`, () => {
    const fixture = path.join(FIXTURES, `content-${layout}.json`);
    const out = path.join(OUT_DIR, `out-${layout}.pptx`);
    execFileSync('node', [RENDER, '--file', fixture, '--skip-confirm', '--output', out], { stdio: 'pipe' });
    assert.ok(fs.existsSync(out), `${out} should exist`);
    const size = fs.statSync(out).size;
    assert.ok(size > 5000, `${out} size ${size} should be > 5KB`);
    const head = fs.readFileSync(out).slice(0, 2).toString();
    assert.strictEqual(head, 'PK', `${out} should be a valid zip (PK header)`);
    const slideCount = countSlidesInPptx(out);
    assert.strictEqual(slideCount, 1, `${layout} should produce exactly 1 slide, got ${slideCount}`);
  });
}

test('multi-page fixture produces exactly 7 slides (verified via zip content)', () => {
  const fixture = path.join(FIXTURES, 'content-multipage.json');
  const out = path.join(OUT_DIR, 'out-multipage.pptx');
  execFileSync('node', [RENDER, '--file', fixture, '--skip-confirm', '--output', out], { stdio: 'pipe' });
  const slideCount = countSlidesInPptx(out);
  assert.strictEqual(slideCount, 7, `expected 7 slides, got ${slideCount}`);
  const size = fs.statSync(out).size;
  assert.ok(size > 50000, `multi-page pptx size ${size} should be > 50KB`);
});

test('hard gate rejects missing brand', () => {
  const tmpFile = path.join(OUT_DIR, 'no-brand.json');
  fs.writeFileSync(tmpFile, JSON.stringify({ theme: 'minimal-white', layout: 'content', title: 'Hi' }));
  let stderr = '';
  try {
    execFileSync('node', [RENDER, '--file', tmpFile, '--skip-confirm'], { stdio: ['pipe', 'pipe', 'pipe'] });
  } catch (err) {
    stderr = err.stderr ? err.stderr.toString() : '';
  }
  assert.ok(/缺少 brand 字段/.test(stderr), `expected brand error, got: ${stderr}`);
});

test('hard gate rejects unknown theme with helpful list of available themes', () => {
  const tmpFile = path.join(OUT_DIR, 'bad-theme.json');
  fs.writeFileSync(tmpFile, JSON.stringify({
    brand: 'minimal-white', theme: 'minimalist', layout: 'content', title: 'Hi',
  }));
  let stderr = '';
  try {
    execFileSync('node', [RENDER, '--file', tmpFile, '--skip-confirm'], { stdio: ['pipe', 'pipe', 'pipe'] });
  } catch (err) {
    stderr = (err.stderr || err.stdout || '').toString();
  }
  assert.ok(/主题 'minimalist' 不存在/.test(stderr), `expected theme error, got: ${stderr}`);
  assert.ok(/minimal-white/.test(stderr), `expected available themes listed, got: ${stderr}`);
});

test('--theme CLI flag overrides content.json theme', () => {
  const fixture = path.join(FIXTURES, 'content-content.json');
  const out = path.join(OUT_DIR, 'out-cli-theme-override.pptx');
  execFileSync('node', [RENDER, '--file', fixture, '--theme', 'tech-modern', '--skip-confirm', '--output', out], { stdio: 'pipe' });
  assert.ok(fs.existsSync(out));
  const slideCount = countSlidesInPptx(out);
  assert.strictEqual(slideCount, 1);
});

test('--help flag prints usage and exits 0', () => {
  let stdout = '';
  try {
    stdout = execFileSync('node', [RENDER, '--help'], { stdio: ['pipe', 'pipe', 'pipe'] }).toString();
  } catch (err) {
    stdout = (err.stdout || '').toString();
  }
  assert.ok(/用法/.test(stdout), `--help should print usage, got: ${stdout}`);
  assert.ok(/--file/.test(stdout));
  assert.ok(/--theme/.test(stdout));
});

test('--brand-spec applies brand color override', () => {
  const fixture = path.join(FIXTURES, 'content-content.json');
  const brandSpec = path.join(OUT_DIR, 'brand-spec.json');
  fs.writeFileSync(brandSpec, JSON.stringify({ primary: '#ff5500' }));
  const out = path.join(OUT_DIR, 'out-brand-override.pptx');
  execFileSync('node', [RENDER, '--file', fixture, '--brand-spec', brandSpec, '--skip-confirm', '--output', out], { stdio: 'pipe' });
  assert.ok(fs.existsSync(out));
  const slideCount = countSlidesInPptx(out);
  assert.strictEqual(slideCount, 1);
});

test('4-3 platform renders all text boxes within slide width', () => {
  const fixture = path.join(FIXTURES, 'content-content.json');
  const out = path.join(OUT_DIR, 'out-4-3.pptx');
  execFileSync('node', [RENDER, '--file', fixture, '--platforms', '4-3', '--skip-confirm', '--output', out], { stdio: 'pipe' });
  assert.ok(fs.existsSync(out));
  assert.ok(fs.statSync(out).size > 5000);
});
