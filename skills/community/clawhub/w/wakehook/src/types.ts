/**
 * Provider-agnostic domain types. Sources translate vendor payloads into these;
 * the core reasons only about these; subscribers receive only WakeEvent.
 */

/** A normalized sleep session, as produced by any Source adapter. */
export interface SleepSession {
  /** Stable id of the session from the provider (used for logging/idempotency). */
  id: string;
  /** Opaque per-person id from the provider (e.g. Google healthUserId). */
  user: string;
  /** Start instant (ISO 8601 with offset). */
  start: string;
  /** End / wake instant (ISO 8601 with offset). */
  end: string;
  /** Duration in minutes. */
  durationMin: number;
  /** True for the main nightly sleep; false for naps. */
  isMainSleep: boolean;
}

/** The neutral fact this bus exists to broadcast. */
export interface WakeEvent {
  event: "user.awake";
  /** Wake instant (ISO 8601 with offset) — equals session.end. */
  wokeAt: string;
  /** Opaque per-person id. */
  user: string;
  /** Which provider produced the underlying data. */
  source: string;
  session: {
    start: string;
    end: string;
    durationMin: number;
  };
}

/** A configured downstream consumer. The bus knows nothing of its purpose. */
export interface Subscriber {
  /** Friendly id, also used in delivery state + logs. */
  id: string;
  /** Destination URL the WakeEvent is POSTed to. */
  url: string;
  /** Optional HMAC-SHA256 secret; when set, the body is signed (see signatureHeader). */
  secret?: string;
  /**
   * Header carrying the HMAC signature. Default `X-Wake-Signature`. Set it to
   * match a receiver that verifies a specific header — e.g. Hermes Agent's
   * `X-Hub-Signature-256` (GitHub-style) or `X-Webhook-Signature` (generic).
   */
  signatureHeader?: string;
  /**
   * How the signature is encoded: `prefixed` → `sha256=<hex>` (default, GitHub /
   * X-Hub-Signature-256 style), `hex` → bare `<hex>` (Hermes X-Webhook-Signature).
   */
  signatureFormat?: "prefixed" | "hex";
  /**
   * Extra HTTP headers sent with every delivery — used to satisfy the receiver's
   * own auth. For OpenClaw, point `url` at a mapped hook and set
   * `{ "Authorization": "Bearer <hooks.token>" }`; OpenClaw turns the raw event
   * into a wake/agent action via `hooks.mappings`.
   */
  headers?: Record<string, string>;
  /**
   * Output shape. Only "generic" today: POST the raw signed WakeEvent — the
   * vendor-neutral contract; the consumer decides what it means. Defaults to
   * "generic".
   */
  preset?: "generic";
}

/**
 * A Source adapter bridges one provider to normalized SleepSessions. Providers
 * deliver data in one of two ways, modeled as optional capabilities — a source
 * implements whichever fit (and may implement both):
 *
 *   - `webhook` (push): the provider POSTs notifications to /webhook.
 *       e.g. Google Health, Fitbit Web, WHOOP, Withings, Oura, Sleep as Android.
 *   - `poll`   (pull): we periodically ask the provider for recent sessions.
 *       e.g. an on-device Health Connect bridge, Open Wearables, plain REST APIs.
 *
 * The core (inference, dedup, fan-out) is identical regardless of how sessions
 * arrive. Adding a provider = implement this interface in src/sources/<name>/
 * and register it in src/sources/registry.ts. No core changes.
 */
export interface Source {
  /** Stable provider id placed into WakeEvent.source. */
  readonly name: string;
  /** Present if this provider pushes notifications to an inbound webhook. */
  readonly webhook?: WebhookCapability;
  /** Present if this provider is polled for recent sessions. */
  readonly poll?: PollCapability;
}

/** Inbound-webhook capability (push providers). */
export interface WebhookCapability {
  /**
   * Handle the provider's endpoint-ownership verification challenge.
   * Return a Response to send verbatim if this request was a challenge;
   * return null if it's an ordinary notification to be parsed.
   */
  handleChallenge(req: Request): Promise<Response | null>;
  /**
   * Parse an inbound notification and return the affected sessions, fetching
   * full detail from the provider API as needed. May return [] (nothing relevant).
   */
  sessionsFromNotification(req: Request, rawBody: string): Promise<SleepSession[]>;
}

/** Polling capability (pull providers). */
export interface PollCapability {
  /** How often to poll, in milliseconds. */
  readonly intervalMs: number;
  /** Fetch recent sessions. May return [] when nothing new. */
  run(): Promise<SleepSession[]>;
}
