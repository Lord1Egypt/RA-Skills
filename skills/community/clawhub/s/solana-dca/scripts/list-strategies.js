#!/usr/bin/env node
/**
 * List DCA strategies for a user
 * Usage: node list-strategies.js <telegram_user_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { listStrategies } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { formatStrategy } = require(path.join(sharedDir, 'formatter'));

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

if (typeof listStrategies !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

const result = listStrategies(telegramId);
if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

const strategies = result.strategies || [];
if (strategies.length === 0) {
    console.log('📭 暂无定投策略 / No strategies yet');
    process.exit(0);
}

console.log(`📋 定投策略列表 / DCA Strategies (${strategies.length}):\n`);
for (const strategy of strategies) {
    console.log(formatStrategy(strategy, lang));
    console.log('');
}
