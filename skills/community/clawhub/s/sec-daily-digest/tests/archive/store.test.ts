import { describe, expect, test } from "bun:test";
import { mkdtemp, rm, mkdir, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { readRecentArchive, writeArchiveEntry, cleanOldArchive } from "../../src/archive/store";

describe("archive store", () => {
  test("write/read cycle returns correct URLs", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "archive-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    await writeArchiveEntry(
      [
        { title: "Article A", link: "https://example.com/a", date: "2026-03-01" },
        { title: "Article B", link: "https://example.com/b", date: "2026-03-01" },
      ],
      "2026-03-01",
      env,
    );

    const seen = await readRecentArchive(env, 30);
    expect(seen.has("https://example.com/a")).toBe(true);
    expect(seen.has("https://example.com/b")).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("7-day boundary: excludes entries older than N days", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "archive-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const archiveDir = path.join(tempDir, "archive");
    await mkdir(archiveDir, { recursive: true });

    // Write old entry (10 days ago)
    const oldDate = new Date(Date.now() - 10 * 24 * 3600_000);
    const oldDateStr = oldDate.toISOString().slice(0, 10);
    await writeFile(
      path.join(archiveDir, `${oldDateStr}.json`),
      JSON.stringify([{ title: "Old", link: "https://old.com/a", date: oldDateStr }]),
    );

    // Write recent entry (1 day ago)
    const recentDate = new Date(Date.now() - 1 * 24 * 3600_000);
    const recentDateStr = recentDate.toISOString().slice(0, 10);
    await writeFile(
      path.join(archiveDir, `${recentDateStr}.json`),
      JSON.stringify([{ title: "Recent", link: "https://recent.com/b", date: recentDateStr }]),
    );

    const seen = await readRecentArchive(env, 7);
    expect(seen.has("https://old.com/a")).toBe(false);
    expect(seen.has("https://recent.com/b")).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("cleanOldArchive removes files older than maxAgeDays", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "archive-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const archiveDir = path.join(tempDir, "archive");
    await mkdir(archiveDir, { recursive: true });

    // Write very old entry (100 days ago)
    const veryOldDate = new Date(Date.now() - 100 * 24 * 3600_000);
    const veryOldDateStr = veryOldDate.toISOString().slice(0, 10);
    await writeFile(path.join(archiveDir, `${veryOldDateStr}.json`), "[]");

    // Write recent entry
    const recentDateStr = new Date().toISOString().slice(0, 10);
    await writeFile(path.join(archiveDir, `${recentDateStr}.json`), "[]");

    await cleanOldArchive(env, 90);

    // Old file should be gone
    const seen = await readRecentArchive(env, 200);
    // After clean, the old file is removed; reading archive should not find old URLs
    // The recent file still exists
    const { readdir } = await import("node:fs/promises");
    const files = await readdir(archiveDir);
    expect(files.includes(`${veryOldDateStr}.json`)).toBe(false);
    expect(files.includes(`${recentDateStr}.json`)).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("returns empty set when archive dir does not exist", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "archive-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const seen = await readRecentArchive(env, 7);
    expect(seen.size).toBe(0);

    await rm(tempDir, { recursive: true, force: true });
  });
});
