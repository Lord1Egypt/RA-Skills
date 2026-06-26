#!/usr/bin/env node
/**
 * Get current price for a token
 * Usage: node get-price.js <token_symbol> [--lang en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { getTokenPrice } = require(path.join(sharedDir, 'price-service'));
const { formatPrice } = require(path.join(sharedDir, 'formatter'));
const { formatError } = require(path.join(sharedDir, 'errors'));

const symbol = (process.argv[2] || '').toUpperCase();
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';

if (!symbol) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing: ['代币符号 / Token symbol'],
        message: lang === 'zh'
            ? '我需要更多信息才能继续：代币符号'
            : 'I need more information to proceed: Token symbol'
    }, null, 2));
    process.exit(0);
}

async function main() {
    try {
        const price = await getTokenPrice(symbol);
        if (price > 0) {
            console.log(formatPrice(symbol, price, lang));
        } else {
            console.log(`⚠️ ${lang === 'zh' ? `未能获取 ${symbol} 价格` : `Could not fetch ${symbol} price`}`);
        }
    } catch (err) {
        console.log(`❌ ${formatError(err.code || 'INTERNAL_ERROR', lang)}`);
        process.exit(1);
    }
}

main();
