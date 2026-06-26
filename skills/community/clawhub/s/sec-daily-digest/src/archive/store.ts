import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { normalizeUrl } from "../articles/normalize";
import { getStateRoot } from "../config/paths";

export interface ArchiveEntry {
  title: string;
  link: string;
  date: string;
}

function archiveDir(env: NodeJS.ProcessEnv): string {
  return path.join(getStateRoot(env), "archive");
}

function dateFromFilename(filename: string): Date | null {
  const match = filename.match(/^(\d{4}-\d{2}-\d{2})\.json$/);
  if (!match) return null;
  return new Date(match[1]!);
}

export async function readRecentArchive(env: NodeJS.ProcessEnv, days = 7): Promise<Set<string>> {
  const dir = archiveDir(env);
  const cutoff = new Date(Date.now() - days * 24 * 3_600_000);
  const seen = new Set<string>();

  try {
    const files = await readdir(dir);
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      const fileDate = dateFromFilename(file);
      if (!fileDate || fileDate < cutoff) continue;

      try {
        const content = await readFile(path.join(dir, file), "utf8");
        const entries = JSON.parse(content) as ArchiveEntry[];
        for (const entry of entries) {
          seen.add(normalizeUrl(entry.link));
        }
      } catch {
        // corrupt file; skip
      }
    }
  } catch {
    // directory doesn't exist yet
  }

  return seen;
}

export async function writeArchiveEntry(articles: ArchiveEntry[], date: string, env: NodeJS.ProcessEnv): Promise<void> {
  const dir = archiveDir(env);
  await mkdir(dir, { recursive: true });
  const filePath = path.join(dir, `${date}.json`);
  await writeFile(filePath, JSON.stringify(articles, null, 2), "utf8");
}

export async function cleanOldArchive(env: NodeJS.ProcessEnv, maxAgeDays = 90): Promise<void> {
  const dir = archiveDir(env);
  const cutoff = new Date(Date.now() - maxAgeDays * 24 * 3_600_000);

  try {
    const files = await readdir(dir);
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      const fileDate = dateFromFilename(file);
      if (fileDate && fileDate < cutoff) {
        await rm(path.join(dir, file), { force: true });
      }
    }
  } catch {
    // directory doesn't exist; nothing to clean
  }
}
