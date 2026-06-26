#!/usr/bin/env node
/**
 * 🐋 WhaleWatch - 巨鲸钱包监控
 * 显示追踪的巨鲸钱包列表
 */

// 模拟巨鲸数据
const WHALES = [
    {
        address: '0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503',
        label: 'Unknown Whale',
        type: 'unknown',
        totalAssets: 125800000,
        change24h: 2.3,
        winRate: 68,
        txCount30d: 45
    },
    {
        address: '0x8f3B2A8e1C4d5E6f7890aBcDeF1234567890ABcD',
        label: 'Smart Money',
        type: 'smart_money',
        totalAssets: 89200000,
        change24h: 5.1,
        winRate: 75,
        txCount30d: 128
    },
    {
        address: '0x2C91f36A8f8b5D3e9C0a1B2c3D4e5F6a7B8c9Dd4',
        label: 'VC Fund',
        type: 'vc_fund',
        totalAssets: 67500000,
        change24h: -1.2,
        winRate: 62,
        txCount30d: 23
    },
    {
        address: '0x5E2a1B3c4D5e6F7a8B9c0D1e2F3a4B5c6D7e8Ff2',
        label: 'Market Maker',
        type: 'market_maker',
        totalAssets: 54300000,
        change24h: 0.8,
        winRate: 55,
        txCount30d: 856
    },
    {
        address: '0x9D1f2A3b4C5d6E7f8A9b0C1d2E3f4A5b6C7d8Ee2',
        label: 'DeFi Protocol',
        type: 'defi_protocol',
        totalAssets: 43700000,
        change24h: 12.4,
        winRate: 71,
        txCount30d: 67
    },
    {
        address: '0x1C4e5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1Dd2',
        label: 'Smart Money',
        type: 'smart_money',
        totalAssets: 38900000,
        change24h: 3.7,
        winRate: 72,
        txCount30d: 94
    }
];

const TYPE_ICONS = {
    smart_money: '🧠',
    vc_fund: '💼',
    market_maker: '🏦',
    defi_protocol: '🔧',
    unknown: '❓'
};

function formatAsset(num) {
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(2)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
}

function showWhales(limit = 20, type = null) {
    let list = [...WHALES];
    
    // 按类型筛选
    if (type) {
        list = list.filter(w => w.type === type);
    }
    
    // 按总资产排序
    list.sort((a, b) => b.totalAssets - a.totalAssets);
    
    // 限制数量
    list = list.slice(0, limit);
    
    if (list.length === 0) {
        console.log('❌ 暂无符合条件的巨鲸');
        return;
    }
    
    console.log('\n🐋 WhaleWatch - 巨鲸钱包监控\n');
    console.log(`排名  钱包地址          标签            总资产      24h 变化   胜率`);
    console.log(`─────────────────────────────────────────────────────────────────────────`);
    
    list.forEach((w, i) => {
        const rank = String(i + 1).padEnd(4);
        const addr = w.address.slice(0, 6) + '...' + w.address.slice(-4);
        const label = `${TYPE_ICONS[w.type]} ${w.label}`.padEnd(16);
        const assets = formatAsset(w.totalAssets).padEnd(12);
        const change = w.change24h >= 0 ? `🟢 +${w.change24h}%` : `🔴 ${w.change24h}%`;
        const winRate = `${w.winRate}%`.padEnd(6);
        
        console.log(`${rank} ${addr.padEnd(16)} ${label} ${assets} ${change.padEnd(10)} ${winRate}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/whale.mjs --limit 10       # 限制显示 10 个`);
    console.log(`   node scripts/whale.mjs --type smart_money  # 只看聪明钱`);
    console.log(`   node scripts/holdings.mjs 0x8f3B...2Ae1  # 查看持仓`);
    console.log(`   node scripts/smart.mjs                  # 聪明钱排行`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🐋 WhaleWatch - 巨鲸钱包监控

用法:
  node scripts/whale.mjs              # 查看所有巨鲸
  node scripts/whale.mjs --type smart_money  # 只看聪明钱
  node scripts/whale.mjs --limit 10   # 限制显示 10 个

选项:
  --help, -h          显示帮助
  --type [type]       按类型筛选 (smart_money/vc_fund/market_maker/defi_protocol/unknown)
  --limit N           限制显示数量
`);
    process.exit(0);
}

const typeIndex = args.indexOf('--type');
const type = typeIndex > -1 ? args[typeIndex + 1] : null;

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 20;

showWhales(limit, type);
