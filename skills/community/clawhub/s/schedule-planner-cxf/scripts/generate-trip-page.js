#!/usr/bin/env node
/**
 * generate-trip-page.js — 生成行程网页
 *
 * 用法:
 *   node scripts/generate-trip-page.js            # 从 JSON 文件读取
 *   node scripts/generate-trip-page.js --mock     # 使用预置模拟数据
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// === 解析参数 ===
const args = process.argv.slice(2);
const useMock = args.includes('--mock');

// === 获取行程数据 ===
let tripData;
let tripDataPath;

if (useMock) {
  const mockDataModule = path.join(__dirname, 'mock-data.js');
  const { getMockTripData } = require(mockDataModule);
  tripData = getMockTripData();
  tripDataPath = 'MOCK';
  console.log('[Mock mode] Using built-in mock trip data');
} else {
  tripDataPath = path.join(__dirname, 'trip-data.json');
  if (!fs.existsSync(tripDataPath)) {
    console.error('Error: trip-data.json not found.');
    console.log('');
    console.log('  Option 1: Create trip-data.json in scripts/ directory');
    console.log('  Option 2: Use --mock for demo mode:');
    console.log('    node scripts/generate-trip-page.js --mock');
    console.log('');
    process.exit(1);
  }
  tripData = JSON.parse(fs.readFileSync(tripDataPath, 'utf8'));
}

// === 生成 HTML ===
const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${tripData.destination}${tripData.tripType} Trip - ${tripData.duration}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh; padding: 20px;
    }
    .container {
      max-width: 1400px; margin: 0 auto; background: white;
      border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; padding: 30px 40px; text-align: center;
    }
    .header h1 { font-size: 32px; margin-bottom: 10px; font-weight: 600; }
    .header p { font-size: 16px; opacity: 0.9; }
    .content { display: flex; min-height: 700px; }
    .left { flex: 1; padding: 40px; border-right: 1px solid #eee; max-height: 800px; overflow-y: auto; }
    .right { width: 400px; padding: 40px; background: #f8f9fa; display: flex; flex-direction: column; align-items: center; }
    .section { margin-bottom: 35px; }
    .section-title { font-size: 20px; font-weight: 600; color: #333; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
    .card {
      background: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 15px;
      border-left: 4px solid #667eea;
    }
    .card h3 { font-size: 16px; color: #333; margin-bottom: 12px; display: flex; justify-content: space-between; }
    .card h3 .price { color: #667eea; font-weight: 600; font-size: 18px; }
    .card p { font-size: 14px; color: #666; line-height: 1.8; }
    .card .route { display: flex; align-items: center; gap: 15px; margin: 10px 0; }
    .card .route .airport { text-align: center; }
    .card .route .airport .time { font-size: 20px; font-weight: 600; color: #333; }
    .card .route .airport .name { font-size: 12px; color: #666; }
    .card .route .arrow { font-size: 24px; color: #667eea; }
    .card .info-row {
      background: white; padding: 10px 15px; border-radius: 8px; margin-top: 10px;
      font-size: 13px; color: #666; display: flex; justify-content: space-between;
    }
    .hotel-card {
      background: #f8f9fa; border-radius: 12px; padding: 20px; border-left: 4px solid #667eea;
    }
    .hotel-card h3 { font-size: 18px; color: #333; margin-bottom: 15px; }
    .hotel-card .info { font-size: 14px; color: #666; line-height: 2; }
    .day-plan {
      background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
      border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }
    .day-plan h4 { font-size: 16px; color: #667eea; margin-bottom: 10px; font-weight: 600; }
    .day-plan ul { list-style: none; }
    .day-plan li { padding: 8px 0; padding-left: 20px; font-size: 14px; color: #555; line-height: 1.6; }
    .tips-list { list-style: none; }
    .tips-list li { padding: 10px 0; padding-left: 25px; font-size: 14px; color: #666; line-height: 1.6; }
    .qr-section { text-align: center; margin-bottom: 30px; width: 100%; }
    .qr-section h3 { font-size: 18px; color: #333; margin-bottom: 20px; }
    .qr-code { width: 280px; height: 280px; background: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .qr-code img { width: 100%; height: 100%; object-fit: contain; }
    .total-box {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; border-radius: 12px; padding: 25px; width: 100%; margin-bottom: 20px;
    }
    .total-box .label { font-size: 14px; opacity: 0.9; margin-bottom: 10px; }
    .total-box .amount { font-size: 36px; font-weight: 700; }
    .total-box .breakdown { font-size: 13px; opacity: 0.9; margin-top: 10px; line-height: 1.8; }
    .btn {
      display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none;
      font-size: 14px; font-weight: 600; cursor: pointer; text-align: center; width: 100%; margin-bottom: 10px;
    }
    .btn-secondary { background: white; color: #667eea; border: 2px solid #667eea; }
    .footer { text-align: center; padding: 20px; background: #f8f9fa; font-size: 13px; color: #999; }
    @media (max-width: 768px) { .content { flex-direction: column; } .right { width: 100%; border-top: 1px solid #eee; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${tripData.destination}${tripData.tripType} Trip</h1>
      <p>${tripData.duration} | Passenger: ${tripData.passenger || 'N/A'}</p>
    </div>
    <div class="content">
      <div class="left">
        ${tripData.dailyPlan && tripData.dailyPlan.length > 0 ? `
        <div class="section">
          <div class="section-title"><span>📅</span><span>Daily Plan</span></div>
          ${tripData.dailyPlan.map(day => `
          <div class="day-plan">
            <h4>${day.day}</h4>
            <div style="font-size:13px;color:#666;margin-bottom:12px;">${day.title}</div>
            <ul>${day.items.map(item => `<li>${item}</li>`).join('')}</ul>
          </div>`).join('')}
        </div>` : ''}

        ${tripData.segments.filter(s => s.type === 'train').length > 0 ? `
        <div class="section">
          <div class="section-title"><span>🚄</span><span>Train</span></div>
          ${tripData.segments.filter(s => s.type === 'train').map(train => `
          <div class="card">
            <h3><span>${train.segmentNo || train.trainNo}</span><span class="price">¥${train.price}</span></h3>
            <div class="route">
              <div class="airport"><div class="time">${train.departure.split(' ').pop()}</div><div class="name">${train.departure.split(' ').slice(0,-1).join(' ')}</div></div>
              <div class="arrow">→</div>
              <div class="airport"><div class="time">${train.arrival.split(' ').pop()}</div><div class="name">${train.arrival.split(' ').slice(0,-1).join(' ')}</div></div>
            </div>
            <div class="info-row"><span>📅 ${train.date}</span><span>💺 ${train.seat || ''}</span>${train.duration ? `<span>⏱ ${train.duration}</span>` : ''}</div>
          </div>`).join('')}
        </div>` : ''}

        ${tripData.segments.filter(s => s.type === 'hotel').length > 0 ? `
        <div class="section">
          <div class="section-title"><span>🏨</span><span>Hotel</span></div>
          ${tripData.segments.filter(s => s.type === 'hotel').map(hotel => `
          <div class="hotel-card">
            <h3>${hotel.name}</h3>
            <div class="info">
              ${hotel.address ? `<div>📍 ${hotel.address}</div>` : ''}
              ${hotel.roomType ? `<div>🛏 ${hotel.roomType}</div>` : ''}
              ${hotel.checkIn ? `<div>Check-in: ${hotel.checkIn}</div>` : ''}
              ${hotel.checkOut ? `<div>Check-out: ${hotel.checkOut}</div>` : ''}
              ${hotel.nights ? `<div>📅 ${hotel.nights} nights</div>` : ''}
              ${hotel.price ? `<div>💰 ¥${hotel.price}/night</div>` : ''}
            </div>
          </div>`).join('')}
        </div>` : ''}

        ${tripData.segments.filter(s => s.type === 'flight').length > 0 ? `
        <div class="section">
          <div class="section-title"><span>✈️</span><span>Flight</span></div>
          ${tripData.segments.filter(s => s.type === 'flight').map(flight => `
          <div class="card">
            <h3><span>${flight.flightNo || flight.segmentNo}</span><span class="price">¥${flight.price}</span></h3>
            <div class="route">
              <div class="airport"><div class="time">${flight.departure.split(' ').pop()}</div><div class="name">${flight.departure.split(' ').slice(0,-1).join(' ')}</div></div>
              <div class="arrow">→</div>
              <div class="airport"><div class="time">${flight.arrival.split(' ').pop()}</div><div class="name">${flight.arrival.split(' ').slice(0,-1).join(' ')}</div></div>
            </div>
          </div>`).join('')}
        </div>` : ''}

        ${tripData.tips && tripData.tips.length > 0 ? `
        <div class="section">
          <div class="section-title"><span>💡</span><span>Tips</span></div>
          <ul class="tips-list">${tripData.tips.map(tip => `<li>${tip}</li>`).join('')}</ul>
        </div>` : ''}
      </div>

      <div class="right">
        <div class="total-box">
          <div class="label">Total Cost</div>
          <div class="amount">¥${tripData.costs.total}</div>
          <div class="breakdown">
            ${Object.entries(tripData.costs).filter(([k]) => k !== 'total').map(([k, v]) => {
              const labels = { train: 'Train', hotel: 'Hotel', flight: 'Flight', ticket: 'Ticket' };
              return `${labels[k] || k}: ¥${v}<br>`;
            }).join('')}
          </div>
        </div>
        <div class="qr-section">
          <h3>Scan to Pay</h3>
          <div class="qr-code" style="display:flex;align-items:center;justify-content:center;font-size:14px;color:#999;">
            [QR Code Placeholder]
          </div>
          <p style="font-size:13px;color:#667eea;">Open WeChat to scan</p>
        </div>
        ${tripData.paymentUrl ? `<a href="${tripData.paymentUrl}" class="btn" target="_blank">📱 View Orders</a>` : ''}
      </div>
    </div>
    <div class="footer">Safe travels!</div>
  </div>
</body>
</html>`;

// === 写入文件 ===
const outputDir = './output';
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const timestamp = Date.now();
const sanitizedDest = tripData.destination.replace(/\s+/g, '-');
const htmlFileName = `trip-${sanitizedDest}-${timestamp}.html`;
const htmlPath = path.join(outputDir, htmlFileName);
fs.writeFileSync(htmlPath, html, 'utf8');

console.log('HTML generated:', htmlPath);

// === 生成二维码 ===
const qrScript = path.join(__dirname, 'qrcode.js');
const paymentUrl = tripData.paymentUrl;

if (paymentUrl && !useMock) {
  try {
    console.log('Generating QR code for:', paymentUrl);
    const qrOutput = path.join(outputDir, `qr-${timestamp}.html`);
    execSync(`node "${qrScript}" "${paymentUrl}" "${qrOutput}"`, {
      stdio: 'inherit',
      timeout: 15000
    });
    console.log('QR code generated:', qrOutput);
  } catch (err) {
    console.log('QR generation skipped:', err.message);
  }
} else if (paymentUrl && useMock) {
  console.log('[Mock mode] QR code generation skipped');
}

// === 打开网页 ===
try {
  execSync(`powershell -NoProfile -Command "Start-Process '${htmlPath}'"`, { stdio: 'pipe', timeout: 5000 });
  console.log('Opened in browser:', htmlPath);
} catch (e) {
  console.log('File path:', htmlPath);
}