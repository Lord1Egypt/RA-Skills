#!/usr/bin/env node
/**
 * Cookie extraction module — wraps @steipete/sweet-cookie
 * Extracts YC session cookies from Chrome/Safari/Firefox
 */

import { getCookies } from "@steipete/sweet-cookie";
import { readFileSync, existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import kleur from "kleur";

export interface YcCookies {
  [key: string]: string;
}

export type CookieSource = "chrome" | "safari" | "firefox";

interface ChromeProfileInfo {
  dirName: string;
  displayName: string;
}

/**
 * Discover Chrome profiles from Local State file.
 */
function discoverChromeProfiles(): ChromeProfileInfo[] {
  if (process.platform !== "darwin") return [];

  const localStatePath = join(
    homedir(),
    "Library",
    "Application Support",
    "Google",
    "Chrome",
    "Local State"
  );

  if (!existsSync(localStatePath)) return [];

  try {
    const raw = readFileSync(localStatePath, "utf-8");
    const state = JSON.parse(raw);
    const infoCache = state?.profile?.info_cache;
    if (!infoCache || typeof infoCache !== "object") return [];

    const profiles: ChromeProfileInfo[] = [];
    for (const [dirName, meta] of Object.entries(infoCache)) {
      const m = meta as Record<string, unknown>;
      const displayName = String(m.name || m.gaia_name || dirName);
      profiles.push({ dirName, displayName });
    }

    profiles.sort((a, b) => {
      if (a.dirName === "Default") return -1;
      if (b.dirName === "Default") return 1;
      return a.dirName.localeCompare(b.dirName);
    });

    return profiles;
  } catch {
    return [];
  }
}

function toCookieMap(cookies: Array<{ name: string; value: string }>): Record<string, string> {
  const map: Record<string, string> = {};
  for (const cookie of cookies) {
    map[cookie.name] = cookie.value;
  }
  return map;
}

function buildNoCookieError(
  source: CookieSource,
  warnings: string[],
  checkedProfiles?: ChromeProfileInfo[]
): Error {
  const lines: string[] = [
    `No session cookie found for startupschool.org in ${source}.`,
    "",
  ];

  if (checkedProfiles && checkedProfiles.length > 0) {
    lines.push(
      `Checked ${checkedProfiles.length} Chrome profile(s): ` +
        checkedProfiles.map((p) => `"${p.dirName}" (${p.displayName})`).join(", ")
    );
    lines.push("");
  }

  if (warnings.length > 0) {
    lines.push("Warnings from cookie extraction:");
    for (const w of warnings) {
      lines.push(`  - ${w}`);
    }
    lines.push("");
  }

  lines.push(
    `Debug info:`,
    `  - Platform: ${process.platform}`,
    `  - Node: ${process.version}`,
    `  - Cookie source: ${source}`,
    "",
    "Troubleshooting:",
    "  1. Keychain access: when macOS prompts for your password, click 'Always Allow'",
    "     to avoid being asked again.",
    "  2. Login: open Chrome and visit https://www.startupschool.org/ — make sure you",
    "     are logged in and can see your dashboard.",
    "  3. Session expired: try logging out and back in on startupschool.org.",
    "  4. Non-standard browser: if you use Brave, Arc, or another Chromium browser,",
    "     try --cookie-source safari instead.",
  );

  return new Error(lines.join("\n"));
}

/**
 * Check if cookies contain a valid YC session.
 * YC uses Rails session cookies — the exact name may vary,
 * but we look for common Rails session cookie patterns.
 */
function hasValidSession(cookieMap: Record<string, string>): boolean {
  // Check for any cookie that looks like a session
  const sessionKeys = Object.keys(cookieMap).filter(
    (k) =>
      k.includes("session") ||
      k.includes("_sso") ||
      k === "_startup_school_session" ||
      k === "_ycombinator_session"
  );
  return sessionKeys.length > 0;
}

/**
 * Extract YC cookies from browser cookie store.
 * For Chrome on macOS, auto-discovers all profiles.
 */
export async function extractCookies(
  source: CookieSource = "chrome",
  chromeProfile?: string
): Promise<YcCookies> {
  const log = (msg: string) => console.error(kleur.dim(msg));

  // We need cookies from both startupschool.org and ycombinator.com
  // (SSO cookies may be on the ycombinator.com domain)
  const domains = [
    "https://www.startupschool.org/",
    "https://account.ycombinator.com/",
  ];

  if (chromeProfile || source !== "chrome") {
    log(`Reading cookies from ${source}${chromeProfile ? ` (profile: ${chromeProfile})` : ""}...`);

    const allCookies: Record<string, string> = {};
    for (const url of domains) {
      const result = await getCookies({
        url,
        browsers: [source],
        timeoutMs: 30_000,
        ...(chromeProfile ? { chromeProfile } : {}),
      });
      Object.assign(allCookies, toCookieMap(result.cookies));
    }

    if (!hasValidSession(allCookies)) {
      throw buildNoCookieError(source, []);
    }
    log(`Authenticated via ${source}.`);
    return allCookies as YcCookies;
  }

  // Auto-discover Chrome profiles
  const profiles = discoverChromeProfiles();

  if (profiles.length === 0) {
    log("Reading cookies from Chrome (default profile)...");
    const allCookies: Record<string, string> = {};
    for (const url of domains) {
      const result = await getCookies({
        url,
        browsers: [source],
        timeoutMs: 30_000,
      });
      Object.assign(allCookies, toCookieMap(result.cookies));
    }
    if (!hasValidSession(allCookies)) {
      throw buildNoCookieError(source, []);
    }
    log("Authenticated via Chrome.");
    return allCookies as YcCookies;
  }

  log(`Found ${profiles.length} Chrome profile(s): ${profiles.map((p) => `${p.dirName} (${p.displayName})`).join(", ")}`);

  const found: Array<{ profile: ChromeProfileInfo; cookies: Record<string, string> }> = [];
  let lastWarnings: string[] = [];

  for (const profile of profiles) {
    log(`  Checking "${profile.dirName}" (${profile.displayName})...`);
    const allCookies: Record<string, string> = {};
    for (const url of domains) {
      const result = await getCookies({
        url,
        browsers: ["chrome"],
        chromeProfile: profile.dirName,
        timeoutMs: 30_000,
      });
      lastWarnings = result.warnings;
      Object.assign(allCookies, toCookieMap(result.cookies));
    }

    if (hasValidSession(allCookies)) {
      log(`  -> Found YC session in "${profile.dirName}"`);
      found.push({ profile, cookies: allCookies });
    } else {
      log(`  -> No YC session`);
    }
  }

  if (found.length === 0) {
    throw buildNoCookieError(source, lastWarnings, profiles);
  }

  if (found.length === 1) {
    log(`Authenticated via Chrome profile "${found[0].profile.dirName}" (${found[0].profile.displayName}).`);
  } else {
    const names = found.map((f) => `"${f.profile.dirName}" (${f.profile.displayName})`);
    log(
      `Found YC sessions in ${found.length} profiles: ${names.join(", ")}. ` +
        `Using "${found[0].profile.dirName}". ` +
        `To choose a specific one: --chrome-profile "${found[found.length - 1].profile.dirName}"`
    );
  }

  return found[0].cookies as YcCookies;
}

/**
 * Format cookies as a cookie header string.
 */
export function cookiesToString(cookies: YcCookies): string {
  return Object.entries(cookies)
    .map(([k, v]) => `${k}=${v}`)
    .join("; ");
}
