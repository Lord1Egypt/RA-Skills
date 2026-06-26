#!/usr/bin/env node
/**
 * Pause a DCA strategy
 * Usage: node pause-strategy.js <telegram_user_id> <strategy_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');
const { pauseStrategy } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const telegramId = process.argv[2];
const strategyId = process.argv[3];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

// Parameter validation with MISSING_PARAMS protocol
if (!telegramId || !strategyId) {
    const missing = [];
    if (!telegramId) missing.push(lang === 'zh' ? '用户ID' : 'User ID');
    if (!strategyId) missing.push(lang === 'zh' ? '策略ID' : 'Strategy ID');

    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: lang === 'zh'
            ? `我需要更多信息才能继续：${missing.join('、')}`
            : `I need more information to proceed: ${missing.join(', ')}`
    }, null, 2));
    process.exit(0);
}

const result = pauseStrategy(telegramId, strategyId);

// Handle already paused (warning, not error)
if (result.code === 'STRATEGY_ALREADY_PAUSED') {
    console.log(`⚠️ ${formatError(result.code, lang)}`);
    process.exit(0);
}

// Handle actual errors
if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

// Success
console.log(`🟡 ${formatError('OK', lang).replace('操作成功', `策略 #${result.strategyId} 已暂停`)} / Strategy #${result.strategyId} paused`);
