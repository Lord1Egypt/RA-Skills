import { describe, expect, test } from "bun:test";
import { createHmac } from "node:crypto";
import { fanout, toWakeEvent } from "../src/subscribers/fanout.ts";
import type { Subscriber } from "../src/types.ts";

// Minimal in-memory Store stub (only recordDelivery is used by fanout).
const store = { recordDelivery() {} } as any;

const event = toWakeEvent(
  { user: "u1", start: "2026-06-13T21:52:00Z", end: "2026-06-14T05:03:00Z", durationMin: 431 },
  "google-health",
);

describe("fanout", () => {
  test("generic preset posts the raw signed event with a valid HMAC", async () => {
    let received: { body: string; sig: string | null } | null = null;
    const server = Bun.serve({
      port: 0,
      async fetch(req) {
        received = { body: await req.text(), sig: req.headers.get("x-wake-signature") };
        return new Response("ok");
      },
    });
    const sub: Subscriber = {
      id: "generic-1",
      url: `http://localhost:${server.port}/`,
      secret: "shh",
      preset: "generic",
    };

    const res = await fanout(event, [sub], store);
    server.stop();

    expect(res.delivered).toBe(1);
    expect(received).not.toBeNull();
    const { body, sig } = received!;
    expect(JSON.parse(body).event).toBe("user.awake");
    const expected = "sha256=" + createHmac("sha256", "shh").update(body).digest("hex");
    expect(sig).toBe(expected);
  });

  test("custom headers are sent; no secret means no signature", async () => {
    let received: { body: any; auth: string | null; sig: string | null } | null = null;
    const server = Bun.serve({
      port: 0,
      async fetch(req) {
        received = {
          body: await req.json(),
          auth: req.headers.get("authorization"),
          sig: req.headers.get("x-wake-signature"),
        };
        return new Response("ok");
      },
    });
    // OpenClaw-style: raw event + a bearer header, no HMAC secret.
    const sub: Subscriber = {
      id: "openclaw",
      url: `http://localhost:${server.port}/hooks/wakehook`,
      headers: { Authorization: "Bearer tok" },
    };

    const res = await fanout(event, [sub], store);
    server.stop();

    expect(res.delivered).toBe(1);
    expect(received!.body.event).toBe("user.awake"); // raw neutral event, not pre-formatted
    expect(received!.auth).toBe("Bearer tok");
    expect(received!.sig).toBeNull(); // no secret → unsigned
  });

  test("signs under a custom header in raw-hex format (Hermes-style)", async () => {
    let received: { sig: string | null; defaultSig: string | null } | null = null;
    const server = Bun.serve({
      port: 0,
      async fetch(req) {
        received = {
          sig: req.headers.get("x-webhook-signature"),
          defaultSig: req.headers.get("x-wake-signature"),
        };
        return new Response("ok");
      },
    });
    const sub: Subscriber = {
      id: "hermes",
      url: `http://localhost:${server.port}/webhooks/wakehook`,
      secret: "route-secret",
      signatureHeader: "X-Webhook-Signature",
      signatureFormat: "hex",
    };

    const res = await fanout(event, [sub], store);
    server.stop();

    const body = JSON.stringify(event);
    const expectedHex = createHmac("sha256", "route-secret").update(body).digest("hex");
    expect(res.delivered).toBe(1);
    expect(received!.sig).toBe(expectedHex); // bare hex, custom header
    expect(received!.defaultSig).toBeNull(); // not under the default header
  });

  test("one failing subscriber does not block the others", async () => {
    const ok = Bun.serve({ port: 0, fetch: () => new Response("ok") });
    const good: Subscriber = {
      id: "good",
      url: `http://localhost:${ok.port}/`,
      secret: "s",
      preset: "generic",
    };
    const bad: Subscriber = {
      id: "bad",
      url: "http://127.0.0.1:1/", // connection refused
      secret: "s",
      preset: "generic",
    };

    const res = await fanout(event, [good, bad], store);
    ok.stop();

    expect(res.delivered).toBe(1);
    expect(res.failed).toBe(1);
  });
});
