/**
 * HTTP surface (Hono):
 *   GET  /healthz        — liveness
 *   POST /webhook        — provider notifications + ownership-verification handshake
 *   POST /test/replay    — fire a synthetic wake to exercise subscribers without
 *                          waiting for morning
 *
 * No ingress assumptions: front this with a Cloudflare Tunnel / reverse proxy / etc.
 */
import { Hono } from "hono";
import type { Config } from "./config.ts";
import type { SleepSession, Source } from "./types.ts";
import type { Engine } from "./engine.ts";

export function buildServer(cfg: Config, source: Source, engine: Engine): Hono {
  const app = new Hono();

  app.get("/healthz", (c) =>
    c.json({
      ok: true,
      source: source.name,
      modes: [source.webhook ? "webhook" : null, source.poll ? "poll" : null].filter(Boolean),
    }),
  );

  // The provider's ownership-verification challenge succeeds WITH the configured
  // auth token and is rejected (401) WITHOUT it — exactly what Google probes for.
  function authorized(req: Request): boolean {
    const token = cfg.google.webhookAuthToken;
    if (!token) return true; // unset → open (dev only; warned at boot)
    const header = req.headers.get("authorization") ?? "";
    const presented = header.replace(/^Bearer\s+/i, "");
    return (
      presented === token || req.headers.get("x-webhook-token") === token
    );
  }

  // Only mounted for push providers. A poll-only source has no inbound webhook.
  const wh = source.webhook;
  if (wh) {
    app.post("/webhook", async (c) => {
      if (!authorized(c.req.raw)) return c.text("unauthorized", 401);

      // Verification challenge (echo), if this is one.
      const challenge = await wh.handleChallenge(c.req.raw);
      if (challenge) return challenge;

      const rawBody = await c.req.text();

      // Ack immediately (204) so the provider is satisfied; process out-of-band.
      queueMicrotask(async () => {
        try {
          const sessions = await wh.sessionsFromNotification(c.req.raw, rawBody);
          if (sessions.length) await engine.process(sessions, source.name);
        } catch (err) {
          console.error(`[webhook] processing error: ${String(err)}`);
        }
      });

      return c.body(null, 204);
    });
  } else {
    app.post("/webhook", (c) => c.text(`source "${source.name}" does not use webhooks`, 501));
  }

  // Synthetic wake for testing the subscriber side. Defaults to "now" so it
  // lands in the morning window only if you call it during the window — pass an
  // explicit `end` to force a fire.
  app.post("/test/replay", async (c) => {
    if (!authorized(c.req.raw)) return c.text("unauthorized", 401);
    const body = (await c.req.json().catch(() => ({}))) as Partial<SleepSession>;
    const end = body.end ?? new Date().toISOString();
    const durationMin = body.durationMin ?? 420;
    const start = body.start ?? new Date(new Date(end).getTime() - durationMin * 60000).toISOString();
    const session: SleepSession = {
      id: body.id ?? `test:${end}`,
      user: body.user ?? "test-user",
      start,
      end,
      durationMin,
      isMainSleep: body.isMainSleep ?? true,
    };
    const fired = await engine.process([session], source.name);
    return c.json({ fired, session });
  });

  return app;
}
