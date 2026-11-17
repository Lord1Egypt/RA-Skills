import crypto from "node:crypto";
import { discover as networkDiscover } from "./discovery.mjs";
import { YeelightTransport } from "./transport.mjs";
import {
  compileOperation,
  planTargetActions,
  OperationError,
  validateExecutionGate,
} from "./operations.mjs";
import {
  loadStore,
  mutateStore,
  exportStore,
  repairStore,
  resetStore,
  storeStatus,
} from "./store.mjs";
import {
  syncDevices,
  resolveDeviceSelector,
  setDeviceAlias,
  setDeviceAliases,
  createRoom,
  renameRoom,
  deleteRoom,
  moveDevices,
  listRooms,
  confirmRebindPersisted,
  normalizeProtocolId,
} from "./home.mjs";
import {
  createGroup,
  renameGroup,
  deleteGroup,
  addGroupMembers,
  removeGroupMembers,
  replaceGroupMembers,
  revalidateGroup,
  assessGroupWrite,
  resolveGroupSelector,
  listGroups,
} from "./groups.mjs";
import {
  RECOMMENDED_SCENES,
  recommendedSceneCatalog,
  getScene,
  listScenes,
  createSceneInCollection,
  updateSceneInCollection,
  deleteSceneInCollection,
  copyScene,
  captureSnapshotScene,
  planSceneApplication,
  compileRecommendedScene,
} from "./scenes.mjs";
import {
  createScheduleDraft,
  buildHostSchedulerRequest,
  bindSchedule,
  updateSchedule,
  markBindingPending,
  applySchedulerLifecycleReply,
  markDeletePending,
  completeScheduleDelete,
  scheduleRunnable,
  normalizeOccurrenceMetadata,
  acquireOccurrence,
  completeOccurrence,
  markOccurrenceUncertain,
} from "./schedules.mjs";
import {
  createRecoveryRecord,
  recordRecoveryOutcome,
  finalizeRecoveryRecord,
  recoverOperation,
} from "./recovery.mjs";
import { runMusicSession, stopMusicSession } from "./music.mjs";
import {
  publicDevice,
  publicRoom,
  publicGroup,
  publicScene,
  publicSchedule,
  publicHostSchedulerRequest,
  publicRecoveryRef,
  publicRebindRef,
  sanitizePublicValue,
  response,
} from "./response.mjs";

const DEFAULT_PROPERTIES = ["power", "bright", "ct", "rgb", "hue", "sat", "color_mode", "name"];
const SNAPSHOT_DYNAMIC_PROPERTIES = ["flowing", "flow_params", "bg_flowing", "bg_flow_params"];
const READABLE_STATE = new Set([
  "power", "bright", "ct", "rgb", "hue", "sat", "color_mode", "flowing", "delayoff", "flow_params", "music_on", "name",
  "bg_power", "bg_flowing", "bg_flow_params", "bg_ct", "bg_lmode", "bg_bright", "bg_rgb", "bg_hue", "bg_sat", "nl_br", "active_mode",
]);
const REACHABILITY_ERRORS = new Set([
  "connect_timeout", "connect_failed", "connect_closed", "socket_error", "connection_closed",
  "request_timeout", "write_failed",
]);
const OPERATION_ALIASES = new Map([
  ["adjust", "adjust.brightness"],
  ["brightness", "brightness.set"],
  ["color", "color.rgb"],
  ["temperature", "color.temperature"],
]);
const OCCURRENCE_FENCE_ERRORS = new Set(["occurrence_lease_expired", "occurrence_lease_conflict", "occurrence_lease_required"]);

export class RuntimeError extends Error {
  constructor(code, message = code, details = {}) {
    super(message);
    this.name = "RuntimeError";
    this.code = code;
    this.details = details;
  }
}

const clone = (value) => value === undefined ? undefined : structuredClone(value);
const randomId = (prefix) => `${prefix}${crypto.randomUUID()}`;

function nowIso(now) {
  const value = typeof now === "function" ? now() : now;
  const date = value instanceof Date ? value : new Date(value ?? Date.now());
  if (Number.isNaN(date.getTime())) throw new RuntimeError("invalid_timestamp", "时间戳无效。");
  return date.toISOString();
}

function defaultStoreOptions() {
  return process.env.YEELIGHT_WIFI_STORE_DIR ? { directory: process.env.YEELIGHT_WIFI_STORE_DIR } : {};
}

function defaultDiscover(options = {}) {
  return networkDiscover({
    deadlineMs: Number.isInteger(options.deadlineMs) ? options.deadlineMs : 1500,
    includeAdvertisements: options.includeAdvertisements === true,
    signal: options.signal,
    maxDatagrams: Number.isInteger(options.maxDatagrams) ? options.maxDatagrams : 64,
  });
}

function defaultTransportFactory(device) {
  if (!device?.endpoint) throw new RuntimeError("device_endpoint_missing", "设备尚未绑定可用的局域网端点。");
  return new YeelightTransport({ host: device.endpoint.host, port: device.endpoint.port });
}

export function createRuntime(overrides = {}) {
  return {
    storeOptions: overrides.storeOptions || defaultStoreOptions(),
    discover: overrides.discover || defaultDiscover,
    transportFactory: overrides.transportFactory || defaultTransportFactory,
    hostScheduler: overrides.hostScheduler || null,
    now: overrides.now || (() => Date.now()),
    refreshBeforeWrite: overrides.refreshBeforeWrite !== false,
    allowTestFixtures: overrides.allowTestFixtures === true,
  };
}

function assertRequest(request) {
  if (!request || typeof request !== "object" || Array.isArray(request)) throw new RuntimeError("invalid_request", "请求必须是 JSON 对象。");
  const keys = Object.keys(request);
  if (keys.length > 96) throw new RuntimeError("invalid_request", "请求字段过多。");
  return request;
}

function statusForError(error) {
  if (error?.code === "confirmation_required" || error?.code === "execution_gate_required") return "clarification_required";
  if (error?.code?.includes("not_supported") || error?.code === "method_not_supported" || error?.code === "scene_no_supported_actions") return "not_supported";
  if (["ambiguous_device_selector", "ambiguous_group_selector", "ambiguous_room_selector", "ambiguous_scene_selector", "ambiguous_schedule_selector", "device_selector_required", "group_selector_required", "offline_members_require_confirmation", "offline_target_requires_confirmation", "rebind_confirmation_required", "scene_selector_required", "scene_action_conflict", "plan_conflict", "conflicting_actions", "schedule_occurrence_running"].includes(error?.code)) return "clarification_required";
  if (["partial", "uncertain", "conflict", "schedule_occurrence_lost"].includes(error?.code)) return error.code === "schedule_occurrence_lost" ? "uncertain" : error.code;
  return "error";
}

function operationName(request) {
  const raw = String(request.operation || request.action || "").trim();
  return OPERATION_ALIASES.get(raw) || raw;
}

function mapDiscoveryResult(result) {
  const rows = Array.isArray(result) ? result : result?.devices || [];
  return rows.map((row) => ({
    protocolId: row.id ?? row.protocolId,
    endpoint: row.endpoint || row.location,
    sender: row.sender || row.senderAddress,
    model: row.model,
    firmware: row.firmware || row.fwVersion || row.fw_ver,
    name: row.name,
    support: row.support,
    capabilities: row.capabilities,
    state: row.state || row.properties,
    observedAt: row.observedAt || Date.now(),
    discoveryNonce: row.discoveryNonce,
  }));
}

async function load(rt) {
  return loadStore(rt.storeOptions);
}

async function persist(rt, mutator, options = {}) {
  return mutateStore({ ...rt.storeOptions, ...options, now: rt.now() }, async (draft, current) => {
    const outcome = await mutator(draft, current);
    if (outcome && typeof outcome === "object" && outcome.store) return { store: outcome.store, result: outcome };
    return outcome;
  });
}

function deviceRows(store) {
  return store.devices.map(publicDevice).filter(Boolean);
}

function roomBySelector(store, selector) {
  if (selector && typeof selector === "object") selector = selector.id ?? selector.ref ?? selector.name ?? selector.value;
  if (typeof selector !== "string" || !selector.trim()) return null;
  const byRef = store.rooms.find((room) => publicRoom(room)?.ref === selector);
  if (byRef) return byRef;
  const exact = store.rooms.filter((room) => room.id === selector);
  if (exact.length === 1) return exact[0];
  const key = selector.normalize("NFKC").trim().toLocaleLowerCase("en-US");
  const matches = store.rooms.filter((room) => room.name.normalize("NFKC").trim().toLocaleLowerCase("en-US") === key);
  if (matches.length > 1) throw new RuntimeError("ambiguous_room_selector", "房间名称对应多个结果，请选择一个房间。", { matches: matches.length });
  return matches[0] || null;
}

function selectorValue(selector) {
  if (selector && typeof selector === "object") return selector.ref ?? selector.id ?? selector.name ?? selector.value;
  return selector;
}

function deviceIdForSelector(store, selector) {
  const value = selectorValue(selector);
  if (typeof value !== "string" || !value.trim()) throw new RuntimeError("device_selector_required", "请选择一个设备。");
  const byRef = store.devices.find((device) => publicDevice(device)?.ref === value);
  if (byRef) return byRef.id;
  const resolved = resolveDeviceSelector(store, value);
  if (resolved.status === "ok") return resolved.device.id;
  throw new RuntimeError(resolved.code || "device_not_found", resolved.code === "ambiguous_device_selector" ? "设备名称对应多个结果，请选择一个设备。" : "没有找到已保存的设备。", { matches: resolved.matches?.length || 0 });
}

function deviceIdsForSelectors(store, selectors) {
  const values = Array.isArray(selectors) ? selectors : [selectors];
  return [...new Set(values.map((selector) => deviceIdForSelector(store, selector)))];
}

function roomIdForSelector(store, selector) {
  const room = roomBySelector(store, selectorValue(selector));
  if (room) return room.id;
  throw new RuntimeError("room_not_found", "没有找到该房间。");
}

function groupIdForSelector(store, selector) {
  const value = selectorValue(selector);
  const byRef = store.groups.find((group) => publicGroup(group)?.ref === value);
  const resolved = resolveGroupSelector(store, byRef?.id || value);
  if (resolved.status === "ok") return resolved.group.id;
  throw new RuntimeError(resolved.code || "group_not_found", resolved.code === "ambiguous_group_selector" ? "灯组名称对应多个结果，请选择一个灯组。" : "没有找到该灯组。", { matches: resolved.matches?.length || 0 });
}

function sceneForSelector(store, selector) {
  const value = selectorValue(selector);
  if (typeof value !== "string" || !value.trim()) return null;
  const byRef = store.scenes.find((scene) => publicScene(scene)?.ref === value);
  if (byRef) return byRef;
  const byId = store.scenes.find((scene) => scene.id === value);
  if (byId) return byId;
  const key = value.normalize("NFKC").trim().toLocaleLowerCase("en-US");
  const matches = store.scenes.filter((scene) => scene.name.normalize("NFKC").trim().toLocaleLowerCase("en-US") === key);
  if (matches.length > 1) throw new RuntimeError("ambiguous_scene_selector", "情景名称对应多个结果，请选择一个情景。", { matches: matches.length });
  return matches[0] || null;
}

function scheduleForSelector(store, selector) {
  const value = selectorValue(selector);
  if (typeof value !== "string" || !value.trim()) return null;
  const byRef = store.schedules.find((schedule) => publicSchedule(schedule)?.ref === value);
  if (byRef) return byRef;
  const byId = store.schedules.find((schedule) => schedule.id === value);
  if (byId) return byId;
  const key = value.normalize("NFKC").trim().toLocaleLowerCase("en-US");
  const matches = store.schedules.filter((schedule) => schedule.name.normalize("NFKC").trim().toLocaleLowerCase("en-US") === key);
  if (matches.length > 1) throw new RuntimeError("ambiguous_schedule_selector", "调度名称对应多个结果，请选择一个调度。", { matches: matches.length });
  return matches[0] || null;
}

function normalizeSchedulerReply(store, reply) {
  const normalized = clone(reply);
  if (!normalized || typeof normalized !== "object" || Array.isArray(normalized)) return normalized;
  if (typeof normalized.scheduleId === "string") {
    const selected = store.schedules.find((schedule) => publicSchedule(schedule)?.ref === normalized.scheduleId);
    if (selected) normalized.scheduleId = selected.id;
  }
  return normalized;
}

function normalizeSceneTarget(store, target) {
  if (!target || typeof target !== "object" || Array.isArray(target)) return target;
  const normalized = { ...target };
  const type = String(normalized.type || normalized.kind || "");
  if (type === "device") normalized.id = deviceIdForSelector(store, normalized);
  else if (type === "room") normalized.id = roomIdForSelector(store, normalized);
  else if (type === "group") normalized.id = groupIdForSelector(store, normalized);
  else if (type === "subset") normalized.deviceIds = deviceIdsForSelectors(store, normalized.deviceIds || normalized.devices || normalized.ids || []);
  delete normalized.ref;
  delete normalized.name;
  delete normalized.value;
  return normalized;
}

function normalizeScenePayload(store, input) {
  const payload = clone(input || {});
  if (payload.scope) payload.scope = normalizeSceneTarget(store, payload.scope);
  if (Array.isArray(payload.actions)) payload.actions = payload.actions.map((action) => ({ ...action, ...(action?.target ? { target: normalizeSceneTarget(store, action.target) } : {}) }));
  return payload;
}

function expandSelector(store, selector, options = {}) {
  if (Array.isArray(selector)) {
    const all = selector.map((item) => expandSelector(store, item, options));
    const devices = [...new Map(all.flatMap((row) => row.devices).map((device) => [device.id, device])).values()];
    return { devices, groups: all.flatMap((row) => row.groups), skippedIds: all.flatMap((row) => row.skippedIds) };
  }
  const value = selector && typeof selector === "object" ? selector : { type: "reference", value: selector };
  const type = String(value.type || value.kind || "reference");
  if (type === "home") return { devices: [...store.devices], groups: [], skippedIds: [] };
  if (type === "subset") return expandSelector(store, deviceIdsForSelectors(store, value.deviceIds || value.devices || value.ids || []), options);
  if (type === "device" || type === "reference") {
    const result = resolveDeviceSelector(store, deviceIdForSelector(store, value));
    if (result.status !== "ok") throw new RuntimeError(result.code || "device_not_found", result.code === "ambiguous_device_selector" ? "设备名称对应多个结果，请选择一个设备。" : "没有找到已保存的设备。", { matches: result.matches?.length || 0 });
    return { devices: [result.device], groups: [], skippedIds: [] };
  }
  if (type === "room") {
    const room = roomBySelector(store, selectorValue(value));
    if (!room) throw new RuntimeError("room_not_found", "没有找到该房间。");
    return { devices: room.deviceIds.map((id) => store.devices.find((device) => device.id === id)).filter(Boolean), groups: [], skippedIds: [] };
  }
  if (type === "group") {
    const result = resolveGroupSelector(store, groupIdForSelector(store, value));
    if (result.status !== "ok") throw new RuntimeError(result.code || "group_not_found", result.code === "ambiguous_group_selector" ? "灯组名称对应多个结果，请选择一个灯组。" : "没有找到该灯组。");
    const group = result.group;
    const assessment = assessGroupWrite(store, group.id, { onlineOnly: options.onlineOnly === true });
    if (options.forWrite && assessment.status === "clarification_required") throw new RuntimeError("offline_members_require_confirmation", "灯组中有离线或待重新绑定设备；请确认只控制当前在线成员。", { skippedCount: assessment.skippedIds.length });
    if (options.forWrite && assessment.status === "needs_review") throw new RuntimeError("group_needs_review", "灯组控制能力已变化，请先重新确认成员。");
    const allDevices = group.memberIds.map((id) => store.devices.find((device) => device.id === id)).filter(Boolean);
    const devices = options.forWrite && options.onlineOnly === true
      ? allDevices.filter((device) => device.online && !device.stale && device.status === "online" && device.rebind?.status !== "rebind_pending")
      : allDevices;
    return { devices, groups: [group], skippedIds: assessment.skippedIds || [] };
  }
  if (type === "scene") {
    const scene = sceneForSelector(store, value.id ?? value.ref ?? value.value ?? value.name);
    if (!scene) throw new RuntimeError("scene_not_found", "没有找到该情景。");
    return expandSelector(store, scene.scope, options);
  }
  throw new RuntimeError("selector_invalid", "目标选择器无效。");
}

function requestTarget(request) {
  return request.target ?? request.targets ?? request.selector ?? request.device ?? request.devices ?? null;
}

function assertTargets(targets) {
  if (!targets.devices.length) throw new RuntimeError("target_empty", "没有可控制的目标设备。");
  const pending = targets.devices.filter((device) => device.rebind?.status === "rebind_pending");
  if (pending.length) throw new RuntimeError("rebind_confirmation_required", "目标设备地址已变化，需要先确认一次重新绑定。", { count: pending.length });
  const offline = targets.devices.filter((device) => !device.online || device.stale || device.status === "offline");
  if (offline.length) throw new RuntimeError("offline_target_requires_confirmation", "目标中包含离线或过期设备，请先刷新设备或确认只控制在线设备。", { count: offline.length });
}

async function refreshForWrite(rt, store, targets, request) {
  if (!rt.refreshBeforeWrite || !targets.devices.some((device) => device.stale || device.status === "offline" || device.rebind?.status === "rebind_pending")) return { store, refreshed: false, result: null };
  const sync = await syncDevices({ ...rt.storeOptions, now: rt.now(), discover: async () => mapDiscoveryResult(await rt.discover({ signal: request.signal, deadlineMs: 1200 })) });
  const nextTargets = expandSelector(sync.store, requestTarget(request), { forWrite: true, onlineOnly: request.onlineOnly === true });
  return { store: sync.store, refreshed: true, result: sync.result, targets: nextTargets };
}

function propertyValue(property, value) {
  if (typeof value !== "string") return value;
  if (property === "power" || property === "bg_power" || property === "flow_params" || property === "bg_flow_params" || property === "name") return value;
  if (/^-?\d+$/u.test(value)) return Number(value);
  return value;
}

function stateFromResult(properties, result) {
  if (!Array.isArray(result)) return {};
  return Object.fromEntries(properties.map((property, index) => [property, propertyValue(property, result[index])]).filter(([, value]) => value !== undefined));
}

async function readDeviceState(rt, device, properties = DEFAULT_PROPERTIES, request = {}) {
  const props = [...new Set(properties.filter((property) => READABLE_STATE.has(property)))];
  if (!props.length) throw new RuntimeError("properties_invalid", "没有可读取的设备属性。");
  const transport = rt.transportFactory(device, { operation: "inspect" });
  try {
    const result = await transport.request("get_prop", props, { support: device.support, signal: request.signal });
    const state = stateFromResult(props, result);
    return { state, result, fresh: true, verified: true, properties: props, warnings: transport.warnings || [] };
  } finally {
    transport.close?.();
  }
}

async function persistDeviceState(rt, deviceId, state, extra = {}) {
  return persist(rt, (draft) => {
    const device = draft.devices.find((row) => row.id === deviceId);
    if (!device) return;
    device.state = { ...(device.state || {}), ...clone(state) };
    device.online = true;
    device.stale = false;
    device.status = "online";
    device.lastSeenAt = nowIso(rt.now());
    device.observedAt = device.lastSeenAt;
    if (extra.name !== undefined) device.name = extra.name;
    device.updatedAt = device.lastSeenAt;
    device.revision = Number.isInteger(device.revision) ? device.revision + 1 : 1;
  });
}

async function executeCompiled(rt, device, compiled, request) {
  const transport = rt.transportFactory(device, { operation: request.operation, method: compiled.method });
  try {
    const ack = await transport.request(compiled.method, compiled.params, { support: device.support, signal: request.signal });
    let verification = { status: "acknowledged", properties: compiled.verification || [] };
    let state = {};
    const canRead = compiled.verification?.length && (!Array.isArray(device.support) || device.support.includes("get_prop"));
    if (canRead) {
      const values = await transport.request("get_prop", compiled.verification, { support: device.support, signal: request.signal });
      state = stateFromResult(compiled.verification, values);
      verification = { status: "verified", properties: compiled.verification, state };
    }
    return { status: verification.status, ack, state, verification, warnings: transport.warnings || [] };
  } finally {
    transport.close?.();
  }
}

function semanticPropertyActions(set, background = false) {
  const actions = [];
  const add = (operation, values, isBackground = background) => actions.push({ operation: `${isBackground ? "background." : ""}${operation}`, ...values });
  for (const [key, value] of Object.entries(set || {})) {
    const isBackground = key.startsWith("bg");
    if (key === "power" || key === "bgPower") add("power.set", { power: value ? "on" : "off" }, isBackground);
    else if (key === "brightness" || key === "bgBrightness") add("brightness.set", { brightness: value }, isBackground);
    else if (key === "color" || key === "bgColor") add("color.rgb", { rgb: value }, isBackground);
    else if (key === "colorTemperature" || key === "bgColorTemperature") add("color.temperature", { temperature: value }, isBackground);
    else if (key === "hue" || key === "bgHue") add("color.hsv", { hue: value, saturation: set[key === "hue" ? "saturation" : "bgSaturation"] ?? 0, brightness: set[key === "hue" ? "brightness" : "bgBrightness"] ?? 100 }, isBackground);
    else if (key === "saturation" || key === "bgSaturation") {
      if (!Object.hasOwn(set, key === "saturation" ? "hue" : "bgHue")) continue;
    }
  }
  return actions;
}

function toCompiledActions(device, action, request) {
  const operation = OPERATION_ALIASES.get(action.operation) || action.operation;
  const compiled = compileOperation(operation, { ...request, ...action }, device);
  return [{ device, operation, compiled }];
}

function publicOperationRows(rows) {
  return rows.map((row) => ({
    device: publicDevice(row.device),
    status: row.status,
    verification: row.verification?.status || row.status,
    error: row.error ? { code: row.error.code || "device_error", message: row.error.message || "设备操作失败。" } : undefined,
    skipped: row.skipped === true,
  }));
}

async function runDeviceOperation(rt, store, request, operation, targetInfo) {
  const targets = await refreshForWrite(rt, store, targetInfo, request);
  const currentStore = targets.store || store;
  const resolved = targets.targets || targetInfo;
  if (request.preview !== true) assertTargets(resolved);
  const compiledRows = resolved.devices.map((device) => {
    const item = toCompiledActions(device, { operation, ...request }, request);
    return item[0];
  });
  const plan = planTargetActions({ actions: compiledRows.map(({ device, compiled }) => ({ target: device.id, method: compiled.method, params: compiled.params, idempotent: compiled.idempotent })) });
  if (!plan.ok) throw new OperationError(plan.conflicts[0]?.code || "plan_conflict", "目标设备收到冲突或重复的动作，未发送任何网络写入。", { conflictCount: plan.conflicts.length });
  if (request.preview === true) {
    return { store: currentStore, rows: compiledRows.map(({ device, compiled }) => ({ device, status: "preview", verification: { status: "not_applicable", properties: compiled.verification }, compiled })), refreshed: targets.refreshed };
  }
  const rows = [];
  for (const { device, compiled } of compiledRows) {
    try {
      const result = await executeCompiled(rt, device, compiled, request);
      rows.push({ device, ...result });
      if (Object.keys(result.state || {}).length) await persistDeviceState(rt, device.id, result.state);
    } catch (error) {
      rows.push({ device, status: error?.code === "request_timeout" ? "uncertain" : "failed", error, verification: { status: "failed" } });
    }
  }
  let refreshedAfterFailure = false;
  if (!targets.refreshed && rows.some((row) => REACHABILITY_ERRORS.has(row.error?.code))) {
    try {
      await syncDevices({
        ...rt.storeOptions,
        now: rt.now(),
        discover: async () => mapDiscoveryResult(await rt.discover({ signal: request.signal, deadlineMs: 1200 })),
      });
      refreshedAfterFailure = true;
    } catch {
      // Preserve the original uncertain/failed device result when discovery is unavailable.
    }
  }
  const status = rows.every((row) => ["verified", "acknowledged"].includes(row.status)) ? "ok" : rows.some((row) => ["verified", "acknowledged"].includes(row.status)) ? "partial" : rows.some((row) => row.status === "uncertain") ? "uncertain" : "error";
  const finalStore = await load(rt);
  const finalRows = rows.map((row) => ({ ...row, device: finalStore.devices.find((device) => device.id === row.device.id) || row.device }));
  return { store: finalStore, rows: finalRows, status, refreshed: targets.refreshed || refreshedAfterFailure };
}

async function routeDiscovery(rt, request, operation) {
  const discovery = await rt.discover({ signal: request.signal, deadlineMs: request.deadlineMs, includeAdvertisements: request.includeAdvertisements === true });
  const sync = await syncDevices({ ...rt.storeOptions, now: rt.now(), discover: async () => mapDiscoveryResult(discovery) });
  const result = sync.result || {};
  const challenges = (result.rebindChallenges || []).map((row) => ({
    device: publicDevice(sync.store.devices.find((device) => device.id === row.deviceId || device.id === row.id)),
    challenge: publicRebindRef(typeof row.challenge === "string" ? row.challenge : row.challenge?.token || row.token),
  }));
  return response({
    operation,
    status: result.collisions?.length ? "partial" : "ok",
    devices: deviceRows(sync.store),
    result: { added: result.added?.length || 0, updated: result.updated?.length || 0, offline: result.missing?.length || 0, collisions: result.collisions?.length || 0, rebind: challenges },
    warnings: [...(discovery.parseErrors || []), ...(result.collisions || []).map(() => "identity_collision")],
    nextActions: challenges.length ? ["确认设备重新绑定后再控制"] : [],
  });
}

async function routeHome(rt, request, operation) {
  const store = await load(rt);
  if (operation === "home.get" || operation === "device.list") return response({ operation, devices: deviceRows(store), result: { home: { name: store.home.name, revision: store.home.revision, updatedAt: store.home.updatedAt }, rooms: store.rooms.map((room) => publicRoom(room, store)), groups: store.groups.map((group) => publicGroup(group, store)), scenes: store.scenes.map(publicScene), schedules: store.schedules.map(publicSchedule) } });
  if (operation === "store.status") return response({ operation, result: await storeStatus(rt.storeOptions) });
  if (operation === "store.export") return response({ operation, result: await exportStore(rt.storeOptions) });
  if (operation === "store.repair") return response({ operation, result: await repairStore({ ...rt.storeOptions, confirm: request.confirm === true || request.confirmation }) });
  if (operation === "store.reset") return response({ operation, result: await resetStore({ ...rt.storeOptions, confirm: request.confirm === true || request.confirmation, homeName: request.name }) });
  if (operation === "home.rename") {
    if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "修改家庭名称需要明确确认。");
    const changed = await persist(rt, (draft) => { if (typeof request.name !== "string" || !request.name.trim()) throw new RuntimeError("invalid_name", "家庭名称不能为空。"); draft.home.name = request.name.trim().slice(0, 80); draft.home.revision += 1; draft.home.updatedAt = nowIso(rt.now()); });
    return response({ operation, result: { name: changed.store.home.name } });
  }
  if (operation === "device.alias.set" || operation === "device.alias.batch_set") {
    if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "保存设备名称需要明确确认。");
    const assignments = request.assignments ?? request.aliases ?? request.items;
    const changed = await persist(rt, (draft) => {
      if (operation === "device.alias.batch_set" && assignments !== undefined) {
        if (Array.isArray(assignments)) {
          const rows = assignments.map((row) => ({
            deviceId: deviceIdForSelector(draft, row?.deviceId ?? row?.device ?? row?.deviceRef ?? row?.id ?? row?.ref ?? row?.target),
            alias: row?.alias ?? row?.name ?? "",
          }));
          return setDeviceAliases(draft, rows, { now: rt.now() });
        }
        if (!assignments || typeof assignments !== "object") throw new RuntimeError("alias_batch_invalid", "批量设备名称必须是对象或数组。");
        const resolved = Object.fromEntries(Object.entries(assignments).map(([selector, alias]) => [deviceIdForSelector(draft, selector), alias]));
        return setDeviceAliases(draft, resolved, { now: rt.now() });
      }
      const ids = deviceIdsForSelectors(draft, request.deviceIds || request.devices || request.target);
      return setDeviceAlias(draft, ids, request.alias ?? request.name ?? "", { now: rt.now() });
    });
    const refs = (changed.result?.changed || []).map((id) => publicDevice(changed.store.devices.find((device) => device.id === id))?.ref).filter(Boolean);
    return response({ operation, devices: deviceRows(changed.store), result: { changed: refs, changedCount: refs.length } });
  }
  if (operation === "device.rebind.confirm") {
    if (request.confirm !== true && request.confirmation !== true && request.confirmed !== true) throw new RuntimeError("confirmation_required", "重新绑定设备端点需要明确确认。");
    const requestedDevice = request.deviceId || request.target;
    const requestedDeviceValue = requestedDevice && typeof requestedDevice === "object" ? requestedDevice.ref || requestedDevice.id || requestedDevice.value : requestedDevice;
    const selectedDevice = store.devices.find((device) => publicDevice(device)?.ref === requestedDeviceValue || device.id === requestedDeviceValue);
    const requestedChallenge = request.challenge && typeof request.challenge === "object" ? request.challenge.ref || request.challenge.value || request.challenge.token : request.challenge;
    if (typeof requestedChallenge !== "string" || !requestedChallenge.trim()) throw new RuntimeError("rebind_challenge_invalid", "重新绑定必须提供当前设备的 challenge。", { operation: "device.rebind.confirm" });
    const selectedByChallenge = store.devices.find((device) => {
      const token = device.rebind?.challenge?.token;
      return token && (requestedChallenge === token || requestedChallenge === publicRebindRef(token));
    });
    const device = selectedDevice || selectedByChallenge;
    const rawChallenge = device?.rebind?.challenge?.token;
    if (!device || typeof rawChallenge !== "string" || (requestedChallenge !== rawChallenge && requestedChallenge !== publicRebindRef(rawChallenge))) throw new RuntimeError("rebind_challenge_invalid", "重新绑定 challenge 无效、缺失或与设备不匹配。");
    const result = await confirmRebindPersisted({ ...rt.storeOptions, deviceId: device.id, challenge: rawChallenge, confirmation: true, confirm: true, now: rt.now() });
    return response({ operation, devices: deviceRows(result.store), result: { device: publicDevice(result.result?.device), consumed: true } });
  }
  return null;
}

async function routeRooms(rt, request, operation) {
  const store = await load(rt);
  if (operation === "room.list") return response({ operation, result: { rooms: listRooms(store).map((room) => publicRoom(room, store)) } });
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "修改房间组织需要明确确认。");
  const result = await persist(rt, (draft) => {
    if (operation === "room.create") return createRoom(draft, request.name, { now: rt.now() });
    const roomSelector = request.roomId || request.id || request.target;
    const roomId = roomSelector === null || roomSelector === undefined ? null : roomIdForSelector(draft, roomSelector);
    const destinationRoomId = request.destinationRoomId === undefined || request.destinationRoomId === null
      ? undefined
      : roomIdForSelector(draft, request.destinationRoomId);
    if (operation === "room.rename") return renameRoom(draft, roomId, request.name, { now: rt.now() });
    if (operation === "room.delete") return deleteRoom(draft, roomId, { now: rt.now(), unassign: request.unassign === true, destinationRoomId });
    if (operation === "room.device.move" || operation === "room.device.batch_move") return moveDevices(draft, deviceIdsForSelectors(draft, request.deviceIds || request.devices || request.target), roomId, { now: rt.now() });
    throw new RuntimeError("operation_not_supported", "房间操作不受支持。");
  });
  const changedRefs = (result.result?.changed || []).map((id) => publicDevice(result.store.devices.find((device) => device.id === id))?.ref).filter(Boolean);
  return response({ operation, result: { room: result.result?.room ? publicRoom(result.result.room, result.store) : undefined, changed: changedRefs, changedCount: changedRefs.length, deleted: Boolean(result.result?.deleted) }, devices: deviceRows(result.store) });
}

async function routeGroups(rt, request, operation) {
  const store = await load(rt);
  if (operation === "group.list") return response({ operation, result: { groups: listGroups(store).map((group) => publicGroup(group, store)) } });
  if (operation === "group.get") {
    const selected = resolveGroupSelector(store, groupIdForSelector(store, request.groupId || request.id || request.target || request.name));
    if (selected.status !== "ok") throw new RuntimeError(selected.code || "group_not_found", "没有找到该灯组。");
    return response({ operation, result: { group: publicGroup(selected.group, store) } });
  }
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "修改灯组需要明确确认。");
  const result = await persist(rt, (draft) => {
    const id = operation === "group.create" ? null : groupIdForSelector(draft, request.groupId || request.id || request.target || request.name);
    if (operation === "group.create") return createGroup(draft, request.name, deviceIdsForSelectors(draft, request.deviceIds || request.devices || request.members), { now: rt.now() });
    if (operation === "group.rename") return renameGroup(draft, id, request.name, { now: rt.now() });
    if (operation === "group.delete") return deleteGroup(draft, id, { now: rt.now() });
    if (operation === "group.revalidate") return revalidateGroup(draft, id, { now: rt.now() });
    const members = deviceIdsForSelectors(draft, request.deviceIds || request.devices || request.members);
    if (operation === "group.members.add") return addGroupMembers(draft, id, members, { now: rt.now() });
    if (operation === "group.members.remove") return removeGroupMembers(draft, id, members, { now: rt.now() });
    if (operation === "group.members.replace") return replaceGroupMembers(draft, id, members, { now: rt.now() });
    throw new RuntimeError("operation_not_supported", "灯组操作不受支持。");
  });
  return response({ operation, devices: deviceRows(result.store), result: { group: result.result?.group ? publicGroup(result.result.group, result.store) : undefined, changed: result.result?.changed, status: result.result?.status } });
}

async function routeScenes(rt, request, operation) {
  const store = await load(rt);
  if (operation === "scene.recommended.list") return response({ operation, result: { scenes: recommendedSceneCatalog().map(publicScene) } });
  if (operation === "scene.list") return response({ operation, result: { scenes: listScenes(store.scenes).map(publicScene) } });
  if (operation === "scene.get") {
    const scene = sceneForSelector(store, request.sceneId || request.id || request.target || request.name);
    if (!scene) throw new RuntimeError("scene_not_found", "没有找到该情景。");
    return response({ operation, result: { scene: publicScene(scene) } });
  }
  if (operation === "scene.apply") return routeSceneApply(rt, request, store);
  if (operation === "scene.snapshot") return routeSceneSnapshot(rt, request, store);
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "修改情景需要明确确认。");
  const result = await persist(rt, (draft) => {
    if (operation === "scene.create") {
      const created = createSceneInCollection(draft.scenes, normalizeScenePayload(draft, request.scene || request), { now: () => nowIso(rt.now()) });
      draft.scenes = created.scenes;
      return { store: draft, ...created };
    }
    if (operation === "scene.update") {
      const selected = sceneForSelector(draft, request.sceneId || request.id || request.target || request.name);
      if (!selected) throw new RuntimeError("scene_not_found", "没有找到该情景。");
      const updated = updateSceneInCollection(draft.scenes, selected.id, normalizeScenePayload(draft, request.scene || request), { now: () => nowIso(rt.now()), expectedRevision: request.expectedRevision, schedules: draft.schedules, force: request.force === true });
      draft.scenes = updated.scenes;
      return { store: draft, ...updated };
    }
    if (operation === "scene.delete") {
      const selected = sceneForSelector(draft, request.sceneId || request.id || request.target || request.name);
      if (!selected) throw new RuntimeError("scene_not_found", "没有找到该情景。");
      const deleted = deleteSceneInCollection(draft.scenes, selected.id, { schedules: draft.schedules, force: request.force === true });
      draft.scenes = deleted.scenes;
      return { store: draft, ...deleted };
    }
    if (operation === "scene.copy") {
      const selected = sceneForSelector(draft, request.sceneId || request.id || request.target || request.name);
      if (!selected) throw new RuntimeError("scene_not_found", "没有找到该情景。");
      const copied = copyScene(selected, { name: request.name, now: () => nowIso(rt.now()), schedules: draft.schedules });
      draft.scenes = [...draft.scenes, copied];
      return { store: draft, scenes: draft.scenes, scene: copied };
    }
    throw new RuntimeError("operation_not_supported", "情景操作不受支持。");
  });
  return response({ operation, result: { scene: result.result?.scene ? publicScene(result.result.scene) : undefined, deleted: result.result?.deleted }, devices: deviceRows(result.store) });
}

async function routeSceneSnapshot(rt, request, store) {
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "保存当前状态为情景需要明确确认。");
  const target = normalizeSceneTarget(store, request.scope || request.target || { type: "home" });
  const selected = expandSelector(store, target, { onlineOnly: true });
  const snapshotWarnings = [];
  const requestedProperties = Array.isArray(request.properties) ? request.properties : DEFAULT_PROPERTIES;
  const scene = await captureSnapshotScene({
    name: request.name,
    scope: target,
    targetContext: { devices: selected.devices, rooms: store.rooms, groups: store.groups },
    readState: async (device) => {
      const read = await readDeviceState(rt, device, [...new Set([...requestedProperties, ...SNAPSHOT_DYNAMIC_PROPERTIES])], request);
      await persistDeviceState(rt, device.id, read.state);
      const dynamicProperties = ["flowing", "bg_flowing"].filter((property) => {
        const value = read.state[property];
        return value !== undefined && String(value).toLocaleLowerCase() !== "off" && String(value) !== "0";
      });
      if (dynamicProperties.length) snapshotWarnings.push({
        code: "snapshot_dynamic_flow_omitted",
        deviceRef: publicDevice(device)?.ref,
        properties: dynamicProperties,
        message: "当前动态流效果不会写入快照，应用快照时不会猜测或恢复该效果。",
      });
      return { ...read.state, id: device.id, fresh: true, verified: true };
    },
    now: () => nowIso(rt.now()),
  });
  const saved = await persist(rt, (draft) => {
    if (draft.scenes.some((row) => row.name === scene.name)) throw new RuntimeError("scene_name_conflict", "同一家庭中的情景名称不能重复。");
    draft.scenes.push(scene);
    return { scene };
  });
  return response({ operation: "scene.snapshot", devices: deviceRows(saved.store), result: { scene: publicScene(saved.result.scene) }, warnings: snapshotWarnings, verification: { status: "verified" } });
}

function compileSceneActions(device, set, request, state) {
  const actions = semanticPropertyActions(set).map((action) => ({ ...action, target: device.id }));
  const simulated = { ...device, state: { ...(state || device.state || {}) } };
  const compiled = [];
  for (const action of actions) {
    const item = toCompiledActions(simulated, action, request)[0];
    compiled.push(item);
    if (action.operation === "power.set") simulated.state.power = action.power;
    if (action.operation === "background.power.set") simulated.state.bg_power = action.power;
  }
  return { actions, compiled };
}

async function routeSceneApply(rt, request, store) {
  const scene = request.recommendedId
    ? recommendedSceneCatalog().find((row) => row.recommendedId === request.recommendedId)
    : sceneForSelector(store, request.sceneId || request.id || request.target || request.name);
  if (!scene) throw new RuntimeError("scene_not_found", "没有找到该情景。");
  const effectiveScene = request.target ? { ...scene, scope: normalizeSceneTarget(store, request.target) } : scene;
  const selected = expandSelector(store, effectiveScene.scope, { forWrite: true, onlineOnly: request.onlineOnly === true });
  if (!selected.devices.length) throw new RuntimeError("target_empty", "情景没有可用的目标设备。");
  if (request.preview !== true) assertTargets(selected);
  // Resolve every room/group/device action first. This is the zero-write
  // boundary for duplicate targets and conflicting scene definitions.
  const planned = planSceneApplication(effectiveScene, {
    devices: store.devices,
    rooms: store.rooms,
    groups: store.groups,
  });
  const selectedIds = new Set(selected.devices.map((device) => device.id));
  const plannedRows = planned.actions.filter((row) => selectedIds.has(row.deviceId));
  if (!plannedRows.length) throw new RuntimeError("scene_no_supported_actions", "情景在当前目标上没有可执行的动作。");
  const preStates = new Map();
  if (request.preview !== true) {
    for (const plannedRow of plannedRows) {
      const device = store.devices.find((row) => row.id === plannedRow.deviceId);
      try {
        const read = await readDeviceState(rt, device, DEFAULT_PROPERTIES, request);
        if (read.fresh !== true || read.verified !== true) throw new RuntimeError("scene_pre_state_untrusted", "情景应用需要每个目标的新鲜已验证状态。", { deviceRef: publicDevice(device)?.ref });
        preStates.set(plannedRow.deviceId, read.state);
      } catch (error) {
        throw new RuntimeError("scene_pre_state_untrusted", "无法在任何设备写入前读取全部目标的最新状态。", { deviceRef: publicDevice(device)?.ref, cause: error?.code || "read_failed" });
      }
    }
  }
  const targetRows = plannedRows.map((plannedRow) => {
    const device = store.devices.find((row) => row.id === plannedRow.deviceId);
    const set = scene.source === "recommended"
      ? compileRecommendedScene(scene.recommendedId || scene.id, [device]).actions[0]?.set || {}
      : plannedRow.set;
    const compiledActions = compileSceneActions(device, set, request, preStates.get(device.id));
    return { device, set, actions: compiledActions.actions, compiled: compiledActions.compiled, preState: preStates.get(device.id) || device.state || {} };
  });
  const executionPlan = planTargetActions({ actions: targetRows.map((row) => ({ target: row.device.id, method: "scene.apply", params: [row.set], idempotent: true })) });
  if (!executionPlan.ok) throw new OperationError("plan_conflict", "目标设备收到冲突或重复的情景动作，未发送任何网络写入。", { conflictCount: executionPlan.conflicts.length });
  if (request.preview === true) return response({ operation: "scene.apply", devices: targetRows.map((row) => publicDevice(row.device)), result: { scene: publicScene(scene), plan: targetRows.map((row) => ({ device: publicDevice(row.device), actionCount: row.compiled.length })) } });
  const operationRef = randomId("operation-");
  const recovery = createRecoveryRecord({ idFactory: () => randomId("recovery-"), now: () => nowIso(rt.now()), sceneId: scene.id, sceneRevision: scene.revision, sceneHash: scene.payloadHash, operationRef, targets: targetRows.map((row) => ({ deviceId: row.device.id, preState: row.preState, action: row.compiled[0]?.compiled })) });
  await persist(rt, (draft) => { draft.operations.push({ ...recovery, id: operationRef, recoveryId: recovery.id, revision: 1, status: "pending" }); });
  const rows = [];
  let nextRecovery = recovery;
  for (const row of targetRows) {
    let outcome;
    try {
      for (const item of row.compiled) {
        const result = await executeCompiled(rt, row.device, item.compiled, request);
        if (Object.keys(result.state || {}).length) await persistDeviceState(rt, row.device.id, result.state);
      }
      const read = await readDeviceState(rt, row.device, DEFAULT_PROPERTIES, request);
      outcome = { deviceId: row.device.id, status: "success", state: read.state, postState: read.state, touched: true };
      rows.push({ device: row.device, status: "verified", verification: { status: "verified", state: read.state } });
    } catch (error) {
      outcome = { deviceId: row.device.id, status: error?.code === "request_timeout" ? "uncertain" : "failed", error, touched: true };
      rows.push({ device: row.device, status: outcome.status, error, verification: { status: "failed" } });
    }
    nextRecovery = recordRecoveryOutcome(nextRecovery, outcome, { now: () => nowIso(rt.now()) });
    await persist(rt, (draft) => {
      const op = draft.operations.find((item) => item.id === operationRef);
      if (op) Object.assign(op, clone(nextRecovery), { id: operationRef, recoveryId: nextRecovery.id, revision: (op.revision || 1) + 1, status: nextRecovery.status });
    });
  }
  nextRecovery = finalizeRecoveryRecord(nextRecovery, { now: () => nowIso(rt.now()) });
  const status = nextRecovery.pendingDeviceIds.length ? (rows.some((row) => row.status === "verified") ? "partial" : "uncertain") : "ok";
  return response({ operation: "scene.apply", status, devices: targetRows.map((row) => publicDevice(row.device)), result: { scene: publicScene(scene), rows: publicOperationRows(rows), recoveryRef: nextRecovery.pendingDeviceIds.length ? publicRecoveryRef(nextRecovery.id) : null } });
}

async function routeSchedules(rt, request, operation) {
  const store = await load(rt);
  if (operation === "schedule.list") return response({ operation, result: { schedules: store.schedules.map(publicSchedule) } });
  const scheduleSelector = request.scheduleId || request.id || request.target || request.name;
  const selectedSchedule = scheduleForSelector(store, scheduleSelector);
  const id = selectedSchedule?.id;
  if (operation === "schedule.get") {
    const schedule = selectedSchedule;
    if (!schedule) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
    return response({ operation, result: { schedule: publicSchedule(schedule), hostSchedulerRequest: publicHostSchedulerRequest(schedule.hostSchedulerRequest) || undefined } });
  }
  if (operation === "schedule.create_draft") {
    if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "创建调度需要明确确认。");
    const sceneSelector = request.sceneId || request.scene || request.sceneName;
    const saved = await persist(rt, (draft) => {
      const scene = sceneForSelector(draft, sceneSelector);
      if (!scene) throw new RuntimeError("scene_not_found", "调度必须引用已保存的情景。");
      const schedule = createScheduleDraft({ ...request, target: normalizeSceneTarget(draft, request.target || { type: "home" }), sceneId: scene.id, sceneRevision: scene.revision, sceneHash: scene.payloadHash }, { now: () => nowIso(rt.now()), hostSchedulerAvailable: Boolean(rt.hostScheduler) });
      draft.schedules.push(schedule);
      return { schedule };
    });
    const schedule = saved.result.schedule;
    return response({ operation, result: { schedule: publicSchedule(schedule), hostSchedulerRequest: publicHostSchedulerRequest(schedule.hostSchedulerRequest) || undefined }, status: rt.hostScheduler ? "ok" : "not_supported" });
  }
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "修改调度需要明确确认。");
  if (operation === "schedule.bind") {
    const saved = await persist(rt, (draft) => {
      const current = scheduleForSelector(draft, scheduleSelector);
      if (!current) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      const bound = bindSchedule(current, normalizeSchedulerReply(draft, request.reply || request.hostReply));
      const index = draft.schedules.findIndex((row) => row.id === current.id);
      if (index < 0) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      draft.schedules[index] = bound;
      return { schedule: bound };
    });
    return response({ operation, result: { schedule: publicSchedule(saved.result.schedule) } });
  }
  if (operation === "schedule.update") {
    const saved = await persist(rt, (draft) => {
      const current = scheduleForSelector(draft, scheduleSelector);
      if (!current) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      const reply = request.reply || request.hostReply;
      const suppliedPatch = request.patch || request.schedule;
      let next;
      if (reply && !suppliedPatch) {
        const normalizedReply = normalizeSchedulerReply(draft, reply);
        const action = current.hostSchedulerRequest?.action || (current.taskId ? "update" : "create");
        if (normalizedReply?.action !== undefined && String(normalizedReply.action) !== action) throw new RuntimeError("scheduler_reply_mismatch", "Host 回执 action 与当前待处理请求不匹配。", { expectedAction: action });
        next = action === "create"
          ? bindSchedule(current, normalizedReply, { now: () => nowIso(rt.now()) })
          : applySchedulerLifecycleReply(current, normalizedReply, { action: "update", now: () => nowIso(rt.now()) });
      } else {
        const patch = clone(suppliedPatch || request);
        if (patch.target) patch.target = normalizeSceneTarget(draft, patch.target);
        next = updateSchedule(current, patch, { expectedRevision: request.expectedRevision, now: () => nowIso(rt.now()) });
        if (reply) {
          const normalizedReply = normalizeSchedulerReply(draft, reply);
          const action = next.hostSchedulerRequest?.action || (next.taskId ? "update" : "create");
          if (normalizedReply?.action !== undefined && String(normalizedReply.action) !== action) throw new RuntimeError("scheduler_reply_mismatch", "Host 回执 action 与当前待处理请求不匹配。", { expectedAction: action });
          next = action === "create"
            ? bindSchedule(next, normalizedReply, { now: () => nowIso(rt.now()) })
            : applySchedulerLifecycleReply(next, normalizedReply, { action, now: () => nowIso(rt.now()) });
        }
      }
      const index = draft.schedules.findIndex((row) => row.id === current.id);
      if (index < 0) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      draft.schedules[index] = next;
      return { schedule: next };
    });
    return response({ operation, result: { schedule: publicSchedule(saved.result.schedule), hostSchedulerRequest: publicHostSchedulerRequest(saved.result.schedule.hostSchedulerRequest) || undefined } });
  }
  if (operation === "schedule.pause" || operation === "schedule.resume") {
    const saved = await persist(rt, (draft) => {
      const current = scheduleForSelector(draft, scheduleSelector);
      if (!current) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      const action = operation.endsWith("pause") ? "pause" : "resume";
      const reply = request.reply || request.hostReply;
      const next = reply
        ? applySchedulerLifecycleReply(current, normalizeSchedulerReply(draft, reply), { action, now: () => nowIso(rt.now()) })
        : markBindingPending(current, action, { now: () => nowIso(rt.now()) });
      const index = draft.schedules.findIndex((row) => row.id === current.id);
      if (index < 0) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      draft.schedules[index] = next;
      return { schedule: next };
    });
    return response({ operation, result: { schedule: publicSchedule(saved.result.schedule), hostSchedulerRequest: publicHostSchedulerRequest(saved.result.schedule.hostSchedulerRequest) || undefined } });
  }
  if (operation === "schedule.delete") {
    const saved = await persist(rt, (draft) => {
      const current = scheduleForSelector(draft, scheduleSelector);
      if (!current) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      if (current.taskId && !request.reply && !request.hostReply) {
        const pending = markDeletePending(current, { now: () => nowIso(rt.now()) });
        const index = draft.schedules.findIndex((row) => row.id === current.id);
        if (index < 0) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
        draft.schedules[index] = pending;
        return { pending };
      }
      if (current.taskId) {
        if (current.occurrences?.some((occurrence) => occurrence.status === "running")) throw new RuntimeError("schedule_occurrence_running", "调度仍有正在执行的 occurrence，请等待完成后再确认删除。");
        completeScheduleDelete(current, normalizeSchedulerReply(draft, request.reply || request.hostReply), { now: () => nowIso(rt.now()) });
      }
      draft.schedules = draft.schedules.filter((row) => row.id !== current.id);
      return { deleted: true };
    });
    if (saved.result?.pending) return response({ operation, status: "clarification_required", result: { schedule: publicSchedule(saved.result.pending), hostSchedulerRequest: publicHostSchedulerRequest(saved.result.pending.hostSchedulerRequest) } });
    return response({ operation, result: { deleted: true } });
  }
  if (operation === "schedule.run") {
    validateExecutionGate(request, { method: "schedule.run", confirmation: true });
    // Acquire and persist the lease before any scene/device write. A fresh
    // store read inside the transaction closes the duplicate-run race. The
    // occurrence key is derived from the private schedule ID and canonical UTC
    // instant; caller-supplied keys are never trusted or persisted.
    const leaseCommit = await persist(rt, (draft) => {
      const current = scheduleForSelector(draft, scheduleSelector);
      if (!current) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
      const runnable = scheduleRunnable(current, { scene: draft.scenes.find((scene) => scene.id === current.sceneId) });
      if (!runnable.ok) throw new RuntimeError("schedule_not_runnable", "调度当前处于关闭状态，不能执行。", { reason: runnable.reason });
      let occurrence;
      try {
        occurrence = normalizeOccurrenceMetadata(current, {
          scheduledAt: request.scheduledAt,
          localDateTime: request.localDateTime,
          fold: request.fold,
        });
      } catch (error) {
        throw new RuntimeError(error.code || "occurrence_invalid", error.message, error.details);
      }
      const acquired = acquireOccurrence(current, occurrence.key, {
        now: () => nowIso(rt.now()),
        occurrenceMetadata: occurrence,
      });
      if (acquired.acquired || acquired.status === "uncertain") {
        const index = draft.schedules.findIndex((row) => row.id === current.id);
        if (index < 0) throw new RuntimeError("schedule_not_found", "没有找到该调度。");
        draft.schedules[index] = acquired.schedule;
      }
      return { ...acquired, occurrenceKey: occurrence.key };
    });
    const acquired = leaseCommit.result;
    const occurrenceKey = acquired.occurrenceKey;
    if (acquired.status === "duplicate") return response({ operation, result: { skipped: true, reason: "duplicate_occurrence" } });
    if (acquired.status === "leased") return response({ operation, status: "uncertain", result: { skipped: true, reason: "occurrence_leased" } });
    if (acquired.status === "uncertain") return response({ operation, status: "uncertain", result: { skipped: true, reason: "occurrence_lease_expired" } });
    if (!acquired.acquired || !acquired.occurrence?.leaseId) throw new RuntimeError("occurrence_acquire_failed", "调度 occurrence 未能取得执行租约。");
    const scheduleId = acquired.schedule?.id;
    if (!scheduleId) throw new RuntimeError("occurrence_acquire_failed", "调度 occurrence 缺少有效调度引用。");
    const leasedStore = leaseCommit.store || await load(rt);
    const leasedSchedule = leasedStore.schedules.find((row) => row.id === scheduleId);
    if (!leasedSchedule) throw new RuntimeError("schedule_not_found", "没有找到取得租约后的调度。");
    const { occurrenceKey: _callerOccurrenceKey, scheduledAt: _scheduledAt, localDateTime: _localDateTime, fold: _fold, ...sceneRequestFields } = request;
    const sceneRequest = { ...sceneRequestFields, operation: "scene.apply", sceneId: leasedSchedule.sceneId, target: leasedSchedule.target, confirmation: true, executionRequested: true, preview: false };
    const persistOccurrenceCompletion = async (status, result) => persist(rt, (draft) => {
      const index = draft.schedules.findIndex((row) => row.id === scheduleId);
      if (index < 0) return { missing: true };
      const current = draft.schedules[index];
      try {
        draft.schedules[index] = completeOccurrence(current, occurrenceKey, { status, result, now: () => nowIso(rt.now()), leaseId: acquired.occurrence.leaseId });
        return { completed: true };
      } catch (error) {
        if (!OCCURRENCE_FENCE_ERRORS.has(error?.code)) throw error;
        const uncertain = markOccurrenceUncertain(current, occurrenceKey, { leaseId: acquired.occurrence.leaseId, reason: error.code, now: () => nowIso(rt.now()) });
        draft.schedules[index] = uncertain;
        return { completed: true, uncertain: true, fenceError: error.code };
      }
    });
    let applied;
    try {
      applied = await routeSceneApply(rt, sceneRequest, leasedStore);
    } catch (error) {
      const completion = await persistOccurrenceCompletion("uncertain", { code: "scene_apply_failed" });
      if (completion.result?.missing) throw new RuntimeError("schedule_occurrence_lost", "设备写入后调度记录已被删除，执行结果无法完整记账。", { cause: error?.code || "scene_apply_failed" });
      if (completion.result?.uncertain) return response({ operation, status: "uncertain", result: { reason: "occurrence_completion_fenced", completionError: completion.result.fenceError, appliedStatus: "uncertain" } });
      throw error;
    }
    const occurrenceStatus = applied.status === "ok" ? "success" : applied.status === "partial" ? "partial" : applied.status === "uncertain" ? "uncertain" : "failed";
    const completion = await persistOccurrenceCompletion(occurrenceStatus, { status: applied.status });
    if (completion.result?.missing) {
      return response({ operation, status: "uncertain", result: { reason: "schedule_deleted_after_write", appliedStatus: applied.status } });
    }
    if (completion.result?.uncertain) return response({ operation, status: "uncertain", result: { reason: "occurrence_completion_fenced", completionError: completion.result.fenceError, appliedStatus: applied.status } });
    return applied;
  }
  throw new RuntimeError("operation_not_supported", "调度操作不受支持。");
}

async function routeRecovery(rt, request) {
  const store = await load(rt);
  const requestedRecoveryRef = request.recoveryRef;
  const operation = store.operations.find((row) => row.id === request.operationRef
    || row.recoveryId === request.recoveryId
    || row.id === request.id
    || (requestedRecoveryRef && publicRecoveryRef(row.recoveryId || row.id) === requestedRecoveryRef));
  const record = operation?.targets ? operation : null;
  if (!record) throw new RuntimeError("recovery_not_found", "没有找到可恢复的未完成操作。");
  const current = store.devices;
  const result = await recoverOperation(record, {
    confirmation: request.confirmation || request.confirm,
    readState: async (deviceId) => {
      const device = current.find((row) => row.id === deviceId);
      if (!device) return { state: null, fresh: false, verified: false };
      return readDeviceState(rt, device, DEFAULT_PROPERTIES, request);
    },
    restoreState: async (deviceId, state) => {
      const device = current.find((row) => row.id === deviceId);
      if (!device) return { status: "failed", error: { code: "device_not_found" } };
      const actions = semanticPropertyActions({ power: state.power === "on", brightness: state.bright, color: state.rgb, colorTemperature: state.ct });
      for (const action of actions) {
        const compiled = toCompiledActions(device, action, { executionRequested: true, preview: false, confirmation: true })[0].compiled;
        await executeCompiled(rt, device, compiled, { executionRequested: true, preview: false, confirmation: true });
      }
      return { status: "verified", state };
    },
    persist: async (next) => {
      await persist(rt, (draft) => { const row = draft.operations.find((item) => item.id === operation.id); if (row) Object.assign(row, clone(next), { id: operation.id, recoveryId: next.id, revision: (row.revision || 1) + 1, status: next.status }); });
    },
    now: () => nowIso(rt.now()),
  });
  return response({
    operation: "operation.recover",
    status: result.status === "complete" ? "ok" : result.status,
    result: {
      recovery: result.rows.map((row) => {
        const { deviceId, ...safeRow } = row;
        const device = current.find((candidate) => candidate.id === deviceId);
        return { ...safeRow, deviceRef: publicDevice(device)?.ref || null };
      }),
      complete: result.complete,
      recoveryRef: result.recoveryId ? publicRecoveryRef(result.recoveryId) : null,
    },
  });
}

async function routeMusic(rt, request, operation) {
  const store = await load(rt);
  const targetInfo = expandSelector(store, requestTarget(request), { forWrite: true, onlineOnly: request.onlineOnly === true });
  if (targetInfo.devices.length !== 1) throw new RuntimeError("music_single_device_required", "音乐模式一次只能选择一台设备。");
  assertTargets(targetInfo);
  if (request.confirm !== true && request.confirmation !== true) throw new RuntimeError("confirmation_required", "音乐模式会打开短期局域网反向连接，需要明确确认。");
  validateExecutionGate(request, { method: "set_music", confirmation: true });
  const device = targetInfo.devices[0];
  const transport = rt.transportFactory(device, { operation });
  try {
    if (operation === "music.stop") { await stopMusicSession({ transport, device }); return response({ operation, devices: [publicDevice(device)], result: { status: "acknowledged" }, verification: { status: "acknowledged" } }); }
    const result = await runMusicSession({ device, transport, requestedHost: request.localHost, sequence: request.sequence, durationMs: request.durationMs, now: rt.now });
    return response({ operation, devices: [publicDevice(device)], result, verification: { status: result.status } });
  } finally { transport.close?.(); }
}

async function routeBasic(rt, request, operation) {
  const store = await load(rt);
  const target = requestTarget(request);
  if (!target) throw new RuntimeError("target_required", "请指定设备、房间、灯组或家庭目标。");
  const targetInfo = expandSelector(store, target, { forWrite: operation !== "inspect" && operation !== "device.inspect" && operation !== "watch", onlineOnly: request.onlineOnly === true });
  if (operation === "inspect" || operation === "device.inspect") {
    const rows = [];
    for (const device of targetInfo.devices) {
      try { const read = await readDeviceState(rt, device, request.properties || DEFAULT_PROPERTIES, request); await persistDeviceState(rt, device.id, read.state); rows.push({ device, status: "verified", state: read.state, verification: { status: "verified" } }); } catch (error) { rows.push({ device, status: "failed", error, verification: { status: "failed" } }); }
    }
    return response({ operation, status: rows.every((row) => row.status === "verified") ? "ok" : "partial", devices: rows.map((row) => publicDevice(row.device)), result: { rows: publicOperationRows(rows) }, verification: { status: "verified" } });
  }
  if (operation === "watch") {
    const rows = [];
    for (const device of targetInfo.devices) {
      const transport = rt.transportFactory(device, { operation });
      try { const notifications = await transport.collectNotifications({ durationMs: request.durationMs || 1000, maxNotifications: Math.min(32, request.maxNotifications || 32), signal: request.signal }); rows.push({ device: publicDevice(device), notifications: sanitizePublicValue(notifications) }); } finally { transport.close?.(); }
    }
    return response({ operation, devices: targetInfo.devices.map(publicDevice), result: { rows } });
  }
  const result = await runDeviceOperation(rt, store, request, operation, targetInfo);
  return response({ operation, status: result.status, devices: result.rows.map((row) => publicDevice(row.device)), result: { rows: publicOperationRows(result.rows), refreshed: result.refreshed }, verification: { status: result.rows.every((row) => row.verification?.status === "verified") ? "verified" : "acknowledged" } });
}

export async function handleRequest(rawRequest, overrides = {}) {
  const request = assertRequest(rawRequest);
  const rt = createRuntime(overrides);
  const operation = operationName(request);
  try {
    if (["discover", "devices.sync", "devices.refresh"].includes(operation)) return await routeDiscovery(rt, request, operation);
    const home = await routeHome(rt, request, operation);
    if (home) return home;
    if (operation.startsWith("room.")) return await routeRooms(rt, request, operation);
    if (operation.startsWith("group.")) return await routeGroups(rt, request, operation);
    if (operation.startsWith("scene.")) return await routeScenes(rt, request, operation);
    if (operation.startsWith("schedule.")) return await routeSchedules(rt, request, operation);
    if (operation === "operation.recover") return await routeRecovery(rt, request);
    if (operation === "music.play" || operation === "music.stop") return await routeMusic(rt, request, operation);
    return await routeBasic(rt, request, operation);
  } catch (error) {
    return response({ operation, status: statusForError(error), error });
  }
}
