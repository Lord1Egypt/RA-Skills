const { request, pick, withResolvedShopId } = require('./_http');

module.exports = async function getMemberInfo(params) {
  const memberId = params.memberId;
  if (!memberId) {
    return { success: false, error: 'memberId 不能为空' };
  }
  return request('GET', `/member/${memberId}`, {
    query: withResolvedShopId(pick(params, ['saasId', 'tenantId', 'shopId'])),
  });
};
