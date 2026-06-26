#!/usr/bin/env node
/**
 * 🐋 WhaleWatch - 大额转账监控
 * 显示链上大额转账
 */

// 模拟转账数据
const TRANSFERS = [
    {
        time: '2 分钟前',
        direction: 'out',
        amount: 2500000,
        token: 'ETH',
        from: '0x8f3B...2Ae1',
        to: '0x742d...9Aa3'
    },
    {
        time: '5 分钟前',
        direction: 'in',
        amount: 1800000,
        token: 'USDC',
        from: '0x1C4e...8Bb2',
        to: '0x47ac...5Df3'
    },
    {
        time: '10 分钟前',
        direction: 'out',
        amount: 950000,
        token: 'WBTC',
        from: '0x2C91...9Bb4',
        to: 'Binance'
    },
    {
        time: '15 分钟前',
        direction: 'in',
        amount: 3200000,
        token: 'ETH',
        from: 'Coinbase',
        to: '0x9D1f...4Ef2'
    },
    {
        time: '22 分钟前',
        direction: 'out',
        amount: 500000,
        token: 'UNI',
        from: '0x5E2a...7Cd8',
        to: '0x742d...9Aa3'
    },
    {
        time: '30 分钟前',
        direction: 'in',
        amount: 1200000,
        token: 'LINK',
        from: '0x1C4e...8Bb2',
        to: '0x8f3B...2Ae1'
    }
];

function formatAmount(num) {
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(2)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toLocaleString()}`;
}

function showTransfers(minAmount = 100000) {
    let list = TRANSFERS.filter(t => t.amount >= minAmount);
    
    if (list.length === 0) {
        console.log(`ℹ️  暂无 > $${(minAmount / 1000).toFixed(0)}K 的转账`);
        return;
    }
    
    console.log('\n💸 WhaleWatch - 大额转账监控\n');
    console.log(`时间      方向   金额        代币   从                    至`);
    console.log(`───────────────────────────────────────────────────────────────────────────────`);
    
    list.forEach(t => {
        const time = t.time.padEnd(8);
        const dir = t.direction === 'in' ? '🟢 IN ' : '🔴 OUT';
        const amount = formatAmount(t.amount).padEnd(12);
        const token = t.token.padEnd(6);
        const from = t.from.padEnd(20);
        const arrow = t.direction === 'in' ? '→' : '→';
        const to = t.to;
        
        console.log(`${time} ${dir}  ${amount} ${token} ${from} ${arrow} ${to}`);
    });
    
    console.log(`\n💡 提示:`);
    console.log(`   node scripts/transfers.mjs --min 500000  # 只看 >$500K`);
    console.log(`   node scripts/transfers.mjs --token ETH   # 只看 ETH 转账`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🐋 WhaleWatch v0.1.0 - Follow The Whales`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🐋 WhaleWatch - 大额转账监控

用法:
  node scripts/transfers.mjs           # 查看所有大额转账
  node scripts/transfers.mjs --min 500000  # 只看 >$500K
  node scripts/transfers.mjs --token ETH   # 只看 ETH

选项:
  --help, -h          显示帮助
  --min <amount>      最小金额 (美元)
  --token <symbol>    代币符号
`);
    process.exit(0);
}

const minIndex = args.indexOf('--min');
const minAmount = minIndex > -1 ? parseInt(args[minIndex + 1]) : 100000;

showTransfers(minAmount);
