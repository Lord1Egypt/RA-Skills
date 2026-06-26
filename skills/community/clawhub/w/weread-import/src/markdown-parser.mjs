import { cleanText } from './utils.mjs';
import { comparableBookmarkEntry, comparableReviewEntry } from './entries.mjs';

export function getTopLevelSection(markdown, title) {
  const escaped = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`## ${escaped}\\n\\n([\\s\\S]*?)(?=\\n## |$)`);
  const m = String(markdown || '').match(regex);
  return m ? m[1].trim() : '';
}

export function parseEntryGroups(sectionMarkdown, idKind) {
  const text = String(sectionMarkdown || '').trim();
  if (!text) return [];
  const groups = [];
  const chapterRegex = /^###\s+(.+)$/gm;
  const matches = [...text.matchAll(chapterRegex)];
  for (let i = 0; i < matches.length; i += 1) {
    const chapterName = matches[i][1].trim();
    const start = matches[i].index + matches[i][0].length;
    const end = i + 1 < matches.length ? matches[i + 1].index : text.length;
    const chapterBody = text.slice(start, end).trim();
    if (!chapterBody) continue;
    const entryRegex = new RegExp(`<!-- ${idKind}: ([^>]+) -->([\\s\\S]*?)(?=\\n<!-- ${idKind}: |$)`, 'g');
    const items = [];
    let m;
    while ((m = entryRegex.exec(chapterBody))) {
      items.push({ id: m[1].trim(), body: m[2].trim() });
    }
    if (items.length) groups.push({ chapterName, items });
  }
  return groups;
}

export function parseMetadataComment(body, key) {
  const m = String(body || '').match(new RegExp(`<!-- ${key}: ([^>]+) -->`));
  return m ? m[1].trim() : '';
}

export function extractComparableMapsFromMarkdown(markdown) {
  const bookmarkSection = getTopLevelSection(markdown, '划线');
  const reviewSection = getTopLevelSection(markdown, '想法');

  const bookmarkPairs = [];
  for (const group of parseEntryGroups(bookmarkSection, 'bookmarkId')) {
    for (const item of group.items) {
      const body = item.body.trim();
      const quote = cleanText(body.replace(/<!--[^>]*-->/g, '').replace(/^>\s?/gm, '').trim());
      const entry = comparableBookmarkEntry({
        id: item.id,
        chapterName: group.chapterName,
        chapterUid: parseMetadataComment(body, 'chapterUid'),
        createdIso: parseMetadataComment(body, 'time'),
        quote,
      });
      if (entry.id) bookmarkPairs.push([entry.id, entry]);
    }
  }
  const bookmarkEntryMap = Object.fromEntries(bookmarkPairs);

  const reviewPairs = [];
  for (const group of parseEntryGroups(reviewSection, 'reviewId')) {
    for (const item of group.items) {
      const body = item.body.trim();
      const quoteMatch = body.match(/> \*\*摘录\*\*：([^\n]*)/);
      const noteMatch = body.match(/> \*\*想法\*\*：([^\n]*)/);
      const entry = comparableReviewEntry({
        id: item.id,
        chapterName: group.chapterName,
        chapterUid: parseMetadataComment(body, 'chapterUid'),
        createdIso: parseMetadataComment(body, 'time'),
        quote: cleanText(quoteMatch ? quoteMatch[1] : ''),
        note: cleanText(noteMatch ? noteMatch[1] : ''),
      });
      if (entry.id) reviewPairs.push([entry.id, entry]);
    }
  }
  const reviewEntryMap = Object.fromEntries(reviewPairs);

  return { bookmarkEntryMap, reviewEntryMap };
}

export function extractIds(text, kind) {
  const regex = new RegExp(`<!-- ${kind}: ([^>]+) -->`, 'g');
  const ids = [];
  let m;
  while ((m = regex.exec(text || ''))) ids.push(m[1].trim());
  return ids;
}
