#!/usr/bin/env node
/**
 * Check token risk report using RugCheck
 * Usage: node check-token-risk.js <token_symbol_or_mint> [--lang en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { getTokenPrice, resolveToken } = require(path.join(sharedDir, 'price-service'));
const { formatUSD } = require(path.join(sharedDir, 'formatter'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const tokenInput = (process.argv[2] || '').trim();
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const isZh = lang !== 'en';

if (!tokenInput) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing: ['token_symbol'],
        message: isZh
            ? '我需要知道代币符号，才能查询风险报告。'
            : 'I need the token symbol to fetch its risk report.',
    }, null, 2));
    process.exit(0);
}

if (!resolveToken(tokenInput)) {
    console.log(`❌ ${formatError('UNKNOWN_TOKEN', lang)}`);
    process.exit(0);
}

function formatWarningLine(warning) {
    const level = String(warning.level || 'unknown').toUpperCase();
    const icon = warning.isCritical ? '🔴' : '🟡';
    return `${icon} [${level}] ${warning.message}`;
}

function formatHolderLine(holder, index) {
    const pct = Number.isFinite(holder.percentage) ? `${holder.percentage.toFixed(2)}%` : '--';
    return `${index + 1}. ${holder.address} (${pct})`;
}

async function main() {
    try {
        const data = await getTokenPrice(tokenInput, { includeRisk: true });
        const risk = data.risk;

        console.log(isZh ? '🛡️ 代币风险报告' : '🛡️ Token Risk Report');
        console.log(`${isZh ? '代币' : 'Token'}: ${data.symbol} (${data.mint})`);
        console.log(`${isZh ? '价格' : 'Price'}: ${formatUSD(data.price || 0)}`);

        if (!risk) {
            console.log(isZh ? '⚠️ 暂未获取到 RugCheck 风险数据' : '⚠️ RugCheck risk data is currently unavailable');
            return;
        }

        console.log(`${isZh ? '风险评分' : 'Risk Score'}: ${risk.score} ${data.riskLabel}`);
        console.log(`${isZh ? '高风险' : 'High Risk'}: ${data.highRisk ? (isZh ? '是' : 'Yes') : (isZh ? '否' : 'No')}`);

        const warnings = Array.isArray(risk.warnings) ? risk.warnings : [];
        if (warnings.length > 0) {
            console.log(`\n${isZh ? '风险警告' : 'Warnings'}:`);
            warnings.slice(0, 5).forEach((warning) => console.log(`  ${formatWarningLine(warning)}`));
        }

        const topHolders = Array.isArray(risk.topHolders) ? risk.topHolders : [];
        if (topHolders.length > 0) {
            console.log(`\n${isZh ? '前5大持仓' : 'Top 5 Holders'}:`);
            topHolders.slice(0, 5).forEach((holder, index) => console.log(`  ${formatHolderLine(holder, index)}`));
        }
    } catch (err) {
        console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }
}

main();
