import { describe, expect, test } from "bun:test";
import { Engine } from "../src/engine.ts";
import { Store } from "../src/db.ts";
import { createSource, availableSources } from "../src/sources/registry.ts";
import type { Config } from "../src/config.ts";
import type { PollCapability, SleepSession, Source, WebhookCapability } from "../src/types.ts";

const NOW = "2026-06-14T05:30:00Z"; // 07:30 Europe/Brussels (UTC+2 in June)
const now = () => Date.parse(NOW);

function cfg(): Config {
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
      clientId: "",
      clientSecret: "",
      redirectUri: "",
      webhookAuthToken: "",
      scopes: [],
      apiBase: "https://health.googleapis.com/v1",
      mode: "webhook",
      pollIntervalMs: 900_000,
      pollLookbackMin: 720,
    },
    subscribers: [], // fan-out is exercised in fanout.test.ts; here we assert firing
  };
}

function morningSession(user: string): SleepSession {
  return {
    id: `${user}:s`,
    user,
    start: "2026-06-13T21:52:00Z",
    end: "2026-06-14T05:03:00Z", // 07:03 local — inside the window
    durationMin: 431,
    isMainSleep: true,
  };
}

// A made-up provider that needs NO core changes to work — proof the interface
// is generic. It exposes BOTH capabilities to show either path feeds the engine.
class FakeSource implements Source {
  readonly name = "fake";
  constructor(private session: SleepSession) {}
  readonly webhook: WebhookCapability = {
    handleChallenge: async () => null,
    sessionsFromNotification: async () => [this.session],
  };
  readonly poll: PollCapability = {
    intervalMs: 1000,
    run: async () => [this.session],
  };
}

describe("source registry", () => {
  test("resolves the built-in google-health source with a webhook capability", () => {
    const s = createSource("google-health", cfg(), new Store(":memory:"));
    expect(s.name).toBe("google-health");
    expect(s.webhook).toBeDefined();
    expect(s.poll).toBeUndefined();
  });

  test("throws with available names on an unknown source", () => {
    expect(() => createSource("nope", cfg(), new Store(":memory:"))).toThrow(/unknown source/);
    expect(availableSources()).toContain("google-health");
  });
});

describe("generic Source → core", () => {
  test("sessions arriving via the WEBHOOK capability fire a wake", async () => {
    const store = new Store(":memory:");
    const engine = new Engine(cfg(), store, now);
    const src = new FakeSource(morningSession("wh-user"));
    const sessions = await src.webhook.sessionsFromNotification(new Request("http://x"), "{}");
    expect(await engine.process(sessions, src.name)).toBe(1);
  });

  test("sessions arriving via the POLL capability fire a wake", async () => {
    const store = new Store(":memory:");
    const engine = new Engine(cfg(), store, now);
    const src = new FakeSource(morningSession("poll-user"));
    const sessions = await src.poll.run();
    expect(await engine.process(sessions, src.name)).toBe(1);
  });
});
