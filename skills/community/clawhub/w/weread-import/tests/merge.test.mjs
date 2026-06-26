import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { computeMergeStats, mergeDeletedContent, normalizeDeletedContent, buildDeletedSection } from '../src/merge.mjs';

describe('computeMergeStats', () => {
  it('counts all as added when prev is empty', () => {
    const stats = computeMergeStats([], ['a', 'b', 'c']);
    assert.deepEqual(stats, { added: 3, updated: 0, retained: 0, deleted: 0 });
  });

  it('counts all as deleted when next is empty', () => {
    const stats = computeMergeStats(['a', 'b'], []);
    assert.deepEqual(stats, { added: 0, updated: 0, retained: 0, deleted: 2 });
  });

  it('counts retained when ids match without entry maps', () => {
    const stats = computeMergeStats(['a', 'b'], ['a', 'b']);
    assert.deepEqual(stats, { added: 0, updated: 0, retained: 2, deleted: 0 });
  });

  it('detects updated entries via entry maps', () => {
    const prev = new Map([['a', { id: 'a', quote: 'old' }]]);
    const next = new Map([['a', { id: 'a', quote: 'new' }]]);
    const stats = computeMergeStats(['a'], ['a'], prev, next);
    assert.deepEqual(stats, { added: 0, updated: 1, retained: 0, deleted: 0 });
  });

  it('handles mixed add/update/retain/delete', () => {
    const prev = new Map([
      ['a', { id: 'a', v: 1 }],
      ['b', { id: 'b', v: 1 }],
      ['c', { id: 'c', v: 1 }],
    ]);
    const next = new Map([
      ['a', { id: 'a', v: 1 }],  // retained
      ['b', { id: 'b', v: 2 }],  // updated
      ['d', { id: 'd', v: 1 }],  // added
    ]);
    const stats = computeMergeStats(['a', 'b', 'c'], ['a', 'b', 'd'], prev, next);
    assert.deepEqual(stats, { added: 1, updated: 1, retained: 1, deleted: 1 });
  });

  it('returns zeros for empty inputs', () => {
    const stats = computeMergeStats([], []);
    assert.deepEqual(stats, { added: 0, updated: 0, retained: 0, deleted: 0 });
  });
});

describe('normalizeDeletedContent', () => {
  it('returns empty string for falsy input', () => {
    assert.equal(normalizeDeletedContent(null), '');
    assert.equal(normalizeDeletedContent(''), '');
  });

  it('converts h3 chapter headings to h4', () => {
    const input = '### 第一章\n\nsome content';
    const result = normalizeDeletedContent(input);
    assert.ok(result.includes('#### 第一章'));
  });

  it('removes h3 划线/想法 headings', () => {
    const input = '### 划线\n\n#### 第一章\n\ncontent';
    const result = normalizeDeletedContent(input);
    assert.ok(!result.includes('### 划线'));
  });
});

describe('mergeDeletedContent', () => {
  it('returns empty string when both inputs are empty', () => {
    assert.equal(mergeDeletedContent('', ''), '');
  });

  it('deduplicates entries by id', () => {
    const existing = '#### 第一章\n\n<!-- bookmarkId: abc -->\n<!-- time: 2024-01-01 -->\n\n> quote';
    const newly = '#### 第一章\n\n<!-- bookmarkId: abc -->\n<!-- time: 2024-01-01 -->\n\n> quote';
    const result = mergeDeletedContent(existing, newly, 'bookmarkId');
    const matches = result.match(/<!-- bookmarkId: abc -->/g);
    assert.equal(matches.length, 1);
  });

  it('sorts deleted bookmark chapters and items with metadata', () => {
    const existing = `#### 第二章

<!-- bookmarkId: b2 -->
<!-- time: 2024-01-02T00:00:00.000Z -->
<!-- chapterUid: 2 -->
<!-- chapterIdx: 2 -->
<!-- range: 200-220 -->

> second`;
    const newly = `#### 第一章

<!-- bookmarkId: b3 -->
<!-- time: 2024-01-03T00:00:00.000Z -->
<!-- chapterUid: 1 -->
<!-- chapterIdx: 1 -->
<!-- range: 300-320 -->

> later

<!-- bookmarkId: b1 -->
<!-- time: 2024-01-01T00:00:00.000Z -->
<!-- chapterUid: 1 -->
<!-- chapterIdx: 1 -->
<!-- range: 100-120 -->

> earlier`;
    const result = mergeDeletedContent(existing, newly, 'bookmarkId', new Map([['1', 1], ['2', 2]]));
    assert.ok(result.indexOf('#### 第一章') < result.indexOf('#### 第二章'));
    assert.ok(result.indexOf('<!-- bookmarkId: b1 -->') < result.indexOf('<!-- bookmarkId: b3 -->'));
  });

  it('keeps deleted chapters with the same name separate when chapterUid differs', () => {
    const existing = `#### 章节名

<!-- bookmarkId: b1 -->
<!-- chapterUid: 1 -->
<!-- chapterIdx: 1 -->
<!-- range: 100-120 -->

> first`;
    const newly = `#### 章节名

<!-- bookmarkId: b2 -->
<!-- chapterUid: 2 -->
<!-- chapterIdx: 2 -->
<!-- range: 200-220 -->

> second`;
    const result = mergeDeletedContent(existing, newly, 'bookmarkId', new Map([['1', 1], ['2', 2]]));
    const matches = result.match(/^#### 章节名$/gm);
    assert.equal(matches.length, 2);
  });

  it('sorts deleted reviews by range when available', () => {
    const existing = `#### 第一章

<!-- reviewId: r2 -->
<!-- time: 2024-01-02T00:00:00.000Z -->
<!-- chapterUid: 1 -->
<!-- chapterIdx: 1 -->
<!-- range: 200-220 -->

> **摘录**：second`;
    const newly = `#### 第一章

<!-- reviewId: r1 -->
<!-- time: 2024-01-01T00:00:00.000Z -->
<!-- chapterUid: 1 -->
<!-- chapterIdx: 1 -->
<!-- range: 100-120 -->

> **摘录**：first`;
    const result = mergeDeletedContent(existing, newly, 'reviewId', new Map([['1', 1]]));
    assert.ok(result.indexOf('<!-- reviewId: r1 -->') < result.indexOf('<!-- reviewId: r2 -->'));
  });
});

describe('buildDeletedSection', () => {
  it('returns empty string when both inputs are empty', () => {
    assert.equal(buildDeletedSection('', ''), '');
  });

  it('builds section with bookmark only', () => {
    const result = buildDeletedSection('#### ch1\n\ncontent', '');
    assert.ok(result.includes('### 划线'));
    assert.ok(!result.includes('### 想法'));
  });

  it('builds section with both bookmark and review', () => {
    const result = buildDeletedSection('#### ch1\n\nbookmark', '#### ch1\n\nreview');
    assert.ok(result.includes('### 划线'));
    assert.ok(result.includes('### 想法'));
  });
});
