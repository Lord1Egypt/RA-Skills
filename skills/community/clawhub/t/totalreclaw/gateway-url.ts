/**
 * gateway-url — autodetect the gateway's externally-reachable URL for QR
 * pairing. This module runs sync + network-I/O-free so the OpenClaw
 * dangerous-code scanner never flags it (the 3.3.1-rc.1 implementation
 * used `child-process.execFileSync('tailscale', ...)` which blocked every
 * `openclaw plugins install` — see QA report
 * `docs/notes/QA-plugin-3.3.1-rc.1-20260422-0121.md`).
 *
 * Two layers:
 *
 *   1. Tailscale — PASSIVE detection via `os.networkInterfaces()`. If a
 *      `tailscale*` NIC has a CGNAT IPv4 (100.64/10), we return that IP
 *      as an auto-detected host — the operator can verify + override via
 *      `plugins.entries.totalreclaw.config.publicUrl` when they want a
 *      proper MagicDNS hostname. We DO NOT call `tailscale` the CLI —
 *      that requires `child-process` which the scanner blocks.
 *
 *   2. LAN — first non-loopback, non-virtual IPv4 interface. Emit with a
 *      caveat that the URL only works on the same network.
 *
 *   3. Null — no signal; caller falls through to localhost with a warning.
 *
 * The caller is expected to surface `detected.note` to the operator and
 * tell them to set `publicUrl` when auto-detect isn't good enough
 * (remote-accessible https, MagicDNS, etc.).
 *
 * Scope and scanner surface
 * -------------------------
 * - No `child-process` import — the original scanner-blocking flaw.
 * - No `fetch` / `post` / `http.request` substrings — the potential-
 *   exfiltration rule is also clear.
 * - Only `node:os` (synchronous, local) is used; no disk reads, no
 *   subprocess execution, no network calls.
 */

import os from 'node:os';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface DetectedGatewayHost {
  /** Kind of host detected — determines warning copy. */
  kind: 'tailscale' | 'lan';
  /** Host (no scheme, no port). */
  host: string;
  /** If true, assume TLS (https + port 443). */
  tls: boolean;
  /** Explanatory string the caller can surface to the operator. */
  note?: string;
}

// ---------------------------------------------------------------------------
// Tailscale — passive detection (no subprocess, no network I/O)
// ---------------------------------------------------------------------------

/** CGNAT range 100.64.0.0/10 — Tailscale assigns IPs here by default. */
function isTailscaleCGNAT(addr: string): boolean {
  if (!/^\d{1,3}(?:\.\d{1,3}){3}$/.test(addr)) return false;
  const parts = addr.split('.').map((p) => Number.parseInt(p, 10));
  if (parts[0] !== 100) return false;
  return parts[1] >= 64 && parts[1] <= 127;
}

/**
 * Passive Tailscale detection — checks `os.networkInterfaces()` for a
 * `tailscale*` NIC carrying a CGNAT IPv4. Returns null if not found.
 *
 * Unlike rc.1, this does NOT shell out to `tailscale status` — that
 * tripped the OpenClaw scanner's dangerous-code detector and blocked
 * install. The trade-off: we surface the raw CGNAT IP instead of the
 * MagicDNS hostname. Operators who want a MagicDNS host must set
 * `plugins.entries.totalreclaw.config.publicUrl` explicitly (documented
 * in SKILL.md).
 */
export function detectTailscaleHost(options?: {
  /** Override os.networkInterfaces for tests. */
  networkInterfaces?: () => NodeJS.Dict<os.NetworkInterfaceInfo[]>;
}): DetectedGatewayHost | null {
  const nif = (options?.networkInterfaces ?? os.networkInterfaces)();
  for (const [name, addrs] of Object.entries(nif)) {
    if (!name.toLowerCase().startsWith('tailscale')) continue;
    if (!addrs) continue;
    for (const a of addrs) {
      if (a.family !== 'IPv4' || a.internal) continue;
      if (isTailscaleCGNAT(a.address)) {
        return {
          kind: 'tailscale',
          host: a.address,
          tls: false,
          note:
            `Tailscale CGNAT IP detected on interface ${name}. For a proper ` +
            `https://<magicdns>.ts.net URL, set plugins.entries.totalreclaw.config.publicUrl ` +
            `(Tailscale CLI auto-resolution was removed in 3.3.1-rc.2 to pass the ` +
            `OpenClaw security scanner).`,
        };
      }
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// LAN autodetect
// ---------------------------------------------------------------------------

/** Interfaces we explicitly skip — these are virtual / tunneled. */
const SKIP_IFACE_PREFIXES = [
  'lo',
  'tailscale',
  'docker',
  'br-',
  'bridge',
  'veth',
  'utun',
  'vmnet',
  'ovpn',
  'wg',
  'virbr',
  'tun',
  'ham',
];

function shouldSkipIface(name: string): boolean {
  const lower = name.toLowerCase();
  return SKIP_IFACE_PREFIXES.some((p) => lower.startsWith(p));
}

/**
 * Docker container internal IP detection — issue #110 fix 4.
 *
 * From INSIDE a Docker container, `eth0` carries the container's bridge IP
 * (e.g. `172.18.0.2`). That IP is reachable from other containers on the
 * SAME Docker network but NOT from the host browser, the user's phone, or
 * any external device. Surfacing it as the pairing URL produces a hard-
 * dead user experience: "scan QR" yields connection-refused.
 *
 * Docker default-bridge ranges:
 *   - 172.17.0.0/16 — `bridge` (default)
 *   - 172.18.0.0/16 .. 172.31.0.0/16 — user-defined networks
 *
 * We use the conservative test: 172.16.0.0/12 (the full RFC-1918 172.x
 * range, which is what Docker draws from). If the host is clearly Docker
 * (`/.dockerenv`), we treat 172.16-31.x.x AS Docker-internal and skip it.
 *
 * Outside Docker, 172.16.x.x can be a legitimate corporate LAN, so we
 * only apply the rule when we have positive Docker evidence.
 */
export function isDockerInternalIp(addr: string): boolean {
  if (!/^\d{1,3}(?:\.\d{1,3}){3}$/.test(addr)) return false;
  const parts = addr.split('.').map((p) => Number.parseInt(p, 10));
  if (parts[0] !== 172) return false;
  return parts[1] >= 16 && parts[1] <= 31;
}

/**
 * Pick the first non-loopback, non-virtual IPv4 address. Returns null if
 * none found (headless VPS with only lo + tailscale, for example).
 *
 * issue #110 fix 4: when the host is detected as Docker (caller passes
 * `isDocker: true`), skip Docker-bridge IPs in the 172.16/12 range — they
 * are container-internal and useless for any external browser. Returning
 * null from this function in that scenario lets `buildPairingUrl` fall
 * through to the localhost-with-relay-fallback warning rather than handing
 * the user a dead URL.
 */
export function detectLanHost(options?: {
  /** Override os.networkInterfaces for tests. */
  networkInterfaces?: () => NodeJS.Dict<os.NetworkInterfaceInfo[]>;
  /** True when the host is Docker — skips 172.16/12 bridge IPs. */
  isDocker?: boolean;
}): DetectedGatewayHost | null {
  const nif = (options?.networkInterfaces ?? os.networkInterfaces)();
  for (const [name, addrs] of Object.entries(nif)) {
    if (shouldSkipIface(name)) continue;
    if (!addrs) continue;
    for (const a of addrs) {
      if (a.family !== 'IPv4' || a.internal) continue;
      // issue #110 fix 4 — Docker container internal IP is unreachable
      // from any external browser. Skip it so the caller falls back to
      // the relay-brokered URL.
      if (options?.isDocker && isDockerInternalIp(a.address)) continue;
      return {
        kind: 'lan',
        host: a.address,
        tls: false,
        note: `LAN IPv4 on interface ${name} — only reachable from the same network.`,
      };
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// Composed resolver
// ---------------------------------------------------------------------------

/**
 * Try Tailscale first (passive NIC probe), then LAN. Returns null when
 * neither is available (caller falls through to localhost).
 *
 * Sync: no I/O, no subprocess, no network. Safe in sync callers like
 * `buildPairingUrl` in index.ts.
 *
 * issue #110 fix 4: the `isDocker` option, when true, skips the 172.16/12
 * Docker-bridge range during LAN detection. The caller (index.ts) passes
 * `isRunningInDocker()` so we don't surface a container-internal IP that
 * no external browser can reach.
 */
export function detectGatewayHost(options?: {
  networkInterfaces?: () => NodeJS.Dict<os.NetworkInterfaceInfo[]>;
  isDocker?: boolean;
}): DetectedGatewayHost | null {
  const ts = detectTailscaleHost({ networkInterfaces: options?.networkInterfaces });
  if (ts) return ts;
  const lan = detectLanHost({
    networkInterfaces: options?.networkInterfaces,
    isDocker: options?.isDocker,
  });
  if (lan) return lan;
  return null;
}
