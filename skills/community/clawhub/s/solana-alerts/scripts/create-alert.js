#!/usr/bin/env node
/**
 * Create a price alert
 * Usage: node create-alert.js <telegram_user_id> <token_symbol> <condition> <target_price> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const services = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { formatUSD } = require(path.join(sharedDir, 'formatter'));

const createAlert = services.createAlert || services.createAlertForUser;

const telegramId = process.argv[2];
const tokenSymbolRaw = process.argv[3];
const condition = process.argv[4];
const targetPriceRaw = process.argv[5];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!tokenSymbolRaw) missing.push('代币符号 / Token symbol');
if (!condition) missing.push('条件 / Condition');
if (!targetPriceRaw) missing.push('目标价格 / Target price');
if (missing.length > 0) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`
    }, null, 2));
    process.exit(0);
}

if (typeof createAlert !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const tokenSymbol = tokenSymbolRaw.toUpperCase();
const result = createAlert(telegramId, {
    tokenSymbol,
    condition,
    targetPrice: targetPriceRaw,
});

if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

const targetPrice = Number.parseFloat(targetPriceRaw);
const condStr = condition === 'above' ? '高于 / above' : '低于 / below';

console.log(`🔔 ${formatError(result.code || 'ALERT_CREATED', lang)} / Alert created!`);
console.log(`  ID: #${result.alertId}`);
console.log(`  代币 / Token: ${tokenSymbol}`);
console.log(`  条件 / Condition: ${condStr} ${formatUSD(targetPrice)}`);
