#!/usr/bin/env node
/**
 * Create a stop-loss alert based on cost basis drawdown.
 * Usage: node create-stop-loss.js <telegram_user_id> <token_symbol> <loss_percent> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { createStopLossAlertForUser } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const telegramId = process.argv[2];
const tokenSymbolRaw = process.argv[3];
const lossPercentRaw = process.argv[4];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const isZh = lang !== 'en';

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!tokenSymbolRaw) missing.push('代币符号 / Token symbol');
if (!lossPercentRaw) missing.push('止损百分比 / Stop-loss percent');

if (missing.length > 0) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`,
    }, null, 2));
    process.exit(0);
}

if (typeof createStopLossAlertForUser !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const tokenSymbol = tokenSymbolRaw.toUpperCase();
const lossPercent = Number.parseFloat(lossPercentRaw);
if (!Number.isFinite(lossPercent) || lossPercent <= 0 || lossPercent >= 100) {
    console.log(`❌ ${formatError('INVALID_ALERT_PERCENTAGE', lang)}: ${isZh ? '止损百分比需在 0-100 之间' : 'Stop-loss percent must be between 0 and 100'}`);
    process.exit(1);
}

const result = createStopLossAlertForUser(telegramId, {
    tokenSymbol,
    lossPercent,
});

if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

console.log(`🛑 ${isZh ? '止损提醒已创建' : 'Stop-loss alert created'} / Alert created!`);
console.log(`  ID: #${result.alertId}`);
console.log(`  代币 / Token: ${tokenSymbol}`);
console.log(`  阈值 / Threshold: ${lossPercent.toFixed(2)}%`);
