const { apiRequest } = require('../lib/api-client');
const { int, ok, requireParams } = require('../lib/utils');

/**
 * 规则组操作
 * 接口前缀：/admin/validateRuleGroup
 */
module.exports = {

  async 'create-rule-group'(p) {
    requireParams(p, ['groupName', 'orderNum']);
    const result = await apiRequest('/admin/validateRuleGroup/create', 'POST', {
      groupName:   p.groupName,
      description: p.description || '',
      orderNum:    int(p.orderNum, 1),
      parentId:    int(p.parentId, 0),
      tenantId:    int(p.tenantId, 0),
    });
    ok('规则组创建成功', result);
  },

  async 'query-rule-groups'(p) {
    const result = await apiRequest('/admin/validateRuleGroup/queryPageList', 'POST', {
      id:        p.id        ? int(p.id)       : undefined,
      parentId:  p.parentId  !== undefined ? int(p.parentId) : undefined,
      groupName: p.groupName || '',
      pageNum:   int(p.pageNum,  1),
      pageSize:  int(p.pageSize, 10),
    });
    ok('查询成功', result);
  },

  async 'update-rule-group'(p) {
    requireParams(p, ['id', 'groupName', 'orderNum']);
    const result = await apiRequest('/admin/validateRuleGroup/update', 'POST', {
      id:          int(p.id),
      groupName:   p.groupName,
      description: p.description || '',
      orderNum:    int(p.orderNum, 1),
      parentId:    int(p.parentId, 0),
    });
    ok('规则组更新成功', result);
  },

  async 'delete-rule-group'(p) {
    requireParams(p, ['id']);
    ok('规则组删除成功', await apiRequest('/admin/validateRuleGroup/delete', 'POST', { id: int(p.id) }));
  },

};
