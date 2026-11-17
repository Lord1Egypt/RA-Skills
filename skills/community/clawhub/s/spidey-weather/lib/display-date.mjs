// Date-only values are calendar dates, not UTC instants to shift into Pacific.
export function formatDisplayDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return 'Date unavailable';
  const date = new Date(`${value}T12:00:00Z`);
  if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== value) return 'Date unavailable';
  return new Intl.DateTimeFormat('en-US', { timeZone: 'UTC', month: 'long', day: 'numeric', year: 'numeric' }).format(date);
}
export function formatDisplayInstant(value, timezone = 'America/Los_Angeles') {
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) return 'Date unavailable';
  return new Intl.DateTimeFormat('en-US', { timeZone: timezone, month: 'long', day: 'numeric', year: 'numeric' }).format(date);
}

// Compatibility for older reminder text. Accept only unambiguous named months.
export function formatReminderDate(value) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return formatDisplayDate(value);
  const months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
  const legacy = /^(\d{1,2})-([A-Za-z]{3})-(\d{4})$/.exec(value);
  const display = /^([A-Za-z]+) (\d{1,2}), (\d{4})$/.exec(value);
  if (!legacy && !display) return 'Date unavailable';
  const name = (legacy ? legacy[2] : display[1]).toLowerCase();
  const month = months.findIndex(item => legacy ? item.slice(0, 3) === name : item === name) + 1;
  const day = legacy ? legacy[1] : display[2];
  const year = legacy ? legacy[3] : display[3];
  return formatDisplayDate(`${year}-${String(month).padStart(2, '0')}-${day.padStart(2, '0')}`);
}
