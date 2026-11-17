import { catalogMethod, validateMethodParams, getVerificationProperties, methodRequiresConfirmation, isIdempotentMethod, CatalogError, normalizeFlowExpression } from "./catalog.mjs";
import { isCanonicalIPv4, isPrivateIPv4 } from "./network-policy.mjs";

const READ_METHODS = new Set(["get_prop", "cron_get"]);
const OPERATION_METHODS = new Map([
  ["power.set", "set_power"], ["power.toggle", "toggle"],
  ["brightness.set", "set_bright"], ["color.rgb", "set_rgb"], ["color.hsv", "set_hsv"], ["color.temperature", "set_ct_abx"],
  ["adjust", "set_adjust"], ["adjust.brightness", "adjust_bright"], ["adjust.temperature", "adjust_ct"], ["adjust.color", "adjust_color"],
  ["flow.start", "start_cf"], ["flow.stop", "stop_cf"], ["scene.apply", "set_scene"],
  ["timer.set", "cron_add"], ["timer.get", "cron_get"], ["timer.cancel", "cron_del"],
  ["default.save", "set_default"], ["name.set", "set_name"], ["device.toggle_both", "dev_toggle"],
  ["music.play", "set_music"], ["music.stop", "set_music"],
  ["background.power.set", "bg_set_power"], ["background.power.toggle", "bg_toggle"],
  ["background.brightness.set", "bg_set_bright"], ["background.color.rgb", "bg_set_rgb"], ["background.color.hsv", "bg_set_hsv"], ["background.color.temperature", "bg_set_ct_abx"],
  ["background.adjust.brightness", "bg_adjust_bright"], ["background.adjust.temperature", "bg_adjust_ct"], ["background.adjust.color", "bg_adjust_color"],
  ["background.adjust", "bg_set_adjust"],
  ["background.flow.start", "bg_start_cf"], ["background.flow.stop", "bg_stop_cf"], ["background.scene.apply", "bg_set_scene"], ["background.default.save", "bg_set_default"],
]);

export class OperationError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "OperationError";
    this.code = code;
    this.details = sanitize(details);
  }
}

export function isPhysicalWriteMethod(method) {
  return Boolean(catalogMethod(method)) && !READ_METHODS.has(method);
}

export function validateExecutionGate(input = {}, { method = null, confirmation = false, confirmationField = "confirm" } = {}) {
  const executionRequested = input?.executionRequested === true;
  const preview = input?.preview;
  if (!executionRequested || preview !== false) throw new OperationError("execution_gate_required", "Physical device writes require executionRequested=true and preview=false.", { method });
  if (confirmation && input?.[confirmationField] !== true && input?.confirmation !== true && input?.confirmed !== true) throw new OperationError("confirmation_required", "This operation requires explicit confirmation.", { method });
  return Object.freeze({ executionRequested, preview, confirmed: confirmation ? true : undefined });
}

export const assertExecutionGate = validateExecutionGate;

export function compileProtocolMethod({ method, params = [], device = null, support, request = {}, allowPreview = false } = {}) {
  if (!catalogMethod(method)) throw new OperationError("method_not_supported", "The requested protocol method is not cataloged.", { method });
  const physicalWrite = isPhysicalWriteMethod(method);
  if (physicalWrite && !(allowPreview && request.preview === true)) validateExecutionGate(request, { method, confirmation: methodRequiresConfirmation(method) });
  if (physicalWrite && allowPreview && request.preview === true && request.executionRequested !== true) return { method, params: validateParams(method, params, support), preview: true, requiresExecution: true, verification: getVerificationProperties(method) };
  const normalized = validateParams(method, params, support);
  assertPrecondition(method, device);
  return Object.freeze({
    method,
    params: normalized,
    requiresExecution: physicalWrite,
    verification: getVerificationProperties(method),
    idempotent: isIdempotentMethod(method),
    specialConfirmation: methodRequiresConfirmation(method),
  });
}

export const compileMethod = compileProtocolMethod;

export function compileOperation(operation, input = {}, device = null) {
  const name = typeof operation === "string" ? operation : operation?.name || operation?.operation;
  const request = typeof operation === "object" ? { ...operation, ...input } : input;
  const allowPreview = request.preview === true && request.executionRequested !== true;
  if (name === "inspect" || name === "device.inspect") return compileProtocolMethod({ method: "get_prop", params: request.properties || request.props || ["power", "bright", "ct", "rgb", "hue", "sat", "color_mode", "name"], device, support: device?.support, request, allowPreview });
  if (name === "watch") return compileProtocolMethod({ method: "get_prop", params: request.properties || ["power", "bright"], device, support: device?.support, request, allowPreview });
  if (name === "protocol.execute") return compileProtocolMethod({ method: request.method, params: request.params, device, support: device?.support, request, allowPreview });
  const method = OPERATION_METHODS.get(name);
  if (!method) throw new OperationError("operation_not_supported", "The semantic operation is not cataloged.", { operation: name });
  const params = paramsForOperation(name, method, request);
  return compileProtocolMethod({ method, params, device, support: device?.support, request, allowPreview });
}

export const compileSemanticOperation = compileOperation;

export function verificationPlan(compiled) {
  return { status: compiled?.verification?.length ? "read_after_write" : "acknowledged", properties: [...(compiled?.verification || [])] };
}

function paramsForOperation(name, method, input) {
  if (name === "power.set" || name === "background.power.set") return [requiredString(input.power, "power"), input.effect || "sudden", integerOrDefault(input.duration, 0), ...(input.mode === undefined ? [] : [input.mode])];
  if (name === "brightness.set" || name === "background.brightness.set") return [requiredInteger(input.brightness ?? input.bright, "brightness"), input.effect || "sudden", integerOrDefault(input.duration, 0)];
  if (name === "color.rgb" || name === "background.color.rgb") return [requiredInteger(input.rgb ?? input.color, "rgb"), input.effect || "sudden", integerOrDefault(input.duration, 0)];
  if (name === "color.hsv" || name === "background.color.hsv") return [requiredInteger(input.hue, "hue"), requiredInteger(input.saturation ?? input.sat, "saturation"), input.effect || "sudden", integerOrDefault(input.duration, 0)];
  if (name === "color.temperature" || name === "background.color.temperature") return [requiredInteger(input.temperature ?? input.ct, "temperature"), input.effect || "sudden", integerOrDefault(input.duration, 0)];
  if (name === "power.toggle" || name === "background.power.toggle" || name === "device.toggle_both") return [];
  if (name === "adjust") return [requiredString(input.action, "action"), requiredString(input.property || input.prop, "property")];
  if (name === "background.adjust") return [requiredString(input.action, "action"), requiredString(input.property || input.prop, "property")];
  if (name === "adjust.brightness" || name === "adjust.temperature" || name === "adjust.color" || name === "background.adjust.brightness" || name === "background.adjust.temperature" || name === "background.adjust.color") return [requiredInteger(input.percentage ?? input.value, "percentage"), integerOrDefault(input.duration, 30)];
  if (name === "flow.start" || name === "background.flow.start") return [integerOrDefault(input.count, 0), integerOrDefault(input.action, 0), normalizeFlowExpression(input.flow || input.expression, method)];
  if (name === "flow.stop" || name === "background.flow.stop") return [];
  if (name === "scene.apply" || name === "background.scene.apply") return sceneParams(input);
  if (name === "timer.set") return [0, requiredInteger(input.minutes ?? input.delay, "minutes")];
  if (name === "timer.get" || name === "timer.cancel") return [0];
  if (name === "default.save" || name === "background.default.save") return [];
  if (name === "name.set") return [String(input.name ?? "")];
  if (name === "music.play") {
    const host = requiredString(input.host, "host");
    if (!isCanonicalIPv4(host) || !isPrivateIPv4(host, { includeLinkLocal: true })) throw new OperationError("music_host_invalid", "Music mode requires an eligible private IPv4 listener.");
    return [1, host, requiredInteger(input.port, "port")];
  }
  if (name === "music.stop") return [0];
  throw new OperationError("operation_params_invalid", "The semantic operation parameters are unsupported.", { operation: name });
}

function sceneParams(input) {
  if (Array.isArray(input.params)) return input.params;
  const sceneClass = input.class || input.sceneClass;
  if (sceneClass === "color") return [sceneClass, requiredInteger(input.rgb, "rgb"), requiredInteger(input.brightness, "brightness")];
  if (sceneClass === "hsv") return [sceneClass, requiredInteger(input.hue, "hue"), requiredInteger(input.saturation ?? input.sat, "saturation"), requiredInteger(input.brightness, "brightness")];
  if (sceneClass === "ct") return [sceneClass, requiredInteger(input.temperature ?? input.ct, "temperature"), requiredInteger(input.brightness, "brightness")];
  if (sceneClass === "cf") return [sceneClass, integerOrDefault(input.count, 0), integerOrDefault(input.action, 0), normalizeFlowExpression(input.flow || input.expression, "set_scene")];
  if (sceneClass === "auto_delay_off") return [sceneClass, requiredInteger(input.brightness, "brightness"), requiredInteger(input.minutes ?? input.delay, "minutes")];
  throw new OperationError("scene_params_invalid", "The semantic scene class is unsupported.");
}

function validateParams(method, params, support) {
  try { return validateMethodParams(method, params, { support }).params; } catch (error) {
    if (error instanceof CatalogError) throw new OperationError(error.code, error.message, error.details);
    throw error;
  }
}

function assertPrecondition(method, device) {
  const descriptor = catalogMethod(method);
  if (!descriptor?.precondition || !device) return;
  const props = device.props || device.state || {};
  const background = method.startsWith("bg_");
  const state = props[background ? "bg_power" : "power"];
  if (state !== undefined && state !== "on") throw new OperationError("precondition_not_met", "The device is not on for this operation.", { method });
}

function expandTarget(target) {
  if (target === null || target === undefined) return [];
  if (Array.isArray(target)) return target.flatMap(expandTarget);
  if (typeof target === "string") return [{ deviceId: target }];
  if (typeof target !== "object") return [];
  const nested = target.devices || target.deviceIds || target.members || target.targets;
  if (nested) return expandTarget(nested);
  const deviceId = target.deviceId || target.protocolId || (target.kind === "device" ? target.id : null) || (target.type === "device" ? target.id : null);
  return deviceId ? [{ ...target, deviceId: String(deviceId) }] : target.id ? [{ ...target, deviceId: String(target.id) }] : [];
}

export function planTargetActions(input, maybeActions) {
  const { actions, targets } = Array.isArray(input) ? { actions: input, targets: maybeActions } : input || {};
  if (!Array.isArray(actions)) throw new OperationError("plan_invalid", "The execution planner requires an action array.");
  const rows = [];
  for (const action of actions) {
    const selected = expandTarget(action.targets || action.target || action.deviceId || targets);
    for (const target of selected) rows.push({ deviceId: target.deviceId, action: normalizeAction(action) });
  }
  const byDevice = new Map();
  const conflicts = [];
  const deduped = [];
  for (const row of rows) {
    if (!row.deviceId) { conflicts.push({ code: "target_invalid" }); continue; }
    const key = row.deviceId;
    const existing = byDevice.get(key) || [];
    const same = existing.find((item) => stable(item.action) === stable(row.action));
    if (same && row.action.idempotent !== false) continue;
    if (existing.length) {
      const repeatedNonIdempotent = existing.some((item) => item.action.idempotent === false || row.action.idempotent === false);
      if (repeatedNonIdempotent || existing.some((item) => stable(item.action) !== stable(row.action))) {
        conflicts.push({ code: repeatedNonIdempotent ? "repeated_non_idempotent" : "conflicting_actions", deviceId: key });
        continue;
      }
    }
    existing.push(row);
    byDevice.set(key, existing);
    deduped.push(row);
  }
  return { ok: conflicts.length === 0, actions: conflicts.length ? [] : deduped, conflicts, deviceIds: [...byDevice.keys()] };
}

export const buildExecutionPlan = planTargetActions;
export const planGlobalActions = planTargetActions;
export const buildGlobalExecutionPlan = planTargetActions;

function normalizeAction(action) {
  const method = action.method || (action.operation && OPERATION_METHODS.get(action.operation));
  return { method: method || null, operation: action.operation || null, params: action.params || [], idempotent: action.idempotent === undefined ? method ? isIdempotentMethod(method) : false : action.idempotent };
}

function requiredString(value, name) {
  if (typeof value !== "string" || !value) throw new OperationError("operation_params_invalid", `The ${name} parameter is required.`, { field: name });
  return value;
}

function requiredInteger(value, name) {
  if (!Number.isInteger(value)) throw new OperationError("operation_params_invalid", `The ${name} parameter must be an integer.`, { field: name });
  return value;
}

function integerOrDefault(value, fallback) {
  return value === undefined ? fallback : requiredInteger(value, "value");
}

function stable(value) {
  return JSON.stringify(value, Object.keys(value || {}).sort());
}

function sanitize(details) {
  const output = {};
  for (const [key, value] of Object.entries(details).slice(0, 8)) if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") output[key] = typeof value === "string" ? value.slice(0, 120) : value;
  return output;
}
