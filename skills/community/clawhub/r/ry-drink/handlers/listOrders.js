const { pick, invokeDiningTool } = require('./_http');

module.exports = async function listOrders(params) {
  const args = pick(params, ['saasId', 'tenantId', 'reserveId']);
  if (!args.reserveId) {
    return { success: false, error: 'reserveId 不能为空' };
  }
  return invokeDiningTool('dining_order_list', args);
};
