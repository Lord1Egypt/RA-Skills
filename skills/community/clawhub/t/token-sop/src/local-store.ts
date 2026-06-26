/**
 * Local Workflow Store - 保存和检索本地工作流
 * 
 * 功能：
 * - 保存成功的工作流到本地文件
 * - 按 intent + url 匹配本地工作流
 * - 优先级：本地 > 云端 > LLM
 */

import * as fs from "fs";
import * as path from "path";
import type { LobsterWorkflow } from "./types.js";

export interface LocalWorkflow {
  intent: string;
  url: string;
  workflow: LobsterWorkflow;
  createdAt: number;
  updatedAt: number;
  successCount: number;
  failureCount: number;
}

export interface LocalStoreConfig {
  storageDir: string;
  enabled: boolean;
}

const DEFAULT_STORAGE_DIR = path.join(process.env.HOME || "/root", ".openclaw", "workflows");

/**
 * 初始化本地存储目录
 */
export function initLocalStore(config: LocalStoreConfig): void {
  if (!config.enabled) return;
  
  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * 保存工作流到本地
 */
export function saveLocalWorkflow(
  config: LocalStoreConfig,
  intent: string,
  url: string,
  workflow: LobsterWorkflow
): void {
  if (!config.enabled) return;

  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  
  // 确保目录存在
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  const key = generateKey(intent, url);
  const filePath = path.join(dir, `${key}.json`);

  let existing: LocalWorkflow | null = null;
  if (fs.existsSync(filePath)) {
    try {
      existing = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    } catch {
      existing = null;
    }
  }

  const data: LocalWorkflow = {
    intent,
    url,
    workflow,
    createdAt: existing?.createdAt || Date.now(),
    updatedAt: Date.now(),
    successCount: (existing?.successCount || 0) + 1,
    failureCount: existing?.failureCount || 0,
  };

  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

/**
 * 从本地检索工作流
 */
export function findLocalWorkflow(
  config: LocalStoreConfig,
  intent: string,
  url: string
): LobsterWorkflow | null {
  if (!config.enabled) return null;

  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  
  // 精确匹配
  const exactKey = generateKey(intent, url);
  const exactPath = path.join(dir, `${exactKey}.json`);
  
  if (fs.existsSync(exactPath)) {
    try {
      const data: LocalWorkflow = JSON.parse(fs.readFileSync(exactPath, "utf-8"));
      return data.workflow;
    } catch {
      return null;
    }
  }

  // 模糊匹配 - 按 intent 前缀
  try {
    const files = fs.readdirSync(dir);
    const intentLower = intent.toLowerCase();
    
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      
      const filePath = path.join(dir, file);
      try {
        const data: LocalWorkflow = JSON.parse(fs.readFileSync(filePath, "utf-8"));
        if (data.intent.toLowerCase().includes(intentLower) || 
            intentLower.includes(data.intent.toLowerCase())) {
          return data.workflow;
        }
      } catch {
        continue;
      }
    }
  } catch {
    // 目录不存在
  }

  return null;
}

/**
 * 记录工作流失败
 */
export function recordLocalFailure(
  config: LocalStoreConfig,
  intent: string,
  url: string
): void {
  if (!config.enabled) return;

  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  const key = generateKey(intent, url);
  const filePath = path.join(dir, `${key}.json`);

  if (!fs.existsSync(filePath)) return;

  try {
    const data: LocalWorkflow = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    data.failureCount += 1;
    data.updatedAt = Date.now();
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  } catch {
    // 忽略错误
  }
}

/**
 * 列出所有本地工作流
 */
export function listLocalWorkflows(config: LocalStoreConfig): LocalWorkflow[] {
  if (!config.enabled) return [];

  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  const workflows: LocalWorkflow[] = [];

  if (!fs.existsSync(dir)) return workflows;

  try {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      if (!file.endsWith(".json")) continue;
      
      const filePath = path.join(dir, file);
      try {
        const data: LocalWorkflow = JSON.parse(fs.readFileSync(filePath, "utf-8"));
        workflows.push(data);
      } catch {
        continue;
      }
    }
  } catch {
    // 忽略错误
  }

  return workflows;
}

/**
 * 删除本地工作流
 */
export function deleteLocalWorkflow(
  config: LocalStoreConfig,
  intent: string,
  url: string
): boolean {
  if (!config.enabled) return false;

  const dir = config.storageDir || DEFAULT_STORAGE_DIR;
  const key = generateKey(intent, url);
  const filePath = path.join(dir, `${key}.json`);

  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
    return true;
  }

  return false;
}

/**
 * 生成唯一键名
 */
function generateKey(intent: string, url: string): string {
  const combined = `${intent}:${url}`;
  // 简单哈希
  let hash = 0;
  for (let i = 0; i < combined.length; i++) {
    const char = combined.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}
