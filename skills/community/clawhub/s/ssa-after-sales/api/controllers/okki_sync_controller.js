/**
 * OKKI 同步控制器
 * 负责将投诉/返单记录同步到 OKKI CRM 作为跟进记录（trail_type=107 售后跟进）
 */

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
  // OKKI CLI 路径（支持环境变量覆盖）
  okkiCliPath: process.env.OKKI_CLI_PATH || path.resolve(__dirname, '../../../../xiaoman-okki/api/okki_cli.py'),
  
  // OKKI Python 客户端路径（支持环境变量覆盖）
  okkiClientPath: process.env.OKKI_CLIENT_PATH || path.resolve(__dirname, '../../../../xiaoman-okki/api/okki_client.py'),
  
  // OKKI 工作区根目录（用于 Python path）
  okkiWorkspacePath: process.env.OKKI_WORKSPACE_PATH || path.resolve(__dirname, '../../../../xiaoman-okki/api'),
  
  // Trail 类型
  TRAIL_TYPE: {
    QUOTATION: 101,      // 快速记录
    EMAIL: 102,          // 邮件备注
    PHONE: 103,          // 电话
    INSPECTION: 104,     // 会面/验货跟进
    SOCIAL: 105,         // 社交平台
    AFTER_SALES: 107     // 售后跟进
  }
};

// ==================== 工具函数 ====================

/**
 * 执行 Python 脚本
 */
function execPython(scriptPath, args = [], options = {}) {
  return new Promise((resolve, reject) => {
    const pythonPath = 'python3';
    const fullArgs = [scriptPath, ...args];
    
    execFile(pythonPath, fullArgs, {
      timeout: options.timeout || 15000,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`Python 执行失败：${error.message}\n${stderr}`));
        return;
      }
      
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        resolve({ raw: stdout, stderr });
      }
    });
  });
}

/**
 * 执行 OKKI CLI 命令
 */
function execOkkiCli(args = [], options = {}) {
  return new Promise((resolve, reject) => {
    const fullArgs = [CONFIG.okkiCliPath, ...args];
    
    execFile('python3', fullArgs, {
      timeout: options.timeout || 15000,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(`OKKI CLI 执行失败：${error.message}\n${stderr}`));
        return;
      }
      
      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        resolve({ raw: stdout, stderr });
      }
    });
  });
}

/**
 * 通过客户 ID 查找 OKKI 公司
 * @param {string} customerId - 客户 ID
 * @param {string} customerName - 客户名称（备用）
 * @returns {Promise<{company_id: string, name: string, match_type: string} | null>}
 */
async function findCompanyByCustomerId(customerId, customerName = null) {
  try {
    // 方法 1: 使用客户 ID 直接搜索
    if (customerId) {
      const searchResult = await execOkkiCli([
        'search_company',
        customerId
      ]);
      
      if (searchResult && searchResult.companies && searchResult.companies.length > 0) {
        const company = searchResult.companies[0];
        return {
          company_id: company.company_id || company.id,
          name: company.name,
          match_type: 'customer_id'
        };
      }
    }
    
    // 方法 2: 使用客户名称搜索
    if (customerName) {
      const searchResult = await execOkkiCli([
        'search_company',
        customerName
      ]);
      
      if (searchResult && searchResult.companies && searchResult.companies.length > 0) {
        const company = searchResult.companies[0];
        return {
          company_id: company.company_id || company.id,
          name: company.name,
          match_type: 'customer_name'
        };
      }
    }
    
    return null;
  } catch (e) {
    console.error('查找 OKKI 客户失败:', e.message);
    return null;
  }
}

/**
 * 创建售后跟进记录
 * @param {string} companyId - OKKI 客户 ID
 * @param {object} data - 售后数据
 * @param {string} type - 类型：complaint 或 repeat_order
 * @returns {Promise<object>}
 */
async function createAfterSalesTrail(companyId, data, type) {
  let content;
  
  if (type === 'complaint') {
    const statusLabel = data.status === 'resolved' ? '✅ 已解决' : 
                       data.status === 'pending' ? '⏳ 处理中' : 
                       data.status === 'closed' ? '🔒 已关闭' : data.status;
    
    content = `⚠️ 客户投诉\n` +
      `投诉编号：${data.complaintId}\n` +
      `投诉类型：${data.type || '(未指定)'}\n` +
      `产品型号：${data.productModel || '(未指定)'}\n` +
      `投诉日期：${data.createdAt}\n` +
      `处理状态：${statusLabel}\n` +
      `严重程度：${data.severity || '(未指定)'}\n` +
      `投诉描述：${data.description || '(无)'}\n` +
      `\n备注：${data.notes || '(无)'}`;
  } else if (type === 'repeat_order') {
    content = `🔄 返单报价\n` +
      `返单编号：${data.repeatOrderId}\n` +
      `原订单号：${data.originalOrderId || '(无)'}\n` +
      `报价单号：${data.quotationNo || '(未生成)'}\n` +
      `返单金额：${data.amount ? `$${data.amount}` : '(未指定)'}\n` +
      `产品型号：${data.productModel || '(未指定)'}\n` +
      `数量：${data.quantity || '(未指定)'}\n` +
      `报价日期：${data.quotationDate || data.createdAt}\n` +
      `客户备注：${data.notes || '(无)'}`;
  }
  
  try {
    // 使用 OKKI CLI 创建跟进记录（带 trail_type 参数）
    const result = await execOkkiCli([
      'add_trail',
      companyId,
      content,
      '--type',
      CONFIG.TRAIL_TYPE.AFTER_SALES.toString()
    ]);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add',
      trail_type: CONFIG.TRAIL_TYPE.AFTER_SALES
    };
  } catch (e) {
    console.warn('OKKI CLI 创建跟进失败，尝试 Python 客户端:', e.message);
    return await createAfterSalesTrailViaPython(companyId, data, type);
  }
}

/**
 * 通过 Python 客户端创建售后跟进记录（回退方案）
 */
async function createAfterSalesTrailViaPython(companyId, data, type) {
  let content;
  
  if (type === 'complaint') {
    const statusLabel = data.status === 'resolved' ? '✅ 已解决' : 
                       data.status === 'pending' ? '⏳ 处理中' : 
                       data.status === 'closed' ? '🔒 已关闭' : data.status;
    
    content = `⚠️ 客户投诉\n` +
      `投诉编号：${data.complaintId}\n` +
      `投诉类型：${data.type || '(未指定)'}\n` +
      `产品型号：${data.productModel || '(未指定)'}\n` +
      `投诉日期：${data.createdAt}\n` +
      `处理状态：${statusLabel}\n` +
      `投诉描述：${data.description || '(无)'}`;
  } else if (type === 'repeat_order') {
    content = `🔄 返单报价\n` +
      `返单编号：${data.repeatOrderId}\n` +
      `返单金额：${data.amount ? `$${data.amount}` : '(未指定)'}\n` +
      `报价单号：${data.quotationNo || '(未生成)'}\n` +
      `产品型号：${data.productModel || '(未指定)'}\n` +
      `报价日期：${data.quotationDate || data.createdAt}`;
  }
  
  try {
    // 创建临时 Python 脚本调用 OKKI 客户端
    const tempScript = `
import sys
sys.path.insert(0, '${CONFIG.okkiWorkspacePath.replace(/\\/g, '\\\\')}')
from okki_client import OKKIClient
import json

client = OKKIClient()
result = client.create_trail(
  company_id=${companyId},
  content='''${content.replace(/'/g, "\\'")}''',
  trail_type=${CONFIG.TRAIL_TYPE.AFTER_SALES}
)
print(json.dumps(result))
`.trim();
    
    const tempScriptPath = '/tmp/okki_trail_' + Date.now() + '.py';
    fs.writeFileSync(tempScriptPath, tempScript);
    
    const result = await execPython(tempScriptPath);
    
    // 清理临时文件
    try { fs.unlinkSync(tempScriptPath); } catch (e) {}
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.data?.trail_id || result.trail_id,
      action: 'trail.add',
      trail_type: CONFIG.TRAIL_TYPE.AFTER_SALES
    };
  } catch (e) {
    return {
      success: false,
      reason: 'api_error',
      message: e.message,
      company_id: companyId
    };
  }
}

/**
 * 同步投诉记录到 OKKI（主入口函数）
 * @param {string} complaintId - 投诉 ID
 * @returns {Promise<object>}
 */
async function syncComplaintToOKKI(complaintId) {
  try {
    // 1. 获取投诉记录详情
    // 注意：实际应用中应从数据库获取，这里使用模拟数据
    const complaintData = getComplaintData(complaintId);
    
    if (!complaintData) {
      return {
        success: false,
        message: '投诉记录不存在',
        complaintId
      };
    }
    
    // 2. 查找关联的 OKKI 客户
    const company = await findCompanyByCustomerId(
      complaintData.customerId, 
      complaintData.customerName
    );
    
    if (!company) {
      return {
        success: false,
        message: '未找到关联的 OKKI 客户',
        complaintId,
        customerId: complaintData.customerId,
        note: '无法通过客户 ID/名称匹配客户，请手动关联'
      };
    }
    
    // 3. 创建 OKKI 跟进记录
    const trailResult = await createAfterSalesTrail(company.company_id, complaintData, 'complaint');
    
    if (!trailResult.success) {
      return {
        success: false,
        message: '创建 OKKI 跟进记录失败',
        complaintId,
        companyId: company.company_id,
        error: trailResult.message
      };
    }
    
    // 4. 记录同步日志
    const { OkkiSyncLog } = require('../models/okki_sync_log_model');
    const logEntry = OkkiSyncLog.create({
      complaintId,
      companyId: company.company_id,
      trailId: trailResult.trail_id,
      status: 'success',
      syncType: 'complaint',
      matchType: company.match_type
    });
    
    return {
      success: true,
      complaintId,
      companyId: company.company_id,
      companyName: company.name,
      trailId: trailResult.trail_id,
      trailType: CONFIG.TRAIL_TYPE.AFTER_SALES,
      matchType: company.match_type,
      logId: logEntry.id,
      message: '投诉记录已成功同步到 OKKI'
    };
    
  } catch (error) {
    console.error('同步投诉记录到 OKKI 失败:', error);
    
    // 记录失败日志
    try {
      const { OkkiSyncLog } = require('../models/okki_sync_log_model');
      OkkiSyncLog.create({
        complaintId,
        status: 'failed',
        syncType: 'complaint',
        errorMessage: error.message
      });
    } catch (e) {
      console.warn('记录同步日志失败:', e.message);
    }
    
    return {
      success: false,
      complaintId,
      message: '同步失败',
      error: error.message
    };
  }
}

/**
 * 同步返单报价到 OKKI（主入口函数）
 * @param {string} repeatOrderId - 返单 ID
 * @returns {Promise<object>}
 */
async function syncRepeatOrderToOKKI(repeatOrderId) {
  try {
    // 1. 获取返单记录详情
    const repeatOrderData = getRepeatOrderData(repeatOrderId);
    
    if (!repeatOrderData) {
      return {
        success: false,
        message: '返单记录不存在',
        repeatOrderId
      };
    }
    
    // 2. 查找关联的 OKKI 客户
    const company = await findCompanyByCustomerId(
      repeatOrderData.customerId, 
      repeatOrderData.customerName
    );
    
    if (!company) {
      return {
        success: false,
        message: '未找到关联的 OKKI 客户',
        repeatOrderId,
        customerId: repeatOrderData.customerId,
        note: '无法通过客户 ID/名称匹配客户，请手动关联'
      };
    }
    
    // 3. 创建 OKKI 跟进记录
    const trailResult = await createAfterSalesTrail(company.company_id, repeatOrderData, 'repeat_order');
    
    if (!trailResult.success) {
      return {
        success: false,
        message: '创建 OKKI 跟进记录失败',
        repeatOrderId,
        companyId: company.company_id,
        error: trailResult.message
      };
    }
    
    // 4. 记录同步日志
    const { OkkiSyncLog } = require('../models/okki_sync_log_model');
    const logEntry = OkkiSyncLog.create({
      repeatOrderId,
      companyId: company.company_id,
      trailId: trailResult.trail_id,
      status: 'success',
      syncType: 'repeat_order',
      matchType: company.match_type
    });
    
    return {
      success: true,
      repeatOrderId,
      companyId: company.company_id,
      companyName: company.name,
      trailId: trailResult.trail_id,
      trailType: CONFIG.TRAIL_TYPE.AFTER_SALES,
      matchType: company.match_type,
      logId: logEntry.id,
      message: '返单报价已成功同步到 OKKI'
    };
    
  } catch (error) {
    console.error('同步返单报价到 OKKI 失败:', error);
    
    // 记录失败日志
    try {
      const { OkkiSyncLog } = require('../models/okki_sync_log_model');
      OkkiSyncLog.create({
        repeatOrderId,
        status: 'failed',
        syncType: 'repeat_order',
        errorMessage: error.message
      });
    } catch (e) {
      console.warn('记录同步日志失败:', e.message);
    }
    
    return {
      success: false,
      repeatOrderId,
      message: '同步失败',
      error: error.message
    };
  }
}

/**
 * 获取投诉数据（模拟，实际应从数据库获取）
 */
function getComplaintData(complaintId) {
  // 模拟数据 - 实际应用中应从数据库获取
  const mockComplaints = {
    'CMP-001': {
      complaintId: 'CMP-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      productId: 'PROD-001',
      productName: 'HDMI Cable 2.0',
      productModel: 'HDMI-2.0-2M',
      type: 'quality',
      status: 'resolved',
      description: 'Cable stopped working after 2 weeks',
      createdAt: '2026-03-10',
      resolvedAt: '2026-03-15',
      severity: 'medium',
      notes: 'Replacement sent'
    },
    'CMP-002': {
      complaintId: 'CMP-002',
      customerId: 'CUST-002',
      customerName: 'XYZ Electronics Inc.',
      productId: 'PROD-003',
      productName: 'USB-C Cable',
      productModel: 'USBC-3.0-1M',
      type: 'delivery',
      status: 'pending',
      description: 'Delivery delayed by 1 week',
      createdAt: '2026-03-20',
      resolvedAt: null,
      severity: 'low',
      notes: ''
    }
  };
  
  return mockComplaints[complaintId] || null;
}

/**
 * 获取返单数据（模拟，实际应从数据库获取）
 */
function getRepeatOrderData(repeatOrderId) {
  // 模拟数据 - 实际应用中应从数据库获取
  const mockRepeatOrders = {
    'RO-001': {
      repeatOrderId: 'RO-001',
      customerId: 'CUST-001',
      customerName: 'ABC Trading Ltd.',
      originalOrderId: 'ORD-2025-001',
      quotationNo: 'QT-2026-050',
      productModel: 'HDMI-2.1-3M',
      quantity: 500,
      amount: 2500.00,
      quotationDate: '2026-03-25',
      createdAt: '2026-03-25',
      notes: 'Repeat order for HDMI 2.1 cables'
    },
    'RO-002': {
      repeatOrderId: 'RO-002',
      customerId: 'CUST-003',
      customerName: 'Global Tech Solutions',
      originalOrderId: 'ORD-2025-015',
      quotationNo: 'QT-2026-055',
      productModel: 'DP-1.4-2M',
      quantity: 300,
      amount: 1800.00,
      quotationDate: '2026-03-26',
      createdAt: '2026-03-26',
      notes: 'Customer requested faster delivery'
    }
  };
  
  return mockRepeatOrders[repeatOrderId] || null;
}

// 导出函数
module.exports = {
  syncComplaintToOKKI,
  syncRepeatOrderToOKKI,
  findCompanyByCustomerId,
  createAfterSalesTrail,
  CONFIG
};
