// OpenClaw ShieldClaw 集成示例
import { app } from 'electron';
import path from 'path';
import { createCore, closeCore, } from '@shieldclaw/core';
import ScanPlugin from '@shieldclaw/scan';
import GuardPlugin from '@shieldclaw/guard';
import AuditPlugin from '@shieldclaw/audit';
import VaultPlugin from '@shieldclaw/vault';
/**
 * OpenClaw Hook 框架实现
 *
 * 这是 OpenClaw 需要实现的核心部分
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
        // 按优先级排序
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
        // TODO: 实现 fs/network/process 的 Hook
        this.core.logger.info('[HookFramework] Hooks initialized');
    }
    /**
     * 评估操作
     *
     * 由 OpenClaw 在拦截到系统调用时调用
     */
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
 * OpenClaw 应用集成示例
 */
class OpenClawApp {
    shieldclawCore = null;
    plugins = new Map();
    hookFramework = null;
    async initialize() {
        // 1. 创建 ShieldClaw Core
        const userDataPath = app.getPath('userData');
        this.shieldclawCore = createCore({
            dbPath: path.join(userDataPath, 'shieldclaw.db'),
            logDir: path.join(userDataPath, 'logs'),
            logLevel: 'info',
        });
        // 2. 初始化加密服务
        await this.shieldclawCore.crypto.initialize();
        // 3. 初始化 Hook 框架
        this.hookFramework = new OpenClawHookFramework(this.shieldclawCore);
        // 4. 加载插件
        await this.loadPlugins();
        this.shieldclawCore.logger.info('OpenClaw ShieldClaw integration initialized');
    }
    async loadPlugins() {
        if (!this.shieldclawCore || !this.hookFramework)
            return;
        const config = this.shieldclawCore.config.getAll();
        // 创建 PluginAPI
        const createPluginAPI = () => ({
            registerCommand: this.registerCommand.bind(this),
            on: this.shieldclawCore.eventBus.on.bind(this.shieldclawCore.eventBus),
            once: this.shieldclawCore.eventBus.once.bind(this.shieldclawCore.eventBus),
            off: this.shieldclawCore.eventBus.off.bind(this.shieldclawCore.eventBus),
            showNotification: this.showNotification.bind(this),
            showDialog: this.showDialog.bind(this),
            hookFramework: this.hookFramework,
        });
        // 加载 Scan 插件
        if (config.scan.enabled) {
            const scanPlugin = new ScanPlugin(this.shieldclawCore, createPluginAPI());
            await scanPlugin.activate();
            this.plugins.set('scan', scanPlugin);
        }
        // 加载 Guard 插件
        if (config.guard.enabled) {
            const guardPlugin = new GuardPlugin(this.shieldclawCore, createPluginAPI());
            await guardPlugin.activate();
            this.plugins.set('guard', guardPlugin);
        }
        // 加载 Audit 插件
        if (config.audit.enabled) {
            const auditPlugin = new AuditPlugin(this.shieldclawCore, createPluginAPI());
            await auditPlugin.activate();
            this.plugins.set('audit', auditPlugin);
        }
        // 加载 Vault 插件
        if (config.vault.enabled) {
            const vaultPlugin = new VaultPlugin(this.shieldclawCore, createPluginAPI());
            await vaultPlugin.activate();
            this.plugins.set('vault', vaultPlugin);
        }
    }
    /**
     * 注册命令（示例实现）
     */
    registerCommand(command, _handler) {
        console.log(`[OpenClaw] Command registered: ${command}`);
        // TODO: 实现命令注册逻辑
    }
    /**
     * 显示通知（示例实现）
     */
    async showNotification(options) {
        // Electron 通知 API
        // new Notification({ title: options.title, body: options.body }).show();
        console.log(`[Notification] ${options.title}: ${options.body}`);
    }
    /**
     * 显示对话框（示例实现）
     */
    async showDialog(options) {
        // Electron 对话框 API
        // return dialog.showMessageBox({ ... });
        console.log(`[Dialog] ${options.title}: ${options.message}`);
        return { response: 0 };
    }
    /**
     * 扫描 Skill（供 OpenClaw 调用）
     */
    async scanSkill(skillPath) {
        const { SkillScanner } = await import('@shieldclaw/scan');
        if (!this.shieldclawCore)
            throw new Error('ShieldClaw not initialized');
        const scanner = new SkillScanner(this.shieldclawCore);
        return scanner.scan(skillPath);
    }
    /**
     * 关闭应用
     */
    async shutdown() {
        // 停用所有插件
        for (const [, plugin] of this.plugins) {
            if (plugin.deactivate) {
                await plugin.deactivate();
            }
        }
        this.plugins.clear();
        // 关闭 ShieldClaw Core
        if (this.shieldclawCore) {
            await closeCore(this.shieldclawCore);
            this.shieldclawCore = null;
        }
    }
}
// 导出
export { OpenClawApp, OpenClawHookFramework };
export default OpenClawApp;
//# sourceMappingURL=index.js.map