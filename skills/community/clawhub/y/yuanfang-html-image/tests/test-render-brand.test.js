const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { findBrandSpec, buildBrandOverrideCss, mergeBrandSpec } = require('../scripts/render');

test('buildBrandOverrideCss: no spec returns empty', () => {
  assert.strictEqual(buildBrandOverrideCss(null, 'minimal-white'), '');
});

test('buildBrandOverrideCss: no colors returns empty', () => {
  const spec = { name: 'X', domain: 'x.com' };
  assert.strictEqual(buildBrandOverrideCss(spec, 'minimal-white'), '');
});

test('buildBrandOverrideCss: empty colors object returns empty', () => {
  const spec = { colors: {} };
  assert.strictEqual(buildBrandOverrideCss(spec, 'minimal-white'), '');
});

test('buildBrandOverrideCss: single color (primary only)', () => {
  const spec = { colors: { primary: '#FF5733' } };
  const css = buildBrandOverrideCss(spec, 'minimal-white');
  assert.ok(css.includes('[data-theme="minimal-white"]'));
  assert.ok(css.includes('--accent: #FF5733'));
  assert.ok(!css.includes('--bg:'));
  assert.ok(!css.includes('--secondary:'));
});

test('buildBrandOverrideCss: all three colors', () => {
  const spec = { colors: { primary: '#FF5733', background: '#FAFAFA', secondary: '#1F2937' } };
  const css = buildBrandOverrideCss(spec, 'dark-gold');
  assert.ok(css.includes('--accent: #FF5733'));
  assert.ok(css.includes('--bg: #FAFAFA'));
  assert.ok(css.includes('--secondary: #1F2937'));
  assert.ok(css.includes('[data-theme="dark-gold"]'));
});

test('buildBrandOverrideCss: skips null colors but keeps defined', () => {
  const spec = { colors: { primary: '#FF5733', background: null, secondary: '#1F2937' } };
  const css = buildBrandOverrideCss(spec, 'minimal-white');
  assert.ok(css.includes('--accent: #FF5733'));
  assert.ok(!css.includes('--bg:'));
  assert.ok(css.includes('--secondary: #1F2937'));
});

test('buildBrandOverrideCss: ignores unknown color keys', () => {
  const spec = { colors: { primary: '#000', tertiary: '#FFF' } };
  const css = buildBrandOverrideCss(spec, 'minimal-white');
  assert.ok(!css.includes('tertiary'));
});

test('mergeBrandSpec: fills missing brand from spec', () => {
  const content = { title: 'X' };
  const spec = { name: 'MyBrand', domain: 'x.com' };
  const out = mergeBrandSpec(content, spec);
  assert.strictEqual(out.brand, 'MyBrand');
  assert.strictEqual(out.brandDomain, 'x.com');
});

test('mergeBrandSpec: keeps content brand when present', () => {
  const content = { brand: 'Override', brandImage: 'data:...' };
  const spec = { name: 'MyBrand', logo: 'data:...' };
  const out = mergeBrandSpec(content, spec);
  assert.strictEqual(out.brand, 'Override');
  assert.strictEqual(out.brandImage, 'data:...');
});

test('mergeBrandSpec: no spec is passthrough', () => {
  const content = { brand: 'X' };
  assert.deepStrictEqual(mergeBrandSpec(content, null), { brand: 'X' });
});

test('findBrandSpec: --brand-spec points to a JSON file', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bs-'));
  const specPath = path.join(tmp, 'mysite.com.json');
  fs.writeFileSync(specPath, JSON.stringify({ domain: 'mysite.com', name: 'MySite', colors: { primary: '#000' } }));
  const spec = findBrandSpec({ brand: 'MySite' }, { 'brand-spec': specPath });
  assert.strictEqual(spec.domain, 'mysite.com');
  assert.strictEqual(spec.colors.primary, '#000');
  fs.rmSync(tmp, { recursive: true });
});

test('findBrandSpec: --brand-spec file missing falls through to scan', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bs-'));
  const origCwd = process.cwd();
  process.chdir(tmp);
  try {
    const spec = findBrandSpec({}, { 'brand-spec': '/nonexistent/file.json' });
    assert.strictEqual(spec, null);
  } finally {
    process.chdir(origCwd);
    fs.rmSync(tmp, { recursive: true });
  }
});

test('findBrandSpec: scans .yuanfang/brand-specs/ in cwd', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bs-'));
  const brandDir = path.join(tmp, '.yuanfang', 'brand-specs');
  fs.mkdirSync(brandDir, { recursive: true });
  fs.writeFileSync(path.join(brandDir, 'onlyone.com.json'), JSON.stringify({ domain: 'onlyone.com', name: 'Only' }));
  const origCwd = process.cwd();
  process.chdir(tmp);
  try {
    const spec = findBrandSpec({ brand: 'Only' }, {});
    assert.strictEqual(spec.domain, 'onlyone.com');
  } finally {
    process.chdir(origCwd);
    fs.rmSync(tmp, { recursive: true });
  }
});

test('findBrandSpec: multiple specs, no brand match returns first', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bs-'));
  const brandDir = path.join(tmp, '.yuanfang', 'brand-specs');
  fs.mkdirSync(brandDir, { recursive: true });
  fs.writeFileSync(path.join(brandDir, 'a.com.json'), JSON.stringify({ domain: 'a.com', name: 'A' }));
  fs.writeFileSync(path.join(brandDir, 'b.com.json'), JSON.stringify({ domain: 'b.com', name: 'B' }));
  const origCwd = process.cwd();
  process.chdir(tmp);
  try {
    const spec = findBrandSpec({ brand: 'Z' }, {});
    assert.ok(['a.com', 'b.com'].includes(spec.domain));
  } finally {
    process.chdir(origCwd);
    fs.rmSync(tmp, { recursive: true });
  }
});

test('findBrandSpec: no .yuanfang dir returns null', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bs-'));
  const origCwd = process.cwd();
  process.chdir(tmp);
  try {
    const spec = findBrandSpec({ brand: 'X' }, {});
    assert.strictEqual(spec, null);
  } finally {
    process.chdir(origCwd);
    fs.rmSync(tmp, { recursive: true });
  }
});
