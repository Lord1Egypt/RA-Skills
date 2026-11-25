import https from 'node:https';
import dns from 'node:dns';
import net from 'node:net';
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import type { LookupFunction } from 'node:net';
import { sanitiseUrl } from './sanitise.js';

export type Resolver = (hostname: string) => Promise<string[]>;

const defaultResolver: Resolver = async (hostname) => {
  const results = await dns.promises.lookup(hostname, { all: true, verbatim: true });
  return results.map((r) => r.address);
};

function ipv4ToInt(ip: string): number {
  return ip.split('.').reduce((acc, octet) => (acc << 8) + Number(octet), 0) >>> 0;
}

const BLOCKED_IPV4_CIDRS: Array<[string, number]> = [
  ['0.0.0.0', 8],
  ['10.0.0.0', 8],
  ['100.64.0.0', 10],
  ['127.0.0.0', 8],
  ['169.254.0.0', 16],
  ['172.16.0.0', 12],
  ['192.0.0.0', 24],
  ['192.0.2.0', 24],
  ['192.168.0.0', 16],
  ['198.18.0.0', 15],
  ['198.51.100.0', 24],
  ['203.0.113.0', 24],
  ['224.0.0.0', 4],
  ['240.0.0.0', 4],
];

function isPublicIpv4(ip: string): boolean {
  const value = ipv4ToInt(ip);
  return !BLOCKED_IPV4_CIDRS.some(([base, bits]) => {
    const mask = bits === 0 ? 0 : (~0 << (32 - bits)) >>> 0;
    return (value & mask) === (ipv4ToInt(base) & mask);
  });
}

/** True only for globally routable unicast addresses. */
export function isPublicAddress(ip: string): boolean {
  if (net.isIPv4(ip)) return isPublicIpv4(ip);
  if (!net.isIPv6(ip)) return false;

  const lower = ip.toLowerCase();
  const mapped = lower.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/);
  if (mapped?.[1]) return isPublicIpv4(mapped[1]);

  if (lower === '::' || lower === '::1') return false;
  // Only global unicast (2000::/3) is public; excludes ULA, link-local, multicast.
  if (!/^[23]/.test(lower)) return false;
  // Documentation (2001:db8::/32), ORCHID/benchmarking ranges and 6to4/Teredo wrap other addresses.
  if (/^2001:0?db8:/.test(lower) || /^2001:0?0?[0-3][0-9a-f]?:/.test(lower) || lower.startsWith('2002:')) {
    return false;
  }
  return true;
}

/** Resolve a hostname and return its addresses, failing if any of them is not public. */
export async function resolvePublicHost(hostname: string, resolver: Resolver = defaultResolver): Promise<string[]> {
  if (net.isIP(hostname)) {
    throw new Error('IP-literal hosts are not permitted');
  }
  const addresses = await resolver(hostname);
  if (addresses.length === 0) {
    throw new Error(`Host "${hostname}" did not resolve`);
  }
  const blocked = addresses.find((a) => !isPublicAddress(a));
  if (blocked) {
    throw new Error(`Host "${hostname}" resolves to a non-public address (${blocked})`);
  }
  return addresses;
}

/** Git versions before 2.37 silently ignore `http.curloptResolve`, which would undo the address pin. */
export const MIN_GIT_FOR_RESOLVE_PIN: [number, number] = [2, 37];

/** Throw unless `git --version` output names a git new enough to honour `http.curloptResolve`. */
export function assertGitSupportsResolvePin(versionOutput: string): void {
  const match = /^git version (\d+)\.(\d+)/.exec(versionOutput);
  const [minMajor, minMinor] = MIN_GIT_FOR_RESOLVE_PIN;
  if (!match) {
    throw new Error('Could not determine the git version; refusing to clone without an address pin');
  }
  const major = Number(match[1]);
  const minor = Number(match[2]);
  if (major < minMajor || (major === minMajor && minor < minMinor)) {
    throw new Error(
      `git ${major}.${minor} ignores http.curloptResolve; git ${minMajor}.${minMinor} or later is required to clone .git URLs`,
    );
  }
}

/**
 * Build a curl resolve entry for git's `http.curloptResolve`, so git connects only to addresses
 * that already passed the public-address check and cannot be sent elsewhere by DNS rebinding
 * between the check and the connection. IPv4 answers are preferred: an IPv6 entry makes curl
 * reject the whole option on builds or hosts without IPv6, so IPv6 is used (bracketed, as curl's
 * resolve syntax requires) only when the host has no IPv4 address.
 */
export function gitResolvePin(hostname: string, addresses: string[]): string {
  if (addresses.length === 0 || addresses.some((a) => !isPublicAddress(a))) {
    throw new Error(`Refusing to pin "${hostname}" to a non-public or empty address list`);
  }
  const ipv4 = addresses.filter((a) => net.isIPv4(a));
  const pinned = ipv4.length > 0 ? ipv4 : addresses.map((a) => `[${a}]`);
  return `${hostname}:443:${pinned.join(',')}`;
}

/**
 * Decompress a gzip file to `destPath`, aborting once the output passes `maxBytes`. The
 * decompressed tar's size bounds what `tar` can write, so a small archive cannot expand into
 * an unbounded amount of disk.
 */
export async function gunzipCapped(srcPath: string, destPath: string, maxBytes = 200 * 1024 * 1024): Promise<void> {
  let total = 0;
  const limiter = new Transform({
    transform(chunk: Buffer, _enc, cb) {
      total += chunk.length;
      if (total > maxBytes) {
        cb(new Error(`Archive expands to more than ${maxBytes} bytes`));
        return;
      }
      cb(null, chunk);
    },
  });
  try {
    await pipeline(fs.createReadStream(srcPath), zlib.createGunzip(), limiter, fs.createWriteStream(destPath, { mode: 0o600 }));
  } catch (err) {
    await fs.promises.rm(destPath, { force: true });
    throw err;
  }
}

/**
 * Validate a redirect destination. Unlike the user-supplied URL, signed download
 * URLs carry query strings, so only the scheme, credentials and port are checked
 * here; the host is checked by resolvePublicHost before connecting.
 */
export function checkRedirectTarget(target: string): string {
  const parsed = new URL(target);
  if (parsed.protocol !== 'https:') {
    throw new Error('Redirect target must use HTTPS');
  }
  if (parsed.username || parsed.password) {
    throw new Error('Redirect target must not contain credentials');
  }
  if (parsed.port && parsed.port !== '443') {
    throw new Error('Redirect target must use the default HTTPS port');
  }
  return parsed.toString();
}

export interface DownloadOptions {
  maxBytes?: number;
  timeoutMs?: number;
  maxRedirects?: number;
  resolver?: Resolver;
}

/**
 * Download an HTTPS URL to a file. The initial URL is validated with sanitiseUrl; each redirect
 * target is validated with checkRedirectTarget (HTTPS, no credentials, default port). Every hop's
 * host must resolve to public addresses, and the connection is pinned to the address that passed
 * that check, so DNS rebinding between check and connect is not possible.
 */
export async function downloadPublicHttps(url: string, destPath: string, opts: DownloadOptions = {}): Promise<void> {
  const maxBytes = opts.maxBytes ?? 50 * 1024 * 1024;
  const timeoutMs = opts.timeoutMs ?? 120_000;
  const maxRedirects = opts.maxRedirects ?? 5;
  const resolver = opts.resolver ?? defaultResolver;

  const deadline = Date.now() + timeoutMs;
  let current = sanitiseUrl(url);
  for (let hop = 0; hop <= maxRedirects; hop++) {
    const parsed = new URL(current);
    const [address] = await resolvePublicHost(parsed.hostname, resolver);
    const pinned: LookupFunction = (_host, options, callback) => {
      const family = net.isIPv6(address!) ? 6 : 4;
      if (typeof options === 'object' && options.all) {
        (callback as unknown as (err: null, addrs: Array<{ address: string; family: number }>) => void)(null, [
          { address: address!, family },
        ]);
      } else {
        callback(null, address!, family);
      }
    };

    const redirect = await new Promise<string | null>((resolve, reject) => {
      const req = https.get(parsed, { lookup: pinned, timeout: timeoutMs }, (res) => {
        const status = res.statusCode ?? 0;
        if (status >= 300 && status < 400 && res.headers.location) {
          res.resume();
          try {
            resolve(new URL(res.headers.location, parsed).toString());
          } catch {
            reject(new Error('Redirect has an invalid Location header'));
          }
          return;
        }
        if (status !== 200) {
          res.resume();
          reject(new Error(`Download failed with HTTP ${status}`));
          return;
        }
        const declared = Number(res.headers['content-length'] ?? 0);
        if (declared > maxBytes) {
          res.resume();
          reject(new Error('Download exceeds maximum size'));
          return;
        }
        let received = 0;
        const out = fs.createWriteStream(destPath, { mode: 0o600 });
        res.on('data', (chunk: Buffer) => {
          received += chunk.length;
          if (received > maxBytes) {
            res.destroy(new Error('Download exceeds maximum size'));
          }
        });
        res.on('error', (err) => {
          out.destroy();
          reject(err);
        });
        out.on('error', reject);
        out.on('finish', () => resolve(null));
        res.pipe(out);
      });
      const remaining = deadline - Date.now();
      const timer = setTimeout(() => req.destroy(new Error('Download timed out')), Math.max(remaining, 0));
      req.on('close', () => clearTimeout(timer));
      req.on('timeout', () => req.destroy(new Error('Download timed out')));
      req.on('error', reject);
    });

    if (redirect === null) return;
    current = checkRedirectTarget(redirect);
  }
  throw new Error('Too many redirects');
}

/**
 * Throw if the files under `dir` add up to more than `maxBytes` of logical size. A tar can hold
 * sparse members whose declared size is far larger than their stored bytes, and the scanner
 * reads every file in full, so the extracted tree is checked as well as the archive. Symlinks
 * are counted by their own size and never followed.
 */
export async function assertTreeWithinLimit(dir: string, maxBytes = 200 * 1024 * 1024): Promise<void> {
  let total = 0;
  const pending = [dir];
  while (pending.length > 0) {
    const current = pending.pop() as string;
    for (const entry of await fs.promises.readdir(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        pending.push(full);
        continue;
      }
      total += (await fs.promises.lstat(full)).size;
      if (total > maxBytes) {
        throw new Error(`Extracted skill is larger than ${maxBytes} bytes`);
      }
    }
  }
}
