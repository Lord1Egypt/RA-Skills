/**
 * The heart of the bus: decide whether a sleep session represents a real wake
 * worth broadcasting — and exactly once per morning.
 *
 * Locked priorities: NEVER MISS a wakeup; fire as FAST as the data arrives.
 *  - No upper "freshness" gate: a late-syncing webhook still fires (slightly late)
 *    rather than being rejected.
 *  - Fire on the FIRST qualifying session: lowest possible latency.
 *  - Morning-window lower bound guards against Fitbit "first-part" split-sleep
 *    logs firing too early.
 *  - Supersede: a later main-sleep ending well after one we already fired on
 *    re-fires once, healing the rare split-night.
 */
import type { InferenceConfig } from "../config.ts";
import type { SleepSession } from "../types.ts";
import type { WakeStateRow } from "../db.ts";
import { hhmmToMinutes, localParts } from "./time.ts";

export type Decision =
  | { fire: true; firedDate: string; reason: string }
  | { fire: false; reason: string };

export function decide(
  session: SleepSession,
  cfg: InferenceConfig,
  prior: WakeStateRow | null,
  nowIso: string,
): Decision {
  if (!session.isMainSleep) {
    return { fire: false, reason: "not main sleep (nap/other)" };
  }

  const end = localParts(session.end, cfg.timezone);
  const today = localParts(nowIso, cfg.timezone).date;

  if (end.date !== today) {
    return { fire: false, reason: `session ends ${end.date}, not today ${today}` };
  }

  const winStart = hhmmToMinutes(cfg.windowStart);
  const winEnd = hhmmToMinutes(cfg.windowEnd);
  if (end.minutes < winStart || end.minutes > winEnd) {
    return {
      fire: false,
      reason: `end ${cfg.timezone} ${fmtMin(end.minutes)} outside window ${cfg.windowStart}-${cfg.windowEnd}`,
    };
  }

  if (session.durationMin < cfg.minDurationMin) {
    return {
      fire: false,
      reason: `duration ${session.durationMin}m < min ${cfg.minDurationMin}m`,
    };
  }

  // Dedup + supersede.
  if (prior && prior.fired_date === today) {
    const gapMs =
      new Date(session.end).getTime() - new Date(prior.last_fired_end).getTime();
    const gapMin = gapMs / 60000;
    if (gapMin > cfg.supersedeGapMin) {
      return {
        fire: true,
        firedDate: today,
        reason: `supersede: ends ${Math.round(gapMin)}m after prior fire`,
      };
    }
    return { fire: false, reason: "already fired today" };
  }

  return { fire: true, firedDate: today, reason: "first qualifying main sleep today" };
}

function fmtMin(m: number): string {
  const h = Math.floor(m / 60);
  const min = m % 60;
  return `${String(h).padStart(2, "0")}:${String(min).padStart(2, "0")}`;
}
