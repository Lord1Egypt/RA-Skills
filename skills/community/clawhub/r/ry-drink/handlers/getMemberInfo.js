const {
  request,
  pick,
  withDefaults,
  ensureShopId,
  buildContextHeaders,
} = require('./_http');

module.exports = async function getMemberInfo(params) {
  const normalized = withDefaults(pick(params, ['memberId', 'shopId', 'saasId', 'tenantId', 'linkPhone']));
  const shopErr = ensureShopId(normalized);
  if (shopErr) {
    return shopErr;
  }
  const memberId = normalized.memberId || params.memberId;
  if (!memberId) {
    return { success: false, error: 'memberId 不能为空，请向顾客确认会员编号或手机号' };
  }
  return request('GET', `/member/${memberId}`, {
    query: pick(normalized, ['saasId', 'tenantId', 'shopId']),
    headers: buildContextHeaders(normalized),
  });
};
