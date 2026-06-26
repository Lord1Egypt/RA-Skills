#!/usr/bin/env node
/**
 * Vexa API CLI (reusable skill helper)
 *
 * Env:
 * - VEXA_API_KEY (required)
 * - VEXA_BASE_URL (optional, default https://api.cloud.vexa.ai)
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SKILL_ROOT = path.join(__dirname, "..");
const SKILL_SECRETS_DIR = path.join(SKILL_ROOT, "secrets");
const SECRETS_FILE_SKILL = path.join(SKILL_SECRETS_DIR, "vexa.env");
const STATE_FILE_SKILL = path.join(SKILL_SECRETS_DIR, "vexa-state.json");
const ENDPOINTS_FILE = path.join(SKILL_SECRETS_DIR, "vexa-endpoints.json");
const SECRETS_FILE_HOME = path.join(os.homedir(), ".openclaw", "secrets", "vexa.env");
const STATE_FILE_HOME = path.join(os.homedir(), ".openclaw", "secrets", "vexa-state.json");

function getStateFile() {
  return fs.existsSync(STATE_FILE_SKILL) ? STATE_FILE_SKILL : STATE_FILE_HOME;
}

function getStateWriteFile() {
  return STATE_FILE_SKILL;
}

function loadVexaEnv() {
  if (process.env.VEXA_API_KEY?.trim()) return;
  // Try endpoint-specific env file first (e.g. vexa-prod.env, vexa-local.env)
  const endpointFiles = [];
  const epConfig = loadEndpointsConfig();
  if (epConfig?.active) {
    endpointFiles.push(path.join(SKILL_SECRETS_DIR, `vexa-${epConfig.active}.env`));
  }
  for (const file of [...endpointFiles, SECRETS_FILE_SKILL, SECRETS_FILE_HOME]) {
    try {
      const raw = fs.readFileSync(file, "utf8");
      for (const line of raw.split("\n")) {
        const rest = line.replace(/^\s*export\s+/, "").trim();
        const m = rest.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$/);
        if (m && !process.env[m[1]]) {
          process.env[m[1]] = m[2].replace(/^["']|["']$/g, "").trim();
        }
      }
      break;
    } catch {}
  }
}

loadVexaEnv();

/**
 * Endpoint environment switching.
 * File: secrets/vexa-endpoints.json
 * Format: { "active": "prod", "endpoints": { "prod": "https://api.cloud.vexa.ai", "local": "http://localhost:8000" } }
 * Priority: VEXA_BASE_URL env > endpoints config > default prod URL.
 */
function loadEndpointsConfig() {
  try {
    return JSON.parse(fs.readFileSync(ENDPOINTS_FILE, "utf8"));
  } catch {
    return null;
  }
}

function saveEndpointsConfig(config) {
  fs.mkdirSync(path.dirname(ENDPOINTS_FILE), { recursive: true });
  fs.writeFileSync(ENDPOINTS_FILE, JSON.stringify(config, null, 2) + "\n", { mode: 0o600 });
}

function getDefaultEndpointsConfig() {
  return {
    active: "prod",
    endpoints: {
      prod: "https://api.cloud.vexa.ai",
      local: "http://localhost:8000"
    }
  };
}

/**
 * Normalize endpoint config: supports both legacy string format and new object format.
 * Legacy: { "endpoints": { "prod": "https://..." } }
 * New:    { "endpoints": { "prod": { "url": "https://...", "apiKey": "..." } } }
 */
function getEndpointEntry(config, name) {
  if (!config?.endpoints?.[name]) return null;
  const entry = config.endpoints[name];
  if (typeof entry === "string") return { url: entry, apiKey: null };
  return { url: entry.url || null, apiKey: entry.apiKey || null };
}

function resolveBaseUrl() {
  // Explicit env var always wins
  if (process.env.VEXA_BASE_URL?.trim()) return process.env.VEXA_BASE_URL.trim().replace(/\/$/, "");
  const config = loadEndpointsConfig();
  const entry = getEndpointEntry(config, config?.active);
  if (entry?.url) return entry.url.replace(/\/$/, "");
  return "https://api.cloud.vexa.ai";
}

function resolveApiKey() {
  // Explicit env var always wins
  if (process.env.VEXA_API_KEY?.trim()) {
    // But check if active endpoint has its own key — prefer that
    const config = loadEndpointsConfig();
    const entry = getEndpointEntry(config, config?.active);
    if (entry?.apiKey) return entry.apiKey;
    return process.env.VEXA_API_KEY.trim();
  }
  // Try endpoint-specific key
  const config = loadEndpointsConfig();
  const entry = getEndpointEntry(config, config?.active);
  if (entry?.apiKey) return entry.apiKey;
  return process.env.VEXA_API_KEY || null;
}

const BASE_URL = resolveBaseUrl();
const API_KEY = resolveApiKey();

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1];
      if (v == null || v.startsWith("--")) out[k] = true;
      else {
        out[k] = v;
        i++;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

function readState() {
  const stateFile = getStateFile();
  try {
    const raw = fs.readFileSync(stateFile, "utf8");
    const parsed = JSON.parse(raw);
    return { first_use: parsed?.first_use !== false };
  } catch {
    return { first_use: true };
  }
}

function writeState(state) {
  const stateFile = getStateWriteFile();
  const dir = path.dirname(stateFile);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2) + "\n", { mode: 0o600 });
  try { fs.chmodSync(stateFile, 0o600); } catch {}
}

function forwardOnboardingArgs(args) {
  const keys = ["api_key", "meeting_url", "platform", "native_meeting_id", "passcode", "language", "bot_name", "persist", "wait_seconds", "poll_every_seconds"];
  const out = [];
  for (const k of keys) {
    if (args[k] === undefined) continue;
    out.push(`--${k}`);
    if (args[k] !== true) out.push(String(args[k]));
  }
  return out;
}

function runOnboardingAndExit(args) {
  const onboardScript = path.join(__dirname, "onboard.mjs");
  const result = spawnSync(process.execPath, [onboardScript, ...forwardOnboardingArgs(args)], {
    stdio: "inherit",
    env: process.env
  });
  process.exit(result.status ?? 1);
}

function ensureConfiguredOrOnboard(cmd) {
  if (cmd === "parse:meeting-url" || cmd === "onboard") return;

  const state = readState();

  if (API_KEY) {
    if (state.first_use) {
      writeState({ first_use: false, configured_at: new Date().toISOString() });
    }
    return;
  }

  die("Missing VEXA_API_KEY. Source skills/vexa/secrets/vexa.env or run: node skills/vexa/scripts/onboard.mjs");
}

function csv(value) {
  if (value == null || value === true) return undefined;
  return String(value).split(",").map((s) => s.trim()).filter(Boolean);
}

function assertDeleteGuard(args, scopeLabel) {
  if (!args.confirm) die(`Refusing destructive call (${scopeLabel}). Re-run with --confirm DELETE.`);
  if (String(args.confirm) !== "DELETE") die("Invalid --confirm value. Expected exactly: DELETE");
}

function normalizeGoogleMeetId(raw) {
  if (!raw) return null;
  const v = String(raw).trim();
  if (/^[a-z]{3}-[a-z]{4}-[a-z]{3}$/i.test(v)) return v.toLowerCase();
  try {
    const u = new URL(v);
    if (!/meet\.google\.com$/i.test(u.hostname)) return null;
    const m = u.pathname.match(/\/([a-z]{3}-[a-z]{4}-[a-z]{3})/i);
    return m?.[1]?.toLowerCase() || null;
  } catch {
    return null;
  }
}

function normalizeZoomInfo(raw) {
  if (!raw) return null;
  const v = String(raw).trim();
  // Bare numeric ID (10-11 digits)
  if (/^\d{10,11}$/.test(v)) return { native_meeting_id: v, passcode: null };
  try {
    const u = new URL(v);
    if (!/zoom\.us$/i.test(u.hostname)) return null;
    // Typical paths: /j/<id> or /w/<id>
    const parts = u.pathname.split("/").filter(Boolean);
    if (parts.length < 2 || !["j", "w"].includes(parts[0])) return null;
    const nativeId = parts[1];
    if (!/^\d{10,11}$/.test(nativeId)) return null;
    const passcode = u.searchParams.get("pwd") || null;
    return { native_meeting_id: nativeId, passcode };
  } catch {
    return null;
  }
}

function normalizeTeamsInfo(raw) {
  if (!raw) return null;
  const v = String(raw).trim();
  if (/^\d{10,15}$/.test(v)) return { native_meeting_id: v, passcode: null };
  try {
    const u = new URL(v);
    if (!/teams\./i.test(u.hostname)) return null;
    const m = u.pathname.match(/\/meet\/(\d{10,15})/i);
    const native_meeting_id = m?.[1] || null;
    const passcode = u.searchParams.get("p") || null;
    if (!native_meeting_id) return null;
    return { native_meeting_id, passcode };
  } catch {
    return null;
  }
}

function parseMeetingInput({ meeting_url, platform, native_meeting_id, passcode }) {
  // Explicit platform/id wins.
  if (platform && native_meeting_id) {
    return {
      platform,
      native_meeting_id: String(native_meeting_id),
      passcode: passcode ? String(passcode) : undefined
    };
  }

  if (!meeting_url) return null;

  const g = normalizeGoogleMeetId(meeting_url);
  if (g) return { platform: "google_meet", native_meeting_id: g };

  const t = normalizeTeamsInfo(meeting_url);
  if (t) return {
    platform: "teams",
    native_meeting_id: t.native_meeting_id,
    passcode: t.passcode || (passcode ? String(passcode) : undefined)
  };

  const z = normalizeZoomInfo(meeting_url);
  if (z) return {
    platform: "zoom",
    native_meeting_id: z.native_meeting_id,
    passcode: z.passcode || (passcode ? String(passcode) : undefined)
  };

  return null;
}

async function vexaFetch(path, { method = "GET", body } = {}) {
  if (!API_KEY) die("Missing VEXA_API_KEY. Source ~/.openclaw/secrets/vexa.env or run: node skills/vexa/scripts/onboard.mjs");

  const url = `${BASE_URL}${path}`;
  const headers = {
    "X-API-Key": API_KEY,
    Accept: "application/json"
  };
  if (body !== undefined) headers["Content-Type"] = "application/json";

  const res = await fetch(url, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body)
  });

  const text = await res.text();
  let json;
  try { json = text ? JSON.parse(text) : null; } catch { json = { raw: text }; }

  if (!res.ok) {
    const msg = typeof json === "object" ? JSON.stringify(json, null, 2) : String(json);
    die(`Vexa API error ${res.status} ${res.statusText}\n${msg}`);
  }

  return json;
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + "\n");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];

  ensureConfiguredOrOnboard(cmd);

  switch (cmd) {
    case "onboard": {
      runOnboardingAndExit(args);
      return;
    }
    case "parse:meeting-url": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id,
        passcode: args.passcode
      });
      if (!parsed) {
        die("Unable to parse meeting input. Pass --meeting_url (Google Meet/Teams/Zoom) or --platform + --native_meeting_id.");
      }
      return print({ ok: true, ...parsed });
    }

    case "bots:status": {
      return print(await vexaFetch("/bots/status"));
    }

    case "meetings:list": {
      return print(await vexaFetch("/meetings"));
    }

    case "bots:start": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id,
        passcode: args.passcode
      });

      if (!parsed) {
        die("Usage: bots:start (--meeting_url <url> | --platform <google_meet|teams|zoom> --native_meeting_id <id>) [--passcode ...] [--bot_name ...] [--language ...]");
      }

      if (parsed.platform === "teams" && !parsed.passcode) {
        die("Teams bot join requires passcode. Provide --passcode or a Teams URL containing ?p=...");
      }

      const body = {
        platform: parsed.platform,
        native_meeting_id: parsed.native_meeting_id,
        passcode: parsed.passcode ?? undefined,
        bot_name: args.bot_name ?? undefined,
        language: args.language ?? undefined
      };

      return print(await vexaFetch("/bots", { method: "POST", body }));
    }

    case "bots:stop": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id,
        passcode: args.passcode
      });
      if (!parsed) {
        die("Usage: bots:stop (--meeting_url <url> | --platform <google_meet|teams|zoom> --native_meeting_id <id>)");
      }
      return print(await vexaFetch(`/bots/${encodeURIComponent(parsed.platform)}/${encodeURIComponent(parsed.native_meeting_id)}`, { method: "DELETE" }));
    }

    case "bots:config:update": {
      const { platform, native_meeting_id, language } = args;
      if (!platform || !native_meeting_id || !language) {
        die("Usage: bots:config:update --platform <google_meet|teams> --native_meeting_id <id> --language <code>");
      }
      return print(await vexaFetch(`/bots/${encodeURIComponent(platform)}/${encodeURIComponent(native_meeting_id)}/config`, {
        method: "PUT",
        body: { language }
      }));
    }

    case "transcripts:get": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id,
        passcode: args.passcode
      });
      if (!parsed) {
        die("Usage: transcripts:get (--meeting_url <url> | --platform <google_meet|teams> --native_meeting_id <id>)");
      }
      return print(await vexaFetch(`/transcripts/${encodeURIComponent(parsed.platform)}/${encodeURIComponent(parsed.native_meeting_id)}`));
    }

    case "transcripts:share": {
      const { platform, native_meeting_id, meeting_id, ttl_seconds } = args;
      if (!platform || !native_meeting_id) {
        die("Usage: transcripts:share --platform <google_meet|teams> --native_meeting_id <id> [--meeting_id <int>] [--ttl_seconds <int>]");
      }
      const qs = new URLSearchParams();
      if (meeting_id !== undefined) qs.set("meeting_id", String(meeting_id));
      if (ttl_seconds !== undefined) qs.set("ttl_seconds", String(ttl_seconds));
      const suffix = qs.toString() ? `?${qs.toString()}` : "";
      return print(await vexaFetch(`/transcripts/${encodeURIComponent(platform)}/${encodeURIComponent(native_meeting_id)}/share${suffix}`, { method: "POST" }));
    }

    case "meetings:update": {
      const { platform, native_meeting_id, name, notes } = args;
      const participants = csv(args.participants);
      const languages = csv(args.languages);
      if (!platform || !native_meeting_id) {
        die("Usage: meetings:update --platform <google_meet|teams> --native_meeting_id <id> [--name ...] [--participants a,b] [--languages en,es] [--notes ...]");
      }
      const data = {};
      if (name !== undefined) data.name = String(name);
      if (notes !== undefined) data.notes = String(notes);
      if (participants !== undefined) data.participants = participants;
      if (languages !== undefined) data.languages = languages;
      if (Object.keys(data).length === 0) die("Nothing to update. Provide at least one updatable field.");
      return print(await vexaFetch(`/meetings/${encodeURIComponent(platform)}/${encodeURIComponent(native_meeting_id)}`, {
        method: "PATCH",
        body: { data }
      }));
    }

    case "meetings:delete": {
      const { platform, native_meeting_id } = args;
      if (!platform || !native_meeting_id) {
        die("Usage: meetings:delete --platform <google_meet|teams> --native_meeting_id <id> --confirm DELETE");
      }
      assertDeleteGuard(args, `meeting ${platform}/${native_meeting_id}`);
      return print(await vexaFetch(`/meetings/${encodeURIComponent(platform)}/${encodeURIComponent(native_meeting_id)}`, { method: "DELETE" }));
    }

    case "report":
    case "meetings:report": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id
      });
      if (!parsed) {
        die("Usage: report (--meeting_url <url> | --platform <google_meet|teams> --native_meeting_id <id>)");
      }
      const ingestScript = path.join(__dirname, "ingest.mjs");
      const ingestArgs = args.meeting_url
        ? ["--meeting_url", args.meeting_url]
        : ["--platform", parsed.platform, "--native_meeting_id", parsed.native_meeting_id];
      const result = spawnSync(process.execPath, [ingestScript, ...ingestArgs], {
        stdio: "inherit",
        env: process.env
      });
      process.exit(result.status ?? 1);
    }

    case "user:webhook:set": {
      const { webhook_url } = args;
      if (!webhook_url) die("Usage: user:webhook:set --webhook_url https://example.com/path");
      return print(await vexaFetch("/user/webhook", { method: "PUT", body: { webhook_url: String(webhook_url) } }));
    }

    case "voice-agent:config:get": {
      return print(await vexaFetch("/voice-agent-config"));
    }

    case "voice-agent:config:set": {
      const { prompt } = args;
      if (!prompt) die("Usage: voice-agent:config:set --prompt \"Your system prompt here\"");
      return print(await vexaFetch("/voice-agent-config", { method: "PUT", body: { ultravox_system_prompt: String(prompt) } }));
    }

    case "voice-agent:config:reset": {
      return print(await vexaFetch("/voice-agent-config", { method: "PUT", body: { ultravox_system_prompt: null } }));
    }

    case "env:list": {
      const config = loadEndpointsConfig() || getDefaultEndpointsConfig();
      // Show endpoints with key status (masked)
      const display = {};
      for (const [name, val] of Object.entries(config.endpoints || {})) {
        const entry = getEndpointEntry(config, name);
        const epEnvFile = path.join(SKILL_SECRETS_DIR, `vexa-${name}.env`);
        const hasEpEnv = fs.existsSync(epEnvFile);
        display[name] = {
          url: entry?.url || val,
          apiKey: entry?.apiKey ? entry.apiKey.slice(0, 6) + "..." : hasEpEnv ? `(from vexa-${name}.env)` : "(from vexa.env)",
          envFile: hasEpEnv ? `vexa-${name}.env` : "vexa.env (fallback)"
        };
      }
      const result = { active: config.active, activeUrl: BASE_URL, activeApiKey: API_KEY ? API_KEY.slice(0, 6) + "..." : null, endpoints: display };
      return print(result);
    }

    case "env:use": {
      const envName = args._[1] || args.name;
      if (!envName) die("Usage: env:use <name>  (e.g. prod, local)");
      const config = loadEndpointsConfig() || getDefaultEndpointsConfig();
      if (!config.endpoints[envName]) die(`Unknown environment "${envName}". Available: ${Object.keys(config.endpoints).join(", ")}`);
      config.active = envName;
      saveEndpointsConfig(config);
      const entry = getEndpointEntry(config, envName);
      return print({ ok: true, active: envName, url: entry?.url, apiKey: entry?.apiKey ? entry.apiKey.slice(0, 6) + "..." : "(from vexa.env)" });
    }

    case "env:set": {
      const envName = args._[1] || args.name;
      const url = args.url;
      const apiKey = args.api_key || args.apiKey;
      if (!envName || !url) die("Usage: env:set <name> --url <base_url> [--api_key <key>]  (e.g. env:set staging --url https://staging.vexa.ai --api_key sk-...)");
      const config = loadEndpointsConfig() || getDefaultEndpointsConfig();
      // Store as object if apiKey provided, otherwise keep string for backward compat
      if (apiKey) {
        const existing = getEndpointEntry(config, envName);
        config.endpoints[envName] = { url, apiKey };
      } else {
        // Preserve existing apiKey if just updating URL
        const existing = getEndpointEntry(config, envName);
        if (existing?.apiKey) {
          config.endpoints[envName] = { url, apiKey: existing.apiKey };
        } else {
          config.endpoints[envName] = url;
        }
      }
      saveEndpointsConfig(config);
      return print({ ok: true, endpoints: Object.keys(config.endpoints) });
    }

    case "recordings:list": {
      const qs = new URLSearchParams();
      if (args.limit !== undefined) qs.set("limit", String(args.limit));
      if (args.offset !== undefined) qs.set("offset", String(args.offset));
      if (args.meeting_id !== undefined) qs.set("meeting_id", String(args.meeting_id));
      const suffix = qs.toString() ? `?${qs.toString()}` : "";
      return print(await vexaFetch(`/recordings${suffix}`));
    }

    case "recordings:get": {
      const id = args._[1] || args.id;
      if (!id) die("Usage: recordings:get <recording_id>");
      return print(await vexaFetch(`/recordings/${encodeURIComponent(id)}`));
    }

    case "recordings:delete": {
      const id = args._[1] || args.id;
      if (!id) die("Usage: recordings:delete <recording_id> --confirm DELETE");
      assertDeleteGuard(args, `recording ${id}`);
      return print(await vexaFetch(`/recordings/${encodeURIComponent(id)}`, { method: "DELETE" }));
    }

    case "recordings:download": {
      const recordingId = args._[1] || args.recording_id;
      const mediaFileId = args._[2] || args.media_file_id;
      if (!recordingId || !mediaFileId) die("Usage: recordings:download <recording_id> <media_file_id>");
      return print(await vexaFetch(`/recordings/${encodeURIComponent(recordingId)}/media/${encodeURIComponent(mediaFileId)}/download`));
    }

    case "recordings:config:get": {
      return print(await vexaFetch("/recording-config"));
    }

    case "recordings:config:update": {
      const body = {};
      if (args.enabled !== undefined) body.enabled = String(args.enabled) === "true";
      if (args.capture_modes !== undefined) body.capture_modes = csv(args.capture_modes);
      if (Object.keys(body).length === 0) die("Usage: recordings:config:update [--enabled true|false] [--capture_modes audio,video]");
      return print(await vexaFetch("/recording-config", { method: "PUT", body }));
    }

    case "meetings:bundle": {
      const parsed = parseMeetingInput({
        meeting_url: args.meeting_url,
        platform: args.platform,
        native_meeting_id: args.native_meeting_id,
        passcode: args.passcode
      });
      if (!parsed) {
        die("Usage: meetings:bundle (--meeting_url <url> | --platform <google_meet|teams|zoom> --native_meeting_id <id>) [--segments] [--no-share] [--no-recordings] [--download-urls]");
      }
      // Fetch transcript
      const transcript = await vexaFetch(`/transcripts/${encodeURIComponent(parsed.platform)}/${encodeURIComponent(parsed.native_meeting_id)}`);
      const result = { ...transcript };

      // Optionally strip segments (default: strip them to keep output small)
      if (!args.segments) delete result.segments;

      // Optionally strip recordings
      if (args["no-recordings"]) delete result.recordings;

      // Optionally resolve download URLs for recordings
      if (args["download-urls"] && Array.isArray(result.recordings)) {
        for (const rec of result.recordings) {
          if (!rec?.id || !Array.isArray(rec.media_files)) continue;
          for (const mf of rec.media_files) {
            if (!mf?.id) continue;
            try {
              mf.download = await vexaFetch(`/recordings/${encodeURIComponent(rec.id)}/media/${encodeURIComponent(mf.id)}/download`);
            } catch {}
          }
        }
      }

      // Optionally create share link (default: yes)
      if (!args["no-share"]) {
        const shareQs = new URLSearchParams();
        if (args.ttl_seconds !== undefined) shareQs.set("ttl_seconds", String(args.ttl_seconds));
        const shareSuffix = shareQs.toString() ? `?${shareQs.toString()}` : "";
        try {
          result.share_link = await vexaFetch(
            `/transcripts/${encodeURIComponent(parsed.platform)}/${encodeURIComponent(parsed.native_meeting_id)}/share${shareSuffix}`,
            { method: "POST" }
          );
        } catch (e) {
          result.share_link_error = String(e);
        }
      }

      return print(result);
    }

    case "env:remove": {
      const envName = args._[1] || args.name;
      if (!envName) die("Usage: env:remove <name>");
      const config = loadEndpointsConfig() || getDefaultEndpointsConfig();
      if (config.active === envName) die(`Cannot remove active environment "${envName}". Switch to another first with env:use.`);
      delete config.endpoints[envName];
      saveEndpointsConfig(config);
      return print({ ok: true, endpoints: config.endpoints });
    }

    default: {
      die([
        "Unknown or missing command.",
        "Commands:",
        "  parse:meeting-url --meeting_url <url>",
        "  bots:status",
        "  bots:start (--meeting_url <url> | --platform ... --native_meeting_id ...) [--passcode ...] [--bot_name ...] [--language ...]",
        "  bots:stop --platform ... --native_meeting_id ...",
        "  bots:config:update --platform ... --native_meeting_id ... --language ...",
        "  meetings:list",
        "  meetings:update --platform ... --native_meeting_id ... [--name ...] [--participants a,b] [--languages en,es] [--notes ...]",
        "  meetings:delete --platform ... --native_meeting_id ... --confirm DELETE",
        "  meetings:bundle (--meeting_url <url> | --platform ... --native_meeting_id ...) [--segments] [--no-share] [--no-recordings] [--download-urls]",
        "  report (--meeting_url <url> | --platform ... --native_meeting_id ...)",
        "  transcripts:get --platform ... --native_meeting_id ...",
        "  transcripts:share --platform ... --native_meeting_id ... [--meeting_id ...] [--ttl_seconds ...]",
        "  recordings:list [--limit ...] [--offset ...] [--meeting_id ...]",
        "  recordings:get <recording_id>",
        "  recordings:delete <recording_id> --confirm DELETE",
        "  recordings:download <recording_id> <media_file_id>",
        "  recordings:config:get",
        "  recordings:config:update [--enabled true|false] [--capture_modes audio,video]",
        "  user:webhook:set --webhook_url https://...",
        "  voice-agent:config:get",
        "  voice-agent:config:set --prompt \"Your system prompt\"",
        "  voice-agent:config:reset",
        "  env:list",
        "  env:use <name>                  (switch active endpoint: prod, local, etc.)",
        "  env:set <name> --url <base_url> (add/update a named endpoint)",
        "  env:remove <name>               (remove a named endpoint)",
      ].join("\n"));
    }
  }
}

main().catch((err) => {
  console.error(err?.stack || String(err));
  process.exit(1);
});
