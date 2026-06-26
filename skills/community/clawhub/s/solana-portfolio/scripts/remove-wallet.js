#!/usr/bin/env node
/**
 * Remove a wallet from a user's account
 * Usage: node remove-wallet.js <telegram_user_id> <solana_address> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { findOrCreateUser, removeWallet } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { isValidAddress } = require(path.join(sharedDir, 'wallet'));

const telegramId = process.argv[2];
const address = process.argv[3];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

const missing = [];
if (!telegramId) missing.push('用户ID / User ID');
if (!address) missing.push('钱包地址 / Wallet address');
if (missing.length > 0) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`
    }, null, 2));
    process.exit(0);
}

if (!isValidAddress(address)) {
    console.log(`❌ ${formatError('MISSING_REQUIRED_PARAMS', lang)}: ${lang === 'zh' ? '无效的 Solana 地址' : 'Invalid Solana address'}`);
    process.exit(1);
}

if (typeof findOrCreateUser !== 'function' || typeof removeWallet !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

try {
    const user = findOrCreateUser(telegramId, '');
    const removed = removeWallet(user.id, address);

    if (removed) {
        console.log(`✅ ${lang === 'zh' ? '钱包已移除' : 'Wallet removed'}: ${address.slice(0, 6)}...${address.slice(-4)}`);
        process.exit(0);
    }

    console.log(`⚠️ ${lang === 'zh' ? '钱包不存在' : 'Wallet not found'}`);
    process.exit(0);
} catch (err) {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
}
