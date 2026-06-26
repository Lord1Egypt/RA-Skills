#!/usr/bin/env node
/**
 * 🐋 WhaleWatch - 持仓分析
 * 查看巨鲸持仓详情
 */

// 模拟持仓数据
function getHoldings(address) {
    const short = address.slice(-4).toLowerCase();
    
    if (['ae1', 'bb2'].includes(short)) {
        return {
            address,
            label: 'Smart Money',
            winRate: 75,
            holdings: [
                { token: 'ETH', value: 45200000, percent: 51, change24h: 12 },
                { token: 'USDC', value: 18500000, percent: 21, change24h: -3 },
                { token: 'WBTC', value: 12800000, percent: 14, change24h: 5 },
                { token: 'UNI', value: 6200000, percent: 7, change24h: 28 },
                { token: 'LINK', value: 4100000, percent: 5, change24h: 0 }
            ],
            operations24h: [
                { action: 'buy', token: 'UNI', amount: 2300000, price: 5.82 },
                { action: 'buy', token: 'ETH', amount: 1100000, price: 2050 },
                { action: 'sell', token: 'USDC', amount: 800000, price: 1.0 }
            ],
            insight: '持续加仓 DeFi 蓝筹'
        };
    } else if (['503', 'dd4'].includes(short)) {
        return {
            address,
            label: 'Unknown Whale',
            winRate: 68,
            holdings: [
                { token: 'ETH', value: 63000000, percent: 50, change24h: 4 },
                { token: 'USDT', value: 37500000, percent: 30, change24h: 0 },
                { token: 'WBTC', value: 25300000, percent: 20, change24h: 2 }
            ],
            operations24h: [
                { action: 'buy', token: 'ETH', amount: 2800000, price: 2040 }
            ],
            insight: '大额增持 ETH'
        };
    } else {
        return {
            address,
            label: 'Market Maker',
            winRate: 55,
            holdings: [
                { token: 'ETH', value: 27000000, percent: 50, change24h: 1 },
                { token: 'USDC', value: 21600000, percent: 40, change24h: 0 },
                { token: 'DAI', value: 5400000, percent: 10, change24h: 0 }
            ],
            operations24h: [
                { action: 'sell', token: 'ETH', amount: 500000, price: 2070 },
                { action: 'buy', token: 'USDC', amount: 500000, price: 1.0 }
            ],
            insight: '正常做市操作'
        };
    }
}

function formatValue(num) {
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(2)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toLocaleString()}`;
}

function showHoldings(address) {
    if (!address || address.length < 10) {
        console.log('❌ 请提供有效的钱包地址');
        console.log('用法：node scripts/holdings.mjs 0x8f3B...2Ae1');
        return;
    }
    
    const data = getHoldings(address);
    
    console.log(`\n📊 WhaleWatch - 巨鲸持仓分析\n`);
    console.log(`钱包：${data.address}`);
    console.log(`标签：${data.label}`);
    console.log(`胜率：${data.winRate}% (过去 30 天)`);
    
    console.log(`\n持仓分布:`);
    data.holdings.forEach(h => {
        const icon = h.change24h > 0 ? '🟢' : h.change24h < 0 ? '🔴' : '🟡';
        const change = h.change24h > 0 ? `+${h.change24h}%` : `${h.change24h}%`;
        console.log(`  ${h.token.padEnd(8)} ${formatValue(h.value).padEnd(12)} ${h.percent}%     ${icon} ${change}`);
    });
    
    if (data.operations24h && data.operations24h.length > 0) {
        console.log(`\n24h 操作:`);
        data.operations24h.forEach(op => {
            const icon = op.action === 'buy' ? '✅' : '❌';
            const action = op.action === 'buy' ? '买入' : '卖出';
            const price = op.price < 1 ? op.price.toFixed(4) : op.price.toLocaleString();
            console.log(`  ${icon} ${action} $${(op.amount / 1000000).toFixed(2)}M ${op.token} @ $${price}`);
        });
    }
    
    console.log(`\n💡 聪明钱指标：${data.insight}`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🐋 WhaleWatch - 持仓分析

用法:
  node scripts/holdings.mjs <address>    # 分析巨鲸持仓

示例:
  node scripts/holdings.mjs 0x8f3B2A8e1C4d5E6f7890aBcDeF1234567890ABcD

选项:
  --help, -h        显示帮助
`);
    process.exit(0);
}

const address = args.find(a => !a.startsWith('--'));

if (!address) {
    console.log('❌ 请提供钱包地址');
    console.log('用法：node scripts/holdings.mjs 0x8f3B...2Ae1');
    process.exit(1);
}

showHoldings(address);
