const { request, pick } = require('./_http');

module.exports = async function getOrderDetail(params) {
  const body = pick(params, ['saasId', 'tenantId', 'orderId']);
  if (!body.orderId) {
    return { success: false, error: 'orderId 不能为空' };
  }
  return request('POST', '/aiemployees/dining/detail', { body });
};
