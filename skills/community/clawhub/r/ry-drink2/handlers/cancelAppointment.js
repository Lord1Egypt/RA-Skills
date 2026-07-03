const { request, pick } = require('./_http');

module.exports = async function cancelAppointment(params) {
  const body = pick(params, ['saasId', 'tenantId', 'reserveId']);
  if (!body.reserveId) {
    return { success: false, error: 'reserveId 不能为空' };
  }
  if (!body.saasId || !body.tenantId) {
    return { success: false, error: 'saasId 与 tenantId 不能为空' };
  }
  return request('POST', '/aiemployees/appointment/cancel', { body });
};
