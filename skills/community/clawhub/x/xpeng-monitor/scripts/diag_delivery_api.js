/**
 * 诊断脚本：对比同一车型在两套接口下的交付周期数据
 *
 * 用途：排查 G9L 等新车型该走 Case 1（configurator 逐版本接口）还是 Case 2（allInOne 接口）
 * 用法: node diag_delivery_api.js <carSeriesCode>
 * 输出: 对每个版本分别打印两条路径的默认配置匹配结果，便于对比差异
 */
const https = require('https');

const carSeriesCode = process.argv[2];
if (!carSeriesCode) {
  console.error('Usage: node diag_delivery_api.js <carSeriesCode>');
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
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('JSON parse failed for ' + url + ': ' + e.message));
        }
      });
    }).on('error', reject);
  });
}

function findDefaultSpecCodes(specGroups) {
  const defaultCodes = [];
  for (const group of specGroups) {
    for (const spec of (group.specList || [])) {
      if (spec.isDefault === 1) {
        defaultCodes.push(spec.carSpecificationCode);
      }
    }
  }
  return defaultCodes.sort();
}

function findMatchingSku(skus, defaultCodes) {
  for (const sku of skus) {
    const specCodes = (sku.specList || []).map(s => s.specCode).sort();
    if (specCodes.length === defaultCodes.length &&
        specCodes.every((v, i) => v === defaultCodes[i])) {
      return sku;
    }
  }
  return null;
}

function fmtSku(sku) {
  if (!sku) return 'NO_MATCHED_SKU';
  const min = sku.minDeliveryPeriod, max = sku.maxDeliveryPeriod;
  const period = (min != null && max != null) ? (min + '-' + max + '周') : 'null';
  return period + ' | ' + (sku.carName || '');
}

async function main() {
  // ---- 路径A: Case 1 的逐版本接口 ----
  const specUrl = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/listSpecGroupAndSpecList?carVersionSn=';
  const skuUrl = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/listCarInfoList?carVersionSn=';
  // ---- 路径B: Case 2 的 allInOne 接口 ----
  const allUrl = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/allInOne?carSeriesSn=' + carSeriesCode;

  // 先拿 allInOne 确定版本列表
  const allRes = await httpGet(allUrl);
  if (allRes.code !== 200 || !allRes.data) {
    console.log('ALLINONE_FAILED|code=' + allRes.code);
    return;
  }
  const versionCodes = Object.keys(allRes.data.carInfoVoMap || {});
  console.log('=== carSeriesCode: ' + carSeriesCode + ', versions: ' + versionCodes.length + ' ===');

  for (const vc of versionCodes) {
    // 路径B: allInOne 内的数据
    const specGroupsB = (allRes.data.carSpecGroupVoMap || {})[vc] || [];
    const skusB = (allRes.data.carInfoVoMap || {})[vc] || [];
    const skuB = skusB.length ? findMatchingSku(skusB, findDefaultSpecCodes(specGroupsB)) : null;

    // 路径A: configurator 逐版本接口
    let lineA;
    try {
      const specRes = await httpGet(specUrl + vc);
      const skuRes = await httpGet(skuUrl + vc);
      if (skuRes.code === 200 && Array.isArray(skuRes.data) && skuRes.data.length > 0) {
        const defaultCodes = (specRes.code === 200 && Array.isArray(specRes.data))
          ? findDefaultSpecCodes(specRes.data) : [];
        const skuA = findMatchingSku(skuRes.data, defaultCodes);
        lineA = 'A(configurator): ' + fmtSku(skuA);
      } else {
        lineA = 'A(configurator): 无数据(code=' + skuRes.code + ',len=' + (skuRes.data || []).length + ')';
      }
    } catch (e) {
      lineA = 'A(configurator): 请求失败 ' + e.message;
    }

    console.log(vc);
    console.log('  ' + lineA);
    console.log('  B(allInOne)   : ' + fmtSku(skuB));
  }
}

main().catch(e => {
  console.error('DIAG_ERROR|' + e.message);
  process.exit(1);
});
