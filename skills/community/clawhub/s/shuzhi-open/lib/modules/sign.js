/**
 * 电子签章组件模块
 * 包含文件管理、企业/个人主体管理、印章管理、合同模板管理、签署流程管理
 */

const { request } = require('../client');

// ==================== 文件模块 ====================

const file = {
  /**
   * 上传文件（Base64）
   * @param {string} inputSource - Base64编码的文件内容
   * @param {string} fileName - 文件名
   * @param {string} fileExt - 文件后缀，如 '.pdf'
   * @returns {Promise<{fileId: number, fileName: string, filePath: string}>}
   */
  async upload(inputSource, fileName, fileExt) {
    return request('sign', 'fileUpload', { inputSource, fileName, fileExt });
  },

  /**
   * Word转PDF（Base64）
   * @param {string} inputSource - Base64编码的Word文件内容
   * @param {string} fileName - 文件名
   * @param {string} fileExt - 文件后缀，如 '.docx'
   * @returns {Promise<string>} PDF临时下载链接（有效期1小时）
   */
  async wordToPdf(inputSource, fileName, fileExt) {
    return request('sign', 'wordToPdf', { inputSource, fileName, fileExt });
  },

  /**
   * 文件下载
   * @param {string} fileName - 文件名
   * @returns {Promise<Buffer>} 文件流
   */
  async download(fileName) {
    // 注意：此接口返回文件流，需要特殊处理
    const result = await request('sign', 'fileDownload', { fileName });
    return result;
  },

  /**
   * 上传印章文件（Base64）
   * @param {string} inputSource - Base64编码的印章图片
   * @param {number} type - 类型：0=企业，1=个人
   * @param {string} fileName - 文件名
   * @param {string} fileExt - 文件后缀，如 '.png'
   * @returns {Promise<{fileId: number}>}
   */
  async uploadSeal(inputSource, type, fileName, fileExt) {
    return request('sign', 'sealFileUpload', { inputSource, type, fileName, fileExt });
  },

  /**
   * 获取文件详情
   * @param {string|number} dscFileId - 文件ID
   * @returns {Promise<object>}
   */
  async getDetail(dscFileId) {
    return request('sign', 'fileDetail', { dscFileId });
  }
};

// ==================== 企业主体管理 ====================

const enterprise = {
  /**
   * 创建企业主体信息
   * @param {string} principalName - 企业名称
   * @param {string} unifiedSocialCreditCode - 统一社会信用代码
   * @param {number} [isTemp=0] - 是否临时：0=否，1=是
   * @returns {Promise<{userId: number, principalName: string}>}
   */
  async create(principalName, unifiedSocialCreditCode, isTemp = 0) {
    return request('sign', 'enterpriseCreate', { 
      principalName, 
      unifiedSocialCreditCode, 
      isTemp 
    });
  },

  /**
   * 查询企业主体列表
   * @param {string} [principalName] - 企业名称（模糊查询）
   * @param {string} [unifiedSocialCreditCode] - 统一社会信用代码
   * @returns {Promise<Array>}
   */
  async list(principalName, unifiedSocialCreditCode) {
    return request('sign', 'enterpriseList', { 
      principalName, 
      unifiedSocialCreditCode 
    });
  },

  /**
   * 查询企业主体详情
   * @param {string|number} userId - 用户ID
   * @returns {Promise<object>}
   */
  async detail(userId) {
    return request('sign', 'enterpriseDetail', { userId });
  },

  /**
   * 删除企业主体
   * @param {string|number} userId - 用户ID
   * @returns {Promise<boolean>}
   */
  async delete(userId) {
    return request('sign', 'enterpriseDelete', { userId });
  }
};

// ==================== 个人主体管理 ====================

const person = {
  /**
   * 创建个人主体信息
   * @param {string} name - 姓名
   * @param {string} idCard - 身份证号
   * @param {number} [isTemp=0] - 是否临时
   * @returns {Promise<{userId: string, name: string}>}
   */
  async create(name, idCard, isTemp = 0) {
    return request('sign', 'personCreate', { name, idCard, isTemp });
  },

  /**
   * 查询个人主体列表
   * @param {string} [name] - 姓名（模糊查询）
   * @param {string} [idCard] - 身份证号
   * @returns {Promise<Array>}
   */
  async list(name, idCard) {
    return request('sign', 'personList', { name, idCard });
  },

  /**
   * 查询个人主体详情
   * @param {string|number} userId - 用户ID
   * @returns {Promise<object>}
   */
  async detail(userId) {
    return request('sign', 'personDetail', { userId });
  },

  /**
   * 删除个人主体
   * @param {string|number} userId - 用户ID
   * @returns {Promise<boolean>}
   */
  async delete(userId) {
    return request('sign', 'personDelete', { userId });
  }
};

// ==================== 企业印章管理 ====================

const enterpriseSeal = {
  /**
   * 创建企业印章
   * @param {object} params - 印章参数
   * @param {number} params.userId - 企业用户ID
   * @param {string} params.sealName - 印章名称
   * @param {number} params.enterpriseSealType - 印章类型：0=模板印章，1=自定义印章
   * @param {number} params.sealMode - 印章样式
   * @param {string} [params.sealPath] - 自定义印章图片路径（自定义印章时必填）
   * @param {string} [params.licenseProtocol] - 授权协议文件路径
   * @returns {Promise<{sealId: string, sealCode: string}>}
   */
  async create(params) {
    return request('sign', 'enterpriseSealCreate', params);
  },

  /**
   * 获取企业印章详情
   * @param {string|number} sealId - 印章ID
   * @returns {Promise<object>}
   */
  async detail(sealId) {
    return request('sign', 'enterpriseSealDetail', { sealId });
  },

  /**
   * 获取企业印章列表
   * @param {object} params - 查询参数
   * @param {string} [params.principalName] - 企业名称
   * @param {string} [params.unifiedSocialCreditCode] - 统一社会信用代码
   * @param {string} [params.sealName] - 印章名称
   * @param {number} [params.enterpriseSealType] - 印章类型
   * @returns {Promise<Array>}
   */
  async list(params) {
    return request('sign', 'enterpriseSealList', params);
  },

  /**
   * 删除企业印章
   * @param {string|number} sealId - 印章ID
   * @returns {Promise<boolean>}
   */
  async delete(sealId) {
    return request('sign', 'enterpriseSealDelete', { sealId });
  }
};

// ==================== 个人印章管理 ====================

const personSeal = {
  /**
   * 创建个人签名
   * @param {object} params - 签名参数
   * @param {number} params.userId - 个人用户ID
   * @param {string} params.sealName - 签名名称
   * @param {number} params.sealMode - 签名样式：0=模板签名，1=自定义签名
   * @param {string} [params.sealPath] - 自定义签名图片路径
   * @returns {Promise<{sealId: string, sealCode: string}>}
   */
  async create(params) {
    return request('sign', 'personSealCreate', params);
  },

  /**
   * 获取个人签名详情
   * @param {string|number} sealId - 印章ID
   * @returns {Promise<object>}
   */
  async detail(sealId) {
    return request('sign', 'personSealDetail', { sealId });
  },

  /**
   * 获取个人签名列表
   * @param {string} [name] - 姓名
   * @param {string} [idCard] - 身份证号
   * @returns {Promise<Array>}
   */
  async list(name, idCard) {
    return request('sign', 'personSealList', { name, idCard });
  },

  /**
   * 删除个人签名
   * @param {string|number} sealId - 印章ID
   * @returns {Promise<boolean>}
   */
  async delete(sealId) {
    return request('sign', 'personSealDelete', { sealId });
  }
};

// ==================== 合同模板管理 ====================

const template = {
  /**
   * 创建合同模板
   * @param {object} params - 模板参数
   * @param {string} params.templateName - 模板名称
   * @param {string} [params.completeCallbackUrl] - 配置完成回调URL
   * @param {Array} params.fileList - 文件列表
   * @returns {Promise<{templateId: number, previewUrl: string}>}
   */
  async create(params) {
    return request('sign', 'templateCreate', params);
  },

  /**
   * 获取合同模板详情
   * @param {string|number} templateId - 模板ID
   * @returns {Promise<object>}
   */
  async detail(templateId) {
    return request('sign', 'templateDetail', { templateId });
  },

  /**
   * 获取模板预览链接
   * @param {string|number} templateId - 模板ID
   * @returns {Promise<{templateId: number, previewUrl: string}>}
   */
  async preview(templateId) {
    return request('sign', 'templatePreview', { templateId });
  },

  /**
   * 删除合同模板
   * @param {string|number} templateId - 模板ID
   * @returns {Promise<boolean>}
   */
  async delete(templateId) {
    return request('sign', 'templateDelete', { templateId });
  }
};

// ==================== 签署流程管理 ====================

const signFlow = {
  /**
   * 创建签署流程
   * @param {object} params - 流程参数
   * @param {number} params.templateId - 模板ID
   * @param {Array} params.fileList - 文件列表（包含签署方和控件值）
   * @param {string} [params.createCallbackUrl] - 创建完成回调URL
   * @param {string} [params.signCallbackUrl] - 签署完成回调URL
   * @param {string} [params.signerCallbackUrl] - 签署方签署完成回调URL
   * @returns {Promise<{signFlowId: string, signFlowNo: string}>}
   */
  async create(params) {
    return request('sign', 'signFlowCreate', params);
  },

  /**
   * 获取签署流程详情
   * @param {string} signFlowId - 签署流程ID
   * @returns {Promise<object>}
   */
  async detail(signFlowId) {
    return request('sign', 'signFlowDetail', { signFlowId });
  },

  /**
   * 获取预览链接和签署链接
   * @param {string} signFlowId - 签署流程ID
   * @returns {Promise<{signFlowId: string, previewUrl: string, signUrl: string}>}
   */
  async preview(signFlowId) {
    return request('sign', 'signFlowPreview', { signFlowId });
  },

  /**
   * 获取签署流程的所有合同文件
   * @param {string} signFlowId - 签署流程ID
   * @returns {Promise<Array>}
   */
  async files(signFlowId) {
    return request('sign', 'signFlowFiles', { signFlowId });
  },

  /**
   * 获取签署流程的所有签署方
   * @param {string} signFlowId - 签署流程ID
   * @returns {Promise<Array>}
   */
  async signers(signFlowId) {
    return request('sign', 'signFlowSigners', { signFlowId });
  }
};

// ==================== 业务流程封装 ====================

const workflow = {
  /**
   * 快速创建企业印章（创建主体 + 创建印章）
   * @param {string} principalName - 企业名称
   * @param {string} creditCode - 统一社会信用代码
   * @param {number} [sealType=0] - 印章类型：0=模板印章，1=自定义印章
   * @param {string} [sealName] - 印章名称（默认使用企业名称）
   * @returns {Promise<{userId: number, sealId: string}>}
   */
  async createEnterpriseWithSeal(principalName, creditCode, sealType = 0, sealName) {
    // 创建企业主体
    const entResult = await enterprise.create(principalName, creditCode);
    
    // 创建印章
    const sealResult = await enterpriseSeal.create({
      userId: entResult.userId,
      sealName: sealName || principalName + '印章',
      enterpriseSealType: sealType,
      sealMode: 0
    });
    
    return {
      userId: entResult.userId,
      sealId: sealResult.sealId,
      sealCode: sealResult.sealCode
    };
  },

  /**
   * 快速创建个人签名
   * @param {string} name - 姓名
   * @param {string} idCard - 身份证号
   * @param {number} [sealMode=0] - 签名样式
   * @param {string} [sealName] - 签名名称
   * @returns {Promise<{userId: string, sealId: string}>}
   */
  async createPersonWithSeal(name, idCard, sealMode = 0, sealName) {
    // 创建个人主体
    const personResult = await person.create(name, idCard);
    
    // 创建签名
    const sealResult = await personSeal.create({
      userId: personResult.userId,
      sealName: sealName || name + '签名',
      sealMode
    });
    
    return {
      userId: personResult.userId,
      sealId: sealResult.sealId,
      sealCode: sealResult.sealCode
    };
  },

  /**
   * 等待签署完成（轮询）
   * @param {string} signFlowId - 签署流程ID
   * @param {object} options - 选项
   * @returns {Promise<object>}
   */
  async waitSigned(signFlowId, options = {}) {
    const { interval = 10000, timeout = 86400000, onProgress } = options;
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const flow = await signFlow.detail(signFlowId);
      
      if (onProgress) {
        onProgress(flow);
      }
      
      // signStatus: 1 = 已完成
      if (flow.signStatus === 1) {
        return flow;
      }
      
      await new Promise(resolve => setTimeout(resolve, interval));
    }
    
    throw new Error('等待签署超时');
  }
};

module.exports = {
  file,
  enterprise,
  person,
  enterpriseSeal,
  personSeal,
  template,
  signFlow,
  workflow
};