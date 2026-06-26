const { apiRequest } = require('../lib/api-client');
const { int, ok, requireParams } = require('../lib/utils');

/**
 * 校验场景操作
 * 接口前缀：/admin/validateScene
 */
module.exports = {

  async 'create-scene'(p) {
    requireParams(p, ['sceneCode', 'sceneName']);
    const result = await apiRequest('/admin/validateScene/create', 'POST', {
      sceneCode:     p.sceneCode,
      sceneName:     p.sceneName,
      description:   p.description   || '',
      status:        p.status        || 'draft',
      errorStrategy: p.errorStrategy || 'stop_on_error',
      extensions:    {},
      rules:         [],
    });
    ok('场景创建成功', result);
  },

  async 'query-scenes'(p) {
    const result = await apiRequest('/admin/validateScene/queryPageList', 'POST', {
      sceneCode: p.sceneCode || '',
      sceneName: p.sceneName || '',
      status:    p.status    || '',
      pageNum:   int(p.pageNum,  1),
      pageSize:  int(p.pageSize, 10),
    });
    ok('查询成功', result);
  },

  async 'enable-scene'(p) {
    requireParams(p, ['id', 'status']);
    const isEnable = p.status === 'enabled';
    const endpoint = isEnable ? '/admin/validateScene/enable' : '/admin/validateScene/disable';
    ok(`场景已${isEnable ? '启用' : '禁用'}`, await apiRequest(endpoint, 'POST', { id: int(p.id) }));
  },

  async 'delete-scene'(p) {
    requireParams(p, ['id']);
    ok('场景删除成功', await apiRequest('/admin/validateScene/delete', 'POST', { id: int(p.id) }));
  },

};
