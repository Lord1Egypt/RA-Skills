/**
 * Source registry: maps a config `source` name to a constructed Source.
 *
 * To add a provider:
 *   1. implement the Source interface under src/sources/<name>/
 *   2. add one line to REGISTRY below
 *   3. set `"source": "<name>"` in config
 * No changes to the core, server, or scheduler are needed.
 */
import type { Config } from "../config.ts";
import type { Store } from "../db.ts";
import type { Source } from "../types.ts";
import { GoogleHealthSource } from "./google/source.ts";

type SourceFactory = (cfg: Config, store: Store, now?: () => number) => Source;

const REGISTRY: Record<string, SourceFactory> = {
  "google-health": (cfg, store, now) => new GoogleHealthSource(cfg.google, store, now),
  // "fitbit-web":     (cfg, store) => new FitbitWebSource(...),      ← future PR
  // "health-connect": (cfg, store) => new HealthConnectSource(...),  ← future PR (poll)
};

export function availableSources(): string[] {
  return Object.keys(REGISTRY);
}

export function createSource(
  name: string,
  cfg: Config,
  store: Store,
  now?: () => number,
): Source {
  const factory = REGISTRY[name];
  if (!factory) {
    throw new Error(
      `unknown source "${name}". Available: ${availableSources().join(", ")}`,
    );
  }
  return factory(cfg, store, now);
}
