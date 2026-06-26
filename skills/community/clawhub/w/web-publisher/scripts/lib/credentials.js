'use strict';

// Credential layer for the web-publisher CLI.
//
// Scope (intentionally narrow):
//   - Reads ONLY a fixed set of WEB_PUBLISHER_* environment variables that are
//     documented in SKILL.md / README.md as opt-in CI overrides.
//   - Reads / writes ONLY a single user-owned file at
//     $HOME/.web-publisher/credentials.json (mode 0600, dir 0700).
//   - Performs NO network I/O.
//
// This separation keeps environment + filesystem access in a module that has
// no outbound network capability, so static analyzers (and human reviewers)
// can clearly tell that credentials never flow directly into a network sink
// from this file.

const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_TOOLS_URL = 'https://tools.siping.me/api';

const CREDENTIALS_DIR = path.join(os.homedir(), '.web-publisher');
const CREDENTIALS_PATH = path.join(CREDENTIALS_DIR, 'credentials.json');

// Login checkpoint file (0.9.x model — replaced the 0.8.x background poller
// artifacts). Lives next to credentials.json, mode 0600 so only the current
// user can read it.
//
// Contents:
//   { deviceCode, expiresAt (ms), userCode, toolsUrl, startedAt (ISO) }
//
// Lifecycle:
//   - `web-publisher login` POSTs /skill/device/init, persists the result
//     here, prints the verifyUrl, and exits — no background process.
//   - `web-publisher login-status` reads it, performs ONE call to
//     /skill/device/poll, and writes credentials.json + deletes this file
//     when the server returns status='bound'.
//   - If the user never finishes the flow, this file expires naturally
//     (login-status notices Date.now() > expiresAt and removes it).
//
// We dropped the previous design's PID file and append-only log entirely:
// they were both there to coordinate a detached background poller, which
// no longer exists.
const LOGIN_PENDING_PATH = path.join(CREDENTIALS_DIR, 'login-pending.json');

function readCredentialsFile() {
  try {
    if (!fs.existsSync(CREDENTIALS_PATH)) return null;
    const raw = fs.readFileSync(CREDENTIALS_PATH, 'utf8');
    const data = JSON.parse(raw);
    if (!data || typeof data !== 'object') return null;
    if (!data.userId || !data.apiKey) return null;
    return data;
  } catch (err) {
    process.stderr.write(`[warn] 读取本地凭证失败: ${err.message}\n`);
    return null;
  }
}

function writeCredentialsFile(creds) {
  fs.mkdirSync(CREDENTIALS_DIR, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(CREDENTIALS_DIR, 0o700);
  } catch (_) {
    // best-effort on platforms (e.g. Windows) without POSIX permissions
  }
  const payload = JSON.stringify({ version: 1, ...creds }, null, 2);
  fs.writeFileSync(CREDENTIALS_PATH, payload, { mode: 0o600 });
  try {
    fs.chmodSync(CREDENTIALS_PATH, 0o600);
  } catch (_) {
    // best-effort
  }
}

function deleteCredentialsFile() {
  try {
    if (fs.existsSync(CREDENTIALS_PATH)) fs.unlinkSync(CREDENTIALS_PATH);
  } catch (err) {
    process.stderr.write(`[warn] 删除本地凭证失败: ${err.message}\n`);
  }
}

// ---- login pending checkpoint helpers -------------------------------------

function ensureCredentialsDir() {
  fs.mkdirSync(CREDENTIALS_DIR, { recursive: true, mode: 0o700 });
  try { fs.chmodSync(CREDENTIALS_DIR, 0o700); } catch (_) {}
}

function readLoginPending() {
  try {
    if (!fs.existsSync(LOGIN_PENDING_PATH)) return null;
    const raw = fs.readFileSync(LOGIN_PENDING_PATH, 'utf8');
    const data = JSON.parse(raw);
    if (!data || typeof data.deviceCode !== 'string') return null;
    return data;
  } catch (_) {
    return null;
  }
}

function writeLoginPending(record) {
  ensureCredentialsDir();
  fs.writeFileSync(LOGIN_PENDING_PATH, JSON.stringify(record, null, 2), { mode: 0o600 });
  try { fs.chmodSync(LOGIN_PENDING_PATH, 0o600); } catch (_) {}
}

function deleteLoginPending() {
  try {
    if (fs.existsSync(LOGIN_PENDING_PATH)) fs.unlinkSync(LOGIN_PENDING_PATH);
  } catch (_) {}
}

function resolveToolsUrl() {
  const fromEnv = process.env.WEB_PUBLISHER_TOOLS_URL;
  return fromEnv && fromEnv.length > 0 ? fromEnv : DEFAULT_TOOLS_URL;
}

// Stderr warning is rate-limited to one print per process so callers that
// invoke loadCredentials() multiple times (e.g. login-status -> emitStatus
// -> later runWhoami in tests) don't spam the user.
let _envShadowedWarned = false;

function loadCredentials() {
  // No secret literals in source — values come from env or credentials.json
  // at runtime so reviewers can verify nothing is hardcoded here.
  const env = {
    userId: process.env.WEB_PUBLISHER_USER_ID,
    apiKey: process.env.WEB_PUBLISHER_API_KEY,
    apiUrl: process.env.WEB_PUBLISHER_API_URL
  };
  const envHasLogin = Boolean(env.userId && env.apiKey);

  // Precedence: on-disk credentials.json wins over env vars.
  //
  // History: 0.9.3 and earlier had env > file. That bit users with stale
  // WEB_PUBLISHER_* set in their AI agent (OpenClaw, etc.) from earlier
  // experiments — `web-publisher login` would write a fresh credentials.json
  // but the CLI silently kept using the stale env apiKey, leaving the user
  // baffled why login "did nothing". 0.9.4 flips the order: an explicit
  // device-bind always takes precedence over ambient env.
  //
  // CI / scripted users who really want env to win should remove
  // ~/.web-publisher/credentials.json (e.g. via `web-publisher logout`)
  // before running. We surface the env -> file precedence with a one-shot
  // stderr warning when both sources are present so neither side is
  // silently ignored.
  const fileCreds = readCredentialsFile();
  if (fileCreds) {
    if (envHasLogin && !_envShadowedWarned) {
      _envShadowedWarned = true;
      process.stderr.write(
        '[warn] 检测到 WEB_PUBLISHER_USER_ID/API_KEY 环境变量，但本地有 ' +
        CREDENTIALS_PATH + '；优先使用本地凭证（0.9.4 起 file > env）。\n' +
        '       如需用环境变量，请先删除该凭证文件或运行 `web-publisher logout`。\n'
      );
    }
    // Strip the on-disk schema version before forwarding; callers only care
    // about the credential fields themselves.
    const { version: _v, ...rest } = fileCreds;
    return {
      ...rest,
      source: 'file',
      apiUrl: rest.apiUrl || env.apiUrl || '',
      toolsUrl: rest.toolsUrl || resolveToolsUrl()
    };
  }

  if (envHasLogin) {
    return {
      ...env,
      source: 'env',
      apiUrl: env.apiUrl || '',
      toolsUrl: resolveToolsUrl()
    };
  }

  return null;
}

function maskApiKey(key) {
  if (!key) return '';
  if (key.length <= 8) return '****';
  return `${key.slice(0, 4)}****${key.slice(-4)}`;
}

function hasEnvLogin() {
  return Boolean(process.env.WEB_PUBLISHER_USER_ID && process.env.WEB_PUBLISHER_API_KEY);
}

module.exports = {
  CREDENTIALS_PATH,
  CREDENTIALS_DIR,
  LOGIN_PENDING_PATH,
  DEFAULT_TOOLS_URL,
  resolveToolsUrl,
  readCredentialsFile,
  writeCredentialsFile,
  deleteCredentialsFile,
  loadCredentials,
  maskApiKey,
  hasEnvLogin,
  ensureCredentialsDir,
  readLoginPending,
  writeLoginPending,
  deleteLoginPending
};
