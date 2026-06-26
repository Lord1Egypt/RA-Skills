import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { getTopLevelSection, parseEntryGroups, parseMetadataComment, extractComparableMapsFromMarkdown, extractIds } from '../src/markdown-parser.mjs';

describe('getTopLevelSection', () => {
  it('extracts section content by title', () => {
    const md = '## 划线\n\ncontent here\n\n## 想法\n\nother';
    assert.equal(getTopLevelSection(md, '划线'), 'content here');
  });

  it('returns empty string when section not found', () => {
    assert.equal(getTopLevelSection('## foo\n\nbar', '划线'), '');
  });

  it('handles empty/null input', () => {
    assert.equal(getTopLevelSection(null, '划线'), '');
    assert.equal(getTopLevelSection('', '划线'), '');
  });
});

describe('parseEntryGroups', () => {
  it('returns empty array for empty input', () => {
    assert.deepEqual(parseEntryGroups('', 'bookmarkId'), []);
  });

  it('parses chapter groups with entries', () => {
    const section = `### 第一章

<!-- bookmarkId: b1 -->
<!-- time: 2024-01-01 -->

> some quote

<!-- bookmarkId: b2 -->
<!-- time: 2024-01-02 -->

> another quote`;

    const groups = parseEntryGroups(section, 'bookmarkId');
    assert.equal(groups.length, 1);
    assert.equal(groups[0].chapterName, '第一章');
    assert.equal(groups[0].items.length, 2);
    assert.equal(groups[0].items[0].id, 'b1');
    assert.equal(groups[0].items[1].id, 'b2');
  });

  it('parses multiple chapters', () => {
    const section = `### Ch1

<!-- bookmarkId: b1 -->

> q1

### Ch2

<!-- bookmarkId: b2 -->

> q2`;

    const groups = parseEntryGroups(section, 'bookmarkId');
    assert.equal(groups.length, 2);
    assert.equal(groups[0].chapterName, 'Ch1');
    assert.equal(groups[1].chapterName, 'Ch2');
  });
});

describe('parseMetadataComment', () => {
  it('extracts value from metadata comment', () => {
    assert.equal(parseMetadataComment('<!-- time: 2024-01-01 -->', 'time'), '2024-01-01');
  });

  it('returns empty string when not found', () => {
    assert.equal(parseMetadataComment('no comment here', 'time'), '');
  });
});

describe('extractIds', () => {
  it('extracts all ids of given kind', () => {
    const text = '<!-- bookmarkId: a -->\n<!-- bookmarkId: b -->\n<!-- reviewId: c -->';
    assert.deepEqual(extractIds(text, 'bookmarkId'), ['a', 'b']);
    assert.deepEqual(extractIds(text, 'reviewId'), ['c']);
  });

  it('returns empty array for no matches', () => {
    assert.deepEqual(extractIds('no ids here', 'bookmarkId'), []);
  });
});

describe('extractComparableMapsFromMarkdown', () => {
  it('round-trips bookmark entries from markdown', () => {
    const md = `## 划线

### 第一章

<!-- bookmarkId: b1 -->
<!-- time: 2024-01-01T00:00:00.000Z -->
<!-- chapterUid: 1 -->

> some quote text

## 想法

### 第一章

<!-- reviewId: r1 -->
<!-- time: 2024-01-01T00:00:00.000Z -->
<!-- chapterUid: 1 -->

> **摘录**：the abstract
>
> **想法**：my thought`;

    const { bookmarkEntryMap, reviewEntryMap } = extractComparableMapsFromMarkdown(md);
    assert.ok(bookmarkEntryMap.b1);
    assert.equal(bookmarkEntryMap.b1.quote, 'some quote text');
    assert.equal(bookmarkEntryMap.b1.chapterName, '第一章');

    assert.ok(reviewEntryMap.r1);
    assert.equal(reviewEntryMap.r1.quote, 'the abstract');
    assert.equal(reviewEntryMap.r1.note, 'my thought');
  });

  it('returns empty maps for empty markdown', () => {
    const { bookmarkEntryMap, reviewEntryMap } = extractComparableMapsFromMarkdown('');
    assert.deepEqual(bookmarkEntryMap, {});
    assert.deepEqual(reviewEntryMap, {});
  });
});
