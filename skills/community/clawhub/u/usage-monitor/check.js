#!/usr/bin/env node

/**
 * Usage Monitor - 通用用量监控脚本
 * 
 * 特性:
 * - 用户自定义面板 URL
 * - 用户自定义告警阈值
 * - 支持多维度用量监控
 * 
 * 配置:
 * 复制 config.example.json 为 config.json 并填写你的配置
 */

const path = require('path');
const fs = require('fs');

// 脚本目录
const SCRIPT_DIR = __dirname;

// 配置文件路径
const CONFIG_PATH = path.join(SCRIPT_DIR, 'config.json');
const CONFIG_EXAMPLE_PATH = path.join(SCRIPT_DIR, 'config.example.json');
const USAGE_LOG_PATH = path.join(SCRIPT_DIR, 'usage-log.md');

// 默认配置
const DEFAULT_CONFIG = {
  panelUrl: 'https://example.com/usage',
  alertThreshold: 80,
  serviceName: '服务',
  checkIntervalHours: 4,
  remainingDays: 30,
};

/**
 * 加载用户配置
 * @returns {Object} 配置对象
 */
function loadConfig() {
  // 检查配置文件是否存在
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在！');
    console.error('');
    console.error('请复制 config.example.json 为 config.json 并填写配置：');
    console.error('');
    console.error(`  cp "${CONFIG_EXAMPLE_PATH}" "${CONFIG_PATH}"`);
    console.error('');
    console.error('然后编辑 config.json，填写你的：');
    console.error('  - panelUrl: 用量面板页面 URL');
    console.error('  - alertThreshold: 告警阈值百分比 (1-100)');
    console.error('');
    process.exit(1);
  }

  try {
    const configContent = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const config = JSON.parse(configContent);
    
    // 合并默认配置
    return { ...DEFAULT_CONFIG, ...config };
  } catch (e) {
    console.error('❌ 配置文件解析失败！');
    console.error(`错误信息：${e.message}`);
    console.error('');
    console.error('请检查 config.json 格式是否正确。');
    process.exit(1);
  }
}

/**
 * 验证配置
 * @param {Object} config 配置对象
 * @returns {boolean} 是否有效
 */
function validateConfig(config) {
  const errors = [];

  // 验证 URL
  if (!config.panelUrl || typeof config.panelUrl !== 'string') {
    errors.push('panelUrl 必须是有效的字符串');
  } else if (!config.panelUrl.startsWith('http://') && !config.panelUrl.startsWith('https://')) {
    errors.push('panelUrl 必须以 http:// 或 https:// 开头');
  }

  // 验证阈值
  if (typeof config.alertThreshold !== 'number') {
    errors.push('alertThreshold 必须是数字');
  } else if (config.alertThreshold < 1 || config.alertThreshold > 100) {
    errors.push('alertThreshold 必须在 1-100 之间');
  }

  // 验证检查间隔
  if (typeof config.checkIntervalHours !== 'number') {
    errors.push('checkIntervalHours 必须是数字');
  } else if (config.checkIntervalHours < 1 || config.checkIntervalHours > 24) {
    errors.push('checkIntervalHours 必须在 1-24 之间');
  }

  if (errors.length > 0) {
    console.error('❌ 配置验证失败：');
    errors.forEach(err => console.error(`  - ${err}`));
    console.error('');
    console.error('请参考 config.example.json 修正配置。');
    return false;
  }

  return true;
}

/**
 * 读取用量日志
 * @returns {string} 日志内容
 */
function readUsageLog() {
  try {
    if (fs.existsSync(USAGE_LOG_PATH)) {
      return fs.readFileSync(USAGE_LOG_PATH, 'utf-8');
    }
  } catch (e) {
    // 忽略读取错误
  }
  return '';
}

/**
 * 更新用量日志
 * @param {Object} data 用量数据
 */
function updateUsageLog(data) {
  const today = new Date().toISOString().split('T')[0];
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  
  let log = readUsageLog();
  
  if (!log) {
    // 创建新日志
    log = `# Usage Log

## Current Status (Last Updated: ${timestamp})

### Service Info
- **Service:** ${data.serviceName}
- **Status:** 正常
- **Remaining Days:** ${data.remainingDays}
- **Alert Threshold:** ${data.threshold}%

### Usage Tracking

| Date | Current | Notes |
|------|---------|-------|
| ${today} | ${data.current}% | Auto-check |

### Panel URL
${data.panelUrl}

---

## Monitoring Setup

- **Check Frequency:** Every ${data.checkIntervalHours} hours
- **Last Check:** ${timestamp}
`;
    fs.writeFileSync(USAGE_LOG_PATH, log);
    return;
  }
  
  // 添加新记录到表格
  const newLine = `| ${today} | ${data.current}% | Auto-check |`;
  
  if (!log.includes(`| ${today} |`)) {
    const tableRegex = /(\| Date \| Current \| Notes \|\n\|------\|---------\|-------\|)/;
    if (tableRegex.test(log)) {
      log = log.replace(tableRegex, `$1\n${newLine}`);
    }
  }
  
  // 更新最后检查时间
  log = log.replace(/Last Check:.*$/, `Last Check: ${timestamp}`);
  
  fs.writeFileSync(USAGE_LOG_PATH, log);
}

/**
 * 创建告警消息
 * @param {Object} data 用量数据
 * @returns {string} 告警消息
 */
function createAlertMessage(data) {
  return `⚠️ 服务使用量提醒

📊 服务：${data.serviceName}
📈 当前用量：${data.current}%
📈 可用额度：${100 - data.current}%
⏰ 剩余天数：${data.remainingDays} 天
🔗 查看：${data.panelUrl}

当前用量已达告警阈值（${data.threshold}%），请及时关注用量或考虑增加额度。`;
}

/**
 * 检查用量并返回结果
 * @param {Object} usageData 用量数据
 * @param {Object} config 配置
 * @returns {Object} 检查结果
 */
function checkUsage(usageData, config) {
  console.log('🔍 开始检查服务使用量...');
  console.log(`📋 告警阈值：${config.alertThreshold}%`);
  console.log(`📊 当前用量：${usageData.current}%`);
  console.log('');
  
  const alerts = [];
  
  if (usageData.current >= config.alertThreshold) {
    alerts.push(`当前用量已达 ${usageData.current}%`);
  }
  
  if (alerts.length > 0) {
    console.log('⚠️  触发告警：' + alerts.join(', '));
    return {
      alert: true,
      message: createAlertMessage({ 
        ...usageData, 
        threshold: config.alertThreshold,
        serviceName: config.serviceName,
        panelUrl: config.panelUrl,
        remainingDays: config.remainingDays,
      }),
      alerts,
    };
  } else {
    console.log('✅ 用量正常，未触发告警');
    return {
      alert: false,
      message: null,
      alerts: [],
    };
  }
}

/**
 * 显示使用说明
 */
function showUsage() {
  console.log('📝 使用流程（OpenClaw）:');
  console.log('');
  console.log('1. 配置参数:');
  console.log('   cp config.example.json config.json');
  console.log('   编辑 config.json，填写你的 URL 和阈值');
  console.log('');
  console.log('2. 通过 browser 工具访问用量面板页面:');
  console.log('   browser.open(config.panelUrl)');
  console.log('   browser.snapshot()');
  console.log('');
  console.log('3. 解析快照中的用量百分比数据');
  console.log('');
  console.log('4. 检查是否触发告警:');
  console.log('   const result = checkUsage(');
  console.log('     { current: 85 },');
  console.log('     config');
  console.log('   )');
  console.log('');
  console.log('5. 如有告警，发送消息:');
  console.log('   if (result.alert) {');
  console.log('     message.send(result.message)');
  console.log('   }');
  console.log('');
  console.log('6. 更新用量日志:');
  console.log('   updateUsageLog({');
  console.log('     current: 85,');
  console.log('     serviceName: config.serviceName,');
  console.log('     threshold: config.alertThreshold,');
  console.log('     panelUrl: config.panelUrl,');
  console.log('     checkIntervalHours: config.checkIntervalHours,');
  console.log('     remainingDays: config.remainingDays,');
  console.log('   })');
  console.log('');
}

/**
 * 主函数
 */
async function main() {
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║          Usage Monitor - 通用用量监控工具              ║');
  console.log('╚════════════════════════════════════════════════════════╝');
  console.log('');
  
  // 加载配置
  const config = loadConfig();
  
  // 验证配置
  if (!validateConfig(config)) {
    process.exit(1);
  }
  
  console.log('✅ 配置加载成功！');
  console.log('');
  console.log('📋 当前配置:');
  console.log(`   用量面板 URL: ${config.panelUrl}`);
  console.log(`   告警阈值：${config.alertThreshold}%`);
  console.log(`   服务名称：${config.serviceName}`);
  console.log(`   检查间隔：每 ${config.checkIntervalHours} 小时`);
  console.log(`   剩余天数：${config.remainingDays} 天`);
  console.log('');
  
  // 显示使用说明
  showUsage();
  
  return {
    status: 'ready',
    message: '监控脚本已就绪，请按照上述流程使用',
    config: config,
  };
}

// 导出函数供外部调用
module.exports = { 
  loadConfig,
  validateConfig,
  checkUsage, 
  createAlertMessage, 
  updateUsageLog,
  showUsage,
  DEFAULT_CONFIG,
};

// 如果直接运行则执行 main
if (require.main === module) {
  main().catch(console.error);
}
