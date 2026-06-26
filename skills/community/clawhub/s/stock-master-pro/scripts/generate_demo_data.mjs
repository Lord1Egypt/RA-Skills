#!/usr/bin/env node

/**
 * 生成演示数据
 * 用于 Dashboard 展示效果（复盘、公告、龙虎榜、财报、选股）
 */

import { writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STOCKS_DIR = join(__dirname, '../stocks');

/**
 * 生成复盘报告数据
 */
function generateReviewData() {
  const dateStr = new Date().toISOString().split('T')[0];
  const reviewDir = join(STOCKS_DIR, 'reviews');
  
  const noonReview = `# 【午盘复盘】${dateStr} 12:30

## 📊 大盘概览

| 指数 | 现价 | 涨跌 | 幅度 | 成交额 |
|------|------|------|------|--------|
| 上证指数 | 3878.04 | +64.76 | +1.70% | 8746 亿 |
| 深证成指 | 13519.91 | +174.40 | +1.31% | 10774 亿 |
| 创业板指 | 3243.65 | +8.43 | +0.26% | 4847 亿 |
| 中证 500 | 8194.33 | +96.08 | +1.19% | 1285 亿 |

## 🔥 热点板块

| 排名 | 板块 | 涨幅 | 资金净流入 |
|------|------|------|------------|
| 1 | 电力板块 | +3.5% | +25.6 亿 |
| 2 | 绿色电力 | +2.8% | +18.3 亿 |
| 3 | 粤港澳大湾区 | +2.1% | +12.5 亿 |

## 💰 持仓表现

### 📈 穗恒运 A (000531.SZ)

- **现价**: 7.83 元
- **今日**: +8.45% 🔥
- **量比**: 3.00
- **换手**: 10.52%
- **盈亏**: +400.96 元 (+7.89%)
- **备注**: 趋势票，电力概念

**操作建议**: 🔥 强势，继续持有

## 📌 下午策略

- **仓位建议**: 6-7 成
- **关注方向**: 电力板块持续性
- **风险提示**: 避免追高，逢低布局

---

⚠️ **免责声明**: 以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。
`;

  writeFileSync(join(reviewDir, `${dateStr}_noon.md`), noonReview);
  console.log('✅ 午盘复盘已生成');
}

/**
 * 生成公告数据
 */
function generateAnnouncementsData() {
  const announcements = {
    updateTime: new Date().toISOString(),
    count: 3,
    announcements: [
      {
        code: '000531.SZ',
        name: '穗恒运 A',
        type: 'positive',
        level: 'good',
        label: '利好',
        title: '关于公司签订重大经营合同的公告',
        date: '2026-03-24',
        summary: '公司与广州发展集团股份有限公司签订供用电合同，预计年度交易金额约 5 亿元'
      },
      {
        code: '603259.SH',
        name: '药明康德',
        type: 'positive',
        level: 'good',
        label: '利好',
        title: '关于回购公司股份进展的公告',
        date: '2026-03-23',
        summary: '公司已累计回购股份 500 万股，占总股本的 0.17%'
      },
      {
        code: '002466.SZ',
        name: '天齐锂业',
        type: 'neutral',
        level: 'info',
        label: '中性',
        title: '关于股东权益变动的提示性公告',
        date: '2026-03-22',
        summary: '股东完成股份减持计划，累计减持 1.5% 股份'
      }
    ]
  };
  
  writeFileSync(join(STOCKS_DIR, 'announcements.json'), JSON.stringify(announcements, null, 2));
  console.log('✅ 公告数据已生成');
}

/**
 * 生成龙虎榜数据
 */
function generateDragonTigerData() {
  const dragonTiger = {
    updateTime: new Date().toISOString(),
    count: 2,
    data: [
      {
        code: '000531.SZ',
        name: '穗恒运 A',
        date: '2026-03-24',
        closePrice: 7.83,
        changePct: 8.45,
        turnover: 53900,
        buyAmount: 12500,
        sellAmount: 8200,
        netAmount: 4300,
        institutionalBuy: 3500,
        institutionalSell: 1200,
        hotMoneyBuy: 5000,
        hotMoneySell: 4500,
        northboundBuy: 2000,
        northboundSell: 1500,
        summary: '净买入 4300 万元，机构净买入，游资净买入',
        buySeats: [
          { name: '机构专用', amount: 3500, type: '机构' },
          { name: '中信证券上海分公司', amount: 2800, type: '游资' },
          { name: '深股通专用', amount: 2000, type: '北向资金' }
        ],
        sellSeats: [
          { name: '机构专用', amount: 1200, type: '机构' },
          { name: '国泰君安上海江苏路', amount: 2500, type: '游资' }
        ]
      }
    ]
  };
  
  writeFileSync(join(STOCKS_DIR, 'dragon_tiger.json'), JSON.stringify(dragonTiger, null, 2));
  console.log('✅ 龙虎榜数据已生成');
}

/**
 * 生成财报日历数据
 */
function generateEarningsCalendarData() {
  const earningsCalendar = {
    updateTime: new Date().toISOString(),
    count: 5,
    calendar: [
      {
        code: '000531.SZ',
        name: '穗恒运 A',
        earningsType: '一季报',
        estimatedDate: '2026-04-15',
        daysUntil: 22,
        isEstimated: true,
        forecast: '预增',
        riskLevel: 'normal'
      },
      {
        code: '603259.SH',
        name: '药明康德',
        earningsType: '一季报',
        estimatedDate: '2026-04-20',
        daysUntil: 27,
        isEstimated: true,
        forecast: '预增',
        riskLevel: 'normal'
      },
      {
        code: '002466.SZ',
        name: '天齐锂业',
        earningsType: '一季报',
        estimatedDate: '2026-04-25',
        daysUntil: 32,
        isEstimated: true,
        forecast: '未知',
        riskLevel: 'normal'
      }
    ]
  };
  
  writeFileSync(join(STOCKS_DIR, 'earnings_calendar.json'), JSON.stringify(earningsCalendar, null, 2));
  console.log('✅ 财报日历已生成');
}

/**
 * 生成选股结果数据
 */
function generateScreenerData() {
  const screenerResults = {
    updateTime: new Date().toISOString(),
    count: 5,
    results: [
      {
        name: '药明康德',
        code: '603259.SH',
        price: 93.14,
        changePct: 6.09,
        volumeRatio: 3.47,
        turnover: 2.17,
        marketCap: 2779,
        score: 85,
        rating: '⭐⭐⭐⭐⭐',
        reasons: ['放量突破', '缠论向上段', '机构净买入']
      },
      {
        name: '天齐锂业',
        code: '002466.SZ',
        price: 50.43,
        changePct: 2.92,
        volumeRatio: 2.02,
        turnover: 2.44,
        marketCap: 744,
        score: 82,
        rating: '⭐⭐⭐⭐⭐',
        reasons: ['底部反转', '筹码集中', '量能温和']
      },
      {
        name: '海螺水泥',
        code: '600585.SH',
        price: 23.14,
        changePct: 1.89,
        volumeRatio: 1.03,
        turnover: 0.39,
        marketCap: 926,
        score: 75,
        rating: '⭐⭐⭐⭐',
        reasons: ['低估值', '稳健上涨', '高股息']
      },
      {
        name: '中国平安',
        code: '601318.SH',
        price: 58.10,
        changePct: 1.10,
        volumeRatio: 1.12,
        turnover: 0.85,
        marketCap: 1060,
        score: 78,
        rating: '⭐⭐⭐⭐',
        reasons: ['突破形态', '筹码集中', '金融龙头']
      },
      {
        name: '招商银行',
        code: '600036.SH',
        price: 39.18,
        changePct: 1.29,
        volumeRatio: 1.05,
        turnover: 0.62,
        marketCap: 980,
        score: 76,
        rating: '⭐⭐⭐⭐',
        reasons: ['强势上涨', '低估值', '零售银行']
      }
    ]
  };
  
  writeFileSync(join(STOCKS_DIR, 'screener_results.json'), JSON.stringify(screenerResults, null, 2));
  console.log('✅ 选股结果已生成');
}

/**
 * 主函数
 */
function main() {
  console.log('📊 Stock Master Pro - 生成演示数据\n');
  
  // 确保目录存在
  const reviewDir = join(STOCKS_DIR, 'reviews');
  if (!existsSync(reviewDir)) {
    import('fs').then(({ mkdirSync }) => {
      mkdirSync(reviewDir, { recursive: true });
    });
  }
  
  generateReviewData();
  generateAnnouncementsData();
  generateDragonTigerData();
  generateEarningsCalendarData();
  generateScreenerData();
  
  console.log('\n✅ 所有演示数据已生成完成！');
  console.log('\n📁 生成的文件：');
  console.log('  - stocks/reviews/YYYY-MM-DD_noon.md');
  console.log('  - stocks/announcements.json');
  console.log('  - stocks/dragon_tiger.json');
  console.log('  - stocks/earnings_calendar.json');
  console.log('  - stocks/screener_results.json');
}

main();
