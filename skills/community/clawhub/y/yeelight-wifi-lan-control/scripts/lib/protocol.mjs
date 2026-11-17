import { isWireProperty, validateMethodParams, CatalogError } from "./catalog.mjs";

export const CRLF = "\r\n";

export class ProtocolError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "ProtocolError";
    this.code = code;
    this.details = sanitizeDetails(details);
  }
}

export function encodeCommand(id, method, params, options = {}) {
  if (!Number.isSafeInteger(id) || id < 1) throw new ProtocolError("request_id_invalid", "A protocol request ID must be a positive safe integer.");
  let normalized;
  try { normalized = options.validate === false ? params : validateMethodParams(method, params, options).params; } catch (error) {
    if (error instanceof CatalogError) throw new ProtocolError(error.code, error.message, error.details);
    throw error;
  }
  const body = JSON.stringify({ id, method, params: normalized });
  if (Buffer.byteLength(body, "utf8") > (options.maxFrameBytes || 65536) - 2) throw new ProtocolError("frame_too_large", "The protocol command exceeds its frame limit.");
  return `${body}${CRLF}`;
}

export function parseProtocolFrame(frame, { maxFrameBytes = 65536 } = {}) {
  if (typeof frame !== "string" && !Buffer.isBuffer(frame)) throw new ProtocolError("frame_type_invalid", "A protocol frame must be text.");
  const text = Buffer.isBuffer(frame) ? frame.toString("utf8") : frame;
  if (Buffer.byteLength(text, "utf8") > maxFrameBytes) throw new ProtocolError("frame_too_large", "The protocol frame exceeds its size limit.");
  if (text.includes("\r") || text.includes("\n") || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(text)) throw new ProtocolError("frame_framing_invalid", "A complete protocol frame contains unsupported control characters.");
  let value;
  try { value = JSON.parse(text); } catch { throw new ProtocolError("json_invalid", "The device returned invalid JSON."); }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new ProtocolError("message_shape_invalid", "The device message must be a JSON object.");
  if (Object.prototype.hasOwnProperty.call(value, "method")) {
    if (value.method !== "props" || !value.params || typeof value.params !== "object" || Array.isArray(value.params) || Object.prototype.hasOwnProperty.call(value, "id")) throw new ProtocolError("notification_invalid", "The device notification shape is unsupported.");
    const notification = parsePropsNotification(value.params);
    return { kind: "notification", method: "props", props: notification.props, ignored: notification.ignored };
  }
  if (!Number.isSafeInteger(value.id) || value.id < 1 || Object.prototype.hasOwnProperty.call(value, "method")) throw new ProtocolError("response_shape_invalid", "The device response does not contain a valid request ID.");
  if (Object.prototype.hasOwnProperty.call(value, "result") && Object.prototype.hasOwnProperty.call(value, "error")) throw new ProtocolError("response_shape_invalid", "The device response cannot contain both result and error.");
  if (Object.prototype.hasOwnProperty.call(value, "result")) return { kind: "result", id: value.id, result: Array.isArray(value.result) ? value.result : value.result === null ? [] : [value.result] };
  if (Object.prototype.hasOwnProperty.call(value, "error")) return { kind: "error", id: value.id, error: sanitizeDeviceError(value.error) };
  return { kind: "unknown", id: value.id, details: {} };
}

export function parsePropsNotification(params) {
  const props = {};
  const ignored = [];
  for (const [key, value] of Object.entries(params).slice(0, 32)) {
    if (!isWireProperty(key)) { ignored.push(key.slice(0, 64)); continue; }
    if (typeof value !== "string" || value.length > 512 || /[\u0000-\u001f\u007f]/.test(value)) throw new ProtocolError("notification_value_invalid", "Notification property values must be bounded strings.", { property: key });
    props[key] = value;
  }
  return { props, ignored };
}

export function sanitizeDeviceError(error) {
  if (!error || typeof error !== "object" || Array.isArray(error)) return { code: "device_error", message: "The device rejected the command." };
  const code = Number.isInteger(error.code) ? error.code : "device_error";
  const message = typeof error.message === "string" ? error.message.replace(/[\u0000-\u001f\u007f]/g, "?").slice(0, 160) : "The device rejected the command.";
  return { code, message };
}

export function nextRequestId(previous = 0) {
  const id = Number.isSafeInteger(previous) && previous > 0 ? previous + 1 : 1;
  return id > Number.MAX_SAFE_INTEGER ? 1 : id;
}

export function isNotification(message) {
  return message?.kind === "notification" && message.method === "props";
}

function sanitizeDetails(details) {
  if (!details || typeof details !== "object") return {};
  const output = {};
  for (const [key, value] of Object.entries(details).slice(0, 10)) {
    if (typeof value === "string") output[key] = value.replace(/[\u0000-\u001f\u007f]/g, "?").slice(0, 160);
    else if (typeof value === "number" || typeof value === "boolean") output[key] = value;
    else if (Array.isArray(value)) output[key] = value.slice(0, 16);
  }
  return output;
}
