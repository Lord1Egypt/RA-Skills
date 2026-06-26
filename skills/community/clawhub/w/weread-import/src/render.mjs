import fs from 'node:fs/promises';
import path from 'node:path';
import { sanitizeFileName, cleanText, yamlScalar } from './utils.mjs';
import { buildBookmarkEntries, buildReviewEntries, groupByChapter, collectBookmarkIds, collectReviewIds } from './entries.mjs';
import { getTopLevelSection, extractIds } from './markdown-parser.mjs';
import { pickDeletedEntries, mergeDeletedContent, buildDeletedSection } from './merge.mjs';
import { toFiniteNumber } from './sort.mjs';

const DEFAULT_TAGS = (process.env.WEREAD_TAGS || 'reading,weread').split(',').map((x) => x.trim()).filter(Boolean);

function parseDeletedSections(markdown) {
  const m = markdown.match(/## 已删除\n\n([\s\S]*?)$/);
  const deleted = m ? m[1].trim() : '';
  const bookmark = (() => {
    const x = deleted.match(/### 划线\n\n([\s\S]*?)(?=\n### 想法|$)/);
    return x ? x[1].trim() : '';
  })();
  const review = (() => {
    const x = deleted.match(/### 想法\n\n([\s\S]*?)$/);
    return x ? x[1].trim() : '';
  })();
  return { bookmark, review };
}

function buildChapterOrderMap(entries) {
  const orderMap = new Map();
  for (const entry of entries) {
    const chapterUid = String(entry.chapterUid ?? '').trim();
    const chapterIndex = toFiniteNumber(entry.sortChapterIndex);
    if (!chapterUid || chapterIndex === null || orderMap.has(chapterUid)) continue;
    orderMap.set(chapterUid, chapterIndex);
  }
  return orderMap;
}

export function renderBookmarkSections(bookmarks) {
  const groups = groupByChapter(buildBookmarkEntries(bookmarks))
    .map((g) => ({ ...g, items: g.items.filter((e) => e.id && e.quote) }))
    .filter((g) => g.items.length);
  if (!groups.length) return '';
  return groups.map((g) => {
    const body = g.items.map((e) => [
      `<!-- bookmarkId: ${e.id} -->`,
      `<!-- time: ${e.createdIso} -->`,
      `<!-- chapterUid: ${e.chapterUid} -->`,
      ...(Number.isFinite(e.sortChapterIndex) ? [`<!-- chapterIdx: ${e.sortChapterIndex} -->`] : []),
      ...(e.range ? [`<!-- range: ${e.range} -->`] : []),
      '',
      `> ${e.quote}`,
    ].join('\n')).join('\n\n');
    return `### ${g.chapterName}\n\n${body}`;
  }).join('\n\n');
}

export function renderReviewSections(reviews) {
  const groups = groupByChapter(buildReviewEntries(reviews))
    .map((g) => ({ ...g, items: g.items.filter((e) => e.id && (e.quote || e.note)) }))
    .filter((g) => g.items.length);
  if (!groups.length) return '';
  return groups.map((g) => {
    const body = g.items.map((e) => {
      const lines = [
        `<!-- reviewId: ${e.id} -->`,
        `<!-- time: ${e.createdIso} -->`,
        `<!-- chapterUid: ${e.chapterUid} -->`,
        ...(Number.isFinite(e.sortChapterIndex) ? [`<!-- chapterIdx: ${e.sortChapterIndex} -->`] : []),
        ...(e.range ? [`<!-- range: ${e.range} -->`] : []),
        '',
      ];
      if (e.quote) lines.push(`> **摘录**：${e.quote}`);
      if (e.quote && e.note) lines.push('>');
      if (e.note) lines.push(`> **想法**：${e.note}`);
      return lines.join('\n');
    }).join('\n\n');
    return `### ${g.chapterName}\n\n${body}`;
  }).join('\n\n');
}

export function buildFrontmatter({ title, author, bookId, noteUpdatedIso, highlightCount, reviewCount, tags = DEFAULT_TAGS }) {
  const normalizedTags = Array.isArray(tags) ? tags.map((x) => String(x).trim()).filter(Boolean) : DEFAULT_TAGS;
  return [
    '---',
    `title: ${yamlScalar(title)}`,
    `author: ${yamlScalar(author || '未知')}`,
    `bookId: ${yamlScalar(bookId)}`,
    'source: weread',
    `lastNoteUpdate: ${yamlScalar(noteUpdatedIso)}`,
    `highlightCount: ${Number(highlightCount || 0)}`,
    `reviewCount: ${Number(reviewCount || 0)}`,
    'tags:',
    ...normalizedTags.map((tag) => `  - ${tag}`),
    '---',
  ].join('\n');
}

export function buildMarkdownFromApi(book, bookmarks, reviews, existingMarkdown = '', options = {}) {
  const title = sanitizeFileName(book.title);
  const author = cleanText(book.author || '');
  const noteUpdatedIso = book.sort ? new Date(book.sort * 1000).toISOString() : '';
  const bookmarkEntries = buildBookmarkEntries(bookmarks);
  const reviewEntries = buildReviewEntries(reviews);
  const bookmarkChapterOrder = buildChapterOrderMap(bookmarkEntries);
  const reviewChapterOrder = buildChapterOrderMap(reviewEntries);
  const bookmarkBlocks = renderBookmarkSections(bookmarks);
  const reviewBlocks = renderReviewSections(reviews);

  const prevBookmarkIds = extractIds(existingMarkdown, 'bookmarkId');
  const prevReviewIds = extractIds(existingMarkdown, 'reviewId');
  const nextBookmarkIds = collectBookmarkIds(bookmarks);
  const nextReviewIds = collectReviewIds(reviews);
  const deletedBookmarkIds = prevBookmarkIds.filter((id) => !nextBookmarkIds.includes(id));
  const deletedReviewIds = prevReviewIds.filter((id) => !nextReviewIds.includes(id));

  const existingDeleted = existingMarkdown ? parseDeletedSections(existingMarkdown) : { bookmark: '', review: '' };
  const previousBookmarkSection = getTopLevelSection(existingMarkdown, '划线');
  const previousReviewSection = getTopLevelSection(existingMarkdown, '想法');
  const newlyDeletedBookmarks = pickDeletedEntries(previousBookmarkSection, 'bookmarkId', deletedBookmarkIds);
  const newlyDeletedReviews = pickDeletedEntries(previousReviewSection, 'reviewId', deletedReviewIds);
  const deletedBlocks = buildDeletedSection(
    mergeDeletedContent(existingDeleted.bookmark, newlyDeletedBookmarks, 'bookmarkId', bookmarkChapterOrder),
    mergeDeletedContent(existingDeleted.review, newlyDeletedReviews, 'reviewId', reviewChapterOrder),
  );

  const sections = [
    buildFrontmatter({
      title,
      author,
      bookId: book.bookId,
      noteUpdatedIso,
      highlightCount: bookmarks.length,
      reviewCount: reviews.length,
      tags: options.tags,
    }),
    `# ${title}`,
  ];
  if (bookmarkBlocks) sections.push(`## 划线\n\n${bookmarkBlocks}`);
  if (reviewBlocks) sections.push(`## 想法\n\n${reviewBlocks}`);
  if (deletedBlocks) sections.push(`## 已删除\n\n${deletedBlocks}`);
  return `${sections.join('\n\n')}\n`;
}

export async function writeBook(outputDir, title, markdown) {
  await fs.mkdir(outputDir, { recursive: true });
  const fileName = `${sanitizeFileName(title)}.md`;
  const filePath = path.join(outputDir, fileName);
  await fs.writeFile(filePath, `${markdown.trim()}\n`, 'utf8');
  return { filePath };
}
