#!/usr/bin/env node
/**
 * List all wallets for a user
 * Usage: node list-wallets.js <telegram_user_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { findOrCreateUser, getUserWallets } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));

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

if (typeof findOrCreateUser !== 'function' || typeof getUserWallets !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

try {
    const user = findOrCreateUser(telegramId, '');
    const wallets = getUserWallets(user.id);

    if (wallets.length === 0) {
        console.log('📭 暂无钱包 / No wallets');
        process.exit(0);
    }

    console.log(`👛 钱包列表 / Wallets (${wallets.length}):\n`);
    wallets.forEach((wallet, index) => {
        const shortAddress = `${wallet.address.slice(0, 6)}...${wallet.address.slice(-4)}`;
        console.log(`${index + 1}. ${shortAddress}${wallet.label ? ` (${wallet.label})` : ''}`);
    });
} catch (err) {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
}
