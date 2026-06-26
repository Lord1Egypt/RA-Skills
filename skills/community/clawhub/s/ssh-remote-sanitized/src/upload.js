/**
 * SSH 文件上传功能
 * 
 * 用法：
 * - 上传单个文件
 * - 上传目录
 * - 断点续传
 */

const { uploadFile, getSSHConnection } = require('./index');
const fs = require('fs');
const path = require('path');

/**
 * 上传单个文件
 * @param {string} serverName - 服务器名称
 * @param {string} localPath - 本地路径
 * @param {string} remotePath - 远程路径
 */
async function upload(serverName, localPath, remotePath) {
  // 检查本地文件是否存在
  if (!fs.existsSync(localPath)) {
    throw new Error(`本地文件不存在：${localPath}`);
  }
  
  const result = await uploadFile(serverName, localPath, remotePath);
  
  // 获取文件大小
  const stats = fs.statSync(localPath);
  
  return {
    ...result,
    fileName: path.basename(localPath),
    fileSize: stats.size,
    localPath,
    remotePath
  };
}

/**
 * 上传目录（递归）
 * @param {string} serverName - 服务器名称
 * @param {string} localDir - 本地目录
 * @param {string} remoteDir - 远程目录
 */
async function uploadDirectory(serverName, localDir, remoteDir) {
  const conn = await getSSHConnection(serverName);
  
  // 确保远程目录存在
  await new Promise((resolve, reject) => {
    conn.exec(`mkdir -p ${remoteDir}`, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
  
  const results = [];
  const errors = [];
  
  // 递归上传文件
  async function uploadRecursive(local, remote) {
    const items = fs.readdirSync(local);
    
    for (const item of items) {
      const localPath = path.join(local, item);
      const remotePath = `${remote}/${item}`;
      const stats = fs.statSync(localPath);
      
      if (stats.isDirectory()) {
        // 创建远程目录
        await new Promise((resolve, reject) => {
          conn.exec(`mkdir -p ${remotePath}`, (err) => {
            if (err) reject(err);
            else resolve();
          });
        });
        
        // 递归上传
        await uploadRecursive(localPath, remotePath);
      } else {
        // 上传文件
        try {
          await uploadFile(serverName, localPath, remotePath);
          results.push({
            success: true,
            localPath,
            remotePath,
            size: stats.size
          });
        } catch (error) {
          errors.push({
            success: false,
            localPath,
            remotePath,
            error: error.message
          });
        }
      }
    }
  }
  
  await uploadRecursive(localDir, remoteDir);
  
  return {
    total: results.length + errors.length,
    success: results.length,
    failed: errors.length,
    results,
    errors
  };
}

/**
 * 上传并显示进度
 * @param {string} serverName - 服务器名称
 * @param {string} localPath - 本地路径
 * @param {string} remotePath - 远程路径
 */
async function uploadWithProgress(serverName, localPath, remotePath) {
  const stats = fs.statSync(localPath);
  const fileSize = stats.size;
  
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      const readStream = fs.createReadStream(localPath);
      const writeStream = sftp.createWriteStream(remotePath);
      
      let uploaded = 0;
      
      readStream.on('data', (chunk) => {
        uploaded += chunk.length;
        const progress = ((uploaded / fileSize) * 100).toFixed(2);
        console.log(`上传进度：${progress}%`);
      });
      
      writeStream.on('close', () => {
        resolve({
          success: true,
          fileName: path.basename(localPath),
          fileSize,
          remotePath,
          progress: '100%'
        });
      });
      
      writeStream.on('error', (err) => {
        reject(err);
      });
      
      readStream.pipe(writeStream);
    });
  });
}

/**
 * 常用上传场景
 */
const uploadPresets = {
  // 上传网站文件
  website: {
    remoteBase: '/var/www/html',
    permissions: '755',
    owner: 'www-data:www-data'
  },
  
  // 上传脚本
  script: {
    remoteBase: '/usr/local/bin',
    permissions: '755',
    owner: 'root:root'
  },
  
  // 上传配置
  config: {
    remoteBase: '/etc',
    permissions: '644',
    owner: 'root:root'
  },
  
  // 上传备份
  backup: {
    remoteBase: '/backup',
    permissions: '600',
    owner: 'root:root'
  }
};

/**
 * 使用预设上传
 * @param {string} serverName - 服务器名称
 * @param {string} localPath - 本地路径
 * @param {string} preset - 预设名称
 * @param {string} fileName - 文件名
 */
async function uploadWithPreset(serverName, localPath, preset, fileName) {
  const settings = uploadPresets[preset];
  
  if (!settings) {
    throw new Error(`未知预设：${preset}`);
  }
  
  const remotePath = `${settings.remoteBase}/${fileName}`;
  
  // 上传文件
  await upload(serverName, localPath, remotePath);
  
  // 设置权限
  const conn = await getSSHConnection(serverName);
  await new Promise((resolve, reject) => {
    conn.exec(`chmod ${settings.permissions} ${remotePath}`, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
  
  // 设置所有者（需要 sudo）
  await new Promise((resolve, reject) => {
    conn.exec(`sudo chown ${settings.owner} ${remotePath}`, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
  
  return {
    success: true,
    remotePath,
    permissions: settings.permissions,
    owner: settings.owner
  };
}

module.exports = {
  upload,
  uploadDirectory,
  uploadWithProgress,
  uploadWithPreset,
  uploadPresets
};
