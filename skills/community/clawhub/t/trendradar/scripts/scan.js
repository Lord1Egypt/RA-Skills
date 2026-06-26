#!/usr/bin/env node
'use strict';
/**
 * TrendRadar — 热搜雷达主入口
 * 扫描社交媒体和社区，识别正在爆火的商品/品牌/话题，输出趋势方向和商业信号
 * 用法: node scripts/scan.js [关键词/品类] [--region cn|us|global|all] [--lang zh|en]
 */

const ALLOWED_REGIONS = new Set(['cn', 'us', 'global', 'all']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const regionIdx = args.indexOf('--region');
const rawRegion = regionIdx !== -1 ? args[regionIdx + 1] : 'all';
const region = ALLOWED_REGIONS.has(rawRegion) ? rawRegion : 'all';
const queryArgs = args.filter((a, i) => {
  if (['--lang', '--region'].includes(a)) return false;
  if (['--lang', '--region'].includes(args[i - 1])) return false;
  return true;
});
const query = queryArgs.join(' ').trim();

const now = new Date();
const dateISO = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const WEEKDAYS_ZH = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const dateZH = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${WEEKDAYS_ZH[now.getDay()]}`;
const dateEN = `${MONTHS_EN[now.getMonth()]} ${now.getDate()}, ${now.getFullYear()}`;

const encoded = query ? encodeURIComponent(query) : '';

const sources = {
  cn: query ? [
    { label: '小红书', url: `https://www.xiaohongshu.com/search_result?keyword=${encoded}&type=51`, note: '搜索笔记数量、最近发布时间、热门标签，判断是否处于爆发期' },
    { label: '微博热搜', url: `https://s.weibo.com/weibo?q=${encoded}&Refer=top`, note: '查是否进入微博热搜，记录热搜排名和阅读量' },
    { label: '什么值得买', url: `https://search.smzdm.com/?c=home&s=${encoded}&v=b`, note: '查近7天收藏数/评论数增长趋势，判断购买意愿热度' },
  ] : [
    { label: '小红书今日热门', url: `https://www.xiaohongshu.com/explore`, note: '提取首页"发现"板块热门商品笔记，取互动量最高的前5条' },
    { label: '微博热搜', url: `https://s.weibo.com/top/summary`, note: '提取消费/商品相关热搜词，过滤娱乐话题' },
    { label: '什么值得买热门', url: `https://www.smzdm.com/`, note: '提取今日收藏量增长最快的前5个商品' },
    { label: '抖音热销', url: `https://www.douyin.com/hot`, note: '如可访问，提取热销商品榜单前5条' },
  ],
  us: query ? [
    { label: 'Reddit', url: `https://www.reddit.com/search/?q=${encoded}&sort=hot&t=week`, note: '提取过去7天热帖数量、upvotes、评论数，判断讨论热度' },
    { label: 'Google Trends', url: `https://trends.google.com/trends/explore?q=${encoded}&date=now%207-d`, note: '查近7天搜索量趋势，是否"突破性上升"' },
    { label: 'Product Hunt', url: `https://www.producthunt.com/search?q=${encoded}`, note: '科技/新品类产品查热度排名和点赞数' },
  ] : [
    { label: 'Reddit /r/deals', url: `https://www.reddit.com/r/deals/hot/`, note: '提取热帖中的热销商品，记录 upvotes 和评论数' },
    { label: 'Reddit /r/BuyItForLife', url: `https://www.reddit.com/r/BuyItForLife/hot/`, note: '口碑型热销品，提取近7天热帖' },
    { label: 'Google Trends', url: `https://trends.google.com/trending?geo=US`, note: '提取今日美国热门搜索中的商品类词条' },
    { label: 'Product Hunt', url: `https://www.producthunt.com/`, note: '提取今日/本周热门新品' },
  ],
};

const activeSources = [];
if (region === 'cn') activeSources.push(...sources.cn);
else if (region === 'us') activeSources.push(...sources.us);
else activeSources.push(...sources.cn, ...sources.us);

if (lang === 'zh') {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. 打开 ${s.url}\n   → ${s.label}：${s.note}`
  ).join('\n\n');

  const subject = query ? `「${query}」` : '全品类';

  console.log(`请扫描${subject}的社交媒体热度，识别正在爆火的商品和趋势信号。
当前日期：${dateZH}

使用 browser 工具依次导航以下页面，提取真实热度数据：

${sourceList}

${query ? '' : `
另外补充执行：
- web_search "今日 ${dateISO} 小红书爆款 好物推荐" → 获取今日热词
- web_search "trending products Reddit ${dateISO}" → 获取英文社区今日趋势
`}

【趋势判断规则】
根据以下信号判断每个商品的趋势方向：
- ↑↑ 急速上升：近7天讨论量增长 >200%，或刚进热搜前50
- ↑ 上升中：近7天讨论量增长 50-200%，热度持续
- → 高位平稳：热度高但增速放缓，已进入成熟期
- ↓ 开始降温：讨论量连续3天下降

【商业信号判断】
- 🔥 爆发期（↑↑）：先买先得，价格可能随热度上涨
- 📈 上升期（↑）：好时机，热度带来更多优惠竞争
- 📊 成熟期（→）：稳定选择，但不会有价格红利
- 🧊 降温期（↓）：可等待价格下跌，或改选替代品

输出格式：
📡 TrendRadar · ${subject} · ${dateZH}
━━━━━━━━━━━━━━━━━━━━━━━
🔥 热度趋势排行

① [商品/品牌名] [↑↑/↑/→/↓]
   热度来源：[平台] [数据，如：12.3k笔记 / 热搜第X位 / 5.2k upvotes]
   商业信号：[🔥爆发期 / 📈上升期 / 📊成熟期 / 🧊降温期]
   → 深度分析：openclaw run buywise advise "[商品名]"
   → 找券省钱：openclaw run couponclaw find "[商品名]"

② [重复格式]
③ ...（共列出5-8条）

📊 趋势概览
↑↑ 急速上升：X个 | ↑ 上升中：X个 | → 平稳：X个 | ↓ 降温：X个

💡 最值得关注：[最有商业价值的1个趋势 + 1句理由]
━━━━━━━━━━━━━━━━━━━━━━━
💬 回复商品名查热度详情 · 回复"今日爆款"查全品类热榜`);

} else {
  const sourceList = activeSources.map((s, i) =>
    `${i + 1}. Open ${s.url}\n   → ${s.label}: ${s.note}`
  ).join('\n\n');

  const subject = query ? `"${query}"` : 'all categories';

  console.log(`Please scan social media and community platforms for trending products/brands${query ? ` related to ${subject}` : ''}.
Date: ${dateEN}

Use the browser tool to navigate each page and extract real trend data:

${sourceList}

${query ? '' : `
Also run:
- web_search "trending products today ${dateISO} Reddit TikTok" → supplement with keyword signals
- web_search "viral product TikTok ${dateISO}" → TikTok viral items
`}

[Trend direction rules]
Assign a trend direction to each item based on the data:
- ↑↑ Surging: discussion volume up >200% in 7 days, or just entered top trending
- ↑ Rising: discussion volume up 50-200% in 7 days, sustained momentum
- → Peak / stable: high volume but growth slowing, entering maturity
- ↓ Cooling: discussion volume declining 3+ consecutive days

[Commercial signal]
- 🔥 Surging (↑↑): buy before price rises with demand
- 📈 Rising (↑): good timing — more deals as competition increases
- 📊 Mature (→): stable choice, no price advantage
- 🧊 Cooling (↓): wait for price drop, or switch to alternatives

Output format:
📡 TrendRadar · ${subject} · ${dateEN}
━━━━━━━━━━━━━━━━━━━━━━━
🔥 Trending Now

① [Product/Brand] [↑↑/↑/→/↓]
   Signal source: [Platform] [data, e.g.: 12.3k posts / trending #X / 5.2k upvotes]
   Commercial signal: [🔥 Surging / 📈 Rising / 📊 Mature / 🧊 Cooling]
   → Deep analysis: openclaw run buywise advise "[product name]"
   → Find coupons: openclaw run couponclaw find "[product name]"

② [repeat format]
③ ... (list 5-8 items total)

📊 Trend overview
↑↑ Surging: X | ↑ Rising: X | → Stable: X | ↓ Cooling: X

💡 Top pick: [the 1 item with most commercial value + one-sentence reason]
━━━━━━━━━━━━━━━━━━━━━━━
💬 Reply with a product name for detailed trend data · Reply "hot today" for full trending list`);
}
