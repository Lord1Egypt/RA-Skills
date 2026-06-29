/**
 * 获取小鹏全部车型列表
 * 输出格式：序号|carSeriesCode|carSeriesName（每行一个）
 */
const https = require('https');
const url = 'https://store.xiaopeng.com/api/v1/client/orion/carSeries/navigationBar';
https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' } }, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      if (json.code === 200 && json.data) {
        json.data.forEach((item, i) => {
          console.log((i + 1) + '|' + item.carSeriesCode + '|' + item.carSeriesName);
        });
      } else {
        console.error('ERROR: API returned code=' + json.code);
        process.exit(1);
      }
    } catch (e) {
      console.error('ERROR: Failed to parse response - ' + e.message);
      process.exit(1);
    }
  });
}).on('error', (e) => {
  console.error('ERROR: Request failed - ' + e.message);
  process.exit(1);
});
