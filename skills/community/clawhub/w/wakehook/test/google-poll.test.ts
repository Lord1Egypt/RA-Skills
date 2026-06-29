import { describe, expect, test } from "bun:test";
import { Store } from "../src/db.ts";
import { GoogleHealthSource } from "../src/sources/google/source.ts";
import type { GoogleHealthConfig, GoogleMode } from "../src/config.ts";

const NOW = "2026-06-14T05:30:00Z"; // 07:30 Europe/Brussels
const now = () => Date.parse(NOW);

function gcfg(mode: GoogleMode): GoogleHealthConfig {
  return {
    clientId: "",
    clientSecret: "",
    redirectUri: "",
    webhookAuthToken: "",
    scopes: [],
    apiBase: "https://fake.local/v4",
    mode,
    pollIntervalMs: 1000,
    pollLookbackMin: 720,
  };
}

/** A store pre-seeded with a non-expiring token, so no real OAuth call is made. */
function seededStore(): Store {
  const store = new Store(":memory:");
  store.upsertToken({
    user: "user-123",
    access_token: "fake-access",
    refresh_token: "fake-refresh",
    expires_at: now() + 3_600_000, // valid for an hour → no refresh round-trip
  });
  return store;
}

describe("google-health capabilities by mode", () => {
  test("webhook → only webhook present", () => {
    const s = new GoogleHealthSource(gcfg("webhook"), new Store(":memory:"), now);
    expect(s.webhook).toBeDefined();
    expect(s.poll).toBeUndefined();
  });

  test("poll → only poll present, with the configured interval", () => {
    const s = new GoogleHealthSource(gcfg("poll"), new Store(":memory:"), now);
    expect(s.webhook).toBeUndefined();
    expect(s.poll).toBeDefined();
    expect(s.poll?.intervalMs).toBe(1000);
  });

  test("both → webhook and poll present", () => {
    const s = new GoogleHealthSource(gcfg("both"), new Store(":memory:"), now);
    expect(s.webhook).toBeDefined();
    expect(s.poll).toBeDefined();
  });
});

describe("google-health poll.run()", () => {
  test("fetches the lookback window and maps the sleep response", async () => {
    let calledUrl = "";
    const fetcher = (async (url: string | URL) => {
      calledUrl = String(url);
      // Real Google Health v4 sleep dataPoint shape.
      return new Response(
        JSON.stringify({
          dataPoints: [
            {
              name: "users/2834047355338061809/dataTypes/sleep/dataPoints/8550210982076189912",
              sleep: {
                interval: { startTime: "2026-06-13T21:52:00Z", endTime: "2026-06-14T05:03:00Z" },
                type: "STAGES",
              },
            },
          ],
        }),
        { status: 200 },
      );
    }) as unknown as typeof fetch;

    const s = new GoogleHealthSource(gcfg("poll"), seededStore(), now, fetcher);
    const sessions = await s.poll!.run();

    expect(calledUrl).toStartWith("https://fake.local/v4/users/me/dataTypes/sleep/dataPoints?");
    expect(calledUrl).toContain("filter=");
    expect(sessions).toHaveLength(1);
    expect(sessions[0]).toMatchObject({
      id: "users/2834047355338061809/dataTypes/sleep/dataPoints/8550210982076189912",
      user: "user-123",
      end: "2026-06-14T05:03:00Z",
      durationMin: 431,
      isMainSleep: true,
    });
  });

  test("returns [] (no throw) when no token is stored yet", async () => {
    const s = new GoogleHealthSource(gcfg("poll"), new Store(":memory:"), now);
    expect(await s.poll!.run()).toEqual([]);
  });
});
