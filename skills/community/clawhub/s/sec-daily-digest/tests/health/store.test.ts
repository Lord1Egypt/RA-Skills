import { describe, expect, test } from "bun:test";
import { mkdtemp, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {
  loadHealthStore,
  saveHealthStore,
  recordSourceResult,
  getUnhealthySources,
  formatHealthWarnings,
} from "../../src/health/store";

describe("health store", () => {
  test("load returns empty object when file missing", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "health-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const store = await loadHealthStore(env);
    expect(Object.keys(store)).toHaveLength(0);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("save and reload health store", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "health-test-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const store = await loadHealthStore(env);
    recordSourceResult(store, "feed-a", "Feed A", true);
    await saveHealthStore(store, env);

    const reloaded = await loadHealthStore(env);
    expect(reloaded["feed-a"]?.name).toBe("Feed A");
    expect(reloaded["feed-a"]?.checks).toHaveLength(1);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("7-day pruning: old checks are removed", () => {
    const store = {};
    const now = Date.now();
    const eightDaysAgo = now - 8 * 24 * 3600_000;

    recordSourceResult(store, "src", "Source", false, eightDaysAgo);
    recordSourceResult(store, "src", "Source", true, now);

    expect(store["src"].checks).toHaveLength(1);
    expect(store["src"].checks[0].ok).toBe(true);
  });

  test("getUnhealthySources: > 50% failure rate reported", () => {
    const store = {};
    recordSourceResult(store, "src", "Unhealthy Feed", false);
    recordSourceResult(store, "src", "Unhealthy Feed", false);
    recordSourceResult(store, "src", "Unhealthy Feed", false);
    recordSourceResult(store, "src", "Unhealthy Feed", true);

    const unhealthy = getUnhealthySources(store);
    expect(unhealthy).toContain("Unhealthy Feed");
  });

  test("getUnhealthySources: < 2 checks not reported", () => {
    const store = {};
    recordSourceResult(store, "src", "New Feed", false);

    const unhealthy = getUnhealthySources(store);
    expect(unhealthy).not.toContain("New Feed");
  });

  test("getUnhealthySources: exactly 50% not flagged", () => {
    const store = {};
    recordSourceResult(store, "src", "Borderline Feed", false);
    recordSourceResult(store, "src", "Borderline Feed", true);

    const unhealthy = getUnhealthySources(store);
    expect(unhealthy).not.toContain("Borderline Feed");
  });

  test("formatHealthWarnings returns empty string for empty list", () => {
    expect(formatHealthWarnings([])).toBe("");
  });

  test("formatHealthWarnings includes source names", () => {
    const result = formatHealthWarnings(["Feed A", "Feed B"]);
    expect(result).toContain("Feed A");
    expect(result).toContain("Feed B");
    expect(result).toContain("⚠️");
  });
});
