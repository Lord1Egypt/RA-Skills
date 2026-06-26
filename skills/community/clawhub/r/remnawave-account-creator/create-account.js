#!/usr/bin/env node

/**
 * Remnawave 账号创建脚本
 * 
 * 用法:
 * node create-account.js \
 *   --username jim_pc \
 *   --email jim@codeforce.tech \
 *   --device-limit 1 \
 *   --traffic-gb 100 \
 *   --traffic-reset WEEKLY \
 *   --expire-days 365 \
 *   --squad "Ops Debugging" \
 *   --cc crads@codeforce.tech
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// 配置文件路径
const CONFIG_DIR = path.join(__dirname, '../../config');
const ENV_FILE = path.join(__dirname, '../../.env');
const REMNAWAVE_CONFIG = path.join(CONFIG_DIR, 'remnawave.json');
const SQUADS_CONFIG = path.join(CONFIG_DIR, 'remnawave-squads.json');
const SMTP_CONFIG = path.join(CONFIG_DIR, 'smtp.json');
const LOG_SCRIPT = path.join(__dirname, 'log-creation.js');

// 从 .env 读取 Remnawave API Token
function getRemnawaveToken() {
  try {
    const envContent = fs.readFileSync(ENV_FILE, 'utf-8');
    const match = envContent.match(/^REMNAWAVE_API_TOKEN=(.*)$/m);
    if (match && match[1]) {
      return match[1].trim();
    }
    throw new Error('REMNAWAVE_API_TOKEN not found in .env');
  } catch (error) {
    console.error('❌ 读取 Remnawave API Token 失败:', error.message);
    console.error('   请确保 .env 文件存在且包含 REMNAWAVE_API_TOKEN');
    process.exit(1);
  }
}

// 解析命令行参数
const args = process.argv.slice(2);
const params = {
  username: null,
  email: null,
  deviceLimit: 1,
  trafficGb: 100,
  trafficReset: 'WEEKLY',
  expireDays: 365,
  squad: null,
  cc: null
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--username' && args[i + 1]) params.username = args[++i];
  else if (args[i] === '--email' && args[i + 1]) params.email = args[++i];
  else if (args[i] === '--device-limit' && args[i + 1]) params.deviceLimit = parseInt(args[++i]);
  else if (args[i] === '--traffic-gb' && args[i + 1]) params.trafficGb = parseInt(args[++i]);
  else if (args[i] === '--traffic-reset' && args[i + 1]) params.trafficReset = args[++i];
  else if (args[i] === '--expire-days' && args[i + 1]) params.expireDays = parseInt(args[++i]);
  else if (args[i] === '--squad' && args[i + 1]) params.squad = args[++i];
  else if (args[i] === '--cc' && args[i + 1]) params.cc = args[++i];
}

// 验证必填参数
if (!params.username || !params.email) {
  console.error('❌ 错误：缺少必填参数');
  console.error('用法：node create-account.js --username <用户名> --email <邮箱> [其他选项]');
  console.error('\n必填参数:');
  console.error('  --username    账号用户名');
  console.error('  --email       用户邮箱');
  console.error('\n可选参数:');
  console.error('  --device-limit    设备限制 (默认：1)');
  console.error('  --traffic-gb      流量限制 GB (默认：100)');
  console.error('  --traffic-reset   流量重置周期 (默认：WEEKLY)');
  console.error('  --expire-days     过期天数 (默认：365)');
  console.error('  --squad           内部分组名称');
  console.error('  --cc              邮件抄送地址');
  process.exit(1);
}

// 读取配置文件
function readConfig(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`❌ 读取配置文件失败：${filePath}`);
    console.error(error.message);
    process.exit(1);
  }
}

// 调用 Remnawave API
function callApi(method, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readConfig(REMNAWAVE_CONFIG);
    const apiToken = getRemnawaveToken(); // 从 .env 读取 Token
    const url = new URL(endpoint, remnawaveConfig.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: remnawaveConfig.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API 错误：${res.statusCode} - ${JSON.stringify(response)}`));
          }
        } catch (error) {
          reject(new Error(`解析响应失败：${responseData}`));
        }
      });
    });
    
    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    
    req.end();
  });
}

// 获取组 UUID（需要完整 UUID 格式）
function getSquadUuids(squadName) {
  if (!squadName) {
    // 默认分配到 Default-Squad
    return ["751440da-da97-4bc9-8a18-1074994189d1"];
  }
  
  const squadsConfig = readConfig(SQUADS_CONFIG);
  
  // 检查是否是完整的 UUID 格式（8-4-4-4-12 格式）
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (uuidRegex.test(squadName.trim())) {
    return [squadName.trim()];
  }
  
  // 从配置中查找
  const squadUuid = squadsConfig.squads[squadName.trim()];
  
  if (!squadUuid) {
    console.warn(`⚠️ 警告：找不到组 "${squadName}"，将分配到 Default-Squad`);
    return ["751440da-da97-4bc9-8a18-1074994189d1"];
  }
  
  // 如果配置的是短 UUID，需要补全为完整 UUID
  if (squadUuid.length < 36) {
    console.warn(`⚠️ 警告：组 UUID 格式不正确，需要完整 UUID 格式`);
    console.warn(`   当前：${squadUuid}`);
    console.warn(`   需要：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`);
    return ["751440da-da97-4bc9-8a18-1074994189d1"];
  }
  
  return [squadUuid];
}

// 获取所有用户（分页遍历）
async function getAllUsers() {
  let allUsers = [];
  let page = 1;
  let hasMore = true;
  
  while (hasMore) {
    const response = await callApi('GET', `/api/users?page=${page}&limit=500`);
    const users = response.response.users || [];
    allUsers = allUsers.concat(users);
    hasMore = users.length === 500;
    page++;
    
    // 安全限制，防止无限循环
    if (page > 20) {
      console.warn('⚠️  达到最大分页数 (20 页)');
      break;
    }
  }
  
  return allUsers;
}

// 检查用户是否存在（使用全局搜索）
async function checkUserExists(username) {
  try {
    // 优先使用 by-username 接口（最准确）
    try {
      const directResponse = await callApi('GET', `/api/users/by-username/${username}`);
      if (directResponse.response && directResponse.response.username === username) {
        return directResponse.response;
      }
    } catch (e) {
      // by-username 不存在，继续全局搜索
    }
    
    // 全局搜索所有用户
    const allUsers = await getAllUsers();
    return allUsers.find(u => u.username === username);
  } catch (error) {
    console.error('❌ checkUserExists 错误:', error.message);
    return null;
  }
}

// 删除用户
async function deleteUser(uuid) {
  return new Promise((resolve, reject) => {
    const remnawaveConfig = readConfig(REMNAWAVE_CONFIG);
    const url = new URL(`/api/users/${uuid}`, remnawaveConfig.apiBaseUrl);
    
    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname + url.search,
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${remnawaveConfig.apiToken}`,
        'Content-Type': 'application/json'
      },
      rejectUnauthorized: remnawaveConfig.sslRejectUnauthorized !== false
    };
    
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(responseData);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(response);
          } else {
            reject(new Error(`API 错误：${res.statusCode} - ${JSON.stringify(response)}`));
          }
        } catch (error) {
          reject(new Error(`解析响应失败：${responseData}`));
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

// 创建账号
async function createAccount() {
  console.log('🚀 开始创建 Remnawave 账号...\n');
  
  // 计算参数
  const trafficLimitBytes = params.trafficGb * 1024 * 1024 * 1024;
  const expireDate = new Date();
  expireDate.setDate(expireDate.getDate() + params.expireDays);
  const expireAt = expireDate.toISOString();
  
  const squadUuids = getSquadUuids(params.squad);
  
  // 流量重置策略映射
  const strategyMap = {
    'NO_RESET': 'NO_RESET',
    '不重置': 'NO_RESET',
    '每天': 'DAY',
    'DAILY': 'DAY',
    'DAY': 'DAY',
    '每周': 'WEEK',
    'WEEKLY': 'WEEK',
    'WEEK': 'WEEK',
    '每月': 'MONTH',
    'MONTHLY': 'MONTH',
    'MONTH': 'MONTH'
  };
  
  const trafficLimitStrategy = strategyMap[params.trafficReset?.toUpperCase()] || 'NO_RESET';
  
  const requestData = {
    username: params.username,
    email: params.email,
    hwidDeviceLimit: params.deviceLimit,
    trafficLimitBytes: trafficLimitBytes,
    trafficLimitStrategy: trafficLimitStrategy,
    expireAt: expireAt,
    activeInternalSquads: squadUuids  // ✅ 正确参数名
  };
  
  console.log('📋 账号信息:');
  console.log(`  用户名：${params.username}`);
  console.log(`  邮箱：${params.email}`);
  console.log(`  设备限制：${params.deviceLimit} 台`);
  console.log(`  流量限制：${params.trafficGb}GB`);
  console.log(`  流量重置：${params.trafficReset || 'NO_RESET'}`);
  console.log(`  过期时间：${expireDate.toISOString().split('T')[0]}`);
  if (params.squad) console.log(`  内部分组：${params.squad} ✅`);
  if (params.cc) console.log(`  邮件抄送：${params.cc}`);
  console.log('');
  
  // 检查用户是否已存在
  console.log('🔍 检查用户是否存在...');
  const existingUser = await checkUserExists(params.username);
  
  if (existingUser) {
    console.log(`⚠️  用户 ${params.username} 已存在！`);
    console.log(`   UUID: ${existingUser.uuid}`);
    console.log(`   邮箱：${existingUser.email}`);
    console.log(`   分组：${existingUser.activeInternalSquads?.[0]?.name || '未知'}`);
    console.log(`   状态：${existingUser.status}`);
    console.log('');
    
    // 检查是否需要删除重建（通过环境变量或参数控制）
    const forceRecreate = process.argv.includes('--force-recreate') || 
                          process.env.REMNAWAVE_FORCE_RECREATE === 'true';
    
    if (forceRecreate) {
      console.log('🔄 检测到 --force-recreate 参数，正在删除旧账号...');
      try {
        await deleteUser(existingUser.uuid);
        console.log(`✅ 已删除旧用户 (UUID: ${existingUser.uuid})`);
        // 等待 API 缓存刷新
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(`❌ 删除失败：${error.message}`);
        console.error('请手动删除后重试');
        process.exit(1);
      }
    } else {
      console.error('❌ 停止创建');
      console.error('');
      console.error('💡 解决方案:');
      console.error('   1. 使用新用户名（推荐）');
      console.error('   2. 或添加 --force-recreate 参数强制删除重建');
      console.error('   3. 或在 Remnawave 后台手动删除旧账号');
      console.error('');
      console.error('📋 命令行示例:');
      console.error(`   node create-account.js --username ${params.username} --email ${params.email} --force-recreate`);
      process.exit(1);
    }
  } else {
    console.log('✅ 用户不存在，可以创建');
  }
  console.log('');
  
  let account = null;
  let emailSent = false;
  let messageId = null;
  let errorMessage = null;
  
  try {
    // 调用 API 创建账号
    console.log('📡 调用 Remnawave API...');
    let response;
    try {
      response = await callApi('POST', '/api/users', requestData);
    } catch (createError) {
      // 如果创建失败且错误是"用户已存在"，尝试自动删除后重试
      if (createError.message.includes('User username already exists')) {
        console.log('⚠️  检测到用户已存在但搜索不到，尝试强制删除...');
        
        // 尝试通过用户名获取用户 UUID
        const usersResponse = await callApi('GET', '/api/users?limit=500');
        const allUsers = usersResponse.response.users || [];
        const existingUser = allUsers.find(u => u.username === params.username);
        
        if (existingUser) {
          console.log(`🔍 找到旧用户：${existingUser.uuid}`);
          await deleteUser(existingUser.uuid);
          console.log(`✅ 已删除旧用户`);
          await new Promise(resolve => setTimeout(resolve, 2000)); // 等待 2 秒
          
          // 重试创建
          console.log('🔄 重试创建...');
          response = await callApi('POST', '/api/users', requestData);
        } else {
          // 搜索不到但 API 说存在，尝试遍历所有用户（包括已删除）
          console.log('⚠️  搜索接口找不到，尝试分页遍历所有用户...');
          let allUsers = [];
          let page = 1;
          let hasMore = true;
          
          while (hasMore) {
            const pageResponse = await callApi('GET', `/api/users?page=${page}&limit=500`);
            const users = pageResponse.response.users || [];
            allUsers = allUsers.concat(users);
            hasMore = users.length === 500;
            page++;
          }
          
          const foundUser = allUsers.find(u => u.username === params.username);
          if (foundUser) {
            console.log(`🔍 分页遍历找到旧用户：${foundUser.uuid}`);
            await deleteUser(foundUser.uuid);
            console.log(`✅ 已删除旧用户`);
            await new Promise(resolve => setTimeout(resolve, 3000)); // 等待 3 秒
            console.log('🔄 重试创建...');
            response = await callApi('POST', '/api/users', requestData);
          } else {
            console.error('❌ 遍历所有用户也找不到，可能是 Remnawave 用户名保留机制');
            console.error('💡 解决方案：使用替代用户名（如 lucky2_pc）或管理后台手动删除');
            throw new Error('用户已存在但无法找到 UUID，请手动删除或使用其他用户名');
          }
        }
      } else {
        throw createError;
      }
    }
    
    account = response.response;
    console.log('✅ 账号创建成功!\n');
    
    console.log('📋 账号详情:');
    console.log(`  UUID: ${account.uuid}`);
    console.log(`  短 UUID: ${account.shortUuid}`);
    console.log(`  状态：${account.status}`);
    console.log(`  订阅地址：${account.subscriptionUrl}`);
    console.log('');
    
    // 发送邮件
    console.log('📧 准备发送开通邮件...');
    const emailResult = await sendEmail(account);
    emailSent = emailResult.sent;
    messageId = emailResult.messageId;
    
    console.log('\n✅ 全部完成!\n');
    
    // 记录日志
    await logCreation('success', account, emailSent, messageId);
    
    return account;
    
  } catch (error) {
    errorMessage = error.message;
    console.error('❌ 创建账号失败:', error.message);
    
    // 记录失败日志
    if (!account) {
      await logCreation('failed', null, false, null, errorMessage);
    }
    
    process.exit(1);
  }
}

// 发送邮件
async function sendEmail(account) {
  const sendEmailScript = path.join(CONFIG_DIR, 'send-template-email.js');
  const tutorialUrl = 'https://rjdx19yd9zo.sg.larksuite.com/docx/EwMLdN3asoQ44FxOlN6lQ6frgdh?from=from_copylink';
  const downloadUrl = 'https://v2raytun.com/';
  const downloadBackup = 'https://testappdownload-bydtmscom.oss-cn-hongkong.aliyuncs.com/OPSFILE/v2RayTun_Setup.zip';
  const appstoreUrl = 'https://apps.apple.com/us/app/v2raytun/id6476628951';
  const sendDate = new Date().toISOString().split('T')[0];
  
  const vars = {
    recipient_name: params.username,
    recipient_email: params.email,
    account_name: params.username,
    subscription_url: account.subscriptionUrl,
    tutorial_url: tutorialUrl,
    download_url: downloadUrl,
    download_backup: downloadBackup,
    appstore_url: appstoreUrl,
    send_date: sendDate
  };
  
  let command = `node "${sendEmailScript}"`;
  command += ` --to "${params.email}"`;
  command += ` --template remnawave-account-created`;
  command += ` --vars '${JSON.stringify(vars)}'`;
  
  if (params.cc) {
    command += ` --cc "${params.cc}"`;
  }
  
  try {
    const { stdout, stderr } = await execPromise(command);
    console.log(stdout);
    if (stderr) console.error(stderr);
    
    // 提取 Message ID
    let messageId = null;
    const messageIdMatch = stdout.match(/Message ID: <([^>]+)>/);
    if (messageIdMatch) {
      messageId = messageIdMatch[1];
    }
    
    return { sent: true, messageId };
  } catch (error) {
    console.error('❌ 邮件发送失败:', error.message);
    if (error.stdout) console.log(error.stdout);
    if (error.stderr) console.error(error.stderr);
    return { sent: false, messageId: null };
  }
}

// 记录创建日志
async function logCreation(status, account, emailSent, messageId, errorMessage = null) {
  let command = `node "${LOG_SCRIPT}"`;
  command += ` --username "${params.username}"`;
  command += ` --email "${params.email}"`;
  command += ` --status "${status}"`;
  
  if (params.squad) command += ` --squad "${params.squad}"`;
  if (params.deviceLimit) command += ` --device-limit ${params.deviceLimit}`;
  if (params.trafficGb) command += ` --traffic-gb ${params.trafficGb}`;
  if (params.trafficReset) command += ` --traffic-reset "${params.trafficReset}"`;
  if (params.expireDays) command += ` --expire-days ${params.expireDays}`;
  if (params.cc) command += ` --cc "${params.cc}"`;
  
  if (account) {
    command += ` --uuid "${account.uuid}"`;
    command += ` --short-uuid "${account.shortUuid}"`;
    command += ` --subscription-url "${account.subscriptionUrl}"`;
  }
  
  command += ` --email-sent ${emailSent}`;
  
  if (messageId) {
    command += ` --message-id "${messageId}"`;
  }
  
  if (errorMessage) {
    command += ` --error-message "${errorMessage}"`;
  }
  
  try {
    const { stdout } = await execPromise(command);
    console.log(stdout);
  } catch (error) {
    console.error('⚠️  日志记录失败:', error.message);
  }
}

// 主函数
createAccount();
