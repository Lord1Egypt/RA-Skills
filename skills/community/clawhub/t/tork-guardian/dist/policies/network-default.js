"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_NETWORK_POLICY = void 0;
/**
 * Default network policy — balanced security for development and production.
 *
 * Inbound:  dev-server ranges (3000-3999, 8000-8999)
 * Outbound: HTTP/HTTPS/alt-HTTP (80, 443, 8080)
 * Blocks:   privileged ports, reverse shells, private-network SSRF
 */
exports.DEFAULT_NETWORK_POLICY = {
    networkPolicy: 'default',
    // Inbound: typical dev-server ranges
    allowedInboundPorts: expandRange(3000, 3999).concat(expandRange(8000, 8999)),
    // Outbound: standard web ports
    allowedOutboundPorts: [80, 443, 8080],
    // No domain restrictions in default policy
    allowedDomains: [],
    blockedDomains: [],
    // Rate limiting
    maxConnectionsPerMinute: 60,
    // Detection flags
    detectPortHijacking: true,
    detectReverseShells: true,
    blockPrivilegedPorts: true,
    blockPrivateNetworks: true,
    logAllActivity: true,
};
function expandRange(start, end) {
    const ports = [];
    for (let i = start; i <= end; i++) {
        ports.push(i);
    }
    return ports;
}
//# sourceMappingURL=network-default.js.map