import { type Message, type UsageReport } from '@token-saver/core';
interface PluginAPI {
    registerCommand: (command: string, handler: (args: string) => Promise<string>) => void;
    showNotification: (options: {
        title: string;
        body: string;
    }) => Promise<void>;
    getConversationContext: () => {
        messages: Message[];
        totalTokens: number;
    };
}
interface OpenClawCore {
    logger: {
        info: (msg: string, meta?: any) => void;
        warn: (msg: string, meta?: any) => void;
    };
}
export declare class TokenSaverPlugin {
    private saver;
    private api;
    private core;
    private isEnabled;
    constructor(core: OpenClawCore, api: PluginAPI);
    activate(): Promise<void>;
    deactivate(): Promise<void>;
    /**
     * Main optimization method - called before each AI request
     */
    optimizeContext(): {
        messages: Message[];
        report: UsageReport;
    };
    private showSavingsIndicator;
    private handleTokensCommand;
    private handleSaveCommand;
    private handleBalanceCommand;
    private handleQualityCommand;
    private handleReportCommand;
    private handleCacheCommand;
    private handleOffCommand;
}
export default TokenSaverPlugin;
//# sourceMappingURL=index.d.ts.map