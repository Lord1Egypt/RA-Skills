import { type ShieldClawCore, type HookFrameworkAPI } from '@shieldclaw/core';
/**
 * OpenClaw Hook 框架实现
 *
 * 这是 OpenClaw 需要实现的核心部分
 */
declare class OpenClawHookFramework implements HookFrameworkAPI {
    private rules;
    private core;
    constructor(core: ShieldClawCore);
    registerRule(rule: any): void;
    unregisterPlugin(pluginId: string): void;
    private initHooks;
    /**
     * 评估操作
     *
     * 由 OpenClaw 在拦截到系统调用时调用
     */
    evaluate(ctx: any): {
        action: 'allow' | 'block' | 'alert';
        rules: string[];
    };
}
/**
 * OpenClaw 应用集成示例
 */
declare class OpenClawApp {
    private shieldclawCore;
    private plugins;
    private hookFramework;
    initialize(): Promise<void>;
    private loadPlugins;
    /**
     * 注册命令（示例实现）
     */
    private registerCommand;
    /**
     * 显示通知（示例实现）
     */
    private showNotification;
    /**
     * 显示对话框（示例实现）
     */
    private showDialog;
    /**
     * 扫描 Skill（供 OpenClaw 调用）
     */
    scanSkill(skillPath: string): Promise<import("@shieldclaw/core").ScanReport>;
    /**
     * 关闭应用
     */
    shutdown(): Promise<void>;
}
export { OpenClawApp, OpenClawHookFramework };
export default OpenClawApp;
//# sourceMappingURL=index.d.ts.map