/**
 * 12-factor config: a single JSON file (CONFIG_PATH, default ./config.json) with
 * env-var overrides for secrets. Nothing about host/ingress is configured here —
 * exposure is the operator's concern (Cloudflare Tunnel, reverse proxy, …).
 */
import { existsSync, readFileSync } from "node:fs";
import type { Subscriber } from "./types.ts";

export interface InferenceConfig {
  /** IANA timezone used to evaluate "today" and the morning window. */
  timezone: string;
  /** Morning window (local 24h "HH:MM"); a main-sleep ending inside it can fire. */
  windowStart: string; // e.g. "04:00"
  windowEnd: string; // e.g. "11:00"
  /** Minimum main-sleep length (minutes) to qualify; weak guard vs split logs. */
  minDurationMin: number;
  /** If a later main-sleep ends > this many minutes after one we already fired
   *  on, re-fire once (heals Fitbit split-night logs). */
  supersedeGapMin: number;
}

export type GoogleMode = "webhook" | "poll" | "both";

export interface GoogleHealthConfig {
  clientId: string;
  clientSecret: string;
  /** Redirect URI registered in Google Cloud, used by the one-time auth CLI. */
  redirectUri: string;
  /** Shared token the provider must present on webhook calls (Authorization). */
  webhookAuthToken: string;
  scopes: string[];
  /** Base URL of the Google Health REST API. Overridable for local testing. */
  apiBase: string;
  /**
   * How sleep data is ingested:
   *  - "webhook" — Google pushes to /webhook (needs a public HTTPS URL).
   *  - "poll"    — we pull from the API on a timer (no inbound URL; all outbound).
   *  - "both"    — push primary, poll as a safety net.
   */
  mode: GoogleMode;
  /** Poll cadence in ms (when mode includes poll). Lower = faster wake, more calls. */
  pollIntervalMs: number;
  /** How far back each poll scans for recent sleep, in minutes. */
  pollLookbackMin: number;
  /**
   * Only poll around the morning window (inference.windowStart..windowEnd ±
   * pollWindowMarginMin) and stop once we've fired today — instead of all day.
   * Cuts API calls dramatically; set false to poll on every tick, 24/7.
   */
  pollWindowOnly: boolean;
  /** Minutes of slack before windowStart / after windowEnd to still poll. */
  pollWindowMarginMin: number;
}

export interface Config {
  port: number;
  dbPath: string;
  /** Which registered Source to run (see src/sources/registry.ts). */
  source: string;
  inference: InferenceConfig;
  google: GoogleHealthConfig;
  subscribers: Subscriber[];
}

const DEFAULTS = {
  port: 8080,
  dbPath: "./wake.sqlite",
  inference: {
    timezone: "Europe/Brussels",
    windowStart: "04:00",
    windowEnd: "11:00",
    minDurationMin: 180,
    supersedeGapMin: 45,
  } satisfies InferenceConfig,
};

function env(name: string, fallback = ""): string {
  return process.env[name] ?? fallback;
}

function envBool(name: string, fallback: boolean): boolean {
  const v = process.env[name];
  if (v === undefined) return fallback;
  return v === "true" || v === "1";
}

function normalizeMode(v: string): GoogleMode {
  return v === "poll" || v === "both" || v === "webhook" ? v : "webhook";
}

export function loadConfig(): Config {
  const path = env("CONFIG_PATH", "./config.json");
  const file: Partial<Config> = existsSync(path)
    ? JSON.parse(readFileSync(path, "utf8"))
    : {};

  const google: GoogleHealthConfig = {
    clientId: env("GOOGLE_CLIENT_ID", file.google?.clientId ?? ""),
    clientSecret: env("GOOGLE_CLIENT_SECRET", file.google?.clientSecret ?? ""),
    redirectUri: env(
      "GOOGLE_REDIRECT_URI",
      file.google?.redirectUri ?? "http://localhost:8080/oauth/callback",
    ),
    webhookAuthToken: env(
      "GOOGLE_WEBHOOK_AUTH_TOKEN",
      file.google?.webhookAuthToken ?? "",
    ),
    scopes: file.google?.scopes ?? [
      "https://www.googleapis.com/auth/googlehealth.sleep.readonly",
    ],
    apiBase: env(
      "GOOGLE_HEALTH_API_BASE",
      file.google?.apiBase ?? "https://health.googleapis.com/v4",
    ),
    mode: normalizeMode(env("GOOGLE_MODE", file.google?.mode ?? "webhook")),
    pollIntervalMs: Number(
      env("GOOGLE_POLL_INTERVAL_MS", String(file.google?.pollIntervalMs ?? 300_000)),
    ),
    pollLookbackMin: Number(
      env("GOOGLE_POLL_LOOKBACK_MIN", String(file.google?.pollLookbackMin ?? 720)),
    ),
    pollWindowOnly: envBool("GOOGLE_POLL_WINDOW_ONLY", file.google?.pollWindowOnly ?? true),
    pollWindowMarginMin: Number(
      env("GOOGLE_POLL_WINDOW_MARGIN_MIN", String(file.google?.pollWindowMarginMin ?? 30)),
    ),
  };

  return {
    port: Number(env("PORT", String(file.port ?? DEFAULTS.port))),
    dbPath: env("DB_PATH", file.dbPath ?? DEFAULTS.dbPath),
    source: env("SOURCE", file.source ?? "google-health"),
    inference: { ...DEFAULTS.inference, ...(file.inference ?? {}) },
    google,
    subscribers: file.subscribers ?? [],
  };
}
