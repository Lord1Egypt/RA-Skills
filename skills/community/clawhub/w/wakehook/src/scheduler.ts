/**
 * Drives a poll-based Source: periodically calls poll.run() and feeds any
 * sessions into the engine. No-op for push-only sources. Ticks never overlap.
 *
 * When google.pollWindowOnly is set, a tick only hits the API while local time
 * is within the morning window (± margin) and we haven't already fired today —
 * so it polls a handful of times around wake-up instead of all day.
 */
import type { Config } from "./config.ts";
import type { Store } from "./db.ts";
import type { Engine } from "./engine.ts";
import type { Source } from "./types.ts";
import { hhmmToMinutes, localParts } from "./core/time.ts";

/**
 * Whether a poll should actually run now. Pure given (cfg, store, now) so it can
 * be unit-tested. Outside the gated window — or after today's fire — returns false.
 */
export function shouldPollNow(cfg: Config, store: Store, now: () => number): boolean {
  if (!cfg.google.pollWindowOnly) return true;

  const { timezone, windowStart, windowEnd } = cfg.inference;
  const margin = cfg.google.pollWindowMarginMin;
  const local = localParts(new Date(now()).toISOString(), timezone);

  const start = hhmmToMinutes(windowStart) - margin;
  const end = hhmmToMinutes(windowEnd) + margin;
  if (local.minutes < start || local.minutes > end) return false; // outside window

  // Single-user poll: once the sole user has fired today, stop until tomorrow.
  const token = store.getSoleToken();
  if (token) {
    const state = store.getWakeState(token.user);
    if (state && state.fired_date === local.date) return false;
  }
  return true;
}

export function startPolling(
  source: Source,
  engine: Engine,
  cfg: Config,
  store: Store,
  now: () => number = Date.now,
): { stop: () => void } | null {
  const poll = source.poll;
  if (!poll) return null;

  let running = false;
  const tick = async () => {
    if (running) return; // skip if the previous tick is still in flight
    if (!shouldPollNow(cfg, store, now)) return; // outside window / already fired today
    running = true;
    try {
      const sessions = await poll.run();
      if (sessions.length) await engine.process(sessions, source.name);
    } catch (err) {
      console.error(`[poll] ${source.name} error: ${String(err)}`);
    } finally {
      running = false;
    }
  };

  const handle = setInterval(tick, poll.intervalMs);
  const when = cfg.google.pollWindowOnly
    ? `${cfg.inference.windowStart}-${cfg.inference.windowEnd} ±${cfg.google.pollWindowMarginMin}m ${cfg.inference.timezone}`
    : "all day";
  console.log(`[poll] polling ${source.name} every ${poll.intervalMs}ms (${when})`);
  void tick(); // run once immediately on boot
  return { stop: () => clearInterval(handle) };
}
