#!/usr/bin/env node
/**
 * Get smart rebalancing suggestions by comparing current allocation vs benchmark.
 * Usage: node get-rebalance-suggestion.js <telegram_user_id> [conservative|moderate|aggressive] [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { findOrCreateUser, getUserWallets, generateRebalanceSuggestion } = require(path.join(sharedDir, 'services'));
const { getPortfolio } = require(path.join(sharedDir, 'tracker'));
const { formatUSD } = require(path.join(sharedDir, 'formatter'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const telegramId = process.argv[2];
const benchmarkArg = process.argv[3];
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const isZh = lang !== 'en';

if (!telegramId) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing: ['用户ID / User ID'],
        message: '我需要更多信息才能继续：用户ID / User ID / I need more information to proceed: User ID',
    }, null, 2));
    process.exit(0);
}

function pct(value) {
    const parsed = Number(value) || 0;
    return `${parsed.toFixed(2)}%`;
}

function benchmarkLabel(value) {
    const normalized = String(value || '').toLowerCase();
    if (normalized === 'conservative') return isZh ? '保守型 / Conservative' : 'Conservative / 保守型';
    if (normalized === 'aggressive') return isZh ? '进取型 / Aggressive' : 'Aggressive / 进取型';
    return isZh ? '稳健型 / Moderate' : 'Moderate / 稳健型';
}

async function main() {
    try {
        if (typeof findOrCreateUser !== 'function'
            || typeof getUserWallets !== 'function'
            || typeof generateRebalanceSuggestion !== 'function') {
            console.log(`❌ ${formatError('INTERNAL_ERROR', lang)}`);
            process.exit(1);
        }

        const user = findOrCreateUser(telegramId, '');
        const wallets = getUserWallets(user.id);
        if (!wallets || wallets.length === 0) {
            console.log(isZh ? '📭 暂无钱包，无法生成再平衡建议。' : '📭 No wallets found. Unable to generate rebalancing suggestions.');
            process.exit(0);
        }

        const portfolio = await getPortfolio(user.id);
        if (!portfolio || portfolio.isEmpty || portfolio.totalValue <= 0) {
            console.log(isZh ? '📭 投资组合为空，无法生成再平衡建议。' : '📭 Portfolio is empty. Unable to generate rebalancing suggestions.');
            process.exit(0);
        }

        const profile = benchmarkArg || user.risk_profile || 'moderate';
        const result = generateRebalanceSuggestion(portfolio, {
            profile,
            rebalanceThresholdPct: 5,
        });

        const actionable = result.suggestions || [];
        console.log(isZh ? '⚖️ 智能再平衡建议（教育用途）' : '⚖️ Smart Rebalancing Suggestions (Educational)');
        console.log(`${isZh ? '组合总值' : 'Portfolio Value'}: ${formatUSD(portfolio.totalValue)}`);
        console.log(`${isZh ? '参考基准' : 'Benchmark'}: ${benchmarkLabel(profile)}`);
        console.log(`${isZh ? '偏离分数' : 'Divergence Score'}: ${pct(result.divergenceScore)}`);
        console.log(`${isZh ? '稳定币占比' : 'Stablecoin Share'}: ${pct(result.stablecoinShare)}`);
        console.log('');

        if (actionable.length === 0) {
            console.log(isZh ? '✅ 当前仓位与基准接近，暂无明显再平衡动作。' : '✅ Your allocation is close to benchmark. No major rebalance action.');
        } else {
            console.log(isZh ? '📌 关注项（偏离 >= 5%）:' : '📌 Focus areas (drift >= 5%):');
            for (const item of actionable) {
                const action = item.action === 'reduce'
                    ? (isZh ? '可考虑降低配置' : 'consider reducing exposure')
                    : (isZh ? '可考虑提高配置' : 'consider increasing exposure');
                console.log(
                    `- ${item.symbol}: ${action} | ${isZh ? '当前' : 'Current'} ${pct(item.currentPct)} / ${isZh ? '基准' : 'Target'} ${pct(item.targetPct)} | ${isZh ? '偏离' : 'Drift'} ${pct(item.driftPct)} | ${isZh ? '名义金额' : 'Notional'} ${formatUSD(item.notionalUsd)}`
                );
            }
        }

        console.log('');
        console.log(isZh
            ? '⚠️ 提示：以上仅为模型化对比结果，不构成投资建议。'
            : '⚠️ Note: This is a model-based comparison and not investment advice.');
    } catch (err) {
        console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }
}

main();
