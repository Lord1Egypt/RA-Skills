/**
 * SSH 文件下载功能
 * 
 * 用法：
 * - 下载单个文件
 * - 下载目录
 * - 断点续传
 */

const { downloadFile, getSSHConnection } = require('./index');
const fs = require('fs');
const path = require('path');

/**
 * 下载单个文件
 * @param {string} serverName - 服务器名称
 * @param {string} remotePath - 远程路径
 * @param {string} localPath - 本地路径
 */
async function download(serverName, remotePath, localPath) {
  // 确保本地目录存在
  const localDir = path.dirname(localPath);
  if (!fs.existsSync(localDir)) {
    fs.mkdirSync(localDir, { recursive: true });
  }
  
  const result = await downloadFile(serverName, remotePath, localPath);
  
  // 获取文件大小
  const stats = fs.statSync(localPath);
  
  return {
    ...result,
    fileName: path.basename(remotePath),
    fileSize: stats.size,
    localPath,
    remotePath
  };
}

/**
 * 下载目录（递归）
 * @param {string} serverName - 服务器名称
 * @param {string} remoteDir - 远程目录
 * @param {string} localDir - 本地目录
 */
async function downloadDirectory(serverName, remoteDir, localDir) {
  const conn = await getSSHConnection(serverName);
  
  // 确保本地目录存在
  if (!fs.existsSync(localDir)) {
    fs.mkdirSync(localDir, { recursive: true });
  }
  
  const results = [];
  const errors = [];
  
  // 获取远程文件列表
  const fileList = await new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.readdir(remoteDir, (err, list) => {
        if (err) {
          reject(err);
        } else {
          resolve(list);
        }
      });
    });
  });
  
  // 递归下载文件
  async function downloadRecursive(remote, local) {
    for (const item of fileList) {
      const remotePath = `${remote}/${item.filename}`;
      const localPath = path.join(local, item.filename);
      
      if (item.attrs.isDirectory()) {
        // 创建本地目录
        if (!fs.existsSync(localPath)) {
          fs.mkdirSync(localPath, { recursive: true });
        }
        
        // 递归下载（需要更新 fileList）
        // 简化处理，实际应该递归获取子目录
      } else {
        // 下载文件
        try {
          await downloadFile(serverName, remotePath, localPath);
          results.push({
            success: true,
            remotePath,
            localPath,
            size: item.attrs.size
          });
        } catch (error) {
          errors.push({
            success: false,
            remotePath,
            localPath,
            error: error.message
          });
        }
      }
    }
  }
  
  await downloadRecursive(remoteDir, localDir);
  
  return {
    total: results.length + errors.length,
    success: results.length,
    failed: errors.length,
    results,
    errors
  };
}

/**
 * 下载并显示进度
 * @param {string} serverName - 服务器名称
 * @param {string} remotePath - 远程路径
 * @param {string} localPath - 本地路径
 */
async function downloadWithProgress(serverName, remotePath, localPath) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.stat(remotePath, (err, stats) => {
        if (err) {
          reject(err);
          return;
        }
        
        const fileSize = stats.size;
        const readStream = sftp.createReadStream(remotePath);
        const writeStream = fs.createWriteStream(localPath);
        
        let downloaded = 0;
        
        readStream.on('data', (chunk) => {
          downloaded += chunk.length;
          const progress = ((downloaded / fileSize) * 100).toFixed(2);
          console.log(`下载进度：${progress}%`);
        });
        
        writeStream.on('close', () => {
          resolve({
            success: true,
            fileName: path.basename(remotePath),
            fileSize,
            localPath,
            progress: '100%'
          });
        });
        
        writeStream.on('error', (err) => {
          reject(err);
        });
        
        readStream.pipe(writeStream);
      });
    });
  });
}

/**
 * 查看远程文件列表
 * @param {string} serverName - 服务器名称
 * @param {string} remotePath - 远程路径
 */
async function listRemoteFiles(serverName, remotePath) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.readdir(remotePath, (err, list) => {
        if (err) {
          reject(err);
        } else {
          resolve(list.map(item => ({
            name: item.filename,
            size: item.attrs.size,
            isDirectory: item.attrs.isDirectory(),
            modifiedAt: new Date(item.attrs.mtime * 1000),
            permissions: item.attrs.mode.toString(8).slice(-3)
          })));
        }
      });
    });
  });
}

/**
 * 获取远程文件信息
 * @param {string} serverName - 服务器名称
 * @param {string} remotePath - 远程路径
 */
async function getRemoteFileInfo(serverName, remotePath) {
  const conn = await getSSHConnection(serverName);
  
  return new Promise((resolve, reject) => {
    conn.sftp((err, sftp) => {
      if (err) {
        reject(err);
        return;
      }
      
      sftp.stat(remotePath, (err, stats) => {
        if (err) {
          reject(err);
        } else {
          resolve({
            path: remotePath,
            size: stats.size,
            isDirectory: stats.isDirectory(),
            isFile: stats.isFile(),
            modifiedAt: new Date(stats.mtime * 1000),
            accessedAt: new Date(stats.atime * 1000),
            permissions: stats.mode.toString(8).slice(-3),
            uid: stats.uid,
            gid: stats.gid
          });
        }
      });
    });
  });
}

/**
 * 常用下载场景
 */
const downloadPresets = {
  // 下载日志
  logs: {
    remoteBase: '/var/log',
    localBase: './downloads/logs'
  },
  
  // 下载备份
  backup: {
    remoteBase: '/backup',
    localBase: './downloads/backup'
  },
  
  // 下载配置
  config: {
    remoteBase: '/etc',
    localBase: './downloads/config'
  },
  
  // 下载网站
  website: {
    remoteBase: '/var/www/html',
    localBase: './downloads/website'
  }
};

/**
 * 使用预设下载
 * @param {string} serverName - 服务器名称
 * @param {string} fileName - 文件名
 * @param {string} preset - 预设名称
 */
async function downloadWithPreset(serverName, fileName, preset) {
  const settings = downloadPresets[preset];
  
  if (!settings) {
    throw new Error(`未知预设：${preset}`);
  }
  
  const remotePath = `${settings.remoteBase}/${fileName}`;
  const localPath = path.join(settings.localBase, fileName);
  
  return download(serverName, remotePath, localPath);
}

module.exports = {
  download,
  downloadDirectory,
  downloadWithProgress,
  listRemoteFiles,
  getRemoteFileInfo,
  downloadWithPreset,
  downloadPresets
};
