#!/usr/bin/env node
/**
 * List active price alerts for a user
 * Usage: node list-alerts.js <telegram_user_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { listAlerts } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { formatAlert } = require(path.join(sharedDir, 'formatter'));

const telegramId = process.argv[2];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

if (!telegramId) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing: ['用户ID / User ID'],
        message: '我需要更多信息才能继续：用户ID / User ID / I need more information to proceed: User ID'
    }, null, 2));
    process.exit(0);
}

if (typeof listAlerts !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const result = listAlerts(telegramId);
if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

const alerts = result.alerts || [];
if (alerts.length === 0) {
    console.log('📭 暂无价格警报 / No active alerts');
    process.exit(0);
}

console.log(`🔔 价格警报列表 / Price Alerts (${alerts.length}):\n`);
for (const alert of alerts) {
    console.log(formatAlert(alert, lang));
}
