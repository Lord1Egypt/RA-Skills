const { request, pick } = require('./_http');

module.exports = async function listMyAppointments(params) {
  if (!params.linkPhone) {
    return { success: false, error: 'linkPhone 不能为空' };
  }
  return request('GET', '/aiemployees/appointment/list', {
    query: pick(params, ['saasId', 'linkPhone', 'bookingStatus']),
  });
};
