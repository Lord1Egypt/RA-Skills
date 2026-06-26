/**
 * Tests for gateway-url.ts — 3.3.1-rc.2 passive host autodetect.
 *
 * Covers:
 *   - detectTailscaleHost picks CGNAT IPv4 on tailscale* NIC
 *   - detectTailscaleHost ignores non-tailscale NICs
 *   - detectTailscaleHost ignores non-CGNAT IPv4 on tailscale* NIC
 *   - detectLanHost picks first physical IPv4, skips virtual NICs
 *   - detectGatewayHost prefers Tailscale over LAN when both present
 *   - detectGatewayHost falls through to null when nothing is available
 *   - No subprocess execution / no network I/O used (enforced by
 *     check-scanner.mjs child-process rule on this file + code-read)
 *
 * Run with: npx tsx gateway-url.test.ts
 */

import type os from 'node:os';
import { detectTailscaleHost, detectLanHost, detectGatewayHost, isDockerInternalIp } from './gateway-url.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function fakeNetifs(
  nifs: NodeJS.Dict<os.NetworkInterfaceInfo[]>,
): () => NodeJS.Dict<os.NetworkInterfaceInfo[]> {
  return () => nifs;
}

// Helper: build a NetworkInterfaceInfo record without pulling the real types.
function iface(addr: string, family: 'IPv4' | 'IPv6', internal = false): os.NetworkInterfaceInfo {
  return {
    address: addr,
    netmask: '255.255.255.0',
    family,
    mac: '00:00:00:00:00:00',
    internal,
    cidr: `${addr}/24`,
  } as os.NetworkInterfaceInfo;
}

// ---------------------------------------------------------------------------
// detectTailscaleHost
// ---------------------------------------------------------------------------

{
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      tailscale0: [iface('100.64.5.12', 'IPv4')],
    }),
  });
  assert(result !== null && result.kind === 'tailscale', 'tailscale: CGNAT IP on tailscale0 detected');
  assert(result?.host === '100.64.5.12', 'tailscale: host = CGNAT IPv4');
  assert(result?.tls === false, 'tailscale: tls=false (no MagicDNS, use gateway tls config)');
  assert(typeof result?.note === 'string' && result!.note!.includes('CGNAT'), 'tailscale: note mentions CGNAT');
}

{
  // tailscale NIC present but IP is NOT in CGNAT range
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      tailscale0: [iface('192.168.1.1', 'IPv4')],
    }),
  });
  assert(result === null, 'tailscale: non-CGNAT IP on tailscale0 ignored');
}

{
  // No tailscale NIC
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      eth0: [iface('192.168.1.10', 'IPv4')],
      en0: [iface('100.64.5.12', 'IPv4')], // CGNAT but wrong NIC
    }),
  });
  assert(result === null, 'tailscale: CGNAT on non-tailscale NIC ignored');
}

{
  // Upper boundary of CGNAT
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      tailscale1: [iface('100.127.255.254', 'IPv4')],
    }),
  });
  assert(result !== null && result.host === '100.127.255.254', 'tailscale: CGNAT upper boundary (100.127.x.x) accepted');
}

{
  // Just outside CGNAT
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      tailscale0: [iface('100.128.0.1', 'IPv4')],
    }),
  });
  assert(result === null, 'tailscale: IP just above CGNAT range rejected');
}

{
  // Internal tailscale IP (should be skipped)
  const result = detectTailscaleHost({
    networkInterfaces: fakeNetifs({
      tailscale0: [iface('100.64.5.12', 'IPv4', /* internal */ true)],
    }),
  });
  assert(result === null, 'tailscale: internal=true IP ignored');
}

// ---------------------------------------------------------------------------
// detectLanHost
// ---------------------------------------------------------------------------

{
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      eth0: [iface('192.168.1.10', 'IPv4')],
      docker0: [iface('172.17.0.1', 'IPv4')],
    }),
  });
  assert(result?.kind === 'lan', 'lan: detected kind=lan');
  assert(result?.host === '192.168.1.10', 'lan: picks eth0 over docker0 (virtual) and lo0 (loopback)');
}

{
  // Headless VPS with only lo + tailscale
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      tailscale0: [iface('100.64.5.12', 'IPv4')],
    }),
  });
  assert(result === null, 'lan: no physical NIC → null');
}

{
  // Skip all known virtual prefixes
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      'br-abc123': [iface('172.20.0.1', 'IPv4')],
      'veth0': [iface('10.0.0.1', 'IPv4')],
      'utun0': [iface('10.1.0.1', 'IPv4')],
      'tun0': [iface('10.2.0.1', 'IPv4')],
      'wg0': [iface('10.3.0.1', 'IPv4')],
    }),
  });
  assert(result === null, 'lan: all virtual-prefix NICs skipped');
}

// ---------------------------------------------------------------------------
// detectGatewayHost — composed
// ---------------------------------------------------------------------------

{
  // Tailscale wins over LAN
  const result = detectGatewayHost({
    networkInterfaces: fakeNetifs({
      eth0: [iface('192.168.1.10', 'IPv4')],
      tailscale0: [iface('100.64.5.12', 'IPv4')],
    }),
  });
  assert(result?.kind === 'tailscale', 'composed: tailscale preferred over LAN');
}

{
  // Only LAN available
  const result = detectGatewayHost({
    networkInterfaces: fakeNetifs({
      eth0: [iface('192.168.1.10', 'IPv4')],
    }),
  });
  assert(result?.kind === 'lan', 'composed: LAN fallback when tailscale absent');
}

{
  // Nothing available
  const result = detectGatewayHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
    }),
  });
  assert(result === null, 'composed: null when only loopback');
}

// ---------------------------------------------------------------------------
// Scanner-surface sanity check (meta-test): this file should NOT import
// child-process, fetch, or any outbound-request primitives. The scanner-sim
// check-scanner.mjs enforces this at pre-publish. We verify here that the
// module behaves sync (no Promise returns) so buildPairingUrl remains sync.
// ---------------------------------------------------------------------------

{
  const r = detectGatewayHost({
    networkInterfaces: fakeNetifs({}),
  });
  assert(r === null, 'meta: detectGatewayHost returns sync null on empty NIC table');
  // If detectGatewayHost returned a Promise, the assertion above would be
  // `Promise<null>` which is truthy — so `r === null` catches it.
}

// ---------------------------------------------------------------------------
// Issue #110 fix 4: Docker container internal IP detection
// ---------------------------------------------------------------------------

{
  // isDockerInternalIp — 172.16/12 range
  assert(isDockerInternalIp('172.17.0.1') === true, 'docker: 172.17.0.1 (default-bridge) recognized');
  assert(isDockerInternalIp('172.18.0.2') === true, 'docker: 172.18.0.2 (issue #110 user IP) recognized');
  assert(isDockerInternalIp('172.31.255.255') === true, 'docker: 172.31.255.255 (top of /12) recognized');
  assert(isDockerInternalIp('172.16.0.1') === true, 'docker: 172.16.0.1 (bottom of /12) recognized');
  assert(isDockerInternalIp('172.15.0.1') === false, 'docker: 172.15.x outside /12 not flagged');
  assert(isDockerInternalIp('172.32.0.1') === false, 'docker: 172.32.x outside /12 not flagged');
  assert(isDockerInternalIp('192.168.1.1') === false, 'docker: 192.168.x not flagged');
  assert(isDockerInternalIp('10.0.0.1') === false, 'docker: 10.x not flagged (rare for Docker default)');
  assert(isDockerInternalIp('not-an-ip') === false, 'docker: malformed input safe');
}

{
  // detectLanHost with isDocker=true skips 172.18.x
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      eth0: [iface('172.18.0.2', 'IPv4')], // Docker bridge IP — must be skipped
    }),
    isDocker: true,
  });
  assert(result === null, 'docker-aware LAN: 172.18.0.2 on eth0 skipped when isDocker=true (issue #110)');
}

{
  // detectLanHost with isDocker=false KEEPS 172.18.x (could be a real LAN)
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      eth0: [iface('172.18.0.2', 'IPv4')],
    }),
    isDocker: false,
  });
  assert(result !== null && result.host === '172.18.0.2', 'docker-aware LAN: 172.18.0.2 kept when isDocker=false (legitimate corporate LAN)');
}

{
  // detectLanHost with isDocker=true skips Docker IP but picks up a non-Docker LAN
  const result = detectLanHost({
    networkInterfaces: fakeNetifs({
      lo0: [iface('127.0.0.1', 'IPv4', true)],
      eth0: [iface('172.18.0.2', 'IPv4')], // Docker bridge — skip
      eth1: [iface('192.168.1.50', 'IPv4')], // real LAN — keep
    }),
    isDocker: true,
  });
  assert(result?.host === '192.168.1.50', 'docker-aware LAN: skips Docker IP, picks real LAN if present');
}

{
  // detectGatewayHost forwards isDocker to detectLanHost
  const result = detectGatewayHost({
    networkInterfaces: fakeNetifs({
      eth0: [iface('172.18.0.2', 'IPv4')],
    }),
    isDocker: true,
  });
  assert(result === null, 'composed: detectGatewayHost returns null in Docker when only Docker-internal IP found');
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
