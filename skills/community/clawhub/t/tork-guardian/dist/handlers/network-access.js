"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NetworkAccessHandler = void 0;
exports.validatePortBind = validatePortBind;
exports.validateEgress = validateEgress;
exports.validateDNS = validateDNS;
const network_monitor_1 = require("../utils/network-monitor");
const network_default_1 = require("../policies/network-default");
const network_strict_1 = require("../policies/network-strict");
/** Resolve the active network policy from TorkConfig. */
function resolvePolicy(config) {
    if (config.networkPolicy === 'strict')
        return network_strict_1.STRICT_NETWORK_POLICY;
    if (config.networkPolicy === 'default')
        return network_default_1.DEFAULT_NETWORK_POLICY;
    // 'custom' — merge user-supplied values over the default policy
    return {
        ...network_default_1.DEFAULT_NETWORK_POLICY,
        networkPolicy: 'custom',
        ...(config.allowedInboundPorts && { allowedInboundPorts: config.allowedInboundPorts }),
        ...(config.allowedOutboundPorts && { allowedOutboundPorts: config.allowedOutboundPorts }),
        ...(config.allowedDomains && { allowedDomains: config.allowedDomains }),
        ...(config.blockedDomains && { blockedDomains: config.blockedDomains }),
        ...(config.maxConnectionsPerMinute !== undefined && { maxConnectionsPerMinute: config.maxConnectionsPerMinute }),
    };
}
// Private-network CIDRs (for SSRF prevention)
const PRIVATE_NETWORK_PATTERNS = [
    /^127\./,
    /^10\./,
    /^172\.(1[6-9]|2\d|3[01])\./,
    /^192\.168\./,
    /^169\.254\./,
    /^0\./,
    /^::1$/,
    /^fc00:/i,
    /^fe80:/i,
    /^localhost$/i,
];
function isPrivateNetwork(host) {
    return PRIVATE_NETWORK_PATTERNS.some((p) => p.test(host));
}
function isRawIP(host) {
    return /^\d{1,3}(\.\d{1,3}){3}$/.test(host) || /^[0-9a-f:]+$/i.test(host);
}
class NetworkAccessHandler {
    constructor(config, client) {
        this.activityLog = [];
        this.policy = resolvePolicy(config);
        this.monitor = new network_monitor_1.NetworkMonitor();
        this.client = client ?? null;
    }
    getMonitor() {
        return this.monitor;
    }
    // ── Port binding governance ──────────────────────────────────
    validatePortBind(skillId, port, protocol = 'tcp') {
        // Block privileged ports
        if (this.policy.blockPrivilegedPorts && port < 1024) {
            return this.deny(skillId, 'port_bind', `Privileged port ${port} is blocked (< 1024)`);
        }
        // Check allowlist
        if (!this.policy.allowedInboundPorts.includes(port)) {
            return this.deny(skillId, 'port_bind', `Port ${port} is not in the inbound allowlist`);
        }
        // Port hijacking detection
        if (this.policy.detectPortHijacking) {
            const existing = this.monitor.getPortOwner(port);
            if (existing && existing.skillId !== skillId) {
                const msg = `Port hijacking detected: port ${port} is owned by skill "${existing.skillId}", attempted by "${skillId}"`;
                this.reportThreat(skillId, 'port_hijacking', msg);
                return this.deny(skillId, 'port_bind', msg);
            }
        }
        // Register the binding
        this.monitor.registerPort(port, protocol, skillId);
        return this.allow(skillId, 'port_bind', `Port ${port}/${protocol} bound`);
    }
    // ── Egress governance ────────────────────────────────────────
    validateEgress(skillId, host, port) {
        // SSRF prevention — block private networks
        if (this.policy.blockPrivateNetworks && isPrivateNetwork(host)) {
            return this.deny(skillId, 'egress', `Private network access blocked: ${host}`);
        }
        // Outbound port allowlist
        if (!this.policy.allowedOutboundPorts.includes(port)) {
            return this.deny(skillId, 'egress', `Outbound port ${port} is not allowed`);
        }
        // Domain blocklist
        if (this.policy.blockedDomains.length > 0) {
            const blocked = this.policy.blockedDomains.some((d) => host === d || host.endsWith(`.${d}`));
            if (blocked) {
                return this.deny(skillId, 'egress', `Domain "${host}" is blocked`);
            }
        }
        // Domain allowlist (only enforced when non-empty)
        if (this.policy.allowedDomains.length > 0) {
            const allowed = this.policy.allowedDomains.some((d) => host === d || host.endsWith(`.${d}`));
            if (!allowed) {
                return this.deny(skillId, 'egress', `Domain "${host}" is not in the allowlist`);
            }
        }
        // Reverse-shell detection: check recent shell activity
        if (this.policy.detectReverseShells) {
            const shellCheck = this.monitor.checkRecentShellActivity(skillId);
            if (shellCheck.suspicious) {
                const msg = `Reverse shell pattern detected for skill "${skillId}" during egress to ${host}:${port}`;
                this.reportThreat(skillId, 'reverse_shell', msg);
                return this.deny(skillId, 'egress', msg);
            }
        }
        // Rate limiting
        const currentRate = this.monitor.getConnectionsPerMinute(skillId);
        if (currentRate >= this.policy.maxConnectionsPerMinute) {
            return this.deny(skillId, 'egress', `Rate limit exceeded: ${currentRate}/${this.policy.maxConnectionsPerMinute} connections/min`);
        }
        // Record the connection
        this.monitor.recordConnection(host, port, skillId);
        return this.allow(skillId, 'egress', `Egress to ${host}:${port} allowed`);
    }
    // ── DNS governance ───────────────────────────────────────────
    validateDNS(skillId, hostname) {
        // Flag raw IP usage
        if (isRawIP(hostname)) {
            const decision = this.deny(skillId, 'dns', `Raw IP address "${hostname}" used instead of hostname — potential SSRF or C2 channel`);
            this.reportThreat(skillId, 'raw_ip_usage', decision.reason);
            return decision;
        }
        // Domain blocklist
        if (this.policy.blockedDomains.length > 0) {
            const blocked = this.policy.blockedDomains.some((d) => hostname === d || hostname.endsWith(`.${d}`));
            if (blocked) {
                return this.deny(skillId, 'dns', `DNS lookup for blocked domain: ${hostname}`);
            }
        }
        // Domain allowlist
        if (this.policy.allowedDomains.length > 0) {
            const allowed = this.policy.allowedDomains.some((d) => hostname === d || hostname.endsWith(`.${d}`));
            if (!allowed) {
                return this.deny(skillId, 'dns', `DNS lookup for domain not in allowlist: ${hostname}`);
            }
        }
        return this.allow(skillId, 'dns', `DNS lookup for ${hostname} allowed`);
    }
    // ── Activity log & reporting ─────────────────────────────────
    getActivityLog() {
        return this.activityLog;
    }
    clearActivityLog() {
        this.activityLog = [];
    }
    // ── Private helpers ──────────────────────────────────────────
    allow(skillId, action, reason) {
        const entry = {
            timestamp: new Date().toISOString(),
            skillId,
            action,
            allowed: true,
            reason,
        };
        if (this.policy.logAllActivity) {
            this.activityLog.push(entry);
        }
        return { allowed: true, reason };
    }
    deny(skillId, action, reason) {
        const entry = {
            timestamp: new Date().toISOString(),
            skillId,
            action,
            allowed: false,
            reason,
        };
        this.activityLog.push(entry); // always log denials
        return { allowed: false, reason };
    }
    reportThreat(skillId, type, detail) {
        if (!this.client)
            return;
        // Fire-and-forget threat report to Tork Cloud
        this.client
            .govern(`[THREAT] skill=${skillId} type=${type} detail=${detail}`)
            .catch(() => {
            /* best-effort */
        });
    }
}
exports.NetworkAccessHandler = NetworkAccessHandler;
// ── Standalone convenience functions ─────────────────────────────
function validatePortBind(config, skillId, port, protocol = 'tcp') {
    const handler = new NetworkAccessHandler(config);
    return handler.validatePortBind(skillId, port, protocol);
}
function validateEgress(config, skillId, host, port) {
    const handler = new NetworkAccessHandler(config);
    return handler.validateEgress(skillId, host, port);
}
function validateDNS(config, skillId, hostname) {
    const handler = new NetworkAccessHandler(config);
    return handler.validateDNS(skillId, hostname);
}
//# sourceMappingURL=network-access.js.map