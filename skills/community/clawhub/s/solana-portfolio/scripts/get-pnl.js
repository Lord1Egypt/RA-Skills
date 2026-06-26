#!/usr/bin/env node
/**
 * Get portfolio PnL summary for a user
 * Usage: node get-pnl.js <telegram_user_id> [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const {
    findOrCreateUser,
    getUserWallets,
    getPortfolioPnl,
} = require(path.join(sharedDir, 'services'));
const { getPortfolio } = require(path.join(sharedDir, 'tracker'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const telegramId = process.argv[2];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

if (!telegramId) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing: ['用户ID / User ID'],
        message: '我需要更多信息才能继续：用户ID / User ID / I need more information to proceed: User ID',
    }, null, 2));
    process.exit(0);
}

function formatAmount(value) {
    if (!Number.isFinite(value)) return '0';
    if (value >= 1) return value.toFixed(4).replace(/\.?0+$/, '');
    return value.toFixed(6).replace(/\.?0+$/, '');
}

function formatUsd(value) {
    const num = Number(value) || 0;
    return `$${Math.abs(num).toFixed(2)}`;
}

function formatSignedUsd(value) {
    const num = Number(value) || 0;
    if (num > 0) return `+${formatUsd(num)}`;
    if (num < 0) return `-${formatUsd(num)}`;
    return '$0.00';
}

function formatSignedPercent(value) {
    const num = Number(value) || 0;
    if (num > 0) return `+${num.toFixed(2)}%`;
    if (num < 0) return `${num.toFixed(2)}%`;
    return '0.00%';
}

async function main() {
    if (
        typeof findOrCreateUser !== 'function' ||
        typeof getUserWallets !== 'function' ||
        typeof getPortfolioPnl !== 'function'
    ) {
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
    if (!portfolio.holdings || portfolio.holdings.length === 0) {
        console.log('📭 暂无持仓 / No holdings yet.');
        process.exit(0);
    }

    const pnlRows = await getPortfolioPnl(user.id, portfolio.holdings);
    if (!pnlRows || pnlRows.length === 0) {
        console.log('📊 暂无盈亏数据 / No PnL data yet.');
        process.exit(0);
    }

    let totalUnrealized = 0;
    let totalRealized = 0;
    const lines = ['📊 盈亏统计 / PnL Summary', ''];

    for (const row of pnlRows) {
        const costBase = row.avgCost * row.amount;
        const pct = costBase > 0 ? (row.unrealizedPnl / costBase) * 100 : 0;
        totalUnrealized += row.unrealizedPnl;
        totalRealized += row.realizedPnl;

        lines.push(`${row.symbol}: ${formatAmount(row.amount)} tokens @ ${formatUsd(row.avgCost)} avg`);
        lines.push(`   未实现盈亏 / Unrealized: ${formatSignedUsd(row.unrealizedPnl)} (${formatSignedPercent(pct)})`);
        lines.push('');
    }

    lines.push(`总未实现盈亏 / Total Unrealized: ${formatSignedUsd(totalUnrealized)}`);
    lines.push(`总已实现盈亏 / Total Realized: ${formatSignedUsd(totalRealized)}`);
    console.log(lines.join('\n'));
}

main().catch((err) => {
    console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
    process.exit(1);
});
