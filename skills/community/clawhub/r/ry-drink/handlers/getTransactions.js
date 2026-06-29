const { request, pick, withResolvedShopId } = require('./_http');

module.exports = async function getTransactions(params) {
  if (!params.memberId) {
    return { success: false, error: 'memberId 不能为空' };
  }
  return request('GET', '/transaction/list', {
    query: withResolvedShopId(pick(params, ['saasId', 'tenantId', 'shopId', 'memberId'])),
  });
};
