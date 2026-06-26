import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { buildFrontmatter, buildMarkdownFromApi, renderBookmarkSections, renderReviewSections } from '../src/render.mjs';

describe('buildFrontmatter', () => {
  it('generates valid YAML frontmatter', () => {
    const fm = buildFrontmatter({
      title: '测试书名',
      author: '作者',
      bookId: '123',
      noteUpdatedIso: '2024-01-01T00:00:00.000Z',
      highlightCount: 5,
      reviewCount: 3,
      tags: ['reading', 'weread'],
    });
    assert.ok(fm.startsWith('---'));
    assert.ok(fm.endsWith('---'));
    assert.ok(fm.includes('title: "测试书名"'));
    assert.ok(fm.includes('author: "作者"'));
    assert.ok(fm.includes('bookId: "123"'));
    assert.ok(fm.includes('source: weread'));
    assert.ok(fm.includes('highlightCount: 5'));
    assert.ok(fm.includes('reviewCount: 3'));
    assert.ok(fm.includes('  - reading'));
    assert.ok(fm.includes('  - weread'));
  });

  it('escapes special characters in title', () => {
    const fm = buildFrontmatter({
      title: 'say "hello"',
      author: '',
      bookId: '',
      noteUpdatedIso: '',
      highlightCount: 0,
      reviewCount: 0,
    });
    assert.ok(fm.includes('title: "say \\"hello\\""'));
  });

  it('defaults author to 未知', () => {
    const fm = buildFrontmatter({ title: 'x', bookId: '', noteUpdatedIso: '', highlightCount: 0, reviewCount: 0 });
    assert.ok(fm.includes('author: "未知"'));
  });
});

describe('renderBookmarkSections', () => {
  it('returns empty string for empty bookmarks', () => {
    assert.equal(renderBookmarkSections([]), '');
  });

  it('renders bookmarks grouped by chapter', () => {
    const bookmarks = [
      { bookmarkId: 'b1', chapterUid: 1, chapterIdx: 1, chapterName: '第一章', createTime: 1700000000, range: '10-20', markText: 'highlight text' },
    ];
    const result = renderBookmarkSections(bookmarks);
    assert.ok(result.includes('### 第一章'));
    assert.ok(result.includes('<!-- bookmarkId: b1 -->'));
    assert.ok(result.includes('<!-- chapterIdx: 1 -->'));
    assert.ok(result.includes('<!-- range: 10-20 -->'));
    assert.ok(result.includes('> highlight text'));
  });

  it('sorts bookmarks by position parsed from bookmarkId within a chapter', () => {
    const bookmarks = [
      { bookmarkId: '33628204_51_9261-9269', chapterUid: 51, chapterIdx: 51, chapterName: '第一章', createTime: 1700000000, markText: 'later in chapter' },
      { bookmarkId: '33628204_51_1130-1204', chapterUid: 51, chapterIdx: 51, chapterName: '第一章', createTime: 1700000001, markText: 'earlier in chapter' },
      { bookmarkId: '33628204_51_6409-6420', chapterUid: 51, chapterIdx: 51, chapterName: '第一章', createTime: 1700000002, markText: 'middle of chapter' },
    ];
    const result = renderBookmarkSections(bookmarks);
    assert.ok(result.indexOf('earlier in chapter') < result.indexOf('middle of chapter'));
    assert.ok(result.indexOf('middle of chapter') < result.indexOf('later in chapter'));
  });

  it('supports legacy bookmarkId values with a single position number', () => {
    const bookmarks = [
      { bookmarkId: '840236_21_392', chapterUid: 21, chapterIdx: 21, chapterName: '第一章', createTime: 1700000001, markText: 'single position' },
      { bookmarkId: '840236_21_105-120', chapterUid: 21, chapterIdx: 21, chapterName: '第一章', createTime: 1700000000, markText: 'range position' },
    ];
    const result = renderBookmarkSections(bookmarks);
    assert.ok(result.indexOf('range position') < result.indexOf('single position'));
  });

  it('sorts bookmark chapters by chapterIdx before chapterUid', () => {
    const bookmarks = [
      { bookmarkId: 'b2', chapterUid: 10, chapterIdx: 4, chapterName: '第四章', createTime: 1700000000, range: '10-20', markText: 'chapter four' },
      { bookmarkId: 'b1', chapterUid: 6, chapterIdx: 1, chapterName: '第一章', createTime: 1700000001, range: '10-20', markText: 'chapter one' },
    ];
    const result = renderBookmarkSections(bookmarks);
    assert.ok(result.indexOf('### 第一章') < result.indexOf('### 第四章'));
  });
});

describe('renderReviewSections', () => {
  it('returns empty string for empty reviews', () => {
    assert.equal(renderReviewSections([]), '');
  });

  it('renders reviews with quote and note', () => {
    const reviews = [
      { reviewId: 'r1', review: { reviewId: 'r1', chapterUid: 1, chapterIdx: 1, chapterName: '第一章', createTime: 1700000000, range: '20-40', abstract: 'the quote', content: 'my thought' } },
    ];
    const result = renderReviewSections(reviews);
    assert.ok(result.includes('### 第一章'));
    assert.ok(result.includes('<!-- reviewId: r1 -->'));
    assert.ok(result.includes('<!-- chapterIdx: 1 -->'));
    assert.ok(result.includes('<!-- range: 20-40 -->'));
    assert.ok(result.includes('> **摘录**：the quote'));
    assert.ok(result.includes('> **想法**：my thought'));
  });

  it('sorts reviews by range within a chapter', () => {
    const reviews = [
      { reviewId: 'r3', review: { reviewId: 'r3', chapterUid: 1, chapterIdx: 1, chapterName: '第一章', createTime: 1700000002, range: '300-320', abstract: 'later', content: 'later note' } },
      { reviewId: 'r1', review: { reviewId: 'r1', chapterUid: 1, chapterIdx: 1, chapterName: '第一章', createTime: 1700000000, range: '100-120', abstract: 'earlier', content: 'earlier note' } },
      { reviewId: 'r2', review: { reviewId: 'r2', chapterUid: 1, chapterIdx: 1, chapterName: '第一章', createTime: 1700000001, range: '200-220', abstract: 'middle', content: 'middle note' } },
    ];
    const result = renderReviewSections(reviews);
    assert.ok(result.indexOf('> **摘录**：earlier') < result.indexOf('> **摘录**：middle'));
    assert.ok(result.indexOf('> **摘录**：middle') < result.indexOf('> **摘录**：later'));
  });

  it('sorts review chapters by chapterIdx before chapterUid', () => {
    const reviews = [
      { reviewId: 'r2', review: { reviewId: 'r2', chapterUid: 10, chapterIdx: 4, chapterName: '第四章', createTime: 1700000000, range: '10-20', abstract: 'chapter four', content: 'note' } },
      { reviewId: 'r1', review: { reviewId: 'r1', chapterUid: 6, chapterIdx: 1, chapterName: '第一章', createTime: 1700000001, range: '10-20', abstract: 'chapter one', content: 'note' } },
    ];
    const result = renderReviewSections(reviews);
    assert.ok(result.indexOf('### 第一章') < result.indexOf('### 第四章'));
  });
});

describe('buildMarkdownFromApi', () => {
  it('produces complete markdown with frontmatter', () => {
    const book = { bookId: '123', title: '测试', author: '作者', sort: 1700000000 };
    const bookmarks = [
      { bookmarkId: 'b1', chapterUid: 1, chapterName: '第一章', createTime: 1700000000, markText: 'text' },
    ];
    const md = buildMarkdownFromApi(book, bookmarks, []);
    assert.ok(md.startsWith('---'));
    assert.ok(md.includes('# 测试'));
    assert.ok(md.includes('## 划线'));
    assert.ok(!md.includes('## 想法'));
  });

  it('omits bookmark/review sections when empty', () => {
    const book = { bookId: '123', title: '测试', author: '', sort: 0 };
    const md = buildMarkdownFromApi(book, [], []);
    assert.ok(!md.includes('## 划线'));
    assert.ok(!md.includes('## 想法'));
    assert.ok(!md.includes('## 已删除'));
  });
});
