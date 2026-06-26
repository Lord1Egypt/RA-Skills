#!/usr/bin/env node
/**
 * Create a DCA strategy
 * Usage: node create-dca.js <telegram_user_id> <target_token> <amount_usdc> <schedule> [--lang zh|en]
 * schedule: daily | weekly | monthly | 6hours
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { createStrategy } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { resolveToken } = require(path.join(sharedDir, 'price-service'));

const telegramId = process.argv[2];
const targetToken = process.argv[3];
const amountRaw = process.argv[4];
const schedule = process.argv[5];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

function printMissingParams(missing) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`
    }, null, 2));
    process.exit(0);
}

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!targetToken) missing.push('目标代币 / Target token');
if (!amountRaw) missing.push('金额 / Amount');
if (!schedule) missing.push('频率 / Schedule');
if (missing.length > 0) {
    printMissingParams(missing);
}

const amount = Number.parseFloat(amountRaw);
if (!Number.isFinite(amount) || amount <= 0) {
    console.log(`❌ ${formatError('MISSING_REQUIRED_PARAMS', lang)}: ${lang === 'zh' ? '金额必须是大于 0 的数字' : 'Amount must be a number greater than 0'}`);
    process.exit(1);
}

const schedules = {
    daily: '0 9 * * *',
    weekly: '0 9 * * 1',
    monthly: '0 9 1 * *',
    '6hours': '0 */6 * * *',
};

const cron = schedules[schedule];
if (!cron) {
    console.log(`❌ ${formatError('MISSING_REQUIRED_PARAMS', lang)}: ${lang === 'zh' ? '无效频率（支持: daily, weekly, monthly, 6hours）' : 'Invalid schedule (supported: daily, weekly, monthly, 6hours)'}`);
    process.exit(1);
}

if (typeof createStrategy !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const symbol = targetToken.toUpperCase();
if (!resolveToken(symbol)) {
    console.log(`❌ ${formatError('UNKNOWN_TOKEN', lang)}`);
    process.exit(1);
}

const name = `DCA ${amount} USDC -> ${symbol}`;

const result = createStrategy(telegramId, {
    name,
    source_token: 'USDC',
    target_token: symbol,
    amount,
    cron_expression: cron,
});

if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

const scheduleNames = {
    daily: '每天 9:00 UTC / Daily 9:00 UTC',
    weekly: '每周一 9:00 UTC / Every Monday 9:00 UTC',
    monthly: '每月1日 9:00 UTC / Monthly 1st 9:00 UTC',
    '6hours': '每6小时 / Every 6 hours',
};

console.log(`🎉 ${lang === 'zh' ? 'DCA 策略已创建' : 'DCA strategy created'} / Strategy created!`);
console.log(`  ID: #${result.strategyId}`);
console.log(`  名称 / Name: ${name}`);
console.log(`  频率 / Schedule: ${scheduleNames[schedule]}`);
console.log('  状态 / Status: active');
