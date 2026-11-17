/**
 * 诊断脚本：dump 指定 carVersionSn 的原始接口返回，检查 SKU 上所有字段
 * 用法: node diag_raw_dump.js <carVersionCode>
 */
const https = require('https');
const fs = require('fs');

const vc = process.argv[2];
if (!vc) {
  console.error('Usage: node diag_raw_dump.js <carVersionCode>');
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

async function main() {
  const base = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/';
  const skuRes = await httpGet(base + 'listCarInfoList?carVersionSn=' + vc);
  const specRes = await httpGet(base + 'listSpecGroupAndSpecList?carVersionSn=' + vc);

  // 保存完整原始 JSON 便于检查
  fs.writeFileSync('scripts/tmp_' + vc + '_sku.json', JSON.stringify(skuRes, null, 2));
  fs.writeFileSync('scripts/tmp_' + vc + '_spec.json', JSON.stringify(specRes, null, 2));

  console.log('== listCarInfoList code: ' + skuRes.code + ', SKU数: ' + ((skuRes.data || []).length));
  const sku = (skuRes.data || [])[0];
  if (sku) {
    console.log('-- 第一个 SKU 的全部字段 --');
    for (const k of Object.keys(sku).sort()) {
      const v = sku[k];
      const vs = (typeof v === 'object') ? JSON.stringify(v) : String(v);
      console.log('  ' + k + ' = ' + (vs.length > 120 ? vs.slice(0, 120) + '...' : vs));
    }
  }
  console.log('完整JSON已写入 scripts/tmp_' + vc + '_sku.json / tmp_' + vc + '_spec.json');
}

main().catch(e => { console.error('DIAG_ERROR|' + e.message); process.exit(1); });
