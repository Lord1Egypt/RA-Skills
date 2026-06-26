import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import type { LinkCache, LinkCacheEntry, NormalizedSchedule } from "./types.js";

const CACHE_DIR = join(homedir(), ".qiguan-cli");
const LAST_LIST_FILE = join(CACHE_DIR, "last-list.json");

export async function saveLastList(items: NormalizedSchedule[]): Promise<void> {
  const entries: LinkCacheEntry[] = items
    .filter((item): item is NormalizedSchedule & { code: string } => Boolean(item.code))
    .map((item) => ({
      code: item.code,
      date: item.raw.startDay,
      startCampus: item.startCampus,
      toCampus: item.toCampus,
      zhuhaiStation: item.zhuhaiStation,
      lineTime: item.lineTime,
      boardingTime: item.boardingTime,
      fromStation: item.fromStation,
      toStation: item.toStation,
      shiftScheduleId: item.raw.shiftScheduleId,
    }));

  await mkdir(CACHE_DIR, { recursive: true });
  await writeFile(LAST_LIST_FILE, JSON.stringify({ createdAt: new Date().toISOString(), entries }, null, 2), "utf8");
}

export async function loadLastList(): Promise<LinkCache> {
  try {
    const raw = await readFile(LAST_LIST_FILE, "utf8");
    const parsed = JSON.parse(raw) as LinkCache;
    if (!Array.isArray(parsed.entries)) throw new Error("Invalid cache");
    return parsed;
  } catch {
    throw new Error("No qg list cache found. Run qg list first, then use qg link <code>.");
  }
}
