// SubsTracker HTTP Client — env loading, auth, cookie management
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import type { SubsTrackerEnv } from "./types";

const COOKIE_PATH = path.join(os.homedir(), ".substracker-skills", "cookie");

// ─── Env Loading (baoyu-style) ───

function loadEnvFile(envPath: string): Record<string, string> {
  const env: Record<string, string> = {};
  if (!fs.existsSync(envPath)) return env;

  const content = fs.readFileSync(envPath, "utf-8");
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx > 0) {
      const key = trimmed.slice(0, eqIdx).trim();
      let value = trimmed.slice(eqIdx + 1).trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  }
  return env;
}

export function loadConfig(): SubsTrackerEnv {
  const cwdEnvPath = path.join(process.cwd(), ".substracker-skills", ".env");
  const homeEnvPath = path.join(os.homedir(), ".substracker-skills", ".env");

  const cwdEnv = loadEnvFile(cwdEnvPath);
  const homeEnv = loadEnvFile(homeEnvPath);

  const url = process.env.SUBSTRACKER_URL || cwdEnv.SUBSTRACKER_URL || homeEnv.SUBSTRACKER_URL;
  const user = process.env.SUBSTRACKER_USER || cwdEnv.SUBSTRACKER_USER || homeEnv.SUBSTRACKER_USER;
  const pass = process.env.SUBSTRACKER_PASS || cwdEnv.SUBSTRACKER_PASS || homeEnv.SUBSTRACKER_PASS;

  const missing = [
    !url && "SUBSTRACKER_URL",
    !user && "SUBSTRACKER_USER",
    !pass && "SUBSTRACKER_PASS",
  ].filter(Boolean);

  if (missing.length) {
    throw new Error(
      `Missing: ${missing.join(", ")}.\n` +
      "Set via environment variables or in .substracker-skills/.env file."
    );
  }

  return { SUBSTRACKER_URL: url.replace(/\/+$/, ""), SUBSTRACKER_USER: user, SUBSTRACKER_PASS: pass };
}

// ─── Cookie ───

function saveCookie(setCookieHeader: string): void {
  fs.mkdirSync(path.dirname(COOKIE_PATH), { recursive: true });
  fs.writeFileSync(COOKIE_PATH, setCookieHeader, "utf-8");
}

function loadCookie(): string {
  if (!fs.existsSync(COOKIE_PATH)) return "";
  return fs.readFileSync(COOKIE_PATH, "utf-8").trim();
}

export function hasCookie(): boolean {
  return !!loadCookie();
}

// ─── Auth ───

let _config: SubsTrackerEnv | null = null;

export function init(cfg: SubsTrackerEnv): void {
  _config = cfg;
}

function getConfig(): SubsTrackerEnv {
  if (!_config) throw new Error("Client not initialized. Call init() first.");
  return _config;
}

export async function login(): Promise<boolean> {
  const cfg = getConfig();
  const res = await fetch(`${cfg.SUBSTRACKER_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: cfg.SUBSTRACKER_USER, password: cfg.SUBSTRACKER_PASS }),
    redirect: "manual",
  });

  const setCookie = res.headers.get("set-cookie");
  if (setCookie) saveCookie(setCookie);

  const data = (await res.json()) as { success: boolean };
  return data.success === true;
}

// ─── Generic API Call ───

export async function api<T = unknown>(
  method: string,
  endpoint: string,
  body?: unknown,
  retried = false
): Promise<T> {
  const cfg = getConfig();
  const cookie = loadCookie();
  const headers: Record<string, string> = { "Content-Type": "application/json" };

  if (cookie) {
    const match = cookie.match(/([^=]+=[^;]+)/);
    if (match) headers["Cookie"] = match[1]!;
  }

  const res = await fetch(`${cfg.SUBSTRACKER_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    redirect: "manual",
  });

  if (res.status === 401 && !retried) {
    console.error("[substracker] Session expired, re-logging in...");
    const ok = await login();
    if (ok) return api<T>(method, endpoint, body, true);
    throw new Error("Login failed");
  }

  return (await res.json()) as T;
}
