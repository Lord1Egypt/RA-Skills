#!/usr/bin/env node
/**
 * RunningHub API Client
 * 直接复用 RHMCP 的 API 调用逻辑
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// 加载共享 APP 清单
function loadSharedApps() {
  const sharedAppsPath = join(__dirname, '../references/shared-apps.json');
  if (existsSync(sharedAppsPath)) {
    const content = readFileSync(sharedAppsPath, 'utf-8');
    return JSON.parse(content).apps || {};
  }
  return {};
}

// 加载用户配置
function loadUserConfig() {
  const configPath = join(process.env.HOME || '/root', '.openclaw/openclaw.json');
  if (existsSync(configPath)) {
    try {
      const content = readFileSync(configPath, 'utf-8');
      // 使用 JSON5 兼容的方式：先尝试直接解析，失败则清理注释
      let config;
      try {
        config = JSON.parse(content);
      } catch (e) {
        // 清理单行注释和多行注释
        const cleanContent = content
          .replace(/\/\/.*$/gm, '')
          .replace(/\/\*[\s\S]*?\*\//g, '');
        config = JSON.parse(cleanContent);
      }
      return config.skills?.entries?.['runninghub-api']?.config || {};
    } catch (e) {
      // 静默失败，使用默认配置
      console.error('[RH] 配置加载失败，使用默认配置');
    }
  }
  return {};
}

// RunningHub Client 类
export class RunningHubClient {
  constructor(apiKey, baseUrl, maxConcurrent = 1) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.maxConcurrent = maxConcurrent;
    this.activeRequests = 0;
    
    // 合并共享 APP 和用户自定义 APP
    this.sharedApps = loadSharedApps();
    this.userConfig = loadUserConfig();
    this.apps = { ...this.sharedApps, ...(this.userConfig.apps || {}) };
  }

  /**
   * 获取 APP 信息
   */
  async getAppInfo(webappId) {
    const url = `https://${this.baseUrl}/api/webapp/apiCallDemo?apiKey=${this.apiKey}&webappId=${webappId}`;
    const response = await fetch(url);
    return response.json();
  }

  /**
   * 上传文件
   */
  async uploadFile(fileBuffer, fileType) {
    const formData = new FormData();
    formData.append('apiKey', this.apiKey);
    formData.append('fileType', fileType);
    
    // 创建 Blob
    const blob = new Blob([fileBuffer]);
    formData.append('file', blob, 'upload');

    const response = await fetch(`https://${this.baseUrl}/task/openapi/upload`, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  }

  /**
   * 提交任务
   */
  async submitTask(webappId, nodeInfoList) {
    await this.acquireSlot();

    try {
      const response = await fetch(`https://${this.baseUrl}/task/openapi/ai-app/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          webappId,
          apiKey: this.apiKey,
          nodeInfoList,
        }),
      });
      return response.json();
    } finally {
      this.releaseSlot();
    }
  }

  /**
   * 查询任务
   */
  async queryTask(taskId) {
    const response = await fetch(`https://${this.baseUrl}/task/openapi/outputs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        apiKey: this.apiKey,
        taskId,
      }),
    });
    return response.json();
  }

  /**
   * 列出所有可用 APP
   */
  listApps() {
    return Object.entries(this.apps).map(([alias, app]) => ({
      alias,
      appId: app.appId,
      category: app.category,
      description: app.description,
    }));
  }

  /**
   * 根据别名获取 APP 配置
   */
  getAppByAlias(alias) {
    return this.apps[alias];
  }

  // 并发控制
  async acquireSlot() {
    while (this.activeRequests >= this.maxConcurrent) {
      await new Promise(r => setTimeout(r, 100));
    }
    this.activeRequests++;
  }

  releaseSlot() {
    this.activeRequests--;
  }
}

// 创建客户端实例（从环境变量）
export function createClientFromEnv() {
  const apiKey = process.env.RUNNINGHUB_API_KEY;
  const baseUrl = process.env.RUNNINGHUB_BASE_URL || 'www.runninghub.cn';
  
  if (!apiKey) {
    throw new Error('RUNNINGHUB_API_KEY environment variable is required');
  }
  
  return new RunningHubClient(apiKey, baseUrl);
}
