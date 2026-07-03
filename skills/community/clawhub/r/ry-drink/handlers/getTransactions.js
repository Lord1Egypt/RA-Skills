const {
  request,
  pick,
  withDefaults,
  ensureShopId,
  buildContextHeaders,
} = require('./_http');

module.exports = async function getTransactions(params) {
  const normalized = withDefaults(pick(params, ['memberId', 'shopId', 'saasId', 'tenantId', 'linkPhone']));
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  if (!normalized.memberId && !params.memberId) {
    return { success: false, error: 'memberId 不能为空' };
  }
  const query = pick(normalized, ['saasId', 'tenantId', 'shopId']);
  query.memberId = normalized.memberId || params.memberId;
  return request('GET', '/transaction/list', {
    query,
    headers: buildContextHeaders(normalized),
  });
};
