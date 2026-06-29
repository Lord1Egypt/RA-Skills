const { request, pick, withDefaults, ensureShopId, buildContextHeaders } = require('./_http');

module.exports = async function getTables(params) {
  const normalized = withDefaults(pick(params, ['shopId', 'saasId', 'tenantId']));
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  return request('GET', '/aiemployees/appointment/tables', {
    query: { shopId: normalized.shopId, saasId: normalized.saasId },
    headers: buildContextHeaders(normalized),
  });
};
