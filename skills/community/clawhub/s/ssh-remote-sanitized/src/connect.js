/**
 * SSH 连接管理功能
 * 
 * 用法：
 * - 连接测试
 * - 列出所有服务器
 * - 添加/删除服务器配置
 */

const { getSSHConfig, testConnection, closeAllConnections } = require('./index');
const fs = require('fs');
const path = require('path');

/**
 * 获取配置文件路径
 */
function getConfigPath() {
  return path.join(process.env.HOME || '', '.openclaw', 'skills', 'ssh-remote', 'configs', 'servers.json');
}

/**
 * 列出所有配置的服务器
 */
function listServers() {
  const servers = getSSHConfig();
  
  return servers.map(server => ({
    name: server.name,
    host: server.host,
    port: server.port,
    username: server.username,
    authType: server.privateKeyPath ? 'key' : 'password'
  }));
}

/**
 * 测试服务器连接
 * @param {string} serverName - 服务器名称
 */
async function testServer(serverName) {
  try {
    const result = await testConnection(serverName);
    return {
      success: true,
      message: '连接成功',
      ...result
    };
  } catch (error) {
    return {
      success: false,
      message: error.message
    };
  }
}

/**
 * 测试所有服务器连接
 */
async function testAllServers() {
  const servers = getSSHConfig();
  const results = [];
  
  for (const server of servers) {
    try {
      const result = await testConnection(server.name);
      results.push({
        name: server.name,
        host: server.host,
        status: 'online',
        latency: result.latency
      });
    } catch (error) {
      results.push({
        name: server.name,
        host: server.host,
        status: 'offline',
        error: error.message
      });
    }
  }
  
  return results;
}

/**
 * 添加服务器配置
 * @param {Object} serverConfig - 服务器配置
 */
function addServer(serverConfig) {
  const configPath = getConfigPath();
  let config = { servers: [] };
  
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  // 检查是否已存在
  const exists = config.servers.find(s => s.name === serverConfig.name);
  if (exists) {
    throw new Error(`服务器已存在：${serverConfig.name}`);
  }
  
  config.servers.push(serverConfig);
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  return { success: true, name: serverConfig.name };
}

/**
 * 更新服务器配置
 * @param {string} serverName - 服务器名称
 * @param {Object} config - 新配置
 */
function updateServer(serverName, config) {
  const configPath = getConfigPath();
  
  if (!fs.existsSync(configPath)) {
    throw new Error('配置文件不存在');
  }
  
  const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const index = data.servers.findIndex(s => s.name === serverName);
  
  if (index === -1) {
    throw new Error(`服务器不存在：${serverName}`);
  }
  
  data.servers[index] = { ...data.servers[index], ...config };
  fs.writeFileSync(configPath, JSON.stringify(data, null, 2));
  
  return { success: true, name: serverName };
}

/**
 * 删除服务器配置
 * @param {string} serverName - 服务器名称
 */
function removeServer(serverName) {
  const configPath = getConfigPath();
  
  if (!fs.existsSync(configPath)) {
    throw new Error('配置文件不存在');
  }
  
  const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const filtered = data.servers.filter(s => s.name !== serverName);
  
  if (filtered.length === data.servers.length) {
    throw new Error(`服务器不存在：${serverName}`);
  }
  
  data.servers = filtered;
  fs.writeFileSync(configPath, JSON.stringify(data, null, 2));
  
  return { success: true, name: serverName };
}

/**
 * 断开服务器连接
 * @param {string} serverName - 服务器名称
 */
function disconnectServer(serverName) {
  const { connectionPool } = require('./index');
  
  if (connectionPool.has(serverName)) {
    const conn = connectionPool.get(serverName);
    conn.end();
    connectionPool.delete(serverName);
    return { success: true, message: `已断开：${serverName}` };
  }
  
  return { success: false, message: `未找到连接：${serverName}` };
}

/**
 * 断开所有连接
 */
function disconnectAll() {
  closeAllConnections();
  return { success: true, message: '已断开所有连接' };
}

module.exports = {
  listServers,
  testServer,
  testAllServers,
  addServer,
  updateServer,
  removeServer,
  disconnectServer,
  disconnectAll
};
