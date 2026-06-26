const axios = require('axios');
const { wenjuanUrl } = require('./api_config');

// API 地址
const IMPORT_URL = wenjuanUrl('/edit/api/textproject/?jwt=1');

/**
 * 导入项目
 * @param {Object} projectData - 项目数据
 * @param {string} jwtToken - JWT认证令牌
 */
async function importProject(projectData, jwtToken) {
  const headers = {
    Authorization: `Bearer ${jwtToken}`,
    'Content-Type': 'application/json',
  };

  try {
    const response = await axios.post(
      IMPORT_URL,
      { project_json: projectData },
      { headers, timeout: 30000 }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      return { error: `请求失败: ${error.response.status} ${error.response.statusText}` };
    }
    return { error: `请求失败: ${error.message}` };
  }
}

/**
 * 轮询导入状态
 * @param {string} fingerprint - 导入任务标识
 * @param {string} jwtToken - JWT认证令牌
 * @param {number} maxAttempts - 最大尝试次数
 */
async function pollImportStatus(fingerprint, jwtToken, maxAttempts = 30) {
  const headers = {
    Authorization: `Bearer ${jwtToken}`,
    'Content-Type': 'application/json',
  };

  for (let i = 0; i < maxAttempts; i++) {
    await new Promise((resolve) => setTimeout(resolve, 1000));

    try {
      const response = await axios.get(`${IMPORT_URL}&fingerprint=${fingerprint}`, {
        headers,
        timeout: 30000,
      });
      const status = response.data;
      const data = status.data || {};

      if (!data.continue_poll) {
        const projectId = data.project_id;
        if (projectId) {
          return {
            success: true,
            project_id: projectId,
            short_id: data.short_id || '',
          };
        }
        return {
          success: false,
          error: 'IMPORT_FAILED',
          message: '导入失败',
        };
      }

      console.log(`   导入中... (${i + 1}/${maxAttempts})`);
    } catch (error) {
      console.log(`   查询状态出错: ${error.message}，继续轮询...`);
    }
  }

  return { success: false, error: 'IMPORT_TIMEOUT', message: '导入超时' };
}

module.exports = {
  importProject,
  pollImportStatus,
};
