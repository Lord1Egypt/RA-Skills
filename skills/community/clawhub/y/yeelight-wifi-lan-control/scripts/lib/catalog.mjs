import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
const CATALOG_PATH = path.resolve(MODULE_DIR, "../../assets/protocol-catalog.json");
const MAX_DIAGNOSTIC_TEXT = 160;

export const PROTOCOL_CATALOG = Object.freeze(JSON.parse(fs.readFileSync(CATALOG_PATH, "utf8")));
export const METHOD_NAMES = Object.freeze(PROTOCOL_CATALOG.methods.map((method) => method.name));
export const PROPERTY_NAMES = Object.freeze(PROTOCOL_CATALOG.properties.map((property) => property.name));
export const WIRE_PROPERTY_NAMES = Object.freeze(PROTOCOL_CATALOG.properties.filter((property) => !property.private).map((property) => property.name));
export const METHODS = Object.freeze(Object.fromEntries(PROTOCOL_CATALOG.methods.map((method) => [method.name, method])));
export const PROPERTIES = Object.freeze(Object.fromEntries(PROTOCOL_CATALOG.properties.map((property) => [property.name, property])));

const ENUMS = Object.freeze({
  effect: new Set(["sudden", "smooth"]),
  power: new Set(["on", "off"]),
  sceneClass: new Set(["color", "hsv", "ct", "cf", "auto_delay_off"]),
  adjustAction: new Set(["bright", "ct", "color"]),
});

export class CatalogError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "CatalogError";
    this.code = code;
    this.details = sanitizeDiagnostics(details);
  }
}

export function catalogMethod(name) {
  return typeof name === "string" ? METHODS[name] || null : null;
}

export const getMethod = catalogMethod;

export function catalogProperty(name) {
  return typeof name === "string" ? PROPERTIES[name] || null : null;
}

export const getProperty = catalogProperty;

export function isCatalogMethod(name) {
  return Boolean(catalogMethod(name));
}

export function isCatalogProperty(name) {
  return Boolean(catalogProperty(name));
}

export function isWireProperty(name) {
  return WIRE_PROPERTY_NAMES.includes(name);
}

export function validateCatalog(catalog = PROTOCOL_CATALOG) {
  const errors = [];
  if (!catalog || typeof catalog !== "object") return ["catalog_not_object"];
  if (catalog.version !== 1) errors.push("catalog_version_invalid");
  if (!Array.isArray(catalog.methods) || catalog.methods.length !== 35) errors.push("method_count_invalid");
  if (!Array.isArray(catalog.properties) || catalog.properties.length !== 25) errors.push("property_count_invalid");
  const methodSet = new Set();
  for (const method of catalog.methods || []) {
    if (!method || typeof method.name !== "string" || !/^[-a-z0-9_]+$/.test(method.name)) errors.push("method_name_invalid");
    else if (methodSet.has(method.name)) errors.push(`duplicate_method:${method.name}`);
    else methodSet.add(method.name);
    if (!Array.isArray(method.params) || !method.arity || !Number.isInteger(method.arity.min) || !Number.isInteger(method.arity.max) || method.arity.min < 0 || method.arity.max < method.arity.min) errors.push(`method_shape:${method?.name || "unknown"}`);
  }
  const propertySet = new Set();
  for (const property of catalog.properties || []) {
    if (!property || typeof property.name !== "string" || !/^[a-z][a-z0-9_]*$/.test(property.name)) errors.push("property_name_invalid");
    else if (propertySet.has(property.name)) errors.push(`duplicate_property:${property.name}`);
    else propertySet.add(property.name);
  }
  return errors;
}

export function assertValidCatalog(catalog = PROTOCOL_CATALOG) {
  const errors = validateCatalog(catalog);
  if (errors.length) throw new CatalogError("catalog_invalid", "The protocol catalog is invalid.", { errors });
  return true;
}

/**
 * Normalize a support value from discovery. Devices have emitted both a
 * comma-separated string and an array in the wild; no other value is trusted.
 */
export function normalizeSupport(support) {
  const values = Array.isArray(support) ? support : typeof support === "string" ? support.split(/[\s,]+/) : [];
  return [...new Set(values.map((value) => String(value).trim()).filter((value) => isCatalogMethod(value)))].sort();
}

export function supportsMethod(support, method) {
  if (support === undefined || support === null || support === "") return { known: false, supported: true };
  const normalized = normalizeSupport(support);
  return { known: true, supported: normalized.includes(method), support: normalized };
}

export function validateMethodParams(methodName, params, options = {}) {
  const method = catalogMethod(methodName);
  if (!method) throw new CatalogError("method_not_supported", "The requested protocol method is not cataloged.", { method: methodName });
  if (!Array.isArray(params)) throw new CatalogError("params_invalid", "Protocol parameters must be an array.", { method: methodName });
  if (params.length < method.arity.min || params.length > method.arity.max) {
    throw new CatalogError("arity_invalid", "The protocol method received an invalid number of parameters.", { method: methodName, expected: method.arity, actual: params.length });
  }
  const normalized = normalizeParams(methodName, params, options);
  const support = supportsMethod(options.support, methodName);
  if (!support.supported) throw new CatalogError("method_not_supported", "The device does not advertise this method.", { method: methodName, support: support.support });
  return { method: methodName, params: normalized, support };
}

export const validateParams = validateMethodParams;

export function normalizeParams(methodName, params, options = {}) {
  const method = catalogMethod(methodName);
  if (!method) throw new CatalogError("method_not_supported", "The requested protocol method is not cataloged.", { method: methodName });
  if (!Array.isArray(params)) throw new CatalogError("params_invalid", "Protocol parameters must be an array.", { method: methodName });
  if (params.length < method.arity.min || params.length > method.arity.max) throw new CatalogError("arity_invalid", "The protocol method received an invalid number of parameters.", { method: methodName, expected: method.arity, actual: params.length });
  if (methodName === "set_scene" || methodName === "bg_set_scene") return normalizeSceneParams(methodName, params);
  if (methodName === "start_cf" || methodName === "bg_start_cf") return normalizeFlowParams(methodName, params);
  const output = [];
  for (let index = 0; index < params.length; index += 1) {
    const descriptor = method.params[index] || method.params[method.params.length - 1];
    output.push(validateValue(descriptor, params[index], { methodName, index, options }));
  }
  if (["set_ct_abx", "set_rgb", "set_hsv", "set_bright", "set_power", "bg_set_rgb", "bg_set_hsv", "bg_set_ct_abx", "bg_set_power", "bg_set_bright"].includes(methodName) && output[1] === "smooth" && output[2] < 30) throw new CatalogError("duration_invalid", "A smooth transition duration must be at least 30 ms.", { method: methodName });
  if (methodName === "set_music" && output[0] === 0 && output.length !== 1) throw new CatalogError("music_stop_shape_invalid", "Stopping music mode accepts only action 0.", { method: methodName });
  if (methodName === "set_music" && output[0] === 1 && output.length !== 3) throw new CatalogError("music_start_shape_invalid", "Starting music mode requires an IPv4 host and port.", { method: methodName });
  if ((methodName === "set_adjust" || methodName === "bg_set_adjust") && output[1] === "color" && output[0] !== "circle") throw new CatalogError("adjust_action_invalid", "Color adjustment only supports the circle action.", { method: methodName });
  return output;
}

function normalizeFlowParams(methodName, params) {
  const [count, action, flow] = params;
  if (!Number.isInteger(count) || count < 0 || count > 65535) throw new CatalogError("count_invalid", "Flow count must be a non-negative bounded integer.", { method: methodName });
  if (![0, 1, 2].includes(action)) throw new CatalogError("flow_action_invalid", "Flow action must be 0, 1, or 2.", { method: methodName });
  const normalizedFlow = normalizeFlowExpression(flow, methodName);
  return [count, action, normalizedFlow];
}

export function normalizeFlow(flow, methodName = "start_cf") {
  if (!Array.isArray(flow) || flow.length === 0 || flow.length > 32) throw new CatalogError("flow_invalid", "A flow must contain one to 32 tuples.", { method: methodName });
  const tuples = flow.map((tuple, tupleIndex) => {
    if (!Array.isArray(tuple) || tuple.length !== 4) throw new CatalogError("flow_tuple_invalid", "Every flow tuple must contain duration, mode, value, and brightness.", { method: methodName, tuple: tupleIndex });
    const [duration, mode, value, brightness] = tuple;
    if (!Number.isInteger(duration) || duration < 50 || duration > 86400000) throw new CatalogError("duration_invalid", "Flow duration must be at least 50 ms.", { method: methodName, tuple: tupleIndex });
    if (![1, 2, 7].includes(mode)) throw new CatalogError("flow_mode_invalid", "Flow mode must be RGB (1), CT (2), or sleep (7).", { method: methodName, tuple: tupleIndex });
    if (!Number.isInteger(value) || (mode === 1 && (value < 0 || value > 16777215)) || (mode === 2 && (value < 1700 || value > 6500)) || (mode === 7 && !Number.isInteger(value))) throw new CatalogError("flow_value_invalid", "The flow tuple value is outside the PDF range.", { method: methodName, tuple: tupleIndex });
    if (!Number.isInteger(brightness) || (mode !== 7 && brightness !== -1 && (brightness < 1 || brightness > 100))) throw new CatalogError("flow_brightness_invalid", "Flow brightness must be -1 or 1..100.", { method: methodName, tuple: tupleIndex });
    return [duration, mode, value, brightness];
  });
  return tuples;
}

export function normalizeFlowExpression(flow, methodName = "start_cf") {
  if (typeof flow === "string") {
    if (Buffer.byteLength(flow, "utf8") > 4096 || !/^[0-9,\s-]+$/.test(flow) || /(^|,)\s*,/.test(flow)) throw new CatalogError("flow_expression_invalid", "The flow expression contains unsupported text.", { method: methodName });
    const values = flow.split(",").map((value) => Number(value.trim()));
    if (values.length === 0 || values.length % 4 !== 0 || values.some((value) => !Number.isInteger(value))) throw new CatalogError("flow_expression_invalid", "The flow expression must contain groups of four integers.", { method: methodName });
    normalizeFlow(Array.from({ length: values.length / 4 }, (_, index) => values.slice(index * 4, index * 4 + 4)), methodName);
    return values.join(",");
  }
  return normalizeFlow(flow, methodName).flat().join(",");
}

function normalizeSceneParams(methodName, params) {
  const [sceneClass, ...values] = params;
  if (!ENUMS.sceneClass.has(sceneClass)) throw new CatalogError("scene_class_invalid", "The scene class is not supported by the PDF.", { method: methodName, sceneClass });
  const expected = { color: 2, hsv: 3, ct: 2, cf: 3, auto_delay_off: 2 }[sceneClass];
  if (values.length !== expected) throw new CatalogError("scene_shape_invalid", "The scene values do not match the selected scene class.", { method: methodName, sceneClass, expected, actual: values.length });
  if (sceneClass === "color") return [sceneClass, validateValue({ type: "integer", minimum: 0, maximum: 16777215 }, values[0], { methodName }), validateValue({ type: "integer", minimum: 1, maximum: 100 }, values[1], { methodName })];
  if (sceneClass === "hsv") return [sceneClass, validateValue({ type: "integer", minimum: 0, maximum: 359 }, values[0], { methodName }), validateValue({ type: "integer", minimum: 0, maximum: 100 }, values[1], { methodName }), validateValue({ type: "integer", minimum: 1, maximum: 100 }, values[2], { methodName })];
  if (sceneClass === "ct") return [sceneClass, validateValue({ type: "integer", minimum: 1700, maximum: 6500 }, values[0], { methodName }), validateValue({ type: "integer", minimum: 1, maximum: 100 }, values[1], { methodName })];
  if (sceneClass === "cf") {
    if (values.length !== 3) throw new CatalogError("scene_shape_invalid", "A color-flow scene requires count, action, and flow expression.", { method: methodName });
    const [count, action, flow] = normalizeFlowParams(methodName, values);
    return [sceneClass, count, action, flow];
  }
  if (sceneClass === "auto_delay_off") return [sceneClass, validateValue({ type: "integer", minimum: 1, maximum: 100 }, values[0], { methodName }), validateValue({ type: "integer", minimum: 1, maximum: 60 }, values[1], { methodName })];
  return [sceneClass, ...values];
}

function validateValue(descriptor, value, context) {
  const { methodName, index } = context;
  if (value === undefined && descriptor?.optional) return undefined;
  const type = descriptor?.type;
  if (type === "integer" || type === "duration" || type === "port" || type === "percentage" || type === "enumInteger") {
    if (!Number.isInteger(value)) throw new CatalogError("param_type_invalid", "A protocol numeric parameter must be an integer.", { method: methodName, index });
    if (descriptor.minimum !== undefined && value < descriptor.minimum || descriptor.maximum !== undefined && value > descriptor.maximum) throw new CatalogError("param_range_invalid", "A protocol numeric parameter is outside its allowed range.", { method: methodName, index });
    if (type === "port" && (value < 1 || value > 65535)) throw new CatalogError("port_invalid", "The port is outside the IPv4 TCP range.", { method: methodName, index });
    if (type === "enumInteger" && !descriptor.enum.includes(value)) throw new CatalogError("enum_invalid", "A protocol enum value is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "enum") {
    if (typeof value !== "string" || !descriptor.enum.includes(value)) throw new CatalogError("enum_invalid", "A protocol enum value is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "string") {
    if (typeof value !== "string" || /[\u0000-\u001f\u007f]/.test(value)) throw new CatalogError("string_invalid", "A protocol string contains unsupported characters.", { method: methodName, index });
    if (descriptor.maxBytes && Buffer.byteLength(value, "utf8") > descriptor.maxBytes) throw new CatalogError("name_too_long", "The protocol string exceeds its byte limit.", { method: methodName, index, maxBytes: descriptor.maxBytes });
    return value;
  }
  if (type === "ipv4") {
    if (typeof value !== "string" || !/^\d{1,3}(?:\.\d{1,3}){3}$/.test(value)) throw new CatalogError("ipv4_invalid", "The protocol host must be an IPv4 address.", { method: methodName, index });
    return value;
  }
  if (type === "propertyList") {
    if (!Array.isArray(value) || value.length < (descriptor.minItems || 1) || value.length > (descriptor.maxItems || 25) || value.some((item) => !isWireProperty(item))) throw new CatalogError("property_list_invalid", "The property list contains an unknown or duplicate property.", { method: methodName, index });
    if (new Set(value).size !== value.length) throw new CatalogError("property_list_invalid", "The property list contains duplicate properties.", { method: methodName, index });
    return [...value];
  }
  if (type === "adjustAction") {
    if (typeof value !== "string" || !ENUMS.adjustAction.has(value)) throw new CatalogError("adjust_action_invalid", "The adjustment action is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "adjustDirection") {
    if (typeof value !== "string" || !["increase", "decrease", "circle"].includes(value)) throw new CatalogError("adjust_action_invalid", "The adjustment direction is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "adjustProperty") {
    if (typeof value !== "string" || !["bright", "ct", "color"].includes(value)) throw new CatalogError("adjust_property_invalid", "The adjustment property is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "sceneClass") {
    if (typeof value !== "string" || !ENUMS.sceneClass.has(value)) throw new CatalogError("scene_class_invalid", "The scene class is invalid.", { method: methodName, index });
    return value;
  }
  if (type === "sceneValues" || type === "flow" || type === "flowExpression") return value;
  return value;
}

export function getVerificationProperties(methodName) {
  return [...(catalogMethod(methodName)?.verify || [])];
}

export function isIdempotentMethod(methodName) {
  const method = catalogMethod(methodName);
  if (!method) return false;
  return method.idempotent !== false;
}

export function requiresExecution(methodName) {
  return catalogMethod(methodName) ? methodName !== "get_prop" && methodName !== "cron_get" : false;
}

export function methodRequiresConfirmation(methodName) {
  return Boolean(catalogMethod(methodName)?.special);
}

function sanitizeDiagnostics(value) {
  if (!value || typeof value !== "object") return {};
  const output = {};
  for (const [key, raw] of Object.entries(value).slice(0, 12)) {
    if (typeof raw === "string") output[key] = raw.replace(/[\u0000-\u001f\u007f]/g, "?").slice(0, MAX_DIAGNOSTIC_TEXT);
    else if (typeof raw === "number" || typeof raw === "boolean" || raw === null) output[key] = raw;
    else if (Array.isArray(raw)) output[key] = raw.slice(0, 16).map((item) => typeof item === "string" ? item.slice(0, MAX_DIAGNOSTIC_TEXT) : item);
  }
  return output;
}

assertValidCatalog();
