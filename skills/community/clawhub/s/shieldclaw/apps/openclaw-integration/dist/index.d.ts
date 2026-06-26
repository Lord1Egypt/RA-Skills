import { type ShieldClawCore, type HookFrameworkAPI } from '@shieldclaw/core';
/**
 * OpenClaw Hook framework implementation
 */
declare class OpenClawHookFramework implements HookFrameworkAPI {
    private rules;
    private core;
    constructor(core: ShieldClawCore);
    registerRule(rule: any): void;
    unregisterPlugin(pluginId: string): void;
    private initHooks;
    evaluate(ctx: any): {
        action: 'allow' | 'block' | 'alert';
        rules: string[];
    };
}
/**
 * OpenClaw application integration example
 * Supports Electron and pure Node.js environments
 */
declare class OpenClawApp {
    private shieldclawCore;
    private plugins;
    private hookFramework;
    initialize(): Promise<void>;
    private loadPlugins;
    private registerCommand;
    private showNotification;
    private showDialog;
    scanSkill(skillPath: string): Promise<import("@shieldclaw/core").ScanReport>;
    shutdown(): Promise<void>;
}
export { OpenClawApp, OpenClawHookFramework };
export default OpenClawApp;
//# sourceMappingURL=index.d.ts.map