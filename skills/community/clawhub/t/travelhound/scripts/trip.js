#!/usr/bin/env node
'use strict';
/**
 * TravelHound — 全程行程规划（机票+酒店+目的地情报）
 * 用法: node scripts/trip.js <目的地> [--from 出发城市] [--date YYYY-MM-DD] [--nights N] [--budget budget|mid|luxury] [--lang zh|en]
 */

const ALLOWED_BUDGETS = new Set(['budget', 'mid', 'luxury']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';

const fromIdx = args.indexOf('--from');
const from = fromIdx !== -1 ? args[fromIdx + 1] : null;

const dateIdx = args.indexOf('--date');
const date = dateIdx !== -1 ? args[dateIdx + 1] : null;

const nightsIdx = args.indexOf('--nights');
const nights = nightsIdx !== -1 ? parseInt(args[nightsIdx + 1], 10) || null : null;

const budgetIdx = args.indexOf('--budget');
const rawBudget = budgetIdx !== -1 ? args[budgetIdx + 1] : 'mid';
const budget = ALLOWED_BUDGETS.has(rawBudget) ? rawBudget : 'mid';

const destArgs = args.filter((a, i) => {
  const flags = ['--lang', '--from', '--date', '--nights', '--budget'];
  if (flags.includes(a)) return false;
  if (flags.includes(args[i - 1])) return false;
  return true;
});
const destination = destArgs.join(' ').trim();

if (!destination) {
  console.error(lang === 'zh'
    ? '用法: node scripts/trip.js <目的地> [--from 出发城市] [--date YYYY-MM-DD] [--nights N] [--budget budget|mid|luxury]'
    : 'Usage: node scripts/trip.js <destination> [--from city] [--date YYYY-MM-DD] [--nights N] [--budget budget|mid|luxury]');
  process.exit(1);
}

const encoded = encodeURIComponent(destination);
const encodedFrom = from ? encodeURIComponent(from) : null;
const returnDate = (date && nights)
  ? new Date(new Date(date).getTime() + nights * 86400000).toISOString().slice(0, 10)
  : null;

const budgetLabelZH = { budget: '经济型', mid: '中档', luxury: '高档' }[budget];
const budgetLabelEN = { budget: 'Budget', mid: 'Mid-range', luxury: 'Luxury' }[budget];
const now = new Date();
const year = now.getFullYear();

if (lang === 'zh') {
  console.log(`请为以下旅行规划完整的行程方案，包括机票、酒店和目的地情报。

目的地：${destination}
${from ? `出发城市：${from}` : '出发城市：未指定（请询问或按最近主要机场）'}
${date ? `出发日期：${date}` : '出发日期：未指定（请查询灵活日期最低价）'}
${nights ? `住宿天数：${nights}晚${returnDate ? `（返程：${returnDate}）` : ''}` : '行程天数：未指定'}
预算档位：${budgetLabelZH}

═══ 第一步：目的地情报 ═══

1. web_search「${destination} 旅游 签证要求 ${year}」
   → 中国护照/目标护照是否需要签证，办理周期和费用

2. web_search「${destination} 汇率 人民币 ${year}」
   → 当前汇率，近期走势（是否适合换汇）

3. web_search「${destination} 旅游安全 ${year} 最新」
   → 目前是否有安全警告或特别注意事项

4. openclaw run newstoday morning "${destination}" --lang zh
   → 获取目的地相关最新新闻（政治/天气/活动）

═══ 第二步：机票比价 ═══

${from ? `5. 打开 https://www.google.com/travel/flights?q=${encodeURIComponent(from + ' to ' + destination)}${date ? `+${date}` : ''}
   → Google Flights：提取最低价、最便宜日期和"订票建议"` : `5. 打开 https://www.google.com/travel/flights?q=${encodeURIComponent('flights to ' + destination)}
   → Google Flights：提取各出发城市到${destination}的最低价`}

6. 打开 https://www.skyscanner.com/transport/flights/${encodedFrom || 'anywhere'}/${encoded}/${date || ''}
   → Skyscanner：提取最低价航班，查看 "Everywhere" 视图找最便宜出发地

7. 打开 https://www.kayak.com/flights/${encodedFrom || 'anywhere'}-${encoded}/${date || 'flexible'}
   → Kayak：查看 Price Forecast（Buy now / Wait）

═══ 第三步：酒店比价 ═══

8. 打开 https://www.booking.com/searchresults.html?ss=${encoded}${date ? `&checkin=${date}` : ''}${returnDate ? `&checkout=${returnDate}` : ''}
   → Booking.com：提取${budgetLabelZH}档位前3家酒店（价格/评分/位置）

9. 打开 https://www.agoda.com/search?q=${encoded}${date ? `&checkIn=${date}` : ''}${returnDate ? `&checkOut=${returnDate}` : ''}
   → Agoda：对比价格，亚洲目的地通常更优惠

═══ 第四步：OTA优惠码 ═══

10. openclaw run couponclaw find "Booking.com" --region all
11. openclaw run couponclaw find "Agoda" --region all
12. openclaw run couponclaw find "Trip.com" --region all
    → 在以上平台价格基础上叠加券码，计算实际到手价

═══ 整合输出 ═══

输出格式：
🌍 TravelHound · ${from ? from + ' → ' : ''}${destination}
━━━━━━━━━━━━━━━━━━━━━━━
📋 ${date || '日期灵活'} · ${nights ? nights + '晚' : '天数待定'} · ${budgetLabelZH}

🛂 目的地情报
签证：[需要/免签/落地签 + 费用]
汇率：1 CNY = X.XX [当地货币]（近期走势：升/贬/稳）
安全：[安全/注意事项/警告]
近期新闻：[1-2条相关资讯]

✈️ 最优机票
[航班] | ¥/$ XXX | [订票建议：立即订/等待]
最便宜日期：± X天调整可省 ¥/$ XXX

🏨 最优酒店（${budgetLabelZH}）
[酒店名] | ¥/$ XXX/晚 | 评分 X.X | [平台]
叠加优惠码后：¥/$ XXX/晚

💰 全程预算估算（${nights || 'X'}晚）
机票：¥/$ XXX（${from || '出发城市'} 往返）
住宿：¥/$ XXX × ${nights || 'X'}晚 = ¥/$ XXX
合计：¥/$ XXX（含已知优惠）

✅ 综合建议
[🟢/🟡/🔴 + 是否是好时机出行 + 1-2句核心理由]
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"机票详情"或"酒店详情"深入查询`);

} else {
  console.log(`Please plan a complete trip to ${destination}, covering flights, hotels, and destination intelligence.

Destination: ${destination}
${from ? `From: ${from}` : 'From: not specified — use nearest major airport or ask'}
${date ? `Departure: ${date}` : 'Departure: not specified — check flexible date lowest fares'}
${nights ? `Duration: ${nights} nights${returnDate ? ` (return: ${returnDate})` : ''}` : 'Duration: not specified'}
Budget tier: ${budgetLabelEN}

═══ Step 1: Destination intelligence ═══

1. web_search "${destination} visa requirements ${year} passport"
   → Check if visa required, processing time, and cost

2. web_search "${destination} exchange rate USD EUR ${year}"
   → Current rate and recent trend (good time to exchange?)

3. web_search "${destination} travel safety advisory ${year}"
   → Active warnings or special precautions

4. openclaw run newstoday morning "${destination}" --lang en
   → Latest news relevant to the destination (political/weather/events)

═══ Step 2: Flight comparison ═══

${from ? `5. Open https://www.google.com/travel/flights?q=${encodeURIComponent(from + ' to ' + destination)}${date ? `+${date}` : ''}
   → Google Flights: lowest fares, cheapest date calendar, booking recommendation` : `5. Open https://www.google.com/travel/flights?q=${encodeURIComponent('flights to ' + destination)}
   → Google Flights: fares from multiple origins to ${destination}`}

6. Open https://www.skyscanner.com/transport/flights/${encodedFrom || 'anywhere'}/${encoded}/${date || ''}
   → Skyscanner: lowest fares including connections; check "Everywhere" view if origin flexible

7. Open https://www.kayak.com/flights/${encodedFrom || 'anywhere'}-${encoded}/${date || 'flexible'}
   → Kayak: Price Forecast (Buy now / Wait) and price history chart

═══ Step 3: Hotel comparison ═══

8. Open https://www.booking.com/searchresults.html?ss=${encoded}${date ? `&checkin=${date}` : ''}${returnDate ? `&checkout=${returnDate}` : ''}
   → Booking.com: top 3 ${budgetLabelEN} hotels (price/rating/location)

9. Open https://www.agoda.com/search?q=${encoded}${date ? `&checkIn=${date}` : ''}${returnDate ? `&checkOut=${returnDate}` : ''}
   → Agoda: compare prices — often cheaper for Asian destinations

═══ Step 4: OTA promo codes ═══

10. openclaw run couponclaw find "Booking.com" --region all
11. openclaw run couponclaw find "Agoda" --region all
12. openclaw run couponclaw find "Trip.com" --region all
    → Stack coupon codes on top of platform prices; calculate effective final price

═══ Output ═══

Output format:
🌍 TravelHound · ${from ? from + ' → ' : ''}${destination}
━━━━━━━━━━━━━━━━━━━━━━━
📋 ${date || 'Flexible dates'} · ${nights ? nights + ' nights' : 'duration TBD'} · ${budgetLabelEN}

🛂 Destination intelligence
Visa: [required / visa-free / on-arrival + fee]
Exchange rate: 1 USD = X.XX [local currency] (trend: rising/falling/stable)
Safety: [safe / advisory / warning]
Latest news: [1-2 relevant headlines]

✈️ Best flight
[Flight] | $XXX | [Booking advice: buy now / wait]
Cheapest nearby date: ±X days saves $XXX

🏨 Best hotel (${budgetLabelEN})
[Hotel name] | $XXX/night | Rating X.X | [Platform]
After coupon code: $XXX/night effective

💰 Total trip budget estimate (${nights || 'X'} nights)
Flights: $XXX (${from || 'origin'} round trip)
Hotels: $XXX × ${nights || 'X'} nights = $XXX
Total: $XXX (after known savings)

✅ Overall verdict
[🟢/🟡/🔴 + is this a good time to go + 1-2 key reasons]
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "flight details" or "hotel details" to dig deeper`);
}
