"use strict";
/**
 * Network monitor — tracks port bindings, connection rates,
 * and shell activity for compliance and threat detection.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.NetworkMonitor = void 0;
const REVERSE_SHELL_PATTERNS = [
    /\bbash\s+-i\b.*[>&]\s*\/dev\/tcp\//,
    /\bnc\s+(-e|-c)\b/,
    /\bncat\s+(-e|-c)\b/,
    /\bsocat\b.*\bexec\b/,
    /\bpython[23]?\s+-c\b.*\bsocket\b/,
    /\bperl\s+-e\b.*\bsocket\b/,
    /\bruby\s+-rsocket\b/,
    /\bphp\s+-r\b.*\bfsockopen\b/,
    /\bpowershell\b.*\bNew-Object\b.*\bNet\.Sockets/,
    /\bmkfifo\b.*\bnc\b/,
    /\/dev\/tcp\/\d/,
];
class NetworkMonitor {
    constructor() {
        this.portRegistry = new Map();
        this.connections = [];
        this.shellCommands = [];
        this.startupPorts = new Set();
    }
    snapshotStartupPorts(ports) {
        this.startupPorts = new Set(ports);
    }
    getStartupPorts() {
        return this.startupPorts;
    }
    registerPort(port, protocol, skillId) {
        this.portRegistry.set(port, { port, protocol, skillId, boundAt: Date.now() });
    }
    unregisterPort(port) {
        this.portRegistry.delete(port);
    }
    getPortOwner(port) {
        return this.portRegistry.get(port);
    }
    getActivePorts() {
        return Array.from(this.portRegistry.values());
    }
    recordConnection(host, port, skillId) {
        this.connections.push({ host, port, skillId, timestamp: Date.now() });
        // Prune entries older than 5 minutes
        const cutoff = Date.now() - 5 * 60 * 1000;
        this.connections = this.connections.filter((c) => c.timestamp > cutoff);
    }
    getConnectionsPerMinute(skillId) {
        const oneMinuteAgo = Date.now() - 60 * 1000;
        return this.connections.filter((c) => c.timestamp > oneMinuteAgo && (!skillId || c.skillId === skillId)).length;
    }
    recordShellCommand(command, skillId) {
        this.shellCommands.push({ command, skillId, timestamp: Date.now() });
        // Prune entries older than 5 minutes
        const cutoff = Date.now() - 5 * 60 * 1000;
        this.shellCommands = this.shellCommands.filter((s) => s.timestamp > cutoff);
    }
    checkRecentShellActivity(skillId) {
        const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
        const recent = this.shellCommands.filter((s) => s.timestamp > fiveMinutesAgo && (!skillId || s.skillId === skillId));
        const matches = [];
        for (const record of recent) {
            for (const pattern of REVERSE_SHELL_PATTERNS) {
                if (pattern.test(record.command)) {
                    matches.push(record.command);
                    break;
                }
            }
        }
        return { suspicious: matches.length > 0, matches };
    }
    getNetworkReport() {
        const anomalies = [];
        // Check for ports opened after startup that weren't in the snapshot
        for (const binding of this.portRegistry.values()) {
            if (!this.startupPorts.has(binding.port)) {
                anomalies.push(`Port ${binding.port} opened after startup by skill "${binding.skillId}"`);
            }
        }
        // Check for high connection rates
        const rate = this.getConnectionsPerMinute();
        if (rate > 100) {
            anomalies.push(`High connection rate: ${rate}/min`);
        }
        // Check for reverse shell patterns
        const shellCheck = this.checkRecentShellActivity();
        if (shellCheck.suspicious) {
            anomalies.push(`Reverse shell patterns detected: ${shellCheck.matches.length} match(es)`);
        }
        const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
        return {
            timestamp: new Date().toISOString(),
            activePorts: this.getActivePorts(),
            recentConnections: this.connections.filter((c) => c.timestamp > fiveMinutesAgo),
            recentShellCommands: this.shellCommands.filter((s) => s.timestamp > fiveMinutesAgo),
            connectionRatePerMinute: rate,
            anomalies,
        };
    }
    reset() {
        this.portRegistry.clear();
        this.connections = [];
        this.shellCommands = [];
        this.startupPorts.clear();
    }
}
exports.NetworkMonitor = NetworkMonitor;
//# sourceMappingURL=network-monitor.js.map