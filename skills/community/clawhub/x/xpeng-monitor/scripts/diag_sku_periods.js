/**
 * 诊断脚本：列出指定车型每个版本下所有 SKU 的交付周期分布
 *
 * 用途：排查"默认配置匹配"取到的周期是否与该版本其他配置组合差异过大
 * 用法: node diag_sku_periods.js <carSeriesCode>
 */
const https = require('https');

const carSeriesCode = process.argv[2];
if (!carSeriesCode) {
  console.error('Usage: node diag_sku_periods.js <carSeriesCode>');
  process.exit(1);
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json'
      }
    };
    https.get(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

function findDefaultSpecCodes(specGroups) {
  const codes = [];
  for (const group of specGroups) {
    for (const spec of (group.specList || [])) {
      if (spec.isDefault === 1) codes.push(spec.carSpecificationCode);
    }
  }
  return codes.sort();
}

async function main() {
  const url = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/allInOne?carSeriesSn=' + carSeriesCode;
  const res = await httpGet(url);
  if (res.code !== 200 || !res.data) {
    console.log('FAILED|code=' + res.code);
    return;
  }
  const specMap = res.data.carSpecGroupVoMap || {};
  const infoMap = res.data.carInfoVoMap || {};

  for (const vc of Object.keys(infoMap)) {
    const skus = infoMap[vc] || [];
    const defaults = findDefaultSpecCodes(specMap[vc] || []);
    // 按周期聚合
    const groups = {};
    for (const sku of skus) {
      const key = (sku.minDeliveryPeriod ?? 'null') + '-' + (sku.maxDeliveryPeriod ?? 'null');
      (groups[key] = groups[key] || []).push(sku);
    }
    // 找默认配置的 SKU 对应哪个周期组
    let defaultKey = '(未匹配)';
    for (const sku of skus) {
      const specCodes = (sku.specList || []).map(s => s.specCode).sort();
      if (specCodes.length === defaults.length && specCodes.every((v, i) => v === defaults[i])) {
        defaultKey = (sku.minDeliveryPeriod ?? 'null') + '-' + (sku.maxDeliveryPeriod ?? 'null');
        break;
      }
    }
    console.log('\n## ' + vc + ' (SKU总数: ' + skus.length + ', 默认配置命中周期: ' + defaultKey + ')');
    for (const key of Object.keys(groups).sort()) {
      const mark = key === defaultKey ? ' <== 默认配置' : '';
      const names = groups[key].map(s => s.carName || '(无名)').slice(0, 3);
      console.log('  ' + key + '周 x' + groups[key].length + mark);
      for (const n of names) console.log('      - ' + n);
      if (groups[key].length > 3) console.log('      ... 其余 ' + (groups[key].length - 3) + ' 个省略');
    }
  }
}

main().catch(e => {
  console.error('DIAG_ERROR|' + e.message);
  process.exit(1);
});
