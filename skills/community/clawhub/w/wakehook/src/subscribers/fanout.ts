/**
 * Broadcast a WakeEvent to every configured subscriber. Each delivery posts the
 * raw, vendor-neutral event; it is signed with the subscriber's secret when one
 * is set, carries any configured headers (e.g. the receiver's auth bearer), and
 * is retried a few times. One slow/failing subscriber never blocks the others.
 */
import { createHmac } from "node:crypto";
import type { Subscriber, WakeEvent } from "../types.ts";
import type { Store } from "../db.ts";

const MAX_ATTEMPTS = 4;
const BASE_BACKOFF_MS = 500;

function sign(body: string, sub: Subscriber): string {
  const hex = createHmac("sha256", sub.secret!).update(body).digest("hex");
  return sub.signatureFormat === "hex" ? hex : `sha256=${hex}`;
}

async function deliverOne(
  event: WakeEvent,
  eventId: string,
  sub: Subscriber,
  store: Store,
  now: () => number,
): Promise<boolean> {
  const body = JSON.stringify(event);
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-Wake-Event-Id": eventId,
    ...(sub.headers ?? {}),
    ...(sub.secret ? { [sub.signatureHeader ?? "X-Wake-Signature"]: sign(body, sub) } : {}),
  };

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    try {
      const res = await fetch(sub.url, {
        method: "POST",
        headers,
        body,
        signal: AbortSignal.timeout(10_000),
      });
      if (res.ok) {
        store.recordDelivery(eventId, sub.id, "ok", attempt, now());
        console.log(`[fanout] ${sub.id} ✓ (${res.status}, attempt ${attempt})`);
        return true;
      }
      console.warn(`[fanout] ${sub.id} non-2xx ${res.status} (attempt ${attempt})`);
    } catch (err) {
      console.warn(`[fanout] ${sub.id} error (attempt ${attempt}): ${String(err)}`);
    }
    if (attempt < MAX_ATTEMPTS) {
      await Bun.sleep(BASE_BACKOFF_MS * 2 ** (attempt - 1));
    }
  }
  store.recordDelivery(eventId, sub.id, "failed", MAX_ATTEMPTS, now());
  return false;
}

export async function fanout(
  event: WakeEvent,
  subscribers: Subscriber[],
  store: Store,
  now: () => number = Date.now,
): Promise<{ delivered: number; failed: number }> {
  const eventId = `${event.user}:${event.wokeAt}`;
  if (subscribers.length === 0) {
    console.warn("[fanout] no subscribers configured — event not delivered anywhere");
    return { delivered: 0, failed: 0 };
  }
  const results = await Promise.all(
    subscribers.map((s) => deliverOne(event, eventId, s, store, now)),
  );
  const delivered = results.filter(Boolean).length;
  return { delivered, failed: results.length - delivered };
}

export function toWakeEvent(
  session: { user: string; start: string; end: string; durationMin: number },
  source: string,
): WakeEvent {
  return {
    event: "user.awake",
    wokeAt: session.end,
    user: session.user,
    source,
    session: {
      start: session.start,
      end: session.end,
      durationMin: session.durationMin,
    },
  };
}
