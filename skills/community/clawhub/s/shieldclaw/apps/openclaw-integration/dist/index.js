// OpenClaw ShieldClaw integration example
// Supports Electron desktop and pure Node.js CLI environments
import path from 'path';
import os from 'os';
import fs from 'fs';
import { createCore, closeCore, } from '@shieldclaw/core';
import ScanPlugin from '@shieldclaw/scan';
import GuardPlugin from '@shieldclaw/guard';
import AuditPlugin from '@shieldclaw/audit';
import VaultPlugin from '@shieldclaw/vault';
/**
 * Get user data directory
 * Compatible with Electron and pure Node.js environments
 */
function getUserDataPath() {
    // Check if in Electron environment
    const isElectron = process.versions.hasOwnProperty('electron');
    if (isElectron) {
        // Electron environment
        try {
            const { app } = require('electron');
            return app.getPath('userData');
        }
        catch {
            // If require fails, fall back to Node.js approach
        }
    }
    // Pure Node.js environment (Linux/Mac/Windows)
    const homeDir = os.homedir();
    const appName = 'shieldclaw';
    // Select appropriate data directory based on platform
    if (process.platform === 'win32') {
        return path.join(process.env.APPDATA || homeDir, appName);
    }
    else if (process.platform === 'darwin') {
        return path.join(homeDir, 'Library', 'Application Support', appName);
    }
    else {
        // Linux and other Unix systems
        return path.join(process.env.XDG_CONFIG_HOME || path.join(homeDir, '.config'), appName);
    }
}
/**
 * Ensure directory exists
 */
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
/**
 * OpenClaw Hook framework implementation
 */
class OpenClawHookFramework {
    rules = [];
    core;
    constructor(core) {
        this.core = core;
        this.initHooks();
    }
    registerRule(rule) {
        this.rules.push(rule);
        this.rules.sort((a, b) => b.priority - a.priority);
        this.core.logger.info(`[HookFramework] Rule registered: ${rule.id}`);
    }
    unregisterPlugin(pluginId) {
        const beforeCount = this.rules.length;
        this.rules = this.rules.filter(r => r.pluginId !== pluginId);
        const afterCount = this.rules.length;
        this.core.logger.info(`[HookFramework] Unregistered ${beforeCount - afterCount} rules from ${pluginId}`);
    }
    initHooks() {
        this.core.logger.info('[HookFramework] Hooks initialized');
    }
    evaluate(ctx) {
        const matchingRules = this.rules.filter(r => r.condition(ctx));
        if (matchingRules.some(r => r.action === 'block')) {
            return { action: 'block', rules: matchingRules.map(r => r.id) };
        }
        if (matchingRules.some(r => r.action === 'alert')) {
            return { action: 'alert', rules: matchingRules.map(r => r.id) };
        }
        return { action: 'allow', rules: [] };
    }
}
/**
 * OpenClaw application integration example
 * Supports Electron and pure Node.js environments
 */
class OpenClawApp {
    shieldclawCore = null;
    plugins = new Map();
    hookFramework = null;
    async initialize() {
        // 1. Get user data directory (compatible with Electron and Node.js)
        const userDataPath = getUserDataPath();
        ensureDir(userDataPath);
        // 2. Create ShieldClaw Core
        this.shieldclawCore = createCore({
            dbPath: path.join(userDataPath, 'shieldclaw.db'),
            logDir: path.join(userDataPath, 'logs'),
            logLevel: 'info',
        });
        // 3. Initialize encryption service
        await this.shieldclawCore.crypto.initialize();
        // 4. Initialize Hook framework
        this.hookFramework = new OpenClawHookFramework(this.shieldclawCore);
        // 5. Load plugins
        await this.loadPlugins();
        this.shieldclawCore.logger.info('OpenClaw ShieldClaw integration initialized');
        this.shieldclawCore.logger.info(`Data directory: ${userDataPath}`);
    }
    async loadPlugins() {
        if (!this.shieldclawCore || !this.hookFramework)
            return;
        const config = this.shieldclawCore.config.getAll();
        const createPluginAPI = () => ({
            registerCommand: this.registerCommand.bind(this),
            on: this.shieldclawCore.eventBus.on.bind(this.shieldclawCore.eventBus),
            once: this.shieldclawCore.eventBus.once.bind(this.shieldclawCore.eventBus),
            off: this.shieldclawCore.eventBus.off.bind(this.shieldclawCore.eventBus),
            showNotification: this.showNotification.bind(this),
            showDialog: this.showDialog.bind(this),
            hookFramework: this.hookFramework,
        });
        // Load Scan plugin
        if (config.scan.enabled) {
            const scanPlugin = new ScanPlugin(this.shieldclawCore, createPluginAPI());
            await scanPlugin.activate();
            this.plugins.set('scan', scanPlugin);
        }
        // Load Guard plugin
        if (config.guard.enabled) {
            const guardPlugin = new GuardPlugin(this.shieldclawCore, createPluginAPI());
            await guardPlugin.activate();
            this.plugins.set('guard', guardPlugin);
        }
        // Load Audit plugin
        if (config.audit.enabled) {
            const auditPlugin = new AuditPlugin(this.shieldclawCore, createPluginAPI());
            await auditPlugin.activate();
            this.plugins.set('audit', auditPlugin);
        }
        // Load Vault plugin
        if (config.vault.enabled) {
            const vaultPlugin = new VaultPlugin(this.shieldclawCore, createPluginAPI());
            await vaultPlugin.activate();
            this.plugins.set('vault', vaultPlugin);
        }
    }
    registerCommand(command, _handler) {
        console.log(`[OpenClaw] Command registered: ${command}`);
    }
    async showNotification(options) {
        console.log(`[Notification] ${options.title}: ${options.body}`);
    }
    async showDialog(options) {
        console.log(`[Dialog] ${options.title}: ${options.message}`);
        return { response: 0 };
    }
    async scanSkill(skillPath) {
        const { SkillScanner } = await import('@shieldclaw/scan');
        if (!this.shieldclawCore)
            throw new Error('ShieldClaw not initialized');
        const scanner = new SkillScanner(this.shieldclawCore);
        return scanner.scan(skillPath);
    }
    async shutdown() {
        for (const [, plugin] of this.plugins) {
            if (plugin.deactivate) {
                await plugin.deactivate();
            }
        }
        this.plugins.clear();
        if (this.shieldclawCore) {
            await closeCore(this.shieldclawCore);
            this.shieldclawCore = null;
        }
    }
}
export { OpenClawApp, OpenClawHookFramework };
export default OpenClawApp;
//# sourceMappingURL=index.js.map