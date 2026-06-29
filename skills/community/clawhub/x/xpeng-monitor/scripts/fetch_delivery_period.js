/**
 * 查询指定配置版本的交付周期
 *
 * 用法1（Case 1 - GX/M03/P7 车型，按版本查询）:
 *   node fetch_delivery_period.js <carVersionCode> <carSeriesCode>
 *   输出: OK|minDelivery|maxDelivery|carName 或 NO_DATA|0|0| 或 ERROR|0|0|
 *
 * 用法2（Case 2 - 其他车型，批量查询全部版本）:
 *   node fetch_delivery_period.js <carSeriesCode> --all
 *   输出: carVersionCode|OK|minDelivery|maxDelivery|carName（每行一个版本）
 *        或 carVersionCode|NO_DATA|0|0|
 *
 * 用法3（Case 2 - 其他车型，查询单个版本）:
 *   node fetch_delivery_period.js <carVersionCode> <carSeriesCode>
 *   输出: OK|minDelivery|maxDelivery|carName 或 NO_DATA|0|0| 或 ERROR|0|0|
 *
 * 交付周期单位是周，不需要转换
 */
const https = require('https');

const args = process.argv.slice(2);
const isAllMode = args.includes('--all');

// ---------- HTTP 工具 ----------

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
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

// ---------- 核心匹配逻辑 ----------

/**
 * 从配置规格组列表中找出所有 isDefault=1 的 carSpecificationCode
 * @param {Array} specGroups - 可选配置规格列表，每项含 specList
 * @returns {string[]} 排序后的默认规格代码列表
 */
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

/**
 * 在 SKU 列表中找到规格配置与 defaultCodes 完全匹配的 SKU
 * 匹配规则：SKU 的 specList 中所有 specCode 组成的列表排序后与 defaultCodes 完全一致
 * @param {Array} skus - SKU 列表
 * @param {string[]} defaultCodes - 排序后的默认规格代码列表
 * @returns {Object|null} 匹配的 SKU，未找到返回 null
 */
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

/**
 * 判断是否为 Case 1 车型（GX/M03/P7）
 */
function isCase1Model(carSeriesCode) {
  if (!carSeriesCode) return false;
  const upper = carSeriesCode.toUpperCase();
  return upper.startsWith('GX') || upper.startsWith('M03') || upper.startsWith('P7');
}

/**
 * 从 SKU 中提取交付周期并输出
 * @param {Object} sku - 匹配的 SKU
 * @param {string} [prefix] - 可选前缀（用于 --all 模式）
 */
function outputDelivery(sku, prefix) {
  const pfx = prefix ? prefix + '|' : '';
  if (sku) {
    const min = sku.minDeliveryPeriod;
    const max = sku.maxDeliveryPeriod;
    const carName = sku.carName || '';
    if (min != null && max != null) {
      console.log(pfx + 'OK|' + min + '|' + max + '|' + carName);
    } else {
      console.log(pfx + 'NO_DATA|0|0|' + carName);
    }
  } else {
    console.log(pfx + 'NO_DATA|0|0|');
  }
}

// ---------- Case 1: GX/M03/P7 车型 ----------

async function handleCase1(carVersionCode, carSeriesCode) {
  try {
    // 1) 获取可选配置规格列表
    const specUrl = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/listSpecGroupAndSpecList?carVersionSn=' + carVersionCode;
    const specRes = await httpGet(specUrl);

    let defaultCodes = [];
    if (specRes.code === 200 && Array.isArray(specRes.data)) {
      defaultCodes = findDefaultSpecCodes(specRes.data);
    }

    // 2) 获取 SKU 列表（含交付周期）
    const skuUrl = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/listCarInfoList?carVersionSn=' + carVersionCode;
    const skuRes = await httpGet(skuUrl);

    if (skuRes.code !== 200 || !Array.isArray(skuRes.data) || skuRes.data.length === 0) {
      console.log('NO_DATA|0|0|');
      return;
    }

    // 3) 找到默认配置匹配的 SKU，输出交付周期
    const matchedSku = findMatchingSku(skuRes.data, defaultCodes);
    outputDelivery(matchedSku);
  } catch (e) {
    console.error('ERROR|0|0|');
    process.exit(1);
  }
}

// ---------- Case 2: 其他车型（allInOne） ----------

/**
 * 处理 allInOnce 响应中指定版本的数据
 * @param {Object} allInOneData - allInOne API 的 data 字段
 * @param {string} versionCode - 要查询的版本代码
 * @param {string} [prefix] - 输出前缀（--all 模式使用）
 */
function processVersionFromAllInOne(allInOneData, versionCode, prefix) {
  const carSpecGroupVoMap = allInOneData.carSpecGroupVoMap || {};
  const carInfoVoMap = allInOneData.carInfoVoMap || {};

  const specGroups = carSpecGroupVoMap[versionCode] || [];
  const skus = carInfoVoMap[versionCode] || [];

  const defaultCodes = findDefaultSpecCodes(specGroups);

  if (skus.length === 0) {
    const pfx = prefix ? prefix + '|' : '';
    console.log(pfx + 'NO_DATA|0|0|');
    return;
  }

  const matchedSku = findMatchingSku(skus, defaultCodes);
  outputDelivery(matchedSku, prefix);
}

/**
 * Case 2 批量模式：输出 carSeriesCode 下所有版本的交付周期
 */
async function handleCase2All(carSeriesCode) {
  try {
    const url = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/allInOne?carSeriesSn=' + carSeriesCode;
    const res = await httpGet(url);

    if (res.code !== 200 || !res.data) {
      console.error('ERROR: allInOne API returned code=' + (res.code || 'unknown'));
      process.exit(1);
    }

    const carInfoVoMap = res.data.carInfoVoMap || {};
    const versionCodes = Object.keys(carInfoVoMap);

    if (versionCodes.length === 0) {
      console.error('WARN: No versions found in allInOne response');
      return;
    }

    for (const versionCode of versionCodes) {
      processVersionFromAllInOne(res.data, versionCode, versionCode);
    }
  } catch (e) {
    console.error('ERROR: ' + e.message);
    process.exit(1);
  }
}

/**
 * Case 2 单版本模式：获取 allInOne 数据后筛选指定版本
 */
async function handleCase2Single(carVersionCode, carSeriesCode) {
  try {
    const url = 'https://store.xiaopeng.com/api/v1/client/orion/configurator/allInOne?carSeriesSn=' + carSeriesCode;
    const res = await httpGet(url);

    if (res.code !== 200 || !res.data) {
      console.log('NO_DATA|0|0|');
      return;
    }

    const carInfoVoMap = res.data.carInfoVoMap || {};
    if (!carInfoVoMap[carVersionCode]) {
      console.log('NO_DATA|0|0|');
      return;
    }

    processVersionFromAllInOne(res.data, carVersionCode);
  } catch (e) {
    console.error('ERROR|0|0|');
    process.exit(1);
  }
}

// ---------- 主入口 ----------

if (isAllMode) {
  // 用法: node fetch_delivery_period.js <carSeriesCode> --all
  const carSeriesCode = args[0];
  if (!carSeriesCode) {
    console.error('Usage: node fetch_delivery_period.js <carSeriesCode> --all');
    process.exit(1);
  }
  handleCase2All(carSeriesCode);
} else {
  // 用法: node fetch_delivery_period.js <carVersionCode> [carSeriesCode]
  const carVersionCode = args[0];
  const carSeriesCode = args[1] || '';
  if (!carVersionCode) {
    console.error('Usage: node fetch_delivery_period.js <carVersionCode> [carSeriesCode]');
    process.exit(1);
  }

  if (isCase1Model(carSeriesCode)) {
    handleCase1(carVersionCode, carSeriesCode);
  } else {
    handleCase2Single(carVersionCode, carSeriesCode);
  }
}
