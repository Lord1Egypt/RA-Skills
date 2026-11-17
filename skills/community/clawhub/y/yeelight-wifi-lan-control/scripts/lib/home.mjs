import crypto from "node:crypto";
import { mutateStore, validateStore } from "./store.mjs";

export const MAX_DISCOVERY_DEVICES = 512;
export const REBIND_TTL_MS = 5 * 60 * 1000;

export class HomeError extends Error {
  constructor(code, message = code, details = undefined) {
    super(message);
    this.name = "HomeError";
    this.code = code;
    if (details !== undefined) this.details = details;
  }
}

function fail(code, message = code, details) {
  throw new HomeError(code, message, details);
}

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function nowIso(value = Date.now()) {
  if (typeof value === "function") value = value();
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) fail("invalid_timestamp", "Invalid observation timestamp.");
  return date.toISOString();
}

function nowMs(value) {
  if (typeof value === "function") value = value();
  if (value instanceof Date) return value.getTime();
  if (typeof value === "number") return Number.isFinite(value) ? value : Date.now();
  if (typeof value === "string" && value.trim()) {
    const parsed = Date.parse(value);
    if (!Number.isNaN(parsed)) return parsed;
  }
  return Date.now();
}

function randomId(prefix = "") {
  return `${prefix}${crypto.randomUUID()}`;
}

function randomToken() {
  return crypto.randomBytes(32).toString("base64url");
}

export function normalizeName(value) {
  if (typeof value !== "string") fail("invalid_name", "A local name must be text.");
  const normalized = value.normalize("NFKC").trim();
  if (!normalized || normalized.length > 80 || /[\u0000-\u001f\u007f\r\n]/u.test(normalized)) fail("invalid_name", "A local name is empty or contains unsupported characters.");
  return normalized;
}

export function nameKey(value) {
  return normalizeName(value).toLocaleLowerCase("en-US");
}

export function normalizeProtocolId(value) {
  if (typeof value !== "string") fail("invalid_protocol_id", "A protocol device id is required.");
  const id = value.trim();
  if (!id || id.length > 160 || /[\u0000-\u001f\u007f\r\n\\/]/u.test(id)) fail("invalid_protocol_id", "The protocol device id is malformed.");
  if (/^0x[0-9a-f]+$/iu.test(id) || /^[0-9a-f]{16,}$/iu.test(id)) return id.toLowerCase();
  if (!/^[A-Za-z0-9._:-]+$/u.test(id)) fail("invalid_protocol_id", "The protocol device id is malformed.");
  return id;
}

function parseHost(host) {
  if (typeof host !== "string" || !host || host.length > 64 || /[\u0000-\u001f\u007f\s\\/]/u.test(host)) fail("invalid_endpoint", "The Yeelight endpoint host is malformed.");
  const octets = host.split(".");
  if (octets.length !== 4 || octets.some((part) => !/^\d{1,3}$/u.test(part) || Number(part) > 255)) fail("invalid_endpoint", "Only canonical IPv4 Yeelight endpoints are supported.");
  return octets.map((part) => String(Number(part))).join(".");
}

export function normalizeEndpoint(value) {
  if (typeof value === "string") {
    const match = /^yeelight:\/\/([^:]+):(\d{1,5})$/iu.exec(value.trim());
    if (!match) fail("invalid_endpoint", "The endpoint must be yeelight://IPv4:port.");
    return { scheme: "yeelight", host: parseHost(match[1]), port: Number(match[2]) };
  }
  if (!value || typeof value !== "object") fail("invalid_endpoint", "A Yeelight endpoint is required.");
  const port = Number(value.port);
  if (!Number.isInteger(port) || port < 1 || port > 65535) fail("invalid_endpoint", "The endpoint port is invalid.");
  return { scheme: "yeelight", host: parseHost(value.host), port };
}

export function endpointKey(value) {
  if (!value) return "";
  const endpoint = normalizeEndpoint(value);
  return `${endpoint.host}:${endpoint.port}`;
}

export function endpointDigest(value) {
  return crypto.createHash("sha256").update(endpointKey(value)).digest("hex");
}

function normalizeSupport(value) {
  const values = Array.isArray(value) ? value : typeof value === "string" ? value.split(/[\s,]+/u) : [];
  return [...new Set(values.map((item) => String(item).trim()).filter((item) => item && item.length <= 64 && !/[\u0000-\u001f\u007f]/u.test(item)))].sort();
}

function normalizeSender(value, endpoint) {
  if (!value) return endpoint ? { ...endpoint } : null;
  if (typeof value === "string") {
    const match = /^(?:yeelight:\/\/)?([^:]+):(\d{1,5})$/iu.exec(value.trim());
    if (!match) fail("invalid_sender", "Discovery sender is malformed.");
    return normalizeEndpoint({ host: match[1], port: Number(match[2]) });
  }
  return normalizeEndpoint(value);
}

function safeState(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  const allowed = new Set(["power", "bright", "brightness", "ct", "rgb", "hue", "sat", "color_mode", "flowing", "delayoff", "music_on", "bg_power", "bg_bright", "bg_ct", "bg_rgb", "bg_hue", "bg_sat"]);
  return Object.fromEntries(Object.entries(value).filter(([key, child]) => allowed.has(key) && (typeof child === "string" || typeof child === "number" || typeof child === "boolean")));
}

export function normalizeObservation(value, options = {}) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail("invalid_discovery", "A discovery observation must be an object.");
  const protocolId = normalizeProtocolId(value.protocolId ?? value.id ?? value.deviceId);
  const rawEndpoint = value.endpoint ?? value.location;
  const endpoint = rawEndpoint ? normalizeEndpoint(rawEndpoint) : null;
  const sender = normalizeSender(value.sender ?? value.senderAddress ?? value.source, endpoint);
  if (!endpoint) fail("invalid_discovery", "A discovery observation must include a Yeelight endpoint.");
  if (sender && endpointKey(sender) !== endpointKey({ ...endpoint, host: sender.host })) {
    // Discovery parsers may expose the sender port as ephemeral. Host binding is the trust boundary.
    if (sender.host !== endpoint.host) fail("identity_endpoint_mismatch", "The advertised endpoint host differs from the discovery sender.");
  }
  const observedAt = value.observedAt ?? value.lastSeenAt ?? value.timestamp ?? Date.now();
  const observedAtMs = nowMs(observedAt);
  return {
    protocolId,
    endpoint,
    sender,
    model: typeof value.model === "string" ? value.model.slice(0, 128) : "",
    firmware: String(value.firmware ?? value.fwVersion ?? value.fw_ver ?? "").slice(0, 64),
    name: typeof value.name === "string" ? value.name.slice(0, 128) : "",
    support: normalizeSupport(value.support),
    capabilities: value.capabilities && typeof value.capabilities === "object" && !Array.isArray(value.capabilities) ? clone(value.capabilities) : {},
    capabilityFingerprint: typeof value.capabilityFingerprint === "string" ? value.capabilityFingerprint.slice(0, 2048) : "",
    state: safeState(value.state ?? value.properties ?? value),
    observedAt: nowIso(observedAtMs),
    observedAtMs,
    discoveryNonce: typeof value.discoveryNonce === "string" ? value.discoveryNonce.slice(0, 128) : (options.discoveryNonce || randomToken().slice(0, 24)),
  };
}

function touch(entity, now, { increment = true } = {}) {
  const timestamp = nowIso(now);
  if (increment) entity.revision = Number.isInteger(entity.revision) ? entity.revision + 1 : 1;
  entity.updatedAt = timestamp;
  return entity;
}

function emptyRebind() {
  return { status: "active", candidateEndpoint: null, challenge: null };
}

function createDevice(observation, now) {
  const timestamp = nowIso(now);
  return {
    id: observation.protocolId,
    protocolId: observation.protocolId,
    alias: "",
    localAlias: "",
    name: observation.name,
    roomId: null,
    groupIds: [],
    endpoint: clone(observation.endpoint),
    sender: clone(observation.sender),
    model: observation.model,
    firmware: observation.firmware,
    fwVersion: observation.firmware,
    support: observation.support,
    capabilities: clone(observation.capabilities),
    capabilityFingerprint: observation.capabilityFingerprint,
    online: true,
    stale: false,
    status: "online",
    observedAt: observation.observedAt,
    lastSeenAt: observation.observedAt,
    lastObservationAtMs: observation.observedAtMs,
    state: clone(observation.state),
    rebind: emptyRebind(),
    revision: 1,
    createdAt: timestamp,
    updatedAt: timestamp,
  };
}

function metadataEqual(device, observation) {
  return endpointKey(device.endpoint) === endpointKey(observation.endpoint)
    && (device.sender?.host || "") === (observation.sender?.host || "")
    && device.model === observation.model
    && (device.firmware || device.fwVersion || "") === observation.firmware
    && device.name === observation.name
    && JSON.stringify(device.support || []) === JSON.stringify(observation.support)
    && JSON.stringify(device.capabilities || {}) === JSON.stringify(observation.capabilities || {})
    && device.capabilityFingerprint === observation.capabilityFingerprint
    && JSON.stringify(device.state || {}) === JSON.stringify(observation.state || {});
}

function candidateFor(device, observation, now) {
  const token = randomToken();
  const challenge = {
    token,
    tokenDigest: crypto.createHash("sha256").update(token).digest("hex"),
    issuedAt: nowIso(now),
    expiresAt: nowMs(now) + REBIND_TTL_MS,
    localDeviceRef: device.id,
    oldEndpointDigest: endpointDigest(device.endpoint),
    candidateEndpointDigest: endpointDigest(observation.endpoint),
    capabilityFingerprint: observation.capabilityFingerprint || "",
    discoveryNonce: observation.discoveryNonce,
    storeRevision: null,
  };
  return { status: "rebind_pending", candidateEndpoint: clone(observation.endpoint), candidateObservation: clone(observation), challenge };
}

function observationGroups(observations, options = {}) {
  if (!Array.isArray(observations) || observations.length > MAX_DISCOVERY_DEVICES) fail("discovery_limit", "The discovery result set exceeds the local bound.");
  const groups = new Map();
  for (const item of observations) {
    const observation = normalizeObservation(item, options);
    const rows = groups.get(observation.protocolId) || [];
    rows.push(observation);
    groups.set(observation.protocolId, rows);
  }
  return groups;
}

export function upsertDevices(inputStore, observations, options = {}) {
  validateStore(inputStore);
  const store = clone(inputStore);
  const now = options.now ?? Date.now();
  const groups = observationGroups(observations, options);
  const existingById = new Map(store.devices.map((device) => [device.id, device]));
  const collisions = [];
  const added = [];
  const updated = [];
  const rebindPending = [];
  const rebindChallenges = [];
  const seen = new Set();
  for (const [protocolId, rows] of groups) {
    // UDP source ports can differ between valid replies; the identity window is
    // bound to endpoint and sender host, not the ephemeral discovery port.
    const endpointKeys = new Set(rows.map((row) => `${endpointKey(row.endpoint)}|${row.sender?.host || ""}`));
    if (endpointKeys.size > 1) {
      collisions.push({ protocolId, endpoints: [...endpointKeys] });
      continue;
    }
    const observation = rows.slice().sort((left, right) => left.observedAtMs - right.observedAtMs).at(-1);
    seen.add(protocolId);
    const existing = existingById.get(protocolId);
    if (!existing) {
      const device = createDevice(observation, now);
      store.devices.push(device);
      added.push(device.id);
      continue;
    }
    if (observation.observedAtMs < Number(existing.lastObservationAtMs || 0)) continue;
    if (existing.endpoint && endpointKey(existing.endpoint) !== endpointKey(observation.endpoint)) {
      const pendingSameCandidate = existing.rebind?.status === "rebind_pending" && endpointKey(existing.rebind.candidateEndpoint) === endpointKey(observation.endpoint);
      if (!pendingSameCandidate) {
        existing.rebind = candidateFor(existing, observation, now);
        existing.rebind.challenge.storeRevision = store.revision;
        rebindChallenges.push({ deviceId: existing.id, challenge: existing.rebind.challenge.token, expiresAt: existing.rebind.challenge.expiresAt, candidateEndpointDigest: existing.rebind.challenge.candidateEndpointDigest });
      }
      else existing.rebind.candidateObservation = clone(observation);
      existing.lastObservationAtMs = observation.observedAtMs;
      existing.observedAt = observation.observedAt;
      existing.lastSeenAt = observation.observedAt;
      existing.online = false;
      existing.stale = true;
      existing.status = "rebind_pending";
      touch(existing, now);
      rebindPending.push(existing.id);
      updated.push(existing.id);
      continue;
    }
    if (metadataEqual(existing, observation) && existing.online && !existing.stale && existing.status === "online") continue;
    const preserved = { alias: existing.alias || existing.localAlias || "", localAlias: existing.localAlias || existing.alias || "", roomId: existing.roomId ?? null, groupIds: [...(existing.groupIds || [])] };
    Object.assign(existing, {
      ...preserved,
      endpoint: clone(observation.endpoint),
      sender: clone(observation.sender),
      model: observation.model,
      firmware: observation.firmware,
      fwVersion: observation.firmware,
      name: observation.name,
      support: observation.support,
      capabilities: clone(observation.capabilities),
      capabilityFingerprint: observation.capabilityFingerprint,
      state: clone(observation.state),
      online: true,
      stale: false,
      status: "online",
      observedAt: observation.observedAt,
      lastSeenAt: observation.observedAt,
      lastObservationAtMs: observation.observedAtMs,
      rebind: emptyRebind(),
    });
    touch(existing, now);
    updated.push(existing.id);
  }
  const missing = [];
  for (const device of store.devices) {
    if (seen.has(device.id) || collisions.some((item) => item.protocolId === device.id)) continue;
    if (device.online || !device.stale || device.status !== "offline") {
      device.online = false;
      device.stale = true;
      device.status = "offline";
      touch(device, now);
    }
    missing.push(device.id);
  }
  validateStore(store);
  return { store, added, updated: [...new Set(updated)], missing, collisions, rebindPending, rebindChallenges, changed: added.length > 0 || updated.length > 0 || missing.length > 0 };
}

export async function syncDevices(options = {}) {
  const discover = options.discover || options.discovery;
  if (typeof discover !== "function") fail("discovery_unavailable", "A bounded discovery function is required.");
  const observations = await discover({ signal: options.signal, timeoutMs: options.timeoutMs });
  if (!Array.isArray(observations)) fail("invalid_discovery", "The discovery function must return an array.");
  return mutateStore(options, (draft) => {
    const result = upsertDevices(draft, observations, options);
    // Discovery challenges must bind to the revision that the enclosing
    // transaction will commit, not the pre-mutation revision.
    if (result.changed && result.rebindChallenges.length) {
      const committedRevision = draft.revision + 1;
      for (const row of result.rebindChallenges) {
        const device = result.store.devices.find((candidate) => candidate.id === row.deviceId);
        if (device?.rebind?.challenge) device.rebind.challenge.storeRevision = committedRevision;
      }
    }
    return { store: result.store, result };
  });
}

export const refreshDevices = syncDevices;
export const upsertDevicesByProtocolId = upsertDevices;
export const syncHomeDevices = syncDevices;
export const refreshHomeDevices = syncDevices;

function expectedRevision(store, options = {}) {
  if (options.expectedRevision !== undefined && options.expectedRevision !== store.revision) fail("revision_conflict", "The local home changed before this operation.", { expectedRevision: options.expectedRevision, actualRevision: store.revision });
}

function deviceIdsFrom(value) {
  const values = Array.isArray(value) ? value : [value];
  return [...new Set(values.map((item) => normalizeProtocolId(typeof item === "object" ? item.id ?? item.protocolId : item)))];
}

function roomsSync(store) {
  const byRoom = new Map(store.rooms.map((room) => [room.id, []]));
  for (const device of store.devices) if (device.roomId && byRoom.has(device.roomId)) byRoom.get(device.roomId).push(device.id);
  for (const room of store.rooms) room.deviceIds = byRoom.get(room.id).sort();
}

export function setDeviceAlias(inputStore, deviceIds, alias, options = {}) {
  validateStore(inputStore);
  const store = clone(inputStore);
  expectedRevision(store, options);
  const ids = deviceIdsFrom(deviceIds);
  const normalized = alias === "" ? "" : normalizeName(alias);
  const found = new Set(store.devices.map((device) => device.id));
  if (ids.some((id) => !found.has(id))) fail("device_not_found", "One or more devices are not saved locally.");
  const changed = [];
  for (const device of store.devices.filter((candidate) => ids.includes(candidate.id))) {
    if (device.alias === normalized && device.localAlias === normalized) continue;
    device.alias = normalized;
    device.localAlias = normalized;
    touch(device, options.now ?? Date.now());
    changed.push(device.id);
  }
  validateStore(store);
  return { store, changed, changedAny: changed.length > 0 };
}

export function setDeviceAliases(inputStore, assignments, options = {}) {
  if (Array.isArray(assignments)) {
    const rows = assignments.map((row) => ({ id: row?.deviceId ?? row?.id ?? row?.protocolId, alias: row?.alias ?? row?.name ?? "" }));
    let current = inputStore;
    const changed = [];
    for (const row of rows) {
      const result = setDeviceAlias(current, row.id, row.alias, options);
      current = result.store;
      changed.push(...result.changed);
    }
    return { store: current, changed: [...new Set(changed)] };
  }
  if (!assignments || typeof assignments !== "object") fail("alias_batch_invalid", "Alias batch must be an object or rows.");
  let current = inputStore;
  const changed = [];
  for (const [id, alias] of Object.entries(assignments)) {
    const result = setDeviceAlias(current, id, alias, options);
    current = result.store;
    changed.push(...result.changed);
  }
  return { store: current, changed: [...new Set(changed)] };
}

export const aliasDevices = setDeviceAliases;

export function createRoom(inputStore, name, options = {}) {
  validateStore(inputStore);
  if (isOptionsObject(name)) { options = name; name = options.name; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const normalized = normalizeName(name);
  if (store.rooms.some((room) => nameKey(room.name) === nameKey(normalized))) fail("room_name_conflict", "A room with this name already exists.");
  const timestamp = nowIso(options.now ?? Date.now());
  const room = { id: options.id || randomId("room-"), name: normalized, deviceIds: [], revision: 1, createdAt: timestamp, updatedAt: timestamp };
  store.rooms.push(room);
  validateStore(store);
  return { store, room };
}

export function renameRoom(inputStore, roomId, name, options = {}) {
  validateStore(inputStore);
  if (isOptionsObject(roomId)) { options = roomId; roomId = options.roomId ?? options.id; name = options.name; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const room = store.rooms.find((candidate) => candidate.id === roomId);
  if (!room) fail("room_not_found", "The room is not saved locally.");
  const normalized = normalizeName(name);
  if (store.rooms.some((candidate) => candidate.id !== room.id && nameKey(candidate.name) === nameKey(normalized))) fail("room_name_conflict", "A room with this name already exists.");
  if (room.name !== normalized) { room.name = normalized; touch(room, options.now ?? Date.now()); }
  validateStore(store);
  return { store, room };
}

export function deleteRoom(inputStore, roomId, options = {}) {
  validateStore(inputStore);
  if (isOptionsObject(roomId)) { options = roomId; roomId = options.roomId ?? options.id; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const index = store.rooms.findIndex((candidate) => candidate.id === roomId);
  if (index < 0) fail("room_not_found", "The room is not saved locally.");
  const members = store.devices.filter((device) => device.roomId === roomId);
  if (members.length && options.unassign !== true && !options.destinationRoomId) fail("room_not_empty", "Move or explicitly unassign the room's devices first.");
  if (options.destinationRoomId && !store.rooms.some((room) => room.id === options.destinationRoomId && room.id !== roomId)) fail("room_not_found", "The destination room is not saved locally.");
  for (const device of members) device.roomId = options.destinationRoomId || null;
  store.rooms.splice(index, 1);
  roomsSync(store);
  for (const device of members) touch(device, options.now ?? Date.now());
  validateStore(store);
  return { store, deleted: roomId, moved: members.map((device) => device.id) };
}

export function moveDevices(inputStore, deviceIds, roomId = null, options = {}) {
  validateStore(inputStore);
  if (isOptionsObject(deviceIds)) { options = deviceIds; roomId = options.roomId ?? null; deviceIds = options.deviceIds ?? options.ids; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  if (roomId !== null && !store.rooms.some((room) => room.id === roomId)) fail("room_not_found", "The destination room is not saved locally.");
  const ids = deviceIdsFrom(deviceIds);
  const byId = new Map(store.devices.map((device) => [device.id, device]));
  if (ids.some((id) => !byId.has(id))) fail("device_not_found", "One or more devices are not saved locally.");
  const changed = [];
  for (const id of ids) {
    const device = byId.get(id);
    if (device.roomId === roomId) continue;
    device.roomId = roomId;
    touch(device, options.now ?? Date.now());
    changed.push(id);
  }
  roomsSync(store);
  validateStore(store);
  return { store, changed };
}

export const moveDevice = moveDevices;
export const batchMoveDevices = moveDevices;
export const moveRoomDevices = moveDevices;
export const createHomeRoom = createRoom;
export const renameHomeRoom = renameRoom;
export const deleteHomeRoom = deleteRoom;

export function listRooms(store) {
  validateStore(store);
  return store.rooms.map((room) => ({ ...clone(room), devices: room.deviceIds.map((id) => store.devices.find((device) => device.id === id)).filter(Boolean).map((device) => ({ id: device.id, alias: device.alias || device.name, name: device.name })) }));
}

export function resolveDeviceSelector(store, selector) {
  validateStore(store);
  if (selector && typeof selector === "object" && selector.id) selector = selector.id;
  if (typeof selector !== "string" || !selector.trim()) return { status: "clarification_required", code: "device_selector_required", matches: [] };
  const text = selector.trim();
  const exactId = store.devices.filter((device) => device.id === text || device.protocolId === text);
  if (exactId.length === 1) return { status: "ok", device: exactId[0] };
  const key = nameKey(text);
  const matches = store.devices.filter((device) => [device.alias, device.localAlias, device.name].filter(Boolean).some((name) => nameKey(name) === key));
  if (matches.length === 1) return { status: "ok", device: matches[0] };
  return { status: "clarification_required", code: matches.length ? "ambiguous_device_selector" : "device_not_found", matches };
}

export function confirmRebind(inputStore, deviceId, challenge, options = {}) {
  validateStore(inputStore);
  if (isOptionsObject(deviceId)) {
    const request = deviceId;
    options = { ...options, ...request };
    deviceId = request.deviceId ?? request.id;
    challenge = request.challenge ?? request.token;
  }
  if (options.confirm !== true && options.confirmation !== true && options.confirmed !== true) fail("confirmation_required", "重新绑定设备端点需要明确确认。", { operation: "device.rebind.confirm" });
  const store = clone(inputStore);
  expectedRevision(store, options);
  const id = normalizeProtocolId(deviceId);
  const device = store.devices.find((candidate) => candidate.id === id);
  if (!device) fail("device_not_found", "The device is not saved locally.");
  const pending = device.rebind;
  if (challenge && typeof challenge === "object") challenge = challenge.token ?? challenge.value ?? null;
  if (!pending || pending.status !== "rebind_pending" || !pending.challenge || typeof challenge !== "string") fail("rebind_challenge_invalid", "The rebind challenge is no longer valid.");
  const currentTime = nowMs(options.now ?? Date.now());
  if (currentTime > Number(pending.challenge.expiresAt) || challenge !== pending.challenge.token) fail("rebind_challenge_invalid", "The rebind challenge is expired, replayed, or mismatched.");
  if (Number(pending.challenge.storeRevision) !== store.revision) fail("rebind_challenge_invalid", "The local store changed after this challenge was issued.");
  if (options.candidateEndpointDigest && options.candidateEndpointDigest !== pending.challenge.candidateEndpointDigest) fail("rebind_challenge_invalid", "The candidate endpoint changed.");
  const candidate = pending.candidateObservation;
  if (!candidate || endpointDigest(candidate.endpoint) !== pending.challenge.candidateEndpointDigest) fail("rebind_challenge_invalid", "The candidate observation changed.");
  Object.assign(device, {
    endpoint: clone(candidate.endpoint),
    sender: clone(candidate.sender),
    model: candidate.model,
    firmware: candidate.firmware,
    fwVersion: candidate.firmware,
    name: candidate.name,
    support: candidate.support,
    capabilities: clone(candidate.capabilities),
    capabilityFingerprint: candidate.capabilityFingerprint,
    state: clone(candidate.state),
    online: true,
    stale: false,
    status: "online",
    observedAt: candidate.observedAt,
    lastSeenAt: candidate.observedAt,
    lastObservationAtMs: candidate.observedAtMs,
    rebind: emptyRebind(),
  });
  touch(device, options.now ?? Date.now());
  validateStore(store);
  return { store, device, consumed: true };
}

export async function confirmRebindPersisted(options = {}) {
  return mutateStore(options, (draft) => {
    const result = confirmRebind(draft, options);
    return { store: result.store, result };
  });
}

export const deviceRebindConfirm = confirmRebind;
export const confirmDeviceRebind = confirmRebind;

function isOptionsObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export const __testing = {
  clone,
  metadataEqual,
  observationGroups,
  createDevice,
  roomsSync,
  candidateFor,
  safeState,
};
