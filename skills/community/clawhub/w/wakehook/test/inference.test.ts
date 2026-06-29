import { describe, expect, test } from "bun:test";
import { decide } from "../src/core/inference.ts";
import type { InferenceConfig } from "../src/config.ts";
import type { SleepSession } from "../src/types.ts";
import type { WakeStateRow } from "../src/db.ts";

const cfg: InferenceConfig = {
  timezone: "Europe/Brussels", // UTC+2 in June
  windowStart: "04:00",
  windowEnd: "11:00",
  minDurationMin: 180,
  supersedeGapMin: 45,
};

// In June, Brussels is UTC+2. 07:03 local == 05:03Z.
const NOW = "2026-06-14T05:30:00Z"; // 07:30 local

function session(over: Partial<SleepSession> = {}): SleepSession {
  return {
    id: "s1",
    user: "u1",
    start: "2026-06-13T21:52:00Z", // 23:52 local
    end: "2026-06-14T05:03:00Z", // 07:03 local
    durationMin: 431,
    isMainSleep: true,
    ...over,
  };
}

describe("wake inference", () => {
  test("fires on first qualifying main sleep in the window", () => {
    const d = decide(session(), cfg, null, NOW);
    expect(d.fire).toBe(true);
  });

  test("ignores naps", () => {
    const d = decide(session({ isMainSleep: false }), cfg, null, NOW);
    expect(d.fire).toBe(false);
  });

  test("ignores sessions ending on a prior day (late edit)", () => {
    const d = decide(
      session({ end: "2026-06-13T05:03:00Z", start: "2026-06-12T21:00:00Z" }),
      cfg,
      null,
      NOW,
    );
    expect(d.fire).toBe(false);
  });

  test("rejects an end below the morning window (mid-night split log)", () => {
    // 03:30 local == 01:30Z, below 04:00 window start.
    const d = decide(
      session({ end: "2026-06-14T01:30:00Z", durationMin: 200 }),
      cfg,
      null,
      NOW,
    );
    expect(d.fire).toBe(false);
  });

  test("rejects too-short sessions", () => {
    const d = decide(session({ durationMin: 90 }), cfg, null, NOW);
    expect(d.fire).toBe(false);
  });

  test("does not fire twice the same day", () => {
    const prior: WakeStateRow = {
      user: "u1",
      fired_date: "2026-06-14",
      last_fired_end: "2026-06-14T05:03:00Z",
    };
    const d = decide(session(), cfg, prior, NOW);
    expect(d.fire).toBe(false);
  });

  test("supersedes when a later main sleep ends well after the prior fire", () => {
    // Prior fired on a 05:03 local end; now a 07:00 local end arrives (>45m later).
    const prior: WakeStateRow = {
      user: "u1",
      fired_date: "2026-06-14",
      last_fired_end: "2026-06-14T03:03:00Z", // 05:03 local
    };
    const later = session({ end: "2026-06-14T05:03:00Z" }); // 07:03 local, +120m
    const d = decide(later, cfg, prior, NOW);
    expect(d.fire).toBe(true);
  });

  test("does not supersede within the gap", () => {
    const prior: WakeStateRow = {
      user: "u1",
      fired_date: "2026-06-14",
      last_fired_end: "2026-06-14T04:50:00Z", // 06:50 local
    };
    const later = session({ end: "2026-06-14T05:03:00Z" }); // +13m only
    const d = decide(later, cfg, prior, NOW);
    expect(d.fire).toBe(false);
  });
});
