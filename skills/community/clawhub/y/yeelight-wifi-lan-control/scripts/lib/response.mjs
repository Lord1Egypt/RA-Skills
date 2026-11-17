import crypto from "node:crypto";

export const CONTRACT_VERSION = "1.0";

const SECRET_KEY = /(?:token|secret|password|credential|authorization|transcript|raw|packet|header|endpoint|sender|protocolid|protocol_id|host|port|socket|address|path|storepath|store_path)/iu;
const SAFE_PUBLIC_KEYS = new Set(["hostSchedulerRequest"]);

function clone(value) {
  return value === undefined ? undefined : JSON.parse(JSON.stringify(value));
}

function opaqueRef(kind, id) {
  if (id === undefined || id === null) return null;
  return `${kind}-${crypto.createHash("sha256").update(String(id), "utf8").digest("hex").slice(0, 12)}`;
}

export function publicRecoveryRef(id) {
  return opaqueRef("recovery", id);
}

export function publicRebindRef(id) {
  return opaqueRef("rebind", id);
}

function publicCapabilityHighlights(device) {
  const support = new Set(Array.isArray(device?.support) ? device.support : []);
  const capabilities = [];
  if (support.has("set_power") || support.has("toggle")) capabilities.push("power");
  if (support.has("set_bright") || support.has("adjust_bright")) capabilities.push("brightness");
  if (support.has("set_ct_abx") || support.has("adjust_ct")) capabilities.push("temperature");
  if (support.has("set_rgb") || support.has("set_hsv") || support.has("adjust_color")) capabilities.push("color");
  if (support.has("start_cf") || support.has("stop_cf")) capabilities.push("flow");
  if (support.has("bg_set_power") || support.has("bg_set_bright")) capabilities.push("background");
  return capabilities;
}

export function publicDevice(device) {
  if (!device || typeof device !== "object") return null;
  return {
    ref: opaqueRef("device", device.id ?? device.protocolId),
    alias: device.alias || device.localAlias || device.name || "未命名设备",
    model: device.model || "未知型号",
    firmware: device.firmware || device.fwVersion || undefined,
    online: device.online === true,
    stale: device.stale === true,
    status: device.status || (device.online ? "online" : "offline"),
    capabilities: publicCapabilityHighlights(device),
    power: device.state?.power,
    brightness: device.state?.bright,
    colorMode: device.state?.color_mode,
    roomRef: opaqueRef("room", device.roomId),
    groupRefs: Array.isArray(device.groupIds) ? device.groupIds.map((id) => opaqueRef("group", id)).filter(Boolean) : [],
    rebindPending: device.rebind?.status === "rebind_pending",
  };
}

export function publicRoom(room, store = null) {
  if (!room || typeof room !== "object") return null;
  const deviceIds = Array.isArray(room.deviceIds) ? room.deviceIds : [];
  return {
    ref: opaqueRef("room", room.id),
    name: room.name,
    devices: store ? deviceIds.map((id) => publicDevice(store.devices.find((device) => device.id === id))).filter(Boolean) : deviceIds.map((id) => opaqueRef("device", id)),
  };
}

export function publicGroup(group, store = null) {
  if (!group || typeof group !== "object") return null;
  const ids = group.memberIds || group.deviceIds || [];
  return {
    ref: opaqueRef("group", group.id),
    name: group.name,
    status: group.status,
    needsReview: group.status === "needs_review" || group.needsReview === true,
    members: store ? ids.map((id) => publicDevice(store.devices.find((device) => device.id === id))).filter(Boolean) : ids.map((id) => opaqueRef("device", id)),
  };
}

export function publicScene(scene) {
  if (!scene || typeof scene !== "object") return null;
  const scope = scene.scope ? { type: scene.scope.type } : undefined;
  if (scope && scene.scope.type === "subset") scope.deviceRefs = (scene.scope.deviceIds || []).map((id) => opaqueRef("device", id));
  else if (scope && scene.scope.id) scope.ref = opaqueRef(scene.scope.type, scene.scope.id);
  return {
    ref: opaqueRef("scene", scene.id),
    name: scene.name,
    source: scene.source,
    readonly: scene.readonly === true,
    revision: scene.revision,
    payloadHash: scene.payloadHash,
    scope,
    description: scene.description,
  };
}

export function publicSchedule(schedule) {
  if (!schedule || typeof schedule !== "object") return null;
  return {
    ref: opaqueRef("schedule", schedule.id),
    name: schedule.name,
    status: schedule.status || schedule.state || schedule.lifecycle,
    enabled: schedule.enabled === true,
    timezone: schedule.timezone,
    cadence: publicCadence(schedule.cadence),
    sceneRevision: schedule.sceneRevision,
    bindingState: schedule.bindingState,
  };
}

function publicSchedulerTarget(target) {
  if (!target || typeof target !== "object" || Array.isArray(target)) return null;
  const type = String(target.type || "");
  if (type === "home") return { type };
  if (type === "subset") return {
    type,
    deviceIds: Array.isArray(target.deviceIds) ? target.deviceIds.map((id) => opaqueRef("device", id)).filter(Boolean) : [],
  };
  if (["device", "room", "group"].includes(type)) return { type, id: opaqueRef(type, target.id ?? target.deviceId ?? target.ref) };
  return { type: "unknown" };
}

export function publicHostSchedulerRequest(request) {
  if (!request || typeof request !== "object" || Array.isArray(request)) return null;
  const scenePin = request.scenePin && typeof request.scenePin === "object" ? {
    sceneId: opaqueRef("scene", request.scenePin.sceneId),
    sceneRevision: request.scenePin.sceneRevision,
    ...(request.scenePin.sceneHash ? { sceneHash: request.scenePin.sceneHash } : {}),
  } : undefined;
  return {
    contractVersion: request.contractVersion,
    kind: request.kind,
    scheduleId: opaqueRef("schedule", request.scheduleId),
    idempotencyKey: request.idempotencyKey,
    createdBy: request.createdBy,
    action: request.action,
    ...(request.taskId ? { taskId: request.taskId } : {}),
    ...(request.taskRevision !== undefined && request.taskRevision !== null ? { taskRevision: request.taskRevision } : {}),
    timezone: request.timezone,
    cadence: publicCadence(request.cadence),
    ...(scenePin ? { scenePin } : {}),
    target: publicSchedulerTarget(request.target),
  };
}

function publicCadence(cadence) {
  if (!cadence || typeof cadence !== "object" || Array.isArray(cadence)) return null;
  if (cadence.type === "once") return { type: "once", at: typeof cadence.at === "string" ? cadence.at : null };
  if (cadence.type === "daily") return { type: "daily", time: typeof cadence.time === "string" ? cadence.time : null };
  if (cadence.type === "weekly") return {
    type: "weekly",
    days: Array.isArray(cadence.days) ? cadence.days.filter((day) => Number.isInteger(day) && day >= 1 && day <= 7) : [],
    time: typeof cadence.time === "string" ? cadence.time : null,
  };
  return { type: "unknown" };
}

function sanitize(value, key = "") {
  if (value === undefined) return undefined;
  if (value === null || typeof value === "boolean" || typeof value === "number") return value;
  if (typeof value === "string") return value.replace(/[\u0000-\u001f\u007f]/gu, "?").slice(0, 500);
  if (Array.isArray(value)) return value.slice(0, 256).map((child) => sanitize(child, key)).filter((child) => child !== undefined);
  if (typeof value !== "object") return undefined;
  const output = {};
  for (const [childKey, child] of Object.entries(value).slice(0, 256)) {
    if (SECRET_KEY.test(childKey) && !SAFE_PUBLIC_KEYS.has(childKey)) continue;
    const next = sanitize(child, childKey);
    if (next !== undefined) output[childKey] = next;
  }
  return output;
}

export function sanitizePublicValue(value) {
  return sanitize(value);
}

export function publicError(error) {
  if (!error) return null;
  const code = typeof error.code === "string" ? error.code.slice(0, 96) : "runtime_error";
  return {
    code,
    message: typeof error.message === "string" ? error.message.replace(/[\u0000-\u001f\u007f]/gu, "?").slice(0, 300) : "操作失败。",
    details: sanitize(error.details || {}),
  };
}

export function response({
  status = "ok",
  operation = "",
  devices = [],
  result = {},
  verification = { status: "not_applicable" },
  warnings = [],
  nextActions = [],
  error = null,
} = {}) {
  return sanitizePublicValue({
    contractVersion: CONTRACT_VERSION,
    status,
    operation,
    devices,
    result,
    verification,
    warnings,
    nextActions,
    ...(error ? { error: publicError(error) } : {}),
  });
}

export const createResponse = response;
