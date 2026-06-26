/**
 * Smart Web Scraper — test suite
 * Tests the smart-scraper.js CLI interface.
 *
 * Run: node ../../test-runner.js --skill smart-scraper.js --test test/run-tests.js
 */

module.exports = [
  // ── Status ───────────────────────────────────────────────────────────────
  { name: "--status shows scraper status", args: ["--status"], expected: "[smart-scraper] Status:" },
  { name: "No args defaults to status", args: [], expected: "[smart-scraper] Status:" },
  { name: "Status shows cached pages", args: ["--status"], expected: "Cached pages:" },
  { name: "Status shows cache size", args: ["--status"], expected: "Cache size:" },

  // ── Parse (no network needed) ────────────────────────────────────────────
  // Note: paragraphs shorter than 20 chars are filtered by the parser
  // Note: link regex requires double-quoted href="..." not single quotes
  {
    name: "--parse finds title",
    args: ["--parse", "<html><head><title>Hello World</title></head><body><h1>Big Heading</h1></body></html>"],
    expected: "Title: Hello World"
  },
  {
    name: "--parse finds headings",
    args: ["--parse", "<html><body><h1>A</h1><h2>B</h2><h3>C</h3></body></html>"],
    expected: "Headings: 3"
  },
  {
    name: "--parse finds tables",
    args: ["--parse", '<html><body><table><tr><td>A</td></tr></table></body></html>'],
    expected: "Tables: 1"
  },
  {
    name: "--parse finds lists",
    args: ["--parse", '<html><body><ul><li>Alpha</li><li>Beta</li></ul></body></html>'],
    expected: "Lists: 1"
  },
  {
    name: "--parse with empty title uses blank string",
    args: ["--parse", "<html><body><p>content here but no title tag in this one</p></body></html>"],
    expected: "Title: "
  },

  // ── Extract Help / Usage ─────────────────────────────────────────────────
  {
    name: "--extract without URL shows usage",
    args: ["--extract"],
    expected: "Usage: smart-scraper.js --extract <url>"
  },
  {
    name: "--parse with empty string shows usage",
    args: ["--parse", ""],
    expected: "Usage:"
  },

  // ── Extract with real URL (integration check) ────────────────────────────
  {
    name: "--extract --all on example.com",
    args: ["--extract", "--all", "https://example.com"],
    expected: "[smart-scraper] Extracted from",
    timeout: 20000
  },
  {
    name: "--extract sees example.com title",
    args: ["--extract", "https://example.com"],
    expected: "Title: Example Domain",
    timeout: 20000
  },

  // ── Edge Cases ───────────────────────────────────────────────────────────
  {
    name: "--parse with malformed HTML doesn't crash",
    args: ["--parse", "<div><span><p>broken"],
    expected: "Title: "
  },
];
