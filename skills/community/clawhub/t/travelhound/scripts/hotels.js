#!/usr/bin/env node
'use strict';
/**
 * TravelHound — 酒店比价 + OTA优惠码叠加
 * 用法: node scripts/hotels.js <目的地> [--checkin YYYY-MM-DD] [--checkout YYYY-MM-DD] [--guests N] [--budget budget|mid|luxury] [--lang zh|en]
 */

const ALLOWED_BUDGETS = new Set(['budget', 'mid', 'luxury']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';

const checkinIdx = args.indexOf('--checkin');
const checkin = checkinIdx !== -1 ? args[checkinIdx + 1] : null;

const checkoutIdx = args.indexOf('--checkout');
const checkout = checkoutIdx !== -1 ? args[checkoutIdx + 1] : null;

const guestsIdx = args.indexOf('--guests');
const guests = guestsIdx !== -1 ? parseInt(args[guestsIdx + 1], 10) || 1 : 1;

const budgetIdx = args.indexOf('--budget');
const rawBudget = budgetIdx !== -1 ? args[budgetIdx + 1] : 'mid';
const budget = ALLOWED_BUDGETS.has(rawBudget) ? rawBudget : 'mid';

const destArgs = args.filter((a, i) => {
  const flags = ['--lang', '--checkin', '--checkout', '--guests', '--budget'];
  if (flags.includes(a)) return false;
  if (flags.includes(args[i - 1])) return false;
  return true;
});
const destination = destArgs.join(' ').trim();

if (!destination) {
  console.error(lang === 'zh'
    ? '用法: node scripts/hotels.js <目的地> [--checkin YYYY-MM-DD] [--checkout YYYY-MM-DD] [--guests N] [--budget budget|mid|luxury]'
    : 'Usage: node scripts/hotels.js <destination> [--checkin YYYY-MM-DD] [--checkout YYYY-MM-DD] [--guests N] [--budget budget|mid|luxury]');
  process.exit(1);
}

const encoded = encodeURIComponent(destination);
const nights = (checkin && checkout)
  ? Math.round((new Date(checkout) - new Date(checkin)) / 86400000)
  : null;

const budgetLabelZH = { budget: '经济型（¥300以下/晚）', mid: '中档（¥300-800/晚）', luxury: '高档（¥800+/晚）' }[budget];
const budgetLabelEN = { budget: 'Budget (under $50/night)', mid: 'Mid-range ($50-150/night)', luxury: 'Luxury ($150+/night)' }[budget];

if (lang === 'zh') {
  const dateNote = checkin ? `入住：${checkin}${checkout ? ` → 退房：${checkout}（共${nights}晚）` : ''}` : '日期：未指定';

  console.log(`请为以下住宿需求查询酒店价格，并找到最优 OTA 优惠。

目的地：${destination}
${dateNote}
人数：${guests}人 · 预算档位：${budgetLabelZH}

使用 browser 工具依次导航以下页面，提取真实酒店价格：

1. 打开 https://www.booking.com/searchresults.html?ss=${encoded}${checkin ? `&checkin=${checkin}` : ''}${checkout ? `&checkout=${checkout}` : ''}&group_adults=${guests}
   → Booking.com：提取该档位前5家酒店（名称、价格/晚、评分、距市中心距离）
   → 查看是否有"天才会员折扣"或"限时特惠"标签

2. 打开 https://www.agoda.com/search?q=${encoded}${checkin ? `&checkIn=${checkin}` : ''}${checkout ? `&checkOut=${checkout}` : ''}&numberOfGuest=${guests}
   → Agoda：同样提取前5家，Agoda 在亚洲目的地通常有独家低价
   → 注意查看"银行卡专属折扣"（特定信用卡额外减）

3. 打开 https://www.hotels.com/search.do?q-destination=${encoded}${checkin ? `&q-check-in=${checkin}` : ''}${checkout ? `&q-check-out=${checkout}` : ''}
   → Hotels.com：集满10晚送1晚，查询是否有额外促销

4. 打开 https://hotels.trip.com/hotels/list?city=${encoded}${checkin ? `&startDate=${checkin}` : ''}${checkout ? `&endDate=${checkout}` : ''}
   → 携程酒店：国内及亚洲目的地必查，会员价通常比国际平台低 10-20%

5. web_search「${destination} 酒店 ${checkin || '近期'} 优惠 团购」
   → 补充：美团、飞猪等国内平台是否有团购价

【价格对比规则】
- 仅记录实际从页面读取的价格（标注含税/不含税）
- 标注每个平台是否需要会员登录才能看到最低价
- 同一家酒店跨平台比价，找出实际最低平台

【OTA 优惠码叠加】
查询各平台专属优惠码（在价格基础上再减）：
- web_search「Booking.com promo code ${new Date().getFullYear()}」
- web_search「Agoda coupon code ${new Date().getFullYear()}」
或直接运行：openclaw run couponclaw find "Booking.com" --region all
           openclaw run couponclaw find "Agoda" --region all

输出格式：
🏨 TravelHound · ${destination} 酒店
━━━━━━━━━━━━━━━━━━━━━━━
📋 ${dateNote}${nights ? `（${nights}晚）` : ''} · ${guests}人 · ${budgetLabelZH}

💰 各平台价格对比（${budgetLabelZH}）
酒店名         | Booking | Agoda | Hotels.com | 携程 | 最低
[酒店A]        | ¥XXX    | ¥XXX  | ¥XXX       | ¥XXX | [平台] ¥XXX
[酒店B]        | ...
（列出3-5家同档位酒店）

🏷️ 平台优惠
[平台] 优惠码/活动：[描述] | 额外节省：¥XXX

🔢 最优方案
[酒店名] × ${nights || 'X'}晚 = ¥XXX（通过 [平台] + [优惠码] 到手价 ¥XXX/晚）

📌 注意事项
[取消政策 / 含不含早餐 / 需不需提前付款]
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"查机票"继续规划 · 回复"全程规划"一站搞定`);

} else {
  const dateNote = checkin ? `Check-in: ${checkin}${checkout ? ` → Check-out: ${checkout} (${nights} nights)` : ''}` : 'Dates: not specified';

  console.log(`Please search for hotels at the destination below and find the best OTA deal with coupon stacking.

Destination: ${destination}
${dateNote}
Guests: ${guests} · Budget: ${budgetLabelEN}

Use the browser tool to navigate each page and extract real hotel prices:

1. Open https://www.booking.com/searchresults.html?ss=${encoded}${checkin ? `&checkin=${checkin}` : ''}${checkout ? `&checkout=${checkout}` : ''}&group_adults=${guests}
   → Booking.com: extract top 5 hotels in this budget tier (name, price/night, rating, distance from center)
   → Check for "Genius" member discounts or "Limited-time deal" labels

2. Open https://www.agoda.com/search?q=${encoded}${checkin ? `&checkIn=${checkin}` : ''}${checkout ? `&checkOut=${checkout}` : ''}&numberOfGuest=${guests}
   → Agoda: often has exclusive lower rates for Asian destinations
   → Look for "Bank card exclusive discount" offers

3. Open https://www.hotels.com/search.do?q-destination=${encoded}${checkin ? `&q-check-in=${checkin}` : ''}${checkout ? `&q-check-out=${checkout}` : ''}
   → Hotels.com: earn 1 free night per 10 booked; check for additional promos

4. Open https://uk.trip.com/hotels/list?city=${encoded}${checkin ? `&startDate=${checkin}` : ''}${checkout ? `&endDate=${checkout}` : ''}
   → Trip.com: member rates often 10-20% cheaper for Asian destinations

5. web_search "${destination} hotel deals ${checkin || 'this month'} discount"
   → Supplement with any flash sales or coupon sites

[Comparison rules]
- Only record prices actually read from the page (note if tax-inclusive or not)
- Flag any platform requiring login to see lowest price
- Cross-compare the same hotel across platforms to find true best price

[OTA coupon stacking]
  openclaw run couponclaw find "Booking.com" --region all
  openclaw run couponclaw find "Agoda" --region all

Output format:
🏨 TravelHound · ${destination} Hotels
━━━━━━━━━━━━━━━━━━━━━━━
📋 ${dateNote}${nights ? ` (${nights} nights)` : ''} · ${guests} guest(s) · ${budgetLabelEN}

💰 Price comparison (${budgetLabelEN})
Hotel          | Booking | Agoda | Hotels.com | Trip.com | Best
[Hotel A]      | $XXX    | $XXX  | $XXX       | $XXX     | [platform] $XXX
[Hotel B]      | ...
(list 3-5 hotels in this tier)

🏷️ Platform deals
[Platform] Code/promotion: [description] | Extra saving: $XXX

🔢 Best deal
[Hotel name] × ${nights || 'X'} nights = $XXX (via [platform] + [code] → $XXX/night effective)

📌 Watch out for
[Cancellation policy / breakfast included / prepayment required]
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "find flights" to continue · Reply "full trip" for combined planning`);
}
