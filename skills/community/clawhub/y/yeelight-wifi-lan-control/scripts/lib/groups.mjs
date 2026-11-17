import crypto from "node:crypto";
import { validateStore } from "./store.mjs";
import { nameKey, normalizeName, normalizeProtocolId } from "./home.mjs";

export class GroupError extends Error {
  constructor(code, message = code, details = undefined) {
    super(message);
    this.name = "GroupError";
    this.code = code;
    if (details !== undefined) this.details = details;
  }
}

function fail(code, message = code, details) {
  throw new GroupError(code, message, details);
}

const METHOD_FAMILIES = Object.freeze({
  foreground: {
    power: new Set(["set_power", "toggle", "dev_toggle"]),
    brightness: new Set(["set_bright", "adjust_bright"]),
    colorTemperature: new Set(["set_ct_abx", "adjust_ct"]),
    color: new Set(["set_rgb", "set_hsv", "adjust_color"]),
    flow: new Set(["start_cf", "stop_cf"]),
    adjustment: new Set(["set_adjust", "adjust_bright", "adjust_ct", "adjust_color"]),
  },
  background: {
    power: new Set(["bg_set_power", "bg_toggle", "dev_toggle"]),
    brightness: new Set(["bg_set_bright", "bg_adjust_bright"]),
    colorTemperature: new Set(["bg_set_ct_abx", "bg_adjust_ct"]),
    color: new Set(["bg_set_rgb", "bg_set_hsv", "bg_adjust_color"]),
    flow: new Set(["bg_start_cf", "bg_stop_cf"]),
    adjustment: new Set(["bg_set_adjust", "bg_adjust_bright", "bg_adjust_ct", "bg_adjust_color"]),
  },
});

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function nowIso(value = Date.now()) {
  if (typeof value === "function") value = value();
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) fail("invalid_timestamp", "Invalid group timestamp.");
  return date.toISOString();
}

function randomId(prefix = "") {
  return `${prefix}${crypto.randomUUID()}`;
}

function touch(entity, now) {
  entity.revision = Number.isInteger(entity.revision) ? entity.revision + 1 : 1;
  entity.updatedAt = nowIso(now);
}

function expectedRevision(store, options = {}) {
  if (options.expectedRevision !== undefined && options.expectedRevision !== store.revision) fail("revision_conflict", "The local home changed before this group operation.", { expectedRevision: options.expectedRevision, actualRevision: store.revision });
}

function methodSet(device) {
  const support = Array.isArray(device?.support) ? device.support : [];
  return new Set(support.map((method) => String(method).trim().toLowerCase()).filter(Boolean));
}

function booleanCapability(device, key) {
  const capabilities = device?.capabilities;
  if (!capabilities || typeof capabilities !== "object") return null;
  const aliases = {
    power: ["power", "switch"],
    brightness: ["brightness", "bright"],
    colorTemperature: ["colorTemperature", "temperature", "ct"],
    color: ["color", "rgb", "hsv"],
    flow: ["flow", "effect"],
    adjustment: ["adjustment", "adjust", "relative"],
  };
  const keys = aliases[key] || [key];
  for (const alias of keys) if (typeof capabilities[alias] === "boolean") return capabilities[alias];
  return null;
}

function methodHasFamily(methods, family, device, key) {
  if (methods.size > 0) return [...METHOD_FAMILIES[family][key]].some((method) => methods.has(method));
  const explicit = booleanCapability(device, key);
  if (explicit !== null) return explicit;
  return [...METHOD_FAMILIES[family][key]].some((method) => methods.has(method));
}

export function normalizeCapabilityFingerprint(device) {
  if (!device || typeof device !== "object") fail("device_not_found", "A device record is required.");
  const methods = methodSet(device);
  const observed = methods.size > 0 || Object.keys(device.capabilities || {}).length > 0;
  if (!observed) fail("capability_observation_required", "A fresh advertised capability set is required before grouping.");
  const normalized = { foreground: {}, background: {} };
  for (const family of ["foreground", "background"]) {
    for (const key of ["power", "brightness", "colorTemperature", "color", "flow", "adjustment"]) normalized[family][key] = methodHasFamily(methods, family, device, key);
  }
  return normalized;
}

export function controlCapabilityFingerprint(device) {
  return JSON.stringify(normalizeCapabilityFingerprint(device));
}

export const getControlCapabilityFingerprint = controlCapabilityFingerprint;
export const capabilityFingerprint = controlCapabilityFingerprint;
export const computeCapabilityFingerprint = controlCapabilityFingerprint;
export const normalizedCapabilityFingerprint = normalizeCapabilityFingerprint;

function capabilitySummary(device) {
  const normalized = normalizeCapabilityFingerprint(device);
  return { normalized, fingerprint: JSON.stringify(normalized) };
}

function memberIds(group) {
  return [...(group?.memberIds || group?.deviceIds || [])].map(normalizeProtocolId);
}

function deviceIds(value) {
  const list = Array.isArray(value) ? value : [value];
  return [...new Set(list.map((item) => normalizeProtocolId(typeof item === "object" ? item.id ?? item.protocolId : item)))].sort();
}

function findDevices(store, ids) {
  const byId = new Map(store.devices.map((device) => [device.id, device]));
  const missing = ids.filter((id) => !byId.has(id));
  if (missing.length) fail("device_not_found", "One or more group members are not saved locally.", { missingCount: missing.length });
  return ids.map((id) => byId.get(id));
}

function assertCompatible(devices) {
  if (devices.length < 2) fail("group_member_count", "A compatible control group needs at least two devices.");
  const fingerprints = devices.map((device) => capabilitySummary(device));
  const unique = [...new Set(fingerprints.map((entry) => entry.fingerprint))];
  if (unique.length !== 1) fail("group_capability_mismatch", "Every group member must advertise the same control capability fingerprint.", { memberCount: devices.length, fingerprintCount: unique.length });
  return fingerprints[0].fingerprint;
}

function ensureNameAvailable(store, name, exceptId = null) {
  const key = nameKey(name);
  if (store.groups.some((group) => group.id !== exceptId && nameKey(group.name) === key)) fail("group_name_conflict", "A group with this name already exists.");
}

function syncDeviceGroupMembership(store, groupId, oldIds, newIds, now) {
  const oldSet = new Set(oldIds);
  const newSet = new Set(newIds);
  for (const device of store.devices) {
    const isMember = newSet.has(device.id);
    const wasMember = oldSet.has(device.id);
    if (isMember && !wasMember) { device.groupIds = [...new Set([...(device.groupIds || []), groupId])].sort(); touch(device, now); }
    if (!isMember && wasMember) { device.groupIds = (device.groupIds || []).filter((id) => id !== groupId); touch(device, now); }
  }
}

function ensureGroupAliases(group) {
  group.memberIds = [...memberIds(group)].sort();
  group.deviceIds = [...group.memberIds];
  group.capabilityFingerprint = group.fingerprint;
  group.needsReview = group.status === "needs_review";
  return group;
}

export function createGroup(inputStore, name, members, options = {}) {
  validateStore(inputStore);
  if (name && typeof name === "object" && !Array.isArray(name)) { options = name; name = options.name; members = options.memberIds ?? options.deviceIds ?? options.members; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const normalizedName = normalizeName(name);
  ensureNameAvailable(store, normalizedName);
  const ids = deviceIds(members);
  const devices = findDevices(store, ids);
  const fingerprint = assertCompatible(devices);
  const timestamp = nowIso(options.now ?? Date.now());
  const group = ensureGroupAliases({ id: options.id || randomId("group-"), name: normalizedName, memberIds: ids, deviceIds: ids, fingerprint, capabilityFingerprint: fingerprint, status: "active", needsReview: false, revision: 1, createdAt: timestamp, updatedAt: timestamp });
  store.groups.push(group);
  syncDeviceGroupMembership(store, group.id, [], ids, options.now ?? Date.now());
  validateStore(store);
  return { store, group };
}

export function renameGroup(inputStore, groupId, name, options = {}) {
  validateStore(inputStore);
  if (groupId && typeof groupId === "object" && !Array.isArray(groupId)) { options = groupId; groupId = options.groupId ?? options.id; name = options.name; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const group = store.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  const normalizedName = normalizeName(name);
  ensureNameAvailable(store, normalizedName, group.id);
  if (group.name !== normalizedName) { group.name = normalizedName; touch(group, options.now ?? Date.now()); }
  validateStore(store);
  return { store, group };
}

export function deleteGroup(inputStore, groupId, options = {}) {
  validateStore(inputStore);
  if (groupId && typeof groupId === "object" && !Array.isArray(groupId)) { options = groupId; groupId = options.groupId ?? options.id; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const index = store.groups.findIndex((group) => group.id === groupId);
  if (index < 0) fail("group_not_found", "The group is not saved locally.");
  const ids = memberIds(store.groups[index]);
  store.groups.splice(index, 1);
  syncDeviceGroupMembership(store, groupId, ids, [], options.now ?? Date.now());
  validateStore(store);
  return { store, deleted: groupId };
}

function replaceMembers(inputStore, groupId, members, options = {}) {
  validateStore(inputStore);
  const store = clone(inputStore);
  expectedRevision(store, options);
  const group = store.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  const ids = deviceIds(members);
  const devices = findDevices(store, ids);
  const fingerprint = assertCompatible(devices);
  const oldIds = memberIds(group);
  const sameMembers = JSON.stringify([...oldIds].sort()) === JSON.stringify([...ids].sort());
  const wasActive = group.status === "active" && group.needsReview !== true && group.fingerprint === fingerprint;
  if (sameMembers && wasActive) {
    validateStore(store);
    return { store, group, changed: false };
  }
  ensureGroupAliases(Object.assign(group, { memberIds: ids, deviceIds: ids, fingerprint, capabilityFingerprint: fingerprint, status: "active", needsReview: false }));
  touch(group, options.now ?? Date.now());
  syncDeviceGroupMembership(store, group.id, oldIds, ids, options.now ?? Date.now());
  validateStore(store);
  return { store, group, changed: !sameMembers || !wasActive };
}

export const replaceGroupMembers = replaceMembers;
export const createControlGroup = createGroup;
export const renameControlGroup = renameGroup;
export const deleteControlGroup = deleteGroup;

export function addGroupMembers(inputStore, groupId, members, options = {}) {
  validateStore(inputStore);
  const group = inputStore.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  return replaceMembers(inputStore, groupId, [...memberIds(group), ...(Array.isArray(members) ? members : [members])], options);
}

export function removeGroupMembers(inputStore, groupId, members, options = {}) {
  validateStore(inputStore);
  const group = inputStore.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  const remove = new Set(deviceIds(members));
  return replaceMembers(inputStore, groupId, memberIds(group).filter((id) => !remove.has(id)), options);
}

export function revalidateGroup(inputStore, groupId, options = {}) {
  validateStore(inputStore);
  if (groupId && typeof groupId === "object" && !Array.isArray(groupId)) { options = groupId; groupId = options.groupId ?? options.id; }
  const store = clone(inputStore);
  expectedRevision(store, options);
  const group = store.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  const ids = memberIds(group);
  let status = "active";
  let fingerprint = group.fingerprint || group.capabilityFingerprint || "";
  try {
    const devices = findDevices(store, ids);
    fingerprint = assertCompatible(devices);
    if (group.fingerprint && group.fingerprint !== fingerprint) status = "needs_review";
  } catch (error) {
    if (error.code === "group_capability_mismatch" || error.code === "capability_observation_required" || error.code === "device_not_found") status = "needs_review";
    else throw error;
  }
  const changed = group.status !== status || group.fingerprint !== fingerprint;
  if (changed) { group.status = status; group.fingerprint = fingerprint; ensureGroupAliases(group); touch(group, options.now ?? Date.now()); }
  validateStore(store);
  return { store, group, changed, status };
}

export const groupRevalidate = revalidateGroup;
export const revalidateControlGroup = revalidateGroup;

export function assessGroupWrite(store, groupId, options = {}) {
  validateStore(store);
  const group = typeof groupId === "object" ? groupId : store.groups.find((candidate) => candidate.id === groupId);
  if (!group) return { status: "error", code: "group_not_found", writable: false, onlineIds: [], skippedIds: [] };
  const members = memberIds(group);
  const devices = store.devices.filter((device) => members.includes(device.id));
  const online = devices.filter((device) => device.online && !device.stale && device.status === "online" && device.rebind?.status !== "rebind_pending").map((device) => device.id);
  const skipped = members.filter((id) => !online.includes(id));
  if (group.status === "needs_review" || group.needsReview) return { status: "needs_review", writable: false, onlineIds: online, skippedIds: skipped, members };
  if (skipped.length === 0) return { status: "ready", writable: true, onlineIds: online, skippedIds: [], members };
  if (options.onlineOnly === true) return { status: "partial", writable: true, onlineIds: online, skippedIds: skipped, members, warning: "offline_members_skipped" };
  return { status: "clarification_required", writable: false, onlineIds: online, skippedIds: skipped, members, warning: "offline_members_require_confirmation" };
}

export function resolveGroupSelector(store, selector) {
  validateStore(store);
  if (selector && typeof selector === "object" && selector.id) selector = selector.id;
  if (typeof selector !== "string" || !selector.trim()) return { status: "clarification_required", code: "group_selector_required", matches: [] };
  const exact = store.groups.filter((group) => group.id === selector);
  if (exact.length === 1) return { status: "ok", group: exact[0] };
  const key = nameKey(selector);
  const matches = store.groups.filter((group) => nameKey(group.name) === key);
  if (matches.length === 1) return { status: "ok", group: matches[0] };
  return { status: "clarification_required", code: matches.length ? "ambiguous_group_selector" : "group_not_found", matches };
}

export function listGroups(store) {
  validateStore(store);
  return store.groups.map((group) => ({ ...clone(group), members: memberIds(group).map((id) => store.devices.find((device) => device.id === id)).filter(Boolean).map((device) => ({ id: device.id, alias: device.alias || device.name, online: device.online, stale: device.stale })) }));
}

export const groupMembers = (store, groupId) => {
  validateStore(store);
  const group = store.groups.find((candidate) => candidate.id === groupId);
  if (!group) fail("group_not_found", "The group is not saved locally.");
  return memberIds(group);
};

export const __testing = { METHOD_FAMILIES, methodSet, memberIds, deviceIds, assertCompatible, syncDeviceGroupMembership, ensureGroupAliases };
