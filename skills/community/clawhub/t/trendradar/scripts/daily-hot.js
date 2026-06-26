#!/usr/bin/env node
'use strict';
/**
 * TrendRadar — 每日爆款简报
 * 由 openclaw cron 驱动，每日推送全品类热度榜
 * 用法: node scripts/daily-hot.js [--region cn|us|global|all] [--lang zh|en]
 */

const ALLOWED_REGIONS = new Set(['cn', 'us', 'global', 'all']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const regionIdx = args.indexOf('--region');
const rawRegion = regionIdx !== -1 ? args[regionIdx + 1] : 'all';
const region = ALLOWED_REGIONS.has(rawRegion) ? rawRegion : 'all';

const now = new Date();
const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const dateZH = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS_ZH[now.getDay()]}`;
const dateEN = `${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;

// 分品类数据源
const categorySources = {
  cn: [
    { cat: '数码/家电', sources: [
      { url: 'https://www.smzdm.com/fenlei/shuma/', note: '提取今日收藏/评论增长最快的前3条' },
      { url: 'https://www.xiaohongshu.com/explore?type=normal&tag=%E6%95%B0%E7%A0%81', note: '数码标签热门笔记' },
    ]},
    { cat: '美妆/护肤', sources: [
      { url: 'https://www.smzdm.com/fenlei/meizhuang/', note: '提取今日热门美妆商品' },
      { url: 'https://www.xiaohongshu.com/explore?type=normal&tag=%E7%BE%8E%E5%A6%86', note: '美妆标签热门笔记前3条' },
    ]},
    { cat: '家居/生活', sources: [
      { url: 'https://www.smzdm.com/fenlei/jiajushenghuoyongpin/', note: '今日热门家居商品' },
    ]},
    { cat: '服饰/穿搭', sources: [
      { url: 'https://www.xiaohongshu.com/explore?type=normal&tag=%E7%A9%BF%E6%90%AD', note: '穿搭标签热门推荐' },
    ]},
  ],
  us: [
    { cat: 'Electronics', sources: [
      { url: 'https://www.reddit.com/r/gadgets/hot/', note: 'Top 3 posts this week' },
      { url: 'https://www.producthunt.com/', note: "Today's top new tech products" },
    ]},
    { cat: 'Beauty & Health', sources: [
      { url: 'https://www.reddit.com/r/SkincareAddiction/hot/', note: 'Top 3 recommended products' },
    ]},
    { cat: 'Home & Living', sources: [
      { url: 'https://www.reddit.com/r/malelivingspace/hot/', note: 'Popular home products' },
    ]},
    { cat: 'Fashion', sources: [
      { url: 'https://www.reddit.com/r/femalefashionadvice/hot/', note: 'Trending fashion picks' },
    ]},
  ],
};

const activeCategories = region === 'cn' ? categorySources.cn
  : region === 'us' ? categorySources.us
  : [...categorySources.cn, ...categorySources.us];

if (lang === 'zh') {
  const catList = activeCategories.map((c, ci) => {
    const srcList = c.sources.map((s, si) =>
      `   ${ci + 1}.${si + 1} 打开 ${s.url}\n       → ${s.note}`
    ).join('\n');
    return `【${c.cat}】\n${srcList}`;
  }).join('\n\n');

  console.log(`请扫描今日各品类热门商品，生成每日爆款简报。
当前日期：${dateZH}

使用 browser 工具导航以下页面，每个品类提取 1-3 个热度最高的商品：

${catList}

补充信号：
- web_search "今日 ${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 爆款 好物 推荐" → 获取今日全网热词
- web_search "小红书 今日爆款 ${now.getMonth()+1}月" → 补充小红书月度爆款

整理规则：
- 每品类最多3条，全榜共 8-10 条
- 每条注明：商品名、热度来源平台、趋势方向（↑↑/↑/→/↓）、商业信号
- 优先选择"正在爆发"的商品（↑↑），而非已经见顶的
- 跨品类对比，最后选出 TOP 3 最值得关注

输出格式：
📡 TrendRadar · 今日爆款 · ${dateZH}
━━━━━━━━━━━━━━━━━━━━━━━

📱 数码/家电
① [商品名] ↑↑ | [热度说明] | 🔥爆发期
② ...

💄 美妆/护肤
① [商品名] ↑ | [热度说明] | 📈上升期
② ...

🏠 家居/生活
...

👗 服饰/穿搭
...

━━━━━━━━━━━━━━━━━━━━━━━
🏆 今日 TOP 3 最值关注
① [商品] — [1句理由]
   → 立即分析：openclaw run buywise advise "[商品名]"
   → 找券：openclaw run couponclaw find "[商品名]"
② ...
③ ...

💡 回复商品名查详细趋势 · 回复"找券"叠加优惠`);

} else {
  const catList = activeCategories.map((c, ci) => {
    const srcList = c.sources.map((s, si) =>
      `   ${ci + 1}.${si + 1} Open ${s.url}\n       → ${s.note}`
    ).join('\n');
    return `[${c.cat}]\n${srcList}`;
  }).join('\n\n');

  console.log(`Please scan today's trending products across categories and generate a daily hot items briefing.
Date: ${dateEN}

Use the browser tool to navigate each page and extract the top 1-3 trending items per category:

${catList}

Supplement with:
- web_search "trending products today ${now.getFullYear()} Reddit TikTok" → global trend signals
- web_search "viral product TikTok ${MONTHS_EN[now.getMonth()]} ${now.getFullYear()}" → TikTok viral items this month

Rules:
- Max 3 items per category, 8-10 total
- Each entry: product name, source platform, trend direction (↑↑/↑/→/↓), commercial signal
- Prioritize surging items (↑↑) over items already at peak
- Compare across categories; select TOP 3 overall

Output format:
📡 TrendRadar · Daily Hot · ${dateEN}
━━━━━━━━━━━━━━━━━━━━━━━

📱 Electronics
① [product] ↑↑ | [signal data] | 🔥 Surging
② ...

💄 Beauty & Health
① [product] ↑ | [signal data] | 📈 Rising
② ...

🏠 Home & Living
...

👗 Fashion
...

━━━━━━━━━━━━━━━━━━━━━━━
🏆 Today's TOP 3 Picks
① [product] — [one-sentence reason]
   → Deep analysis: openclaw run buywise advise "[product]"
   → Find coupons: openclaw run couponclaw find "[product]"
② ...
③ ...

💡 Reply with a product name for trend details · Reply "find coupons" to stack deals`);
}
