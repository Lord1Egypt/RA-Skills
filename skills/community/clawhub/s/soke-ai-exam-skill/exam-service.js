import apiClient from './api-client.js';
import FormData from 'form-data';
import fs from 'fs';
import { config } from './config.js';

/**
 * AI考试服务
 */
export class ExamService {
  /**
   * 上传文件到大模型
   * @param {string} filePath - 文件路径
   * @param {string} type - 文件类型 (document)
   * @param {string} from - 来源 (examPool)
   * @param {string} permissionUserId - 权限用户ID
   * @returns {Promise<Object>} 文件信息
   */
  async uploadFile(filePath, type = 'document', from = 'examPool', permissionUserId = config.deptUserId) {
    if (!fs.existsSync(filePath)) {
      throw new Error(`文件不存在: ${filePath}`);
    }

    const formData = new FormData();
    formData.append('type', type);
    formData.append('from', from);
    formData.append('permission_user_id', permissionUserId);
    formData.append('file', fs.createReadStream(filePath));

    const result = await apiClient.request('POST', '/ai/uploadFiles', formData);

    if (result.code === '200') {
      return result.data;
    }
    throw new Error(result.message || '上传文件失败');
  }

  /**
   * AI出题
   * @param {Object} options - 出题选项
   * @returns {Promise<Object>} 考试信息
   */
  async createExam(options) {
    const {
      fileIds,
      questionTypes,
      title,
      userId,
      userName,
      deptUserId,
      deptUserName,
      from = 'AiExamPool'
    } = options;

    const data = {
      ids: JSON.stringify(fileIds),
      types: JSON.stringify(questionTypes),
      from,
      title,
      step: 'start',
      user_id: userId,
      user_name: userName,
      dept_user_id: deptUserId,
      dept_user_name: deptUserName
    };

    const result = await apiClient.request('POST', '/exam/exam/create', data);

    if (result.code === '200') {
      return result.data.data;
    }
    throw new Error(result.message || '出题失败');
  }

  /**
   * 考试指派
   * @param {string} examId - 考试ID
   * @param {Array<string>} userIds - 用户ID列表
   * @param {Array<string>} deptIds - 部门ID列表
   * @param {Object} operator - 操作者信息
   * @returns {Promise<Object>} 指派结果
   */
  async assignExam(examId, userIds = [], deptIds = [], operator = {}) {
    const data = {
      exam_id: examId,
      assign_user_ids: userIds.join(','),
      assign_dept_ids: deptIds.join(','),
      user_id: operator.userId,
      user_name: operator.userName,
      dept_user_id: operator.deptUserId,
      dept_user_name: operator.deptUserName
    };

    const result = await apiClient.request('POST', '/exam/user/assign', data);

    if (result.code === '200' || result.code === 200) {
      return result;
    }
    throw new Error(result.message || '指派失败');
  }

  /**
   * 获取考试学员详情
   * @param {string} examId - 考试ID
   * @param {string} deptUserId - 部门用户ID
   * @returns {Promise<Object>} 学员考试详情
   */
  async getUserExamInfo(examId, deptUserId) {
    const result = await apiClient.request(
      'GET',
      '/exam/user/info',
      null,
      { exam_id: examId, dept_user_id: deptUserId }
    );

    if (result.code === '200') {
      return result.data;
    }
    throw new Error(result.message || '获取学员详情失败');
  }
}

export const examService = new ExamService();
