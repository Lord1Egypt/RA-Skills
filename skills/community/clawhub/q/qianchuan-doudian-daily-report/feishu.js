const axios = require('axios').default;

const FEISHU_BASE_URL = 'https://open.feishu.cn/open-apis';
const DEFAULT_HEADER_RANGE = 'A1:AZ1';
const DEFAULT_APPEND_START_ROW = 2;
const FEISHU_REQUEST = { validateStatus: () => true };

function numeric(value) {
  return Number(String(value || '0').replace(/,/g, '').replace('%', '')) || 0;
}

function round2(value) {
  return Math.round(value * 100) / 100;
}

function todayKey() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  return `${yyyy}${mm}${dd}`;
}

function requireValue(value, name) {
  if (!value) {
    throw new Error(`缺少飞书配置: ${name}`);
  }
  return value;
}

function normalizeKey(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[()（）:：_-]/g, '');
}

function buildLookup(row) {
  const lookup = new Map();
  Object.entries(row || {}).forEach(([key, value]) => {
    lookup.set(normalizeKey(key), value);
  });
  return lookup;
}

function valueForHeader(rowLookup, header, aliases) {
  const candidates = [header, ...(aliases[header] || [])];
  for (const candidate of candidates) {
    const value = rowLookup.get(normalizeKey(candidate));
    if (value !== undefined) return value;
  }
  return '';
}

function columnName(index) {
  let name = '';
  let n = index;
  while (n > 0) {
    const remainder = (n - 1) % 26;
    name = String.fromCharCode(65 + remainder) + name;
    n = Math.floor((n - 1) / 26);
  }
  return name;
}

function buildAppendRange(sheetId, columnCount, rowCount, startRow) {
  const endColumn = columnName(Math.max(columnCount, 1));
  const endRow = startRow + Math.max(rowCount, 1) - 1;
  return `${sheetId}!A${startRow}:${endColumn}${endRow}`;
}

async function getTenantAccessToken(feishuConfig) {
  const appId = process.env.FEISHU_APP_ID;
  const feishuSecret = process.env.FEISHU_APP_SECRET;

  requireValue(appId, 'FEISHU_APP_ID');
  requireValue(feishuSecret, 'FEISHU_APP_SECRET');

  const { data } = await axios.post(
    `${FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal`,
    {
      app_id: appId,
      app_secret: feishuSecret
    },
    FEISHU_REQUEST
  );

  if (data.code !== 0) {
    throw new Error(`获取飞书 tenant_access_token 失败: ${data.msg || data.code}`);
  }

  return data.tenant_access_token;
}

function feishuHeaders(token) {
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json; charset=utf-8'
  };
}

async function getFirstSheetId(spreadsheetToken, token) {
  const { data } = await axios.get(
    `${FEISHU_BASE_URL}/sheets/v3/spreadsheets/${spreadsheetToken}/sheets/query`,
    { ...FEISHU_REQUEST, headers: feishuHeaders(token) }
  );

  if (data.code !== 0) {
    throw new Error(`读取飞书 sheet 列表失败: ${data.msg || data.code}`);
  }

  const sheet = data.data && data.data.sheets && data.data.sheets[0];
  if (!sheet) {
    throw new Error('飞书表格中没有可写入的工作表');
  }

  return sheet.sheet_id;
}

async function readHeaders(spreadsheetToken, sheetId, headerRange, token) {
  const range = `${sheetId}!${headerRange}`;
  const { data } = await axios.get(
    `${FEISHU_BASE_URL}/sheets/v2/spreadsheets/${spreadsheetToken}/values/${encodeURIComponent(range)}`,
    { ...FEISHU_REQUEST, headers: feishuHeaders(token) }
  );

  if (data.code !== 0) {
    throw new Error(`读取飞书表头失败: ${data.msg || data.code}`);
  }

  const values = data.data && data.data.valueRange && data.data.valueRange.values;
  const headers = values && values[0] ? values[0].map(value => String(value || '').trim()) : [];
  const usefulHeaders = headers.filter(Boolean);
  if (usefulHeaders.length === 0) {
    throw new Error(`飞书表头为空，请先在 ${range} 填好字段名`);
  }

  return usefulHeaders;
}

function rowsToSheetValues(rows, headers, aliases) {
  return rows.map(row => {
    const lookup = buildLookup(row);
    return headers.map(header => valueForHeader(lookup, header, aliases));
  });
}

async function appendValues(spreadsheetToken, range, values, token) {
  const { data } = await axios.post(
    `${FEISHU_BASE_URL}/sheets/v2/spreadsheets/${spreadsheetToken}/values_append`,
    {
      valueRange: {
        range,
        values
      }
    },
    { ...FEISHU_REQUEST, headers: feishuHeaders(token) }
  );

  if (data.code !== 0) {
    throw new Error(`写入飞书表格失败: ${data.msg || data.code}`);
  }

  return data.data || {};
}

async function updateValues(spreadsheetToken, range, values, token) {
  const { data } = await axios.put(
    `${FEISHU_BASE_URL}/sheets/v2/spreadsheets/${spreadsheetToken}/values`,
    {
      valueRange: {
        range,
        values
      }
    },
    { ...FEISHU_REQUEST, headers: feishuHeaders(token) }
  );

  if (data.code !== 0) {
    throw new Error(`更新飞书表格失败: ${data.msg || data.code}`);
  }

  return data.data || {};
}

async function readValues(spreadsheetToken, range, token) {
  const { data } = await axios.get(
    `${FEISHU_BASE_URL}/sheets/v2/spreadsheets/${spreadsheetToken}/values/${encodeURIComponent(range)}`,
    { ...FEISHU_REQUEST, headers: feishuHeaders(token) }
  );

  if (data.code !== 0) {
    throw new Error(`读取飞书表格失败: ${data.msg || data.code}`);
  }

  return (data.data && data.data.valueRange && data.data.valueRange.values) || [];
}

function summarizeMallDaily(rows) {
  const sourceRows = rows.summary ? [rows.summary] : rows;
  const total = sourceRows.reduce((acc, row) => {
    acc.spend += numeric(row['整体消耗']);
    acc.userPay += numeric(row['用户实际支付金额']);
    acc.coupon += numeric(row['智能优惠券金额']);
    acc.platform += numeric(row['电商平台补贴金额']);
    acc.orders += numeric(row['整体成交订单数']);
    acc.gmv += numeric(row['整体成交金额']);
    acc.netGmv += numeric(row['净成交金额']);
    acc.netOrders += numeric(row['净成交订单数']);
    return acc;
  }, {
    spend: 0,
    userPay: 0,
    coupon: 0,
    platform: 0,
    orders: 0,
    gmv: 0,
    netGmv: 0,
    netOrders: 0
  });

  total.refund = Math.max(0, total.gmv - total.netGmv);
  Object.keys(total).forEach(key => {
    total[key] = round2(total[key]);
  });
  return total;
}

function mallSourceRow(date, carrier, period, total) {
  return [
    date,
    carrier,
    period,
    total.gmv,
    total.userPay,
    total.coupon,
    total.platform,
    0,
    0,
    total.orders,
    total.orders,
    total.orders ? round2(total.userPay / total.orders) : 0,
    total.orders ? round2(total.userPay / total.orders) : 0,
    total.orders,
    total.netGmv,
    total.netOrders,
    0,
    0,
    total.netGmv,
    0,
    0,
    total.userPay,
    total.coupon,
    total.platform,
    total.refund,
    total.refund
  ];
}

async function upsertMallSourceRows(spreadsheetToken, sourceSheetId, date, sourceRows, token) {
  const existing = await readValues(spreadsheetToken, `${sourceSheetId}!A1:Z2000`, token);
  const rowByKey = new Map();
  existing.forEach((row, index) => {
    const rowDate = String(row[0] || '');
    const carrier = String(row[1] || '');
    const period = String(row[2] || '');
    if (rowDate === date) {
      rowByKey.set(`${carrier}|${period}`, index + 1);
    }
  });

  const missing = [];
  for (const row of sourceRows) {
    const key = `${row[1]}|${row[2]}`;
    const rowNumber = rowByKey.get(key);
    if (rowNumber) {
      await updateValues(spreadsheetToken, `${sourceSheetId}!A${rowNumber}:Z${rowNumber}`, [row], token);
    } else {
      missing.push(row);
    }
  }

  if (missing.length) {
    await appendValues(spreadsheetToken, `${sourceSheetId}!A2:Z${missing.length + 1}`, missing, token);
  }
}

async function writeMallDailyRows(rows, config) {
  const feishuConfig = config.feishu || {};
  const spreadsheetToken = requireValue(feishuConfig.spreadsheetToken, 'feishu.spreadsheetToken');
  const token = await getTenantAccessToken(feishuConfig);
  const sourceSheetId = requireValue(feishuConfig.sourceSheetId, 'feishu.sourceSheetId');
  const summarySheetId = feishuConfig.summarySheetId;
  const reportSheetId = feishuConfig.reportSheetId;
  const date = String(feishuConfig.date || todayKey());
  const total = summarizeMallDaily(rows);
  const empty = { spend: 0, userPay: 0, coupon: 0, platform: 0, orders: 0, gmv: 0, netGmv: 0, netOrders: 0, refund: 0 };

  await upsertMallSourceRows(spreadsheetToken, sourceSheetId, date, [
    mallSourceRow(date, '全部', '不限', total),
    mallSourceRow(date, '直播', '不限', empty),
    mallSourceRow(date, '商城', '不限', total)
  ], token);

  if (feishuConfig.summarySpendRange) {
    requireValue(summarySheetId, 'feishu.summarySheetId');
    await updateValues(spreadsheetToken, `${summarySheetId}!${feishuConfig.summarySpendRange}`, [[total.spend, 0]], token);
  }

  if (feishuConfig.reportDateCell) {
    requireValue(reportSheetId, 'feishu.reportSheetId');
    await updateValues(spreadsheetToken, `${reportSheetId}!${feishuConfig.reportDateCell}`, [[feishuConfig.reportDateFormula || 'TODAY()']], token);
  }

  return {
    skipped: false,
    sheetId: sourceSheetId,
    rowsWritten: 3,
    total
  };
}

async function writeRowsToFeishu(rows, config) {
  const feishuConfig = config.feishu || {};
  if (!feishuConfig.enabled) {
    return { skipped: true, reason: 'feishu.enabled 未开启' };
  }

  if (process.env.CONFIRM_WRITE_FEISHU !== '1') {
    throw new Error('写入飞书会修改目标表格。请确认目标表格、工作表和单元格范围正确后，设置环境变量 CONFIRM_WRITE_FEISHU=1 再运行。');
  }

  if (!Array.isArray(rows) || rows.length === 0) {
    return { skipped: true, reason: '没有抓取到可写入的数据' };
  }

  if (feishuConfig.writeMode === 'mallDaily') {
    return writeMallDailyRows(rows, config);
  }

  const spreadsheetToken = requireValue(feishuConfig.spreadsheetToken, 'feishu.spreadsheetToken');
  const token = await getTenantAccessToken(feishuConfig);
  const sheetId = feishuConfig.sheetId || await getFirstSheetId(spreadsheetToken, token);
  const headerRange = feishuConfig.headerRange || DEFAULT_HEADER_RANGE;
  const aliases = feishuConfig.fieldAliases || {};

  const headers = await readHeaders(spreadsheetToken, sheetId, headerRange, token);
  const values = rowsToSheetValues(rows, headers, aliases);
  const appendStartRow = Number(feishuConfig.appendStartRow || DEFAULT_APPEND_START_ROW);
  const appendRange = buildAppendRange(sheetId, headers.length, values.length, appendStartRow);
  const result = await appendValues(spreadsheetToken, appendRange, values, token);

  return {
    skipped: false,
    sheetId,
    appendRange,
    headers,
    rowsWritten: values.length,
    result
  };
}

module.exports = { writeRowsToFeishu };
