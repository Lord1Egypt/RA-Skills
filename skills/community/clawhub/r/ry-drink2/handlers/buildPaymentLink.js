const { request, pick, withDefaults } = require('./_http');

module.exports = async function buildPaymentLink(params) {
  const body = withDefaults(
    pick(params, ['saasId', 'tenantId', 'shopId', 'reserveId', 'orderId', 'thirdOrderId', 'linkPhone']),
  );
  if (!body.shopId) {
    return { success: false, error: '缺少 merchantId（shopId），无法生成付款链接' };
  }
  if (body.tenantId === undefined || body.tenantId === null || body.tenantId === '') {
    return { success: false, error: '缺少 tenantId，无法生成付款链接' };
  }
  if (!body.reserveId && !body.orderId && !body.thirdOrderId) {
    return {
      success: false,
      error: '缺少 reserveId 或 orderId 或 thirdOrderId，请先 listMyAppointments 获取预约后再生成付款链接',
    };
  }
  return request('POST', '/aiemployees/dining/payment/link', { body });
};
