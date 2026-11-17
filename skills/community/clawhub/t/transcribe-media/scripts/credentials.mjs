import { randomUUID } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import {
  chmod,
  lstat,
  mkdir,
  open,
  readFile,
  rename,
  rm,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";

export const AUDIOFLOW_TOKEN_PATTERN = /^vf_stt_[A-Za-z0-9_-]{43}$/u;
const POLL_SECRET_PATTERN = /^[A-Za-z0-9_-]{43}$/u;
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/iu;
const USER_CODE_PATTERN = /^[A-HJ-NP-Z2-9]{8}$/u;
const MAXIMUM_CREDENTIAL_BYTES = 32 * 1024;

function emptyState() {
  return Object.freeze({ version: 1 });
}

function asRecord(value, message = "AudioFlow credentials are invalid.") {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error(message);
  }
  return value;
}

function optionalString(value, pattern, message) {
  if (value === undefined) return undefined;
  if (typeof value !== "string" || !pattern.test(value)) {
    throw new Error(message);
  }
  return value;
}

function validTimestamp(value, message) {
  if (typeof value !== "string" || !Number.isFinite(Date.parse(value))) {
    throw new Error(message);
  }
  return value;
}

function parseActive(value) {
  if (value === undefined) return undefined;
  const active = asRecord(value);
  if (Object.hasOwn(active, "apiOrigin")) {
    throw new Error(
      "AudioFlow credentials contain the retired apiOrigin field. Remove apiOrigin and retry.",
    );
  }
  if (
    typeof active.token !== "string" ||
    !AUDIOFLOW_TOKEN_PATTERN.test(active.token) ||
    typeof active.approvedAt !== "string" ||
    !Number.isFinite(Date.parse(active.approvedAt))
  ) {
    throw new Error("AudioFlow credentials are invalid.");
  }
  return Object.freeze({
    token: active.token,
    approvedAt: active.approvedAt,
    ...(optionalString(
      active.apiTokenId,
      UUID_PATTERN,
      "AudioFlow credentials are invalid.",
    ) === undefined
      ? {}
      : { apiTokenId: active.apiTokenId }),
  });
}

function parsePending(value) {
  if (value === undefined) return undefined;
  const pending = asRecord(value);
  if (
    typeof pending.token !== "string" ||
    !AUDIOFLOW_TOKEN_PATTERN.test(pending.token) ||
    typeof pending.pollSecret !== "string" ||
    !POLL_SECRET_PATTERN.test(pending.pollSecret) ||
    typeof pending.clientName !== "string" ||
    pending.clientName.length < 1 ||
    pending.clientName.length > 64 ||
    (pending.clientVersion !== null &&
      (typeof pending.clientVersion !== "string" ||
        pending.clientVersion.length < 1 ||
        pending.clientVersion.length > 32))
  ) {
    throw new Error("AudioFlow pending credentials are invalid.");
  }
  const requestId = optionalString(
    pending.requestId,
    UUID_PATTERN,
    "AudioFlow pending credentials are invalid.",
  );
  const userCode = optionalString(
    pending.userCode,
    USER_CODE_PATTERN,
    "AudioFlow pending credentials are invalid.",
  );
  if ((requestId === undefined) !== (userCode === undefined)) {
    throw new Error("AudioFlow pending credentials are invalid.");
  }
  const complete = pending.verificationUriComplete;
  if (complete !== undefined) {
    let parsed;
    try {
      parsed = new URL(complete);
    } catch {
      throw new Error("AudioFlow pending credentials are invalid.");
    }
    if (
      parsed.origin !== "https://audioflow123.com" ||
      parsed.pathname !== "/connect-agent"
    ) {
      throw new Error("AudioFlow pending credentials are invalid.");
    }
  }
  return Object.freeze({
    token: pending.token,
    pollSecret: pending.pollSecret,
    clientName: pending.clientName,
    clientVersion: pending.clientVersion,
    startedAt: validTimestamp(
      pending.startedAt,
      "AudioFlow pending credentials are invalid.",
    ),
    ...(requestId === undefined ? {} : { requestId, userCode }),
    ...(complete === undefined ? {} : { verificationUriComplete: complete }),
    ...(pending.expiresAt === undefined
      ? {}
      : {
          expiresAt: validTimestamp(
            pending.expiresAt,
            "AudioFlow pending credentials are invalid.",
          ),
        }),
    ...(pending.interval === undefined
      ? {}
      : {
          interval:
            Number.isSafeInteger(pending.interval) && pending.interval >= 5
              ? pending.interval
              : (() => {
                  throw new Error("AudioFlow pending credentials are invalid.");
                })(),
        }),
  });
}

function parseState(value) {
  const state = asRecord(value);
  if (state.version !== 1) {
    throw new Error("AudioFlow credentials use an unsupported version.");
  }
  const active = parseActive(state.active);
  const pending = parsePending(state.pending);
  return Object.freeze({
    version: 1,
    ...(active === undefined ? {} : { active }),
    ...(pending === undefined ? {} : { pending }),
  });
}

export function resolveCredentialPath({
  environment = process.env,
  platform = process.platform,
  homeDirectory = os.homedir(),
} = {}) {
  const pathApi = platform === "win32" ? path.win32 : path.posix;
  const override = environment.AUDIOFLOW_CONFIG_DIR?.trim();
  if (override) {
    if (!pathApi.isAbsolute(override)) {
      throw new Error("AUDIOFLOW_CONFIG_DIR must be an absolute path.");
    }
    return pathApi.join(override, "credentials.json");
  }
  if (platform === "win32") {
    const appData = environment.APPDATA?.trim();
    if (!appData || !pathApi.isAbsolute(appData)) {
      throw new Error("APPDATA is unavailable for AudioFlow credentials.");
    }
    return pathApi.join(appData, "AudioFlow", "credentials.json");
  }
  const xdg = environment.XDG_CONFIG_HOME?.trim();
  const base =
    xdg && pathApi.isAbsolute(xdg)
      ? xdg
      : pathApi.join(homeDirectory, ".config");
  return pathApi.join(base, "audioflow", "credentials.json");
}

async function assertSafeCredentialFile(filePath) {
  const info = await lstat(filePath);
  if (!info.isFile() || info.isSymbolicLink()) {
    throw new Error("AudioFlow credential path is not a regular file.");
  }
  if (process.platform !== "win32" && (info.mode & 0o077) !== 0) {
    throw new Error("AudioFlow credential file permissions must be 0600.");
  }
  if (
    process.platform !== "win32" &&
    typeof process.getuid === "function" &&
    info.uid !== process.getuid()
  ) {
    throw new Error("AudioFlow credential file has an unexpected owner.");
  }
}

async function assertSafeCredentialDirectory(directory) {
  const info = await lstat(directory);
  if (!info.isDirectory() || info.isSymbolicLink()) {
    throw new Error(
      "AudioFlow credential directory is not a regular directory.",
    );
  }
  if (process.platform !== "win32" && (info.mode & 0o077) !== 0) {
    throw new Error("AudioFlow credential directory permissions must be 0700.");
  }
  if (
    process.platform !== "win32" &&
    typeof process.getuid === "function" &&
    info.uid !== process.getuid()
  ) {
    throw new Error("AudioFlow credential directory has an unexpected owner.");
  }
}

export async function readCredentialState(options = {}) {
  const filePath = resolveCredentialPath(options);
  try {
    await assertSafeCredentialFile(filePath);
    await assertSafeCredentialDirectory(path.dirname(filePath));
  } catch (error) {
    if (error && typeof error === "object" && error.code === "ENOENT") {
      return emptyState();
    }
    throw error;
  }
  const text = await readFile(filePath, "utf8");
  if (Buffer.byteLength(text, "utf8") > MAXIMUM_CREDENTIAL_BYTES) {
    throw new Error("AudioFlow credential file is too large.");
  }
  try {
    return parseState(JSON.parse(text));
  } catch (error) {
    if (error instanceof Error && error.message.startsWith("AudioFlow")) {
      throw error;
    }
    throw new Error("AudioFlow credentials are invalid.");
  }
}

export async function writeCredentialState(state, options = {}) {
  const normalized = parseState(state);
  const filePath = resolveCredentialPath(options);
  const directory = path.dirname(filePath);
  await mkdir(directory, { recursive: true, mode: 0o700 });
  if (process.platform !== "win32") await chmod(directory, 0o700);
  await assertSafeCredentialDirectory(directory);
  try {
    await assertSafeCredentialFile(filePath);
  } catch (error) {
    if (!(error && typeof error === "object" && error.code === "ENOENT")) {
      throw error;
    }
  }

  const temporaryPath = path.join(
    directory,
    `.credentials-${randomUUID()}.tmp`,
  );
  const handle = await open(
    temporaryPath,
    fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY,
    0o600,
  );
  try {
    await handle.writeFile(`${JSON.stringify(normalized, null, 2)}\n`, "utf8");
    await handle.sync();
  } finally {
    await handle.close();
  }
  try {
    if (process.platform !== "win32") await chmod(temporaryPath, 0o600);
    await rename(temporaryPath, filePath);
  } catch (error) {
    await rm(temporaryPath, { force: true });
    throw error;
  }
}

export async function loadAudioflowToken(options = {}) {
  const environment = options.environment ?? process.env;
  const candidate = environment.AUDIOFLOW_TOKEN?.trim() ?? "";
  if (candidate !== "") {
    if (!AUDIOFLOW_TOKEN_PATTERN.test(candidate)) {
      throw new Error("AUDIOFLOW_TOKEN is invalid.");
    }
    return Object.freeze({ token: candidate, source: "environment" });
  }
  const state = await readCredentialState(options);
  return state.active === undefined
    ? null
    : Object.freeze({ token: state.active.token, source: "configuration" });
}

export async function savePendingCredentials(pending, options = {}) {
  const state = await readCredentialState(options);
  await writeCredentialState({ ...state, pending }, options);
}

export async function clearPendingCredentials(options = {}) {
  const state = await readCredentialState(options);
  const { pending: _pending, ...remaining } = state;
  await writeCredentialState(remaining, options);
}

export async function promotePendingCredentials(
  { apiTokenId, approvedAt = new Date().toISOString() },
  options = {},
) {
  const state = await readCredentialState(options);
  if (state.pending === undefined) {
    throw new Error("No pending AudioFlow credentials are available.");
  }
  await writeCredentialState(
    {
      version: 1,
      active: {
        token: state.pending.token,
        approvedAt,
        ...(apiTokenId === null ? {} : { apiTokenId }),
      },
    },
    options,
  );
}

export function maskedToken(token) {
  if (!AUDIOFLOW_TOKEN_PATTERN.test(token)) {
    throw new Error("AudioFlow token is invalid.");
  }
  return `${token.slice(0, 15)}…${token.slice(-4)}`;
}
