const { request, pick, withResolvedShopId } = require('./_http');

module.exports = async function appendOrder(params) {
  const body = withResolvedShopId(pick(params, ['saasId', 'tenantId', 'orderId', 'shopId', 'goods']));
  if (!body.orderId || !body.goods || !body.goods.length) {
    return { success: false, error: 'orderId 与 goods 不能为空' };
  }
  return request('POST', '/aiemployees/dining/append', { body });
};
