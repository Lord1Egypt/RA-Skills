#!/usr/bin/env node
/**
 * Add a Solana wallet to a user's account
 * Usage: node add-wallet.js <telegram_user_id> <solana_address> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { findOrCreateUser, addWallet, getUserWallets } = require(path.join(sharedDir, 'services'));
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

if (typeof findOrCreateUser !== 'function' || typeof getUserWallets !== 'function' || typeof addWallet !== 'function') {
    console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
    process.exit(1);
}

try {
    const user = findOrCreateUser(telegramId, '');
    const wallets = getUserWallets(user.id);

    if (wallets.length >= 5) {
        console.log(`❌ ${formatError('MISSING_REQUIRED_PARAMS', lang)}: ${lang === 'zh' ? '最多支持 5 个钱包' : 'Maximum 5 wallets allowed'}`);
        process.exit(1);
    }

    const added = addWallet(user.id, address);
    if (added) {
        console.log(`✅ ${lang === 'zh' ? '钱包已添加' : 'Wallet added'}: ${address.slice(0, 6)}...${address.slice(-4)}`);
        console.log(`${lang === 'zh' ? '当前共' : 'Total'} ${wallets.length + 1} ${lang === 'zh' ? '个钱包' : 'wallets'}`);
        process.exit(0);
    }

    console.log(`⚠️ ${lang === 'zh' ? '该钱包已存在' : 'Wallet already exists'}`);
    process.exit(0);
} catch (err) {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
}
