#!/usr/bin/env node
/**
 * Track large transfers for a specific wallet via Helius.
 * Usage:
 *   node track-whale.js <wallet_address> <min_usd_value> [--lang zh|en]
 *   node track-whale.js <wallet_address> <min_usd_value> --watch [--interval 30] [--lang zh|en]
 */
const path = require('path');
const sharedDir = path.resolve(__dirname, '..', '..', '..', 'shared');

const { scanWhaleTransfers, createWhaleTracker } = require(path.join(sharedDir, 'services'));
const { formatUSD } = require(path.join(sharedDir, 'formatter'));
const { formatError } = require(path.join(sharedDir, 'errors'));
const { isValidAddress } = require(path.join(sharedDir, 'wallet'));
const config = require(path.join(sharedDir, 'config'));

const walletAddress = process.argv[2];
const minUsdRaw = process.argv[3];
const watchMode = process.argv.includes('--watch');
const lang = process.argv.includes('--lang') ? process.argv[process.argv.indexOf('--lang') + 1] : 'zh';
const intervalIndex = process.argv.indexOf('--interval');
const intervalSec = intervalIndex > -1 ? Number.parseInt(process.argv[intervalIndex + 1], 10) : 30;
const isZh = lang !== 'en';

function printMissing(missing) {
    console.log(JSON.stringify({
        code: 'MISSING_PARAMS',
        missing,
        message: `我需要更多信息才能继续：${missing.join('、')} / I need more information to proceed: ${missing.join(', ')}`,
    }, null, 2));
}

function formatEventLine(event) {
    const direction = event.direction === 'in'
        ? (isZh ? '流入' : 'IN')
        : event.direction === 'out'
            ? (isZh ? '流出' : 'OUT')
            : (isZh ? '未知方向' : 'UNKNOWN');
    return `🐋 ${event.symbol} ${direction} ${event.amount.toFixed(4)} | ${formatUSD(event.usdValue)} | ${event.signature}`;
}

async function runOnce(address, minUsdValue) {
    const result = await scanWhaleTransfers({
        address,
        minUsdValue,
        limit: 30,
    });

    if (!result.events || result.events.length === 0) {
        console.log(isZh
            ? `✅ 最近 ${result.checked} 笔交易中未发现超过 ${formatUSD(minUsdValue)} 的大额转账。`
            : `✅ No whale transfers above ${formatUSD(minUsdValue)} found in the latest ${result.checked} transactions.`);
        return;
    }

    console.log(isZh ? '🐋 鲸鱼转账扫描结果:' : '🐋 Whale transfer scan:');
    for (const event of result.events) {
        console.log(formatEventLine(event));
    }
}

async function runWatch(address, minUsdValue) {
    const pollMs = Math.max(10, Number.isFinite(intervalSec) ? intervalSec : 30) * 1000;
    const tracker = createWhaleTracker({
        address,
        minUsdValue,
        pollIntervalMs: pollMs,
        onEvent: (event) => {
            console.log(formatEventLine(event));
        },
        onError: () => {
            console.log(`⚠️ ${isZh ? '鲸鱼监听暂时失败，系统将继续重试。' : 'Whale tracking temporarily failed, retrying automatically.'}`);
        },
    });

    await tracker.start();
    console.log(isZh
        ? `👀 已开启实时监听，阈值 ${formatUSD(minUsdValue)}，轮询间隔 ${pollMs / 1000}s（Ctrl+C 停止）`
        : `👀 Live whale tracking started with threshold ${formatUSD(minUsdValue)} and ${pollMs / 1000}s polling (Ctrl+C to stop)`);

    process.on('SIGINT', () => {
        tracker.stop();
        console.log(isZh ? '\n🛑 已停止鲸鱼监听。' : '\n🛑 Whale tracking stopped.');
        process.exit(0);
    });
}

async function main() {
    const missing = [];
    if (!walletAddress) missing.push('钱包地址 / Wallet address');
    if (!minUsdRaw) missing.push('金额阈值(USD) / USD threshold');
    if (missing.length > 0) {
        printMissing(missing);
        process.exit(0);
    }

    if (!config.heliusApiKey) {
        console.log(`❌ ${isZh ? '未配置 HELIUS_API_KEY，无法启用鲸鱼追踪。' : 'HELIUS_API_KEY is not configured. Whale tracking is unavailable.'}`);
        process.exit(1);
    }

    if (!isValidAddress(walletAddress)) {
        console.log(`❌ ${isZh ? '地址格式无效。Solana 地址通常是 32-44 个字符的 base58 编码。' : 'Invalid address format. Solana addresses are usually 32-44 chars in base58.'}`);
        process.exit(1);
    }

    const minUsdValue = Number.parseFloat(minUsdRaw);
    if (!Number.isFinite(minUsdValue) || minUsdValue <= 0) {
        console.log(`❌ ${formatError('MISSING_REQUIRED_PARAMS', lang)}: ${isZh ? '金额阈值必须是大于 0 的数字' : 'USD threshold must be a number greater than 0'}`);
        process.exit(1);
    }

    if (watchMode) {
        await runWatch(walletAddress, minUsdValue);
    } else {
        await runOnce(walletAddress, minUsdValue);
    }
}

main().catch(() => {
    console.log(`❌ ${isZh ? '鲸鱼追踪失败，请稍后重试。' : 'Whale tracking failed. Please try again later.'}`);
    process.exit(1);
});
