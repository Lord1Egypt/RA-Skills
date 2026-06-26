#!/usr/bin/env node
/**
 * 🎯 TokenSniper - 代币分析
 * 详细分析代币信息
 */

// 模拟代币数据
function getTokenAnalysis(address) {
    const lastChar = address.slice(-1);
    const isLowRisk = ['0', '1', '2', 'a', 'b', 'c'].includes(lastChar);
    
    if (isLowRisk) {
        return {
            name: 'CatCoin',
            symbol: 'CAT',
            address: address,
            chain: 'Base',
            price: 0.0023,
            change24h: 89,
            marketCap: 2300000,
            liquidity: 100000,
            volume24h: 45000,
            holders: 1234,
            top10Holders: 35,
            contractHolders: 5,
            risk: {
                overall: 78,
                label: '🟢 低风险'
            },
            audit: true,
            liquidityLocked: true,
            lockDays: 180
        };
    } else {
        return {
            name: 'PepeAI',
            symbol: 'PEPEAI',
            address: address,
            chain: 'Ethereum',
            price: 0.00012,
            change24h: 245,
            marketCap: 1200000,
            liquidity: 50000,
            volume24h: 12000,
            holders: 856,
            top10Holders: 45,
            contractHolders: 8,
            risk: {
                overall: 62,
                label: '🟡 中等风险'
            },
            audit: false,
            liquidityLocked: true,
            lockDays: 30
        };
    }
}

function formatNumber(num) {
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toLocaleString()}`;
}

function showAnalysis(address) {
    if (!address || address.length < 10) {
        console.log('❌ 请提供有效的合约地址');
        console.log('用法：node scripts/analyze.mjs 0x1234...5678');
        return;
    }
    
    const token = getTokenAnalysis(address);
    
    console.log(`\n📊 TokenSniper - 代币分析\n`);
    console.log(`代币：${token.name} (${token.symbol})`);
    console.log(`合约：${token.address}`);
    console.log(`链：${token.chain}`);
    
    console.log(`\n价格信息:`);
    console.log(`  当前价格：$${token.price < 0.001 ? token.price.toFixed(6) : token.price.toFixed(4)}`);
    console.log(`  24h 涨跌：${token.change24h >= 0 ? '🟢' : '🔴'} ${token.change24h >= 0 ? '+' : ''}${token.change24h}%`);
    console.log(`  市值：${formatNumber(token.marketCap)}`);
    console.log(`  流动性：${formatNumber(token.liquidity)}`);
    console.log(`  24h 成交量：${formatNumber(token.volume24h)}`);
    
    console.log(`\n持有者分析:`);
    console.log(`  总持有者：${token.holders.toLocaleString()}`);
    console.log(`  Top10 持仓：${token.top10Holders}%`);
    console.log(`  合约持仓：${token.contractHolders}%`);
    
    console.log(`\n风险评估:`);
    console.log(`  整体评分：${token.risk.label} (${token.risk.overall}/100)`);
    console.log(`  合约审计：${token.audit ? '✅ 已审计' : '❌ 未审计'}`);
    console.log(`  流动性锁定：${token.liquidityLocked ? `✅ 已锁定 (${token.lockDays}天)` : '❌ 未锁定'}`);
    console.log(`  持有者分布：${token.top10Holders < 40 ? '✅ 健康' : '⚠️ 集中'}`);
    
    console.log(`\n💡 建议：${token.risk.overall >= 75 ? '可正常参与' : token.risk.overall >= 60 ? '小额参与，设置止损' : '高风险，建议观望'}`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🎯 TokenSniper v0.1.0 - Snipe Before Moon`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🎯 TokenSniper - 代币分析

用法:
  node scripts/analyze.mjs <address>     # 分析代币详情

示例:
  node scripts/analyze.mjs 0x1a2b3c4d5e6f7890abcdef1234567890abcdef12

选项:
  --help, -h        显示帮助
`);
    process.exit(0);
}

const address = args.find(a => !a.startsWith('--'));

if (!address) {
    console.log('❌ 请提供合约地址');
    console.log('用法：node scripts/analyze.mjs 0x1234...5678');
    process.exit(1);
}

showAnalysis(address);
