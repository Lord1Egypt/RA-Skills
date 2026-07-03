const { request, pick } = require('./_http');

module.exports = async function reduceOrder(params) {
  const body = pick(params, ['saasId', 'tenantId', 'orderId', 'goods']);
  if (!body.orderId || !body.goods || !body.goods.length) {
    return { success: false, error: 'orderId 与 goods 不能为空' };
  }
  return request('POST', '/aiemployees/dining/reduce', { body });
};
