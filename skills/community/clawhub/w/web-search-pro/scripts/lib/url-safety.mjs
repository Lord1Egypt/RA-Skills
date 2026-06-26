import dns from "node:dns/promises";
import net from "node:net";

const BLOCKED_HOSTNAMES = new Set([
  "localhost",
  "metadata.google.internal",
  "metadata.google.internal.",
]);

function isPrivateIpv4(address) {
  const octets = address.split(".").map((part) => Number.parseInt(part, 10));
  if (
    octets.length !== 4 ||
    octets.some((value) => !Number.isInteger(value) || value < 0 || value > 255)
  ) {
    return false;
  }

  const [a, b] = octets;
  if (a === 0 || a === 10 || a === 127) {
    return true;
  }
  if (a === 100 && b >= 64 && b <= 127) {
    return true;
  }
  if (a === 169 && b === 254) {
    return true;
  }
  if (a === 172 && b >= 16 && b <= 31) {
    return true;
  }
  if (a === 192 && b === 168) {
    return true;
  }
  if (a >= 224) {
    return true;
  }
  return false;
}

function normalizeIpv6(address) {
  return address.toLowerCase();
}

function isPrivateIpv6(address) {
  const normalized = normalizeIpv6(address);
  return (
    normalized === "::" ||
    normalized === "::1" ||
    normalized.startsWith("fc") ||
    normalized.startsWith("fd") ||
    normalized.startsWith("fe8") ||
    normalized.startsWith("fe9") ||
    normalized.startsWith("fea") ||
    normalized.startsWith("feb")
  );
}

export function isPrivateIpAddress(address) {
  const family = net.isIP(address);
  if (family === 4) {
    return isPrivateIpv4(address);
  }
  if (family === 6) {
    return isPrivateIpv6(address);
  }
  return false;
}

async function defaultLookupAll(hostname) {
  return dns.lookup(hostname, { all: true, verbatim: true });
}

export async function assertSafeRemoteUrl(input, options = {}) {
  const lookupAll = options.lookupAll ?? defaultLookupAll;
  const url = new URL(input);

  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("Only http and https URLs are allowed");
  }
  if (url.username || url.password) {
    throw new Error("Credential-bearing URLs are not allowed");
  }

  const hostname = url.hostname.toLowerCase();
  if (
    BLOCKED_HOSTNAMES.has(hostname) ||
    hostname.endsWith(".local") ||
    hostname.endsWith(".localhost") ||
    hostname.endsWith(".internal")
  ) {
    throw new Error(`Host ${hostname} is not allowed`);
  }

  if (net.isIP(hostname)) {
    if (isPrivateIpAddress(hostname)) {
      throw new Error(`Address ${hostname} is not allowed`);
    }
    return {
      url,
      hostname,
      addresses: [{ address: hostname, family: net.isIP(hostname) }],
    };
  }

  const addresses = await lookupAll(hostname);
  if (!Array.isArray(addresses) || addresses.length === 0) {
    throw new Error(`Could not resolve ${hostname}`);
  }
  for (const entry of addresses) {
    if (isPrivateIpAddress(entry.address)) {
      throw new Error(`Resolved private address ${entry.address} for ${hostname}`);
    }
  }

  return {
    url,
    hostname,
    addresses,
  };
}
