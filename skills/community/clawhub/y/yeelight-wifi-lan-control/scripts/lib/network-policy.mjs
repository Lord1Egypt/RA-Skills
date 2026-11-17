import crypto from "node:crypto";
import net from "node:net";

export const DEFAULT_CONTROL_PORT = 55443;
export const DEFAULT_DISCOVERY_ENDPOINT = Object.freeze({ host: "239.255.255.250", port: 1982 });

export class NetworkPolicyError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "NetworkPolicyError";
    this.code = code;
    this.details = opaqueDiagnostics(details);
  }
}

export function parseIPv4(value) {
  if (typeof value !== "string" || value.length < 7 || value.length > 15 || !/^\d{1,3}(?:\.\d{1,3}){3}$/.test(value)) return null;
  const octets = value.split(".").map(Number);
  if (octets.some((octet) => !Number.isInteger(octet) || octet < 0 || octet > 255)) return null;
  return octets;
}

export function normalizeIPv4(value) {
  const octets = parseIPv4(value);
  return octets ? octets.join(".") : null;
}

export function isCanonicalIPv4(value) {
  const normalized = normalizeIPv4(value);
  return Boolean(normalized && normalized === value);
}

export function ipv4ToInteger(value) {
  const octets = Array.isArray(value) ? value : parseIPv4(value);
  if (!octets) return null;
  return (((octets[0] * 256 + octets[1]) * 256 + octets[2]) * 256 + octets[3]) >>> 0;
}

export function integerToIPv4(value) {
  if (!Number.isInteger(value) || value < 0 || value > 0xffffffff) return null;
  return [value >>> 24, value >>> 16 & 255, value >>> 8 & 255, value & 255].join(".");
}

export function classifyIPv4(value) {
  const ip = normalizeIPv4(value);
  if (!ip) return "invalid";
  const number = ipv4ToInteger(ip);
  if (number === 0) return "unspecified";
  if ((number >>> 24) === 127) return "loopback";
  if ((number >>> 24) >= 224) return "multicast";
  if (number === 0xffffffff) return "broadcast";
  if (((number & 0xff000000) >>> 0) === 0x0a000000) return "private";
  if (((number & 0xfff00000) >>> 0) === 0xac100000) return "private";
  if (((number & 0xffff0000) >>> 0) === 0xc0a80000) return "private";
  if (((number & 0xffff0000) >>> 0) === 0xa9fe0000) return "link_local";
  if (((number & 0xffff0000) >>> 0) === 0xc0000000) return "reserved";
  return "public";
}

export function isPrivateIPv4(value, { includeLinkLocal = true } = {}) {
  const classification = classifyIPv4(value);
  return classification === "private" || includeLinkLocal && classification === "link_local";
}

export const isPrivateAddress = isPrivateIPv4;

export function isEligibleLocalUnicastIPv4(value) {
  const classification = classifyIPv4(value);
  return classification === "private" || classification === "link_local";
}

export function isSameIPv4(left, right) {
  const a = normalizeIPv4(left);
  const b = normalizeIPv4(right);
  return Boolean(a && b && a === b);
}

export function parseYeelightLocation(location, { defaultPort = DEFAULT_CONTROL_PORT } = {}) {
  if (typeof location !== "string" || /[\u0000-\u001f\u007f\s]/.test(location)) throw new NetworkPolicyError("location_invalid", "The discovery Location is malformed.");
  let parsed;
  try { parsed = new URL(location); } catch { throw new NetworkPolicyError("location_invalid", "The discovery Location is malformed."); }
  if (parsed.protocol !== "yeelight:" || parsed.username || parsed.password || parsed.search || parsed.hash || parsed.pathname && parsed.pathname !== "/") throw new NetworkPolicyError("location_invalid", "The discovery Location is not a Yeelight IPv4 endpoint.");
  const host = parsed.hostname;
  const normalizedHost = normalizeIPv4(host);
  if (!normalizedHost || !isCanonicalIPv4(host)) throw new NetworkPolicyError("location_host_invalid", "The discovery Location must use a canonical IPv4 host.");
  const port = parsed.port ? Number(parsed.port) : defaultPort;
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new NetworkPolicyError("location_port_invalid", "The discovery Location port is invalid.");
  return Object.freeze({ protocol: "yeelight:", host: normalizedHost, port });
}

export function validateSenderBoundLocation(location, senderAddress, options = {}) {
  const endpoint = parseYeelightLocation(location, options);
  const sender = normalizeIPv4(senderAddress);
  if (!sender) throw new NetworkPolicyError("sender_invalid", "The UDP sender address is not IPv4.");
  if (!isEligibleLocalUnicastIPv4(sender)) throw new NetworkPolicyError("sender_not_local", "The UDP sender address is not an eligible local unicast.", { sender });
  if (endpoint.host !== sender) throw new NetworkPolicyError("location_sender_mismatch", "The discovery Location host does not match the UDP sender.", { sender });
  if (!isEligibleLocalUnicastIPv4(endpoint.host)) throw new NetworkPolicyError("location_not_local", "The discovery Location points outside the local LAN.", { host: endpoint.host });
  return Object.freeze({ ...endpoint, sender });
}

export function parseNetworkInterface(interfaceEntry) {
  if (!interfaceEntry || typeof interfaceEntry !== "object") return null;
  const address = normalizeIPv4(interfaceEntry.address);
  const netmask = normalizeIPv4(interfaceEntry.netmask);
  if (!address || !netmask || !isEligibleLocalUnicastIPv4(address)) return null;
  const mask = ipv4ToInteger(netmask);
  const inverseMask = mask === null ? null : (~mask) >>> 0;
  if (mask === null || (inverseMask & (inverseMask + 1)) !== 0) return null;
  return Object.freeze({ address, netmask, family: "IPv4", internal: interfaceEntry.internal === true });
}

export function isIPv4InSubnet(address, interfaceAddress, netmask) {
  const ip = ipv4ToInteger(address);
  const network = ipv4ToInteger(interfaceAddress);
  const mask = ipv4ToInteger(netmask);
  return ip !== null && network !== null && mask !== null && ((ip & mask) >>> 0) === ((network & mask) >>> 0);
}

export function validatePrivateIPv4Fallback(address, { interfaces = [], port = DEFAULT_CONTROL_PORT, controlPort = DEFAULT_CONTROL_PORT } = {}) {
  if (!isCanonicalIPv4(address)) throw new NetworkPolicyError("fallback_ip_noncanonical", "Direct-IP fallback requires canonical decimal IPv4.");
  if (!isPrivateIPv4(address, { includeLinkLocal: false })) throw new NetworkPolicyError("fallback_ip_not_private", "Direct-IP fallback is limited to private IPv4 ranges.");
  if (port !== controlPort || !Number.isInteger(port) || port < 1 || port > 65535) throw new NetworkPolicyError("fallback_port_invalid", "Direct-IP fallback is limited to the Yeelight control port.", { port });
  const parsedInterfaces = interfaces.map(parseNetworkInterface).filter(Boolean).filter((entry) => !entry.internal);
  if (!parsedInterfaces.some((entry) => isIPv4InSubnet(address, entry.address, entry.netmask))) throw new NetworkPolicyError("fallback_subnet_mismatch", "The fallback address is not on an enabled local interface subnet.");
  return Object.freeze({ host: address, port, source: "explicit_private_ipv4" });
}

export const validateLocalEndpoint = validatePrivateIPv4Fallback;

export function endpointDigest(endpoint) {
  const normalized = typeof endpoint === "string" ? parseYeelightLocation(endpoint) : endpoint;
  if (!normalized || !isCanonicalIPv4(normalized.host) || !Number.isInteger(normalized.port)) throw new NetworkPolicyError("endpoint_invalid", "The endpoint cannot be digested.");
  return crypto.createHash("sha256").update(`${normalized.host}:${normalized.port}`).digest("hex").slice(0, 24);
}

export function validateControlEndpoint(endpoint, { requirePrivate = true, controlPort = null } = {}) {
  const normalized = typeof endpoint === "string" ? parseYeelightLocation(endpoint) : endpoint;
  if (!normalized || !isCanonicalIPv4(normalized.host)) throw new NetworkPolicyError("endpoint_invalid", "The control endpoint is invalid.");
  if (requirePrivate && !isPrivateIPv4(normalized.host, { includeLinkLocal: true })) throw new NetworkPolicyError("endpoint_not_private", "The control endpoint is outside the local LAN.");
  if (controlPort !== null && normalized.port !== controlPort) throw new NetworkPolicyError("endpoint_port_invalid", "The control endpoint uses an unexpected port.");
  return Object.freeze({ host: normalized.host, port: normalized.port });
}

export function socketAddressIsIPv4(address) {
  return net.isIP(address) === 4;
}

function opaqueDiagnostics(details = {}) {
  const output = {};
  for (const [key, value] of Object.entries(details).slice(0, 8)) {
    if (typeof value === "string") output[key] = value.replace(/[\u0000-\u001f\u007f]/g, "?").slice(0, 96);
    else if (typeof value === "number" || typeof value === "boolean") output[key] = value;
  }
  return output;
}
