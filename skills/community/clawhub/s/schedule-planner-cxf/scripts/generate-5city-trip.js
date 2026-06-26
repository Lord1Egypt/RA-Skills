const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const TUNIU_API_KEY = process.env.TUNIU_API_KEY || '';
const tuniuPath = path.join(
  process.env.APPDATA || process.env.HOME || '',
  'npm', 'node_modules', 'tuniu-cli', 'bin', 'tuniu.js'
);

function callTuniu(server, tool, params) {
  const result = spawnSync('node', [tuniuPath, 'call', server, tool, '-a', JSON.stringify(params)], {
    env: { ...process.env, TUNIU_API_KEY },
    encoding: 'utf8',
    stdio: ['pipe', 'pipe', 'pipe'],
    timeout: 30000,
    shell: false
  });

  try {
    const parsed = JSON.parse(result.stdout);
    if (parsed.result?.structuredContent?.result) {
      return JSON.parse(parsed.result.structuredContent.result);
    }
    if (parsed.result?.content?.[0]?.text) {
      return JSON.parse(parsed.result.content[0].text);
    }
    return parsed;
  } catch (e) {
    return null;
  }
}

// Query trains
function queryTrain(from, to, date) {
  console.log(`${from} -> ${to} (${date})`);
  const result = callTuniu('train', 'searchLowestPriceTrain', {
    departureCityName: from,
    arrivalCityName: to,
    departureDate: date
  });

  const trains = result?.data || [];
  const gaotie = trains.filter(t => t.trainType === 'high-speed' || t.trainNum?.startsWith('G') || t.trainNum?.startsWith('D'));
  return (gaotie.length > 0 ? gaotie : trains).slice(0, 3).map(t => ({
    trainNo: t.trainNum,
    departureTime: t.departureTime?.split(' ')[1] || t.departureTime,
    arrivalTime: t.arrivalTime?.split(' ')[1] || t.arrivalTime,
    duration: t.duration,
    price: parseFloat(t.price?.edzPrice || t.price?.ydzPrice || t.price?.wzPrice || 0),
    seatType: t.price?.edzPrice ? '二等座' : '硬座'
  }));
}

// Query flights
function queryFlight(from, to, date) {
  console.log(`${from} -> ${to} (${date})`);
  const result = callTuniu('flight', 'searchLowestPriceFlight', {
    departureCityName: from,
    arrivalCityName: to,
    departureDate: date
  });

  const flights = result?.data || [];
  return flights.slice(0, 3).map(f => ({
    flightNo: f.flightNumber,
    airline: f.airlineCompany,
    departureTime: f.departureTime?.split(' ')[1] || f.departureTime,
    arrivalTime: f.arrivalTime?.split(' ')[1] || f.arrivalTime,
    duration: f.flyTime || f.totalDuration,
    price: parseFloat(f.basePrice || 0),
    departureAirport: f.departureAirport,
    arrivalAirport: f.arrivalAirport
  }));
}

// Query hotels
function queryHotel(city, checkIn, checkOut) {
  console.log(`Hotel: ${city} (${checkIn})`);
  const result = callTuniu('hotel', 'tuniu_hotel_search', {
    cityName: city,
    checkIn: checkIn,
    checkOut: checkOut,
    pageNum: 1
  });

  const hotels = result?.hotels || [];
  return hotels.slice(0, 3).map(h => ({
    hotelId: String(h.hotelId),
    name: h.hotelName,
    address: h.address,
    business: h.business,
    price: h.lowestPrice,
    rating: h.commentScore,
    starName: h.starName,
    meal: h.meal,
    refund: h.refund
  }));
}

// Main flow
console.log('Starting 5-city business trip query...\n');

const routes = [
  { type: 'train', from: '杭州', to: '南京', date: '2026-05-04', options: [] },
  { type: 'flight', from: '南京', to: '上海', date: '2026-05-05', options: [] },
  { type: 'train', from: '上海', to: '苏州', date: '2026-05-06', options: [] },
  { type: 'train', from: '苏州', to: '北京', date: '2026-05-07', options: [] },
  { type: 'flight', from: '北京', to: '杭州', date: '2026-05-08', options: [] }
];

const hotels = [
  { city: '南京', checkIn: '2026-05-04', checkOut: '2026-05-05', options: [] },
  { city: '上海', checkIn: '2026-05-05', checkOut: '2026-05-06', options: [] },
  { city: '苏州', checkIn: '2026-05-06', checkOut: '2026-05-07', options: [] },
  { city: '北京', checkIn: '2026-05-07', checkOut: '2026-05-08', options: [] }
];

// Query routes
routes.forEach(r => {
  if (r.type === 'train') {
    r.options = queryTrain(r.from, r.to, r.date);
  } else {
    r.options = queryFlight(r.from, r.to, r.date);
  }
});

// Query hotels
hotels.forEach(h => {
  h.options = queryHotel(h.city, h.checkIn, h.checkOut);
});

// Save data
const desktopPath = path.join(process.env.USERPROFILE || '~', 'Desktop', '5city-trip.json');
const data = { routes, hotels };
fs.writeFileSync(desktopPath, JSON.stringify(data, null, 2));
console.log('\nData saved to desktop');

// Generate HTML
const html = generateHTML(data);
const htmlPath = path.join(process.env.USERPROFILE || '~', 'Desktop', '5city-trip.html');
fs.writeFileSync(htmlPath, html);
console.log(`Trip page generated: ${htmlPath}`);

// Open browser via spawnSync (safe)
const openResult = spawnSync('powershell', [
  '-NoProfile', '-Command', 'Start-Process', htmlPath
], { stdio: 'pipe', shell: false, timeout: 10000 });
if (openResult.error) {
  console.log('Auto-open failed, please open manually:', htmlPath);
}

function generateHTML(data) {
  const routesHtml = data.routes.map((r, i) => {
    const optionsHtml = r.options.map((opt, j) => `
      <tr class="option-row">
        <td>${opt.flightNo || opt.trainNo}</td>
        <td>${opt.departureTime}</td>
        <td>${opt.arrivalTime}</td>
        <td>${opt.duration}</td>
        <td class="price">¥${opt.price}</td>
        <td>${opt.seatType || ''}${opt.departureAirport ? `<br><small>${opt.departureAirport}→${opt.arrivalAirport}</small>` : ''}</td>
        <td>${j === 0 ? '推荐' : ''}</td>
      </tr>
    `).join('');

    return `
      <div class="card">
        <h3>${r.type === 'train' ? '🚄' : '✈️'} 第${i+1}段：${r.from} → ${r.to} <span class="date">${r.date}</span></h3>
        <table>
          <tr><th>车次/航班</th><th>出发</th><th>到达</th><th>时长</th><th>价格</th><th>席位/机场</th><th>推荐</th></tr>
          ${optionsHtml}
        </table>
      </div>
    `;
  }).join('');

  const hotelsHtml = data.hotels.map((h, i) => {
    const optionsHtml = h.options.map((opt, j) => `
      <tr class="option-row">
        <td>${opt.name}</td>
        <td>${opt.business}</td>
        <td>${opt.starName}</td>
        <td class="price">¥${opt.price}</td>
        <td>${opt.rating}分</td>
        <td>${opt.meal} | ${opt.refund}</td>
        <td>${j === 0 ? '推荐' : ''}</td>
      </tr>
    `).join('');

    return `
      <div class="card">
        <h3>🏣 ${h.city}酒店 <span class="date">${h.checkIn}入住</span></h3>
        <table>
          <tr><th>酒店名称</th><th>位置</th><th>类型</th><th>价格</th><th>评分</th><th>餐饮/取消</th><th>推荐</th></tr>
          ${optionsHtml}
        </table>
      </div>
    `;
  }).join('');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>5 城商务出差行程单</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
    .container { max-width: 1200px; margin: 0 auto; }
    .header { background: white; border-radius: 16px; padding: 30px; margin-bottom: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    .header h1 { color: #333; font-size: 28px; margin-bottom: 10px; }
    .header .info { display: flex; gap: 30px; margin-top: 20px; flex-wrap: wrap; }
    .header .info-item { background: #f8f9fa; padding: 12px 20px; border-radius: 8px; }
    .card { background: white; border-radius: 16px; padding: 25px; margin-bottom: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); }
    .card h3 { color: #333; font-size: 18px; margin-bottom: 15px; }
    .card h3 .date { color: #667eea; font-size: 14px; font-weight: normal; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #f8f9fa; padding: 12px; text-align: left; font-size: 13px; color: #666; font-weight: 600; }
    td { padding: 12px; border-bottom: 1px solid #eee; font-size: 14px; color: #333; }
    .price { color: #e74c3c; font-weight: 600; font-size: 16px; }
    .summary { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
    .summary-item { color: white; padding: 20px; border-radius: 12px; text-align: center; }
    .summary-item .value { font-size: 32px; font-weight: 700; margin-top: 8px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>5 城商务出差行程单</h1>
      <p>杭州 → 南京 → 上海 → 苏州 → 北京 → 杭州</p>
      <div class="info">
        <div class="info-item"><label>出发日期</label><value>2026-05-04</value></div>
        <div class="info-item"><label>返回日期</label><value>2026-05-08</value></div>
        <div class="info-item"><label>总天数</label><value>5 天 4 晚</value></div>
      </div>
    </div>

    <div style="color: white; margin-bottom: 15px; font-size: 18px;">交通安排</div>
    ${routesHtml}

    <div style="color: white; margin-bottom: 15px; font-size: 18px;">酒店安排</div>
    ${hotelsHtml}

    <div class="summary">
      <h2>费用总计</h2>
      <div class="summary-grid">
        <div class="summary-item" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
          <label>交通费用</label>
          <div class="value">¥${data.routes.reduce((sum, r) => sum + (r.options[0]?.price || 0), 0)}</div>
        </div>
        <div class="summary-item" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
          <label>酒店费用</label>
          <div class="value">¥${data.hotels.reduce((sum, h) => sum + (h.options[0]?.price || 0), 0)}</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>`;
}