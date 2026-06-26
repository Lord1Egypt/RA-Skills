#!/usr/bin/env node
/**
 * Report date utility for daily-report-generator skill.
 * Calculates date ranges for daily, weekly, and custom reports.
 *
 * Usage:
 *   node report_dates.js today
 *   node report_dates.js yesterday
 *   node report_dates.js week
 *   node report_dates.js last7
 *   node report_dates.js display [YYYY-MM-DD]
 */
"use strict";

const fmt = (d) => d.toISOString().split("T")[0];

function today() {
  return fmt(new Date());
}

function yesterday() {
  return fmt(new Date(Date.now() - 864e5));
}

function weekRange() {
  const now = new Date();
  const day = now.getDay(); // 0=Sun
  const monday = new Date(now);
  monday.setDate(now.getDate() - ((day + 6) % 7));
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  return [fmt(monday), fmt(sunday)];
}

function lastNDays(n) {
  const now = new Date();
  return Array.from({ length: n }, (_, i) => {
    const d = new Date(now);
    d.setDate(now.getDate() - (n - 1 - i));
    return fmt(d);
  });
}

const ZH_WEEK = ["一", "二", "三", "四", "五", "六", "日"];
const EN_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function formatDateDisplay(dateStr, lang = "zh") {
  const d = new Date(dateStr + "T00:00:00");
  const wd = d.getDay() === 0 ? 6 : d.getDay() - 1; // 0=Mon..6=Sun
  if (lang === "zh") {
    return `${d.getMonth() + 1}月${d.getDate()}日 周${ZH_WEEK[wd]}`;
  }
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  return `${months[d.getMonth()]} ${d.getDate()} ${EN_WEEK[wd]}`;
}

// CLI
const cmd = process.argv[2] || "today";
switch (cmd) {
  case "today":
    console.log(today());
    break;
  case "yesterday":
    console.log(yesterday());
    break;
  case "week":
    console.log(weekRange().join(" ~ "));
    break;
  case "last7":
    console.log(lastNDays(7).join("\n"));
    break;
  case "last30":
    console.log(lastNDays(30).join("\n"));
    break;
  case "display":
    console.log(formatDateDisplay(process.argv[3] || today()));
    break;
  default:
    console.log(`Usage: node report_dates.js [today|yesterday|week|last7|last30|display <date>]`);
    process.exit(1);
}
