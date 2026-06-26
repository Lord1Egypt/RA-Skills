#!/usr/bin/env node
/**
 * Check all active alerts against current prices
 * Usage: node check-prices.js [--system] [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { runAlertCheck } = require(path.join(sharedDir, 'scheduler'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

async function main() {
    // Security: verify this is a system-authorized call
    if (process.env.OPENCLAW_SYSTEM !== 'true' && !process.argv.includes('--system')) {
        console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}: ${lang === 'zh' ? '未授权的系统调用' : 'Unauthorized system call'}`);
        process.exit(1);
    }

    if (typeof runAlertCheck !== 'function') {
        console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }

    const summary = await runAlertCheck();
    if (!summary || summary.checked === 0) {
        console.log('📭 暂无活跃警报 / No active alerts');
        process.exit(0);
    }

    if (summary.triggered === 0) {
        console.log(`✅ ${lang === 'zh' ? '已检查，暂无触发警报' : 'Checked, no alerts triggered'}`);
        process.exit(0);
    }

    for (const item of summary.triggeredAlerts || []) {
        let condStr = item.condition === 'above' ? '高于 / above' : '低于 / below';
        if (item.alertType === 'stop_loss') condStr = '止损 / stop-loss';
        if (item.alertType === 'take_profit') condStr = '止盈 / take-profit';
        console.log(
            `🚨 TRIGGERED: ${item.symbol} ${condStr} ${item.targetPrice} (current: ${item.currentPrice})`
        );
    }

    console.log(
        `✅ ${lang === 'zh' ? `本次触发 ${summary.triggered} 条，已通知 ${summary.notified} 位用户` : `Triggered ${summary.triggered}, notified ${summary.notified} users`}`
    );
}

main().catch((err) => {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
});
