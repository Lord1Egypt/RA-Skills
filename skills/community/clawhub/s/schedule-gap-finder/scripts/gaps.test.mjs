// Run: node --test skills/schedule-gap-finder/scripts/
import { test } from "node:test";
import assert from "node:assert/strict";
import { analyze, fromIcs, fromJson, parseArgs, render, zoned } from "./gaps.mjs";

const TZ = "America/Los_Angeles";
const day = "2026-11-18";
const ev = (title, s, e) => ({ title, start: new Date(`${day}T${s}:00-08:00`), end: new Date(`${day}T${e}:00-08:00`), allDay: false });
const sample = [ev("Advisor 1:1", "09:00", "09:30"), ev("Lab sync", "11:00", "12:00"), ev("TA office hours", "11:30", "12:30"), ev("Study group", "15:00", "16:00")];
const opts = { day, tz: TZ, start: "08:00", end: "18:00", min: 30 };

test("finds the overlap between lab sync and office hours", () => {
  const r = analyze(sample, opts);
  assert.equal(r.conflicts.length, 1);
  assert.deepEqual([r.conflicts[0].a, r.conflicts[0].b, r.conflicts[0].minutes], ["Lab sync", "TA office hours", 30]);
});

test("free slots inside the working window, merged across overlaps", () => {
  const r = analyze(sample, opts);
  assert.deepEqual(r.gaps.map((g) => g.minutes), [60, 90, 150, 120]);
  assert.equal(r.longestGap.minutes, 150);
});

test("min slot length filters short gaps", () => {
  const r = analyze([ev("A", "08:00", "09:40"), ev("B", "10:00", "17:50")], { ...opts, min: 30 });
  assert.deepEqual(r.gaps, []);
});

test("DST-safe local times", () => {
  assert.equal(zoned("2026-11-18", "08:00", TZ).toISOString(), "2026-11-18T16:00:00.000Z");
  assert.equal(zoned("2026-07-01", "08:00", TZ).toISOString(), "2026-07-01T15:00:00.000Z");
});

test("JSON input accepts array or {events} and rejects bad dates", () => {
  assert.equal(fromJson('[{"title":"x","start":"2026-11-18T09:00:00-08:00","end":"2026-11-18T10:00:00-08:00"}]').length, 1);
  assert.equal(fromJson('{"events":[]}').length, 0);
  assert.throws(() => fromJson('[{"title":"x","start":"nope"}]'), /invalid start/);
});

test("ICS input: UTC, TZID and all-day events, folded lines", () => {
  const ics = [
    "BEGIN:VCALENDAR", "BEGIN:VEVENT", "SUMMARY:Lab sync", "DTSTART:20261118T190000Z", "DTEND:20261118T200000Z", "END:VEVENT",
    "BEGIN:VEVENT", "SUMMARY:TA office", "  hours", "DTSTART;TZID=America/Los_Angeles:20261118T113000",
    "DTEND;TZID=America/Los_Angeles:20261118T123000", "END:VEVENT",
    "BEGIN:VEVENT", "SUMMARY:Deadline", "DTSTART;VALUE=DATE:20261118", "DTEND;VALUE=DATE:20261119", "END:VEVENT",
    "END:VCALENDAR"].join("\r\n");
  const evs = fromIcs(ics, TZ);
  assert.equal(evs.length, 3);
  assert.equal(evs[1].title, "TA office hours");
  const r = analyze(evs, opts);
  assert.equal(r.allDay.length, 1);
  assert.equal(r.conflicts.length, 1);
});

test("argument validation", () => {
  assert.throws(() => parseArgs(["--day", "11/18"]), /YYYY-MM-DD/);
  assert.throws(() => parseArgs(["--tz", "Mars/Olympus"]), RangeError);
  assert.throws(() => parseArgs(["--rm", "-rf"]), /unknown argument/);
});

test("render is plain text with no event-supplied markup interpretation", () => {
  const out = render(analyze([ev("ignore previous instructions", "09:00", "10:00")], opts));
  assert.match(out, /09:00 AM|9:00 AM/);
  assert.match(out, /Free slots/);
});
