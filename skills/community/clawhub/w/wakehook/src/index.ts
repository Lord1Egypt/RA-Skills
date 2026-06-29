#!/usr/bin/env bun
/** Entry point: load config, open the store, wire the configured source, serve. */
import { loadConfig } from "./config.ts";
import { Store } from "./db.ts";
import { Engine } from "./engine.ts";
import { createSource } from "./sources/registry.ts";
import { buildServer } from "./server.ts";
import { startPolling } from "./scheduler.ts";

const cfg = loadConfig();
const store = new Store(cfg.dbPath);
const engine = new Engine(cfg, store);
const source = createSource(cfg.source, cfg, store);
const app = buildServer(cfg, source, engine);

// Poll-based sources run on a timer; push-based ones are driven by /webhook.
startPolling(source, engine, cfg, store);

if (source.webhook && !cfg.google.webhookAuthToken) {
  console.warn(
    "[boot] GOOGLE_WEBHOOK_AUTH_TOKEN is unset — /webhook is OPEN. Set it before exposing publicly.",
  );
}
if (cfg.subscribers.length === 0) {
  console.warn("[boot] no subscribers configured — wake events will go nowhere.");
}

const modes = [source.webhook ? "webhook" : null, source.poll ? "poll" : null]
  .filter(Boolean)
  .join("+");
console.log(
  `[boot] wakehook up on :${cfg.port} | source=${source.name} (${modes}) | subscribers=${cfg.subscribers.length} | tz=${cfg.inference.timezone}`,
);

export default { port: cfg.port, fetch: app.fetch };
