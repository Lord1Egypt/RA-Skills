#!/usr/bin/env node
/**
 * 任务执行器
 * 支持同步/异步模式，自动轮询任务状态
 */

import { RunningHubClient, createClientFromEnv } from './rh-client.mjs';
import { processOutput } from './storage-handler.mjs';

/**
 * 执行 APP 任务
 * 
 * @param {Object} options
 * @param {string} options.alias - APP 别名
 * @param {Object} options.params - APP 参数
 * @param {string} options.storage - 存储模式
 * @param {string} options.zipMode - ZIP 处理方式
 * @param {string} options.cloudProvider - 云存储提供商
 * @param {string} options.projectName - 项目名称
 * @param {string} options.mode - 执行模式 (sync/async)
 * @param {number} options.timeout - 超时时间（秒）
 * @param {string} options.outputPath - 本地输出路径
 */
export async function executeApp(options) {
  const {
    alias,
    params = {},
    storage = 'auto',
    zipMode = 'extract',
    cloudProvider = 'baidu',
    projectName = 'rh_task',
    mode = 'sync',
    timeout = 300,
    outputPath = './output',
  } = options;

  // 创建客户端
  const client = createClientFromEnv();

  // 获取 APP 配置
  const appConfig = client.getAppByAlias(alias);
  if (!appConfig) {
    throw new Error(`未知的 APP 别名: ${alias}。可用 APP: ${client.listApps().map(a => a.alias).join(', ')}`);
  }

  // 构建 nodeInfoList
  const nodeInfoList = [];
  if (appConfig.inputs) {
    for (const [paramName, paramConfig] of Object.entries(appConfig.inputs)) {
      const value = params[paramName] ?? paramConfig.default;
      if (value !== undefined) {
        nodeInfoList.push({
          nodeId: paramConfig.nodeId,
          fieldName: paramConfig.fieldName,
          fieldValue: typeof value === 'object' ? JSON.stringify(value) : String(value),
        });
      }
    }
  }

  // 提交任务
  console.error(`[RH] 提交任务: ${alias} (appId: ${appConfig.appId})`);
  const submitResult = await client.submitTask(appConfig.appId, nodeInfoList);
  
  if (submitResult.code !== 0) {
    throw new Error(`提交任务失败: ${submitResult.msg}`);
  }

  const taskId = submitResult.data?.taskId;
  if (!taskId) {
    throw new Error('提交任务成功但未返回 taskId');
  }

  console.error(`[RH] 任务已提交: ${taskId}`);

  // 异步模式直接返回
  if (mode === 'async') {
    return {
      taskId,
      status: 'PENDING',
      message: '任务已提交，请使用 rh_query_task 查询结果',
    };
  }

  // 同步模式：轮询等待结果
  return await pollTask(client, taskId, {
    storage,
    zipMode,
    cloudProvider,
    projectName,
    timeout,
    outputPath,
  });
}

/**
 * 轮询任务状态
 */
async function pollTask(client, taskId, options) {
  const {
    storage,
    zipMode,
    cloudProvider,
    projectName,
    timeout = 300,
    outputPath,
  } = options;

  const startTime = Date.now();
  const maxWaitMs = timeout * 1000;
  const interval = 5000; // 5秒轮询一次
  let retries = 0;
  const maxRetries = 3;

  console.error(`[RH] 开始轮询任务: ${taskId} (超时: ${timeout}秒)`);

  while (Date.now() - startTime < maxWaitMs) {
    const result = await client.queryTask(taskId);
    console.error(`[RH] 任务状态: ${result.code} - ${result.msg}`);

    // 任务完成
    if (result.code === 0 && result.data) {
      console.error(`[RH] 任务完成，处理输出...`);
      
      // 处理每个输出文件
      const outputs = [];
      for (let i = 0; i < result.data.length; i++) {
        const output = result.data[i];
        if (output.fileUrl) {
          const processed = await processOutput({
            fileUrl: output.fileUrl,
            fileId: `${i + 1}`,
            storage,
            zipMode,
            taskId,
            projectName,
            outputPath,
            cloudProvider,
          });
          outputs.push({
            ...output,
            ...processed,
          });
        } else {
          outputs.push(output);
        }
      }

      return {
        taskId,
        status: 'SUCCESS',
        outputs,
        duration: Math.round((Date.now() - startTime) / 1000),
      };
    }

    // 任务失败
    if (result.code === 805) {
      throw new Error(`任务失败: ${JSON.stringify(result.data)}`);
    }

    // 任务排队或执行中，继续等待
    if (result.code === 804 || result.code === 813) {
      await sleep(interval);
      continue;
    }

    // 并发限制，重试
    if (result.code === 421 || result.code === 415) {
      if (retries < maxRetries) {
        retries++;
        console.error(`[RH] 并发限制，第 ${retries} 次重试...`);
        await sleep(interval);
        continue;
      }
      throw new Error(`并发限制，重试${maxRetries}次后仍失败`);
    }

    // 其他错误
    throw new Error(`查询任务失败: ${result.msg} (code: ${result.code})`);
  }

  // 超时
  throw new Error(`任务超时 (${timeout}秒)，任务ID: ${taskId}。请使用 rh_query_task 继续查询。`);
}

/**
 * 查询任务状态
 */
export async function queryTask(taskId) {
  const client = createClientFromEnv();
  const result = await client.queryTask(taskId);

  if (result.code !== 0) {
    return {
      taskId,
      status: 'ERROR',
      error: result.msg,
      code: result.code,
    };
  }

  // 判断状态
  let status = 'UNKNOWN';
  if (result.data && result.data.length > 0) {
    status = 'SUCCESS';
  } else if (result.code === 804 || result.code === 813) {
    status = 'RUNNING';
  } else if (result.code === 805) {
    status = 'FAILED';
  }

  return {
    taskId,
    status,
    outputs: result.data,
    code: result.code,
    msg: result.msg,
  };
}

/**
 * 列出可用 APP
 */
export function listApps() {
  const client = createClientFromEnv();
  return client.listApps();
}

/**
 * 上传媒体文件
 */
export async function uploadMedia(filePath, fileType) {
  const client = createClientFromEnv();
  const { readFileSync } = await import('fs');
  
  const fileBuffer = readFileSync(filePath);
  const result = await client.uploadFile(fileBuffer, fileType);
  
  if (result.code !== 0) {
    throw new Error(`上传失败: ${result.msg}`);
  }

  return {
    fileUrl: result.data?.fileName,
    fileName: result.data?.fileName,
  };
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// CLI 入口
if (import.meta.url === `file://${process.argv[1]}`) {
  const command = process.argv[2];
  
  try {
    switch (command) {
      case 'list':
        console.log(JSON.stringify(listApps(), null, 2));
        break;
      
      case 'execute':
        const executeOptions = JSON.parse(process.argv[3] || '{}');
        executeApp(executeOptions).then(result => {
          console.log(JSON.stringify(result, null, 2));
        });
        break;
      
      case 'query':
        const taskId = process.argv[3];
        queryTask(taskId).then(result => {
          console.log(JSON.stringify(result, null, 2));
        });
        break;
      
      default:
        console.error('Usage: task-executor.mjs <list|execute|query>');
        process.exit(1);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}
