const https = require('https');
const apiKey = process.env.SIMMER_API_KEY;

const options = {
  hostname: 'api.simmer.markets',
  port: 443,
  path: '/v1/markets',
  method: 'GET',
  headers: { 'Authorization': `Bearer ${apiKey}` }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', (d) => body += d);
  res.on('end', () => {
    console.log("=== АКТИВНІ РИНКИ ПОГОДИ (POLYMARKET) ===");
    try {
      const markets = JSON.parse(body);
      if (markets && markets.length > 0) {
        markets.slice(0, 5).forEach(m => {
          console.log(`Рынок: ${m.title || 'Unnamed Market'}`);
          console.log(`Статус: ${m.status || 'Active'}`);
          console.log(`Останнє оновлення: ${m.lastUpdated || 'N/A'}`);
          console.log('---');
        });
      } else {
        console.log("Список маркетів порожній або доступ обмежено.");
        console.log("Причина: Бот очікує відкриття ліквідності на Polymarket.");
      }
    } catch (e) {
      console.log("Не вдалося отримати дані маркетів. Спробуйте пізніше.");
    }
  });
});

req.on('error', (e) => console.error(e));
req.end();
