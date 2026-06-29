import { describe, expect, test } from "bun:test";
import { Store } from "../src/db.ts";
import { shouldPollNow } from "../src/scheduler.ts";
import type { Config } from "../src/config.ts";

// Window 04:00–11:00 Europe/Brussels (UTC+2 in June), margin 30m → [03:30, 11:30] local.
function cfg(overrides: Partial<Config["google"]> = {}): Config {
  return {
    port: 0,
    dbPath: ":memory:",
    source: "google-health",
    inference: {
      timezone: "Europe/Brussels",
      windowStart: "04:00",
      windowEnd: "11:00",
      minDurationMin: 180,
      supersedeGapMin: 45,
    },
    google: {
      clientId: "", clientSecret: "", redirectUri: "", webhookAuthToken: "", scopes: [],
      apiBase: "https://health.googleapis.com/v4",
      mode: "poll", pollIntervalMs: 300_000, pollLookbackMin: 720,
      pollWindowOnly: true, pollWindowMarginMin: 30,
      ...overrides,
    },
    subscribers: [],
  };
}

const at = (iso: string) => () => Date.parse(iso);

describe("shouldPollNow (window gating)", () => {
  test("polls inside the window", () => {
    // 05:00Z = 07:00 Brussels → inside
    expect(shouldPollNow(cfg(), new Store(":memory:"), at("2026-06-14T05:00:00Z"))).toBe(true);
  });

  test("skips outside the window", () => {
    // 20:00Z = 22:00 Brussels → outside
    expect(shouldPollNow(cfg(), new Store(":memory:"), at("2026-06-14T20:00:00Z"))).toBe(false);
  });

  test("honors the margin (just before windowStart)", () => {
    // 01:40Z = 03:40 Brussels → within 03:30 margin
    expect(shouldPollNow(cfg(), new Store(":memory:"), at("2026-06-14T01:40:00Z"))).toBe(true);
    // 01:20Z = 03:20 Brussels → before the 03:30 margin
    expect(shouldPollNow(cfg(), new Store(":memory:"), at("2026-06-14T01:20:00Z"))).toBe(false);
  });

  test("stops after firing today, resumes next day", () => {
    const store = new Store(":memory:");
    store.upsertToken({ user: "u", access_token: "a", refresh_token: "r", expires_at: 0 });
    store.setWakeState({ user: "u", fired_date: "2026-06-14", last_fired_end: "x" });
    // in-window same day, already fired → skip
    expect(shouldPollNow(cfg(), store, at("2026-06-14T05:00:00Z"))).toBe(false);
    // next day, in-window → poll again
    expect(shouldPollNow(cfg(), store, at("2026-06-15T05:00:00Z"))).toBe(true);
  });

  test("pollWindowOnly:false always polls", () => {
    expect(
      shouldPollNow(cfg({ pollWindowOnly: false }), new Store(":memory:"), at("2026-06-14T20:00:00Z")),
    ).toBe(true);
  });
});
