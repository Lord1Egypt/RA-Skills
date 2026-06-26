#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { fetchLineList } from "./api.js";
import { loadLastList, saveLastList } from "./cache.js";
import { resolveTravelDate } from "./date.js";
import { buildOrderWriteLink } from "./link.js";
import { normalizeSchedule } from "./normalize.js";
import { CAMPUS_LABELS, defaultDestination, parseCampus, parseZhuhaiStation, routeLabel, } from "./routes.js";
import { printScheduleTable } from "./table.js";
const VERSION = "0.1.0";
main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
});
async function main() {
    const args = parseArgs(process.argv.slice(2));
    if (args.command === "help" || args.flags.help) {
        printHelp();
        return;
    }
    if (args.flags.version) {
        console.log(VERSION);
        return;
    }
    if (args.command !== "link" && args.positionals.length > 0) {
        throw new Error(`Unexpected argument "${args.positionals[0]}". Run qg help.`);
    }
    if (args.command === "routes") {
        printRoutes();
        return;
    }
    if (args.command === "list") {
        await listCommand(args.flags);
        return;
    }
    await linkCommand(args.flags, args.positionals);
}
async function listCommand(flags) {
    const date = getDate(flags);
    const start = parseCampus(getString(flags.start), "zhuhai");
    const zhuhaiStation = parseZhuhaiStation(getString(flags.station ?? flags.zhuhai), "zhuhai");
    const targets = getTargets(start, getString(flags.to), Boolean(flags.all));
    const onlyAvailable = Boolean(flags.available);
    const json = Boolean(flags.json);
    const groups = [];
    const cacheItems = [];
    let nextCode = 1;
    for (const to of targets) {
        const data = await fetchLineList({ start, to, zhuhaiStation, date });
        let items = data.carLineList.map((raw) => normalizeSchedule(raw, start, to, zhuhaiStation));
        if (onlyAvailable)
            items = items.filter((item) => item.status === "available");
        items = items.map((item) => ({ ...item, code: String(nextCode++) }));
        cacheItems.push(...items);
        groups.push({ label: routeLabel(start, to, zhuhaiStation), items });
    }
    await saveLastList(cacheItems);
    if (json) {
        console.log(JSON.stringify(groups, null, 2));
        return;
    }
    console.log(`Date: ${date}`);
    for (const group of groups) {
        console.log("");
        console.log(group.label);
        printScheduleTable(group.items);
    }
}
async function linkCommand(flags, positionals) {
    if (positionals.length > 1) {
        throw new Error(`Unexpected extra link arguments: ${positionals.slice(1).join(" ")}. Run qg help.`);
    }
    const code = positionals[0] ?? getString(flags.code);
    if (code) {
        await linkFromCode(code, flags);
        return;
    }
    const time = getString(flags.time);
    if (!time) {
        throw new Error("Missing --time HH:mm or code. Example: qg link 3, or qg link --start zhuhai --to south --time 16:00");
    }
    validateTime(time);
    const date = getDate(flags);
    const start = parseCampus(getString(flags.start), "zhuhai");
    const zhuhaiStation = parseZhuhaiStation(getString(flags.station ?? flags.zhuhai), "zhuhai");
    const to = parseCampus(getString(flags.to), defaultDestination(start));
    validateRoute(start, to);
    const data = await fetchLineList({ start, to, zhuhaiStation, date });
    const items = data.carLineList
        .map((raw) => normalizeSchedule(raw, start, to, zhuhaiStation))
        .filter((item) => item.lineTime === time || item.boardingTime === time);
    if (items.length === 0) {
        throw new Error(`No schedule matched ${time}. Run qg list --start ${start} --to ${to} --date ${date}.`);
    }
    const available = items.find((item) => item.status === "available") ?? items[0];
    if (available.status !== "available") {
        console.error(`Warning: matched schedule is ${available.status}.`);
    }
    const link = buildOrderWriteLink(available.raw);
    if (Boolean(flags.copy)) {
        copyToClipboard(link);
        console.log("Copied order link to clipboard.");
    }
    console.log(`${routeLabel(start, to, zhuhaiStation)} ${date}`);
    console.log(`Line ${available.lineTime}, board ${available.boardingTime}, arrive ${available.arrivalTime}, ${available.fromStation} -> ${available.toStation}`);
    console.log(link);
}
async function linkFromCode(code, flags) {
    if (!/^\d+$/.test(code)) {
        throw new Error(`Invalid link code "${code}". Run qg list, then use a numeric code like qg link 3.`);
    }
    const cache = await loadLastList();
    const entry = cache.entries.find((item) => item.code === code);
    if (!entry) {
        throw new Error(`Code ${code} was not found in the last qg list result. Run qg list again.`);
    }
    const data = await fetchLineList({
        start: entry.startCampus,
        to: entry.toCampus,
        zhuhaiStation: entry.zhuhaiStation,
        date: entry.date,
    });
    const fresh = data.carLineList.find((raw) => {
        const item = normalizeSchedule(raw, entry.startCampus, entry.toCampus, entry.zhuhaiStation);
        return (raw.shiftScheduleId === entry.shiftScheduleId &&
            item.lineTime === entry.lineTime &&
            item.boardingTime === entry.boardingTime &&
            item.fromStation === entry.fromStation &&
            item.toStation === entry.toStation);
    });
    if (!fresh) {
        throw new Error(`Code ${code} no longer matches an available schedule. Run qg list again.`);
    }
    const item = normalizeSchedule(fresh, entry.startCampus, entry.toCampus, entry.zhuhaiStation);
    if (item.status !== "available") {
        console.error(`Warning: code ${code} is now ${item.status}.`);
    }
    const link = buildOrderWriteLink(fresh);
    if (Boolean(flags.copy)) {
        copyToClipboard(link);
        console.log("Copied order link to clipboard.");
    }
    console.log(`${routeLabel(entry.startCampus, entry.toCampus, entry.zhuhaiStation)} ${entry.date}`);
    console.log(`Code ${code}: Line ${item.lineTime}, board ${item.boardingTime}, arrive ${item.arrivalTime}, ${item.fromStation} -> ${item.toStation}`);
    console.log(link);
}
function getTargets(start, toFlag, all) {
    if (toFlag) {
        const to = parseCampus(toFlag, defaultDestination(start));
        validateRoute(start, to);
        return [to];
    }
    if (all && start === "zhuhai")
        return ["south", "east"];
    return [defaultDestination(start)];
}
function validateRoute(start, to) {
    if (to === start)
        throw new Error("--start and --to cannot be the same campus.");
    if (start !== "zhuhai" && to !== "zhuhai") {
        throw new Error("Unsupported route. One side must be zhuhai.");
    }
}
function getDate(flags) {
    return resolveTravelDate({
        today: Boolean(flags.today),
        tomorrow: Boolean(flags.tomorrow),
        date: getString(flags.date),
    });
}
function parseArgs(argv) {
    const flags = {};
    let command = "list";
    const positionals = [];
    const booleanFlags = new Set(["all", "available", "copy", "help", "json", "today", "tomorrow", "version"]);
    let index = 0;
    if (argv[0] && !argv[0].startsWith("-")) {
        const first = argv[0];
        if (first === "list" || first === "link" || first === "routes" || first === "help") {
            command = first;
            index = 1;
        }
        else {
            throw new Error(`Unknown command "${first}". Run qg help.`);
        }
    }
    while (index < argv.length) {
        const arg = argv[index];
        if (arg === "-h" || arg === "--help") {
            flags.help = true;
            index += 1;
            continue;
        }
        if (arg === "-v" || arg === "--version") {
            flags.version = true;
            index += 1;
            continue;
        }
        if (!arg.startsWith("--")) {
            positionals.push(arg);
            index += 1;
            continue;
        }
        const [rawKey, rawValue] = arg.slice(2).split("=", 2);
        const key = camelCase(rawKey);
        if (booleanFlags.has(key)) {
            flags[key] = true;
            index += 1;
            continue;
        }
        if (rawValue !== undefined) {
            flags[key] = rawValue;
            index += 1;
            continue;
        }
        const next = argv[index + 1];
        if (next && !next.startsWith("--")) {
            flags[key] = next;
            index += 2;
        }
        else {
            flags[key] = true;
            index += 1;
        }
    }
    return { command, flags, positionals };
}
function getString(value) {
    return typeof value === "string" ? value : undefined;
}
function camelCase(value) {
    return value.replace(/-([a-z])/g, (_, char) => char.toUpperCase());
}
function copyToClipboard(value) {
    const command = process.platform === "darwin" ? "pbcopy" : process.platform === "win32" ? "clip" : "xclip";
    const args = process.platform === "linux" ? ["-selection", "clipboard"] : [];
    const result = spawnSync(command, args, { input: value });
    if (result.error || result.status !== 0) {
        throw new Error("Failed to copy to clipboard. Install xclip on Linux or copy the printed link manually.");
    }
}
function validateTime(value) {
    const match = /^(\d{2}):(\d{2})$/.exec(value);
    if (!match) {
        throw new Error(`Invalid --time "${value}". Use HH:mm, for example 16:00.`);
    }
    const hour = Number(match[1]);
    const minute = Number(match[2]);
    if (hour > 23 || minute > 59) {
        throw new Error(`Invalid --time "${value}". Use a 24-hour time between 00:00 and 23:59.`);
    }
}
function printRoutes() {
    console.log("Campuses:");
    for (const [key, label] of Object.entries(CAMPUS_LABELS)) {
        console.log(`  ${key}: ${label}`);
    }
    console.log("");
    console.log("Zhuhai station keys:");
    console.log("  zhuhai: 珠海中大岐关服务点");
    console.log("  boya: 博雅苑");
    console.log("  fifth: 中大五院正门");
}
function printHelp() {
    console.log(`qg - Qiguan bus helper

Usage:
  qg list --today
  qg --start zhuhai
  qg list --start south --tomorrow
  qg list --start zhuhai --to east --date 2026-04-10
  qg link 3
  qg link --start zhuhai --to south --time 16:00 --copy
  qg routes
  qg --help

Commands:
  list      List schedules. This is the default command.
  link      Generate a WeChat BusOrderWrite link for a schedule.
  routes    Show supported campus and station keys.
  help      Show this help.

Options:
  --start <campus>       zhuhai, south, or east. Default: zhuhai.
  --to <campus>          Optional destination. Default: south if start=zhuhai, otherwise zhuhai.
  --station <station>    Zhuhai station: zhuhai, boya, or fifth. Default: zhuhai.
  --today                Use today.
  --tomorrow             Use tomorrow.
  --date <date>          YYYY-MM-DD, today, tomorrow, or weekday like fri. Must be within one week.
  --time <HH:mm>         Required for link. Matches either line time or boarding time.
  --code <code>          Generate a link from the last qg list result.
  --available            Only show available schedules in list.
  --all                  With --start zhuhai, list both south and east destinations.
  --json                 Output list data as JSON.
  --copy                 Copy generated link to clipboard.
  -h, --help             Show this help.
  -v, --version          Show version.
`);
}
