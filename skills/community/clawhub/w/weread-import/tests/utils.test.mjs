import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { sanitizeFileName, cleanText, yamlScalar } from '../src/utils.mjs';

describe('sanitizeFileName', () => {
  it('removes book title brackets', () => {
    assert.equal(sanitizeFileName('《自卑与超越》'), '自卑与超越');
  });

  it('replaces illegal filesystem chars with space', () => {
    assert.equal(sanitizeFileName('a/b:c*d'), 'a b c d');
  });

  it('collapses multiple spaces', () => {
    assert.equal(sanitizeFileName('a   b'), 'a b');
  });

  it('defaults to 未命名书籍 for falsy input', () => {
    assert.equal(sanitizeFileName(null), '未命名书籍');
    assert.equal(sanitizeFileName(''), '未命名书籍');
    assert.equal(sanitizeFileName(undefined), '未命名书籍');
  });

  it('trims whitespace', () => {
    assert.equal(sanitizeFileName('  hello  '), 'hello');
  });
});

describe('cleanText', () => {
  it('removes zero-width spaces', () => {
    assert.equal(cleanText('hello\u200bworld'), 'helloworld');
  });

  it('replaces &nbsp; with space', () => {
    assert.equal(cleanText('a&nbsp;b'), 'a b');
  });

  it('replaces &amp; with &', () => {
    assert.equal(cleanText('a&amp;b'), 'a&b');
  });

  it('normalizes line endings', () => {
    assert.equal(cleanText('a\r\nb\rc'), 'a\nb\nc');
  });

  it('collapses triple+ newlines to double', () => {
    assert.equal(cleanText('a\n\n\n\nb'), 'a\n\nb');
  });

  it('returns empty string for falsy input', () => {
    assert.equal(cleanText(null), '');
    assert.equal(cleanText(undefined), '');
  });
});

describe('yamlScalar', () => {
  it('wraps value in JSON quotes', () => {
    assert.equal(yamlScalar('hello'), '"hello"');
  });

  it('escapes special characters', () => {
    assert.equal(yamlScalar('say "hi"'), '"say \\"hi\\""');
  });

  it('handles null/undefined', () => {
    assert.equal(yamlScalar(null), '""');
    assert.equal(yamlScalar(undefined), '""');
  });
});
