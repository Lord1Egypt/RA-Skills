#!/usr/bin/env node
/**
 * 🎯 TokenSniper - 新代币监控
 * 显示最近上线的代币
 */

// 模拟新代币数据 (实际应从 DEX API 获取)
const NEW_TOKENS = [
    {
        name: 'PepeAI',
        symbol: 'PEPEAI',
        chain: 'Ethereum',
        address: '0x1a2b3c4d5e6f7890abcdef1234567890abcdef12',
        price: 0.00012,
        liquidity: 50000,
        risk: 'medium',
        volume24h: 12000,
        listedAgo: 10,
        change24h: 245
    },
    {
        name: 'SafeMoon V3',
        symbol: 'SAFEV3',
        chain: 'BSC',
        address: '0x2b3c4d5e6f7890abcdef1234567890abcdef1234',
        price: 0.000001,
        liquidity: 25000,
        risk: 'high',
        volume24h: 5000,
        listedAgo: 15,
        change24h: -35
    },
    {
        name: 'CatCoin',
        symbol: 'CAT',
        chain: 'Base',
        address: '0x3c4d5e6f7890abcdef1234567890abcdef123456',
        price: 0.0023,
        liquidity: 100000,
        risk: 'low',
        volume24h: 45000,
        listedAgo: 20,
        change24h: 89
    },
    {
        name: 'AI_Token',
        symbol: 'AIT',
        chain: 'Arbitrum',
        address: '0x4d5e6f7890abcdef1234567890abcdef12345678',
        price: 0.15,
        liquidity: 200000,
        risk: 'low',
        volume24h: 89000,
        listedAgo: 30,
        change24h: 156
    },
    {
        name: 'DogeKing',
        symbol: 'DOGEK',
        chain: 'Ethereum',
        address: '0x5e6f7890abcdef1234567890abcdef1234567890',
        price: 0.000045,
        liquidity: 35000,
        risk: 'medium',
        volume24h: 8000,
        listedAgo: 45,
        change24h: 67
    },
    {
        name: 'MetaVerse',
        symbol: 'META',
        chain: 'Polygon',
        address: '0x6f7890abcdef1234567890abcdef1234567890ab',
        price: 0.078,
        liquidity: 150000,
        risk: 'low',
        volume24h: 34000,
        listedAgo: 60,
        change24h: 23
    }
];

const RISK_ICONS = {
    low: '🟢',
    medium: '🟡',
    high: '🔴'
};

const RISK_LABELS = {
    low: '低',
    medium: '中',
    high: '高'
};

function formatNumber(num) {
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
}

function formatPrice(price) {
    if (price < 0.001) return `$${price.toFixed(6)}`;
    if (price < 1) return `$${price.toFixed(4)}`;
    return `$${price.toFixed(2)}`;
}

function showMonitor(chain = null, limit = 20) {
    let tokens = [...NEW_TOKENS];
    
    // 按链筛选
    if (chain) {
        tokens = tokens.filter(t => t.chain.toLowerCase() === chain.toLowerCase());
    }
    
    // 限制数量
    tokens = tokens.slice(0, limit);
    
    if (tokens.length === 0) {
        console.log('❌ 暂无符合条件的代币');
        return;
    }
    
    console.log('\n🎯 TokenSniper - 新代币监控\n');
    console.log(`时间        代币名称        链        价格        流动性    风险    24h 涨跌`);
    console.log(`────────────────────────────────────────────────────────────────────────────────`);
    
    tokens.forEach(t => {
        const time = `${t.listedAgo}分钟前`.padEnd(10);
        const name = `${t.name} (${t.symbol})`.padEnd(16);
        const chain = t.chain.padEnd(10);
        const price = formatPrice(t.price).padEnd(12);
        const liquidity = formatNumber(t.liquidity).padEnd(10);
        const risk = `${RISK_ICONS[t.risk]} ${RISK_LABELS[t.risk]}`.padEnd(8);
        const change = t.change24h >= 0 ? `🟢 +${t.change24h}%` : `🔴 ${t.change24h}%`;
        
        console.log(`${time} ${name} ${chain} ${price} ${liquidity} ${risk} ${change}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/monitor.mjs --chain ethereum  # 只看 Ethereum`);
    console.log(`   node scripts/monitor.mjs --limit 5         # 限制显示 5 个`);
    console.log(`   node scripts/analyze.mjs 0x1234...5678     # 查看代币详情`);
    console.log(`   node scripts/risk.mjs 0x1234...5678        # 风险评估`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🎯 TokenSniper v0.1.0 - Snipe Before Moon`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🎯 TokenSniper - 新代币监控

用法:
  node scripts/monitor.mjs              # 查看所有新代币
  node scripts/monitor.mjs --chain ethereum  # 只看 Ethereum
  node scripts/monitor.mjs --limit 5    # 限制显示 5 个

选项:
  --help, -h          显示帮助
  --chain [name]      按链筛选 (ethereum/bsc/base/arbitrum/polygon)
  --limit N           限制显示数量
`);
    process.exit(0);
}

const chainIndex = args.indexOf('--chain');
const chain = chainIndex > -1 ? args[chainIndex + 1] : null;

const limitIndex = args.indexOf('--limit');
const limit = limitIndex > -1 ? parseInt(args[limitIndex + 1]) : 20;

showMonitor(chain, limit);
