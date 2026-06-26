import { describe, expect, test } from "bun:test";
import { mkdtemp, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { loadSourcesConfig, getTwitterSources, getRssSources } from "../../src/config/sources";

describe("loadSourcesConfig", () => {
  test("first run writes defaults and returns them", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "sources-config-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const config = await loadSourcesConfig(env);
    expect(config.sources.length).toBeGreaterThan(0);
    expect(config.sources.some((s) => s.id === "taviso")).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("getTwitterSources returns only enabled twitter sources", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "sources-config-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const config = await loadSourcesConfig(env);
    const twitterSources = getTwitterSources(config);

    expect(twitterSources.every((s) => s.type === "twitter")).toBe(true);
    expect(twitterSources.every((s) => s.enabled)).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("getRssSources returns only rss sources", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "sources-config-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const config = await loadSourcesConfig(env);
    const rssSources = getRssSources(config);

    expect(rssSources.every((s) => s.type === "rss")).toBe(true);

    await rm(tempDir, { recursive: true, force: true });
  });

  test("all default Twitter sources have expected fields", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "sources-config-"));
    const env = { SEC_DAILY_DIGEST_HOME: tempDir } as NodeJS.ProcessEnv;

    const config = await loadSourcesConfig(env);
    for (const source of config.sources) {
      expect(source.id).toBeTruthy();
      expect(source.type).toBeTruthy();
      expect(source.name).toBeTruthy();
      expect(Array.isArray(source.topics)).toBe(true);
    }

    await rm(tempDir, { recursive: true, force: true });
  });
});
