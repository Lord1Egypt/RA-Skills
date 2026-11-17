export function validateExpectedNotes(expected) {
  if (!expected || Array.isArray(expected) || typeof expected !== 'object') throw new Error('invalid_arguments: notes must map YYYY-MM-DD dates to arrays of {text,time?}');
  for (const [date, notes] of Object.entries(expected)) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !Array.isArray(notes) || notes.some(note => !note || typeof note.text !== 'string' || !note.text.trim() || (note.time !== undefined && typeof note.time !== 'string'))) throw new Error(`invalid_arguments: invalid expected notes for ${date}`);
  }
  return expected;
}
export function auditDayNotes(days, expected) {
  validateExpectedNotes(expected);
  const key = note => JSON.stringify([String(note.text || '').trim(), String(note.time || '').trim()]);
  return Object.entries(expected).map(([date, wanted]) => {
    const day = days.find(day => day.date === date);
    const remaining = [...(Array.isArray(day?.notes) ? day.notes : day?.notes_items || [])];
    const missing = wanted.filter(note => { const index = remaining.findIndex(actual => key(actual) === key(note)); if (index < 0) return true; remaining.splice(index, 1); return false; });
    return { date, dayId: day?.id ?? null, missing, unexpected: remaining, ok: !!day && !missing.length && !remaining.length };
  });
}
