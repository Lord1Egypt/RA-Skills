/**
 * 诊断脚本：拉取官网配置页 HTML 及其 JS 包，分析页面使用的交付周期相关接口和参数
 * 用法: node diag_page_apis.js <carSeriesCode>
 */
const https = require('https');
const fs = require('fs');

const series = process.argv[2] || 'G9L';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36';

function httpGetText(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': UA, 'Accept': '*/*' } }, (res) => {
      if (res.statusCode !== 200) { reject(new Error(url + ' -> HTTP ' + res.statusCode)); return; }
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function findContext(raw, kw, count) {
  const out = [];
  let idx = 0;
  while (out.length < (count || 3)) {
    const i = raw.indexOf(kw, idx);
    if (i < 0) break;
    out.push(raw.slice(Math.max(0, i - 100), i + 150).replace(/\s+/g, ' '));
    idx = i + kw.length;
  }
  return out;
}

async function main() {
  // 1) 拉配置页 HTML
  const pageUrl = 'https://store.xiaopeng.com/configurate.html?carSeries=' + series;
  const html = await httpGetText(pageUrl);
  fs.writeFileSync('scripts/tmp_page.html', html);
  console.log('== 页面大小: ' + html.length + ' 字节');

  // 2) HTML 内联内容中搜周期相关关键词
  for (const kw of ['DeliveryPeriod', 'deliveryPeriod', 'delivery']) {
    const hits = findContext(html, kw, 3);
    for (const h of hits) console.log('[html:' + kw + '] ...' + h + '...');
  }

  // 3) 提取 JS 包地址
  const srcMatches = html.match(/<script[^>]+src="([^"]+)"/g) || [];
  const jsUrls = srcMatches.map(s => s.match(/src="([^"]+)"/)[1])
    .filter(u => u.endsWith('.js') || u.includes('.js?'));
  console.log('== JS包数量: ' + jsUrls.length);

  // 4) 逐个拉取并搜索接口/参数关键词
  const keywords = ['DeliveryPeriod', 'cityCode', 'cityId', 'provinceCode', 'orion/configurator', 'deliveryPeriod', 'getDelivery', 'deliveryTime'];
  let found = 0;
  for (let i = 0; i < jsUrls.length; i++) {
    let u = jsUrls[i];
    if (u.startsWith('//')) u = 'https:' + u;
    else if (u.startsWith('/')) u = 'https://store.xiaopeng.com' + u;
    try {
      const js = await httpGetText(u);
      const hitKws = keywords.filter(kw => js.includes(kw));
      if (hitKws.length > 0) {
        found++;
        console.log('\n-- JS[' + i + '] ' + u + ' (' + Math.round(js.length / 1024) + 'KB) 命中: ' + hitKws.join(','));
        for (const kw of hitKws) {
          for (const ctx of findContext(js, kw, 2)) {
            console.log('   [' + kw + '] ...' + ctx + '...');
          }
        }
      }
    } catch (e) {
      console.log('   JS[' + i + '] ' + u + ' 拉取失败: ' + e.message);
    }
  }
  if (found === 0) console.log('未在 JS 包中命中任何关键词');
}

main().catch(e => { console.error('DIAG_ERROR|' + e.message); process.exit(1); });
