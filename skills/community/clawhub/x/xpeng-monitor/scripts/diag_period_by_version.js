/**
 * 诊断脚本：调用页面真实使用的 listDeliveryPeriodByVersion 接口，
 * 按"默认配置匹配的 SKU carCode"取出页面口径的交付周期，与旧字段对比
 * 用法: node diag_period_by_version.js <carSeriesCode>
 */
const https = require('https');

const series = process.argv[2];
if (!series) {
  console.error('Usage: node diag_period_by_version.js <carSeriesCode>');
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
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}

function findDefaultSpecCodes(specGroups) {
  const codes = [];
  for (const g of specGroups) for (const s of (g.specList || [])) if (s.isDefault === 1) codes.push(s.carSpecificationCode);
  return codes.sort();
}

function findMatchingSku(skus, defaultCodes) {
  for (const sku of skus) {
    const specCodes = (sku.specList || []).map(s => s.specCode).sort();
    if (specCodes.length === defaultCodes.length && specCodes.every((v, i) => v === defaultCodes[i])) return sku;
  }
  return null;
}

async function main() {
  const allRes = await httpGet('https://store.xiaopeng.com/api/v1/client/orion/configurator/allInOne?carSeriesSn=' + series);
  if (allRes.code !== 200 || !allRes.data) { console.log('ALLINONE_FAILED|' + allRes.code); return; }
  const versionCodes = Object.keys(allRes.data.carInfoVoMap || {});
  console.log('carSeriesCode|carVersionCode|carVersionName|旧字段周期|页面口径周期|expectDeliveryTime|carName');

  for (const vc of versionCodes) {
    const skus = allRes.data.carInfoVoMap[vc] || [];
    const defaults = findDefaultSpecCodes((allRes.data.carSpecGroupVoMap || {})[vc] || []);
    const sku = findMatchingSku(skus, defaults);
    if (!sku) { console.log(series + '|' + vc + '|?|无默认匹配SKU|—|—|'); continue; }

    const dpRes = await httpGet('https://store.xiaopeng.com/api/v1/client/orion/configurator/listDeliveryPeriodByVersion?carVersionSn=' + vc);
    let newVal = '接口失败';
    if (dpRes.code === 200 && Array.isArray(dpRes.data)) {
      const hit = dpRes.data.find(x => x.carCode === sku.carCode);
      if (hit) newVal = (hit.minDeliveryPeriod ?? 'null') + '-' + (hit.maxDeliveryPeriod ?? 'null') + '周';
      else newVal = 'carCode未命中(' + dpRes.data.length + '条)';
    } else if (dpRes.code === 200) {
      newVal = '空数据';
    }
    console.log(series + '|' + vc + '|' + (sku.carVersionName || '') + '|'
      + (sku.minDeliveryPeriod ?? 'null') + '-' + (sku.maxDeliveryPeriod ?? 'null') + '周|'
      + newVal + '|' + String(sku.expectDeliveryTime ?? '') + '|' + sku.carName);
  }
}

main().catch(e => { console.error('DIAG_ERROR|' + e.message); process.exit(1); });
