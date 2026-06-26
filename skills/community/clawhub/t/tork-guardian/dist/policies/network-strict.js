"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.STRICT_NETWORK_POLICY = void 0;
/**
 * Strict network policy — enterprise lockdown.
 *
 * Inbound:  only 3000-3010 (single dev-server range)
 * Outbound: 443 only (TLS required)
 * Domains:  explicit allowlist — nothing else gets through
 */
exports.STRICT_NETWORK_POLICY = {
    networkPolicy: 'strict',
    // Inbound: narrow dev-server range only
    allowedInboundPorts: [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010],
    // Outbound: TLS only
    allowedOutboundPorts: [443],
    // Explicit domain allowlist
    allowedDomains: [
        'api.openai.com',
        'api.anthropic.com',
        'tork.network',
        'tork.network',
        'api.tork.network',
        'registry.npmjs.org',
        'github.com',
        'api.github.com',
    ],
    blockedDomains: [],
    // Tight rate limiting
    maxConnectionsPerMinute: 20,
    // All detection enabled
    detectPortHijacking: true,
    detectReverseShells: true,
    blockPrivilegedPorts: true,
    blockPrivateNetworks: true,
    logAllActivity: true,
};
//# sourceMappingURL=network-strict.js.map