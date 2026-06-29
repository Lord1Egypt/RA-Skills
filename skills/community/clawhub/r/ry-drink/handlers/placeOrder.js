const { request, pick, withResolvedShopId } = require('./_http');

module.exports = async function placeOrder(params) {
  const body = withResolvedShopId(pick(params, ['saasId', 'tenantId', 'shopId', 'reserveId', 'goods']));
  if (!body.reserveId || !body.goods || !body.goods.length) {
    return { success: false, error: 'reserveId 与 goods 不能为空' };
  }
  return request('POST', '/aiemployees/dining/order', { body });
};
