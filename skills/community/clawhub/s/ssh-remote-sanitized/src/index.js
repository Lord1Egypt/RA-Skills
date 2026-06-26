/**
 * SSH Remote Skill - 主入口文件
 * 
 * SSH 远程服务器管理工具
 * 基于 ssh2 模块实现
 */

const { Client } = require('ssh2');
const fs = require('fs');
const path = require('path');

/**
 * SSH 连接池
 */
const connectionPool = new Map();

/**
 * 获取 SSH 配置
 */
function getSSHConfig() {
  // 从环境变量或配置文件读取
  const configPath = process.env.SSH_CONFIG_PATH || path.join(process.env.HOME || '', '.openclaw', 'skills', 'ssh-remote', 'configs', 'servers.json');
  
  let servers = [];
  
  if (fs.existsSync(configPath)) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    servers = config.servers || [];
  }
  
  // 也从环境变量读取单个服务器配置
  if (process.env.SSH_HOST) {
    servers.push({
      name: process.env.SSH_NAME || 'default',
      host: process.env.SSH_HOST,
      port: parseInt(process.env.SSH_PORT) || 22,
      username: process.env.SSH_USERNAME || 'root',
      password: process.env.SSH_PASSWORD,
      privateKeyPath: process.env.SSH_PRIVATE_KEY
    });
  }
  
  return servers;
}

/**
 * 创建 SSH 连接
 * @param {Object} config - SSH 连接配置
 */
function createSSHConnection(config) {
  return new Promise((resolve, reject) => {
    const conn = new Client();
    
    const connectionConfig = {
      host: config.host,
      port: config.port || 22,
      username: config.username,
      readyTimeout: 30000,
      keepaliveInterval: 10000
    };
    
    // 使用私钥或密码
    if (config.privateKeyPath && fs.existsSync(config.privateKeyPath)) {
      connectionConfig.privateKey = fs.readFileSync(config.privateKeyPath);
      if (config.passphrase) {
        connectionConfig.passphrase = config.passphrase;
      }
    } else if (config.password) {
      connectionConfig.password = config.password;
    }
    
    conn.on('ready', () => {
      resolve(conn);
    });
    
    conn.on('error', (err) => {
      reject(new Error(`SSH 连接失败：${err.message}`));
    });
    
    conn.on('close', () => {
      // 连接关闭时从池中移除
      if (config.name) {
        connectionPool.delete(config.name);
      }
    });
    
    conn.connect(connectionConfig);
  });
}

/**
 * 获取或创建 SSH 连接
 * @param {string} serverName - 服务器名称
 */
async function getSSHConnection(serverName) {
  // 检查连接池中是否已有连接
  if (connectionPool.has(serverName)) {
    const conn = connectionPool.get(serverName);
    if (conn._sock && conn._sock.readable) {
      return conn;
    }
    // 连接已失效，移除
    connectionPool.delete(serverName);
  }
  
  // 获取服务器配置
  const servers = getSSHConfig();
  const server = servers.find(s => s.name === serverName) || servers[0];
  
  if (!server) {
    throw new Error(`未找到服务器配置：${serverName}`);
  }
  
  // 创建新连接
  const conn = await createSSHConnection(server);
  
  // 存入连接池
  if (server.name) {
    connectionPool.set(server.name, conn);
  }
  
  return conn;
}

/**
 * 执行 SSH 命令
 * @param {string} serverName - 服务器名称
 * @param {string} command - 命令
 * @param {Object} options - 选项
 */
async function execSSH(serverName, command, options = {}) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.exec(command, options, (err, stream) => {
      if (err) {
        reject(err);
        return;
      }
      
      let stdout = '';
      let stderr = '';
      
      stream.on('close', (code, signal) => {
        resolve({
          code,
          signal,
          stdout,
          stderr,
          success: code === 0
        });
      });
      
      stream.on('data', (data) => {
        stdout += data.toString();
      });
      
      stream.stderr.on('data', (data) => {
        stderr += data.toString();
      });
    });
  });
}

/**
 * 上传文件
 * @param {string} serverName - 服务器名称
 * @param {string} localPath - 本地路径
 * @param {string} remotePath - 远程路径
 */
async function uploadFile(serverName, localPath, remotePath) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.fastPut(localPath, remotePath, (err) => {
        if (err) {
          reject(err);
        } else {
          resolve({ success: true, remotePath });
        }
      });
    });
  });
}

/**
 * 下载文件
 * @param {string} serverName - 服务器名称
 * @param {string} remotePath - 远程路径
 * @param {string} localPath - 本地路径
 */
async function downloadFile(serverName, remotePath, localPath) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.fastGet(remotePath, localPath, (err) => {
        if (err) {
          reject(err);
        } else {
          resolve({ success: true, localPath });
        }
      });
    });
  });
}

/**
 * 关闭所有连接
 */
function closeAllConnections() {
  for (const [name, conn] of connectionPool.entries()) {
    conn.end();
    connectionPool.delete(name);
  }
}

/**
 * 测试连接
 * @param {string} serverName - 服务器名称
 */
async function testConnection(serverName) {
  const startTime = Date.now();
  const conn = await getSSHConnection(serverName);
  const latency = Date.now() - startTime;
  
  // 获取服务器基本信息
  const result = await execSSH(serverName, 'uname -a');
  
  return {
    success: true,
    serverName,
    latency: `${latency}ms`,
    system: result.stdout.trim()
  };
}

module.exports = {
  getSSHConfig,
  createSSHConnection,
  getSSHConnection,
  execSSH,
  uploadFile,
  downloadFile,
  closeAllConnections,
  testConnection,
  connectionPool
};
