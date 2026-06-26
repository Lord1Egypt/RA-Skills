#!/usr/bin/env node
/**
 * Delete a price alert
 * Usage: node delete-alert.js <telegram_user_id> <alert_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const services = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const deleteAlert = services.deleteAlert || services.deleteAlertForUser;

const telegramId = process.argv[2];
const alertIdRaw = process.argv[3];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!alertIdRaw) missing.push('警报ID / Alert ID');
if (missing.length > 0) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`
    }, null, 2));
    process.exit(0);
}

if (typeof deleteAlert !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const alertId = Number.parseInt(alertIdRaw, 10);
if (!Number.isInteger(alertId) || alertId <= 0) {
    console.log(`❌ ${formatError('INVALID_ALERT_ID', lang)}`);
    process.exit(1);
}

const result = deleteAlert(telegramId, alertId);
if (!result.ok) {
    if (result.code === 'ALERT_NOT_FOUND') {
        console.log(`⚠️ ${formatError(result.code, lang)}`);
        process.exit(0);
    }
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

console.log(`✅ ${formatError(result.code || 'ALERT_DELETED', lang)} / Alert #${alertId} deleted`);
