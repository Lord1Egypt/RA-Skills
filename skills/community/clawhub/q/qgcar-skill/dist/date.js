const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const WEEKDAYS = {
    sun: 0,
    sunday: 0,
    mon: 1,
    monday: 1,
    tue: 2,
    tuesday: 2,
    wed: 3,
    wednesday: 3,
    thu: 4,
    thursday: 4,
    fri: 5,
    friday: 5,
    sat: 6,
    saturday: 6,
};
export function resolveTravelDate(flags) {
    const today = startOfToday();
    let date;
    if (flags.today && flags.tomorrow) {
        throw new Error("Use only one of --today or --tomorrow.");
    }
    if (flags.today) {
        date = today;
    }
    else if (flags.tomorrow) {
        date = addDays(today, 1);
    }
    else if (!flags.date) {
        date = today;
    }
    else {
        date = parseDateInput(flags.date, today);
    }
    const diff = diffDays(today, date);
    if (diff < 0 || diff > 7) {
        throw new Error(`Date must be within one week: ${formatDate(today)} to ${formatDate(addDays(today, 7))}.`);
    }
    return formatDate(date);
}
function parseDateInput(input, today) {
    const normalized = input.trim().toLowerCase();
    if (normalized === "today")
        return today;
    if (normalized === "tomorrow")
        return addDays(today, 1);
    if (normalized in WEEKDAYS) {
        const target = WEEKDAYS[normalized];
        const offset = (target - today.getDay() + 7) % 7;
        return addDays(today, offset);
    }
    if (!DATE_RE.test(normalized)) {
        throw new Error("Invalid date. Use --today, --tomorrow, --date YYYY-MM-DD, or --date fri.");
    }
    const [year, month, day] = normalized.split("-").map(Number);
    const date = new Date(year, month - 1, day);
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
        throw new Error(`Invalid date: ${input}`);
    }
    return date;
}
function startOfToday() {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}
function addDays(date, days) {
    const next = new Date(date);
    next.setDate(next.getDate() + days);
    return next;
}
function diffDays(start, end) {
    return Math.round((end.getTime() - start.getTime()) / 86_400_000);
}
export function formatDate(date) {
    const year = date.getFullYear();
    const month = `${date.getMonth() + 1}`.padStart(2, "0");
    const day = `${date.getDate()}`.padStart(2, "0");
    return `${year}-${month}-${day}`;
}
