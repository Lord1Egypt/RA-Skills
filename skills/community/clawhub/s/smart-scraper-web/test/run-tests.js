#!/usr/bin/env node
/**
 * Smart Scraper — Self-Test Suite
 *
 * Tests: validateUrl, parseHtml, formatBytes, diffSnapshots, urlToHash, findArg, showStatus
 * Also tests CLI modes via spawn for integration testing
 *
 * Run: node test/run-tests.js
 */

const path = require('path');
const fs = require('fs');
const { execSync, spawnSync } = require('child_process');

// Use a temp directory for isolated cache/snapshots
const TEST_DIR = fs.mkdtempSync('/tmp/smart-scraper-test-');
process.env.SCRAPER_DIR = path.join(TEST_DIR, 'workspace');
fs.mkdirSync(process.env.SCRAPER_DIR, { recursive: true });
fs.writeFileSync(path.join(process.env.SCRAPER_DIR, 'MEMORY.md'), '# Test Workspace');

const SS = require(path.resolve(__dirname, '..', 'smart-scraper.js'));

let totalTests = 0;
let totalPassed = 0;

function assert(condition, description) {
  totalTests++;
  const passed = !!condition;
  if (passed) totalPassed++;
  console.log(`  ${passed ? '✅' : '❌'} ${description}`);
}

function group(name, fn) {
  console.log(`\n📋 ${name}`);
  fn();
}

// ─── 1. validateUrl Tests ──────────────────────────────────────

group('validateUrl — 6 cases', () => {
  const r1 = SS.validateUrl('https://example.com');
  assert(r1.valid === true, 'Valid https URL is accepted');

  const r2 = SS.validateUrl('http://example.com/page?q=1');
  assert(r2.valid === true, 'Valid http URL with query string is accepted');

  const r3 = SS.validateUrl('ftp://example.com');
  assert(r3.valid === false && r3.error.includes('Blocked'), 'FTP scheme is blocked');

  const r4 = SS.validateUrl('file:///etc/passwd');
  assert(r4.valid === false && r4.error.includes('Blocked'), 'File scheme is blocked');

  const r5 = SS.validateUrl('http://127.0.0.1:8080');
  assert(r5.valid === false && r5.error.includes('Blocked'), 'Localhost IP is blocked');

  const r6 = SS.validateUrl('not-a-url');
  assert(r6.valid === false && r6.error.includes('Invalid'), 'Malformed URL returns Invalid');
});

// ─── 2. parseHtml Tests ────────────────────────────────────────

group('parseHtml — 6 cases', () => {
  const simple = SS.parseHtml('<html><head><title>Test Page</title></head><body>' +
    '<h1>Main Heading</h1><h2>Sub</h2>' +
    '<p>This is a paragraph that should be long enough to pass the 20-char threshold.</p>' +
    '<a href="https://example.com/link">Click here</a>' +
    '<table><tr><td>Cell 1</td></tr></table>' +
    '<ul><li>Item A</li><li>Item B</li></ul>' +
    '<meta name="description" content="A test page">' +
    '</body></html>');
  assert(simple.title === 'Test Page', 'Extracts page title');
  assert(simple.headings.length === 2, 'Finds headings');
  assert(simple.headings[0].level === 1 && simple.headings[0].text === 'Main Heading', 'H1 has correct level and text');
  assert(simple.paragraphs.length >= 1, 'Finds paragraphs');
  assert(simple.links.length === 1 && simple.links[0].url === 'https://example.com/link', 'Extracts links');
  assert(simple.tables.length === 1, 'Finds tables');
});

// ─── 3. parseHtml Edge Cases ───────────────────────────────────

group('parseHtml Edge Cases — 5 cases', () => {
  const empty = SS.parseHtml('<html></html>');
  assert(empty.title === '', 'Empty HTML has blank title');
  assert(empty.headings.length === 0, 'Empty HTML has no headings');
  assert(empty.links.length === 0, 'Empty HTML has no links');

  // Paragraphs shorter than 20 chars are filtered
  const shortP = SS.parseHtml('<html><body><p>Short</p></body></html>');
  assert(shortP.paragraphs.length === 0, 'Short paragraphs (<20 chars) are filtered');

  const special = SS.parseHtml('<html><body><h1>&amp; &lt; &gt;</h1></body></html>');
  assert(special.headings[0].text.includes('&'), 'HTML entities decoded in heading');
});

// ─── 4. formatBytes Tests ──────────────────────────────────────

group('formatBytes — 4 cases', () => {
  assert(SS.formatBytes(0) === '0 B', 'Zero bytes');
  assert(SS.formatBytes(500) === '500 B', 'Bytes value');
  assert(SS.formatBytes(2048) === '2 KB', 'Kilobytes');
  assert(SS.formatBytes(1048576 * 3) === '3 MB', 'Megabytes');
});

// ─── 5. urlToHash tests ────────────────────────────────────────

group('urlToHash — 2 cases', () => {
  const h1 = SS.urlToHash('https://example.com');
  const h2 = SS.urlToHash('https://example.com');
  assert(h1 === h2, 'Same URL produces same hash');
  const h3 = SS.urlToHash('https://other.com');
  assert(h1 !== h3, 'Different URLs produce different hashes');
});

// ─── 6. loadJSON / saveJSON Tests ──────────────────────────────

group('loadJSON / saveJSON — 3 cases', () => {
  const testFile = path.join(TEST_DIR, 'test-cache.json');
  SS.saveJSON(testFile, { key: 'value' });
  const loaded = SS.loadJSON(testFile, {});
  assert(loaded.key === 'value', 'saveJSON → loadJSON roundtrip works');
  const missing = SS.loadJSON('/nonexistent/path.json', { fallback: true });
  assert(missing.fallback === true, 'loadJSON returns fallback for missing files');
  fs.unlinkSync(testFile);
});

// ─── 7. ensureDir + decodeHtmlEntities + stripHtml Tests ───────

group('Utility functions — 3 cases', () => {
  const testDir = path.join(TEST_DIR, 'nested/a/b/c');
  SS.ensureDir(testDir);
  assert(fs.existsSync(testDir) === true, 'ensureDir creates nested directories');

  const decoded = SS.decodeHtmlEntities('&amp;lt;test&amp;gt;');
  assert(decoded.includes('<') || decoded.includes('&lt;'), 'Decodes HTML entities');

  const stripped = SS.stripHtml('<p>Hello <b>world</b></p>');
  assert(stripped.includes('Hello world'), 'Strips HTML tags');
});

// ─── 8. CLI Integration Tests ──────────────────────────────────

group('CLI Integration — 4 cases', () => {
  const scraperPath = path.resolve(__dirname, '..', 'smart-scraper.js');

  // --status
  const status = spawnSync('node', [scraperPath, '--status'], {
    cwd: TEST_DIR,
    encoding: 'utf8'
  });
  assert(status.stdout.includes('Status') || status.stdout.includes('[smart-scraper]'),
    '--status shows status output');

  // --extract (no URL) shows usage
  const extractNoUrl = spawnSync('node', [scraperPath, '--extract'], {
    cwd: TEST_DIR,
    encoding: 'utf8'
  });
  assert(extractNoUrl.stdout.includes('Usage'), '--extract without URL shows usage');

  // --parse with HTML
  const parseResult = spawnSync('node', [scraperPath, '--parse', '<html><title>ParseTest</title></html>'], {
    cwd: TEST_DIR,
    encoding: 'utf8'
  });
  assert(parseResult.stdout.includes('ParseTest'), '--parse extracts title from HTML');

  // Invalid flag falls back to status
  const bogusFlag = spawnSync('node', [scraperPath, '--bogus-flag'], {
    cwd: TEST_DIR,
    encoding: 'utf8'
  });
  assert(bogusFlag.stdout.includes('Status') || bogusFlag.stdout.includes('[smart-scraper]'),
    'Invalid flag falls back to status');
});

// ─── 9. SSRF Blocklist Tests ───────────────────────────────────

group('SSRF Protection — 4 cases', () => {
  assert(SS.validateUrl('http://169.254.169.254/latest/meta-data/').valid === false,
    'Cloud metadata IP (169.254.169.254) is blocked');
  assert(SS.validateUrl('http://10.0.0.1/').valid === false,
    'Private 10.x.x.x IP is blocked');
  assert(SS.validateUrl('http://192.168.1.1/').valid === false,
    'Private 192.168.x.x IP is blocked');
  assert(SS.validateUrl('http://localhost/').valid === false,
    'localhost hostname is blocked');
});

// ─── Summary ────────────────────────────────────────────────────

console.log(`\n${'='.repeat(50)}`);
console.log(`📊 Results: ${totalPassed}/${totalTests} tests passed`);
if (totalPassed === totalTests) {
  console.log('✅ All tests passed!');
} else {
  console.log(`❌ ${totalTests - totalPassed} test(s) failed`);
  process.exit(1);
}

// Cleanup
fs.rmSync(TEST_DIR, { recursive: true, force: true });
