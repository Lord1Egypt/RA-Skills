const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const os = require('os');
const {
  extractDomain,
  extractBrandFromHtml,
  resolveImageAsDataUrl,
  dataUrlToBuffer,
  rgbToHex,
  extractDominantColor,
  extractBrandPalette,
  readCache,
  writeCache,
  isExpired,
  cachePath,
  TTL_DAYS,
  parseArgs,
} = require('../scripts/extract-brand.js');

test('extractDomain: simple hostname', () => {
  assert.strictEqual(extractDomain('https://example.com/x'), 'example.com');
});

test('extractDomain: strips www', () => {
  assert.strictEqual(extractDomain('https://www.example.com/x'), 'example.com');
});

test('extractDomain: strips m.', () => {
  assert.strictEqual(extractDomain('https://m.example.com/x'), 'example.com');
});

test('extractDomain: lowercases', () => {
  assert.strictEqual(extractDomain('https://Example.COM/x'), 'example.com');
});

test('extractDomain: invalid URL returns null', () => {
  assert.strictEqual(extractDomain('not a url'), null);
});

test('extractDomain: sub.example.com preserved when needed', () => {
  assert.strictEqual(extractDomain('https://blog.example.com/x'), 'blog.example.com');
});

test('extractBrandFromHtml: og + theme-color + favicon', () => {
  const html = `
    <html>
    <head>
      <meta property="og:site_name" content="Acme Corp">
      <meta property="og:image" content="https://acme.com/logo.png">
      <meta name="theme-color" content="#FF5733">
    </head>
    </html>`;
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.name, 'Acme Corp');
  assert.strictEqual(b.logoUrl, 'https://acme.com/logo.png');
  assert.strictEqual(b.colors.primary, '#FF5733');
  assert.strictEqual(b.domain, 'acme.com');
});

test('extractBrandFromHtml: relative logo URL is resolved', () => {
  const html = '<html><head><link rel="icon" href="/favicon.ico"></head></html>';
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.logoUrl, 'https://acme.com/favicon.ico');
});

test('extractBrandFromHtml: name falls back to domain', () => {
  const html = '<html><head></head></html>';
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.name, 'acme.com');
});

test('extractBrandFromHtml: theme-color missing → null', () => {
  const html = '<html><head></head></html>';
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.colors.primary, null);
});

test('writeCache + readCache roundtrip', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'brand-'));
  const spec = {
    domain: 'test.com',
    extractedAt: new Date().toISOString(),
    name: 'Test',
    logo: null,
    logoUrl: null,
    colors: { primary: null },
  };
  const p = path.join(tmp, 'test.com.json');
  fs.writeFileSync(p, JSON.stringify(spec));
  const loaded = JSON.parse(fs.readFileSync(p, 'utf8'));
  assert.strictEqual(loaded.name, 'Test');
  fs.rmSync(tmp, { recursive: true });
});

test('isExpired: fresh spec not expired', () => {
  const spec = { extractedAt: new Date().toISOString() };
  assert.strictEqual(isExpired(spec), false);
});

test('isExpired: 8-day-old spec is expired', () => {
  const old = new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString();
  assert.strictEqual(isExpired({ extractedAt: old }), true);
});

test('isExpired: missing extractedAt is expired', () => {
  assert.strictEqual(isExpired({}), true);
});

test('parseArgs: url only', () => {
  assert.deepStrictEqual(parseArgs(['node', 'extract-brand.js', 'https://x.com']), {
    url: 'https://x.com', forceRefresh: false,
  });
});

test('parseArgs: with --refresh-brand', () => {
  const r = parseArgs(['node', 'extract-brand.js', 'https://x.com', '--refresh-brand']);
  assert.strictEqual(r.forceRefresh, true);
});

test('parseArgs: no url throws', () => {
  assert.throws(() => parseArgs(['node', 'extract-brand.js']), /Usage/);
});

test('TTL_DAYS default is 7', () => {
  assert.strictEqual(TTL_DAYS, 7);
});

test('rgbToHex: basic colors', () => {
  assert.strictEqual(rgbToHex(255, 87, 51), '#FF5733');
  assert.strictEqual(rgbToHex(0, 0, 0), '#000000');
  assert.strictEqual(rgbToHex(255, 255, 255), '#FFFFFF');
});

test('dataUrlToBuffer: parses data URL', () => {
  const png = Buffer.from([0x89, 0x50, 0x4E, 0x47]).toString('base64');
  const url = `data:image/png;base64,${png}`;
  const r = dataUrlToBuffer(url);
  assert.strictEqual(r.mime, 'image/png');
  assert.strictEqual(r.buffer.toString('hex'), '89504e47');
});

test('dataUrlToBuffer: invalid returns null', () => {
  assert.strictEqual(dataUrlToBuffer('not a data url'), null);
  assert.strictEqual(dataUrlToBuffer(''), null);
});

test('extractDominantColor: red PNG returns reddish hex', async () => {
  const sharp = require('sharp');
  const buf = await sharp({
    create: { width: 32, height: 32, channels: 3, background: { r: 220, g: 38, b: 38 } }
  }).png().toBuffer();
  const dataUrl = `data:image/png;base64,${buf.toString('base64')}`;
  const hex = await extractDominantColor(dataUrl);
  assert.ok(hex);
  assert.match(hex, /^#[0-9a-fA-F]{6}$/);
  // node-vibrant quantizes; accept red channel within ±10
  const r = parseInt(hex.slice(1, 3), 16);
  assert.ok(Math.abs(r - 0xdc) <= 10, `red channel ${r.toString(16)} not near dc`);
});

test('extractDominantColor: null for empty input', async () => {
  assert.strictEqual(await extractDominantColor(null), null);
  assert.strictEqual(await extractDominantColor(''), null);
  assert.strictEqual(await extractDominantColor('invalid'), null);
});

test('extractBrandPalette: returns 6-swatch palette for non-trivial image', async () => {
  const sharp = require('sharp');
  const blue = await sharp({ create: { width: 50, height: 100, channels: 3, background: { r: 30, g: 80, b: 200 } } }).png().toBuffer();
  const yellow = await sharp({ create: { width: 50, height: 100, channels: 3, background: { r: 255, g: 200, b: 0 } } }).png().toBuffer();
  const mixed = await sharp({ create: { width: 100, height: 100, channels: 3, background: { r: 255, g: 255, b: 255 } } })
    .composite([{ input: blue, top: 0, left: 0 }, { input: yellow, top: 0, left: 50 }])
    .png().toBuffer();
  const dataUrl = `data:image/png;base64,${mixed.toString('base64')}`;
  const palette = await extractBrandPalette(dataUrl);
  assert.ok(palette, 'palette should not be null');
  assert.ok(palette.Vibrant, 'should have Vibrant swatch');
  assert.match(palette.Vibrant.hex, /^#[0-9a-fA-F]{6}$/);
  // Vibrant should be the yellow stripe (more saturated than blue+white avg)
  assert.ok(
    palette.Vibrant.hex === '#fccc04' || palette.Vibrant.hex.toLowerCase() === '#fccc04',
    `expected yellow Vibrant, got ${palette.Vibrant.hex}`
  );
});

test('extractBrandPalette: null for empty input', async () => {
  assert.strictEqual(await extractBrandPalette(null), null);
  assert.strictEqual(await extractBrandPalette(''), null);
});

test('extractBrandFromHtml: dark mode theme-color captured', () => {
  const html = `
    <html>
    <head>
      <meta name="theme-color" content="#FAFAFA" media="(prefers-color-scheme: light)">
      <meta name="theme-color" content="#0A0A0A" media="(prefers-color-scheme: dark)">
    </head>
    </html>`;
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.colors.primary, '#FAFAFA');
  assert.strictEqual(b.colors.primaryDark, '#0A0A0A');
});

test('extractBrandFromHtml: no theme-color → null', () => {
  const html = '<html><head></head></html>';
  const b = extractBrandFromHtml(html, 'https://acme.com/');
  assert.strictEqual(b.colors.primary, null);
  assert.strictEqual(b.colors.primaryDark, null);
});
