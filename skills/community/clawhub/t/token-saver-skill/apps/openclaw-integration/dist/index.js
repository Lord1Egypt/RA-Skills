// TokenSaver OpenClaw Integration
// Provides /tokens commands and automatic optimization
import { TokenSaver } from '@token-saver/core';
export class TokenSaverPlugin {
    saver;
    api;
    core;
    isEnabled = true;
    constructor(core, api) {
        this.core = core;
        this.api = api;
        this.saver = new TokenSaver({
            enabled: true,
            showIndicator: true,
            defaultMode: 'adaptive'
        });
    }
    async activate() {
        // Register commands
        this.api.registerCommand('/tokens', this.handleTokensCommand.bind(this));
        this.api.registerCommand('/tokensave', this.handleSaveCommand.bind(this));
        this.api.registerCommand('/tokenbalance', this.handleBalanceCommand.bind(this));
        this.api.registerCommand('/tokenquality', this.handleQualityCommand.bind(this));
        this.api.registerCommand('/tokenreport', this.handleReportCommand.bind(this));
        this.api.registerCommand('/tokencache', this.handleCacheCommand.bind(this));
        this.api.registerCommand('/tokenoff', this.handleOffCommand.bind(this));
        this.core.logger.info('[TokenSaver] Plugin activated');
        // Show welcome message with current savings
        const stats = this.saver.getSessionStats();
        await this.api.showNotification({
            title: 'TokenSaver Active',
            body: `Adaptive optimization enabled. Current savings: ${stats.savings}`
        });
    }
    async deactivate() {
        this.core.logger.info('[TokenSaver] Plugin deactivated');
    }
    /**
     * Main optimization method - called before each AI request
     */
    optimizeContext() {
        if (!this.isEnabled) {
            const context = this.api.getConversationContext();
            return {
                messages: context.messages,
                report: {
                    originalTokens: context.totalTokens,
                    optimizedTokens: context.totalTokens,
                    actualTokens: context.totalTokens,
                    cacheHits: 0,
                    compressionRatio: 0,
                    estimatedSavings: '$0.00',
                    qualityScore: 100
                }
            };
        }
        const context = this.api.getConversationContext();
        const result = this.saver.optimize(context);
        // Show savings indicator
        if (result.report.compressionRatio > 0) {
            this.showSavingsIndicator(result.report);
        }
        return result;
    }
    async showSavingsIndicator(report) {
        const icon = report.compressionRatio > 50 ? '🔥' : '💰';
        await this.api.showNotification({
            title: `${icon} TokenSaver`,
            body: `Saved ${report.compressionRatio}% (${report.estimatedSavings}) • Quality: ${report.qualityScore}%`
        });
    }
    // Command Handlers
    async handleTokensCommand(args) {
        const stats = this.saver.getSessionStats();
        const cacheStats = this.saver.getCacheStats();
        return `
📊 TokenSaver Status
━━━━━━━━━━━━━━━━━━━━
Session Savings: ${stats.savings}
Original Tokens: ${stats.originalTokens.toLocaleString()}
Optimized Tokens: ${stats.optimizedTokens.toLocaleString()}
Cache Hits: ${stats.cacheHits}
Compressions: ${stats.compressionCount}

Cache Status:
• L1 (Exact): ${cacheStats.l1Size} entries
• L2 (Semantic): ${cacheStats.l2Size} entries  
• L3 (Pattern): ${cacheStats.l3Size} entries
• Total Hits: ${cacheStats.totalHits}

Commands:
/tokensave    - Aggressive mode
/tokenbalance - Balanced mode (default)
/tokenquality - Quality priority
/tokenreport  - Detailed report
/tokencache   - Clear cache
/tokenoff     - Disable
    `.trim();
    }
    async handleSaveCommand() {
        this.saver.updateConfig({
            adaptiveMode: {
                thresholds: {
                    stage1: { tokenLimit: 2000, compression: 'none' },
                    stage2: { tokenLimit: 4000, compression: 'light' },
                    stage3: { tokenLimit: 6000, compression: 'medium' },
                    stage4: { tokenLimit: 8000, compression: 'heavy' }
                }
            }
        });
        await this.api.showNotification({
            title: 'TokenSaver',
            body: 'Switched to aggressive save mode'
        });
        return '✅ Aggressive save mode enabled. Maximum token savings.';
    }
    async handleBalanceCommand() {
        this.saver.updateConfig({
            adaptiveMode: {
                thresholds: {
                    stage1: { tokenLimit: 3000, compression: 'none' },
                    stage2: { tokenLimit: 6000, compression: 'light' },
                    stage3: { tokenLimit: 10000, compression: 'medium' },
                    stage4: { tokenLimit: 15000, compression: 'heavy' }
                }
            }
        });
        await this.api.showNotification({
            title: 'TokenSaver',
            body: 'Switched to balanced mode'
        });
        return '✅ Balanced mode enabled. Good savings with quality preserved.';
    }
    async handleQualityCommand() {
        this.saver.updateConfig({
            adaptiveMode: {
                thresholds: {
                    stage1: { tokenLimit: 5000, compression: 'none' },
                    stage2: { tokenLimit: 10000, compression: 'light' },
                    stage3: { tokenLimit: 20000, compression: 'medium' },
                    stage4: { tokenLimit: 30000, compression: 'heavy' }
                }
            },
            compression: {
                neverCompress: ['code', 'error-logs', 'user-marked-important'],
                alwaysKeep: 10,
                summaryStrategy: 'semantic',
                qualityThreshold: 0.95
            }
        });
        await this.api.showNotification({
            title: 'TokenSaver',
            body: 'Switched to quality priority mode'
        });
        return '✅ Quality priority mode. Minimal compression, maximum context retention.';
    }
    async handleReportCommand() {
        const stats = this.saver.getSessionStats();
        return `
📈 TokenSaver Detailed Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Session:
• Total Original Tokens: ${stats.originalTokens.toLocaleString()}
• Total Optimized Tokens: ${stats.optimizedTokens.toLocaleString()}
• Overall Savings: ${stats.savings}
• Cache Hits: ${stats.cacheHits}
• Compressions Applied: ${stats.compressionCount}

Estimates (GPT-4 pricing):
• Tokens Saved: ${(stats.originalTokens - stats.optimizedTokens).toLocaleString()}
• Estimated Cost Saved: ~$${((stats.originalTokens - stats.optimizedTokens) / 1000 * 0.002).toFixed(4)}

Optimization Tips:
• Use /tokensave for long technical discussions
• Use /tokenquality when context is critical
• TokenSaver auto-suggests new chat when topics change
    `.trim();
    }
    async handleCacheCommand(args) {
        if (args.trim() === 'clear') {
            this.saver.clearCache();
            return '✅ Cache cleared.';
        }
        const stats = this.saver.getCacheStats();
        return `
💾 TokenSaver Cache
━━━━━━━━━━━━━━━━━━━━
L1 (Exact Match): ${stats.l1Size} entries
L2 (Semantic): ${stats.l2Size} entries
L3 (Pattern): ${stats.l3Size} entries
Total Hits: ${stats.totalHits}

Use "/tokencache clear" to clear all caches.
    `.trim();
    }
    async handleOffCommand() {
        this.isEnabled = false;
        await this.api.showNotification({
            title: 'TokenSaver',
            body: 'Optimization disabled for this session'
        });
        return '⏸️ TokenSaver disabled. Re-enable with "/tokens" to see options.';
    }
}
export default TokenSaverPlugin;
//# sourceMappingURL=index.js.map