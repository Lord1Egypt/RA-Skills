const { request, pick, withDefaults, buildContextHeaders } = require('./_http');

module.exports = async function listMyAppointments(params) {
  const normalized = withDefaults(pick(params, ['saasId', 'linkPhone', 'bookingStatus', 'tenantId', 'shopId']));
  if (!normalized.linkPhone) {
    return {
      success: false,
      error: 'linkPhone 不能为空，请使用会话已绑定手机号或向顾客确认手机号',
    };
  }
  if (!normalized.saasId) {
    return { success: false, error: '缺少 saasId，请确认门店已绑定 SaaS' };
  }
  return request('GET', '/aiemployees/appointment/list', {
    query: pick(normalized, ['saasId', 'linkPhone', 'bookingStatus']),
    headers: buildContextHeaders(normalized),
  });
};
