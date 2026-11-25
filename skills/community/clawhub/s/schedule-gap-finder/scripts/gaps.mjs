#!/usr/bin/env node
// schedule-gap-finder: find schedule conflicts and free time slots for one day.
// No dependencies, no network, reads only stdin or the given .ics file.
//
// usage:
//   node gaps.mjs [--day YYYY-MM-DD] [--tz IANA] [--start HH:MM] [--end HH:MM] [--min N] [--json] < events.json
//   node gaps.mjs --ics calendar.ics [same options]
// events.json: [{"title": "...", "start": "2026-11-18T09:00:00-08:00", "end": "...", "allDay": false}, ...]
//              (or {"events": [...]})
import { readFileSync } from "node:fs";

export function parseArgs(argv) {
  const o = { day: null, tz: process.env.TZ || "UTC", start: "08:00", end: "18:00", min: 30, json: false, ics: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i], v = argv[i + 1];
    if (a === "--day") { o.day = v; i++; }
    else if (a === "--tz") { o.tz = v; i++; }
    else if (a === "--start") { o.start = v; i++; }
    else if (a === "--end") { o.end = v; i++; }
    else if (a === "--min") { o.min = Number(v); i++; }
    else if (a === "--ics") { o.ics = v; i++; }
    else if (a === "--json") o.json = true;
    else if (a === "-h" || a === "--help") o.help = true;
    else throw new Error(`unknown argument: ${a}`);
  }
  if (o.day && !/^\d{4}-\d{2}-\d{2}$/.test(o.day)) throw new Error("--day must be YYYY-MM-DD");
  for (const k of ["start", "end"]) if (!/^\d{2}:\d{2}$/.test(o[k])) throw new Error(`--${k} must be HH:MM`);
  if (!Number.isFinite(o.min) || o.min <= 0) throw new Error("--min must be a positive number of minutes");
  new Intl.DateTimeFormat("en-US", { timeZone: o.tz }); // throws RangeError on a bad timezone
  return o;
}

// ---------------------------------------------------------------- time zones (Intl only)
export function tzOffsetMinutes(tz, at) {
  const name = new Intl.DateTimeFormat("en-US", { timeZone: tz, timeZoneName: "longOffset" })
    .formatToParts(at).find((p) => p.type === "timeZoneName")?.value ?? "GMT";
  const m = /GMT([+-])(\d{2}):?(\d{2})?/.exec(name);
  return m ? (m[1] === "-" ? -1 : 1) * (Number(m[2]) * 60 + Number(m[3] ?? 0)) : 0;
}
/** UTC instant of local wall-clock `HH:MM` on `ymd` in `tz` (DST-safe). */
export function zoned(ymd, hhmm, tz) {
  const guess = new Date(`${ymd}T${hhmm}:00Z`);
  const off = tzOffsetMinutes(tz, guess);
  const t = new Date(guess.getTime() - off * 60000);
  const off2 = tzOffsetMinutes(tz, t);
  return off2 === off ? t : new Date(guess.getTime() - off2 * 60000);
}
export const todayIn = (tz, now = new Date()) =>
  new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit" }).format(now);
const hm = (d, tz) => new Intl.DateTimeFormat("en-US", { timeZone: tz, hour: "numeric", minute: "2-digit" }).format(d);

// ---------------------------------------------------------------- input
export function fromJson(text) {
  const data = JSON.parse(text);
  const list = Array.isArray(data) ? data : data.events;
  if (!Array.isArray(list)) throw new Error("expected a JSON array of events or {\"events\": [...]}");
  return list.map((e, i) => {
    const allDay = Boolean(e.allDay);
    const start = new Date(e.start), end = new Date(e.end ?? e.start);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) throw new Error(`event ${i}: invalid start/end`);
    return { title: String(e.title ?? e.summary ?? "(untitled)").slice(0, 200), start, end, allDay };
  });
}

/** Minimal RFC 5545 reader: VEVENT SUMMARY/DTSTART/DTEND (UTC "Z", TZID local, or DATE all-day). */
export function fromIcs(text, tz) {
  const lines = text.replace(/\r?\n[ \t]/g, "").split(/\r?\n/); // unfold continuation lines
  const out = [];
  let cur = null;
  const parseDt = (prop, value) => {
    const isDate = /VALUE=DATE(?!-)/.test(prop) || /^\d{8}$/.test(value);
    const zone = /TZID=([^;:]+)/.exec(prop)?.[1] ?? tz;
    const m = /^(\d{4})(\d{2})(\d{2})(?:T(\d{2})(\d{2})(\d{2})?(Z)?)?$/.exec(value.trim());
    if (!m) return null;
    const ymd = `${m[1]}-${m[2]}-${m[3]}`;
    if (isDate) return { date: zoned(ymd, "00:00", tz), allDay: true };
    if (m[7] === "Z") return { date: new Date(`${ymd}T${m[4]}:${m[5]}:${m[6] ?? "00"}Z`), allDay: false };
    return { date: zoned(ymd, `${m[4]}:${m[5]}`, zone), allDay: false };
  };
  for (const raw of lines) {
    if (raw === "BEGIN:VEVENT") cur = {};
    else if (raw === "END:VEVENT" && cur) {
      if (cur.start) out.push({ title: cur.title ?? "(untitled)", start: cur.start.date,
        end: cur.end?.date ?? new Date(cur.start.date.getTime() + (cur.start.allDay ? 86400000 : 3600000)),
        allDay: cur.start.allDay });
      cur = null;
    } else if (cur) {
      const i = raw.indexOf(":");
      if (i < 0) continue;
      const prop = raw.slice(0, i), value = raw.slice(i + 1);
      if (prop.startsWith("SUMMARY")) cur.title = value.replace(/\\,/g, ",").replace(/\\n/gi, " ").slice(0, 200);
      else if (prop.startsWith("DTSTART")) cur.start = parseDt(prop, value);
      else if (prop.startsWith("DTEND")) cur.end = parseDt(prop, value);
    }
  }
  return out;
}

// ---------------------------------------------------------------- analysis
export function analyze(events, { day, tz, start, end, min }) {
  const winStart = zoned(day, start, tz), winEnd = zoned(day, end, tz);
  const dayStart = zoned(day, "00:00", tz), dayEnd = new Date(dayStart.getTime() + 86400000);
  const today = events.filter((e) => e.end > dayStart && e.start < dayEnd);
  const allDay = today.filter((e) => e.allDay);
  const timed = today.filter((e) => !e.allDay).sort((a, b) => a.start - b.start);

  const conflicts = [];
  for (let i = 0; i < timed.length; i++)
    for (let j = i + 1; j < timed.length && timed[j].start < timed[i].end; j++) {
      const overlap = (Math.min(timed[i].end, timed[j].end) - timed[j].start) / 60000;
      conflicts.push({ a: timed[i].title, b: timed[j].title, start: timed[j].start,
        end: new Date(Math.min(timed[i].end, timed[j].end)), minutes: overlap });
    }

  const gaps = [];
  let cursor = winStart.getTime();
  for (const e of timed) {
    const s = Math.max(e.start.getTime(), winStart.getTime()), f = Math.min(e.end.getTime(), winEnd.getTime());
    if (f <= winStart.getTime() || s >= winEnd.getTime()) continue;
    if (s - cursor >= min * 60000) gaps.push({ start: new Date(cursor), end: new Date(s), minutes: (s - cursor) / 60000 });
    cursor = Math.max(cursor, f);
  }
  if (winEnd.getTime() - cursor >= min * 60000)
    gaps.push({ start: new Date(cursor), end: winEnd, minutes: (winEnd.getTime() - cursor) / 60000 });

  return { day, tz, window: { start, end }, minMinutes: min, events: timed, allDay, conflicts, gaps,
    longestGap: gaps.reduce((b, g) => (!b || g.minutes > b.minutes ? g : b), null) };
}

export function render(r) {
  const tz = r.tz, L = [];
  L.push(`Schedule for ${r.day} (${tz}), working window ${r.window.start}-${r.window.end}`);
  for (const e of r.allDay) L.push(`- all day: ${e.title}`);
  for (const e of r.events) L.push(`- ${hm(e.start, tz)}-${hm(e.end, tz)}: ${e.title}`);
  if (!r.events.length && !r.allDay.length) L.push("- (no events)");
  L.push(r.conflicts.length
    ? `Conflicts (${r.conflicts.length}):\n` + r.conflicts.map((c) => `- "${c.a}" overlaps "${c.b}" ${hm(c.start, tz)}-${hm(c.end, tz)} (${c.minutes} min)`).join("\n")
    : "Conflicts: none");
  L.push(r.gaps.length
    ? `Free slots >= ${r.minMinutes} min:\n` + r.gaps.map((g) => `- ${hm(g.start, tz)}-${hm(g.end, tz)} (${g.minutes} min)`).join("\n")
    : `Free slots >= ${r.minMinutes} min: none`);
  if (r.longestGap) L.push(`Best block for focused work: ${hm(r.longestGap.start, tz)}-${hm(r.longestGap.end, tz)} (${r.longestGap.minutes} min)`);
  return L.join("\n");
}

// ---------------------------------------------------------------- CLI
const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/").split("/").pop());
if (isMain) {
  try {
    const o = parseArgs(process.argv.slice(2));
    if (o.help) { console.log("usage: node gaps.mjs [--day YYYY-MM-DD] [--tz IANA] [--start HH:MM] [--end HH:MM] [--min N] [--json] [--ics file] < events.json"); process.exit(0); }
    o.day ??= todayIn(o.tz);
    const events = o.ics ? fromIcs(readFileSync(o.ics, "utf8"), o.tz) : fromJson(readFileSync(0, "utf8"));
    const r = analyze(events, o);
    console.log(o.json ? JSON.stringify(r, null, 2) : render(r));
  } catch (e) {
    console.error(`schedule-gap-finder: ${e.message}`);
    process.exit(2);
  }
}
