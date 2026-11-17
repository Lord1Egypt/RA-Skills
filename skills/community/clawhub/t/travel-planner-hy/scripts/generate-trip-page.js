#!/usr/bin/env node
'use strict';
// Static, escaped itinerary HTML. This renderer performs no network or subprocess calls.
const { CSP, escapeHtml: e, validateTrip, validatePlatformUrl, parseTripJson, readTrip, writeOutput } = require('./safety');
const { generateQRBase64 } = require('./qrcode');
const mockData = require('./mock-data');
function getCSS() {
  return `
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #333; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
.header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 40px; border-radius: 16px; margin-bottom: 24px; text-align: center; }
.header h1 { font-size: 28px; margin-bottom: 8px; }
.header .subtitle { font-size: 14px; opacity: 0.9; }
.main-grid { display: grid; grid-template-columns: 1fr 360px; gap: 24px; }
@media (max-width: 768px) { .main-grid { grid-template-columns: 1fr; } }
.section { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.section h2 { font-size: 18px; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 2px solid #667eea; color: #444; display: flex; align-items: center; gap: 8px; }
.itinerary-item { padding: 12px 0; border-bottom: 1px dashed #eee; display: flex; gap: 12px; }
.itinerary-item:last-child { border-bottom: none; }
.itinerary-item .time { font-weight: 600; color: #667eea; min-width: 80px; font-size: 14px; }
.itinerary-item .content { flex: 1; font-size: 14px; line-height: 1.6; }
.itinerary-item .content .highlight { color: #e74c3c; font-weight: 500; }
.qr-section { text-align: center; }
.qr-section img { max-width: 280px; margin: 16px 0; border-radius: 8px; }
.qr-section .total-price { font-size: 24px; font-weight: 700; color: #e74c3c; margin: 8px 0; }
.qr-section .price-label { font-size: 13px; color: #888; }
.btn-book { display: inline-block; padding: 10px 24px; background: #667eea; color: #fff; text-decoration: none; border-radius: 8px; font-size: 14px; margin: 8px 4px; }
.btn-book:hover { background: #5a6fd6; }
.tag { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; margin: 2px; background: #eef2ff; color: #667eea; }
.tag.free { background: #e8f5e9; color: #2e7d32; }
.tag.paid { background: #fff3e0; color: #e65100; }
.budget-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.budget-table th, .budget-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; }
.budget-table th { background: #f8f9fa; font-weight: 600; color: #555; }
.budget-table tr:last-child td { font-weight: 700; color: #e74c3c; }
.tips-list { list-style: none; padding: 0; }
.tips-list li { padding: 6px 0; font-size: 14px; color: #555; display: flex; align-items: flex-start; gap: 8px; }
.tips-list li::before { content: "💡"; flex-shrink: 0; }
.attraction-card { padding: 12px; margin: 8px 0; border: 1px solid #eee; border-radius: 8px; font-size: 14px; }
.attraction-card .name { font-weight: 600; font-size: 15px; }
.attraction-card .info { color: #666; margin-top: 4px; line-height: 1.6; }
.attraction-card .reason { color: #667eea; margin-top: 4px; font-size: 13px; }
`;
}


async function getHTML(raw) {
  validateTrip(raw);
  // Clone before asynchronous QR work so caller mutations cannot cross the validation boundary.
  const d = JSON.parse(JSON.stringify(raw));
  const zh = d.language === 'zh-CN';
  const l = (cn, en) => zh ? cn : en;
  const money = value => value == null ? l('待核实','Unknown') : '¥' + value;
  const label = l('旅行方案','Travel plan');
  const links = await Promise.all((d.platformUrls || []).map(async value => {
    const url = validatePlatformUrl(value);
    const qr = await generateQRBase64(url);
    return `<div><img src="${e(qr)}" alt="${l('平台首页二维码','Platform homepage QR')}"><p><a class="btn-book" href="${e(url)}" target="_blank" rel="noopener noreferrer">${e(new URL(url).hostname)}</a></p></div>`;
  }));
  return `<!DOCTYPE html>
<html lang="${zh ? 'zh-CN' : 'en'}"><head><meta charset="UTF-8">${CSP}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${e(d.title || d.destination + ' ' + label)}</title><style>${getCSS()}</style></head>
<body><div class="container"><div class="header">
<h1>🗺️ ${e(d.title || d.destination + ' ' + label)}</h1>
<div class="subtitle">${e(d.subtitle || `${d.days} ${l('天','days')} · ${d.travelers} ${l('人','travelers')} · ${money(d.budget)}`)}</div>
${d.mock ? `<p role="note">${l('模拟演示数据 · 非实时报价','MOCK DATA · Not live prices')}</p>` : ''}
</div><div class="main-grid"><div class="left-column">
<div class="section"><h2>💰 ${l('预算概览','Budget overview')}</h2><table class="budget-table">
<tr><th>${l('项目','Item')}</th><th>${l('金额','Amount')}</th><th>${l('占比','Share')}</th></tr>
${(d.costs?.items || []).map(item => `<tr><td>${e(item.name)}</td><td>${money(item.amount)}</td><td>${e(item.pct)}</td></tr>`).join('')}
<tr><td>${l('预估合计','Estimated total')}</td><td>${money(d.costs?.total)}</td><td></td></tr></table></div>
${d.attractions?.length ? `<div class="section"><h2>🏆 ${l('推荐景点','Attractions')}</h2>
${d.attractions.map((a,i) => `<div class="attraction-card"><div class="name">${i+1}. ${e(a.name)}</div>
<div class="info">${a.type.map(t => `<span class="tag">${e(t)}</span>`).join('')}
<span class="tag">${a.ticketPrice === 0 ? l('免费','Free') : money(a.ticketPrice)}</span> ⭐ ${a.rating ?? l('待核实','Unknown')}</div>
<div class="info">${e(a.estimatedDuration)} | ${e(a.openingHours)}</div>
<div class="info">${e(a.description)}</div><div class="reason">${e(a._reason)}</div></div>`).join('')}</div>` : ''}
${(d.itinerary || []).map((day,i) => `<div class="section"><h2>🗓️ ${l('第','Day ')}${i+1}${l('天','')} — ${e(day.date)}</h2>
${day.items.map(item => `<div class="itinerary-item"><div class="time">${e(item.time)}</div><div class="content">${e(item.icon || '📍')} <strong>${e(item.title)}</strong>
${item.detail ? '<br>' + e(item.detail) : ''}${item.cost ? '<br><span class="highlight">' + e(item.cost) + '</span>' : ''}</div></div>`).join('')}
${day.notes ? '<p>' + e(day.notes) + '</p>' : ''}</div>`).join('')}
${d.hotels?.length ? `<div class="section"><h2>🏨 ${l('住宿推荐','Hotels')}</h2>
${d.hotels.map(h => `<div class="attraction-card"><div class="name">${e(h.name)}</div><div class="info">${e(h.area)} | ⭐ ${h.rating ?? l('待核实','Unknown')} | ${money(h.price)} / ${l('晚','night')}</div>
<div class="info">${e(h.features)}</div><div class="info">${e(h.distance)}</div></div>`).join('')}</div>` : ''}
${d.tips?.length ? `<div class="section"><h2>💡 ${l('出行提示','Travel tips')}</h2><ul class="tips-list">${d.tips.map(t => '<li>'+e(t)+'</li>').join('')}</ul></div>` : ''}
</div><div class="right-column">
${links.length ? `<div class="section qr-section"><h2>🔗 ${l('平台公开首页','Platform homepages')}</h2>
<p>${l('以下链接和二维码仅打开第三方公开首页。本页不创建订单或收款，请在平台内自行搜索。','These links and QR codes open third-party public homepages only. This page creates no orders and collects no payments. Search independently on the platform.')}</p>
${links.join('')}</div>` : ''}
<div class="section"><h2>📋 ${l('行程信息','Trip details')}</h2>
<p>${l('目的地','Destination')}: ${e(d.destination)}</p><p>${l('天数','Days')}: ${d.days}</p><p>${l('人数','Travelers')}: ${d.travelers}</p><p>${l('预算','Budget')}: ${money(d.budget)}</p>
${(d.preferences || []).map(p => `<span class="tag">${e(p)}</span>`).join('')}
${d.transport ? Object.values(d.transport).map(value => '<p>'+e(value)+'</p>').join('') : ''}</div>
</div></div></div></body></html>`;
}
function generateMockTripData() {
  const city = '重庆';
  const days = 3;
  const travelers = 2;
  const budget = 5000;
  const preferences = ['美食', '自然', '网红打卡'];

  // 获取景点并评分
  let attractions = mockData.getMockAttractions(city);
  attractions = mockData.filterByPreference(attractions, preferences);
  attractions = mockData.filterByBudget(attractions, budget, days);

  // 生成推荐理由
  attractions = attractions.map(a => {
    let reasons = [];
    if (a.ticketPrice === 0) reasons.push('免费开放，性价比高');
    if (a.rating >= 4.5) reasons.push('评分' + a.rating + '，口碑优秀');
    reasons.push('与您偏好的' + a.type.join(',') + '风格相符');
    a._reason = reasons.join('；');
    return a;
  });

  // 每日行程
  const itinerary = [
    {
      date: '第1天（到达日）',
      items: [
        { time: '08:00-09:00', icon: '🍳', title: '早餐', detail: '酒店/当地特色早餐', cost: '人均15-20元' },
        { time: '09:00-10:30', icon: '🚄', title: '抵达重庆', detail: '高铁/飞机到达，前往酒店办理入住', cost: '' },
        { time: '10:30-12:00', icon: '🎯', title: '解放碑', detail: '重庆标志性商圈，观抗战胜利纪功碑', cost: '免费' },
        { time: '12:00-13:30', icon: '🍜', title: '午餐', detail: '八一好吃街品尝重庆小吃', cost: '人均30-50元' },
        { time: '13:30-17:30', icon: '🎯', title: '磁器口古镇', detail: '千年古镇，品陈麻花、逛古街', cost: '免费' },
        { time: '17:30-18:30', icon: '🛌', title: '回酒店休息', detail: '' },
        { time: '18:30-20:00', icon: '🍽️', title: '晚餐', detail: '枇杷园火锅（老字号，推荐毛肚火锅）', cost: '人均80-120元' },
        { time: '20:00-22:00', icon: '🌙', title: '洪崖洞夜景', detail: '观赏重庆最美夜景，吊脚楼灯光秀', cost: '免费' }
      ],
      notes: '重庆夏季炎热，建议随身带水；洪崖洞亮灯时间为19:30-23:00'
    },
    {
      date: '第2天（全日游）',
      items: [
        { time: '08:00-09:00', icon: '🍳', title: '早餐', detail: '酒店早餐' },
        { time: '09:00-10:00', icon: '🚇', title: '李子坝轻轨站', detail: '网红轻轨穿楼打卡', cost: '免费' },
        { time: '10:00-12:00', icon: '🎯', title: '三峡博物馆', detail: '了解三峡文化与重庆历史（周一闭馆）', cost: '免费，需预约' },
        { time: '12:00-13:30', icon: '🍜', title: '午餐', detail: '中山四路附近餐馆', cost: '人均30-50元' },
        { time: '13:30-14:00', icon: '☕', title: '午休', detail: '' },
        { time: '14:00-17:00', icon: '🎯', title: '长江索道', detail: '空中俯瞰长江两岸风光', cost: '¥30/人往返' },
        { time: '17:00-18:30', icon: '🎯', title: '南山一棵树观景台', detail: '360度俯瞰重庆全景', cost: '¥30/人' },
        { time: '18:30-20:30', icon: '🍽️', title: '晚餐', detail: '南山泉水鸡一条街', cost: '人均60-100元' }
      ],
      notes: '三峡博物馆周一闭馆，请避开；南山观景台建议18:00前到达占位看日落'
    },
    {
      date: '第3天（返程日）',
      items: [
        { time: '07:00-08:00', icon: '🍳', title: '早餐 + 退房', detail: '酒店早餐，办理退房寄存行李' },
        { time: '08:00-10:00', icon: '🎯', title: '湖广会馆', detail: '清代移民会馆建筑群', cost: '¥30/人' },
        { time: '10:00-12:00', icon: '🛍️', title: '解放碑商圈购物', detail: '购买特产伴手礼', cost: '视个人情况' },
        { time: '12:00-13:00', icon: '🍜', title: '午餐', detail: '重庆小面/豆花饭', cost: '人均15-25元' },
        { time: '13:00-14:00', icon: '🎒', title: '取行李前往车站', detail: '' },
        { time: '14:00', icon: '🚄', title: '返程出发', detail: '前往重庆北站/机场' }
      ],
      notes: '最后一班高铁约21:00，飞机请预留2小时到机场'
    }
  ];

  // 住宿推荐
  const hotels = mockData.getMockHotels(city);

  // 交通信息
  const transport = mockData.getMockTransport(city);

  // 预算明细
  const costs = {
    items: [
      { name: '🚄 交通（高铁往返）', amount: 300, pct: '6%' },
      { name: '🏨 住宿（2晚）', amount: 1600, pct: '32%' },
      { name: '🎫 门票', amount: 180, pct: '4%' },
      { name: '🍜 餐饮', amount: 1200, pct: '24%' },
      { name: '🚕 当地交通', amount: 300, pct: '6%' },
      { name: '📦 其他', amount: 420, pct: '8%' }
    ],
    total: 4000
  };

  // 温馨提示
  const tips = [
    '重庆7月平均气温28-35°C，建议携带防晒霜、遮阳帽、便携风扇',
    '重庆饮食以麻辣为主，肠胃敏感建议备好肠胃药',
    '景点间推荐地铁出行（下载"渝畅行"APP扫码乘车）',
    '洪崖洞、长江索道等热门景点建议非高峰时段前往',
    '建议购买旅游意外险，出行前告知家人行程安排'
  ];

  return {
    title: `重庆${days}日游旅行方案`,
    subtitle: `${days}天 · ${travelers}人 · 预算¥${budget}`,
    destination: city,
    days,
    travelers,
    budget,
    language: 'zh-CN',
    mock: true,
    platformUrls: ['https://www.tuniu.com/'],
    preferences: ['美食', '自然', '网红打卡', '人文'],
    attractions,
    itinerary,
    hotels,
    transport,
    costs,
    tips
  };
}


async function main(args = process.argv.slice(2)) {
  let input, mock = false, language;
  for (let i=0; i<args.length; i++) {
    if (args[i] === '--mock') mock = true;
    else if (args[i] === '--input') { input = args[++i]; if (!input || input.startsWith('--')) throw new Error('--input requires a JSON filename.'); }
    else if (args[i] === '--language') { language = args[++i]; if (!['zh-CN','en'].includes(language)) throw new Error('Use --language zh-CN or en.'); }
    else throw new Error('Unsupported argument. Use --mock or --input FILE; open results manually.');
  }
  if (mock && input) throw new Error('Choose either --mock or --input.');
  const data = mock ? generateMockTripData() : input ? readTrip(input) : parseTripJson(process.env.TRIP_DATA);
  if (language) data.language = language;
  const html = await getHTML(data);
  const output = writeOutput(html, 'trip', 'html');
  console.log('HTML saved:', output);
  return output;
}
if (require.main === module) main().catch(e => { console.error(e.message); process.exitCode = 1; });
module.exports = { getHTML, generateMockTripData, main };
