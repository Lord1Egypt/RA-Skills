import crypto from "node:crypto";
import fs from "node:fs";
import fsp from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const { constants: FS } = fs;

export const SCHEMA_VERSION = 1;
export const STORE_FILE = "store-v1.json";
export const BACKUP_FILE = "store-v1.json.bak";
export const LOCK_FILE = "store-v1.json.lock";
export const REPAIR_CONFIRMATION = "repair-local-store";
export const RESET_CONFIRMATION = "reset-local-store";
export const DEFAULT_LIMITS = Object.freeze({
  rooms: 128,
  groups: 128,
  devices: 512,
  scenes: 256,
  schedules: 128,
  operations: 32,
});

export class StoreError extends Error {
  constructor(code, message = code, details = undefined) {
    super(message);
    this.name = "StoreError";
    this.code = code;
    if (details !== undefined) this.details = details;
  }
}

function fail(code, message = code, details) {
  throw new StoreError(code, message, details);
}

function nowIso(value = Date.now()) {
  if (typeof value === "function") value = value();
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) fail("store_invalid_timestamp", "Invalid store timestamp.");
  return date.toISOString();
}

function randomId(prefix = "") {
  return `${prefix}${crypto.randomUUID()}`;
}

function randomToken() {
  return crypto.randomBytes(32).toString("base64url");
}

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function sameJson(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function isObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

const SAFE_STATE_KEYS = new Set([
  "power", "bright", "brightness", "ct", "rgb", "hue", "sat", "color_mode",
  "flowing", "delayoff", "music_on", "bg_power", "bg_bright", "bg_ct", "bg_rgb",
  "bg_hue", "bg_sat",
]);
const SAFE_CAPABILITY_KEYS = new Set([
  "power", "switch", "brightness", "bright", "colorTemperature", "temperature", "ct",
  "color", "rgb", "hsv", "flow", "effect", "adjustment", "adjust", "relative",
  "foreground", "background",
]);
const SAFE_SCENE_SET_KEYS = new Set([
  "power", "brightness", "colorTemperature", "color", "hue", "saturation",
  "bgPower", "bgBrightness", "bgColorTemperature", "bgColor", "bgHue", "bgSaturation",
]);
const SCOPE_REFERENCE_KINDS = Object.freeze({ room: "rooms", group: "groups", device: "devices" });

function hasControl(value) {
  return typeof value === "string" && /[\u0000-\u001f\u007f]/u.test(value);
}

function boundedString(value, max, { allowEmpty = true } = {}) {
  if (typeof value !== "string" || value.length > max || hasControl(value)) return false;
  return allowEmpty || value.length > 0;
}

function validId(value, { min = 1, max = 160 } = {}) {
  return typeof value === "string" && value.length >= min && value.length <= max && !hasControl(value)
    && !/[\r\n]/u.test(value) && !/[\\/]/u.test(value);
}

function validDate(value) {
  return typeof value === "string" && value.length <= 64 && !Number.isNaN(Date.parse(value));
}

function validEntity(entity, kind, limits = DEFAULT_LIMITS) {
  // Protocol IDs and read-only catalog IDs are stable even when short (for
  // example the recommended `away` scene); length is bounded, not padded.
  const minimumIdLength = 1;
  const recoveryRecord = kind === "operation" && entity.kind === "scene-apply" && entity.schemaVersion === 1;
  if (!isObject(entity) || !validId(entity.id, { min: minimumIdLength }) || (!recoveryRecord && (!Number.isInteger(entity.revision) || entity.revision < 1)) || !validDate(entity.createdAt) || !validDate(entity.updatedAt)) return false;
  if (entity.updatedAt < entity.createdAt) return false;
  if (kind === "home") return boundedString(entity.name, 80, { allowEmpty: false });
  if (kind === "room") {
    return boundedString(entity.name, 80, { allowEmpty: false })
      && Array.isArray(entity.deviceIds) && entity.deviceIds.length <= limits.devices
      && uniqueStrings(entity.deviceIds, 160);
  }
  if (kind === "group") {
    const members = entity.memberIds || entity.deviceIds;
    return boundedString(entity.name, 80, { allowEmpty: false })
      && Array.isArray(members) && members.length >= 2 && members.length <= limits.devices
      && uniqueStrings(members, 160)
      && boundedString(entity.fingerprint || entity.capabilityFingerprint, 4096, { allowEmpty: false })
      && ["active", "needs_review"].includes(entity.status);
  }
  if (kind === "device") {
    const protocolId = entity.protocolId || entity.id;
    return validId(protocolId)
      && entity.id === protocolId
      && boundedString(entity.alias ?? entity.localAlias ?? "", 80)
      && (entity.roomId === null || entity.roomId === undefined || validId(entity.roomId))
      && Array.isArray(entity.groupIds) && entity.groupIds.length <= limits.groups && uniqueStrings(entity.groupIds, 160)
      && Array.isArray(entity.support) && entity.support.length <= 128 && uniqueStrings(entity.support, 96)
      && typeof entity.online === "boolean" && typeof entity.stale === "boolean"
      && isObject(entity.rebind) && ["active", "rebind_pending"].includes(entity.rebind.status);
  }
  if (kind === "scene") return boundedString(entity.name, 80, { allowEmpty: false }) && ["custom", "snapshot", "recommended"].includes(entity.source);
  if (kind === "schedule") {
    const state = entity.state ?? entity.status;
    return boundedString(entity.name, 80, { allowEmpty: false }) && ["draft", "inactive", "binding_pending", "enabled", "active", "paused", "delete_pending"].includes(state);
  }
  if (kind === "operation") return ["pending", "running", "success", "partial", "uncertain", "failed", "manual_recovery_required", "complete", "conflict"].includes(entity.status);
  return false;
}

function uniqueStrings(values, max) {
  return values.every((value) => validId(String(value), { max })) && new Set(values).size === values.length;
}

function assertNoSecrets(value, pathName = "store") {
  if (Array.isArray(value)) {
    for (let index = 0; index < value.length; index += 1) assertNoSecrets(value[index], `${pathName}[${index}]`);
    return;
  }
  if (!isObject(value)) return;
  for (const [key, child] of Object.entries(value)) {
    if (/^(?:access[_-]?token|refresh[_-]?token|auth[_-]?token|bearer|client[_-]?secret|authorization|password|credential|transcript|raw[_-]?(?:packet|response)|notification(?:s|History))$/iu.test(key)) {
      fail("store_sensitive_field", `Sensitive field is not allowed at ${pathName}.${key}.`);
    }
    assertNoSecrets(child, `${pathName}.${key}`);
  }
}

export function validateStore(value, options = {}) {
  const limits = { ...DEFAULT_LIMITS, ...(options.limits || {}) };
  try {
    if (!isObject(value) || value.schemaVersion !== SCHEMA_VERSION || !validId(value.storeId, { min: 8 }) || !Number.isInteger(value.revision) || value.revision < 1 || !validDate(value.updatedAt)) fail("store_invalid_shape", "Store header is invalid.");
    const allowedTopLevel = new Set(["schemaVersion", "storeId", "revision", "updatedAt", "home", "rooms", "groups", "devices", "scenes", "schedules", "operations"]);
    if (Object.keys(value).some((key) => !allowedTopLevel.has(key))) fail("store_invalid_shape", "Store contains an unsupported top-level field.");
    for (const key of ["home", "rooms", "groups", "devices", "scenes", "schedules", "operations"]) {
      if (!Object.hasOwn(value, key)) fail("store_invalid_shape", `Store field ${key} is missing.`);
    }
    if (!validEntity(value.home, "home", limits)) fail("store_invalid_home", "Home record is invalid.");
    for (const [kind, max] of Object.entries(limits)) {
      if (!Array.isArray(value[kind]) || value[kind].length > max) fail("store_collection_limit", `${kind} exceeds its local bound.`);
    }
    const collections = ["rooms", "groups", "devices", "scenes", "schedules", "operations"];
    for (const kind of collections) {
      const ids = new Set();
      for (const entity of value[kind]) {
        const entityKind = kind.endsWith("ies") ? `${kind.slice(0, -3)}y` : kind.endsWith("s") ? kind.slice(0, -1) : kind;
        if (!validEntity(entity, entityKind, limits) || ids.has(entity.id)) fail("store_invalid_entity", `${kind} contains an invalid or duplicate entity.`);
        ids.add(entity.id);
      }
    }
    const roomIds = new Set(value.rooms.map((room) => room.id));
    const deviceIds = new Set(value.devices.map((device) => device.id));
    const groupIds = new Set(value.groups.map((group) => group.id));
    for (const room of value.rooms) if (room.deviceIds.some((id) => !deviceIds.has(id))) fail("store_dangling_reference", "Room references an unknown device.");
    for (const device of value.devices) {
      if (device.roomId !== null && device.roomId !== undefined && !roomIds.has(device.roomId)) fail("store_dangling_reference", "Device references an unknown room.");
      if (device.groupIds.some((id) => !groupIds.has(id))) fail("store_dangling_reference", "Device references an unknown group.");
      if (device.protocolId !== device.id) fail("store_identity_mismatch", "Device id and protocolId must match.");
    }
    for (const group of value.groups) {
      const members = group.memberIds || group.deviceIds;
      if (members.some((id) => !deviceIds.has(id))) fail("store_dangling_reference", "Group references an unknown device.");
      if (group.deviceIds && JSON.stringify(group.deviceIds) !== JSON.stringify(members)) fail("store_group_membership_mismatch", "Group member aliases differ.");
    }
    for (const room of value.rooms) {
      const expected = value.devices.filter((device) => device.roomId === room.id).map((device) => device.id).sort();
      const actual = [...room.deviceIds].sort();
      if (JSON.stringify(expected) !== JSON.stringify(actual)) fail("store_room_membership_mismatch", "Room and device room references differ.");
    }
    for (const group of value.groups) {
      const members = group.memberIds || group.deviceIds;
      for (const id of members) {
        const device = value.devices.find((candidate) => candidate.id === id);
        if (!device.groupIds.includes(group.id)) fail("store_group_membership_mismatch", "Device and group references differ.");
      }
    }
    assertNoSecrets(value);
    return true;
  } catch (error) {
    if (options.throwOnError === false) return false;
    if (error instanceof StoreError) throw error;
    throw new StoreError("store_invalid_shape", "Store validation failed.", { cause: error?.message });
  }
}

export const isValidStore = (value, options = {}) => validateStore(value, { ...options, throwOnError: false });

export function createEmptyStore(options = {}) {
  const timestamp = nowIso(options.now ?? Date.now());
  const home = {
    id: options.homeId && validId(options.homeId, { min: 8 }) ? options.homeId : randomId("home-"),
    name: typeof options.homeName === "string" && options.homeName.trim() ? options.homeName.trim().slice(0, 80) : "我的家",
    revision: 1,
    createdAt: timestamp,
    updatedAt: timestamp,
  };
  return {
    schemaVersion: SCHEMA_VERSION,
    storeId: randomId("store-"),
    revision: 1,
    updatedAt: timestamp,
    home,
    rooms: [],
    groups: [],
    devices: [],
    scenes: [],
    schedules: [],
    operations: [],
  };
}

export function getPlatformDataDirectory(options = {}) {
  const platform = options.platform || process.platform;
  const env = options.env || process.env;
  const homeDir = options.homeDir || os.homedir();
  if (platform === "darwin") return path.join(homeDir, "Library", "Application Support", "Yeelight", "yeelight-wifi-lan-control");
  if (platform === "win32") return path.join(env.LOCALAPPDATA || path.join(homeDir, "AppData", "Local"), "Yeelight", "yeelight-wifi-lan-control");
  return path.join(env.XDG_STATE_HOME || path.join(homeDir, ".local", "state"), "yeelight", "yeelight-wifi-lan-control");
}

export function resolveStorePaths(options = {}) {
  const supplied = options.paths || {};
  const directory = supplied.directory || options.directory || options.root || (options.storePath ? path.dirname(options.storePath) : getPlatformDataDirectory(options));
  const primary = supplied.primary || options.storePath || path.join(directory, STORE_FILE);
  const resolvedDirectory = path.resolve(directory);
  const resolvedPrimary = path.resolve(primary);
  if (!path.isAbsolute(resolvedDirectory) || !path.isAbsolute(resolvedPrimary) || resolvedPrimary !== path.join(resolvedDirectory, path.basename(resolvedPrimary))) fail("store_path_invalid", "Store paths must remain inside one absolute private directory.");
  const resolveSidecar = (candidate, fallback, label) => {
    const resolved = path.resolve(candidate || path.join(resolvedDirectory, fallback));
    const relative = path.relative(resolvedDirectory, resolved);
    if (!relative || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative) || resolved === resolvedPrimary) {
      fail("store_path_invalid", `${label} must remain inside the private store directory.`);
    }
    return resolved;
  };
  const backup = resolveSidecar(supplied.backup, BACKUP_FILE, "Backup path");
  const lock = resolveSidecar(supplied.lock, LOCK_FILE, "Lock path");
  if (backup === lock) fail("store_path_invalid", "Backup and lock paths must be different files.");
  return { directory: resolvedDirectory, primary: resolvedPrimary, backup, lock };
}

export const getStorePaths = resolveStorePaths;

async function ensurePrivateDirectory(directory) {
  if (!path.isAbsolute(directory)) fail("store_path_invalid", "Store directory must be absolute.");
  const parsed = path.parse(directory);
  let current = parsed.root;
  const segments = directory.slice(parsed.root.length).split(path.sep).filter(Boolean);
  for (const segment of segments) {
    current = path.join(current, segment);
    try {
      const stat = await fsp.lstat(current);
      if (stat.isSymbolicLink()) {
        // macOS exposes /var as a system compatibility symlink. User-controlled
        // store components, including the final directory, remain no-follow.
        if (!(process.platform === "darwin" && current === "/var")) fail("store_path_unsafe", "Store directory is not a private directory.");
      } else if (!stat.isDirectory()) fail("store_path_unsafe", "Store directory is not a private directory.");
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
      try { await fsp.mkdir(current, { mode: 0o700 }); } catch (mkdirError) {
        if (mkdirError?.code !== "EEXIST") throw mkdirError;
      }
      const stat = await fsp.lstat(current);
      if (stat.isSymbolicLink() || !stat.isDirectory()) fail("store_path_unsafe", "Store directory is not a private directory.");
    }
    await fsp.chmod(current, 0o700).catch(() => {});
  }
}

async function safeLstat(file, { allowMissing = true } = {}) {
  try {
    const stat = await fsp.lstat(file);
    if (stat.isSymbolicLink() || !stat.isFile()) fail("store_path_unsafe", "Store file is not a regular non-symlink file.", { file });
    return stat;
  } catch (error) {
    if (error?.code === "ENOENT" && allowMissing) return null;
    throw error;
  }
}

async function readTextFile(file) {
  await safeLstat(file);
  let handle;
  try {
    const flags = FS.O_RDONLY | (FS.O_NOFOLLOW || 0);
    handle = await fsp.open(file, flags);
    const stat = await handle.stat();
    if (!stat.isFile()) fail("store_path_unsafe", "Store file is not regular.", { file });
    return await handle.readFile("utf8");
  } finally {
    await handle?.close().catch(() => {});
  }
}

async function readJsonFile(file) {
  const text = await readTextFile(file);
  try { return JSON.parse(text); } catch (error) { fail("store_corrupt", "Store JSON is malformed.", { file, cause: error?.message }); }
}

async function syncDirectory(directory) {
  try {
    const handle = await fsp.open(directory, FS.O_RDONLY | (FS.O_DIRECTORY || 0));
    try { await handle.sync(); } finally { await handle.close(); }
  } catch (error) {
    if (!["EINVAL", "ENOTSUP", "EISDIR", "EPERM"].includes(error?.code)) throw error;
  }
}

async function atomicWriteFile(file, text, { mode = 0o600 } = {}) {
  const directory = path.dirname(file);
  await ensurePrivateDirectory(directory);
  await safeLstat(file);
  const temporary = path.join(directory, `.${path.basename(file)}.${process.pid}.${randomToken().slice(0, 20)}.tmp`);
  let handle;
  try {
    const flags = FS.O_WRONLY | FS.O_CREAT | FS.O_EXCL | (FS.O_NOFOLLOW || 0);
    handle = await fsp.open(temporary, flags, mode);
    await handle.writeFile(text, "utf8");
    await handle.sync();
    await handle.close();
    handle = null;
    await fsp.chmod(temporary, mode).catch(() => {});
    await safeLstat(file);
    await fsp.rename(temporary, file);
    await fsp.chmod(file, mode).catch(() => {});
    await syncDirectory(directory);
  } catch (error) {
    await handle?.close().catch(() => {});
    await fsp.unlink(temporary).catch(() => {});
    throw error;
  }
}

async function readLock(lockPath) {
  const value = await readJsonFile(lockPath);
  if (!isObject(value) || !Number.isInteger(value.pid) || value.pid <= 0 || !validId(value.ownerToken, { min: 24, max: 128 }) || !Number.isFinite(value.expiresAt)) fail("store_lock_invalid", "Store writer lock is malformed.");
  return value;
}

function processAlive(pid) {
  try { process.kill(pid, 0); return true; } catch (error) { return error?.code === "EPERM"; }
}

async function reclaimDeadLock(lockPath, lock) {
  if (!lock || processAlive(lock.pid)) return false;
  const stale = `${lockPath}.stale-${randomToken().slice(0, 16)}`;
  try {
    await fsp.rename(lockPath, stale);
    await fsp.unlink(stale).catch(() => {});
    return true;
  } catch (error) {
    if (["ENOENT", "EEXIST"].includes(error?.code)) return true;
    return false;
  }
}

export async function acquireWriterLock(options = {}) {
  const paths = resolveStorePaths(options);
  await ensurePrivateDirectory(paths.directory);
  const leaseMs = Math.max(1000, Math.min(Number(options.leaseMs) || 15_000, 10 * 60_000));
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const ownerToken = randomToken();
    const createdAt = Date.now();
    const value = { version: 1, pid: process.pid, ownerToken, createdAt, expiresAt: createdAt + leaseMs };
    let handle;
    try {
      const flags = FS.O_WRONLY | FS.O_CREAT | FS.O_EXCL | (FS.O_NOFOLLOW || 0);
      handle = await fsp.open(paths.lock, flags, 0o600);
      await handle.writeFile(JSON.stringify(value), "utf8");
      await handle.sync();
      await handle.close();
      handle = null;
      await fsp.chmod(paths.lock, 0o600).catch(() => {});
      let released = false;
      const release = async () => {
        if (released) return false;
        released = true;
        try {
          const current = await readLock(paths.lock);
          if (current.ownerToken !== ownerToken) return false;
          await fsp.unlink(paths.lock);
          await syncDirectory(paths.directory);
          return true;
        } catch (error) {
          if (error?.code === "ENOENT") return true;
          return false;
        }
      };
      const renew = async () => {
        const current = await readLock(paths.lock);
        if (current.ownerToken !== ownerToken) fail("store_lock_lost", "Store writer lock ownership changed.");
        const next = { ...current, expiresAt: Date.now() + leaseMs };
        const fd = await fsp.open(paths.lock, FS.O_RDWR | (FS.O_NOFOLLOW || 0));
        try {
          await fd.truncate(0);
          await fd.writeFile(JSON.stringify(next), "utf8");
          await fd.sync();
        } finally { await fd.close(); }
        return next.expiresAt;
      };
      return { ...value, paths, release, renew };
    } catch (error) {
      await handle?.close().catch(() => {});
      if (error?.code !== "EEXIST") throw error;
      await safeLstat(paths.lock, { allowMissing: false });
      const existing = await readLock(paths.lock);
      if (!(await reclaimDeadLock(paths.lock, existing))) fail("store_lock_busy", "Another local writer owns the store lock.", { pid: existing.pid, expiresAt: existing.expiresAt });
    }
  }
  fail("store_lock_busy", "Another local writer owns the store lock.");
}

export async function withWriterLock(options, callback) {
  const lock = await acquireWriterLock(options);
  try { return await callback(lock); } finally { await lock.release(); }
}

function attachMetadata(store, metadata) {
  for (const [key, value] of Object.entries(metadata)) Object.defineProperty(store, key, { value, enumerable: false, configurable: true });
  // Keep both ergonomic call styles working: `const store = await loadStore()`
  // and `const { store } = await loadStore()`.
  Object.defineProperty(store, "store", { value: store, enumerable: false, configurable: true });
  return store;
}

async function loadWithoutRecovery(paths, options = {}) {
  const primaryStat = await safeLstat(paths.primary);
  if (!primaryStat) return { store: null, state: "missing" };
  try {
    const parsed = await readJsonFile(paths.primary);
    validateStore(parsed, options);
    await fsp.chmod(paths.primary, 0o600).catch(() => {});
    return { store: parsed, state: "ok" };
  } catch (error) {
    if (error?.code === "store_path_unsafe") throw error;
    return { store: null, state: "invalid", error };
  }
}

export async function loadStore(options = {}) {
  const paths = resolveStorePaths(options);
  if (options.ensureDirectory !== false) await ensurePrivateDirectory(paths.directory);
  const primary = await loadWithoutRecovery(paths, options);
  if (primary.store) return attachMetadata(primary.store, { status: "ok", recoveryRequired: false, paths });
  const backupStat = await safeLstat(paths.backup);
  if (backupStat) {
    try {
      const backup = await readJsonFile(paths.backup);
      validateStore(backup, options);
      await fsp.chmod(paths.backup, 0o600).catch(() => {});
      return attachMetadata(backup, { status: "recovered", recoveryRequired: true, paths, recoverySource: "backup" });
    } catch (error) {
      if (error?.code === "store_path_unsafe") throw error;
      fail("storage_corrupt", "The primary and last-known-good store are both invalid.", { primary: primary.error?.message, backup: error?.message });
    }
  }
  if (primary.state === "invalid") fail("storage_corrupt", "The local store is corrupt and has no valid backup.", { cause: primary.error?.message });
  return attachMetadata(createEmptyStore(options), { status: "initialized", recoveryRequired: false, paths });
}

export const openStore = loadStore;
export const readStore = loadStore;
export const getStore = loadStore;

async function writeStoreLocked(paths, store, { previousText = null } = {}) {
  validateStore(store);
  const nextText = `${JSON.stringify(store, null, 2)}\n`;
  if (previousText !== null) await atomicWriteFile(paths.backup, previousText, { mode: 0o600 });
  await atomicWriteFile(paths.primary, nextText, { mode: 0o600 });
  // The first commit has no previous primary to copy. Keep the newly committed
  // value as the initial last-known-good backup so a later corruption is recoverable.
  if (previousText === null) await atomicWriteFile(paths.backup, nextText, { mode: 0o600 });
}

function bumpStore(store, now = Date.now()) {
  store.revision += 1;
  store.updatedAt = nowIso(now);
}

export async function mutateStore(options = {}, mutator = undefined) {
  if (typeof options === "function") { mutator = options; options = {}; }
  if (typeof mutator !== "function") fail("store_mutator_invalid", "A store mutation callback is required.");
  const paths = resolveStorePaths(options);
  return withWriterLock({ ...options, paths }, async () => {
    const current = await loadStore({ ...options, paths, ensureDirectory: true });
    if (current.recoveryRequired && options.repair !== true) fail("store_repair_required", "Repair the local store before writing new data.");
    if (options.expectedRevision !== undefined && options.expectedRevision !== current.revision) fail("revision_conflict", "The local store revision changed.", { expectedRevision: options.expectedRevision, actualRevision: current.revision });
    const draft = clone(current);
    const result = await mutator(draft, current);
    const candidate = result?.schemaVersion === SCHEMA_VERSION ? result : isObject(result) && isObject(result.store) ? result.store : draft;
    validateStore(candidate, options);
    const mutationResult = isObject(result) && Object.hasOwn(result, "store") ? (Object.hasOwn(result, "result") ? result.result : result) : result;
    if (sameJson(candidate, current)) return { store: attachMetadata(candidate, { status: current.status, recoveryRequired: false, paths }), result: mutationResult, changed: false, revision: current.revision };
    const previousText = current.status === "initialized" ? null : `${JSON.stringify(current, null, 2)}\n`;
    bumpStore(candidate, options.now ?? Date.now());
    await writeStoreLocked(paths, candidate, { previousText });
    return { store: attachMetadata(candidate, { status: "ok", recoveryRequired: false, paths }), result: mutationResult, changed: true, revision: candidate.revision };
  });
}

export const transaction = mutateStore;

export async function saveStore(store, options = {}) {
  validateStore(store, options);
  const expectedRevision = options.expectedRevision ?? store.revision;
  return mutateStore({ ...options, expectedRevision }, (draft) => {
    for (const key of Object.keys(draft)) delete draft[key];
    Object.assign(draft, clone(store));
  });
}

async function getValidBackup(paths, options = {}) {
  const stat = await safeLstat(paths.backup);
  if (!stat) return null;
  const backup = await readJsonFile(paths.backup);
  validateStore(backup, options);
  return backup;
}

export async function repairStore(options = {}) {
  if (!(options.confirm === true || options.confirmation === true || options.confirmation === REPAIR_CONFIRMATION)) fail("confirmation_required", "Explicit local-store repair confirmation is required.");
  const paths = resolveStorePaths(options);
  return withWriterLock({ ...options, paths }, async () => {
    const backup = await getValidBackup(paths, options);
    if (!backup) fail("storage_corrupt", "No valid last-known-good store is available for repair.");
    const primary = await loadWithoutRecovery(paths, options);
    if (primary.store && options.force !== true) return { store: attachMetadata(primary.store, { status: "ok", recoveryRequired: false, paths }), repaired: false };
    const repairedStore = clone(backup);
    const repairedAt = nowIso(options.now ?? Date.now());
    let invalidated = false;
    for (const device of repairedStore.devices) {
      if (device.rebind?.status !== "rebind_pending") continue;
      device.rebind = { status: "active", candidateEndpoint: null, challenge: null };
      device.online = false;
      device.stale = true;
      device.status = "offline";
      device.revision = Number.isInteger(device.revision) ? device.revision + 1 : 1;
      device.updatedAt = repairedAt;
      invalidated = true;
    }
    if (invalidated) {
      repairedStore.revision += 1;
      repairedStore.updatedAt = repairedAt;
    }
    validateStore(repairedStore, options);
    // Repair rewrites both generations so a subsequent primary failure cannot
    // restore a consumed rebind challenge from the old pending snapshot.
    await writeStoreLocked(paths, repairedStore, { previousText: null });
    return { store: attachMetadata(repairedStore, { status: "ok", recoveryRequired: false, paths }), repaired: true, invalidatedRebindChallenges: invalidated };
  });
}

export const repairLocalStore = repairStore;

export async function resetStore(options = {}) {
  if (!(options.confirm === true || options.confirmation === true || options.confirmation === RESET_CONFIRMATION)) fail("confirmation_required", "Explicit local-store reset confirmation is required.");
  const paths = resolveStorePaths(options);
  return withWriterLock({ ...options, paths }, async () => {
    const current = await loadStore({ ...options, paths });
    const fresh = createEmptyStore({ ...options, homeName: options.homeName || current.home?.name || "我的家" });
    await writeStoreLocked(paths, fresh, { previousText: null });
    return { store: attachMetadata(fresh, { status: "ok", recoveryRequired: false, paths }), reset: true };
  });
}

export const resetLocalStore = resetStore;

function opaqueReferences(store) {
  const maps = {};
  for (const kind of ["devices", "rooms", "groups", "scenes", "schedules", "operations"]) maps[kind] = new Map(store[kind].map((item, index) => [item.id, `${kind.slice(0, -1)}-${index + 1}`]));
  return maps;
}

function safeScalar(value) {
  return typeof value === "string" || typeof value === "number" || typeof value === "boolean" ? value : undefined;
}

function sanitizeDeviceState(value) {
  if (!isObject(value)) return {};
  return Object.fromEntries(Object.entries(value)
    .filter(([key]) => SAFE_STATE_KEYS.has(key))
    .map(([key, child]) => [key, safeScalar(child)])
    .filter(([, child]) => child !== undefined));
}

function sanitizeCapabilities(value) {
  if (!isObject(value)) return {};
  const output = {};
  for (const [key, child] of Object.entries(value)) {
    if (!SAFE_CAPABILITY_KEYS.has(key)) continue;
    if (key === "foreground" || key === "background") {
      if (!isObject(child)) continue;
      output[key] = Object.fromEntries(Object.entries(child)
        .filter(([nestedKey]) => SAFE_CAPABILITY_KEYS.has(nestedKey) && nestedKey !== "foreground" && nestedKey !== "background")
        .map(([nestedKey, nestedValue]) => [nestedKey, safeScalar(nestedValue)])
        .filter(([, nestedValue]) => nestedValue !== undefined));
      continue;
    }
    const scalar = safeScalar(child);
    if (scalar !== undefined) output[key] = scalar;
  }
  return output;
}

function sanitizeScope(scope, references) {
  if (!isObject(scope)) return null;
  const type = typeof scope.type === "string" && ["home", "room", "group", "device", "subset"].includes(scope.type)
    ? scope.type : "unknown";
  if (type === "home") return { type };
  if (type === "subset") {
    const ids = Array.isArray(scope.deviceIds) ? scope.deviceIds : [];
    const deviceRefs = ids.map((id) => references.devices.get(id) || null);
    return { type, deviceIds: deviceRefs, ...(deviceRefs.some((id) => id === null) ? { unresolved: true } : {}) };
  }
  const kind = SCOPE_REFERENCE_KINDS[type];
  const id = kind && references[kind]?.get(scope.id) || null;
  return { type, id, ...(id === null ? { unresolved: true } : {}) };
}

function sanitizeSceneActions(actions, references) {
  if (!Array.isArray(actions)) return [];
  return actions.slice(0, 64).map((action) => {
    if (!isObject(action)) return null;
    const safe = {};
    if (Object.hasOwn(action, "target")) safe.target = sanitizeScope(action.target, references);
    if (Number.isInteger(action.rank)) safe.rank = action.rank;
    if (isObject(action.set)) {
      safe.set = Object.fromEntries(Object.entries(action.set)
        .filter(([key]) => SAFE_SCENE_SET_KEYS.has(key))
        .map(([key, value]) => [key, safeScalar(value)])
        .filter(([, value]) => value !== undefined));
    } else safe.set = {};
    return safe;
  }).filter(Boolean);
}

function sanitizeCadence(cadence) {
  if (!isObject(cadence)) return null;
  if (cadence.type === "once") return { type: "once", at: typeof cadence.at === "string" ? cadence.at : null };
  if (cadence.type === "daily") return { type: "daily", time: typeof cadence.time === "string" ? cadence.time : null };
  if (cadence.type === "weekly") return {
    type: "weekly",
    days: Array.isArray(cadence.days) ? cadence.days.filter((day) => Number.isInteger(day) && day >= 1 && day <= 7) : [],
    time: typeof cadence.time === "string" ? cadence.time : null,
  };
  return { type: "unknown" };
}

export function sanitizeStoreExport(store, options = {}) {
  validateStore(store);
  if (options.includePrivate === true) return clone(store);
  const refs = opaqueReferences(store);
  const ref = (kind, id) => id && refs[kind]?.get(id) || null;
  return {
    formatVersion: 1,
    schemaVersion: SCHEMA_VERSION,
    revision: store.revision,
    updatedAt: store.updatedAt,
    home: { id: "home-1", name: store.home.name, revision: store.home.revision, updatedAt: store.home.updatedAt },
    rooms: store.rooms.map((room) => ({ id: ref("rooms", room.id), name: room.name, deviceRefs: room.deviceIds.map((id) => ref("devices", id)).filter(Boolean) })),
    devices: store.devices.map((device) => ({ id: ref("devices", device.id), alias: device.alias || device.localAlias || "", name: device.name || device.alias || "", model: device.model || "", firmware: device.firmware || device.fwVersion || "", online: device.online, stale: device.stale, roomRef: ref("rooms", device.roomId), groupRefs: device.groupIds.map((id) => ref("groups", id)).filter(Boolean), capabilities: sanitizeCapabilities(device.capabilities), state: sanitizeDeviceState(device.state) })),
    groups: store.groups.map((group) => ({ id: ref("groups", group.id), name: group.name, deviceRefs: (group.memberIds || group.deviceIds).map((id) => ref("devices", id)).filter(Boolean), status: group.status })),
    scenes: store.scenes.map((scene) => ({ id: ref("scenes", scene.id), name: scene.name, source: scene.source, revision: scene.revision, payloadHash: scene.payloadHash || null, scope: sanitizeScope(scene.scope, refs), deviceRefs: (scene.deviceIds || []).map((id) => ref("devices", id)).filter(Boolean), actions: sanitizeSceneActions(scene.actions, refs) })),
    schedules: store.schedules.map((schedule) => ({ id: ref("schedules", schedule.id), name: schedule.name, state: schedule.state, sceneRef: ref("scenes", schedule.sceneId), sceneRevision: schedule.sceneRevision || null, timezone: schedule.timezone || null, cadence: sanitizeCadence(schedule.cadence) })),
    operations: store.operations.map((operation) => ({ id: ref("operations", operation.id), status: operation.status, deviceRefs: (operation.deviceIds || []).map((id) => ref("devices", id)).filter(Boolean) })),
  };
}

export async function exportStore(options = {}) {
  const store = await loadStore(options);
  const value = sanitizeStoreExport(store, options);
  value.status = store.status;
  value.recoveryRequired = Boolean(store.recoveryRequired);
  return options.stringify === true ? `${JSON.stringify(value, null, 2)}\n` : value;
}

export async function storeStatus(options = {}) {
  const paths = resolveStorePaths(options);
  try {
    const store = await loadStore({ ...options, paths });
    return { status: store.status, recoveryRequired: Boolean(store.recoveryRequired), revision: store.revision, paths: { directory: paths.directory, primary: paths.primary, backup: paths.backup } };
  } catch (error) {
    return { status: error?.code === "storage_corrupt" ? "corrupt" : "unsafe", recoveryRequired: true, error: { code: error?.code || "store_error", message: error?.message || String(error) }, paths: { directory: paths.directory, primary: paths.primary, backup: paths.backup } };
  }
}

export const getStoreStatus = storeStatus;
export const inspectStore = storeStatus;

export const __testing = {
  validEntity,
  validId,
  sameJson,
  normalizePath: resolveStorePaths,
  ensurePrivateDirectory,
  atomicWriteFile,
  readJsonFile,
  processAlive,
  opaqueReferences,
};
