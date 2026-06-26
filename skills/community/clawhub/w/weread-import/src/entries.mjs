import { cleanText, reviewPayload } from './utils.mjs';
import { compareChapterGroups, compareEntriesBySort, formatRangePosition, parseBookmarkIdPosition, parseRangePosition, toFiniteNumber } from './sort.mjs';

export function comparableBookmarkEntry(entry) {
  return {
    id: String(entry.id || ''),
    chapterUid: String(entry.chapterUid ?? ''),
    chapterName: cleanText(entry.chapterName || '章节名'),
    createdIso: String(entry.createdIso || ''),
    quote: cleanText(entry.quote || ''),
  };
}

export function comparableReviewEntry(entry) {
  return {
    id: String(entry.id || ''),
    chapterUid: String(entry.chapterUid ?? ''),
    chapterName: cleanText(entry.chapterName || '章节名'),
    createdIso: String(entry.createdIso || ''),
    quote: cleanText(entry.quote || ''),
    note: cleanText(entry.note || ''),
  };
}

export function buildBookmarkEntries(bookmarks) {
  return bookmarks.map((item) => {
    const position = parseRangePosition(item.range) || parseBookmarkIdPosition(item.bookmarkId);
    return {
      id: item.bookmarkId || '',
      chapterUid: item.chapterUid ?? position?.chapterUid ?? '',
      chapterName: cleanText(item.chapterName || item.chapterTitle || '章节名'),
      createdIso: item.createTime ? new Date(item.createTime * 1000).toISOString() : '',
      sortTime: item.createTime || 0,
      sortChapterIndex: toFiniteNumber(item.chapterIdx),
      sortPositionStart: position ? position.start : null,
      sortPositionEnd: position ? position.end : null,
      range: cleanText(item.range || formatRangePosition(position)),
      quote: cleanText(item.markText || ''),
    };
  });
}

export function buildReviewEntries(reviews) {
  return reviews.map((item) => {
    const p = reviewPayload(item);
    const position = parseRangePosition(p.range || item.range);
    return {
      id: item.reviewId || p.reviewId || '',
      chapterUid: p.chapterUid ?? item.chapterUid ?? '',
      chapterName: cleanText(p.chapterName || p.chapterTitle || item.chapterName || item.chapterTitle || '章节名'),
      createdIso: (p.createTime || item.createTime) ? new Date((p.createTime || item.createTime) * 1000).toISOString() : '',
      sortTime: p.createTime || item.createTime || 0,
      sortChapterIndex: toFiniteNumber(p.chapterIdx ?? item.chapterIdx),
      sortPositionStart: position ? position.start : null,
      sortPositionEnd: position ? position.end : null,
      range: cleanText(p.range || item.range || formatRangePosition(position)),
      quote: cleanText(p.abstract || p.markText || item.abstract || ''),
      note: cleanText(p.content || item.content || ''),
    };
  });
}

export function groupByChapter(entries) {
  const map = new Map();
  for (const e of entries) {
    const key = `${e.chapterUid}__${e.chapterName}`;
    if (!map.has(key)) {
      map.set(key, {
        chapterName: e.chapterName || '章节名',
        chapterUid: e.chapterUid,
        sortChapterIndex: toFiniteNumber(e.sortChapterIndex),
        items: [],
      });
    }
    const group = map.get(key);
    group.items.push(e);
    if (group.sortChapterIndex === null) group.sortChapterIndex = toFiniteNumber(e.sortChapterIndex);
  }
  return Array.from(map.values())
    .map((g) => ({
      ...g,
      items: g.items.sort(compareEntriesBySort),
    }))
    .sort(compareChapterGroups);
}

export function collectBookmarkIds(bookmarks) {
  return bookmarks.map((item) => item.bookmarkId).filter(Boolean).sort();
}

export function collectReviewIds(reviews) {
  return reviews.map((item) => item.reviewId || item.review?.reviewId).filter(Boolean).sort();
}
