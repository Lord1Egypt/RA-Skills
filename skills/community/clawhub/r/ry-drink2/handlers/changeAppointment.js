const { request, pick, withResolvedShopId } = require('./_http');

module.exports = async function changeAppointment(params) {
  const body = withResolvedShopId(pick(params, [
    'saasId',
    'tenantId',
    'shopId',
    'reserveId',
    'linkNickname',
    'linkPhone',
    'dineDate',
    'dineTime',
    'tableCode',
    'personNum',
  ]));
  if (!body.reserveId) {
    return { success: false, error: 'reserveId 不能为空' };
  }
  return request('POST', '/aiemployees/appointment/change', { body });
};
