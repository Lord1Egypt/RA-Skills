/**
 * Wiring: given normalized sessions, run the wake-inference rule, persist dedup
 * state on a fire, and fan the event out to all subscribers. Provider-agnostic.
 */
import type { Config } from "./config.ts";
import type { Store } from "./db.ts";
import type { SleepSession } from "./types.ts";
import { decide } from "./core/inference.ts";
import { fanout, toWakeEvent } from "./subscribers/fanout.ts";

export class Engine {
  constructor(
    private cfg: Config,
    private store: Store,
    private now: () => number = Date.now,
  ) {}

  /** Process sessions from a source. Returns how many wake events were fired. */
  async process(sessions: SleepSession[], source: string): Promise<number> {
    let fired = 0;
    for (const session of sessions) {
      const nowIso = new Date(this.now()).toISOString();
      const prior = this.store.getWakeState(session.user);
      const decision = decide(session, this.cfg.inference, prior, nowIso);

      if (!decision.fire) {
        console.log(`[engine] skip ${session.id}: ${decision.reason}`);
        continue;
      }

      console.log(`[engine] FIRE ${session.id}: ${decision.reason}`);
      this.store.setWakeState({
        user: session.user,
        fired_date: decision.firedDate,
        last_fired_end: session.end,
      });

      const event = toWakeEvent(session, source);
      const res = await fanout(event, this.cfg.subscribers, this.store, this.now);
      console.log(`[engine] delivered ${res.delivered}/${res.delivered + res.failed} subscribers`);
      fired++;
    }
    return fired;
  }
}
