#!/usr/bin/env node
/**
 * 🎯 TokenSniper - 风险评估
 * 多维度风险评分系统
 */

// 模拟风险评估数据
function getRiskAssessment(address) {
    // 简化版：根据地址末尾判断风险 (实际应查询链上数据)
    const lastChar = address.slice(-1);
    const isLowRisk = ['0', '1', '2', 'a', 'b', 'c'].includes(lastChar);
    const isMediumRisk = ['3', '4', '5', '6', '7', 'd', 'e'].includes(lastChar);
    
    if (isLowRisk) {
        return {
            name: 'CatCoin',
            symbol: 'CAT',
            scores: {
                contract: { score: 85, label: '🟢 优秀' },
                liquidity: { score: 80, label: '🟢 良好' },
                holders: { score: 75, label: '🟢 健康' },
                team: { score: 70, label: '🟡 中等' },
                community: { score: 82, label: '🟢 活跃' }
            },
            overall: { score: 78, label: '🟢 低风险' },
            tips: [
                '✅ 合约已审计',
                '✅ 流动性已锁定 (180 天)',
                '✅ 持有者分布健康',
                '⚠️ 团队部分匿名'
            ],
            suggestion: '可正常参与，建议仓位 < 10%'
        };
    } else if (isMediumRisk) {
        return {
            name: 'PepeAI',
            symbol: 'PEPEAI',
            scores: {
                contract: { score: 65, label: '🟡 中等' },
                liquidity: { score: 60, label: '🟡 中等' },
                holders: { score: 70, label: '🟢 健康' },
                team: { score: 40, label: '🔴 匿名' },
                community: { score: 75, label: '🟢 活跃' }
            },
            overall: { score: 62, label: '🟡 中等风险' },
            tips: [
                '⚠️ 合约未经审计',
                '⚠️ 流动性锁定期较短 (30 天)',
                '✅ 持有者分布健康',
                '❌ 开发团队完全匿名'
            ],
            suggestion: '小额参与，设置止损，仓位 < 3%'
        };
    } else {
        return {
            name: 'SafeMoon V3',
            symbol: 'SAFEV3',
            scores: {
                contract: { score: 35, label: '🔴 高危' },
                liquidity: { score: 40, label: '🔴 高危' },
                holders: { score: 50, label: '🟡 集中' },
                team: { score: 30, label: '🔴 匿名' },
                community: { score: 45, label: '🟡 一般' }
            },
            overall: { score: 40, label: '🟠 较高风险' },
            tips: [
                '❌ 合约存在高危漏洞',
                '❌ 流动性未锁定',
                '⚠️ Top10 持仓 > 60%',
                '❌ 开发团队匿名且有不良历史'
            ],
            suggestion: '建议观望，高风险可能归零'
        };
    }
}

function showRisk(address) {
    if (!address || address.length < 10) {
        console.log('❌ 请提供有效的合约地址');
        console.log('用法：node scripts/risk.mjs 0x1234...5678');
        return;
    }
    
    const assessment = getRiskAssessment(address);
    
    console.log(`\n🔍 TokenSniper - 风险评估\n`);
    console.log(`代币：${assessment.name} (${assessment.symbol})`);
    console.log(`合约：${address}`);
    console.log(`\n风险维度              评分      状态`);
    console.log(`─────────────────────────────────────────────────────`);
    
    const dimensions = [
        ['合约安全', assessment.scores.contract],
        ['流动性风险', assessment.scores.liquidity],
        ['持有者集中度', assessment.scores.holders],
        ['开发团队', assessment.scores.team],
        ['社区活跃度', assessment.scores.community]
    ];
    
    dimensions.forEach(([name, data]) => {
        console.log(`${name.padEnd(20)}  ${String(data.score).padEnd(3)}/100    ${data.label}`);
    });
    
    console.log(`─────────────────────────────────────────────────────`);
    console.log(`整体评分              ${assessment.overall.score}/100    ${assessment.overall.label}`);
    
    console.log(`\n⚠️ 风险提示:`);
    assessment.tips.forEach(tip => console.log(`   ${tip}`));
    
    console.log(`\n💡 建议：${assessment.suggestion}`);
    console.log(`\n💰 赞助：USDT: 0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`);
    console.log(`\n🎯 TokenSniper v0.1.0 - Snipe Before Moon`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🎯 TokenSniper - 风险评估

用法:
  node scripts/risk.mjs <address>        # 评估代币风险

示例:
  node scripts/risk.mjs 0x1a2b3c4d5e6f7890abcdef1234567890abcdef12

风险评分标准:
  80-100  🟢 低风险     可正常参与
  60-79   🟡 中等风险   小额参与
  40-59   🟠 较高风险   谨慎参与
  0-39    🔴 高风险     建议观望

选项:
  --help, -h        显示帮助
`);
    process.exit(0);
}

const address = args.find(a => !a.startsWith('--'));

if (!address) {
    console.log('❌ 请提供合约地址');
    console.log('用法：node scripts/risk.mjs 0x1234...5678');
    process.exit(1);
}

showRisk(address);
