#!/usr/bin/env node
/**
 * Get portfolio summary for a user
 * Usage: node get-portfolio.js <telegram_user_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { findOrCreateUser, getUserWallets } = require(path.join(sharedDir, 'services'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { getPortfolio } = require(path.join(sharedDir, 'tracker'));
const { formatPortfolioSummary } = require(path.join(sharedDir, 'formatter'));

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

async function main() {
    if (typeof findOrCreateUser !== 'function' || typeof getUserWallets !== 'function') {
        console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }

    const user = findOrCreateUser(telegramId, '');
    const wallets = getUserWallets(user.id);

    if (!wallets || wallets.length === 0) {
        console.log('📭 暂无钱包 / No wallets. Use add-wallet first.');
        process.exit(0);
    }

    const portfolio = await getPortfolio(user.id);
    console.log(formatPortfolioSummary(portfolio, lang));
}

main().catch((err) => {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
});
