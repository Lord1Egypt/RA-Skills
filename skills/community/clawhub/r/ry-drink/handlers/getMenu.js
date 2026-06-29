const {
  request,
  pick,
  withDefaults,
  ensureShopId,
  buildContextHeaders,
  resolveMerchantPathId,
} = require('./_http');

module.exports = async function getMenu(params) {
  const normalized = withDefaults(pick(params, ['shopId', 'saasId', 'tenantId', 'linkPhone']));
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  const merchantId = resolveMerchantPathId(normalized);
  if (!merchantId) {
    return { success: false, error: '缺少租客 ID（tenantId），无法查询菜单' };
  }
  return request('GET', `/merchant/${merchantId}/menus`, {
    query: {
      saasId: normalized.saasId,
      tenantId: merchantId,
      storeId: normalized.shopId,
    },
    headers: buildContextHeaders(normalized),
  });
};
