#!/usr/bin/env node
/**
 * 存储处理模块
 * 支持 local/cloud/none/auto 四种模式
 */

import { mkdirSync, writeFileSync, existsSync, createWriteStream } from 'fs';
import { join, dirname } from 'path';
import { pipeline } from 'stream/promises';

/**
 * 下载文件到本地
 */
export async function downloadToFile(url, localPath) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`下载失败: ${response.status} ${response.statusText}`);
  }

  // 确保目录存在
  const dir = dirname(localPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  // 下载文件
  const buffer = await response.arrayBuffer();
  writeFileSync(localPath, Buffer.from(buffer));
  
  return localPath;
}

/**
 * 从 URL 提取文件扩展名
 */
function getFileExtension(url) {
  try {
    const urlObj = new URL(url);
    const pathname = urlObj.pathname;
    const ext = pathname.substring(pathname.lastIndexOf('.'));
    return ext || '.zip';
  } catch {
    return '.zip';
  }
}

/**
 * 生成文件名
 */
function generateFileName(taskId, fileId, projectName, ext) {
  const timestamp = Date.now();
  const safeProject = projectName ? projectName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_-]/g, '_') : 'rh';
  
  if (taskId) {
    return `${safeProject}_${timestamp}_${fileId}${ext}`;
  }
  return `${safeProject}_${timestamp}_${fileId}${ext}`;
}

/**
 * 解压 ZIP 文件
 */
export async function extractZip(zipPath, outputDir, projectName) {
  // 使用系统 unzip 命令
  const { execSync } = await import('child_process');
  
  const extractDir = join(outputDir, `${projectName || 'extracted'}_${Date.now()}`);
  mkdirSync(extractDir, { recursive: true });
  
  try {
    execSync(`unzip -o "${zipPath}" -d "${extractDir}"`, { stdio: 'pipe' });
    
    // 读取解压后的文件列表
    const { readdirSync, statSync } = await import('fs');
    const files = [];
    
    function scanDir(dir, baseDir = dir) {
      const items = readdirSync(dir);
      for (const item of items) {
        const fullPath = join(dir, item);
        const stat = statSync(fullPath);
        if (stat.isDirectory()) {
          scanDir(fullPath, baseDir);
        } else {
          files.push({
            name: item,
            path: fullPath,
            relativePath: fullPath.replace(baseDir + '/', ''),
            size: stat.size,
          });
        }
      }
    }
    
    scanDir(extractDir);
    return { extractDir, files };
  } catch (error) {
    throw new Error(`解压失败: ${error.message}`);
  }
}

/**
 * 处理输出文件
 * 
 * @param {Object} options
 * @param {string} options.fileUrl - RH 服务器文件 URL
 * @param {string} options.fileId - 文件标识
 * @param {string} options.storage - 存储模式 (none/local/cloud/auto)
 * @param {string} options.zipMode - ZIP 处理方式 (keep/extract)
 * @param {string} options.taskId - 任务 ID
 * @param {string} options.projectName - 项目名称
 * @param {string} options.outputPath - 本地输出路径
 * @param {string} options.cloudProvider - 云存储提供商
 * @returns {Promise<Object>} 处理结果
 */
export async function processOutput(options) {
  const {
    fileUrl,
    fileId = '1',
    storage = 'auto',
    zipMode = 'extract',
    taskId,
    projectName = 'rh_task',
    outputPath = './output',
    cloudProvider = 'baidu',
  } = options;

  const result = {
    originalUrl: fileUrl,
    storageMode: storage,
    localPath: null,
    cloudUrl: null,
    extractedFiles: null,
  };

  // 根据存储模式处理
  switch (storage) {
    case 'none':
      // 仅返回原始 URL
      return result;

    case 'local':
      // 下载到本地
      result.localPath = await downloadToLocal(fileUrl, fileId, taskId, projectName, outputPath);
      
      // 如果需要解压
      if (zipMode === 'extract' && result.localPath.endsWith('.zip')) {
        const extractResult = await extractZip(result.localPath, outputPath, projectName);
        result.extractedFiles = extractResult.files;
        result.extractDir = extractResult.extractDir;
      }
      return result;

    case 'cloud':
      // 先下载到临时目录，然后上传云盘
      const tempPath = await downloadToLocal(fileUrl, fileId, taskId, projectName, '/tmp/rh-temp');
      
      // 上传到云盘
      result.cloudUrl = await uploadToCloud(tempPath, cloudProvider, projectName);
      
      // 如果需要解压后上传
      if (zipMode === 'extract' && tempPath.endsWith('.zip')) {
        const extractResult = await extractZip(tempPath, '/tmp/rh-temp', projectName);
        // 上传解压后的文件
        const uploadedFiles = [];
        for (const file of extractResult.files) {
          const url = await uploadToCloud(file.path, cloudProvider, projectName);
          uploadedFiles.push({ ...file, cloudUrl: url });
        }
        result.extractedFiles = uploadedFiles;
      }
      return result;

    case 'auto':
    default:
      // 默认行为：返回 URL（由调用方决定后续处理）
      return result;
  }
}

/**
 * 下载到本地
 */
async function downloadToLocal(fileUrl, fileId, taskId, projectName, outputPath) {
  const ext = getFileExtension(fileUrl);
  const fileName = generateFileName(taskId, fileId, projectName, ext);
  const localPath = join(outputPath, fileName);
  
  await downloadToFile(fileUrl, localPath);
  return localPath;
}

/**
 * 上传到云盘
 */
async function uploadToCloud(filePath, provider, projectName) {
  const { execSync } = await import('child_process');
  const fileName = filePath.split('/').pop();
  
  if (provider === 'baidu' || provider === 'bdpan') {
    try {
      // 创建目录结构
      const remoteDir = `runninghub/${projectName || 'tasks'}`;
      try {
        execSync(`bdpan mkdir "${remoteDir}"`, { stdio: 'pipe' });
      } catch (e) {
        // 目录可能已存在，忽略错误
      }
      
      // 生成远程路径
      const timestamp = Date.now();
      const remotePath = `${remoteDir}/${timestamp}_${fileName}`;
      
      // 执行上传
      execSync(`bdpan upload "${filePath}" "${remotePath}"`, { 
        encoding: 'utf-8',
        stdio: 'pipe'
      });
      
      return `bdpan://${remotePath}`;
    } catch (error) {
      console.error('[RH] 上传到百度网盘失败:', error.message);
      throw error;
    }
  }
  
  if (provider === 'google' || provider === 'gog') {
    try {
      // 使用 gog 上传到 Google Drive
      const remoteDir = `RunningHub/${projectName || 'tasks'}`;
      
      // gog drive upload 需要文件夹 ID，这里简化处理
      // 实际使用时需要先创建或获取文件夹
      const result = execSync(`gog drive upload "${filePath}" --folder "${remoteDir}"`, {
        encoding: 'utf-8',
        stdio: 'pipe'
      });
      
      return `gdrive://${remoteDir}/${fileName}`;
    } catch (error) {
      console.error('[RH] 上传到 Google Drive 失败:', error.message);
      throw error;
    }
  }
  
  throw new Error(`[RH] 不支持的云存储提供商: ${provider}`);
}
