#!/usr/bin/env node
/**
 * Resume a paused DCA strategy
 * Usage: node resume-strategy.js <telegram_user_id> <strategy_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');
const { resumeStrategy } = require(path.join(sharedDir, 'services'));
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

const result = resumeStrategy(telegramId, strategyId);

// Handle already active (warning, not error)
if (result.code === 'STRATEGY_ALREADY_ACTIVE') {
    console.log(`⚠️ ${formatError(result.code, lang)}`);
    process.exit(0);
}

// Handle actual errors
if (!result.ok) {
    console.log(`❌ ${formatError(result.code, lang)}`);
    process.exit(1);
}

// Success
console.log(`🟢 ${formatError('OK', lang).replace('操作成功', `策略 #${result.strategyId} 已恢复`)} / Strategy #${result.strategyId} resumed`);
