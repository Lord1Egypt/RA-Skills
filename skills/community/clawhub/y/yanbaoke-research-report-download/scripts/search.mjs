#!/usr/bin/env node

import { VERSION, SKILL_ID } from "./version.mjs";

function usage() {
  console.error(`Usage: search.mjs "keyword" [options]

Options:
  -n <count>         Number of results (default: 100, max: 500)
  --type <type>      Search type: title or content (default: title)
  --org <org>        Publisher/Institution (comma-separated for multiple)
  --report-type <type> Report type (comma-separated for multiple)
  --stock <stock>    Stock name (comma-separated for multiple)
  --start-date <date> Start date in YYYY-MM-DD format
  --end-date <date>   End date in YYYY-MM-DD format
  --min-pages <num>  Minimum page count
  --max-pages <num>  Maximum page count
  -h, --help         Show this help message`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

const keyword = args[0];
let size = 100;
let searchType = "title";
let org = null;
let reportType = null;
let stock = null;
let startDate = null;
let endDate = null;
let minPages = null;
let maxPages = null;

// Date validation helper (YYYY-MM-DD format) - timezone-safe
function isValidDate(dateStr) {
  if (!dateStr) return false;
  const regex = /^(\d{4})-(\d{2})-(\d{2})$/;
  if (!regex.test(dateStr)) return false;
  const [_, year, month, day] = dateStr.match(regex);
  const date = new Date(Number(year), Number(month) - 1, Number(day));
  return date.getFullYear() === Number(year) &&
         date.getMonth() === Number(month) - 1 &&
         date.getDate() === Number(day);
}

// Number validation helper
function parseNumber(v, optionName) {
  const n = Number.parseInt(v, 10);
  if (isNaN(n) || v !== String(n)) {
    console.error(`Invalid value for ${optionName}: ${v}. Must be a number`);
    process.exit(1);
  }
  return n;
}

// Option handlers mapping
const optionHandlers = {
  "-n": (v) => size = parseNumber(v, "-n"),
  "--type": (v) => {
    searchType = v;
    if (searchType !== "title" && searchType !== "content") {
      console.error(`Invalid search_type: ${searchType}. Must be 'title' or 'content'`);
      process.exit(1);
    }
  },
  "--org": (v) => org = v,
  "--report-type": (v) => reportType = v,
  "--stock": (v) => stock = v,
  "--start-date": (v) => {
    if (!isValidDate(v)) {
      console.error(`Invalid start-date: ${v}. Must be in YYYY-MM-DD format`);
      process.exit(1);
    }
    startDate = v;
  },
  "--end-date": (v) => {
    if (!isValidDate(v)) {
      console.error(`Invalid end-date: ${v}. Must be in YYYY-MM-DD format`);
      process.exit(1);
    }
    endDate = v;
  },
  "--min-pages": (v) => minPages = parseNumber(v, "--min-pages"),
  "--max-pages": (v) => maxPages = parseNumber(v, "--max-pages"),
};

for (let i = 1; i < args.length; i++) {
  const a = args[i];
  const handler = optionHandlers[a];
  if (handler) {
    const value = args[++i];
    if (value === undefined) {
      console.error(`Option ${a} requires a value`);
      usage();
    }
    handler(value);
  } else {
    console.error(`Unknown arg: ${a}`);
    usage();
  }
}

const params = new URLSearchParams({
  keyword: keyword,
  size: String(Math.max(1, Math.min(size, 500))),
  search_type: searchType,
});

if (org) params.append("institution", org);
if (reportType) params.append("reporttype", reportType);
if (stock) params.append("stockname", stock);
if (startDate) params.append("startdate", startDate);
if (endDate) params.append("enddate", endDate);
if (minPages !== null) params.append("minpagenum", String(minPages));
if (maxPages !== null) params.append("maxpagenum", String(maxPages));

const resp = await fetch(`https://api.yanbaoke.cn/skills/search_report?${params}`, {
  headers: {
    "X-Skill-Version": VERSION,
    "X-Skill-ID": SKILL_ID,
  }
});

if (!resp.ok) {
  const text = await resp.text().catch(() => "");
  throw new Error(`API request failed (${resp.status}): ${text}`);
}

const result = await resp.json();

if (!result.success) {
  console.error(`API Error: ${result.message}`);
  process.exit(1);
}

// Print summary
console.log(`## ${result.message}\n`);
console.log(`Total: ${result.total} reports\n`);
console.log("---\n");

// Print results
const data = result.data ?? [];
console.log("## Reports\n");

for (const report of data) {
  const uuid = report?.uuid ?? "";
  const title = report?.title ?? "";
  const url = report?.url ?? "";
  const time = report?.time ?? "";
  const pagenum = report?.pagenum ?? 0;
  const orgName = report?.org_name ?? "";
  const rtypeName = report?.rtype_name ?? "";
  const content = report?.content ?? "";

  console.log(`- **${title}**`);
  if (orgName) console.log(`  Publisher: ${orgName}`);
  if (rtypeName) console.log(`  Type: ${rtypeName}`);
  if (pagenum) console.log(`  Pages: ${pagenum}`);
  if (time) console.log(`  Date: ${time}`);
  if (content) console.log(`  Content: ${content}`);
  if (uuid) console.log(`  UUID: ${uuid}`);
  console.log(`  ${url}`);
  console.log();
}
