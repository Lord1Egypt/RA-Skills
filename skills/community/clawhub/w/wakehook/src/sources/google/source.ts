/**
 * GoogleHealthSource — bridges the Google Health API to normalized SleepSessions.
 *
 * Two ingestion modes (config `google.mode`), since the same data is reachable
 * either way:
 *   - "webhook" (push): Google POSTs /webhook when sleep data changes; on UPSERT
 *     we fetch the actual session(s) in those intervals. Needs a public URL.
 *   - "poll" (pull): on a timer we ask the API for recent sleep. All traffic is
 *     outbound, so no inbound URL / tunnel is required.
 *   - "both": push primary, poll as a safety net.
 *
 * Webhook notification shape (per docs):
 *   { "operation": "UPSERT" | "DELETE", "healthUserId": "abc",
 *     "dataType": "sleep", "intervals": [ { "startTime": "...", "endTime": "..." } ] }
 *
 * The exact REST response field names for the new Google Health API should be
 * confirmed against the live API; the mapping is isolated in `mapSession()` so it
 * is the single place to adjust. `apiBase` is overridable (env GOOGLE_HEALTH_API_BASE)
 * so the whole fetch path can be exercised against a local fake.
 */
import type { GoogleHealthConfig } from "../../config.ts";
import type { Store } from "../../db.ts";
import type { PollCapability, SleepSession, Source, WebhookCapability } from "../../types.ts";
import { getValidAccessToken } from "./oauth.ts";

interface Notification {
  operation?: string;
  healthUserId?: string;
  dataType?: string;
  intervals?: Array<{ startTime?: string; endTime?: string }>;
}

export class GoogleHealthSource implements Source {
  readonly name = "google-health";

  /** Push delivery via inbound webhook (present when mode includes "webhook"). */
  readonly webhook?: WebhookCapability;
  /** Pull delivery on a timer (present when mode includes "poll"). No inbound URL. */
  readonly poll?: PollCapability;

  constructor(
    private cfg: GoogleHealthConfig,
    private store: Store,
    private now: () => number = Date.now,
    /** Injectable for tests; defaults to global fetch. */
    private fetcher: typeof fetch = fetch,
  ) {
    if (cfg.mode === "webhook" || cfg.mode === "both") {
      this.webhook = {
        handleChallenge: (req) => this.handleChallenge(req),
        sessionsFromNotification: (req, body) => this.sessionsFromNotification(req, body),
      };
    }
    if (cfg.mode === "poll" || cfg.mode === "both") {
      this.poll = {
        intervalMs: cfg.pollIntervalMs,
        run: () => this.pollOnce(),
      };
    }
  }

  /**
   * Pull recent sleep for the authorized user. The engine's per-day dedup means
   * repeated ticks across a morning fire at most once; a later split-night log
   * supersedes. Needs a stored token (run "bun run auth") but no inbound URL.
   */
  private async pollOnce(): Promise<SleepSession[]> {
    const row = this.store.getSoleToken();
    if (!row) {
      console.warn('[google-health] poll: no stored token yet — run "bun run auth"');
      return [];
    }
    const token = await getValidAccessToken(this.cfg, this.store, row.user, this.now);
    const endTime = new Date(this.now()).toISOString();
    const startTime = new Date(this.now() - this.cfg.pollLookbackMin * 60_000).toISOString();
    return this.fetchSleep(token, row.user, startTime, endTime);
  }

  private async handleChallenge(req: Request): Promise<Response | null> {
    // Some webhook setups send an echo challenge (query or body). Echo it back.
    const url = new URL(req.url);
    const q = url.searchParams.get("challenge") ?? url.searchParams.get("hub.challenge");
    if (q) return new Response(q, { status: 200 });
    return null;
  }

  private async sessionsFromNotification(_req: Request, rawBody: string): Promise<SleepSession[]> {
    let note: Notification;
    try {
      note = JSON.parse(rawBody) as Notification;
    } catch {
      return [];
    }

    if (note.operation !== "UPSERT") return []; // ignore DELETE / unknown
    if (note.dataType && !note.dataType.toLowerCase().includes("sleep")) return [];
    const user = note.healthUserId;
    if (!user) return [];

    const token = await getValidAccessToken(this.cfg, this.store, user, this.now);
    const out: SleepSession[] = [];
    for (const interval of note.intervals ?? []) {
      const fetched = await this.fetchSleep(token, user, interval.startTime, interval.endTime);
      out.push(...fetched);
    }
    return out;
  }

  private async fetchSleep(
    token: string,
    user: string,
    startTime?: string,
    _endTime?: string,
  ): Promise<SleepSession[]> {
    // v4 lists sleep dataPoints; narrow with a civil_end_time lower bound
    // (date is enough — the inference window picks the right session).
    const p = new URLSearchParams();
    if (startTime) {
      p.set("filter", `sleep.interval.civil_end_time >= "${startTime.slice(0, 10)}"`);
    }
    p.set("page_size", "20");
    const res = await this.fetcher(
      `${this.cfg.apiBase}/users/me/dataTypes/sleep/dataPoints?${p.toString()}`,
      { headers: { Authorization: `Bearer ${token}`, Accept: "application/json" } },
    );
    if (!res.ok) {
      console.warn(`[google-health] sleep read ${res.status}: ${await res.text()}`);
      return [];
    }
    const data = (await res.json()) as { dataPoints?: unknown[] };
    return (data.dataPoints ?? [])
      .map((d) => mapSession(d, user))
      .filter((s): s is SleepSession => s !== null);
  }
}

/**
 * Single source of truth for vendor→domain field mapping. Confirmed against the
 * live Google Health v4 API: a sleep dataPoint nests its window under
 * `sleep.interval.{startTime,endTime}` and carries an opaque `name` as the id:
 *   { "name": "users/<id>/dataTypes/sleep/dataPoints/<n>",
 *     "sleep": { "interval": { "startTime": "...", "endTime": "..." },
 *                "type": "STAGES", "stages": [ … ] } }
 */
function mapSession(raw: unknown, user: string): SleepSession | null {
  const dp = raw as Record<string, any>;
  const iv = dp?.sleep?.interval;
  const start: string | undefined = iv?.startTime;
  const end: string | undefined = iv?.endTime;
  if (!start || !end) return null;
  const durationMin = Math.round(
    (new Date(end).getTime() - new Date(start).getTime()) / 60000,
  );
  // The v4 sleep feed has no explicit main-vs-nap flag; treat a substantial
  // session as the main nightly sleep. The morning window + minDurationMin in
  // inference are the real guards against naps / split logs.
  const isMainSleep = durationMin >= 180;
  return {
    id: String(dp.name ?? `${user}:${start}`),
    user,
    start,
    end,
    durationMin,
    isMainSleep,
  };
}
