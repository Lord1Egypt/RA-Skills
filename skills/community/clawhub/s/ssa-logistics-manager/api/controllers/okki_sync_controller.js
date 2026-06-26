/**
 * OKKI 同步控制器
 * 负责将物流记录同步到 OKKI CRM 作为跟进记录（trail_type=105 发货跟进）
 */

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================
const CONFIG = {
  // OKKI CLI 路径
  okkiCliPath: '/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_cli.py',
  
  // OKKI Python 客户端路径
  okkiClientPath: '/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_client.py',
  
  // 物流模块路径（用于通过订单号查找客户）
  logisticsModulePath: '/Users/wilson/.openclaw/workspace/skills/logistics',
  
  // Trail 类型
  TRAIL_TYPE: {
    QUOTATION: 101,      // 快速记录
    EMAIL: 102,          // 邮件备注
    PHONE: 103,          // 电话
    INSPECTION: 104,     // 会面/验货跟进
    SHIPPING: 105        // 发货跟进
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
 * 通过订单号查找客户公司 ID
 * @param {string} orderId - 订单号
 * @returns {Promise<{company_id: string, name: string} | null>}
 */
async function findCompanyByOrderId(orderId) {
  try {
    // 方法 1: 直接使用订单号作为关键词搜索 OKKI 客户
    const searchResult = await execOkkiCli([
      'search_company',
      orderId
    ]);
    
    if (searchResult && searchResult.companies && searchResult.companies.length > 0) {
      return {
        company_id: searchResult.companies[0].company_id || searchResult.companies[0].id,
        name: searchResult.companies[0].name,
        match_type: 'order_id_search'
      };
    }
    
    // 方法 2: 尝试通过物流记录中的客户名称搜索
    const logisticsAPI = loadLogisticsAPI();
    if (logisticsAPI) {
      try {
        const logisticsList = await logisticsAPI.listLogisticsRecords({ orderId });
        if (logisticsList && logisticsList.length > 0) {
          const logistics = logisticsList[0];
          if (logistics.customerName) {
            const searchResult = await execOkkiCli([
              'search_company',
              logistics.customerName
            ]);
            
            if (searchResult && searchResult.companies && searchResult.companies.length > 0) {
              return {
                company_id: searchResult.companies[0].company_id || searchResult.companies[0].id,
                name: searchResult.companies[0].name,
                match_type: 'customer_name_search'
              };
            }
          }
        }
      } catch (e) {
        console.warn('通过物流记录查找客户失败:', e.message);
      }
    }
    
    return null;
  } catch (e) {
    console.error('查找客户公司失败:', e.message);
    return null;
  }
}

/**
 * 加载物流 API 模块
 */
function loadLogisticsAPI() {
  try {
    const logisticsAPI = require(CONFIG.logisticsModulePath + '/api/logistics_api.js');
    return logisticsAPI;
  } catch (error) {
    console.warn('加载物流模块失败:', error.message);
    return null;
  }
}

/**
 * 创建发货跟进记录
 * @param {string} companyId - OKKI 客户 ID
 * @param {object} logisticsData - 物流数据
 * @returns {Promise<object>}
 */
async function createShippingTrail(companyId, logisticsData) {
  // 构建跟进内容
  const statusLabel = logisticsData.status || '待发货';
  const transportLabel = logisticsData.transportMode || '海运';
  
  const content = `📦 发货跟进\n` +
    `物流编号：${logisticsData.logisticsId}\n` +
    `订单编号：${logisticsData.orderId}\n` +
    `运输方式：${transportLabel}\n` +
    `发货状态：${statusLabel}\n` +
    `提单号：${logisticsData.billOfLading?.blNo || '(未指定)'}\n` +
    `船名/航次：${logisticsData.vesselName || '(未指定)'} ${logisticsData.voyageNo ? '(' + logisticsData.voyageNo + ')' : ''}\n` +
    `ETD (预计离港): ${logisticsData.etd || '(未指定)'}\n` +
    `ETA (预计到港): ${logisticsData.eta || '(未指定)'}\n` +
    `起运港：${logisticsData.portOfLoading || '(未指定)'}\n` +
    `目的港：${logisticsData.portOfDischarge || '(未指定)'}\n` +
    `货物总量：${logisticsData.cargoInfo?.totalQuantity || 0} ${logisticsData.cargoInfo?.totalWeight ? `| ${logisticsData.cargoInfo.totalWeight}kg` : ''}\n` +
    `集装箱数：${logisticsData.containerInfo?.length || 0}\n` +
    `备注：${logisticsData.notes || '(无)'}`;
  
  try {
    // 使用 OKKI CLI 创建跟进记录（带 trail_type 参数）
    const result = await execOkkiCli([
      'add_trail',
      companyId,
      content,
      '--type',
      CONFIG.TRAIL_TYPE.SHIPPING.toString()
    ]);
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add',
      trail_type: CONFIG.TRAIL_TYPE.SHIPPING
    };
  } catch (e) {
    // 如果 CLI 不支持 --type 参数，回退到 Python 客户端
    console.warn('OKKI CLI 创建跟进失败，尝试 Python 客户端:', e.message);
    return await createShippingTrailViaPython(companyId, logisticsData);
  }
}

/**
 * 通过 Python 客户端创建发货跟进记录（回退方案）
 */
async function createShippingTrailViaPython(companyId, logisticsData) {
  const statusLabel = logisticsData.status || '待发货';
  const transportLabel = logisticsData.transportMode || '海运';
  
  const content = `📦 发货跟进\n` +
    `物流编号：${logisticsData.logisticsId}\n` +
    `订单编号：${logisticsData.orderId}\n` +
    `运输方式：${transportLabel}\n` +
    `发货状态：${statusLabel}\n` +
    `提单号：${logisticsData.billOfLading?.blNo || '(未指定)'}\n` +
    `船名/航次：${logisticsData.vesselName || '(未指定)'} ${logisticsData.voyageNo ? '(' + logisticsData.voyageNo + ')' : ''}\n` +
    `ETD (预计离港): ${logisticsData.etd || '(未指定)'}\n` +
    `ETA (预计到港): ${logisticsData.eta || '(未指定)'}\n` +
    `起运港：${logisticsData.portOfLoading || '(未指定)'}\n` +
    `目的港：${logisticsData.portOfDischarge || '(未指定)'}\n` +
    `货物总量：${logisticsData.cargoInfo?.totalQuantity || 0}\n` +
    `集装箱数：${logisticsData.containerInfo?.length || 0}\n` +
    `备注：${logisticsData.notes || '(无)'}`;
  
  try {
    // 创建临时 Python 脚本调用 OKKI 客户端
    const tempScript = `
import sys
sys.path.insert(0, '/Users/wilson/.openclaw/workspace/xiaoman-okki/api')
from okki_client import OKKIClient
import json

client = OKKIClient()
result = client.create_trail(
  company_id=${companyId},
  content='''${content.replace(/'/g, "\\'")}''',
  trail_type=${CONFIG.TRAIL_TYPE.SHIPPING}
)
print(json.dumps(result))
`.trim();
    
    const tempScriptPath = '/tmp/okki_trail_' + Date.now() + '.py';
    fs.writeFileSync(tempScriptPath, tempScript);
    
    const result = await execPython(tempScriptPath);
    
    // 清理临时文件
    try {
      fs.unlinkSync(tempScriptPath);
    } catch (e) {
      // 忽略清理失败
    }
    
    if (result.error) {
      throw new Error(result.error);
    }
    
    return {
      success: true,
      company_id: companyId,
      trail_id: result.trail_id || result.data?.trail_id,
      action: 'trail.add',
      trail_type: CONFIG.TRAIL_TYPE.SHIPPING
    };
  } catch (e) {
    console.error('Python 客户端创建跟进失败:', e.message);
    throw e;
  }
}

/**
 * 同步物流记录到 OKKI
 * @param {string} logisticsId - 物流 ID
 * @returns {Promise<{success: boolean, company_id?: string, trail_id?: string, error?: string}>}
 */
async function syncLogisticsToOKKI(logisticsId) {
  try {
    // 步骤 1: 获取物流记录详情
    const logisticsAPI = loadLogisticsAPI();
    if (!logisticsAPI) {
      throw new Error('无法加载物流 API 模块');
    }
    
    const logisticsData = await logisticsAPI.getLogisticsDetails(logisticsId);
    if (!logisticsData) {
      throw new Error(`物流记录 ${logisticsId} 未找到`);
    }
    
    // 步骤 2: 通过订单号查找客户公司
    const companyInfo = await findCompanyByOrderId(logisticsData.orderId);
    if (!companyInfo) {
      return {
        success: false,
        error: `未找到与订单 ${logisticsData.orderId} 关联的 OKKI 客户`,
        logistics_id: logisticsId,
        order_id: logisticsData.orderId
      };
    }
    
    // 步骤 3: 创建发货跟进记录
    const trailResult = await createShippingTrail(companyInfo.company_id, {
      ...logisticsData,
      customerName: companyInfo.name
    });
    
    // 步骤 4: 记录同步日志
    const syncLogModel = loadSyncLogModel();
    if (syncLogModel) {
      await syncLogModel.create({
        logistics_id: logisticsId,
        company_id: companyInfo.company_id,
        trail_id: trailResult.trail_id,
        sync_time: new Date().toISOString(),
        status: 'success',
        match_type: companyInfo.match_type
      });
    }
    
    return {
      success: true,
      company_id: companyInfo.company_id,
      company_name: companyInfo.name,
      trail_id: trailResult.trail_id,
      trail_type: CONFIG.TRAIL_TYPE.SHIPPING,
      logistics_id: logisticsId,
      order_id: logisticsData.orderId,
      match_type: companyInfo.match_type
    };
  } catch (e) {
    console.error('同步物流记录到 OKKI 失败:', e.message);
    
    // 记录错误日志
    const syncLogModel = loadSyncLogModel();
    if (syncLogModel) {
      await syncLogModel.create({
        logistics_id: logisticsId,
        sync_time: new Date().toISOString(),
        status: 'failed',
        error_message: e.message
      });
    }
    
    return {
      success: false,
      error: e.message,
      logistics_id: logisticsId
    };
  }
}

/**
 * 加载同步日志模型
 */
function loadSyncLogModel() {
  try {
    const syncLogModel = require('../models/okki_sync_log_model.js');
    return syncLogModel;
  } catch (error) {
    console.warn('加载同步日志模型失败:', error.message);
    return null;
  }
}

/**
 * 获取 OKKI 同步状态
 * @param {string} logisticsId - 物流 ID
 * @returns {Promise<object>}
 */
async function getOKKISyncStatus(logisticsId) {
  const syncLogModel = loadSyncLogModel();
  if (!syncLogModel) {
    return {
      success: false,
      error: '同步日志模型不可用'
    };
  }
  
  const logs = await syncLogModel.findByLogisticsId(logisticsId);
  if (!logs || logs.length === 0) {
    return {
      logistics_id: logisticsId,
      synced: false,
      message: '暂无同步记录'
    };
  }
  
  // 返回最新的同步记录
  const latestLog = logs[logs.length - 1];
  return {
    logistics_id: logisticsId,
    synced: latestLog.status === 'success',
    last_sync_time: latestLog.sync_time,
    last_status: latestLog.status,
    trail_id: latestLog.trail_id,
    company_id: latestLog.company_id,
    error_message: latestLog.error_message,
    sync_count: logs.length,
    history: logs
  };
}

module.exports = {
  syncLogisticsToOKKI,
  getOKKISyncStatus,
  findCompanyByOrderId,
  createShippingTrail,
  CONFIG
};
