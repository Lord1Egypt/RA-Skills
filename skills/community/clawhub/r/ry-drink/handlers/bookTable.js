const { request, pick, withResolvedShopId, buildContextHeaders, ensureShopId } = require('./_http');

module.exports = async function bookTable(params) {
  const body = withResolvedShopId(pick(params, [
    'saasId',
    'tenantId',
    'shopId',
    'linkNickname',
    'linkPhone',
    'dineDate',
    'dineTime',
    'tableCode',
    'personNum',
  ]));
  const shopErr = ensureShopId(body);
  if (shopErr) {
    return shopErr;
  }
  const required = ['linkNickname', 'linkPhone', 'dineDate', 'dineTime', 'tableCode', 'personNum'];
  const missing = required.filter((k) => body[k] === undefined || body[k] === '');
  if (missing.length) {
    return { success: false, error: `缺少必填参数: ${missing.join(', ')}` };
  }
  return request('POST', '/aiemployees/appointment/booking', {
    body,
    headers: buildContextHeaders(body),
  });
};
