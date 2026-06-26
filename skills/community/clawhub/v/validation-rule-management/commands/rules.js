const { apiRequest } = require('../lib/api-client');
const { int, ok, requireParams } = require('../lib/utils');

/**
 * 校验规则操作
 * 接口前缀：/admin/validateRule
 */
module.exports = {

  async 'create-rule'(p) {
    requireParams(p, ['groupId', 'objectId', 'countryCode', 'ruleCode', 'ruleName', 'ruleType']);
    const result = await apiRequest('/admin/validateRule/create', 'POST', {
      groupId:        int(p.groupId),
      objectId:       p.objectId,
      countryCode:    p.countryCode,
      ruleCode:       p.ruleCode,
      ruleName:       p.ruleName,
      description:    p.description    || '',
      preconditions:  p.preconditions  || '',
      fieldKey:       p.fieldKey       || '',
      ruleType:       p.ruleType,
      errorLevel:     p.errorLevel     || 'error',
      errorCode:      p.errorCode      || '',
      errorMessage:   p.errorMessage   || '',
      executionOrder: int(p.executionOrder, 1),
      status:         p.status         || 'draft',
      effectiveStart: p.effectiveStart || '',
      effectiveEnd:   p.effectiveEnd   || '',
      extensions:     {},
    });
    ok('规则创建成功', result);
  },

  async 'query-rules'(p) {
    const result = await apiRequest('/admin/validateRule/queryPageList', 'POST', {
      groupId:     p.groupId     ? int(p.groupId) : undefined,
      objectId:    p.objectId    || '',
      countryCode: p.countryCode || '',
      ruleCode:    p.ruleCode    || '',
      ruleName:    p.ruleName    || '',
      fieldKey:    p.fieldKey    || '',
      ruleType:    p.ruleType    || '',
      status:      p.status      || '',
      pageNum:     int(p.pageNum,  1),
      pageSize:    int(p.pageSize, 10),
    });
    ok('查询成功', result);
  },

  async 'enable-rule'(p) {
    requireParams(p, ['id', 'status']);
    const isEnable = p.status === 'enabled';
    const endpoint = isEnable ? '/admin/validateRule/enable' : '/admin/validateRule/disable';
    ok(`规则已${isEnable ? '启用' : '禁用'}`, await apiRequest(endpoint, 'POST', { id: int(p.id) }));
  },

  async 'delete-rule'(p) {
    requireParams(p, ['id']);
    ok('规则删除成功', await apiRequest('/admin/validateRule/delete', 'POST', { id: int(p.id) }));
  },

};
