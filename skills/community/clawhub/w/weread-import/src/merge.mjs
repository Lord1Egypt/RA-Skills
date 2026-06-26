import { parseEntryGroups, parseMetadataComment } from './markdown-parser.mjs';
import { compareChapterGroups, compareEntriesBySort, parseBookmarkIdPosition, parseRangePosition, toFiniteNumber } from './sort.mjs';

export function computeMergeStats(prevIds, nextIds, prevEntries = null, nextEntries = null) {
  const prev = new Set(prevIds);
  const next = new Set(nextIds);
  let added = 0, updated = 0, retained = 0, deleted = 0;

  const prevMap = prevEntries instanceof Map ? prevEntries : null;
  const nextMap = nextEntries instanceof Map ? nextEntries : null;

  for (const id of next) {
    if (!prev.has(id)) {
      added++;
      continue;
    }
    if (prevMap && nextMap && prevMap.has(id) && nextMap.has(id)) {
      const prevValue = JSON.stringify(prevMap.get(id));
      const nextValue = JSON.stringify(nextMap.get(id));
      if (prevValue !== nextValue) updated++;
      else retained++;
    } else {
      retained++;
    }
  }
  for (const id of prev) if (!next.has(id)) deleted++;
  return { added, updated, retained, deleted };
}

export function normalizeDeletedContent(text) {
  return String(text || '')
    .replace(/^###\s*划线\s*$/gm, '')
    .replace(/^###\s*想法\s*$/gm, '')
    .replace(/^###\s+(?!划线\s*$|想法\s*$)(.+)$/gm, '#### $1')
    .replace(/^- time:\s*(.*)$/gm, '<!-- time: $1 -->')
    .replace(/^- chapterUid:\s*(.*)$/gm, '<!-- chapterUid: $1 -->')
    .replace(/^- chapterIdx:\s*(.*)$/gm, '<!-- chapterIdx: $1 -->')
    .replace(/^- range:\s*(.*)$/gm, '<!-- range: $1 -->')
    .replace(/(<!-- (?:bookmarkId|reviewId): [^>]+ -->)\n\n(<!-- (?:time|chapterUid|chapterIdx|range): [^>]+ -->)/g, '$1\n$2')
    .trim();
}

export function pickDeletedEntries(sectionMarkdown, idKind, deletedIds) {
  const deleted = new Set((deletedIds || []).filter(Boolean));
  if (!deleted.size) return '';
  const groups = parseEntryGroups(sectionMarkdown, idKind)
    .map((group) => ({
      chapterName: group.chapterName,
      items: group.items.filter((item) => deleted.has(item.id)),
    }))
    .filter((group) => group.items.length);
  if (!groups.length) return '';
  return groups.map((group) => {
    const body = group.items.map((item) => `<!-- ${idKind}: ${item.id} -->\n\n${item.body}`).join('\n\n');
    return `#### ${group.chapterName}\n\n${body}`;
  }).join('\n\n');
}

function createDeletedEntry(itemId, body, idKind, chapterOrderMap) {
  const time = parseMetadataComment(body, 'time');
  const chapterUid = parseMetadataComment(body, 'chapterUid');
  const metadataRange = parseMetadataComment(body, 'range');
  const bookmarkPosition = idKind === 'bookmarkId' ? parseBookmarkIdPosition(itemId) : null;
  const rangePosition = parseRangePosition(metadataRange);
  const position = rangePosition || bookmarkPosition;

  return {
    id: itemId,
    time,
    sortTime: time ? Date.parse(time) || 0 : 0,
    chapterUid,
    sortChapterIndex: toFiniteNumber(parseMetadataComment(body, 'chapterIdx')) ?? toFiniteNumber(chapterOrderMap.get(String(chapterUid))),
    sortPositionStart: position ? position.start : null,
    sortPositionEnd: position ? position.end : null,
    range: metadataRange || '',
    body: body
      .replace(/<!-- time: [^>]+ -->/g, '')
      .replace(/<!-- chapterUid: [^>]+ -->/g, '')
      .replace(/<!-- chapterIdx: [^>]+ -->/g, '')
      .replace(/<!-- range: [^>]+ -->/g, '')
      .trim(),
  };
}

export function mergeDeletedContent(existingDeleted, newlyDeleted, idKind = 'bookmarkId', chapterOrderMap = new Map()) {
  const mergedText = [normalizeDeletedContent(existingDeleted), normalizeDeletedContent(newlyDeleted)].filter(Boolean).join('\n\n');
  if (!mergedText) return '';

  const groups = [];
  const chapterRegex = /^####\s+(.+)$/gm;
  const matches = [...mergedText.matchAll(chapterRegex)];
  for (let i = 0; i < matches.length; i += 1) {
    const chapterName = matches[i][1].trim();
    const start = matches[i].index + matches[i][0].length;
    const end = i + 1 < matches.length ? matches[i + 1].index : mergedText.length;
    const chapterBody = mergedText.slice(start, end).trim();
    if (!chapterBody) continue;
    const entryRegex = new RegExp(`<!-- ${idKind}: ([^>]+) -->([\\s\\S]*?)(?=\\n<!-- ${idKind}: |$)`, 'g');
    const items = [];
    let m;
    while ((m = entryRegex.exec(chapterBody))) {
      const item = createDeletedEntry(m[1].trim(), m[2].trim(), idKind, chapterOrderMap);
      items.push(item);
    }
    if (items.length) {
      groups.push({
        chapterName,
        chapterUid: items.find((item) => item.chapterUid)?.chapterUid || '',
        sortChapterIndex: items.find((item) => toFiniteNumber(item.sortChapterIndex) !== null)?.sortChapterIndex ?? null,
        items,
      });
    }
  }

  const mergedGroups = new Map();
  for (const group of groups) {
    const groupKey = `${group.chapterUid}__${group.chapterName}`;
    if (!mergedGroups.has(groupKey)) {
      mergedGroups.set(groupKey, {
        chapterName: group.chapterName,
        chapterUid: group.chapterUid,
        sortChapterIndex: group.sortChapterIndex,
        itemMap: new Map(),
      });
    }
    const mergedGroup = mergedGroups.get(groupKey);
    if (toFiniteNumber(mergedGroup.sortChapterIndex) === null) mergedGroup.sortChapterIndex = group.sortChapterIndex;
    const itemMap = mergedGroup.itemMap;
    for (const item of group.items) if (!itemMap.has(item.id)) itemMap.set(item.id, item);
  }

  return Array.from(mergedGroups.values()).sort(compareChapterGroups).map((group) => {
    const body = Array.from(group.itemMap.values()).sort(compareEntriesBySort).map((item) => {
      const lines = [`<!-- ${idKind}: ${item.id} -->`];
      if (item.time) lines.push(`<!-- time: ${item.time} -->`);
      if (item.chapterUid) lines.push(`<!-- chapterUid: ${item.chapterUid} -->`);
      if (toFiniteNumber(item.sortChapterIndex) !== null) lines.push(`<!-- chapterIdx: ${item.sortChapterIndex} -->`);
      if (item.range) lines.push(`<!-- range: ${item.range} -->`);
      if (item.body) lines.push('', item.body);
      return lines.join('\n');
    }).join('\n\n');
    return `#### ${group.chapterName}\n\n${body}`;
  }).join('\n\n');
}

export function buildDeletedSection(existingDeletedBookmark, existingDeletedReview) {
  const bookmarkText = normalizeDeletedContent(existingDeletedBookmark);
  const reviewText = normalizeDeletedContent(existingDeletedReview);
  const parts = [];
  if (bookmarkText) parts.push(`### 划线\n\n${bookmarkText}`);
  if (reviewText) parts.push(`### 想法\n\n${reviewText}`);
  return parts.join('\n\n');
}
