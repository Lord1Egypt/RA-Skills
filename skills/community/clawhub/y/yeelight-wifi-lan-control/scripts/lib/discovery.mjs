import dgram from "node:dgram";
import { DEFAULT_CONTROL_PORT, DEFAULT_DISCOVERY_ENDPOINT, validateSenderBoundLocation, normalizeIPv4, isCanonicalIPv4 } from "./network-policy.mjs";

export const SEARCH_REQUEST = [
  "M-SEARCH * HTTP/1.1",
  `HOST: ${DEFAULT_DISCOVERY_ENDPOINT.host}:${DEFAULT_DISCOVERY_ENDPOINT.port}`,
  'MAN: "ssdp:discover"',
  "ST: wifi_bulb",
  "",
  "",
].join("\r\n");

export class DiscoveryError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "DiscoveryError";
    this.code = code;
    this.details = diagnostics(details);
  }
}

export function buildSearchRequest() {
  return SEARCH_REQUEST;
}

export function canonicalDeviceId(value) {
  if (typeof value !== "string" || !/^0x[0-9a-fA-F]{16}$/.test(value)) return null;
  return `0x${value.slice(2).toLowerCase()}`;
}

export function isCanonicalDeviceId(value) {
  return Boolean(canonicalDeviceId(value));
}

export function parseSsdpMessage(input, { senderAddress = null, kind = "response", maxBytes = 65536 } = {}) {
  const bytes = Buffer.isBuffer(input) ? input : Buffer.from(String(input), "utf8");
  if (bytes.length > maxBytes) throw new DiscoveryError("discovery_frame_too_large", "The discovery response exceeded its size limit.");
  const text = bytes.toString("utf8");
  if (text.includes("\u0000") || /(?:^|[^\r])\n/.test(text) || /\r(?!\n)/.test(text)) throw new DiscoveryError("discovery_framing_invalid", "The discovery response did not use CRLF framing.");
  const lines = text.split("\r\n");
  if (lines.at(-1) !== "" || lines.at(-2) !== "") throw new DiscoveryError("discovery_framing_invalid", "The discovery response was not terminated by an empty CRLF line.");
  const startLine = lines.shift();
  const normalizedKind = kind === "advertisement" || kind === "notify" ? "notify" : "response";
  if (normalizedKind === "response" && startLine !== "HTTP/1.1 200 OK") throw new DiscoveryError("discovery_start_line_invalid", "The discovery response start line is invalid.");
  if (normalizedKind === "notify" && startLine !== "NOTIFY * HTTP/1.1") throw new DiscoveryError("discovery_start_line_invalid", "The discovery advertisement start line is invalid.");
  const headers = new Map();
  for (const line of lines.slice(0, -2)) {
    if (!line) continue;
    const separator = line.indexOf(":");
    if (separator <= 0) throw new DiscoveryError("discovery_header_invalid", "A discovery header is malformed.");
    const name = line.slice(0, separator).trim().toLowerCase();
    const value = line.slice(separator + 1).trim();
    if (!/^[a-z0-9_-]+$/.test(name) || /[\u0000-\u001f\u007f]/.test(value) || value.length > 2048) throw new DiscoveryError("discovery_header_invalid", "A discovery header contains unsupported characters.");
    if (headers.has(name)) throw new DiscoveryError("discovery_header_duplicate", "A discovery response contains duplicate headers.", { header: name });
    headers.set(name, value);
  }
  if (normalizedKind === "notify" && headers.get("nts") !== "ssdp:alive") throw new DiscoveryError("discovery_advertisement_invalid", "Only ssdp:alive advertisements are accepted.");
  const location = headers.get("location");
  const id = canonicalDeviceId(headers.get("id"));
  if (!location) throw new DiscoveryError("discovery_location_missing", "The discovery response did not include Location.");
  if (!id) throw new DiscoveryError("discovery_id_invalid", "The discovery response did not include a canonical protocol ID.");
  const endpoint = senderAddress ? validateSenderBoundLocation(location, senderAddress, { defaultPort: DEFAULT_CONTROL_PORT }) : parseLocationForFixture(location);
  const device = {
    id,
    endpoint: { host: endpoint.host, port: endpoint.port },
    sender: normalizeIPv4(senderAddress || endpoint.host),
    model: boundedHeader(headers.get("model")),
    firmware: boundedHeader(headers.get("fw_ver")),
    support: boundedHeader(headers.get("support")),
    state: parseStateHeaders(headers),
    name: boundedHeader(headers.get("name")),
    observedAt: Date.now(),
    source: normalizedKind,
  };
  return Object.freeze(device);
}

export function parseDiscoveryResponse(input, options = {}) {
  return parseSsdpMessage(input, { ...options, kind: "response" });
}

export const parseDiscovery = parseDiscoveryResponse;
export const parseSsdp = parseSsdpMessage;

export function parseAdvertisement(input, options = {}) {
  return parseSsdpMessage(input, { ...options, kind: "notify" });
}

export function mergeDiscoveryObservations(observations) {
  const byId = new Map();
  const errors = [];
  for (const observation of observations || []) {
    if (!observation || !canonicalDeviceId(observation.id)) continue;
    const current = byId.get(observation.id);
    if (current && (current.endpoint.host !== observation.endpoint?.host || current.endpoint.port !== observation.endpoint?.port)) {
      errors.push({ code: "identity_collision", id: observation.id });
      byId.delete(observation.id);
      continue;
    }
    if (!current || Number(observation.observedAt || 0) >= Number(current.observedAt || 0)) byId.set(observation.id, observation);
  }
  const collisionIds = new Set(errors.map((error) => error.id));
  return { devices: [...byId.values()].filter((device) => !collisionIds.has(device.id)), errors, collisionIds: [...collisionIds] };
}

export const dedupeDiscoveryObservations = mergeDiscoveryObservations;

export async function discover({
  socketFactory = () => dgram.createSocket("udp4"),
  deadlineMs = 1500,
  includeAdvertisements = false,
  signal,
  senderAddress = null,
  maxDatagrams = 64,
} = {}) {
  if (!Number.isInteger(deadlineMs) || deadlineMs < 50 || deadlineMs > 10000) throw new DiscoveryError("discovery_deadline_invalid", "The discovery deadline is outside its safe bound.");
  const socket = socketFactory();
  const observations = [];
  const parseErrors = [];
  let timer;
  let settled = false;
  const close = () => { try { socket.close(); } catch {} };
  try {
    const result = await new Promise((resolve, reject) => {
      const finish = () => { if (settled) return; settled = true; clearTimeout(timer); resolve(mergeDiscoveryObservations(observations)); };
      socket.once("error", (error) => reject(new DiscoveryError("discovery_socket_error", "The local discovery socket failed.", { name: error?.code || "socket_error" })));
      socket.on("message", (message, remote) => {
        if (observations.length + parseErrors.length >= maxDatagrams) return;
        const remoteAddress = senderAddress || remote?.address;
        try {
          const parsed = parseSsdpMessage(message, { senderAddress: remoteAddress, kind: "response" });
          observations.push(parsed);
        } catch (error) {
          if (includeAdvertisements) {
            try { observations.push(parseSsdpMessage(message, { senderAddress: remoteAddress, kind: "notify" })); return; } catch {}
          }
          parseErrors.push(error?.code || "discovery_invalid");
        }
      });
      socket.bind(0, "0.0.0.0", () => {
        try { socket.send(Buffer.from(SEARCH_REQUEST, "utf8"), DEFAULT_DISCOVERY_ENDPOINT.port, DEFAULT_DISCOVERY_ENDPOINT.host, (error) => { if (error) reject(new DiscoveryError("discovery_send_error", "The discovery request could not be sent.")); }); } catch { reject(new DiscoveryError("discovery_send_error", "The discovery request could not be sent.")); }
      });
      timer = setTimeout(finish, deadlineMs);
      if (signal) {
        if (signal.aborted) finish();
        else signal.addEventListener("abort", finish, { once: true });
      }
    });
    return { ...result, parseErrors: parseErrors.slice(0, 16) };
  } finally {
    clearTimeout(timer);
    close();
  }
}

export const discoverDevices = discover;

function parseLocationForFixture(location) {
  const match = /^yeelight:\/\/(\d{1,3}(?:\.\d{1,3}){3})(?::(\d+))?$/.exec(location);
  if (!match || !isCanonicalIPv4(match[1])) throw new DiscoveryError("location_invalid", "The discovery Location is malformed.");
  return { host: match[1], port: match[2] ? Number(match[2]) : DEFAULT_CONTROL_PORT };
}

function parseStateHeaders(headers) {
  const state = {};
  for (const property of ["power", "bright", "ct", "rgb", "hue", "sat", "color_mode", "flowing", "delayoff", "flow_params", "music_on", "bg_power", "bg_flowing", "bg_flow_params", "bg_ct", "bg_lmode", "bg_bright", "bg_rgb", "bg_hue", "bg_sat", "nl_br", "active_mode"]) {
    const value = headers.get(property);
    if (value !== undefined) state[property] = boundedHeader(value);
  }
  return state;
}

function boundedHeader(value) {
  return typeof value === "string" && value.length <= 512 ? value : value === undefined ? undefined : String(value).slice(0, 512);
}

function diagnostics(details = {}) {
  const output = {};
  for (const [key, value] of Object.entries(details).slice(0, 8)) if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") output[key] = typeof value === "string" ? value.slice(0, 96) : value;
  return output;
}
