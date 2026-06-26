import apiClient from './api-client.js';

/**
 * 部门服务
 */
export class DepartmentService {
  /**
   * 通过部门名称查询部门ID
   * @param {string} deptName - 部门名称
   * @returns {Promise<Array>} 部门列表
   */
  async searchByName(deptName) {
    const result = await apiClient.request(
      'POST',
      '/oa/department/searchDepartmentByName',
      { dept_name: deptName }
    );

    if (result.code === '200') {
      return result.data.list;
    }
    throw new Error(result.message || '查询部门失败');
  }

  /**
   * 获取部门ID（返回第一个匹配的部门）
   * @param {string} deptName - 部门名称
   * @returns {Promise<string>} 部门ID
   */
  async getDeptId(deptName) {
    const depts = await this.searchByName(deptName);
    if (depts.length === 0) {
      throw new Error(`未找到部门: ${deptName}`);
    }
    return depts[0].dept_id;
  }
}

/**
 * 用户服务
 */
export class UserService {
  /**
   * 通过用户名查询用户ID
   * @param {string} userName - 用户名
   * @param {number} pageSize - 分页大小
   * @returns {Promise<Array>} 用户列表
   */
  async searchByName(userName, pageSize = 10) {
    const result = await apiClient.request(
      'POST',
      '/oa/departmentUser/searchDepartmentUserByName',
      null,
      { page_size: pageSize, dept_user_name: userName }
    );

    if (result.code === '200') {
      return result.data.list;
    }
    throw new Error(result.message || '查询用户失败');
  }

  /**
   * 获取用户ID（返回第一个匹配的用户）
   * @param {string} userName - 用户名
   * @returns {Promise<string>} 用户ID
   */
  async getUserId(userName) {
    const users = await this.searchByName(userName);
    if (users.length === 0) {
      throw new Error(`未找到用户: ${userName}`);
    }
    return users[0].dept_user_id;
  }
}

export const departmentService = new DepartmentService();
export const userService = new UserService();
