/**
 * 获取指定车型下的所有配置版本列表
 * 用法：node fetch_car_versions.js <carSeriesCode>
 * 输出格式：carVersionCode|carVersionName（每行一个）
 */
const https = require('https');
const carSeriesCode = process.argv[2];
if (!carSeriesCode) {
  console.error('Usage: node fetch_car_versions.js <carSeriesCode>');
  process.exit(1);
}
const url = 'https://store.xiaopeng.com/configurate.html?carSeries=' + carSeriesCode;
https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' } }, (res) => {
  let html = '';
  res.on('data', (chunk) => html += chunk);
  res.on('end', () => {
    try {
      // 从 <script> 标签内容中提取 carVersionCode 和 carVersionName
      const scriptMatches = html.match(/<script[^>]*>([\s\S]*?)<\/script>/gi) || [];
      let allContent = scriptMatches.join('\n');
      // 匹配 carVersionCode 和 carVersionName 对
      const pattern = /"carVersionCode"\s*:\s*"([^"]+)"[^}]*?"carVersionName"\s*:\s*"([^"]+)"/g;
      const seen = new Set();
      let match;
      while ((match = pattern.exec(allContent)) !== null) {
        const code = match[1];
        const name = match[2];
        if (!seen.has(code)) {
          seen.add(code);
          console.log(code + '|' + name);
        }
      }
      if (seen.size === 0) {
        console.error('WARN: No carVersionCode/carVersionName found in page');
      }
    } catch (e) {
      console.error('ERROR: Failed to parse HTML - ' + e.message);
      process.exit(1);
    }
  });
}).on('error', (e) => {
  console.error('ERROR: Request failed - ' + e.message);
  process.exit(1);
});
