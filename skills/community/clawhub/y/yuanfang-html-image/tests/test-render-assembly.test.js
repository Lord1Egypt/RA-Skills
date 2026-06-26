const test = require('node:test');
const assert = require('node:assert');
const { assembleHTML } = require('../scripts/render');

test('assembles full HTML with data-theme attribute', () => {
  const result = assembleHTML({
    themeName: 'minimal-white',
    themeCSS: '[data-theme="minimal-white"] { --bg: #FFF; }',
    baseCSS: ':root { --bg: #FFF; --text: #000; }',
    layoutHTML: '<div class="cover">{{TITLE}}</div>',
    content: { title: 'Hello' },
  });
  assert.ok(result.includes('data-theme="minimal-white"'));
  assert.ok(result.includes('--bg: #FFF'));
  assert.ok(result.includes('Hello'));
});

test('sets viewport meta with width/height', () => {
  const result = assembleHTML({
    themeName: 'minimal-white',
    themeCSS: '',
    baseCSS: ':root {}',
    layoutHTML: '<div></div>',
    content: {},
    width: 1080,
    height: 1440,
  });
  assert.ok(result.includes('width=1080'));
  assert.ok(result.includes('height=1440'));
});

test('brand: with image renders <img>', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{BRAND}}',
    content: { brandImage: 'data:image/png;base64,abc', brand: 'X' },
  });
  assert.ok(result.includes('<img'));
  assert.ok(result.includes('class="cover__brand-img"'));
});

test('brand: without image renders nothing (no text fallback)', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{BRAND}}',
    content: { brand: 'ShouldNotRender' },
  });
  assert.ok(!result.includes('ShouldNotRender'));
  assert.ok(!result.includes('<img'));
});

test('brand: empty content renders nothing', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{BRAND}}',
    content: {},
  });
  assert.ok(!result.includes('<img'));
});

test('QR: data:image URL passed through', () => {
  const { isImageRef } = require('../scripts/render');
  assert.strictEqual(isImageRef('data:image/png;base64,abc'), true);
  assert.strictEqual(isImageRef('https://x.com/qr.png'), true);
  assert.strictEqual(isImageRef('https://yuanfang.skills'), false);
  assert.strictEqual(isImageRef('https://x.com'), false);
});

test('QR: URL string auto-generates data URL', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{QR}}',
    content: { qr: 'https://yuanfang.skills' },
  });
  assert.ok(result.includes('data:image/svg+xml;base64,'));
  assert.ok(result.includes('class="cover__qr-img"'));
});

test('QR: pre-generated data URL used as-is', () => {
  const pre = 'data:image/png;base64,PRE_GENERATED';
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{QR}}',
    content: { qr: pre },
  });
  assert.ok(result.includes(pre));
});

test('QR: image URL (.png/.jpg) used as-is', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{QR}}',
    content: { qr: 'https://x.com/qr.png' },
  });
  assert.ok(result.includes('https://x.com/qr.png'));
  assert.ok(!result.includes('data:image/png;base64,'));
});

test('QR: empty renders nothing', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '', layoutHTML: '{{QR}}',
    content: {},
  });
  assert.ok(!result.includes('cover__qr-img'));
});

test('XSS: title is escaped', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '<h1>{{TITLE}}</h1>',
    content: { title: '<script>alert(1)</script>' },
  });
  assert.ok(!result.includes('<script>alert(1)</script>'));
  assert.ok(result.includes('&lt;script&gt;'));
});

test('XSS: body is escaped', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '<p>{{CONTENT}}</p>',
    content: { body: '5 < 10 & "x"' },
  });
  assert.ok(result.includes('5 &lt; 10 &amp; &quot;x&quot;'));
});

test('XSS: points are escaped', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '<ul>{{POINTS_HTML}}</ul>',
    content: { points: ['<b>bold</b>', 'a&b'] },
  });
  assert.ok(!result.includes('<b>bold</b>'));
  assert.ok(result.includes('&lt;b&gt;bold&lt;/b&gt;'));
  assert.ok(result.includes('a&amp;b'));
});

test('XSS: badge and seal are escaped', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '<span>{{BADGE}}</span>',
    content: { badge: '<img onerror=alert(1)>' },
  });
  assert.ok(!result.includes('<img onerror=alert(1)>'));
  assert.ok(result.includes('&lt;img'));
});

test('direction detection: Chinese defaults to LTR/zh-CN', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '{{TITLE}}', content: { title: '中文测试', body: '正文' },
  });
  assert.ok(result.includes('lang="zh-CN"'));
  assert.ok(result.includes('dir="ltr"'));
});

test('direction detection: Arabic flips to RTL', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '{{TITLE}}', content: { title: 'تجربة', body: 'محتوى' },
  });
  assert.ok(result.includes('dir="rtl"'));
});

test('direction detection: Hebrew flips to RTL', () => {
  const result = assembleHTML({
    themeName: 'minimal-white', themeCSS: '', baseCSS: '',
    layoutHTML: '{{TITLE}}', content: { title: 'שלום', body: 'בדיקה' },
  });
  assert.ok(result.includes('dir="rtl"'));
});
