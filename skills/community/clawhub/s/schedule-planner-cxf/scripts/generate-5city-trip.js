'use strict';
const { CSP, escapeHtml, readJson, writeOutput, object, array, text, number } = require('./lib/safety');
function validateComparison(raw) {
  object(raw, ['routes', 'hotels', 'mock', 'startDate'], 'comparison');
  if (typeof raw.mock !== 'boolean') throw new Error('Comparison requires a mock flag.');
  array(raw.routes, 'routes', 30); array(raw.hotels, 'hotels', 30);
  const optionFields = ['trainNo', 'flightNo', 'airline', 'departureTime', 'arrivalTime', 'duration', 'price', 'seatType', 'departureAirport', 'arrivalAirport', 'hotelId', 'name', 'address', 'business', 'rating', 'starName', 'meal', 'refund', 'reviewCount'];
  for (const row of [...raw.routes, ...raw.hotels]) {
    const isRoute = raw.routes.includes(row);
    object(row, isRoute ? ['type', 'from', 'to', 'date', 'options'] : ['city', 'checkIn', 'checkOut', 'options'], 'comparison row');
    if (isRoute && !['train', 'flight'].includes(row.type)) throw new Error('Unsupported route type.');
    for (const [key, value] of Object.entries(row)) if (key !== 'options') text(value, key, true);
    array(row.options, 'options', 10);
    for (const opt of row.options) {
      object(opt, optionFields, 'option');
      for (const [key, value] of Object.entries(opt)) {
        if (value === undefined || (key === 'price' && value === null)) continue;
        if (['price', 'rating', 'reviewCount'].includes(key)) number(value, key); else text(value, key);
      }
    }
  }
  function escape(value) {
    if (typeof value === 'string') return escapeHtml(value);
    if (Array.isArray(value)) return value.map(escape);
    if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k,v]) => [k,escape(v)]));
    return value;
  }
  return escape(raw);
}
function main(args = process.argv.slice(2)) {
  if (args.length !== 2 || args[0] !== '--input') throw new Error('Usage: node scripts/generate-5city-trip.js --input QUERY_RESULT.json');
  const html = generateHTML(readJson(args[1]));
  console.log('Comparison saved:', writeOutput(html, 'comparison'));
}
function generateHTML(raw) {
  const data = validateComparison(raw);
  const routesHtml = data.routes.map((r, i) => {
    const optionsHtml = r.options.map((opt, j) => `
      <tr class="option-row">
        <td>${opt.flightNo || opt.trainNo}</td>
        <td>${opt.departureTime}</td>
        <td>${opt.arrivalTime}</td>
        <td>${opt.duration}</td>
        <td class="price">${opt.price == null ? '未知' : `¥${opt.price}`}</td>
        <td>${opt.seatType || ''}${opt.departureAirport ? `<br><small>${opt.departureAirport}→${opt.arrivalAirport}</small>` : ''}</td>
        <td>${j === 0 ? '首个返回结果' : ''}</td>
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
        <td class="price">${opt.price == null ? '未知' : `¥${opt.price}`}</td>
        <td>${opt.rating}分</td>
        <td>${opt.meal} | ${opt.refund}</td>
        <td>${j === 0 ? '首个返回结果' : ''}</td>
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
  ${CSP}
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
      <h1>多城市行程比价</h1>
      ${data.mock ? '<p>模拟数据 · 非实时报价</p>' : '<p>查询报价仅供参考，未预订</p>'}
      <p>${data.routes.map(r => `${r.from} → ${r.to} (${r.date})`).join(' / ')}</p>
    </div>

    <div style="color: white; margin-bottom: 15px; font-size: 18px;">交通安排</div>
    ${routesHtml}

    <div style="color: white; margin-bottom: 15px; font-size: 18px;">酒店安排</div>
    ${hotelsHtml}

    <div class="summary">
      <h2>已知报价小计（首个返回选项，未含缺失报价）</h2>
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
if (require.main === module) {
  try { main(); } catch { console.error('Comparison generation failed. Check input data and --input argument.'); process.exitCode = 1; }
}
module.exports = { generateHTML };
