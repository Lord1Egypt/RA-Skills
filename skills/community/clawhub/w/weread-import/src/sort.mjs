export function toFiniteNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

export function parseRangePosition(range) {
  const match = String(range || '').match(/^(\d+)(?:-(\d+))?$/);
  if (!match) return null;
  const start = Number(match[1]);
  const end = Number(match[2] || match[1]);
  if (!Number.isFinite(start) || !Number.isFinite(end)) return null;
  return { start, end };
}

export function formatRangePosition(position) {
  if (!position) return '';
  const start = toFiniteNumber(position.start);
  const end = toFiniteNumber(position.end);
  if (start === null || end === null) return '';
  return start === end ? String(start) : `${start}-${end}`;
}

export function parseBookmarkIdPosition(bookmarkId) {
  const match = String(bookmarkId || '').match(/^.+_(\d+)_(\d+)(?:-(\d+))?$/);
  if (!match) return null;
  const chapterUid = match[1];
  const start = Number(match[2]);
  const end = Number(match[3] || match[2]);
  if (!Number.isFinite(start) || !Number.isFinite(end)) return null;
  return { chapterUid, start, end };
}

function compareNullableNumbers(a, b) {
  const numberA = toFiniteNumber(a);
  const numberB = toFiniteNumber(b);
  if (numberA !== null && numberB !== null) return numberA - numberB;
  if (numberA !== null) return -1;
  if (numberB !== null) return 1;
  return 0;
}

export function compareEntriesBySort(a, b) {
  const positionDiff = compareNullableNumbers(a.sortPositionStart, b.sortPositionStart);
  if (positionDiff !== 0) return positionDiff;

  const endDiff = compareNullableNumbers(a.sortPositionEnd, b.sortPositionEnd);
  if (endDiff !== 0) return endDiff;

  const timeDiff = compareNullableNumbers(a.sortTime, b.sortTime);
  if (timeDiff !== 0) return timeDiff;

  return String(a.id || '').localeCompare(String(b.id || ''));
}

export function compareChapterGroups(a, b) {
  const chapterIndexDiff = compareNullableNumbers(a.sortChapterIndex, b.sortChapterIndex);
  if (chapterIndexDiff !== 0) return chapterIndexDiff;

  const chapterUidDiff = compareNullableNumbers(a.chapterUid, b.chapterUid);
  if (chapterUidDiff !== 0) return chapterUidDiff;

  return String(a.chapterName || '').localeCompare(String(b.chapterName || ''), 'zh-Hans-CN');
}
