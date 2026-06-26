#!/usr/bin/env node
'use strict';
/**
 * TravelHound — 机票比价 + 最佳订票时机
 * 用法: node scripts/flights.js <出发地> <目的地> [--date YYYY-MM-DD] [--return YYYY-MM-DD] [--class economy|business] [--passengers N] [--lang zh|en]
 */

const ALLOWED_CLASSES = new Set(['economy', 'business', 'first']);

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';

const dateIdx = args.indexOf('--date');
const date = dateIdx !== -1 ? args[dateIdx + 1] : null;

const returnIdx = args.indexOf('--return');
const returnDate = returnIdx !== -1 ? args[returnIdx + 1] : null;

const classIdx = args.indexOf('--class');
const rawClass = classIdx !== -1 ? args[classIdx + 1] : 'economy';
const cabinClass = ALLOWED_CLASSES.has(rawClass) ? rawClass : 'economy';

const passIdx = args.indexOf('--passengers');
const passengers = passIdx !== -1 ? parseInt(args[passIdx + 1], 10) || 1 : 1;

const locationArgs = args.filter((a, i) => {
  const flags = ['--lang', '--date', '--return', '--class', '--passengers'];
  if (flags.includes(a)) return false;
  if (flags.includes(args[i - 1])) return false;
  return true;
});

const [from = '', to = ''] = locationArgs;

if (!from || !to) {
  console.error(lang === 'zh'
    ? '用法: node scripts/flights.js <出发地> <目的地> [--date YYYY-MM-DD] [--return YYYY-MM-DD]'
    : 'Usage: node scripts/flights.js <from> <to> [--date YYYY-MM-DD] [--return YYYY-MM-DD]');
  process.exit(1);
}

const encFrom = encodeURIComponent(from);
const encTo = encodeURIComponent(to);
const encQuery = encodeURIComponent(`${from} to ${to}`);
const encQueryZH = encodeURIComponent(`${from}到${to}机票`);

const dateNote = date ? (lang === 'zh' ? `出发日期：${date}` : `Departure: ${date}`) : (lang === 'zh' ? '出发日期：未指定（请查询近期最低价区间）' : 'Departure: not specified — look for lowest fare window');
const returnNote = returnDate ? (lang === 'zh' ? `返程日期：${returnDate}` : `Return: ${returnDate}`) : '';
const tripType = returnDate ? (lang === 'zh' ? '往返' : 'Round trip') : (lang === 'zh' ? '单程' : 'One way');
const classNote = lang === 'zh'
  ? ({ economy: '经济舱', business: '商务舱', first: '头等舱' }[cabinClass])
  : ({ economy: 'Economy', business: 'Business', first: 'First' }[cabinClass]);

if (lang === 'zh') {
  console.log(`请为以下行程查询机票价格并分析最佳订票时机。

行程：${from} → ${to}（${tripType} · ${classNote} · ${passengers}人）
${dateNote}${returnNote ? '\n' + returnNote : ''}

使用 browser 工具依次导航以下页面，提取真实票价：

1. 打开 https://www.google.com/travel/flights?q=${encQueryZH}
   → Google Flights：提取各航空公司价格、最便宜日期（日历视图），以及页面底部的"价格走势"和"订票建议"（Buy now / Wait）

2. 打开 https://www.skyscanner.com/transport/flights/${encFrom}/${encTo}/${date || ''}
   → Skyscanner：提取最低价航班（含中转）、价格预警提示（当月最低 / 偏高），记录前3条推荐

3. 打开 https://www.kayak.com/flights/${encFrom}-${encTo}/${date || 'flexible'}
   → Kayak：重点查看 "Price Forecast" 模块（显示 Buy / Wait 建议和理由），以及 Price History 图表

4. 打开 https://flights.trip.com/flights/list?depCityName=${encFrom}&arrCityName=${encTo}${date ? `&flightDate=${date}` : ''}
   → 携程/Trip.com：提取含中文航司的价格，尤其是国内航线和亚洲航线通常比国际平台便宜

5. web_search「${from} ${to} 机票 ${date || '近期'} 最低价 航班」
   → 补充获取近期促销航班信息

【历史价格核查】
6. 在步骤1 Google Flights 中查看"价格图表"，判断当前价格是否处于历史低位
7. web_search「${from} to ${to} flights cheap months best time to fly」→ 了解该航线的淡旺季规律

【判断标准】
- 🟢 立即订：当前价格 ≤ 近3个月均价的 90%，或 Google Flights/Kayak 明确显示 "Buy now"
- 🟡 再等等：价格高于均价但有下降趋势，或距出发超过6周仍有降价空间
- 🔴 贵，考虑替代：旺季/节假日价格，建议改签日期或换出发城市

输出格式：
✈️ TravelHound · ${from} → ${to}
━━━━━━━━━━━━━━━━━━━━━━━
📋 行程：${tripType} · ${classNote} · ${passengers}人 · ${date || '日期灵活'}${returnDate ? ' ~ ' + returnDate : ''}

💰 各平台票价对比
平台            | 最低价  | 航班号/航司 | 飞行时长 | 中转
Google Flights  | ¥/$ XXX |             |          |
Skyscanner      | ¥/$ XXX |             |          |
Kayak           | ¥/$ XXX |             |          |
携程/Trip.com   | ¥/$ XXX |             |          |

📊 价格分析
当前价格位置：历史低位 / 正常 / 偏高
Kayak 预测：Buy now / Wait（原因）
最便宜出发日：± X天调整可省 ¥/$ XXX

✅ 订票建议
[🟢/🟡/🔴 + 1-2句理由 + 推荐平台]

🎟️ 订票优惠码（运行 CouponClaw 查询）：
  openclaw run couponclaw find "Trip.com" --region all
  openclaw run couponclaw find "Skyscanner" --region all
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"查酒店"继续规划住宿 · 回复"全程规划"一站搞定`);

} else {
  console.log(`Please research flight prices for the following itinerary and advise on the best time to book.

Route: ${from} → ${to} (${tripType} · ${classNote} · ${passengers} pax)
${dateNote}${returnNote ? '\n' + returnNote : ''}

Use the browser tool to navigate each page and extract real fares:

1. Open https://www.google.com/travel/flights?q=${encQuery}
   → Google Flights: extract prices per airline, cheapest date calendar, and the "Price insights" / "Buy now vs Wait" recommendation at the bottom

2. Open https://www.skyscanner.com/transport/flights/${encFrom}/${encTo}/${date || ''}
   → Skyscanner: extract lowest fares (incl. connections), price alert badge (lowest this month / high), top 3 results

3. Open https://www.kayak.com/flights/${encFrom}-${encTo}/${date || 'flexible'}
   → Kayak: focus on the "Price Forecast" module (Buy / Wait + reason) and Price History chart

4. Open https://uk.trip.com/flights/list?depCityName=${encFrom}&arrCityName=${encTo}${date ? `&flightDate=${date}` : ''}
   → Trip.com: often has lower fares for Asian routes and Chinese carriers

5. web_search "cheap flights ${from} to ${to} ${date || 'next month'} deals"
   → Supplement with any current fare sales

[Price history check]
6. In Google Flights from step 1, check the price chart — is the current price at/near a low?
7. web_search "${from} to ${to} cheapest months best time to fly" → understand seasonal pricing patterns

[Verdict criteria]
- 🟢 Book now: current price ≤ 90% of 3-month average, or Google Flights/Kayak says "Buy now"
- 🟡 Wait: price above average but trending down, or 6+ weeks out with room to drop
- 🔴 Expensive — consider alternatives: peak season/holiday pricing; suggest date shift or alternate origin

Output format:
✈️ TravelHound · ${from} → ${to}
━━━━━━━━━━━━━━━━━━━━━━━
📋 Trip: ${tripType} · ${classNote} · ${passengers} pax · ${date || 'flexible dates'}${returnDate ? ' ~ ' + returnDate : ''}

💰 Price comparison
Platform        | Lowest fare | Airline     | Duration | Stops
Google Flights  | $XXX        |             |          |
Skyscanner      | $XXX        |             |          |
Kayak           | $XXX        |             |          |
Trip.com        | $XXX        |             |          |

📊 Price analysis
Current price position: near low / average / high
Kayak forecast: Buy now / Wait (reason)
Cheapest nearby date: ±X days saves $XXX

✅ Booking recommendation
[🟢/🟡/🔴 + 1-2 sentence rationale + recommended platform]

🎟️ OTA promo codes (run CouponClaw):
  openclaw run couponclaw find "Trip.com" --region all
  openclaw run couponclaw find "Skyscanner" --region all
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "find hotels" to continue planning · Reply "full trip" for combined itinerary`);
}
