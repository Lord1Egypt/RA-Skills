#!/usr/bin/env node
/**
 * Create a take-profit alert based on cost basis gain.
 * Usage: node create-take-profit.js <telegram_user_id> <token_symbol> <profit_percent> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { createTakeProfitAlertForUser } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const telegramId = process.argv[2];
const tokenSymbolRaw = process.argv[3];
const profitPercentRaw = process.argv[4];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const isZh = lang !== 'en';

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!tokenSymbolRaw) missing.push('代币符号 / Token symbol');
if (!profitPercentRaw) missing.push('止盈百分比 / Take-profit percent');

if (missing.length > 0) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`,
    }, null, 2));
    process.exit(0);
}

if (typeof createTakeProfitAlertForUser !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const tokenSymbol = tokenSymbolRaw.toUpperCase();
const profitPercent = Number.parseFloat(profitPercentRaw);
if (!Number.isFinite(profitPercent) || profitPercent <= 0 || profitPercent > 1000) {
    console.log(`❌ ${formatError('INVALID_ALERT_PERCENTAGE', lang)}: ${isZh ? '止盈百分比需大于 0 且不超过 1000' : 'Take-profit percent must be > 0 and <= 1000'}`);
    process.exit(1);
}

const result = createTakeProfitAlertForUser(telegramId, {
    tokenSymbol,
    profitPercent,
});

if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

console.log(`🎯 ${isZh ? '止盈提醒已创建' : 'Take-profit alert created'} / Alert created!`);
console.log(`  ID: #${result.alertId}`);
console.log(`  代币 / Token: ${tokenSymbol}`);
console.log(`  阈值 / Threshold: ${profitPercent.toFixed(2)}%`);
