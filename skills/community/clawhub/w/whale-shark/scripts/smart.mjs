#!/usr/bin/env node
/**
 * 🐋 WhaleWatch - 聪明钱排行
 * 按胜率排序的钱包列表
 */

// 模拟聪明钱数据
const SMART_MONEY = [
    {
        rank: 1,
        address: '0x8f3B2A8e1C4d5E6f7890aBcDeF1234567890ABcD',
        label: 'Smart Money',
        winRate: 75,
        pnl30d: 12500000,
        txCount: 128,
        avgHold: '5.2 天',
        bestTrade: 'PEPE +2800%'
    },
    {
        rank: 2,
        address: '0x1C4e5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1Dd2',
        label: 'Smart Money',
        winRate: 72,
        pnl30d: 8900000,
        txCount: 94,
        avgHold: '3.8 天',
        bestTrade: 'ARB +450%'
    },
    {
        rank: 3,
        address: '0x9D1f2A3b4C5d6E7f8A9b0C1d2E3f4A5b6C7d8Ee2',
        label: 'DeFi Protocol',
        winRate: 71,
        pnl30d: 15200000,
        txCount: 67,
        avgHold: '12.5 天',
        bestTrade: 'UNI +180%'
    },
    {
        rank: 4,
        address: '0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503',
        label: 'Unknown Whale',
        winRate: 68,
        pnl30d: 6700000,
        txCount: 45,
        avgHold: '8.3 天',
        bestTrade: 'WBTC +95%'
    },
    {
        rank: 5,
        address: '0x2C91f36A8f8b5D3e9C0a1B2c3D4e5F6a7B8c9Dd4',
        label: 'VC Fund',
        winRate: 62,
        pnl30d: 4200000,
        txCount: 23,
        avgHold: '45.2 天',
        bestTrade: 'OP +320%'
    }
];

function formatPnL(num) {
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(2)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toLocaleString()}`;
}

function showSmartMoney(limit = 20) {
    let list = [...SMART_MONEY].sort((a, b) => b.winRate - a.winRate);
    list = list.slice(0, limit);
    
    console.log('\n🧠 WhaleWatch - 聪明钱排行 (按胜率)\n');
    console.log(`排名  钱包地址          胜率    30 天收益    交易数   平均持仓   最佳交易`);
    console.log(`────────────────────────────────────────────────────────────────────────────────────`);
    
    list.forEach(s => {
        const rank = String(s.rank).padEnd(4);
        const addr = s.address.slice(0, 6) + '...' + s.address.slice(-4);
        const winRate = `${s.winRate}%`.padEnd(6);
        const pnl = formatPnL(s.pnl30d).padEnd(12);
        const txCount = String(s.txCount).padEnd(7);
        const hold = s.avgHold.padEnd(9);
        const best = s.bestTrade;
        
        console.log(`${rank} ${addr.padEnd(16)} ${winRate} ${pnl} ${txCount} ${hold} ${best}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/smart.mjs --limit 10       # 限制显示 10 个`);
    console.log(`   node scripts/holdings.mjs 0x8f3B...    # 查看持仓`);
    console.log(`   node scripts/alert.mjs add --whale 0x8f3B --min 50000  # 设置提醒`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🐋 WhaleWatch - 聪明钱排行

用法:
  node scripts/smart.mjs              # 查看聪明钱排行
  node scripts/smart.mjs --limit 10   # 限制显示 10 个

选项:
  --help, -h        显示帮助
  --limit N         限制显示数量
`);
    process.exit(0);
}

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 20;

showSmartMoney(limit);
