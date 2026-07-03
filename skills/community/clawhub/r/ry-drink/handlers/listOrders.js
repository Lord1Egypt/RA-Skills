const { pick, withDefaults, invokeDiningTool, request } = require('./_http');

async function fetchOrderDetail(normalized, orderId) {
  if (!orderId) {
    return null;
  }
  const body = pick({ ...normalized, orderId }, ['saasId', 'tenantId', 'orderId']);
  const detailResult = await request('POST', '/aiemployees/dining/detail', { body });
  if (!detailResult.success) {
    return { orderId, error: detailResult.error || detailResult.msg || '查询详情失败' };
  }
  return detailResult.data ?? detailResult;
}

module.exports = async function listOrders(params) {
  const normalized = withDefaults(pick(params, ['saasId', 'tenantId', 'shopId', 'reserveId', 'linkPhone']));
  if (!normalized.reserveId) {
    return { success: false, error: 'reserveId 不能为空，请先 listMyAppointments 查询有效预约' };
  }

  const listResult = await invokeDiningTool('dining_order_list', pick(normalized, ['saasId', 'tenantId', 'reserveId']));
  if (!listResult.success) {
    return listResult;
  }

  const payload = listResult.data && typeof listResult.data === 'object' ? listResult.data : {};
  const list = Array.isArray(payload.list) ? payload.list : [];
  if (!list.length) {
    return listResult;
  }

  const details = [];
  for (const item of list) {
    const detail = await fetchOrderDetail(normalized, item?.orderId);
    if (detail) {
      details.push(detail);
    }
  }

  const mergedData = { ...payload, details };
  return {
    ...listResult,
    data: mergedData,
    details,
  };
};
